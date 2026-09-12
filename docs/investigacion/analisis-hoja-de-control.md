# Análisis de la hoja de control de tareas

**Archivo:** `Hoja de control de tareas.xlsx`, hoja única «Tareas», 257 filas × 13 columnas.
**Fecha del análisis:** 11-sep-2026.

---

## 1. Qué contiene

| Columna | Contenido |
|---|---|
| Etapa | Nivel topológico, del 1 al 32 |
| Clave | La clave de la nomenclatura, `DP.1`, `JA.1`, etc. |
| Área | Una de las ocho áreas |
| Tarea | Descripción |
| Responsable | Nombre de pila del integrante |
| Estado | Sin empezar · En curso · Completado · Bloqueada |
| Duración | Tal como viene en la nomenclatura, incluidos los rangos |
| Dependencia | Claves antecedentes, o `-` |
| Fecha de inicio / de término | Programadas |
| Fecha real de término | Capturada al cerrar la tarea |
| Ruta crítica | `si` / `no` |
| Observaciones | Libre |

---

## 2. Verificación: está bien construida

Se comprobó fila por fila contra la red del documento de ruta crítica.

| Comprobación | Resultado |
|---|---|
| Número de claves | 257, sin duplicados |
| Correspondencia con la nomenclatura | **1 a 1**. Ninguna clave sobra ni falta |
| Duraciones | **Las 257 idénticas** al documento de origen |
| Dependencias | **Las 417 coinciden exactamente** con la red v2, incluidos los 38 cambios del 9-sep |
| Tareas sin antecedente | 11, las mismas de la red |
| Violaciones de dependencia en las fechas | **Cero de 417.** Ninguna tarea arranca antes de que termine su antecedente |
| Fechas en fin de semana o feriado | Ninguna |
| Columna «Etapa» | 32 niveles topológicamente válidos, cero violaciones |
| Coherencia del estado «Bloqueada» | Correcta: ninguna tarea sin antecedentes está marcada bloqueada |

**No es un Excel improvisado.** Quien lo armó respetó la red completa.

---

## 3. La discrepancia: criterio de duración

Era la única diferencia de fondo.

**La hoja toma el valor menor de los rangos; los documentos tomaban el mayor.**

| Criterio | Duración de la red | Esfuerzo |
|---|---|---|
| Rangos al **mayor**, fracción de día — documentos hasta el 11-sep | 45.25 d | 2,146 h |
| Rangos al **menor**, fracción de día | 38.25 d | 1,978 h |
| Rangos al menor, día entero | 39.00 d | 1,978 h |
| Rangos al mayor, día entero | 47.00 d | 2,146 h |

La hoja va del 7-sep al 29-oct = 38 días hábiles, que corresponde al criterio del menor.

Solo 18 de las 257 tareas tienen rango, pero tres están sobre la ruta crítica —`MA.1`, `AO.6`
y `QB.3`— y ahí se concentra casi todo el efecto.

### Resolución

**Se adoptó el criterio de la hoja.** Los documentos se regeneraron:

| | Antes | Ahora |
|---|---|---|
| Duración de la red | 45.25 d | **38.25 d** |
| Esfuerzo | 2,146 h | **1,978 h** |
| Presupuesto total | $315,034 | **$294,981** |
| Actividades en la cadena crítica | 32 | **28** |

La razón de ceder al criterio del equipo y no al contrario: mantener dos cifras distintas de
duración entre el análisis y la hoja de seguimiento garantizaba que tarde o temprano alguien
tomara una decisión con el número equivocado.

### Efecto cualitativo

Con duraciones menores, `QB.3` baja de 3 días a 1 y la rama de build deja de ser la cola
crítica. **La ruta crítica ahora termina por la rama del informe final** (`QI.1` a `QI.5`),
no por la de la build. Es un cambio de foco que conviene tener presente: el cuello final del
proyecto es documental, no técnico.

---

## 4. Defectos encontrados

### 4.1 Dos fechas invertidas

| Clave | Inicio | Término | Duración |
|---|---|---|---|
| `EO.1` | 8-sep | **7-sep** | 4 horas |
| `EB.1` | 9-sep | **8-sep** | 2 días |

