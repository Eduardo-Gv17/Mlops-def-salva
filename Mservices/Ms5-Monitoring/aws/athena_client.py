import os
import time
import boto3
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def get_athena_client():
    """Crea cliente boto3 para Athena con credenciales del entorno."""
    return boto3.client(
        "athena",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN")
    )

ATHENA_DB      = os.getenv("ATHENA_DATABASE", "mlops_analytics")
ATHENA_OUTPUT  = os.getenv("ATHENA_OUTPUT_LOCATION", "s3://mlops-analytics-oswaldoaqm/athena-results/")

def run_query(sql: str, timeout: int = 60) -> list[dict]:
    client = get_athena_client()

    response = client.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={"Database": ATHENA_DB},
        ResultConfiguration={"OutputLocation": ATHENA_OUTPUT}
    )
    execution_id = response["QueryExecutionId"]
    logger.info(f"Query iniciada: {execution_id}")

    start = time.time()
    while True:
        status_resp = client.get_query_execution(QueryExecutionId=execution_id)
        state = status_resp["QueryExecution"]["Status"]["State"]

        if state == "SUCCEEDED":
            break
        elif state in ("FAILED", "CANCELLED"):
            reason = status_resp["QueryExecution"]["Status"].get("StateChangeReason", "Sin detalle")
            raise RuntimeError(f"Athena query {state}: {reason}")

        if time.time() - start > timeout:
            raise TimeoutError(f"Query excedió timeout de {timeout}s")

        time.sleep(2)

    results_resp = client.get_query_results(QueryExecutionId=execution_id)
    rows = results_resp["ResultSet"]["Rows"]

    if len(rows) < 2:
        return []

    headers = [col.get("VarCharValue", "") for col in rows[0]["Data"]]
    records = []
    for row in rows[1:]:
        values = [cell.get("VarCharValue", None) for cell in row["Data"]]
        records.append(dict(zip(headers, values)))

    return records

def check_connectivity() -> bool:
    """Verifica que Athena responde correctamente."""
    try:
        run_query("SELECT 1 AS ping", timeout=15)
        return True
    except Exception as e:
        logger.warning(f"Athena no disponible: {e}")
        return False
