package com.mlops.models.controller;

import com.mlops.models.dto.MetricaDTO;
import com.mlops.models.model.Metrica;
import com.mlops.models.service.MetricaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/metricas")
@RequiredArgsConstructor
@Tag(name = "Métricas", description = "CRUD de métricas de modelos ML")
@CrossOrigin(origins = "*")
public class MetricaController {

    private final MetricaService metricaService;

    @GetMapping
    @Operation(summary = "Listar métricas paginadas")
    public Page<MetricaDTO> list(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Page<Metrica> metricas = metricaService.findAll(page, size);
        List<MetricaDTO> dtos = metricas.getContent().stream().map(this::toDTO).toList();
        return new PageImpl<>(dtos, metricas.getPageable(), metricas.getTotalElements());
    }

    @GetMapping("/modelo/{modeloId}")
    @Operation(summary = "Métricas de un modelo específico")
    public Page<MetricaDTO> byModelo(
            @PathVariable Long modeloId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Page<Metrica> metricas = metricaService.findByModelo(modeloId, page, size);
        List<MetricaDTO> dtos = metricas.getContent().stream().map(this::toDTO).toList();
        return new PageImpl<>(dtos, metricas.getPageable(), metricas.getTotalElements());
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obtener métrica por ID")
    public MetricaDTO getById(@PathVariable Long id) {
        return toDTO(metricaService.findById(id));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Crear métrica")
    public MetricaDTO create(@Valid @RequestBody MetricaDTO dto) {
        return toDTO(metricaService.create(dto));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Actualizar métrica")
    public MetricaDTO update(@PathVariable Long id, @Valid @RequestBody MetricaDTO dto) {
        return toDTO(metricaService.update(id, dto));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Eliminar métrica")
    public ResponseEntity<String> delete(@PathVariable Long id) {
        metricaService.delete(id);
        return ResponseEntity.ok("Métrica " + id + " eliminada");
    }

    private MetricaDTO toDTO(Metrica m) {
        MetricaDTO dto = new MetricaDTO();
        dto.setId(m.getId());
        dto.setTipoMetrica(m.getTipoMetrica());
        dto.setValorMetrica(m.getValorMetrica());
        dto.setDatasetEvaluacion(m.getDatasetEvaluacion());
        dto.setNotas(m.getNotas());
        dto.setModeloId(m.getModelo().getId());
        dto.setCreatedAt(m.getCreatedAt());
        return dto;
    }
}