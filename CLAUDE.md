# Proyecto: Simulación de Batería en Realidad Virtual con Enfoque Terapéutico

Contexto persistente para sesiones de Claude Code iniciadas desde esta carpeta.

## Qué es

Proyecto de la materia **Administración de Proyectos de Software**, UANL FIME.
Docente: Dra. Leticia Amalia Neira Tovar. **Equipo A**, 8 integrantes.

Doble entregable:
1. Documentación completa de administración de proyectos conforme a PMBOK.
2. Prototipo VR demostrable, validado con usuarios.

**Periodo:** 1-sep-2026 → 13-nov-2026 (11 semanas). Reserva 16–20 nov. Exámenes inician 23-nov.

## Enfoque terapéutico

**Motriz primario, emocional secundario.** Decidido el 31-ago-2026.

- Objetivo medible principal: coordinación óculo-manual y precisión rítmica.
- Beneficio secundario reportado: relajación y reducción de estrés.
- Marco de referencia: Neurologic Music Therapy (RAS, TIMP, PSE) y el iso-principio.
- Protocolo de sesión: mide el tempo espontáneo del usuario, arranca ahí, desciende a 60 BPM, cierra con fase respiratoria a 6 resp/min.

Ver `docs/specs/2026-08-29-vr-percusion-terapeutica-design.md` para el diseño técnico completo.

## Decisiones técnicas cerradas

| Decisión | Valor | Razón |
|---|---|---|
| Motor | **Unity 6** | Equipo sin experiencia previa + Quest standalone. Unreal se evaluó y descartó: su ventaja visual no aporta valor terapéutico y su pipeline Android cuesta horas que no hay |
| Hardware | Meta Quest 3 + Quest 3S | Standalone, sin PC. Dos visores para no bloquear las pruebas |
| Entrada | Controles, **no** hand tracking | Los controles dan háptico y velocidad confiable; las manos no dan ninguno de los dos |
| Backend | **Ninguno** | App standalone, métricas en JSON local. No se requiere perfil de backend en el equipo |
| Reloj rítmico | `AudioSettings.dspTime` | Nunca `Update()` ni `Time.deltaTime`: el tiempo de frame acumula deriva |
| Presupuesto | $384,201 MXN | Recalculado con tarifas de mercado. La v1.0 del acta declaraba $460,000 sin desglose |

## Riesgo dominante

**Latencia golpe → sonido.** Debe quedar por debajo de 30 ms o el golpe deja de sentirse causal y el valor terapéutico se cae. Presupuesto: tracking ~10 ms + frame a 90 Hz ~11 ms + buffer de audio a 256 samples ~5 ms = ~26 ms.

Se mide en la **semana 4 (25-sep) como hito Go/No-Go**, no al final del proyecto.

## Equipo y roles

| Rol | Persona |
|---|---|
| Director de proyecto | Benjamín Ignacio Villalón Bobadilla |
| Coordinador | Sarai Galindo García |
| Gerente de proyecto | Abiud Misael Benítez Franco |
| Desarrollador VR | María Fernanda Montoya Valdez |
| Diseñador de interacción / UX-XR | Diana Laura Tello Salinas |
| Artista 3D | Christian Salvador Valadez Gallegos |
| Diseñador de audio | Javier Alejandro Hernández Caloca |
| Analista de métricas | Kimberly González Sepúlveda |
| Asesor terapéutico | Externo. Contacto identificado por el líder; confirmación prevista 10-sep-2026. |

## Asesor terapéutico

Perfil: fisioterapeuta, terapeuta ocupacional o musicoterapeuta certificado, con experiencia en rehabilitación de miembro superior. Participación: 4 sesiones, 24 h, $21,600. Fecha límite de confirmación: **10-sep-2026**.

Estado: el líder del equipo tiene contacto identificado. Riesgo bajado de alto a medio. Contingencia si no se concreta: usar protocolos publicados de NMT y documentar la ausencia de validación externa como limitación explícita, ajustando las medidas de éxito 8 y 10 de la carta sponsor.

## Estructura de la carpeta

