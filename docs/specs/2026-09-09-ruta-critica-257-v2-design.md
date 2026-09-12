# Diseño — Ruta crítica v2 sobre las 257 tareas

**Fecha:** 9-sep-2026
**Entregable:** `entregables/Ruta_Critica_257_Tareas_v2.docx` + 4 figuras regeneradas.

## Problema

El análisis del 7-sep concluyó que la red de dependencias no cerraba: 90 de 257 actividades
no conducían a ningún entregable y solo 91 alcanzaban la actividad final. Se recomendó que
cada área declarara en qué entregable se integra el resultado de sus tareas.

El líder emitió `Cambios_Dependencias_VR_Bateria_Nomenclatura_Colores.docx` haciendo
exactamente eso. Hay que rehacer el cálculo y contrastar.

## Naturaleza del documento de cambios

Es un **parche, no una lista completa**. Lo dice explícitamente: contiene solo las actividades
cuya dependencia debe modificarse, y las claves indicadas se **agregan** a las ya declaradas
en la lista original. El usuario lo notó y preguntó por ello; se confirmó y se documentó en
la §2.4 del entregable.

Validación previa a aplicarlo: 38 actividades destino, 93 dependencias nuevas, todas las
claves existen en las 257, ninguna estaba ya declarada, ningún ciclo introducido.

## Decisiones

| Decisión | Alternativa descartada | Razón |
|---|---|---|
| Usar la red del líder verbatim, sin mis 6 dependencias del 7-sep | Mantener también mi corrección | Se probó: con `CAMBIOS` aplicados, añadir `DR.2`, `MN.2` y `EG.3` a `QT.8` da **0.00 días** de diferencia. Mantenerlas sería ruido y restaría claridad sobre de quién es cada decisión. |
| Sección 12 dedicada al contraste + notas donde el número se movió | Contraste solo woven, o documento aparte | Elección del usuario. Permite leerlo de corrido y por partes. |
| Reportar el desequilibrio de recursos sin proponer reparto concreto | Proponer qué tareas mover y recalcular | Elección del usuario. El reparto es decisión del equipo. |
| Sección 13 con las tres observaciones residuales | Omitirlas | Elección del usuario. Ninguna cambia el número, las tres importan para el control. |
| Archivar v1 en `superadas/` en vez de sobrescribir | Reemplazar el archivo | Ambos análisis se citan mutuamente; la §12 no tendría sentido sin poder consultar el anterior. |

## Resultados

| | v1 recibida (7-sep) | Corrección mía (7-sep) | **v2 del líder (9-sep)** |
|---|---|---|---|
| Duración | 36.88 d | 39.88 d | **45.25 d** |
| Actividades terminales | 90 | 84 | **1** (correcto) |
| Alcanzan el entregable final | 91 de 257 | 97 | **257 de 257** |
| Actividades críticas | 28 | 29 | **34** |
| Actividades en la cadena | 28 | 32 | **32** |
| Áreas en la ruta crítica | 3 | 3 | **4** |

## Hallazgos

1. **Los cambios corrigen el defecto de fondo.** La red pasa de tener 90 cabos sueltos a uno
   solo, que es el correcto (`QX`, la presentación final). Las 257 actividades alcanzan ahora
   el entregable final.

2. **La duración sube 8.37 días.** No es un empeoramiento: es la duración que el proyecto
   siempre tuvo y que la red anterior ocultaba al regalar holgura a las ramas desconectadas.

3. **La ruta crítica sigue sin tocar el producto.** Entorno 3D (17), QA (12), Experiencia
   emocional (4), Interfaz (1). El resultado es ahora *más* sólido, no menos: en v1 podía
   atribuirse al defecto de la red; ya no.

4. **La cadena de Entorno 3D creció de 14 a 17 actividades seriales**, 23.25 de los 45.25 días
   — más de la mitad del proyecto en una sola persona en secuencia estricta. Los cambios le
   agregaron `AA.4`, `AD.1` y `AO.2`, todas dependencias correctas.

5. **El margen cae de 9 a 1.75 días hábiles** (47 disponibles del 9-sep al 13-nov).

6. **El desequilibrio de recursos no se movió**, porque los cambios no tocaron duraciones. QA
   baja de 178% a 157% solo porque su ventana se alargó. 7 de 8 áreas siguen sobreasignadas.

7. **`DR.2` y `MN.2` no alimentan `QT.8`.** Se puede probar el prototipo integrado sin haber
   corregido los errores de la batería. Agregar la dependencia no mueve la fecha final, así
   que es decisión de criterio.

## Fuera de alcance

- Acta constitutiva, carta sponsor y el documento de ruta crítica de los 42 paquetes: siguen
  desalineados a propósito. `docs/investigacion/brecha-acta-vs-lista-lider.md` sigue vigente.
- Propuesta cuantificada de rebalanceo de QA: decisión del equipo.
- Nivelación de recursos formal: depende de decisiones de alcance aún no tomadas.
