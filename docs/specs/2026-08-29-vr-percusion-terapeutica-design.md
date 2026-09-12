# Diseño — Sistema de Percusión Terapéutica en Realidad Virtual

**Proyecto:** Prototipo VR de percusión para regulación de estrés y ansiedad
**Materia:** Administración de Proyectos de Software · **Equipo:** 03
**Docente:** Dra. Leticia Amalia Neira Tovar
**Periodo:** 31 de agosto de 2026 – 30 de noviembre de 2026 (13 semanas)
**Fecha del documento:** 29 de agosto de 2026
**Estado:** Diseño aprobado, pendiente de plan de implementación

> **AVISO DE VIGENCIA — 31 de agosto de 2026**
>
> Este documento se redactó antes de la presentación del acta constitutiva v1.0. Dos supuestos cambiaron:
>
> | Tema | Lo que dice este documento | Lo vigente |
> |---|---|---|
> | Población y enfoque | Salud mental, estrés y ansiedad | **Motriz primario, emocional secundario** |
> | Variable primaria | Δ STAI-6 (autoreporte de ansiedad) | **Precisión rítmica y velocidad de impacto**; el autoreporte pasa a secundario |
> | Periodo | 31-ago a 30-nov-2026 (13 semanas) | **1-sep a 13-nov-2026 (11 semanas)**, reserva 16–20 nov |
> | Equipo | 5 integrantes implícitos | **8 integrantes más asesor terapéutico externo** |
>
> **Sigue vigente todo lo técnico:** arquitectura de módulos, presupuesto de latencia, regla del `dspTime`,
> presupuesto de rendimiento, esquema de datos, casos borde y la decisión de motor.
>
> Para el alcance, el cronograma y el presupuesto vigentes, ver
> [`2026-08-31-correccion-acta-v2-design.md`](2026-08-31-correccion-acta-v2-design.md) y `CLAUDE.md`.

---

## 1. Resumen ejecutivo

Se desarrollará un prototipo de realidad virtual para Meta Quest standalone en el que el usuario toca una batería virtual dentro de una sesión terapéutica guiada de aproximadamente 12 minutos. La sesión aplica el **iso-principio** de la musicoterapia: mide el tempo espontáneo del usuario, arranca ahí, y desciende gradualmente hasta 60 BPM para arrastrar su nivel de activación fisiológica hacia abajo. Cierra con una fase respiratoria a 6 respiraciones por minuto.

El proyecto entrega dos productos:

1. **Documentación completa de administración de proyectos** conforme a PMBOK (acta constitutiva, alcance, EDT, cronograma, riesgos, cierre).
2. **Prototipo VR demostrable**, validado en un estudio piloto de factibilidad y usabilidad con 12-15 participantes.

---

## 2. Justificación terapéutica

### 2.1 Por qué percusión

El ritmo actúa como referencia temporal continua que arrastra (*entrainment*) los patrones motores y fisiológicos del individuo. El sistema auditivo tiene conexión directa con circuitos motores, lo que permite que un estímulo rítmico externo module la actividad interna.

La percusión presenta ventajas específicas frente a instrumentos melódicos:

- **Cero curva de aprendizaje musical.** El usuario no necesita conocer teoría, notas ni acordes. Golpea y suena.
- **Feedback inmediato y discreto.** Cada golpe produce un evento sonoro puntual, fácil de medir y de asociar causalmente con el movimiento.
- **Descarga física.** El gesto es amplio y enérgico, lo que canaliza activación somática.
- **Facilidad de simulación en VR.** Un golpe es una colisión; no requiere modelar digitación, presión continua ni articulaciones finas.

El piano queda descartado por existir ya un proyecto sobre ese instrumento en el mismo contexto académico.

### 2.2 Evidencia por dominio