```
docs/specs/            Diseño técnico y specs de brainstorming
docs/investigacion/    Evidencia de musicoterapia y apuntes del método de ruta crítica
entregables/           Documentos vigentes del proyecto
entregables/figuras/   Diagramas generados (PNG)
entregables/superadas/ Versiones anteriores. No borrar: son evidencia del avance.
referencia/            Fuentes: plantilla, actas originales, PMI 4 y el PDF del método
tareas/                Tareas de clase con fecha (una carpeta por entrega)
```

## Convenciones

- El acta debe seguir la estructura de `referencia/Plantilla_acta_constitutiva.docx`, incluidas las secciones 5 (Consideraciones) y 6 (Apéndice).
- El cronograma se entrega como **MS Project XML**, que MindView 9 importa sin requerir MS Project instalado. De ahí salen el diagrama de Gantt y la vista de esquema/EDT.
- La EDT se descompone por **entregables** (sustantivos), no por fases. Reglas del 100% y 8/80.
- Cada paquete de trabajo lleva **criterio de aceptación** verificable, responsable, recursos y duración.
- Formato de los Word: **neutral**. Estilos por defecto de Word, sin encabezados de color ni sombreados. Helper en el scratchpad: `neutro.py`.
- Los cálculos (CPM, fechas, presupuesto) se generan con scripts, no a mano: `pdm.py` (red del proyecto), `aoa.py` (ejemplo de aceites), `edt.py` (paquetes y fechas).

## Estado al 3-sep-2026 — documentación cerrada hasta la ruta crítica

Cadena documental completa y consistente entre sí:
**Carta sponsor → Acta constitutiva (contiene la EDT) → secuenciación → ruta crítica.**

### Entregables vigentes (`entregables/`)

| Archivo | Qué es |
|---|---|
| `Carta_Sponsor_v2.0.docx` | Revisión 2. Reorienta el proyecto a musicoterapia. Presupuesto $384,201. |
| `Acta_Constitutiva_v3.0.docx` | EDT de 42 paquetes con criterio de aceptación, responsable, recursos y duración. |
| `Cronograma_MindView_v3.xml` | MS Project XML: 56 tareas, 9 recursos, 65 asignaciones, 48 vínculos con tipo y demora. |
| `Ruta_Critica_Proyecto_Bateria.docx` | Desarrollo PDM/AON completo con justificación. |
| `figuras/` | Red de precedencias y red medida. |

Las versiones anteriores están en `entregables/superadas/`. No se borraron.

### Números que deben mantenerse consistentes

- Duración de la red: **50 días hábiles**, 1-sep → **10-nov-2026**
- Ventana disponible: 53 días hábiles (hasta 13-nov); reserva de gestión 16–20 nov; exámenes 23-nov
- Red sin comprimir: 70 días hábiles → **20 días de compresión por traslape**
- Presupuesto: **$384,201 MXN**
- 42 paquetes EDT · 27 actividades de red · 35 dependencias (24 FS, 11 SS)
- **Dos rutas críticas** que convergen en X (build candidata):
  - `M → N → O → P → Q → R → S → W → X → Y-2 → Z` (interacción, UI, pruebas)
  - `M → N → T → U → V → X → Y-2 → Z` (audio, rutinas, pruebas)
- 15 de 27 actividades sin holgura; rama 3D con holgura total de 1 día (cuasi-crítica)

### Decisiones cerradas en esta versión

- **Notación:** PDM/AON para el proyecto (permite representar los traslapes); AOA para el ejemplo de clase de aceites, que es como viene en la fuente.
- **Rebalanceo:** paquete 3.3 (baquetas y entorno) reasignado del Artista 3D al Diseñador UX-XR, y 3.1 adelantado a la semana 1. Con esto la rama 3D dejó de ser la ruta crítica.
- **Asesor terapéutico:** el líder del equipo tiene contacto identificado. El riesgo bajó de alto a medio. Confirmación prevista 10-sep-2026.

### Pendiente de conversación con el equipo

