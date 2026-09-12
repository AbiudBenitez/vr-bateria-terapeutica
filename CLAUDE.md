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


## Estado al 11-sep-2026 — criterio de duración alineado con el equipo

### CAMBIO DE CRITERIO — leer antes de tocar cualquier cifra

El equipo mantiene `referencia/Hoja de control de tareas.xlsx` con las 257 tareas. Se verificó
fila por fila: claves, duraciones, las 417 dependencias y la ruta crítica **coinciden con la
red v2**. Cero violaciones de dependencia en las fechas.

La única discrepancia era el criterio de rangos. **Se adoptó el del equipo: rangos al valor
MENOR.** `rc257.py` usa `min()`, no `max()`.

| | Antes (mayor) | Ahora (menor) |
|---|---|---|
| Duración de la red | 45.25 d | **38.25 d** |
| Esfuerzo | 2,146 h | **1,978 h** |
| Presupuesto | $315,034 | **$294,981** |
| Cadena crítica | 32 act. | **28 act.** |

Efecto cualitativo: la cola crítica pasó de la rama de build (`QB`) a la del **informe final**
(`QI.1`–`QI.5`). El cuello final del proyecto es documental, no técnico.

### Cifras vigentes

| | |
|---|---|
| Red | **38.25 días hábiles** · 7-sep → 30-oct |
| Disponible 7-sep → 13-nov | 49 días hábiles · margen **10.75 d** |
| Esfuerzo | 1,978 h · tarifa media $113.72/h |
| Mano de obra | $224,931 |
| **Línea base de costos** | **$280,981** |
| **Presupuesto total** | **$294,981** |
| Costo de la calidad | $40,403 · 18.0% |
| Compresión | 38.25 → 34.15 d por $1,964 |
| Carga QA (Diana) | 511 h en ventana de 306 h = **167%** |
| Áreas sobreasignadas | **6 de 8** |

### Entregables vigentes

| Archivo | Qué es |
|---|---|
| `Ruta_Critica_257_Tareas_v3.docx` | Análisis con el criterio alineado. Control del documento explica el cambio. |
| `Analisis_Costos_Calidad_Riesgos.docx` | Costeo ascendente, presupuesto, simultaneidad, compresión, calidad y riesgos. |
| `Plan_Calidad_Plan_Riesgos.docx` | Los dos planes + certificaciones. |
| `Cronograma_257_ProjectLibre.xml` | MS Project XML con **el avance real cargado**: 9 tareas al 100%, `QC.2` al 50%. Arranca 7-sep. |
| `figuras257/` y `figuras_costos/` | 8 figuras, SVG editable + PNG. |
| `docs/investigacion/analisis-hoja-de-control.md` | Verificación de la hoja y plan de migración. |
| `docs/investigacion/reparto-exposicion-costos.md` | Guion de exposición para los 8, con cifras y preguntas probables. |

### Tarifas — NO estimar sin fuente

Solo fuentes oficiales mexicanas. Observatorio Laboral (STPS/ENOE-INEGI) TIC $21,697/mes y
promedio profesionistas $19,494/mes · Data México $11,000/mes · CONASAMI $315.04/día · IMSS
$662.80/día. Conversión: mensual ÷ 173.33 h. Factores por perfil en `PERFIL_BASE` de
`scripts/costos.py`.

Una versión previa usó tarifas a ojo y dio $559,891; la docente dijo que estaba muy caro y
tenía razón.

### La hoja de Excel se retira

`Cronograma_257_ProjectLibre.xml` es el plan único. Argumento para la docente: **la columna
«Ruta Crítica» de la hoja ya tiene 14 filas incorrectas** (9 marcadas que ya no lo son, 5
críticas sin marcar) porque es un valor escrito a mano que no se recalcula. ProjectLibre lo
recalcula solo.

Defectos menores de la hoja: `EO.1` y `EB.1` tienen fecha de término anterior al inicio.

### Avance real al 11-sep

9 completadas (`JA.1` `EO.1` `EO.2` `EB.1` `EB.2` `EB.3` `EB.4` `ML.1` `ML.2`), 1 en curso
(`QC.2`), 12 sin empezar, 235 bloqueadas. **La rama del entorno 3D, que es la crítica, no ha
arrancado.**

### Reparto de la exposición

Misael método · Benjamín tarifas · Kimberly agregación · Christian presupuesto · Javier
escenarios · Sarai simultaneidad · María compresión · Diana calidad, riesgos y cierre.

## Tareas de clase entregadas

| Fecha | Tarea | Carpeta |
|---|---|---|
| 4-sep-2026 | Ejemplo de ruta crítica (aceites esenciales), desarrollo completo hasta ruta crítica | `tareas/2026-09-04-ejemplo-ruta-critica/` |
