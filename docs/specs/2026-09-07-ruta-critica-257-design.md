# Diseño — Ruta crítica sobre las 257 tareas del equipo

**Fecha:** 7-sep-2026
**Entregable:** documento de ruta crítica en el formato del método, con figuras editables.

## Problema

El líder distribuyó una lista de 257 tareas y una estimación de ruta crítica de 36.9 días
hábiles producida con una herramienta externa, sin explicar el procedimiento. Pidió
verificación independiente: «si te da algo parecido estamos bien».

Además la lista describe un proyecto distinto al del acta v3.0 entregada cuatro días antes.

## Verificación

Se parsearon las 257 tareas del docx y se reconstruyó la red aplicando el criterio declarado
en la figura recibida: 8 h = 1 día, rangos al valor mayor, tareas de seguimiento continuo
excluidas. El resultado fue **36.88 días**, con la misma trayectoria de 28 actividades y las
mismas tres áreas. Coincidencia hasta la centésima.

La aritmética de la estimación previa es correcta. El problema es el modelo.

## Decisiones

| Decisión | Alternativa descartada | Razón |
|---|---|---|
| Desarrollar sobre la red corregida (39.88 d) y demostrar aparte que la original da 36.88 | Desarrollar sobre la red tal como se entregó | Entregar un documento construido sobre una red con 90 cabos sueltos es indefendible ante la docente. La §12 deja constancia de que ambos cálculos coinciden, así que no queda como una descalificación del trabajo del líder. |
| Presentar tres cifras escalonadas | Solo la ruta crítica | 36.9 y 39.9 miden trayectorias; 70.9 mide carga de trabajo. Son magnitudes distintas y la tercera es la que restringe. Presentar solo una induce a planear con el número equivocado. |
| Corrección mínima: 6 dependencias a `QT.8` | Reconstruir todas las dependencias faltantes | Declarar el destino de las 90 tareas terminales exige conocimiento de cada área. Inventarlo desde fuera produciría una red falsa. Se documenta como recomendación 2. |
| Cuatro figuras de distinto zoom | Una sola red de 257 nodos | 257 nodos no caben en una hoja legible. Cada figura responde una pregunta: acoplamiento entre áreas, trayectoria crítica, contexto de holguras, y carga por persona. |
| Fig. 1 como matriz, no como grafo | Grafo de 8 nodos | Se intentó el grafo: con más de 20 enlaces cruzados las flechas atraviesan las cajas y es ilegible. La matriz da el mismo dato sin ambigüedad. |
| PDM / AON | AOA | Las 257 dependencias son puras fin a inicio. AOA exigiría numerar 250+ eventos y decenas de ficticias sin aportar nada. |
| SVG con `svg.fonttype = "none"` | PNG solamente, o SVG con texto convertido a trazos | El usuario pidió poder editarlas en Inkscape. Con `none` el texto sigue siendo texto seleccionable. |
| No tocar acta ni carta sponsor | Realinearlas a la lista nueva | Decisión del usuario. La brecha se documenta aparte para que el equipo decida. |

## Hallazgos

1. **La estimación previa es correcta y reproducible.** 36.88 contra 36.9, misma trayectoria.

2. **90 de 257 tareas (35%) no tienen consecuente.** Suman trabajo real que no llega a ningún
   entregable. Al no tener sucesoras reciben automáticamente toda la holgura, lo que hace
   aparecer como holgadas ramas que no lo son.

3. **`QT.8`, «pruebas con usuarios del prototipo integrado», dependía de tres actividades**
   (`JI.5`, `IR.2`, `AO.5`) y no de la batería, el audio ni la música. Corregirlo suma 3 días.

4. **La ruta crítica no toca el producto.** Atraviesa experiencia emocional, entorno 3D y QA.
   El desarrollo VR termina el día 18.9 con más de 20 días de holgura. La causa real: la rama
   de entorno 3D son 14 actividades estrictamente seriales de una sola persona, 24.88 días.

5. **7 de 8 áreas sobreasignadas.** QA acumula 60 tareas y 70.9 días de carga en una ventana
   de 39.9: 178%. Nadie tiene asignados dirección, gerencia ni coordinación, y esa carga cayó
   dentro de QA.

6. **Medido por carga, el proyecto necesita 70.9 días y hay 49.** El proyecto cabe si se mide
   por ruta crítica y no cabe si se mide por trabajo.

7. **La lista describe otro proyecto que el acta v3.0**: agrega un juego de ritmo completo
   (39 tareas, 36 días), elimina al asesor terapéutico —que fue una corrección exigida por la
   docente— y cambia el enfoque de motriz a emocional. Seis integrantes cambiaron de área y
   hay dos nuevos.

## Entregables

| Archivo | Contenido |
|---|---|
| `entregables/Ruta_Critica_257_Tareas.docx` | 15 secciones, 25 tablas, 4 figuras. Matrices de tiempos, secuencias, información y elasticidad de las 257 actividades. |
| `entregables/figuras-ruta-critica/` | 4 figuras en SVG editable y PNG. |
| `docs/investigacion/brecha-acta-vs-lista-lider.md` | Diferencias contra el acta v3.0 y las tres opciones de reconciliación. |
| `scripts/rc257.py`, `fig257.py`, `gen_rc257_*.py` | Todo reproducible. |

## Fuera de alcance

- Carta sponsor y acta constitutiva: quedan desalineadas a propósito, pendientes de que el
  equipo decida qué proyecto defiende.
- Reconstrucción completa de las dependencias faltantes: requiere a los responsables de área.
- Nivelación de recursos formal: se dan las alternativas, no un cronograma nivelado, porque
  depende de decisiones de alcance que el equipo aún no ha tomado.
