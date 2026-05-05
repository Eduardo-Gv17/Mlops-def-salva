package com.mlops.models.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class MetricaDTO {
    private Long id;

    @NotBlank
    private String tipoMetrica;

    @NotNull
    private BigDecimal valorMetrica;

    private String datasetEvaluacion;
    private String notas;

    @NotNull
    private Long modeloId;

    private LocalDateTime createdAt;
}