| Dominio | Hallazgo | Población estudiada |
|---|---|---|
| Motor grueso | La Estimulación Auditiva Rítmica (RAS) mejora marcha, balance y velocidad de movimiento | Parkinson, Huntington, EVC |
| Motor fino / miembro superior | Therapeutic Instrumental Music Performance (TIMP): golpear tambores colocados en el espacio entrena alcance, rango articular y coordinación bilateral | Hemiparesia post-EVC |
| Psicosocial | Los *drum circles* incrementan bienestar social y regulación emocional, y reducen aislamiento | Jóvenes en riesgo, adultos mayores |
| Físico-psico-social | Revisión de alcance sobre membranófonos: impacto positivo en salud física, psicológica y social en entornos de cuidado | Adultos, contextos clínicos diversos |
| Motivación y adherencia | El componente rítmico incrementa la motivación intrínseca frente a terapia convencional repetitiva | Transversal |

### 2.3 Marcos formales de referencia

El proyecto se ancla en **Neurologic Music Therapy (NMT)**, que define protocolos con nombre propio en lugar de intervenciones improvisadas:

- **RAS** — Rhythmic Auditory Stimulation
- **TIMP** — Therapeutic Instrumental Music Performance
- **PSE** — Patterned Sensory Enhancement
- **Iso-principio** — empatar el estado actual del paciente y desplazarlo gradualmente hacia el estado objetivo

Citar estos marcos da rigor metodológico y evita que el proyecto se lea como "tocar tambores y ver qué pasa".

### 2.4 Evidencia sobre VR

- Meta-análisis de VR en rehabilitación de miembro superior post-EVC reportan superioridad sobre terapia convencional en función motora, independencia funcional, calidad de vida, espasticidad y destreza. Las intervenciones de más de seis semanas producen mejores resultados.
- Existen ya sistemas que combinan VR con NMT (xilófono y tambores virtuales) con evaluaciones positivas de usabilidad.

### 2.5 Ventajas de la batería virtual sobre la real

| Dimensión | Batería acústica | Batería VR |
|---|---|---|
| Costo | Instrumento + espacio + insonorización + mantenimiento | Un visor |
| Configurabilidad clínica | Fija | Pads reposicionables: alejar para forzar rango articular, reducir para trabajar precisión |
| Métricas | Ninguna, salvo observación del terapeuta | Timing en ms, fuerza de golpe, alcance, simetría izquierda/derecha, adherencia |
| Ruido | Alto, requiere aislamiento | Nulo, audio por auriculares |
| Higiene y portabilidad | Baja | Alta |
| Gamificación | No aplica | Nativa, favorece adherencia |

### 2.6 Limitación reconocida

**Ausencia de retroalimentación háptica real.** La baqueta virtual atraviesa el pad sin resistencia física. Se compensa parcialmente con vibración del control, respuesta sonora inmediata y respuesta visual del pad, pero es el hueco conocido de la percusión en VR y debe declararse como limitación del prototipo.

### 2.7 Fuentes

- Rhythm and Music-Based Interventions in Motor Rehabilitation — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8801707/
- Membranophone percussion instruments in music therapy: scope review — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10364967/
- Systematic review on rhythm-centred music making and health — https://www.sciencedirect.com/science/article/abs/pii/S1876382016304115
- Efficacy of VR for upper limb rehabilitation in stroke: systematic review and meta-analysis — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11127427/
- VR Rehabilitation Based on Neurologic Music Therapy — https://link.springer.com/chapter/10.1007/978-3-319-91152-6_9
- VR Music Instrument Playing Game for Upper Limb Rehabilitation — https://dl.acm.org/doi/10.1145/3610661.3617159
- Drumming with BEAT: drum set playing in Parkinson's disease — https://www.frontiersin.org/journals/rehabilitation-sciences/articles/10.3389/fresc.2026.1671559/full

---

## 3. Decisión de motor: Unity sobre Unreal

### 3.1 Contexto de la decisión

La propuesta inicial del equipo fue Unreal Engine bajo el supuesto de que sería la opción más sencilla. El análisis no sostiene ese supuesto para las condiciones concretas de este proyecto.

**Condiciones determinantes:** hardware objetivo Meta Quest standalone (sin PC), equipo sin experiencia previa en ningún motor, ventana fija de 13 semanas.

### 3.2 Comparativa

