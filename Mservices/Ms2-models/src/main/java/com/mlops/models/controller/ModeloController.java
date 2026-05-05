package com.mlops.models.controller;

import com.mlops.models.dto.ModeloDTO;
import com.mlops.models.model.Modelo;
import com.mlops.models.service.ModeloService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/modelos")
@RequiredArgsConstructor
@Tag(name = "Modelos", description = "CRUD de modelos ML")
@CrossOrigin(origins = "*")
public class ModeloController {

    private final ModeloService modeloService;

    @GetMapping
    @Operation(summary = "Listar modelos paginados")
    public Page<Modelo> list(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) Boolean activo,
            @RequestParam(required = false) String framework
    ) {
        return modeloService.findAll(page, size, activo, framework);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obtener modelo por ID")
    public Modelo getById(@PathVariable Long id) {
        return modeloService.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Crear nuevo modelo")
    public Modelo create(@Valid @RequestBody ModeloDTO dto) {
        return modeloService.create(dto);
    }

    @PutMapping("/{id}")
    @Operation(summary = "Actualizar modelo")
    public Modelo update(@PathVariable Long id, @Valid @RequestBody ModeloDTO dto) {
        return modeloService.update(id, dto);
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Desactivar modelo (soft delete)")
    public ResponseEntity<String> delete(@PathVariable Long id) {
        modeloService.softDelete(id);
        return ResponseEntity.ok("Modelo " + id + " desactivado correctamente");
    }
}
