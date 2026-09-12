# Ruta crítica del proyecto de batería VR — insumos

Preparado el 3-sep-2026 para la entrega del **lunes 7-sep-2026**.
Método y notación: ver [[metodo-ruta-critica-apuntes]].
Fuente de datos: `entregables/Acta_Constitutiva_v2.0.docx` (EDT, Gantt, hitos) y
`entregables/Cronograma_MindView.xml`.

> **Estado:** los cálculos de esta nota ya están hechos y verificados en Python.
> Lo que falta es dibujar el arreglo lógico y decidir cómo se reporta la brecha
> descrita en la sección 6.

---

## 1. Decisión de granularidad

La EDT del acta tiene **42 paquetes de trabajo** más 6 hitos. Una red AOA de 42 flechas
es ilegible en una hoja y no aporta precisión adicional, porque muchos paquetes de una
misma rama son estrictamente secuenciales y comparten responsable.

Se consolidan en **26 actividades con claves A–Z**, agrupando solo paquetes que cumplen
las dos condiciones: mismo responsable y relación secuencial obligada entre ellos.
Cada actividad conserva la trazabilidad a sus paquetes EDT originales.

Los hitos (H1–H6) **no son actividades**: son eventos y se marcan como nodos en la red.

---

## 2. Lista de actividades y matriz de información

Días hábiles, calendario lunes–viernes, excluyendo el 16-sep-2026 (día inhábil).

| Clave | Actividad | Paquetes EDT | Antecedentes | Consecuentes | Días hábiles |
|---|---|---|---|---|---|
| **A** | Acta constitutiva, plan de alcance y EDT | 1.1, 1.2 | — | B | 9 |
| **B** | Cronograma, línea base y registro de riesgos | 1.3, 1.4 | A | — (fin) | 5 |
| **C** | Investigación de musicoterapia y percusión | 2.1 | — | E | 9 |
| **D** | Definición de perfil y búsqueda del asesor | 2.2 | — | E | 9 |
| **E** | Confirmación del asesor terapéutico | 2.3 | C, D | F | 4 |
| **F** | Diseño y validación de rutinas rítmicas | 2.4, 2.5 | E | G, V | 10 |
| **G** | Definición y validación de métricas motrices | 2.6, 2.7 | F | H, W | 10 |
| **H** | Protocolo de sesión, consentimiento y validación final | 2.8, 2.9 | G | Z | 10 |
| **I** | Diseño conceptual y referencias visuales | 3.1 | — | J | 5 |
| **J** | Modelado de batería, baquetas y entorno | 3.2, 3.3 | I | K | 14 |
| **K** | Texturizado y materiales | 3.4 | J | L | 10 |
| **L** | Optimización de geometría para VR | 3.5 | K | R | 10 |
| **M** | Configuración del proyecto Unity y SDK de Meta | 4.1 | — | N, O | 4 |
| **N** | Spike de latencia (Go / No-Go) | 4.2 | M | T | 5 |
| **O** | Mapeo de controles VR | 4.3 | M | P | 10 |
| **P** | Detección de colisiones | 4.4 | O | Q, U | 10 |
| **Q** | Medición de velocidad de impacto | 4.5 | P | R | 5 |
| **R** | Integración de modelos 3D con físicas | 4.6 | Q, L | S | 5 |
| **S** | Ergonomía y prevención de motion sickness | 4.7 | R | W | 5 |
| **T** | Librería de samples, velocity y round-robin | 5.1, 5.2 | N | U | 15 |
| **U** | Integración de audio con físicas | 5.3 | P, T | V | 10 |
| **V** | Implementación de rutinas rítmicas y guía visual | 5.4, 5.5 | U, F | X | 10 |
| **W** | Menús, interfaz adaptativa y registro de métricas | 6.1, 6.2, 6.3 | S, G | X | 10 |
| **X** | Integración general y build candidata | 6.4 | V, W | Y | 5 |
| **Y** | Plan de pruebas y pruebas de rendimiento/latencia | 7.1, 7.2 | X | Z | 10 |
| **Z** | Pruebas con usuarios, corrección, documentación y cierre | 7.3, 7.4, 7.5, 7.6, 1.6 | Y, H | — (fin) | 5 |
**Suma aritmética de duraciones: 214 días hábiles.** No es la duración del proyecto:
la mayoría de las actividades corren en paralelo.