| Criterio | Unreal Engine 5.7 | Unity 6 |
|---|---|---|
| Soporte Quest standalone | Sí, first-class desde 5.7: Vulkan móvil, foveated rendering, passthrough | Sí, SDK first-party de Meta y Building Blocks |
| Eficiencia en chip móvil | Aceptable con optimización agresiva | Mejor por defecto |
| Audio percusivo | MetaSounds: DSP sample-accurate, síntesis procedural | Sampler estándar; FMOD/Wwise disponibles sin costo para uso no comercial |
| Curva de aprendizaje | Blueprints evitan escribir código, pero el pipeline Android es complejo | XR Interaction Toolkit; volumen de tutoriales VR muy superior |
| Iteración | Lenta: compilación de shaders, APK grande | Rápida |
| Calidad visual | Superior | Suficiente |

### 3.3 Razonamiento

La aplicación es gráficamente trivial: una sala y una batería. La ventaja competitiva de Unreal (Lumen, Nanite, fotorrealismo) no aporta valor terapéutico alguno en este contexto, mientras que sus costos (pipeline Android, builds lentas, menor densidad de material de aprendizaje para VR) se pagan íntegros.

MetaSounds es la única ventaja técnica real de Unreal para este caso. Sin embargo, la percusión no requiere síntesis procedural: samples multi-velocity con round-robin resuelven el requerimiento, y Unity los soporta de forma equivalente.

### 3.4 Decisión

**Unity 6 + XR Interaction Toolkit + Meta XR SDK.**

Unreal Engine se documenta en el acta constitutiva como alternativa evaluada y descartada, con el razonamiento anterior. Esto refuerza el rigor metodológico del proyecto en lugar de debilitarlo.

**Condición bajo la cual Unreal habría sido viable:** que algún integrante ya dominara Unreal o Blueprints. No es el caso.

---

## 4. Arquitectura del prototipo

### 4.1 Plataforma

- **Motor:** Unity 6
- **SDK:** XR Interaction Toolkit + Meta XR SDK
- **Hardware:** Meta Quest 3 / 3S en modo standalone
- **Entrada:** controles Quest, **no** hand tracking

Justificación del uso de controles: los controles entregan vibración háptica y una lectura confiable de velocidad lineal en el momento del impacto. El hand tracking no ofrece ninguna de las dos, y ambas son esenciales para que un golpe de percusión se sienta correcto.

### 4.2 Módulos

| # | Módulo | Responsabilidad | Depende de |
|---|---|---|---|
| M1 | `DrumKit` | Seis piezas: bombo, tarola, hi-hat, dos toms, crash. Collider y detección de cruce. Deriva la *velocity* de la velocidad del controlador al impacto. Histéresis anti-retrigger | — |
| M2 | `AudioEngine` | Reproducción de samples. Tres capas de velocity por dos o tres variantes round-robin por pieza. Pool de `AudioSource` pre-instanciado, sin asignaciones de memoria en tiempo de ejecución | — |
| M3 | `SessionDirector` | Máquina de estados de la sesión. Curva de tempo expuesta como `AnimationCurve` en el inspector, editable sin tocar código | M2, M4, M6 |
| M4 | `RhythmGuide` | Metrónomo y guía visual: el pad correspondiente pulsa antes del beat. Reloj maestro basado en `AudioSettings.dspTime` | M2 |
| M5 | `MetricsLogger` | Registra el timestamp de cada golpe contra el beat esperado y calcula el error en milisegundos. Conteo, duración, abandono. Serializa a JSON en almacenamiento local del visor | M1, M4 |
| M6 | `AssessmentUI` | STAI-6 en canvas world-space. Seis ítems, escala 1-4, selección mediante láser | — |
| M7 | `Environment` | Escena relajante que reacciona a la intensidad de los golpes. Iluminación bakeada, sin GI en tiempo real | M1 |

### 4.3 Regla crítica de temporización