La división de tareas que hizo el líder cubre las ramas 2, 3, 4 y 5, pero **nadie quedó asignado a la rama 1 (gestión), la 6 (menús, interfaz, registro de métricas) ni la 7 (pruebas y documentación)**. Las ramas 6 y 7 están sobre la ruta crítica. Los documentos llevan los roles formales; el anexo A del acta v3.0 tiene la asignación nominal por paquete para poder verificar la cobertura.

## Lista de 257 tareas — estado al 9-sep-2026

El líder trabaja sobre una lista propia de 257 tareas en 8 áreas, que describe una
**simulación VR de batería con juego de ritmo y enfoque emocional**, no la herramienta de
rehabilitación motriz del acta v3.0. Fuentes en `referencia/`:

- `Nomenclatura_Tareas_VR_Bateria_Colores.docx` — las 257 tareas
- `Organizacion_Simulacion_VR_Bateria.docx` — reparto en 8 áreas
- `Cambios_Dependencias_VR_Bateria_Nomenclatura_Colores.docx` — parche del 9-sep

**Antes de tocar carta sponsor o acta, leer `docs/investigacion/brecha-acta-vs-lista-lider.md`.**

### Entregables vigentes

| Archivo | Qué es |
|---|---|
| `entregables/Ruta_Critica_257_Tareas_v2.docx` | El análisis completo. 15 secciones, 30 tablas, 4 figuras. |
| `entregables/figuras257/` | Las 4 figuras en SVG editable en Inkscape + PNG. |
| `entregables/Cronograma_257_MindView.xml` | MS Project XML: 8 resúmenes de área + 257 tareas, 417 vínculos, 8 recursos. Arranca 9-sep-2026, termina 12-nov. |

La v1 y sus figuras están en `entregables/superadas/`.

**Ojo con los dos cronogramas:** `Cronograma_MindView_v3.xml` es de los 42 paquetes del acta
v3.0; `Cronograma_257_MindView.xml` es de las 257 tareas del líder. Son proyectos distintos.

### Evolución del cálculo

| Fecha | Red | Duración | Terminales | Llegan al final |
|---|---|---|---|---|
| 7-sep | tal como se entregó | 36.88 d | 90 | 91 de 257 |
| 7-sep | corrección mínima mía | 39.88 d | 84 | 97 de 257 |
| **9-sep** | **38 cambios del líder** | **45.25 d** | **1** | **257 de 257** |

Los 38 cambios (93 dependencias nuevas) **corrigieron el defecto de fondo**: la red ahora
cierra. Mi corrección del 7-sep quedó superada — con los cambios aplicados aporta 0.00 días.

### Cifras vigentes

- Ruta crítica: **45.25 días hábiles**, 32 actividades, 34 críticas de 257
- Disponible 9-sep → 13-nov: **47 días hábiles**. Margen: **1.75 días**
- Límite real por carga: **70.9 días** (Diana, QA, al 157%)
- 7 de 8 áreas sobreasignadas. Las duraciones no cambiaron, solo las dependencias

### Lo que no cambió con los cambios del líder

- La ruta crítica **sigue sin tocar desarrollo VR ni juego de ritmo**. Ahora es un resultado
  más sólido: ya no puede atribuirse a las tareas que colgaban.
- La cadena de Entorno 3D creció de 14 a **17 actividades seriales**, 23.25 de los 45.25 días,
  en una sola persona (Kimberly). Es el mayor punto de concentración de riesgo.
- Nadie tiene asignados dirección, gerencia ni coordinación; esa carga sigue dentro de QA.

### Observación abierta

`DR.2` (corregir errores de la batería) y `MN.2` (documentación musical) no son predecesoras
de `QT.8` (pruebas con usuarios). Agregarlas no mueve la fecha final — es decisión de criterio,
no de cálculo.

### Convención de figuras

Los diagramas se exportan en **SVG** (`svg.fonttype = "none"`, texto editable en Inkscape) y
PNG. Ver `scripts/README.md`.


## Estado al 14-sep-2026

### Criterio de duración (desde el 11-sep)

