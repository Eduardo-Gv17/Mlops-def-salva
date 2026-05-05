const express = require('express');
const router = express.Router();
const PredLog = require('../models/PredLog');

/**
 * @swagger
 * tags:
 *   name: PredLogs
 *   description: Logs de predicciones de modelos ML
 */

/**
 * @swagger
 * /api/predlogs:
 *   get:
 *     summary: Listar logs de predicciones paginados
 *     tags: [PredLogs]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema: { type: integer, default: 1 }
 *       - in: query
 *         name: limit
 *         schema: { type: integer, default: 10 }
 *       - in: query
 *         name: estado
 *         schema: { type: string }
 */
router.get('/', async (req, res) => {
  try {
    const page = Math.max(1, parseInt(req.query.page) || 1);
    const limit = Math.min(100, parseInt(req.query.limit) || 10);
    const skip = (page - 1) * limit;
    const filter = {};
    if (req.query.estado) filter.estado = req.query.estado;
    if (req.query.modelo_id) filter.modelo_id = parseInt(req.query.modelo_id);

    const [total, items] = await Promise.all([
      PredLog.countDocuments(filter),
      PredLog.find(filter).sort({ timestamp: -1 }).skip(skip).limit(limit)
    ]);

    res.json({ total, page, limit, items });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/**
 * @swagger
 * /api/predlogs/stats/summary:
 *   get:
 *     summary: Resumen estadístico de predicciones
 *     tags: [PredLogs]
 */
router.get('/stats/summary', async (req, res) => {
  try {
    const [total, byEstado, avgLatencia] = await Promise.all([
      PredLog.countDocuments(),
      PredLog.aggregate([{ $group: { _id: '$estado', count: { $sum: 1 } } }]),
      PredLog.aggregate([{ $group: { _id: null, avg: { $avg: '$latencia_ms' }, min: { $min: '$latencia_ms' }, max: { $max: '$latencia_ms' } } }])
    ]);
    res.json({
      total_logs: total,
      por_estado: byEstado,
      latencia_ms: avgLatencia[0] || { avg: 0, min: 0, max: 0 }
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/**
 * @swagger
 * /api/predlogs/modelo/{modelo_id}:
 *   get:
 *     summary: Logs de un modelo específico
 *     tags: [PredLogs]
 */
router.get('/modelo/:modelo_id', async (req, res) => {
  try {
    const page = Math.max(1, parseInt(req.query.page) || 1);
    const limit = Math.min(100, parseInt(req.query.limit) || 10);
    const skip = (page - 1) * limit;
    const modelo_id = parseInt(req.params.modelo_id);
    const [total, items] = await Promise.all([
      PredLog.countDocuments({ modelo_id }),
      PredLog.find({ modelo_id }).sort({ timestamp: -1 }).skip(skip).limit(limit)
    ]);
    res.json({ total, page, limit, items });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/**
 * @swagger
 * /api/predlogs/{id}:
 *   get:
 *     summary: Obtener log por ID
 *     tags: [PredLogs]
 */
router.get('/:id', async (req, res) => {
  try {
    const log = await PredLog.findById(req.params.id);
    if (!log) return res.status(404).json({ error: 'PredLog no encontrado' });
    res.json(log);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/**
 * @swagger
 * /api/predlogs:
 *   post:
 *     summary: Crear nuevo log de predicción
 *     tags: [PredLogs]
 */
router.post('/', async (req, res) => {
  try {
    const log = new PredLog(req.body);
    await log.save();
    res.status(201).json(log);
  } catch (err) {
    if (err.name === 'ValidationError') {
      return res.status(400).json({ error: err.message });
    }
    res.status(500).json({ error: err.message });
  }
});

/**
 * @swagger
 * /api/predlogs/{id}:
 *   delete:
 *     summary: Eliminar log de predicción
 *     tags: [PredLogs]
 */
router.delete('/:id', async (req, res) => {
  try {
    const log = await PredLog.findByIdAndDelete(req.params.id);
    if (!log) return res.status(404).json({ error: 'PredLog no encontrado' });
    res.json({ message: `PredLog ${req.params.id} eliminado` });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