El reloj maestro del sistema rítmico **debe** derivarse de `AudioSettings.dspTime`, nunca de `Update()` ni de `Time.deltaTime`. El tiempo de frame es irregular y acumula deriva; el reloj DSP es estable y está sincronizado con la salida de audio. Usar tiempo de frame es el error más común al construir sistemas rítmicos y produce desincronización acumulativa a lo largo de una sesión de doce minutos.

### 4.4 Presupuesto de latencia

La latencia entre el golpe físico y el sonido resultante es el riesgo técnico dominante. Por encima de aproximadamente 30 ms el golpe deja de sentirse causal y el efecto terapéutico se degrada.

| Fuente | Latencia estimada |
|---|---|
| Tracking del controlador | ~10 ms |
| Un frame a 90 Hz | ~11 ms |
| Buffer de audio a 256 samples / 48 kHz ("Best Latency") | ~5 ms |
| **Total** | **~26 ms** |

Con el valor por defecto de Unity en Android (512 samples) el total sube a aproximadamente 32 ms, que ya resulta perceptible.

**Mitigación adicional — predicción de golpe:** disparar el audio cuando el controlador cruza un plano situado ligeramente por delante del pad, extrapolando el instante de impacto a partir de la velocidad. Es la técnica estándar en percusión virtual y compensa la latencia percibida.

**Esta medición se realiza en la semana 3, no al final del proyecto.** Constituye un hito de go/no-go formal.

### 4.5 Presupuesto de rendimiento (Quest 3)

- Menos de 500 draw calls
- Menos de 300 000 triángulos
- Texturas comprimidas en ASTC
- Iluminación completamente bakeada, sin GI en tiempo real
- Single-pass instanced rendering
- Foveated rendering activado
- Objetivo 72 Hz fijo; 90 Hz si el margen lo permite

---

## 5. Protocolo terapéutico

### 5.1 Estructura de la sesión (~12 minutos)

| # | Fase | Duración | Contenido | Tempo |
|---|---|---|---|---|
| 0 | Onboarding | 60 s | Tutorial: tomar baquetas, golpear un pad, ajustar la altura del kit | — |
| 1 | STAI-6 pre | 40 s | Seis ítems, escala 1-4 | — |
| 2 | Calibración / Iso | 90 s | El usuario toca libremente. El sistema mide su tempo espontáneo mediante la mediana del intervalo entre golpes | Detectado, acotado a 90-120 BPM |
| 3 | Rampa descendente | 6 min | Patrón simple: bombo y tarola alternos más hi-hat. El tempo desciende linealmente | Tempo inicial → 60 BPM |
| 4 | Cierre respiratorio | 2 min | Sin batería. Únicamente bombo cada 5 s alternando inhalación y exhalación, con apoyo visual de expansión | 0.1 Hz = 6 respiraciones/min |
| 5 | STAI-6 post | 40 s | Los mismos seis ítems | — |
| 6 | Resumen | 30 s | Golpes totales, tiempo, variación de ansiedad | — |

### 5.2 Fundamento de los parámetros

- **Fase 2 — iso-principio operacionalizado.** El sistema no asume el estado del usuario: lo mide. Empata su nivel de activación y desde ahí lo desplaza. Convierte un principio clásico de la musicoterapia en un algoritmo verificable.
- **60 BPM como destino.** Corresponde al rango de frecuencia cardiaca en reposo. Es el objetivo del arrastre.
- **6 respiraciones por minuto (0.1 Hz).** Frecuencia de resonancia del barorreflejo, donde la variabilidad de la frecuencia cardiaca se maximiza y se favorece el tono vagal. No es un valor arbitrario.

### 5.3 Máquina de estados

```
Onboarding → STAI-6 pre → Calibración/Iso → Rampa descendente
           → Cierre respiratorio → STAI-6 post → Resumen
```

Cada transición es explícita y registrable. Si el usuario aborta, se registra la fase en la que ocurrió.

### 5.4 Modo libre

Además de la sesión guiada, la aplicación incluye un **modo libre**: el usuario entra al entorno y toca la batería sin protocolo, sin metrónomo y sin evaluación. El entorno responde visualmente a la intensidad de los golpes.

Cumple tres funciones:

