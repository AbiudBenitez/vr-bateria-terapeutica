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
entregables/superados/ Versiones anteriores. No borrar: son evidencia del avance.
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
| `02_Acta_Constitutiva.docx` | EDT de 42 paquetes con criterio de aceptación, responsable, recursos y duración. |
| `Cronograma_MindView_v3.xml` | MS Project XML: 56 tareas, 9 recursos, 65 asignaciones, 48 vínculos con tipo y demora. |
| `Ruta_Critica_Proyecto_Bateria.docx` | Desarrollo PDM/AON completo con justificación. |
| `figuras/` | Red de precedencias y red medida. |

Las versiones anteriores están en `entregables/superados/`. No se borraron.

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
| `entregables/figuras-ruta-critica/` | Las 4 figuras en SVG editable en Inkscape + PNG. |
| `entregables/Cronograma_257_MindView.xml` | MS Project XML: 8 resúmenes de área + 257 tareas, 417 vínculos, 8 recursos. Arranca 9-sep-2026, termina 12-nov. |

La v1 y sus figuras están en `entregables/superados/`.

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
| `03_Ruta_Critica.docx` | Red PDM completa, criterio alineado |
| `05_Analisis_Costos_Calidad_Riesgos.docx` | 14 secciones + 3 anexos. Cubre **7.1 a 7.4**, incluido valor ganado |
| `04_Planes_Costos_Calidad_Riesgos.docx` | Calidad (8.1–8.3), riesgos **11.1 a 11.7**, certificaciones |
| `Entregable_Medio_Curso_21sep.docx` | Compromiso de entrega del 21-sep, derivado del cronograma |
| `Cronograma_ProjectLibre.xml` | 265 tareas, 417 vínculos, **13 recursos con tarifa y costo**, avance real cargado. Total $104,013 |
| `figuras-ruta-critica/` y `figuras-costos/` | 8 figuras, SVG editable + PNG |

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
- ~~Licencia del sample~~ **resuelta**: Dustyroom es CC BY 4.0, atribución en `entregables/ATRIBUCION.txt`.
- **Discrepancia de rol:** el acta v3.0 asigna el desarrollo VR a María Fernanda; lo ejecuta
  Misael. Es carga fuera del rol formal y mueve el cálculo de sobreasignación.

## Juego de ritmo — reloj musical, cerrado el 17-oct-2026

El área de juego de ritmo pasó a desarrollo VR por la respuesta al riesgo R14 (baja de un
integrante). Primera pieza construida: el reloj musical.

| | |
|---|---|
| Spec | `docs/superpowers/specs/2026-10-07-reloj-musical-design.md` |
| Plan | `docs/superpowers/plans/2026-10-10-reloj-musical.md` |
| Código | `TempoMap.cs` · `MusicalTime.cs` · `MusicalClock.cs` · `ClockProbe.cs` |
| Escena | `Cap08_Reloj.unity`, generada por menú |
| Cierra | `JT.1` reloj sin deriva · `JT.2` BPM y duración de beat · `JT.3` compases |

### Verificado: cero deriva

**Desvío de 0.0 ms sostenido durante 205 segundos** contra un metrónomo de 120 BPM exactos.
El criterio era menos de 20 ms sin crecer.

El metrónomo (`Assets/Audio/Pruebas/Metronomo_120BPM.wav`) se genera, no se busca: adivinar
el BPM de una pista mete en la medición la incertidumbre que la medición viene a resolver.
Cada pulso se coloca desde su número de beat y no sumando intervalos — acumular 0.5 s
cuatrocientas veces introduce justo la deriva que se quiere detectar. Verificado con
`scripts/latencia.py`: 420 pulsos, intervalo medio 499.999 ms, error acumulado 0.33 ms.

### Puerta abierta al iso-principio

`ITempoMap` es una interfaz con dos métodos de conversión. La implementación de hoy es de
tempo constante; cuando llegue la rampa que el acta describe —del tempo espontáneo del usuario
hasta 60 BPM— se implementa otro mapa y nada de lo que lo consume cambia.

**Hay una prueba que lo verifica** con un mapa de dos tramos (90 → 60 BPM). Pasó sin tocar
código de producción, que es lo que demuestra que la abstracción aísla de verdad.

### Reglas que no se negocian

1. **La canción se agenda, no se reproduce.** `PlayScheduled(dspTime + margen)` y el reloj
   arranca en ese mismo instante. Llamar a `Play()` y anotar `dspTime` después deja un desfase
   constante que no se nota al principio y es evidente al minuto dos.
2. **Puntuar un golpe no compensa latencia.** `reloj.BeatEn(hit.ImpactDsp)` y ya: `ImpactDsp`
   viene en el mismo reloj DSP que mide la canción. Es lo que cobra el hito Go/No-Go, y por lo
   que `JY` —calibrar latencia entre golpe y música— quedó sin objeto.
3. **Los beats negativos son válidos**: son la cuenta regresiva.

### Lección de la sonda

