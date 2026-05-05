package com.mlops.models.repository;

import com.mlops.models.model.Metrica;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MetricaRepository extends JpaRepository<Metrica, Long> {
    Page<Metrica> findByModeloId(Long modeloId, Pageable pageable);
    List<Metrica> findByTipoMetrica(String tipoMetrica);
}
