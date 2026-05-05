package com.mlops.models.controller;

import com.mlops.models.dto.MetricaDTO;
import com.mlops.models.model.Metrica;
import com.mlops.models.service.MetricaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/metricas")
@RequiredArgsConstructor
@Tag(name = "Métricas", description = "CRUD de métricas de modelos ML")
@CrossOrigin(origins = "*")
public class MetricaController {

    private final MetricaService metricaService;

    @GetMapping
    @Operation(summary = "Listar métricas paginadas")
    public Page<Metrica> list(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size
    ) {
        return metricaService.findAll(page, size);
    }

    @GetMapping("/modelo/{modeloId}")
    @Operation(summary = "Métricas de un modelo específico")
    public Page<Metrica> byModelo(
            @PathVariable Long modeloId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size
    ) {
        return metricaService.findByModelo(modeloId, page, size);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obtener métrica por ID")
    public Metrica getById(@PathVariable Long id) {
        return metricaService.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Crear métrica")
    public Metrica create(@Valid @RequestBody MetricaDTO dto) {
        return metricaService.create(dto);
    }

    @PutMapping("/{id}")
    @Operation(summary = "Actualizar métrica")
    public Metrica update(@PathVariable Long id, @Valid @RequestBody MetricaDTO dto) {
        return metricaService.update(id, dto);
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Eliminar métrica")
    public ResponseEntity<String> delete(@PathVariable Long id) {
        metricaService.delete(id);
        return ResponseEntity.ok("Métrica " + id + " eliminada");
    }
}
