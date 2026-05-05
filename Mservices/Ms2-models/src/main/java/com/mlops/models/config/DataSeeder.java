package com.mlops.models.config;

import com.mlops.models.model.Metrica;
import com.mlops.models.model.Modelo;
import com.mlops.models.repository.MetricaRepository;
import com.mlops.models.repository.ModeloRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Slf4j
@Component
@RequiredArgsConstructor
public class DataSeeder implements CommandLineRunner {

    private final ModeloRepository modeloRepository;
    private final MetricaRepository metricaRepository;

    private static final String[] FRAMEWORKS = {"pytorch", "tensorflow", "sklearn", "xgboost", "lightgbm"};
    private static final String[] TIPOS_MODELO = {
        "churn_predictor", "fraud_detector", "credit_scoring", "demand_forecast",
        "sentiment_analyzer", "price_optimizer", "customer_segment", "anomaly_detector",
        "recommendation_engine", "nlp_classifier"
    };
    private static final String[] METRICAS = {"accuracy", "precision", "recall", "f1", "auc_roc", "rmse", "mae"};
    private static final String[] DATASETS = {
        "customer_churn_2024", "fraud_transactions_2024", "credit_history_2023",
        "retail_sales_2024", "product_reviews_2024", "market_prices_2024"
    };

    private final Random rand = new Random(42);

    @Override
    public void run(String... args) {
        if (modeloRepository.count() > 10) {
            log.info("✅ Seed ya ejecutado. Modelos: {}, Métricas: {}", modeloRepository.count(), metricaRepository.count());
            return;
        }

        log.info("🌱 Iniciando seed masivo de Ms2-models...");

        // Crear 500 modelos
        List<Modelo> modelos = new ArrayList<>();
        for (int i = 1; i <= 500; i++) {
            Modelo m = new Modelo();
            String tipo = TIPOS_MODELO[rand.nextInt(TIPOS_MODELO.length)];
            String framework = FRAMEWORKS[rand.nextInt(FRAMEWORKS.length)];
            m.setNombre(tipo + "_" + framework + "_" + String.format("%04d", i));
            m.setFramework(framework);
            m.setVersion(String.format("%d.%d.%d", rand.nextInt(3) + 1, rand.nextInt(5), rand.nextInt(10)));
            m.setDescripcion("Modelo de " + tipo + " usando " + framework + " - instancia " + i);
            m.setActivo(rand.nextFloat() > 0.15f);
            modelos.add(m);
        }
        List<Modelo> savedModelos = modeloRepository.saveAll(modelos);
        log.info("✅ {} modelos creados", savedModelos.size());

        // Crear 40 métricas por modelo = 20,000 total
        List<Metrica> batch = new ArrayList<>();
        int totalMetricas = 0;
        for (Modelo modelo : savedModelos) {
            for (int j = 0; j < 40; j++) {
                Metrica met = new Metrica();
                String tipoMetrica = METRICAS[rand.nextInt(METRICAS.length)];
                met.setTipoMetrica(tipoMetrica);
                double valor = switch (tipoMetrica) {
                    case "accuracy", "precision", "recall", "f1", "auc_roc" -> 0.5 + rand.nextDouble() * 0.49;
                    default -> rand.nextDouble() * 2.0;  // rmse, mae
                };
                met.setValorMetrica(BigDecimal.valueOf(valor).setScale(6, RoundingMode.HALF_UP));
                met.setDatasetEvaluacion(DATASETS[rand.nextInt(DATASETS.length)]);
                met.setNotas("Evaluación " + j + " del modelo " + modelo.getNombre());
                met.setModelo(modelo);
                batch.add(met);
            }
            if (batch.size() >= 2000) {
                metricaRepository.saveAll(batch);
                totalMetricas += batch.size();
                batch.clear();
                log.info("  → {} métricas insertadas...", totalMetricas);
            }
        }
        if (!batch.isEmpty()) {
            metricaRepository.saveAll(batch);
            totalMetricas += batch.size();
        }

        log.info("🎉 Seed completado: {} modelos, {} métricas", savedModelos.size(), totalMetricas);
    }
}
