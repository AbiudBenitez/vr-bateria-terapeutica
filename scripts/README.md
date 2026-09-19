# Scripts de generación

Todos los documentos y diagramas se generan desde aquí. Si cambia una duración, una
dependencia o una tarifa, se edita el módulo de datos y se regenera: nunca se edita el
Word a mano, porque las cifras aparecen en varios documentos a la vez.

## Módulos de datos

| Archivo | Contiene |
|---|---|
| `pdm.py` | Red PDM del proyecto: 27 actividades, duraciones, dependencias con tipo y demora. Calcula TPI, TPT, TRI, TRT y las cuatro holguras. |
| `edt.py` | Los 42 paquetes de la EDT con criterio de aceptación, responsable, recursos y duración. Deriva las fechas de cada paquete a partir de `pdm.py`. |
| `aoa.py` | Red AOA del ejemplo de aceites esenciales. Mismo cálculo, notación de actividad en la flecha. |
| `neutro.py` | Formato neutral para los Word: estilos por defecto, sin colores ni sombreados. |

## Generadores

```bash
python3 pdm.py                     # imprime la matriz de elasticidad del proyecto
python3 aoa.py                     # imprime la del ejemplo de aceites
python3 edt.py                     # imprime los 42 paquetes con sus fechas

python3 gen_carta.py               # Carta_Sponsor_v2.0.docx
python3 gen_acta_a.py && python3 gen_acta_b.py && \
python3 gen_acta_c.py && python3 gen_acta_d.py    # Acta_Constitutiva_v3.0.docx
python3 gen_mspdi.py               # Cronograma_MindView_v3.xml
python3 gen_rc_proy.py             # Ruta_Critica_Proyecto_Bateria.docx
python3 gen_aceites.py             # Ejemplo_Ruta_Critica_Aceites_Completo.docx
```

El acta se genera en cuatro pasos encadenados a través de `/tmp/_acta_[abc].docx`.
Hay que correrlos en orden.

## Diagramas

Requieren matplotlib, que no está en el Python del sistema:

```bash
python3 -m venv venv && venv/bin/pip install matplotlib
venv/bin/python fig_pdm.py         # red de precedencias y red medida del proyecto
venv/bin/python fig_aoa.py         # arreglo lógico, red medida y ruta crítica del ejemplo
```

Los generadores de Word incrustan los PNG que encuentren, así que hay que **regenerar
primero las figuras y después los documentos**.

---

## Análisis de las 257 tareas (7-sep-2026)

| Archivo | Contiene |
|---|---|
| `tareas_lider.json` | Las 257 tareas extraídas de `referencia/Nomenclatura_Tareas_VR_Bateria_Colores.docx`: clave, descripción, área, tiempo y dependencia. |
| `parse257.py` | Extracción y diagnóstico inicial. Se conserva por trazabilidad; el módulo vigente es `rc257.py`. |
| `rc257.py` | Modelo CPM de las 257 tareas. Calcula dos redes: `ORIG` (tal como se entregó, 36.88 d) y `CORR` (con las dependencias de integración, 39.88 d). |

```bash
python3 rc257.py                   # imprime ambas duraciones y la carga por área
venv/bin/python fig257.py          # las 4 figuras, en SVG y PNG
python3 gen_rc257_a.py && python3 gen_rc257_b.py && python3 gen_rc257_c.py && \
python3 gen_rc257_d.py && python3 gen_rc257_e.py     # Ruta_Critica_257_Tareas.docx
```

Los cinco pasos del documento se encadenan por `/tmp/_rc257_[a-d].docx` y hay que correrlos
en orden.

### Sobre los SVG

`fig257.py` fija `svg.fonttype = "none"`, de modo que en el SVG el texto sigue siendo texto y
en Inkscape se puede seleccionar y editar. Si la tipografía se ve distinta al abrirlo, es
sustitución de fuente: seleccionar todo y cambiarla no rompe nada.

Para volver a exportar tras un cambio de datos conviene editar `rc257.py` y regenerar, en vez
de editar el SVG a mano: las cifras aparecen también en el Word.

---

## Versión 2 del análisis de las 257 tareas (9-sep-2026)

El equipo emitió `referencia/Cambios_Dependencias_VR_Bateria_Nomenclatura_Colores.docx`, que
es un **parche, no una lista completa**: contiene solo las 38 actividades cuya dependencia
cambia, y las claves que indica se **agregan** a las ya declaradas.

`cambios_dep.json` guarda esos cambios ya extraídos y validados (38 actividades, 93
dependencias nuevas, ninguna clave inexistente, ningún duplicado, ningún ciclo).

`rc257.py` calcula ahora tres redes:

| Variable | Red | Duración |
|---|---|---|
| `ORIG` | tal como se entregó el 7-sep | 36.88 d |
| `CORR` | corrección mínima del 7-sep (6 dependencias a `QT.8`) | 39.88 d |
| `V2` | con los 38 cambios del líder — **la vigente** | 45.25 d |