1. **Familiarización.** El participante se acostumbra al kit antes de la sesión formal.
2. **Improvisación expresiva.** Corresponde al componente de *drum circle* reportado en la literatura sobre bienestar psicosocial.
3. **Entregable de respaldo.** Si la sesión guiada se atrasa más allá de la semana 8, el modo libre constituye por sí solo un prototipo demostrable. Es la mitigación operativa del riesgo R2.

El modo libre no requiere módulos adicionales: se apoya en M1, M2 y M7, que la sesión guiada ya necesita. Su costo incremental es una pantalla de selección de modo.

---

## 6. Métricas y datos

### 6.1 Variable primaria

**Δ STAI-6 (pre − post).** Hipótesis: reducción significativa intra-sujeto tras una sesión.

### 6.2 Variables secundarias

- Error de sincronía `|t_golpe − t_beat|` en milisegundos, mediana por fase. Hipótesis: mejora conforme avanza la sesión, como indicador de absorción o estado de flujo.
- Tempo espontáneo inicial, como proxy del nivel de activación basal.
- Golpes totales y densidad de golpes por minuto en cada fase.
- Tasa de finalización y de abandono.
- SUS (usabilidad, 10 ítems) y SSQ abreviado (cybersickness), aplicados en papel al terminar.

### 6.3 Esquema de datos

Archivo JSON escrito en `Application.persistentDataPath`, uno por sesión.

```json
{
  "sessionId": "uuid-v4",
  "participantCode": "P07",
  "startedAt": "2026-11-05T10:32:00Z",
  "device": "Quest3",
  "buildVersion": "0.4.2",
  "staiPre": [2, 3, 3, 2, 4, 3],
  "spontaneousTempoBpm": 104,
  "tempoCurve": { "startBpm": 104, "endBpm": 60, "rampSeconds": 360 },
  "hits": [
    { "t": 12.418, "pad": "snare", "velocity": 0.72, "expectedBeatT": 12.400, "errorMs": 18 }
  ],
  "phaseStats": [
    { "phase": "ramp", "hits": 412, "medianErrorMs": 41, "completed": true }
  ],
  "staiPost": [1, 2, 2, 1, 2, 2],
  "endedAt": "2026-11-05T10:44:31Z",
  "abortedAtPhase": null
}
```

### 6.4 Flujo de datos

```
Golpe (M1)
  → evento con timestamp DSP
  → M2 reproduce sample / M5 registra el evento
  → al cerrar sesión, M5 serializa JSON a persistentDataPath
  → extracción mediante adb pull o SideQuest
  → análisis en Python o Excel
  → informe de resultados
```

### 6.5 Privacidad

- Se identifica al participante por código, nunca por nombre.
- No se graba audio ni video.
- Consentimiento informado en papel, firmado antes de la sesión.
- Los datos nacen anonimizados; no existe tabla de correspondencia digital entre código y persona.

---

## 7. Estudio piloto

**Diseño:** pre-post intra-sujeto, una sesión por participante.
**Muestra:** 12-15 voluntarios (estudiantes).
**Naturaleza:** estudio de factibilidad y usabilidad. **No es un ensayo clínico controlado**, y así debe declararse de forma explícita en todos los documentos del proyecto.

**Limitaciones declaradas:**

- Sin grupo control: no cabe en 13 semanas.
- Muestra pequeña y de conveniencia.
- Sesión única: no mide efectos acumulados ni sostenidos.
- Sin medición fisiológica objetiva (HRV); la variable primaria es autoreporte.

Declarar estas limitaciones de antemano protege el trabajo de cuestionamientos metodológicos y demuestra comprensión del método, en lugar de sobrevender los resultados.

---

## 8. Casos borde y manejo de errores

