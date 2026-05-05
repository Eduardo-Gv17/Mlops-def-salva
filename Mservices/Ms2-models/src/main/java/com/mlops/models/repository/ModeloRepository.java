package com.mlops.models.repository;

import com.mlops.models.model.Modelo;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ModeloRepository extends JpaRepository<Modelo, Long> {
    Page<Modelo> findByActivo(Boolean activo, Pageable pageable);
    Page<Modelo> findByFramework(String framework, Pageable pageable);
    Optional<Modelo> findByNombre(String nombre);
    boolean existsByNombre(String nombre);
}