`CORR` quedó superada: con `CAMBIOS` aplicados ya no aporta duración. Se conserva solo para
la sección de contraste del documento.

```bash
python3 rc257.py                   # las tres duraciones y la carga por área
venv/bin/python fig257.py          # las 4 figuras sobre V2, en SVG y PNG
python3 gen_v2_a.py && python3 gen_v2_b.py && python3 gen_v2_c.py && \
python3 gen_v2_d.py && python3 gen_v2_e.py && python3 gen_v2_f.py
```

Los seis pasos se encadenan por `/tmp/_v2_[a-e].docx` y hay que correrlos en orden.
Regenerar **primero las figuras y después el documento**: los generadores incrustan el PNG
que encuentren en disco.

### Cronograma importable de las 257 tareas

```bash
python3 gen_mspdi257.py            # entregables/Cronograma_257_MindView.xml
```

MS Project XML (MSPDI): 8 tareas resumen por área + 257 tareas, 417 vínculos fin→inicio,
8 recursos con sus asignaciones. Arranca el 9-sep-2026; calendario lunes a viernes
08:00–12:00 y 13:00–17:00, con 16-sep y 16-nov inhábiles.

Las duraciones van en **horas**, no en días, porque muchas tareas son de 3 o 5 horas.
Por eso, a partir de la primera tarea fraccionaria la cadena se desplaza del inicio de
jornada y aparecen tareas que empiezan a las 10:00 o a las 14:00. Es correcto: refleja
que una tarea de 5 h no ocupa un día completo. Si se prefiere un Gantt alineado a días
completos, redondear `dur` hacia arriba en `rc257.py` — pero eso alarga el proyecto.

Los vínculos van con `ConstraintType 0` (lo antes posible), de modo que MindView puede
recalcular el cronograma a partir de la red. Las fechas explícitas coinciden con ese
recálculo, así que sirven de respaldo si la herramienta ignorara los vínculos.

---

## Costos, calidad y riesgos (11-sep-2026)

| Archivo | Contiene |
|---|---|
| `costos.py` | Costeo ascendente de las 257 tareas. Tarifas derivadas de fuentes oficiales (Observatorio Laboral STPS, Data México, CONASAMI, IMSS). Perfiles, agregación por grupo y área, costo de la calidad, registro de riesgos y presupuesto. |
| `compresion.py` | Pendientes de costo, curva tiempo-costo iterativa y tabla de simultaneidad. |
| `fig_costos.py` | Curva S, curva de compresión, distribución del costo y matriz de riesgos. SVG + PNG. |

```bash
python3 costos.py                  # presupuesto, escenarios, costo de la calidad
python3 compresion.py              # pendientes y curva de compresión
venv/bin/python fig_costos.py      # las 4 figuras

python3 gen_cost_a.py && python3 gen_cost_b.py && python3 gen_cost_c.py && \
python3 gen_cost_d.py && python3 gen_cost_e.py && python3 gen_cost_f.py   # Analisis_Costos_Calidad_Riesgos.docx

python3 gen_plan_a.py && python3 gen_plan_b.py && \
python3 gen_plan_c.py && python3 gen_plan_d.py                            # Plan_Calidad_Plan_Riesgos.docx
```

Encadenados por `/tmp/_cost_[a-e].docx` y `/tmp/_plan_[a-c].docx`. Correr en orden, y las
figuras antes que los documentos.

### Si hay que cambiar las tarifas

Editar `PERFIL_BASE` en `costos.py`: cada perfil apunta a un ancla de `OFICIAL` con un factor
y su justificación. No tocar los montos a mano en el Word — las cifras aparecen en los tres
documentos y en las cuatro figuras.

## Medición de latencia

| Archivo | Contiene |
|---|---|
| `latencia.py` | Mide la latencia golpe→sonido desde una grabación WAV. Detecta los dos transitorios (clic físico y tambor virtual), los clasifica por razón de centroides espectrales y reporta mediana, p90 y veredicto contra el criterio de −10 a +25 ms. **Solo numpy y la biblioteca estándar**: scipy no carga en el macOS ARM de esta máquina. |
| `test_latencia.py` | 15 pruebas con WAV sintéticos de offset conocido, incluido el caso de Δ negativo y el de transitorios indistinguibles. |

```bash
~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v
~/.pyenv/versions/redes/bin/python scripts/latencia.py mediciones/corrida.wav --etiqueta "con predicción" --detalle
```

El entorno es pyenv `redes` (Python 3.11.9), que es el que tiene numpy. Requiere `pytest`,
instalable con `~/.pyenv/versions/redes/bin/python -m pip install pytest`.

---

## Modelo de costos vigente desde el 14-sep-2026