| Caso | Manejo |
|---|---|
| El usuario se quita el visor | Pausar la sesión. Ofrecer reanudar o abortar. Registrar `abortedAtPhase` |
| No golpea nada durante la calibración | Usar 100 BPM por defecto |
| Rebote del control produce doble golpe | Debounce de 60 ms por pad |
| Malestar o mareo | Botón de salida siempre visible. **Cero locomoción**: el usuario permanece fijo, sentado o de pie, lo que reduce el riesgo de cybersickness a prácticamente nulo |
| Batería del visor por debajo de 15 % | Advertir antes de permitir iniciar una sesión |
| Cierre inesperado de la aplicación | `MetricsLogger` realiza escritura parcial cada 30 s |
| Pérdida de tracking del controlador | Pausar y notificar; no registrar golpes espurios |

---

## 9. Estructura de Desglose del Trabajo (EDT)

Descomposición orientada a **entregables**, no a fases del ciclo de vida, siguiendo el mismo criterio que la EDT del proyecto de Control de Inventarios. Componentes nombrados con sustantivos. Regla del 100 % y regla 8/80 aplicadas.

| Código | Componente | Paquetes de trabajo |
|---|---|---|
| **1** | **Fundamentación terapéutica** | 1.1 Marco teórico y estado del arte · 1.2 Protocolo de sesión · 1.3 Instrumentos de medición (STAI-6, SUS, SSQ) · 1.4 Consentimiento informado |
| **2** | **Prototipo VR** | 2.1 Entorno y escena · 2.2 Kit de batería y detección de golpe · 2.3 Motor de audio percusivo · 2.4 Modo libre y selección de modo · 2.5 Guía rítmica y director de sesión · 2.6 Módulo de medición y datos · 2.7 Interfaz de evaluación in-VR |
| **3** | **Estudio piloto** | 3.1 Reclutamiento · 3.2 Ejecución de sesiones · 3.3 Análisis de datos · 3.4 Informe de resultados |
| **4** | **Documentación técnica y de usuario** | 4.1 Manual de instalación y despliegue · 4.2 Guía de operación para el facilitador · 4.3 Documentación de arquitectura |
| **5** | **Gestión del proyecto** | 5.1 Acta constitutiva · 5.2 Plan de alcance · 5.3 EDT y diccionario · 5.4 Cronograma · 5.5 Registro de riesgos · 5.6 Seguimiento (paquetes de 10 días) · 5.7 Cierre |

La rama 5 agrupa el trabajo transversal que no pertenece a un solo entregable, conforme a práctica estándar del PMI y en consistencia con el proyecto anterior del equipo.

---

## 10. Cronograma

| Semana | Fechas | Foco | Hito |
|---|---|---|---|
| 1-2 | 31-ago → 13-sep | Acta, alcance, EDT. Capacitación en Unity y XR en paralelo | Acta aprobada |
| **3** | 14 → 20-sep | **Spike de latencia**: un pad, un sample, medición de golpe a sonido | **Go / No-Go** |
| 4-5 | 21-sep → 4-oct | Kit completo (M1) y motor de audio con velocity y round-robin (M2) | Batería tocable |
| 6-7 | 5 → 18-oct | Guía rítmica sobre `dspTime` (M4) y director de sesión (M3) | Sesión guiada de extremo a extremo |
| 8 | 19 → 25-oct | Módulo de métricas (M5) e interfaz STAI in-VR (M6) | JSON exportable |
| 9 | 26-oct → 1-nov | Entorno, háptico y pulido (M7) | Build candidata |
| 10 | 2 → 8-nov | Pruebas internas, rendimiento, correcciones | **Build estable congelada** |
| 11 | 9 → 15-nov | Ejecución del estudio piloto (N = 12-15) | Datos recolectados |
| 12 | 16 → 22-nov | Análisis estadístico e informe | Informe de resultados |
| 13 | 23 → 30-nov | Cierre documental y presentación | Entrega final |

**Ruta crítica:** spike de latencia → motor de audio → guía rítmica → director de sesión → build estable → pilotaje → informe.

El resto de los componentes tiene holgura. **El congelamiento de funcionalidad en la semana 10 no es negociable:** sin build estable no hay piloto, y sin piloto no hay informe de resultados.

---

## 11. Registro de riesgos

