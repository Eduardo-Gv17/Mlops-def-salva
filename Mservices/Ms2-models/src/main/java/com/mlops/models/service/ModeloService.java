package com.mlops.models.service;

import com.mlops.models.dto.ModeloDTO;
import com.mlops.models.exception.ResourceNotFoundException;
import com.mlops.models.model.Modelo;
import com.mlops.models.repository.ModeloRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class ModeloService {

    private final ModeloRepository modeloRepository;

    public Page<Modelo> findAll(int page, int size, Boolean activo, String framework) {
        var pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        if (activo != null) return modeloRepository.findByActivo(activo, pageable);
        if (framework != null) return modeloRepository.findByFramework(framework, pageable);
        return modeloRepository.findAll(pageable);
    }

    public Modelo findById(Long id) {
        return modeloRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Modelo " + id + " no encontrado"));
    }

    @Transactional
    public Modelo create(ModeloDTO dto) {
        if (modeloRepository.existsByNombre(dto.getNombre())) {
            throw new IllegalArgumentException("Ya existe un modelo con nombre '" + dto.getNombre() + "'");
        }
        Modelo modelo = new Modelo();
        mapDtoToEntity(dto, modelo);
        return modeloRepository.save(modelo);
    }

    @Transactional
    public Modelo update(Long id, ModeloDTO dto) {
        Modelo modelo = findById(id);
        mapDtoToEntity(dto, modelo);
        return modeloRepository.save(modelo);
    }

    @Transactional
    public void softDelete(Long id) {
        Modelo modelo = findById(id);
        modelo.setActivo(false);
        modeloRepository.save(modelo);
    }

    private void mapDtoToEntity(ModeloDTO dto, Modelo modelo) {
        modelo.setNombre(dto.getNombre());
        modelo.setFramework(dto.getFramework());
        modelo.setVersion(dto.getVersion());
        modelo.setDescripcion(dto.getDescripcion());
        if (dto.getActivo() != null) modelo.setActivo(dto.getActivo());
    }
}
