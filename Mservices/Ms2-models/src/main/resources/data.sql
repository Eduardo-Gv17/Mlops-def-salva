-- ════════════════════════════════════════════════════
--  data.sql — Seed automático de Ms2-models
--  Se ejecuta solo si las tablas están vacías
-- ════════════════════════════════════════════════════

-- Solo insertamos si no hay datos
INSERT INTO modelos (nombre, framework, version, descripcion, activo, created_at)
SELECT * FROM (
  SELECT 'churn_predictor_v1', 'pytorch', '1.0.0', 'Modelo de predicción de abandono bancario', TRUE, NOW() UNION ALL
  SELECT 'churn_predictor_v2', 'pytorch', '2.0.0', 'Modelo mejorado de predicción de abandono', TRUE, NOW() UNION ALL
  SELECT 'fraud_detector_v1', 'tensorflow', '1.0.0', 'Detector de fraude en transacciones', TRUE, NOW() UNION ALL
  SELECT 'fraud_detector_v2', 'tensorflow', '2.1.0', 'Detector de fraude mejorado con LSTM', TRUE, NOW() UNION ALL
  SELECT 'credit_scoring_v1', 'sklearn', '1.0.0', 'Modelo de scoring crediticio', TRUE, NOW() UNION ALL
  SELECT 'credit_scoring_v2', 'xgboost', '1.0.0', 'Scoring crediticio con XGBoost', TRUE, NOW() UNION ALL
  SELECT 'demand_forecast_v1', 'lightgbm', '1.0.0', 'Pronóstico de demanda retail', TRUE, NOW() UNION ALL
  SELECT 'demand_forecast_v2', 'pytorch', '1.0.0', 'Pronóstico de demanda con LSTM', TRUE, NOW() UNION ALL
  SELECT 'sentiment_analyzer_v1', 'tensorflow', '1.0.0', 'Análisis de sentimiento de reseñas', TRUE, NOW() UNION ALL
  SELECT 'price_optimizer_v1', 'xgboost', '1.0.0', 'Optimización de precios dinámicos', TRUE, NOW()
) AS tmp WHERE NOT EXISTS (SELECT 1 FROM modelos LIMIT 1);