El equipo son **practicantes bajo convenio escolar**, no empleados. La tarifa se ancla al
**salario mínimo nominal**: $315.04 diarios ÷ 8 h de jornada = **$39.38/h = 1 SM**. Cada perfil
es un múltiplo de esa base, de 1.0 a 2.2 SM según responsabilidad (`PERFIL_BASE` en
`costos.py`).

No dividir el equivalente mensual entre 173.33 h: eso da $55.25 y corresponde al **costo
patronal** de un trabajador de planta, que sí cobra días de descanso. Un practicante no.

| | |
|---|---|
| Mano de obra | $104,013 |
| Costos no laborales | **Ninguno**. Equipo prestado, licencias libres |
| Reserva monetaria | **Ninguna**. Ningún riesgo tiene impacto en dinero |
| Reserva de cronograma | 10.75 días hábiles (49 disponibles − 38.25 de red) |
| **Presupuesto** | **$104,013** |

`RIESGOS` en `costos.py` valora el impacto en **días hábiles**, no en pesos, y `EMV_DIAS` da
9.15 d contra una reserva de 10.75.

`costos.corte(dia)` calcula PV, EV y las actividades terminadas a un corte dado, para la
sección 7.4 de valor ganado. `costos.fecha(n)` convierte índice de día hábil a fecha.

```bash
python3 costos.py                  # presupuesto, reserva, corte de medio curso
venv/bin/python fig_costos.py      # curva S con valor ganado, compresión, distribución, matriz en días

python3 gen_cost_a.py && python3 gen_cost_b.py && python3 gen_cost_c.py && \
python3 gen_cost_d.py && python3 gen_cost_e.py && python3 gen_cost_f.py   # Analisis_Costos_Calidad_Riesgos.docx

python3 gen_plan_a.py && python3 gen_plan_b.py && python3 gen_plan_c.py && \
python3 gen_plan_d.py && python3 gen_plan_e.py                            # Plan_Calidad_Plan_Riesgos.docx

python3 gen_medio.py               # Entregable_Medio_Curso_21sep.docx
```

### Costos en el cronograma de ProjectLibre

`gen_mspdi257.py` incluye tarifas y costos. Crea **un recurso por combinación de persona y
perfil** (13 en total), no uno por persona: Diana ejecuta seis perfiles distintos y una tarifa
promedio daría bien el total pero mal el costo de cada tarea.

Cada recurso lleva `StandardRate` (del perfil), `OvertimeRate` al 150 % para el modelo de
compresión, y `Group` con el área para poder agrupar en ProjectLibre. Cada tarea lleva `Work`,
`Cost`, y las cerradas `ActualCost` y `ActualWork`.

El orden de los elementos sigue el esquema MSPDI, que es estricto. En `<Task>` va:
`… Work, Milestone, Summary, Critical, FixedCost, FixedCostAccrual, PercentComplete,
PercentWorkComplete, Cost, ActualStart, ActualFinish, ActualCost, ActualWork, ConstraintType,
PredecessorLink`. Alterarlo hace que la importación falle en silencio.

---

## Tarea individual: elementos de estudio del PMBOK (14-sep-2026)

| Archivo | Contiene |
|---|---|
| `pmbok.py` | Estructura de la 6.ª edición: 5 grupos, 10 áreas, los 49 procesos, y las entradas y salidas características de cada grupo. Valida que sean 49. |
| `fig_pmbok.py` | Tres figuras: grupos de procesos e interacción, modelo ITTO, matriz áreas × grupos. SVG + PNG. |
| `gen_tarea_a..e.py` | El documento, encadenado por `/tmp/_tarea_[a-d].docx`. |

```bash
python3 pmbok.py                   # verifica la estructura
venv/bin/python fig_pmbok.py       # las 3 figuras
python3 gen_tarea_a.py && python3 gen_tarea_b.py && python3 gen_tarea_c.py && \
python3 gen_tarea_d.py && python3 gen_tarea_e.py
```

**Faltan tres datos en la portada**, marcados como `[COMPLETAR]` en `gen_tarea_a.py`: matrícula,
módulo y nombre de la actividad. Editarlos ahí y regenerar.

El diccionario `EJECUTADOS` de `gen_tarea_d.py` mapea los procesos del PMBOK contra los
entregables reales del equipo. Si se producen documentos nuevos, agregarlos ahí y la cobertura
se recalcula sola.

**Formato de la tarea individual:** Arial 12 en todo el documento. `neutro.nuevo()` acepta
`fuente` y `tam`; internamente llama a `tipografia()`, que fija la fuente en las tres variantes
que Word consulta (ascii, eastAsia y cs) porque cambiar solo la primera deja acentos y símbolos
con la tipografía anterior. Los encabezados se escalan sobre el tamaño base: H1 ×1.45, H2 ×1.20,
H3 ×1.05. La portada usa `neutro.campo()`, que escribe «Etiqueta: valor» con la etiqueta en
negrita, en lugar de una tabla.