`rc257.py` usa **`min()`** para los rangos, alineado con la hoja de control del equipo.
Red **38.25 días hábiles**, 7-sep → 30-oct. Esfuerzo **1,978 h**. Cadena crítica 28 actividades,
con la cola en el **informe final** (`QI.1`–`QI.5`), no en la build.

### MODELO DE COSTOS — leer antes de tocar cifras

El equipo son **practicantes bajo convenio escolar**, no empleados. Tarifa anclada al
**salario mínimo nominal**: $315.04 diarios ÷ 8 h = **$39.38/h = 1 SM**.

**No dividir el mensual entre 173.33 h.** Eso da $55.25 y es el *costo patronal* de un
trabajador de planta que cobra días de descanso. Un practicante no los cobra.

Cada perfil es múltiplo del SM según responsabilidad, de 1.0 (redactor) a 2.2 (director).
Definido en `PERFIL_BASE` de `scripts/costos.py`, cada uno con su justificación.

| | |
|---|---|
| Tarifa media | **$52.58/h** (1.34 SM) |
| Mano de obra | **$104,013** |
| Costos no laborales | **Ninguno** — visores prestados, licencias libres, Unity gratuito |
| Reserva monetaria | **Ninguna** — ningún riesgo tiene impacto en dinero |
| Reserva de cronograma | **10.75 d** (49 disponibles − 38.25 de red) |
| **Presupuesto** | **$104,013** |

### Riesgos en días, no en pesos

Como el proyecto no compra ni contrata, **ningún riesgo tiene impacto monetario**. El registro
valora el impacto en **días hábiles** y en degradación de alcance. EMV = **9.15 días** contra
una reserva de 10.75. Alcanza, con 17% de margen.

Advertencia documentada: si R1, R2 y R5 se materializaran juntos serían 15 días y no alcanzaría.

### Evolución del presupuesto — no repetir los errores

| Versión | Supuesto | Presupuesto |
|---|---|---|
| 1ª | Tarifas de mercado sin fuente + compras | $559,891 |
| 2ª | Observatorio Laboral (profesionistas) + equipo prestado | $294,981 |
| **3ª vigente** | **Salario mínimo escalado (practicantes) + sin compras** | **$104,013** |

Cada corrección acercó la estimación a lo que el proyecto realmente es. No volver a estimar
tarifas sin fuente oficial.

### Entregables vigentes

| Archivo | Qué es |
|---|---|
| `Ruta_Critica_257_Tareas_v3.docx` | Red PDM completa, criterio alineado |
| `Analisis_Costos_Calidad_Riesgos.docx` | 14 secciones + 3 anexos. Cubre **7.1 a 7.4**, incluido valor ganado |
| `Plan_Calidad_Plan_Riesgos.docx` | Calidad (8.1–8.3), riesgos **11.1 a 11.7**, certificaciones |
| `Entregable_Medio_Curso_21sep.docx` | Compromiso de entrega del 21-sep, derivado del cronograma |
| `Cronograma_257_ProjectLibre.xml` | 265 tareas, 417 vínculos, **13 recursos con tarifa y costo**, avance real cargado. Total $104,013 |
| `figuras257/` y `figuras_costos/` | 8 figuras, SVG editable + PNG |

Cobertura PMBOK completa: área 7 de 7.1 a 7.4, área 11 de 11.1 a 11.7.

### Corte de medio curso (cierre del 18-sep)

**117 de 257 actividades · 838 de 1,978 h · 42% del esfuerzo.**
PV $47,562 · EV $46,097 · **SPI 0.969**.

Titular: *prototipo jugable de batería VR con ritmo y sonido, más la planeación completa.*

Sarai va con solo 2 tareas cerradas contra 27 de Misael. **No es retraso**: la interfaz arranca
tarde por diseño de la red. Está explicado en el §5 del documento de medio curso.

### Pendiente de registrar

El valor ganado solo calcula PV, EV y SPI. **Falta registrar horas reales** por actividad —
sin ese dato no hay AC ni CPI, y la mitad del método queda inutilizable. Recomendación 4 del
documento de costos.

## Prototipo — etapa A, estado al 16-sep-2026

