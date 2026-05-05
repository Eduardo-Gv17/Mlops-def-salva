/**
 * Seed: 20,000 prediction logs en MongoDB
 * Uso: docker compose exec ms3-predlogs node scripts/seed_predlogs.js
 */
require('dotenv').config({ path: require('path').join(__dirname, '../.env') });
const mongoose = require('mongoose');
const { faker } = require('@faker-js/faker');
const PredLog = require('../models/PredLog');

const MONGO_HOST = process.env.PREDLOGS_DB_HOST || 'localhost';
const MONGO_PORT = process.env.PREDLOGS_DB_PORT || '27017';
const MONGO_DB   = process.env.PREDLOGS_DB_NAME || 'predlogs_db';
const MONGO_URI  = `mongodb://${MONGO_HOST}:${MONGO_PORT}/${MONGO_DB}`;

const MODELOS = [
  { id: 1, nombre: 'churn_predictor_v2', labels: ['churn', 'no_churn'] },
  { id: 2, nombre: 'fraud_detector_v1', labels: ['fraud', 'no_fraud'] },
  { id: 3, nombre: 'credit_scoring_v1', labels: ['high_risk', 'low_risk'] },
  { id: 4, nombre: 'sentiment_analyzer_v1', labels: ['positive', 'negative'] },
  { id: 5, nombre: 'price_optimizer_v1', labels: ['high_risk', 'low_risk'] }
];

const DATASETS = [
  'customer_churn_2024', 'fraud_transactions_2024', 'credit_history_2023',
  'retail_sales_2024', 'product_reviews_2024', 'market_prices_2024'
];

function randomFeatures() {
  return {
    edad: faker.number.int({ min: 18, max: 75 }),
    ingreso_mensual: parseFloat(faker.finance.amount({ min: 500, max: 15000, dec: 2 })),
    num_transacciones: faker.number.int({ min: 1, max: 200 }),
    saldo_promedio: parseFloat(faker.finance.amount({ min: 100, max: 50000, dec: 2 })),
    dias_cliente: faker.number.int({ min: 30, max: 3650 }),
    score_credito: faker.number.int({ min: 300, max: 850 })
  };
}

async function seed() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log('✅ Conectado a MongoDB');

    const existing = await PredLog.countDocuments();
    if (existing > 0) {
      console.log(`⚠️  Ya existen ${existing} predlogs. Saltando seed.`);
      process.exit(0);
    }

    console.log('🌱 Generando 20,000 prediction logs...');
    const TOTAL = 20000;
    const BATCH_SIZE = 500;
    let inserted = 0;

    // Distribuir logs en los últimos 90 días
    const now = new Date();
    const ninetyDaysAgo = new Date(now - 90 * 24 * 60 * 60 * 1000);

    for (let i = 0; i < TOTAL; i += BATCH_SIZE) {
      const batch = [];
      for (let j = 0; j < BATCH_SIZE && (i + j) < TOTAL; j++) {
        const modelo = MODELOS[Math.floor(Math.random() * MODELOS.length)];
        const output = Math.random();
        const label = output > 0.5 ? modelo.labels[0] : modelo.labels[1];
        const latencia = Math.floor(Math.random() * 200) + 10;
        const timestamp = new Date(
          ninetyDaysAgo.getTime() + Math.random() * (now.getTime() - ninetyDaysAgo.getTime())
        );

        batch.push({
          modelo_id: modelo.id,
          modelo_nombre: modelo.nombre,
          dataset_origen: DATASETS[Math.floor(Math.random() * DATASETS.length)],
          input_features: randomFeatures(),
          prediccion_output: parseFloat(output.toFixed(6)),
          prediccion_label: label,
          latencia_ms: latencia,
          estado: Math.random() > 0.03 ? 'success' : (Math.random() > 0.5 ? 'error' : 'timeout'),
          timestamp
        });
      }
      await PredLog.insertMany(batch);
      inserted += batch.length;
      console.log(`  → ${inserted}/${TOTAL} logs insertados...`);
    }

    console.log(`\n🎉 Seed completado: ${inserted} prediction logs`);
    process.exit(0);
  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

seed();