El término es anterior al inicio. Son las únicas dos de 257.

### 4.2 La columna «Ruta crítica» ya está obsoleta

Marca 32 tareas. Con el criterio de duración que la propia hoja usa, la cadena crítica son 28,
y no son las mismas.

| | Claves |
|---|---|
| Marcadas como críticas pero **ya no lo son** | `QE.3` `QE.4` `QE.5` `QV.1` `QV.2` `QB.1` `QB.2` `QB.3` `QB.4` |
| **Críticas pero no marcadas** | `QI.1` `QI.2` `QI.3` `QI.4` `QI.5` |

Son **14 filas mal marcadas**, y el error no lo cometió nadie: la columna se escribió a mano
con la ruta crítica correcta de ese momento, y dejó de serlo cuando cambió el criterio de
duración. Nadie se entera porque la celda no se recalcula.

Esto es lo que mejor ilustra el límite de la hoja de cálculo.

---

## 5. Estado actual del proyecto

| Estado | Tareas |
|---|---|
| Completado | 9 |
| En curso | 1 (`QC.2`, seguimiento) |
| Sin empezar | 12 |
| Bloqueada por dependencias | 235 |

Completadas: `JA.1` `EO.1` `EO.2` `EB.1` `EB.2` `EB.3` `EB.4` `ML.1` `ML.2`. Casi todas de
María, en fundamentación bibliográfica, más dos de Javier en licencias musicales.

Vale la pena notar que **la rama del entorno tridimensional, que es la crítica, no ha
arrancado**. Es la que más conviene destrabar.

---

## 6. Migración a ProjectLibre

### Por qué, en una frase que sirve para la exposición

> En la hoja de cálculo, la ruta crítica y las fechas son datos escritos a mano que se
> desactualizan solos; el software los recalcula. La prueba está en que la columna de ruta
> crítica de la hoja ya tiene 14 filas incorrectas sin que nadie lo notara.

### Qué se pierde y qué no

ProjectLibre cubre **todas** las columnas de la hoja:

| Columna de la hoja | Equivalente en ProjectLibre |
|---|---|
| Etapa | Se deriva de la red; no hace falta mantenerla |
| Clave, Área, Tarea | Nombre y estructura de esquema |
| Responsable | Recurso asignado |
| Estado | % completado |
| Duración | Duración |
| Dependencia | Vínculos de precedencia |
| Fechas de inicio y término | **Calculadas**, no capturadas |
| Fecha real de término | Fin real |
| Ruta crítica | **Calculada y resaltada**, no escrita |
| Observaciones | Notas de la tarea |

### El archivo

`entregables/Cronograma_257_ProjectLibre.xml`, en formato MS Project XML:

- 8 tareas resumen por área + 257 tareas
- 417 vínculos fin → inicio
- 8 recursos con sus asignaciones
- Arranque **7-sep-2026**, fin **30-oct-2026**
- **El avance ya está cargado:** las 9 completadas al 100 % con su fecha real, y `QC.2` al 50 %
- Calendario lunes a viernes, 08:00–12:00 y 13:00–17:00, con 16-sep y 16-nov inhábiles

Se importa con *Archivo → Abrir* y eligiendo el tipo XML.

### Cómo trabajar a partir de aquí

1. Una sola persona, el gerente de proyecto, mantiene el archivo. Evita conflictos de versión.
2. Cada integrante reporta su avance en la reunión semanal; el gerente lo captura.
3. El archivo se versiona en el repositorio con fecha en el nombre.
4. **La hoja de cálculo se retira.** Si alguien necesita una vista tipo tabla, ProjectLibre
   exporta a CSV.

### Si hay que regenerar

`python3 scripts/gen_mspdi257.py`. Lee la red de `rc257.py` y el avance de `hoja.json`. No
editar el XML a mano.

---

## Ver también

- `entregables/Cronograma_257_ProjectLibre.xml` — el cronograma a importar
- `docs/investigacion/alternativas-software-gestion-proyectos.md` — cómo hacer que ProjectLibre abra en Mac con chip ARM
- `entregables/Ruta_Critica_257_Tareas_v3.docx` — el análisis con el criterio ya alineado
