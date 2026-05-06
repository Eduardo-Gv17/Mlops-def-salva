package com.mlops.models.controller;

import com.mlops.models.dto.ModeloDTO;
import com.mlops.models.model.Modelo;
import com.mlops.models.service.ModeloService;
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
@RequestMapping("/api/modelos")
@RequiredArgsConstructor
@Tag(name = "Modelos", description = "CRUD de modelos ML")
@CrossOrigin(origins = "*")
public class ModeloController {

    private final ModeloService modeloService;

    @GetMapping
    @Operation(summary = "Listar modelos paginados")
    public Page<ModeloDTO> list(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) Boolean activo,
            @RequestParam(required = false) String framework) {
        Page<Modelo> modelos = modeloService.findAll(page, size, activo, framework);
        List<ModeloDTO> dtos = modelos.getContent().stream().map(this::toDTO).toList();
        return new PageImpl<>(dtos, modelos.getPageable(), modelos.getTotalElements());
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obtener modelo por ID")
    public ModeloDTO getById(@PathVariable Long id) {
        return toDTO(modeloService.findById(id));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Crear nuevo modelo")
    public ModeloDTO create(@Valid @RequestBody ModeloDTO dto) {
        return toDTO(modeloService.create(dto));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Actualizar modelo")
    public ModeloDTO update(@PathVariable Long id, @Valid @RequestBody ModeloDTO dto) {
        return toDTO(modeloService.update(id, dto));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Desactivar modelo (soft delete)")
    public ResponseEntity<String> delete(@PathVariable Long id) {
        modeloService.softDelete(id);
        return ResponseEntity.ok("Modelo " + id + " desactivado");
    }

    private ModeloDTO toDTO(Modelo m) {
        ModeloDTO dto = new ModeloDTO();
        dto.setId(m.getId());
        dto.setNombre(m.getNombre());
        dto.setFramework(m.getFramework());
        dto.setVersion(m.getVersion());
        dto.setDescripcion(m.getDescripcion());
        dto.setActivo(m.getActivo());
        dto.setCreatedAt(m.getCreatedAt());
        dto.setUpdatedAt(m.getUpdatedAt());
        return dto;
    }
}