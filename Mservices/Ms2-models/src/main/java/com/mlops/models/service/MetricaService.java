package com.mlops.models.service;

import com.mlops.models.dto.MetricaDTO;
import com.mlops.models.exception.ResourceNotFoundException;
import com.mlops.models.model.Metrica;
import com.mlops.models.model.Modelo;
import com.mlops.models.repository.MetricaRepository;
import com.mlops.models.repository.ModeloRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class MetricaService {

    private final MetricaRepository metricaRepository;
    private final ModeloRepository modeloRepository;

    public Page<Metrica> findAll(int page, int size) {
        return metricaRepository.findAll(PageRequest.of(page, size, Sort.by("createdAt").descending()));
    }

    public Page<Metrica> findByModelo(Long modeloId, int page, int size) {
        return metricaRepository.findByModeloId(modeloId, PageRequest.of(page, size, Sort.by("createdAt").descending()));
    }

    public Metrica findById(Long id) {
        return metricaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Métrica " + id + " no encontrada"));
    }

    @Transactional
    public Metrica create(MetricaDTO dto) {
        Modelo modelo = modeloRepository.findById(dto.getModeloId())
                .orElseThrow(() -> new ResourceNotFoundException("Modelo " + dto.getModeloId() + " no encontrado"));
        Metrica metrica = new Metrica();
        mapDtoToEntity(dto, metrica);
        metrica.setModelo(modelo);
        return metricaRepository.save(metrica);
    }

    @Transactional
    public Metrica update(Long id, MetricaDTO dto) {
        Metrica metrica = findById(id);
        mapDtoToEntity(dto, metrica);
        return metricaRepository.save(metrica);
    }

    @Transactional
    public void delete(Long id) {
        Metrica metrica = findById(id);
        metricaRepository.delete(metrica);
    }

    private void mapDtoToEntity(MetricaDTO dto, Metrica metrica) {
        metrica.setTipoMetrica(dto.getTipoMetrica());
        metrica.setValorMetrica(dto.getValorMetrica());
        metrica.setDatasetEvaluacion(dto.getDatasetEvaluacion());
        metrica.setNotas(dto.getNotas());
    }
}
