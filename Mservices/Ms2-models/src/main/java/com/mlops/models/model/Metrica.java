package com.mlops.models.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "metricas")
public class Metrica {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    @Column(name = "tipo_metrica", nullable = false, length = 50)
    private String tipoMetrica;   // accuracy, precision, recall, f1, auc_roc, rmse, mae

    @Column(name = "valor_metrica", nullable = false, precision = 10, scale = 6)
    private BigDecimal valorMetrica;

    @Column(name = "dataset_evaluacion", length = 200)
    private String datasetEvaluacion;

    @Column(columnDefinition = "TEXT")
    private String notas;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "modelo_id", nullable = false)
    private Modelo modelo;
}