| ID | Riesgo | Prob. | Impacto | Respuesta |
|---|---|---|---|---|
| R1 | Latencia superior a 30 ms degrada la sensación de golpe | Alta | Alto | Spike en semana 3 con decisión go/no-go. Buffer en "Best Latency", predicción de golpe, refuerzo háptico. Plan B: aceptar hasta 40 ms y documentarlo como limitación |
| R2 | La curva de aprendizaje de Unity excede lo estimado | Alta | Alto | Capacitación en semanas 1-2 solapada con la documentación. Partir del template VR de Meta en lugar de arquitecturar desde cero. El modo libre queda como entregable de respaldo si la sesión guiada se atrasa |
| R3 | No se reúnen 12-15 participantes | Media | Medio | Iniciar reclutamiento en la semana 8, no en la 11. Convocar en otras materias |
| R4 | Un solo visor genera cuello de botella en pruebas | Alta | Medio | Agenda de uso compartido. Desarrollo con XR Device Simulator y Quest Link; el visor se reserva para validación |
| R5 | Cybersickness durante el piloto | Baja | Medio | Cero locomoción, sesión de máximo 12 minutos, botón de salida siempre visible |
| R6 | Cuestionamiento del instrumento psicométrico | Media | Medio | Buscar asesoría en la facultad de Psicología. Emplear una versión del STAI validada en español y citar la fuente |
| R7 | Pérdida de datos almacenados en el visor | Baja | Alto | Escritura parcial cada 30 s, `adb pull` inmediatamente después de cada sesión, respaldo en dos ubicaciones |
| R8 | Crecimiento no controlado del alcance | Media | Alto | Exclusiones explícitas asentadas en el acta constitutiva |

---

## 12. Exclusiones explícitas del alcance

Los siguientes elementos **no** forman parte del proyecto:

- Modo multijugador o *drum circle* en red
- Panel web o aplicación de escritorio para el terapeuta
- Hand tracking
- Plataformas distintas a Meta Quest standalone (PCVR, PSVR2, Vision Pro)
- Instrumentos distintos a percusión
- Ensayo clínico controlado con grupo de comparación
- Publicación en Meta Horizon Store
- Integración con sensores fisiológicos (HRV, EDA)

---

## 13. Presupuesto

| Rubro | Monto estimado | Nota |
|---|---|---|
| Meta Quest 3S | ~$299 USD | $499 USD para Quest 3. Si el equipo ya cuenta con el dispositivo, se registra como activo aportado |
| Unity Personal | $0 | Elegible por estar bajo el umbral de ingresos |
| Samples de batería | $0 | Freesound (CC0), Sonatina y otras librerías libres |
| Assets de entorno | $0 – 50 USD | Unity Asset Store o modelado propio |
| Horas-hombre | Rubro dominante | Costear por integrante × semanas |

**Justificación económica para el acta:** el costo marginal por usuario adicional tiende a cero frente a una batería acústica, que exige instrumento, espacio, insonorización y mantenimiento. Adicionalmente, ninguna batería real entrega métricas objetivas de progreso, que es precisamente lo que hace del sistema una herramienta clínica y no solo un instrumento.

---

## 14. Criterios de aceptación

El prototipo se considera aceptado cuando cumple simultáneamente:

1. La latencia medida entre golpe y sonido es menor o igual a 30 ms (o se documenta formalmente la desviación aceptada).
2. La sesión guiada completa se ejecuta de extremo a extremo sin intervención manual, desde el onboarding hasta el resumen.
3. El modo libre es accesible desde la pantalla de selección y permite tocar sin protocolo.
4. La aplicación sostiene 72 Hz estables en Quest 3 durante una sesión completa.
5. Cada sesión produce un archivo JSON válido y completo conforme al esquema de la sección 6.3.
6. Al menos 12 participantes completaron una sesión en el estudio piloto.
7. El informe de resultados reporta la variable primaria y las secundarias.

La documentación PMBOK se considera aceptada cuando los entregables de la rama 5 de la EDT están completos y aprobados por la docente.

---

## 15. Siguiente paso

Elaborar el plan de implementación detallado a partir de este diseño.