---

## 3. Matriz de secuencias — lectura de paralelismo

Esto es lo que responde directamente la observación de la profesora sobre indicar
qué se puede hacer al mismo tiempo.

| Momento | Actividades simultáneas | Por qué son independientes |
|---|---|---|
| Arranque (día 0) | **A**, **C**, **D**, **I**, **M** | Gestión, investigación terapéutica, búsqueda de asesor, diseño conceptual y configuración de Unity no dependen unas de otras. |
| Semanas 3–5 | **J** (modelado) ∥ **O**/**P** (interacción) ∥ **E**/**F** (terapia) ∥ **N** (spike latencia) | Tres ramas técnicas y una de contenido avanzan en paralelo con equipos distintos. |
| Semanas 5–7 | **K**/**L** (arte) ∥ **P**/**Q** (físicas) ∥ **T** (audio) ∥ **G** (métricas) | Punto de máximo paralelismo: 4 frentes activos. |
| Semanas 8–9 | **S** (ergonomía) ∥ **V** (rutinas) ∥ **W** (UI y métricas) ∥ **H** (protocolo) | Convergen todas en X. |
| Semanas 10–11 | **Y** (pruebas técnicas) → **Z** (pruebas con usuarios y cierre) | Cadena final, sin paralelismo. |

Puntos de convergencia de la red (nodos donde confluyen varias ramas):

- **R** (integración 3D + físicas) requiere **L** y **Q** → une la rama de arte con la de interacción.
- **U** (audio + físicas) requiere **P** y **T** → une audio con interacción.
- **X** (build candidata) requiere **V** y **W** → une audio/rutinas con UI.
- **Z** (cierre) requiere **Y** y **H** → une la rama técnica con la terapéutica.

---

## 4. Matriz de tiempos y elasticidad (calculada)

Origen de tiempos = día 0 = 1-sep-2026.

| Clave | t | TPI | TPT | TRI | TRT | HT | HL | Crítica |
|---|---|---|---|---|---|---|---|---|
| A | 9 | 0 | 9 | 65 | 74 | 65 | 0 |  |
| B | 5 | 9 | 14 | 74 | 79 | 65 | 65 |  |
| C | 9 | 0 | 9 | 16 | 25 | 16 | 0 |  |
| D | 9 | 0 | 9 | 16 | 25 | 16 | 0 |  |
| E | 4 | 9 | 13 | 25 | 29 | 16 | 0 |  |
| F | 10 | 13 | 23 | 29 | 39 | 16 | 0 |  |
| G | 10 | 23 | 33 | 39 | 49 | 16 | 0 |  |
| H | 10 | 33 | 43 | 64 | 74 | 31 | 31 |  |
| I | 5 | 0 | 5 | 0 | 5 | 0 | 0 | **SÍ** |
| J | 14 | 5 | 19 | 5 | 19 | 0 | 0 | **SÍ** |
| K | 10 | 19 | 29 | 19 | 29 | 0 | 0 | **SÍ** |
| L | 10 | 29 | 39 | 29 | 39 | 0 | 0 | **SÍ** |
| M | 4 | 0 | 4 | 10 | 14 | 10 | 0 |  |
| N | 5 | 4 | 9 | 19 | 24 | 15 | 0 |  |
| O | 10 | 4 | 14 | 14 | 24 | 10 | 0 |  |
| P | 10 | 14 | 24 | 24 | 34 | 10 | 0 |  |
| Q | 5 | 24 | 29 | 34 | 39 | 10 | 10 |  |
| R | 5 | 39 | 44 | 39 | 44 | 0 | 0 | **SÍ** |
| S | 5 | 44 | 49 | 44 | 49 | 0 | 0 | **SÍ** |
| T | 15 | 9 | 24 | 24 | 39 | 15 | 0 |  |
| U | 10 | 24 | 34 | 39 | 49 | 15 | 0 |  |
| V | 10 | 34 | 44 | 49 | 59 | 15 | 15 |  |
| W | 10 | 49 | 59 | 49 | 59 | 0 | 0 | **SÍ** |
| X | 5 | 59 | 64 | 59 | 64 | 0 | 0 | **SÍ** |
| Y | 10 | 64 | 74 | 64 | 74 | 0 | 0 | **SÍ** |
| Z | 5 | 74 | 79 | 74 | 79 | 0 | 0 | **SÍ** |
---