Proyecto Unity en `/Users/abiudbenitez/Documents/code/Unity/BateriaVR` (repo git propio, aparte
de esta carpeta). Unity 6000.5.10f1 · OpenXR 1.18 · XRI 3.6.0.

**Capítulo 4 cerrado: el pad suena al golpearlo, con háptico y con el volumen variando según la
fuerza.** 21 pruebas EditMode en verde. Lo que sigue es el capítulo 5, la medición de latencia,
que es el **hito Go/No-Go del acta, fechado en la semana 4 (25-sep)**.

| | |
|---|---|
| Guía | `entregables/guia/Guia_Bateria_VR_A.md` — 8 capítulos |
| Spec | `docs/superpowers/specs/2026-09-12-guia-bateria-vr-unity-design.md` |
| Código espejo | `proyecto-unity/Assets/` en esta carpeta |
| Medición | `scripts/latencia.py` + 15 pruebas. **Solo numpy**: scipy no carga en este macOS ARM |

### Entorno

Quest 3S. **Quest Link no está disponible** — ninguna máquina tiene GPU dedicada compatible.
Ciclo: Meta XR Simulator en la Mac, y build APK + `adb` al visor para velocidad real de mano,
latencia y háptico.

### Tres bugs resueltos, con su lección

1. **El jugador caía sin parar.** Se usó el prefab `XR Origin (XR Rig)` de los Starter Assets
   (el rig de demo, con locomoción completa) y había quedado inclinado 50°. Su `GravityProvider`
   aplica gravedad en espacio **local** y el `CharacterController` trae `SlopeLimit: 45`: a 50°
   el suelo horizontal deja de contar como piso pisable. Usar `XR Origin (VR)` del menú.
2. **Golpeaba y no sonaba nada.** El array `Targets` del `DrumHitFanout` estaba vacío: los golpes
   se detectaban y se descartaban sin un solo mensaje.
3. **El pad quedaba a 1.43 m.** La distancia que importa es la que separa el pad del `XR Origin`,
   no la posición del pad sola. **Dejar el `XR Origin` en (0,0,0)** y colocar los pads relativos.

Los tres comparten forma: **el síntoma no se parecía a la causa.** Por eso `DrumHitFanout`,
`StickTracker` y `DrumVoice` ahora validan sus referencias en `Awake` con `LogError`, y
`EscenaRigTests` vigila que el rig siga derecho y sin locomoción.

### Reglas del código que no se negocian

1. `AudioSettings.dspTime` se lee **una vez por frame**. Nunca `Time.time` ni `Time.deltaTime`.
2. **Cero asignaciones en el camino del golpe.** `AddComponent` solo en `Awake`.
3. Rearme del pad **por posición, no por tiempo**: semicorcheas a 160 BPM son 94 ms.
4. `deviceVelocity` viene en espacio del **XR Origin**; `pad.Normal` está en **mundo**. Convertir
   con `xrOrigin.TransformVector()`. Mezclarlos solo falla cuando el jugador gira.

### Criterio Go/No-Go de latencia

**−10 ms ≤ Δ(p90) ≤ +25 ms**, con el protocolo del clic físico. Δ **negativo es válido**: la
predicción del plano armado adelanta el sonido. Decide el p90, no la mediana. El sample debe ser
de **bombo** — ya está puesto `512175__kopreusz__kick_2.wav`.

### Pendiente antes del capítulo 5

- **Apagar los dos `DiagnosticoMano`**: imprimen cada frame, 144 líneas/s a dos manos. Cuestan
  frames reales en el visor y contaminarían la medición.
- Confirmar la **licencia del sample** antes de meterlo al repositorio.
- **Discrepancia de rol:** el acta v3.0 asigna el desarrollo VR a María Fernanda; lo ejecuta
  Misael. Es carga fuera del rol formal y mueve el cálculo de sobreasignación.

## Tareas de clase entregadas

| Fecha | Tarea | Carpeta |
|---|---|---|
| 4-sep-2026 | Ejemplo de ruta crítica (aceites esenciales), desarrollo completo hasta ruta crítica | `tareas/2026-09-04-ejemplo-ruta-critica/` |
