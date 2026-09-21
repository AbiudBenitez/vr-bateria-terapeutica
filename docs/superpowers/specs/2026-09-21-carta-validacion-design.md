# Diseño — Carta de validación y lista de verificación corregida

**Fecha:** 21 de septiembre de 2026 · **Estado:** aprobado
**Proceso PMBOK:** 5.5 Validar el Alcance

---

## 1. Qué se resuelve

El equipo necesita que la docente **valide formalmente** los entregables de medio curso. En
PMBOK eso es *Validar el Alcance*, cuya salida son «entregables aceptados»: no una carta de
cortesía sino un instrumento de aceptación con criterios verificables.

De paso se corrige la lista de verificación, que **no se puede firmar como está**.

## 2. El defecto de la lista actual

`Lista_de_verificacion_compromisos.docx` declara:

> Responsable: Misael — 30 tarea(s) — 24 pendiente(s), **6 completada(s)**

La realidad del área D es **27 de 30**. Veintiuna tareas terminadas, probadas y compiladas
figuran como *Bloqueadas*:

| Clave | Dice | Está |
|---|---|---|
| `DG.1` detección de golpe | Bloqueada | Hecha, con latencia medida |
| `DG.2` identificar la pieza | Bloqueada | Hecha, seis piezas |
| `DG.5` niveles de intensidad | Bloqueada | Hecha, con pruebas |
| `DH.1` `DH.2` háptico | Bloqueada | Hecho, proporcional a la fuerza |
| `DR.1` `DR.2` prueba y corrección | Bloqueada | Hechas |

**El documento lleva línea de firma.** Firmarlo así certifica que trabajo terminado no lo está.

Causa: la lista se generó de la hoja de control, y la hoja nunca se actualizó para el área D.
El resto de la lista sí cuadra — las 56 completadas coinciden con la hoja y las 257 claves con
el cronograma.

## 3. La cifra: 77

Tres fuentes dan tres números distintos:

| Fuente | Terminadas |
|---|---|
| `06_Entregable_Medio_Curso.docx` | 117 de 257 · 42% |
| Hoja de control del equipo | 56 |
| **Cronograma, tras fusionar ambas fuentes** | **77** |

**Se cita 77.** Es la única cifra que un tercero puede reproducir abriendo el cronograma en
ProjectLibre. Si la carta dijera 117 y la docente abre el archivo, encuentra 77 y el documento
pierde autoridad justo donde pide que se le crea.

77 es además defendible: es la **unión** de lo que el equipo registró en su hoja y lo que está
construido, compilado y verificable en el repositorio. Ninguna de las dos fuentes se descarta.

La diferencia con el 117 se declara en la propia carta, no se esconde. Sostener el 117 exigiría
actualizar el cronograma primero —y eso depende de que cada responsable marque sus tareas—, no
cambiar la carta.

## 4. Estructura de la carta

| § | Contenido |
|---|---|
| Encabezado | Institución, materia, docente, equipo, fecha, periodo cubierto |
| 1 | Propósito: solicitar validación conforme a PMBOK 5.5 |
| 2 | Entregables sometidos: documento · contenido · **criterio de aceptación** · dónde verificarlo |
| 3 | Estado del avance, con la fuente de cada cifra |
| 4 | Hito Go/No-Go de latencia: el único resultado medido del proyecto |
| 5 | Limitaciones declaradas: lo que **no** se entrega y por qué |
| 6 | Dictamen: acepta · acepta con observaciones · no acepta |
| 7 | Firmas: gerente de proyecto, coordinadora, docente |

**La sección 5 es la que da credibilidad.** Un documento que solo enumera logros se lee como
autopromoción; uno que declara sus huecos se lee como control de proyecto.

## 5. Criterios de aceptación

Cada entregable lleva un criterio que la docente puede comprobar por su cuenta, sin creer al
equipo:

| Entregable | Criterio verificable |
|---|---|
| Acta constitutiva | 42 paquetes EDT, cada uno con criterio de aceptación, responsable, recursos y duración |
| Ruta crítica | Red PDM de 257 actividades y 417 dependencias; la crítica se recalcula sola en ProjectLibre |
| Costos y presupuesto | Tarifas de fuentes oficiales mexicanas: STPS/ENOE-INEGI, CONASAMI, IMSS. Ninguna estimada |
| Planes de calidad y riesgos | Cobertura PMBOK 8.1–8.3 y 11.1–11.7 |
| Cronograma | 77 de 257 al 100%, abrible en ProjectLibre, con fechas reales |
| **Prototipo VR** | Seis piezas con identificación de pieza e intensidad; **p90 de latencia +4.07 ms** contra criterio de ±25 ms |

## 6. Entregables de este diseño

| Archivo | Qué es |
|---|---|
| `entregables/07_Carta_Validacion_Entregables.docx` | La carta que firma la docente |
| `entregables/08_Lista_Verificacion_Compromisos.docx` | La lista corregida, anexo de la carta |
| `scripts/gen_validacion.py` | Generador de ambos, con el formato neutral del proyecto |

Los dos se generan por script, no se editan a mano: la convención del proyecto es que las
cifras aparecen en varios documentos y deben poder regenerarse cuando cambien.

## 7. Error de datos encontrado en la hoja de control

Tres actividades del área de desarrollo VR figuran en la hoja asignadas a María, bajo el área
«Experiencia emocional»:

| Clave | Actividad |
|---|---|
| `DX.4` | Configurar XR Origin, cámara y seguimiento de cabeza |
| `DB.1` | Crear versión provisional de las baquetas para pruebas |
| `DT.1` | Crear batería provisional con objetos simples |

Son inequívocamente trabajo de desarrollo VR. La atribución errónea infla el avance de María
(21 de 22) y desinfla el de Misael (24 de 30); el total de 77 no cambia.

**No se corrige desde aquí.** La hoja de control es el registro del equipo y reasignar
responsables sin acuerdo sería peor que el error. Queda anotado para que el equipo lo decida.

## 8. Fuera de alcance

No se toca `06_Entregable_Medio_Curso.docx` ni su cifra de 117: es un documento ya entregado y
corregirlo es decisión del equipo, no de este diseño. La carta declara la diferencia y deja el
criterio al lector.
