# Hito Go/No-Go de latencia — resultado

**Fecha de medición:** 16 de septiembre de 2026
**Fecha comprometida en el acta:** semana 4, 25 de septiembre de 2026 — **cumplido con 9 días de antelación**
**Ejecutó:** Abiud Misael Benítez Franco

---

## Veredicto

**APRUEBA.** El p90 de la latencia golpe→sonido es de **+4.07 ms** contra un criterio de
**−10 ms ≤ Δ(p90) ≤ +25 ms**. Seis veces de margen.

El riesgo dominante del proyecto queda cerrado: el golpe se siente causal.

## Método

Protocolo del clic físico (capítulo 5 de la guía). Se golpea una superficie rígida situada
exactamente donde vive el pad virtual, previa calibración con `PadCalibrator`. La grabación
contiene dos transitorios por golpe:

- el clic del control contra la superficie — instante **real** del impacto
- el bombo virtual por las bocinas del visor — sonido **generado**

Δ = t_virtual − t_físico, con precisión de muestra a 48 kHz.

Análisis con `scripts/latencia.py`. Discriminación clic/tambor por razón de energía
grave/agudo, con control de calidad de corrida completa.

## Configuración medida

| | |
|---|---|
| Hardware | Meta Quest 3S |
| Unity | 6000.5.10f1 · OpenXR 1.18 · XRI 3.6.0 |
| DSP Buffer Size | Best Latency (256 samples) |
| System Sample Rate | 48000 Hz |
| Graphics API | Vulkan |
| Sample | `512175__kopreusz__kick_2.wav` |
| `radius` | 0.15 m |
| `poseToAudioOffset` | 0 (sin calibrar) |
| Audio | bocinas integradas del visor, **sin Bluetooth** |

## Resultados

Veinte golpes por corrida. Ambas corridas con el mismo sample.

| | CON predicción (`armDistance` 0.06) | SIN predicción (`armDistance` 0) |
|---|---|---|
| Golpes medibles | 19 de 21 | 20 de 21 |
| Mediana | +3.29 ms | +0.81 ms |
| **p90** | **+4.07 ms** | **+3.51 ms** |
| Mínimo / máximo | +1.83 / +6.62 ms | −3.23 / +7.81 ms |
| Desviación estándar | **1.08 ms** | **3.20 ms** |
| Dispersión p10–p90 | **2.07 ms** | **6.51 ms** |
| Veredicto | APRUEBA | APRUEBA |

## Hallazgo: la predicción reduce el jitter, no la latencia media

El diseño (§4.4 del diseño técnico) preveía un presupuesto de ~26 ms —tracking ~10, frame a
90 Hz ~11, buffer de audio ~5— y justificaba la predicción del plano armado como la mitigación
que lo convertiría en latencia percibida cercana a cero.

**Los datos no respaldan ese mecanismo.** Al desactivar la predicción la latencia no subió: se
mantuvo en +0.81 ms de mediana. Lo que sí cambió, y de forma contundente, fue la dispersión.

Prueba de permutación con 20 000 remuestreos:

| Comparación | Valor | p |
|---|---|---|
| Diferencia de medianas | +2.48 ms | **0.0002** |
| Razón de desviaciones (sin/con) | 2.97× | **0.0001** |

Ambas diferencias son estadísticamente sólidas. **La predicción del plano armado reduce la
dispersión temporal a un tercio.** Ese es su beneficio medido, y es relevante para un sistema
rítmico: la irregularidad entre golpes es lo que rompe la sensación de pulso, más que un
retardo constante que el usuario compensa sin darse cuenta.

### Consecuencia para el presupuesto de latencia

El presupuesto de ~26 ms **no se observa en el hardware real**. Explicaciones candidatas, por
orden de plausibilidad y todas pendientes de comprobar:

1. **La pose del controlador ya viene predicha al instante de presentación** por el runtime de
   OpenXR. Eso adelanta `tip.position` respecto a la realidad y compensa por sí solo buena
   parte del retardo del camino de audio.
2. El camino de audio del Quest 3S es más rápido que los ~5 ms presupuestados para el buffer.
3. Los dos efectos se cancelan parcialmente con `poseToAudioOffset` en 0.

**Comprobación pendiente, barata:** el JSON de `LatencyProbe` registra `agendasTardias`. Si el
mecanismo es el descrito, la corrida sin predicción debería mostrar una proporción alta de
agendas tardías y la corrida con predicción, casi ninguna. Sacarlo con `adb pull` y compararlo
confirmaría o descartaría la explicación 1 sin volver a medir.

## Limitaciones declaradas

- `poseToAudioOffset` **no se calibró**. El barrido del capítulo 6 podría mejorar el resultado,
  pero con +4.07 ms de p90 no hay necesidad operativa.
- Una sola sesión, un solo usuario, un solo pad. No se midió a distintas velocidades de golpe
  ni con fatiga.
- La medición cubre golpe→sonido. **No cubre** la latencia de presentación visual, que no se
  midió porque el canal causal de este sistema es el auditivo.
- Corrida con predicción: 19 golpes medibles en lugar de 20. Dos golpes se omitieron por
  detectarse un solo transitorio fuerte.

## Archivos

| | |
|---|---|
| Grabaciones | `mediciones/con_prediccion.wav`, `mediciones/sin_predicciones.wav` |
| Herramienta | `scripts/latencia.py` · 19 pruebas en `scripts/test_latencia.py` |
| Protocolo | Capítulo 5 de `entregables/guia/Guia_Bateria_VR_A.md` |