`AudioSource.isPlaying` devuelve `true` en cuanto la pista queda **agendada**, aunque todavía
no suene. La primera lectura de cada corrida comparaba un reloj en beats negativos contra un
`timeSamples` en cero y reportaba −14.7 ms, que contaminaba el máximo de los tres minutos
siguientes. El defecto era de la sonda, no del reloj.

## Juego de ritmo — jugable, 17-oct-2026

Segunda pieza del área que heredó desarrollo VR por R14. Sobre el reloj musical.

| | |
|---|---|
| Spec | `docs/superpowers/specs/2026-10-17-beatmap-y-juicio-design.md` |
| Plan | `docs/superpowers/plans/2026-10-17-beatmap-y-juicio.md` |
| Código | `Beatmap` · `HitJudge` · `NoteMatcher` · `NoteSpawner` · `Scoreboard` · `JudgePopup` |
| Cierra | `JA.2` `JA.3` · `JB.1`–`JB.3` · `JN.1` `JN.2` · `JW.1` `JW.2` `JW.5` · `JP.1` `JP.3` · `JI.1` |

Con las tres del reloj son **las 15 que R14 conservó**. 79 pruebas en verde.

### Las ventanas van en milisegundos, nunca en beats

```
Perfect ±25 ms · Good ±60 ms · Miss más allá
```

Una ventana en fracciones de pulso se encoge al subir el tempo, y la precisión humana no escala
con el BPM. El ±25 es el criterio Go/No-Go del acta: con un p90 medido de +4.07 ms, la ventana
es **seis veces el error del sistema**. Se mide al jugador, no al motor.

La comparación se hace en tiempo DSP —`hit.ImpactDsp` contra `reloj.DspDelBeat(beat)`—, así que
`HitJudge` no sabe de tempo y sigue valiendo si llega la rampa del iso-principio.

### Cuatro defectos que solo aparecieron en el visor

1. **El `MISS` era inalcanzable por las dos vías.** Una nota no golpeada se contaba sin avisar
   a nadie; y un golpe emparejado tampoco podía darlo, porque `NoteMatcher` busca DENTRO de la
   ventana de Miss y `HitJudge` solo lo devuelve FUERA. Se excluyen.
2. **Dos componentes escribiendo sobre el mismo `TMP_Text`.** Lo causó el cableador al
   «reutilizar el texto existente».
3. **Panel a dieciséis metros.** Posición local colgando de un objeto en `(1.87, 0, 15.98)`,
   creado donde cayó. Una posición local solo vale si controlas dónde está el padre.
4. **El patrón era injugable.** 4 notas/s con dos baquetas. Bajar el hi-hat a la mitad no
   bastó: seguía cayendo en el mismo pulso que el bombo, exigiendo las dos manos a la vez.
   Ahora una nota por pulso, 2/s.

### Reglas nuevas

- **Dos compases de entrada** antes de la primera nota. Sin ellos los fallos iniciales no miden
  precisión, miden que la canción agarró al jugador desprevenido.
- **El veredicto aparece sobre el pad golpeado**, no en un panel arriba: en VR, leer un
  marcador lejano es dejar de ver lo que estás tocando.
- **El tamaño de TMP 3D va en metros.** 0.05 resultó grande; 0.032 se lee sin tapar la pieza.

### Trabajar con el visor sin cable

`scripts/quest.sh` — `wifi` una vez con cable, luego `install`, `ritmo`, `pull`. El modo TCP/IP
se pierde al reiniciar el visor.

## Recorte de alcance — 18-oct-2026

El proyecto pasa de **257 a 158 actividades**. 100 recortadas, 12 que estaban hechas sin
registrar, 1 añadida.

| | |
|---|---|
| Spec | `docs/superpowers/specs/2026-10-18-recorte-de-alcance-design.md` |
| Plan | `docs/superpowers/plans/2026-10-18-recorte-de-alcance.md` |
| Documento | `entregables/10_Recorte_de_Alcance.docx` |
| Datos | `scripts/recorte.py` — única fuente de verdad, con 8 pruebas |

### El criterio

**Sobrevive lo que sirve a una medida de éxito de la carta sponsor. Se recorta lo que no sirve
a ninguna.** No es «lo que dio tiempo»: la carta comprometió diez resultados verificables, no
257 tareas.

### La medida 8 se retira

El asesor terapéutico tenía fecha límite el 10-sep y nunca llegó. Sin asesor no hay dictamen,
así que la medida no se puede verificar por ningún camino. Se sustituye por protocolos
publicados de NMT y se documenta la ausencia de validación externa como limitación explícita
— la contingencia que el acta ya había previsto.

### Los tres recortes grandes

- **Entorno 3D, de 31 a 6.** El área deja de modelar y pasa a integrar assets libres.
  Diecisiete tareas seriales de modelado no caben en diecinueve días.
- **Juego de ritmo, de 22 a 0.** Ya estaban recortadas por R14; esto solo lo refleja.
- **Sonido, de 22 a 1.** Doce ya estaban hechas sin registrar. Solo falta un crash.