## 5. Ruta crítica

```
I → J → K → L → R → S → W → X → Y → Z          79 días hábiles
```

En palabras:

> Diseño conceptual → modelado de batería, baquetas y entorno → texturizado →
> optimización para VR → integración de modelos con físicas → ergonomía →
> menús, interfaz y registro de métricas → build candidata →
> pruebas de rendimiento y latencia → pruebas con usuarios y cierre.

### Hallazgo: contradice lo que declara el acta v2.0

El acta declara como ruta crítica la cadena
`4.1 → 4.2 → 4.4 → 4.5 → 4.6 → 5.3 → 6.4 → 7.2 → 7.3 → 7.6`,
es decir la **rama 4 (interacción y físicas)**.

El cálculo dice otra cosa: la rama 4 tiene **10 días de holgura total** (M, O, P, Q) y
la rama que no admite retraso es la **3 (modelo 3D y entorno)** — I, J, K, L — porque es
una cadena estrictamente secuencial de 39 días con un solo responsable (Artista 3D) y
sin paralelismo interno posible.

**Implicación práctica:** el riesgo dominante del cronograma no es la latencia sino el
**cuello de botella del modelador 3D**. Dos acciones a considerar:

1. Asignar apoyo al modelado (el diseñador UX-XR puede absorber 3.3 baquetas y entorno).
2. Adelantar **I** (diseño conceptual) a la semana 1, ya que no depende de nada.

La declaración del acta debe corregirse o justificarse antes de la entrega del lunes.

### Holguras destacadas

| Rama | Holgura total | Lectura |
|---|---|---|
| 1 Gestión (A, B) | 65 días | Transversal; no condiciona la fecha final. |
| 2 Terapia (C…H) | 16–31 días | Margen amplio para conseguir al asesor. Aun así H2 (confirmación) sigue siendo hito duro. |
| 4 Interacción (M…Q) | 10 días | Contra lo declarado, **no** es crítica. |
| 5 Audio (T, U, V) | 15 días | La más holgada de las ramas técnicas. |
| 3 Modelo 3D (I…L) | **0** | Crítica. |
| 6–7 Cierre (W…Z) | **0** | Crítica. |

---

## 6. Brecha entre la red lógica y el Gantt — resolver antes del lunes

| Cifra | Días hábiles | Equivalente |
|---|---|---|
| Red lógica sin comprimir | 79 | ~16 semanas |
| Ventana del Gantt (1-sep → 13-nov) | 53 | 11 semanas |
| **Traslape aplicado** | **26** | ~5 semanas |

El Gantt del acta arranca varios paquetes antes de que termine su antecedente
(por ejemplo 3.4 texturizado empieza el 28-sep cuando 3.3 termina el 2-oct). La red AOA
solo admite relaciones fin→inicio, así que ese traslape no se puede dibujar directamente.

**Recomendación:** presentarlo como **etapa 7 del método, compresión de la red**, no como
error. Es decir, reportar las dos cifras juntas:

