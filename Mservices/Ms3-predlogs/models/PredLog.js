const mongoose = require('mongoose');

const predLogSchema = new mongoose.Schema({
  modelo_id: {
    type: Number,
    required: true,
    index: true
  },
  modelo_nombre: {
    type: String,
    required: true,
    maxlength: 200,
    index: true
  },
  dataset_origen: {
    type: String,
    required: true,
    maxlength: 200
  },
  input_features: {
    type: mongoose.Schema.Types.Mixed,
    required: true
  },
  prediccion_output: {
    type: Number,
    required: true,
    min: 0,
    max: 1
  },
  prediccion_label: {
    type: String,
    enum: ['churn', 'no_churn', 'fraud', 'no_fraud', 'high_risk', 'low_risk', 'positive', 'negative'],
    required: true
  },
  latencia_ms: {
    type: Number,
    required: true,
    min: 0
  },
  estado: {
    type: String,
    enum: ['success', 'error', 'timeout'],
    default: 'success'
  },
  timestamp: {
    type: Date,
    default: Date.now,
    index: true
  }
}, {
  collection: 'predlogs',
  timestamps: false
});

predLogSchema.index({ modelo_id: 1, timestamp: -1 });
predLogSchema.index({ timestamp: -1 });

module.exports = mongoose.model('PredLog', predLogSchema);
