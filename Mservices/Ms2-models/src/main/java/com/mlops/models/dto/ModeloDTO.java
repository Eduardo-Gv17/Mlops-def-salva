package com.mlops.models.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;
import java.time.LocalDateTime;

@Data
public class ModeloDTO {
    private Long id;

    @NotBlank @Size(max = 200)
    private String nombre;

    @NotBlank @Size(max = 100)
    private String framework;

    @NotBlank @Size(max = 100)
    private String version;

    private String descripcion;
    private Boolean activo;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