> «La red lógica sin comprimir arroja 79 días hábiles. Aplicando traslape en las ramas 3
> y 4 (fast-tracking de 26 días), la duración programada es de 53 días hábiles, que es la
> que refleja el diagrama de Gantt. El traslape es viable porque las actividades
> involucradas pertenecen a la misma rama y al mismo responsable, que puede alternar
> entre ellas.»

Esto convierte una inconsistencia en una decisión de programación documentada, y de paso
cubre las etapas 6 y 7 del método, que normalmente nadie presenta.

Alternativa si se prefiere una red sin comprimir: subdividir **J** en J-1 (batería) y
J-2 (baquetas y entorno) y colgar **K** solo de J-1. Reduce la brecha pero no la elimina.

---

## 7. Fechas de referencia del Gantt

| Clave | Inicio (Gantt) | Fin (Gantt) | Semanas |
|---|---|---|---|
| A | 1-sep | 11-sep | 9 d |
| B | 7-sep | 11-sep | 5 d |
| C | 1-sep | 11-sep | 9 d |
| D | 1-sep | 11-sep | 9 d |
| E | 14-sep | 18-sep | 4 d |
| F | 21-sep | 2-oct | 10 d |
| G | 5-oct | 16-oct | 10 d |
| H | 19-oct | 30-oct | 10 d |
| I | 7-sep | 11-sep | 5 d |
| J | 14-sep | 2-oct | 14 d |
| K | 28-sep | 9-oct | 10 d |
| L | 5-oct | 16-oct | 10 d |
| M | 14-sep | 18-sep | 4 d |
| N | 21-sep | 25-sep | 5 d |
| O | 21-sep | 2-oct | 10 d |
| P | 28-sep | 9-oct | 10 d |
| Q | 5-oct | 9-oct | 5 d |
| R | 12-oct | 16-oct | 5 d |
| S | 19-oct | 23-oct | 5 d |
| T | 28-sep | 16-oct | 15 d |
| U | 12-oct | 23-oct | 10 d |
| V | 19-oct | 30-oct | 10 d |
| W | 19-oct | 30-oct | 10 d |
| X | 2-nov | 6-nov | 5 d |
| Y | 26-oct | 6-nov | 10 d |
| Z | 9-nov | 13-nov | 5 d |
**Hitos como eventos de la red:**

| Hito | Fecha | Evento tras la actividad |
|---|---|---|
| H1 Diseño conceptual aprobado | 11-sep | I |
| H2 Go / No-Go de latencia | 25-sep | N |
| H3 Modelos 3D integrados con físicas | 16-oct | R |
| H4 Audio, rutinas y métricas integradas | 30-oct | V, W |
| H5 Build estable congelada | 6-nov | X |
| H6 Pruebas cerradas y doc. entregada | 13-nov | Z |

Reserva de gestión: 16–20 nov. Exámenes: a partir del 23-nov.

---

## 8. Pendientes para el lunes

- [ ] Dibujar el arreglo lógico (red AOA) con eventos numerados 0…n, i < j.
- [ ] Identificar las actividades ficticias necesarias en las convergencias R, U, X y Z.
- [ ] Decidir cómo se reporta la brecha de la sección 6 (recomendación: compresión).
- [ ] Corregir o justificar la ruta crítica declarada en el acta v2.0.
- [ ] Evaluar el refuerzo al modelador 3D, que es el cuello de botella real.

Script de cálculo reproducible: la red, duraciones y holguras de este documento se
generaron con un script de CPM en Python; para recalcular tras cualquier cambio de
duraciones o dependencias, rehacer el recorrido hacia adelante y hacia atrás descrito en
[[metodo-ruta-critica-apuntes]] §5.

---

## Ver también

- [[metodo-ruta-critica-apuntes]] — el método
- [[evidencia-musicoterapia]] — fundamentación terapéutica
- `entregables/Acta_Constitutiva_v2.0.docx` — EDT, Gantt y hitos de origen