### El Audio Mixer se descarta, y por qué

Añade un nodo al camino del audio y obligaría a **remedir la latencia**, que es la medida 4 y
la única ya ganada con margen. Ninguna medida pide un mixer.

### ProjectLibre: dos cosas que NO soporta

**Tareas inactivas.** Escribe `<Active>` en las 265 tareas pero lo ignora: poner `Active=0` y
guardar lo revierte a `1`. Las tareas inactivas son de MS Project 2010+ y ProjectLibre no las
implementa. **Probado el 18-oct con JY; no funciona.** Por eso las recortadas se marcan con una
nota, no desactivándolas.

**Hitos de duración cero al 100 %.** Hay **38 hitos** en el cronograma —`PT0H0M0S`— y
**ninguno puede quedar marcado como completo**: ProjectLibre deriva el porcentaje de la
duración, y sin duración el cociente es cero. Cada vez que alguien abre y guarda el archivo,
los hitos que estuvieran al 100 % vuelven a 0.

Los 38: `AA.1 AB.4 AD.2 AO.3 AR.1 II.3 IS.3 IS.4 JB.1 JB.2 JF.2 JL.2 JM.3 JP.2 JP.3 JW.3 JW.4
JW.5 JY MP.2 MP.3 QB.4 QC.1 QC.4 QC.5 QD.5 QE.3 QE.4 QT.3 SB.1 SB.2 SB.3 SB.4 SB.5 SC.1 SE.4
SM.1 SU`

Explica los sustos de septiembre y octubre: `QC.5` cayéndose tres veces no era capricho de la
herramienta, era estructural. **Tras cada guardado desde ProjectLibre hay que revisar si algún
hito volvió a cero.** Para eso está `scripts/hitos.py`:

```
hitos.py              informe: cuáles cayeron
hitos.py --guardar    anota el estado bueno (correr ANTES de abrir ProjectLibre)
hitos.py --restaurar  devuelve al 100 % los que cayeron
```

### Cuidado al tocar el cronograma

Las recortadas **no se borran**: llevan `[FUERA DE ALCANCE]` y la razón en el campo de notas.
Una actividad borrada no deja rastro de por qué se quitó.

`validacion.py` las excluye del denominador. El avance vigente es **93 de 157 (59 %)**; sube a
105 de 158 (66 %) cuando el área de sonido marque sus doce desde ProjectLibre.

### Ojo con regenerar la carta de validación

`gen_validacion.py` **sigue produciendo la sección 3.1**, que el equipo decidió retirar el
21-sep. Correrlo sobrescribe esa decisión. Hay un aviso en el propio script.

## Métricas de sesión — 18-oct-2026

`DM.1` terminada. Cierra la **medida de éxito 9**, que estaba en cero.

| | |
|---|---|
| Spec | `docs/superpowers/specs/2026-10-18-metricas-de-sesion-design.md` |
| Plan | `docs/superpowers/plans/2026-10-18-metricas-de-sesion.md` |
| Código | `SessionStats.cs` · volcado en `Scoreboard.cs` |
| Evidencia | `entregables/mediciones/sesion_*.json` |

### Dos constancias, no una

- **Contra la rejilla** — desviación típica de los desfases. Qué tan parejo se pega al patrón.
- **Propia** — desviación típica de los intervalos entre golpes. Qué tan estable es su pulso.

**Se puede ir 30 ms atrasado todo el tiempo y tener un pulso perfectamente estable.** Hay una
prueba que lo verifica, y es la que impide que alguien las implemente iguales sin que nadie
lo note.

### La amplitud de movimiento queda fuera

La medida 9 la nombraba, pero es un dato de rehabilitación de miembro superior. El equipo
retiró ese marco antes del corte de medio curso, y sin él la amplitud mide algo que el
proyecto ya no declara. Las dos métricas rítmicas **no necesitan respaldo clínico**: medir si
alguien toca a tiempo es una observación de ejecución musical.

### El archivo lleva los datos crudos

Además del resumen va el arreglo completo de desfases. Un informe que solo lleva promedios no
se puede reanalizar, y el informe final (`QI.1`) va a necesitar gráficas.

### DEUDA: el enfoque del proyecto cambió y los documentos no

El equipo retiró el marco de **rehabilitación motriz** y se quedó con el **emocional**, antes
del corte de medio curso. Ocho documentos siguen afirmando lo contrario: la carta sponsor con
41 menciones, el acta con 48, y este mismo `CLAUDE.md` en «Motriz primario, emocional
secundario».

No es un cambio nuevo — es que los documentos nunca alcanzaron una decisión ya tomada.
**Pendiente de redactar.** Si la docente cruza la carta sponsor con lo que el equipo presenta,
encuentra la contradicción sin explicación.

## Tareas de clase entregadas

| Fecha | Tarea | Carpeta |
|---|---|---|
| 4-sep-2026 | Ejemplo de ruta crítica (aceites esenciales), desarrollo completo hasta ruta crítica | `tareas-individuales/2026-09-04-ejemplo-ruta-critica/` |
