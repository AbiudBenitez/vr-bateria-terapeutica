# Diseño — Recorte de alcance del proyecto

**Fecha:** 18 de octubre de 2026 · **Estado:** aprobado, pendiente de plan
**Proceso PMBOK:** 4.6 Realizar el Control Integrado de Cambios · 5.6 Controlar el Alcance

---

## 1. Qué se resuelve

El proyecto registra **93 de 257 actividades terminadas (36 %)** con diecinueve días hábiles
hasta el cierre del periodo. Al ritmo actual no cabe, y el hueco no se reparte parejo: dos
áreas están cerradas y tres apenas han arrancado.

| Área | Hechas | Total | | Responsable |
|---|---|---|---|---|
| Experiencia emocional | 18 | 19 | 95 % | María |
| Desarrollo VR | 27 | 33 | 82 % | Misael |
| Juego de ritmo | 17 | 39 | 44 % | reasignado por R14 |
| QA y gestión | 18 | 60 | 30 % | Diana |
| Interfaz | 9 | 31 | 29 % | Sarai |
| Música | 2 | 20 | 10 % | Javier |
| Sonido | 1 | 23 | 4 % | Christian |
| **Entorno 3D** | **1** | **32** | **3 %** | Kimberly |

La cadena de Entorno 3D tiene **diecisiete actividades estrictamente seriales** en una sola
persona. Diecisiete tareas en fila dentro de diecinueve días hábiles exige una por día sin un
solo tropiezo, y lleva seis semanas sin arrancar. No es un retraso recuperable.

## 2. El criterio del recorte

**Sobrevive lo que sirve a una medida de éxito. Se recorta lo que no sirve a ninguna.**

El criterio no es «lo que dio tiempo». La carta sponsor comprometió **diez resultados
verificables**, no doscientas cincuenta y siete tareas; las tareas eran el camino, las medidas
son el destino. Recortar contra las medidas se defiende; recortar contra el reloj, no.

### 2.1 Estado de las diez medidas

| # | Medida | Estado |
|---|---|---|
| 1 | Identificación de componentes | Cumplida: seis piezas con indicador en el visor |
| 2 | Detección de contacto ≥ 95 % | Funciona; falta la medición formal |
| 3 | Correspondencia del sonido | Cumplida |
| 4 | **Latencia < 30 ms** | **Cumplida y medida: p90 de +4.07 ms** |
| 5 | Estabilidad a 72 fps | Sin medir |
| 6 | Interacción intuitiva | Requiere pruebas con usuarios |
| 7 | Sensibilidad a la intensidad | Cumplida: tres niveles desde la velocidad |
| 8 | **Pertinencia terapéutica** | **Imposible: el asesor nunca se concretó** |
| 9 | Registro de métricas | A un paso; ver §5 |
| 10 | Seguridad de uso | Requiere pruebas con usuarios |

## 3. El recorte

| Área | Hechas | Sobreviven | Se recortan | Nuevo total |
|---|---|---|---|---|
| Desarrollo VR | 27 | 2 | 4 | 29 |
| Juego de ritmo | 17 | 0 | 22 | 17 |
| QA y gestión | 18 | 28 | 14 | 46 |
| Experiencia emocional | 18 | 1 | 0 | 19 |
| Interfaz | 9 | 8 | 14 | 17 |
| Entorno 3D | 1 | 6 | 25 | 7 |
| Música | 2 | 5 | 13 | 7 |
| **Sonido** | **13** | **1** | **9** | **14** |
| **TOTAL** | **105** | **51** | **101** | **157** |

Más una actividad nueva: exportar las métricas de sesión (§5). **De 257 actividades a 157.**

El ritmo exigido baja a **2.7 actividades diarias entre siete personas** hasta el 13 de
noviembre, que sí cabe.

### 3.0 Corrección sobre el conteo de Sonido

La primera versión de este diseño contaba las doce actividades de sonido ya ejecutadas como
«recortadas». **No lo están: están terminadas.** La integración con `DrumHit`, la asignación
por intensidad, la medición del retraso y la normalización de las muestras se hicieron desde
desarrollo VR y nadie las registró en el área que las tenía asignadas.

Eso mueve las hechas de 93 a **105** y el nuevo total de 144 a **157**. El error iba en
contra del proyecto —daba por perdido trabajo real—, pero un recorte que no distingue entre
«hecho» y «cancelado» no sirve para decidir nada.

### 3.1 El porcentaje sube y hay que decir por qué

El avance pasa de **36 % a 67 %**. Conviene declararlo sin rodeos, porque leído solo suena a
maquillaje:

> El numerador sube de 93 a 105 por una razón acotada: doce actividades de sonido estaban
> terminadas y no se habían registrado. El resto del salto es del denominador, que baja de 257
> a 157 por una decisión documentada de recortar alcance. El proyecto no avanzó de golpe: dejó
> de medirse contra trabajo que nunca se iba a hacer.

Un porcentaje que sube sin explicación destruye la credibilidad del resto del documento. Con la
explicación, demuestra control.

## 4. Los recortes grandes, con su razón

### Entorno 3D: de 31 pendientes a 5

**Sobrevive:** límites visuales de seguridad del espacio *(medida 10)*, iluminación definitiva,
una composición de escena con assets de licencia libre, y la optimización al presupuesto de
rendimiento *(medida 5)*.

**Se recorta:** el catálogo de assets, la investigación de teoría del color —**ya existe el
documento de paleta del equipo**—, los elementos ambientales secundarios, la investigación de
qué entorno favorece la experiencia, y la revisión cruzada con experiencia emocional.

El área deja de modelar y pasa a **integrar**. Diecisiete tareas seriales de modelado no caben;
componer una escena con assets libres y optimizarla, sí.

### Sonido: de 22 pendientes a 1

Doce de las veintidós **ya están hechas y nadie las registró**: la integración con `DrumHit`
—que selecciona la muestra por pieza y por intensidad, con dinámica timbral y round-robin— y la
normalización de las 82 muestras a 48 kHz, mono, PCM.

**Sobrevive:** conseguir un platillo crash, que es lo único que falta del kit, y registrar lo
ya hecho.

**Se recorta:** sonidos ambientales, controles de volumen por canal, sonidos de interfaz, y el
**Audio Mixer**.

El mixer se descarta por una razón concreta: añade un nodo al camino del audio y obligaría a
**volver a medir la latencia**, que es la medida 4 y la única ya ganada con margen. El riesgo
de perder una medida cumplida no compensa un control que ninguna medida pide.

### Juego de ritmo: de 22 pendientes a 0

Las quince que la respuesta al riesgo R14 conservó están cerradas. Las otras veintidós ya se
habían recortado en aquel documento —dificultades, modos, combo, pausa, resultados— y esto solo
lo refleja en el cronograma.

### Música: de 18 pendientes a 4

**Sobrevive:** una pista, su BPM exacto, su estructura, y el patrón convertido a beatmap.

**Se recorta:** pistas adicionales, los cinco estilos musicales, las tres versiones de
dificultad por patrón, y las pruebas de comodidad del patrón.

Las dificultades ya no existen por R14, de modo que crear tres versiones de cada patrón no
tiene destino.

### Interfaz: de 22 pendientes a 8

**Sobrevive:** el tutorial *(medida 6, interacción intuitiva)*, la corrección de legibilidad en
el visor, y la implementación en Unity de las pantallas del flujo que se demuestra.

**Se recorta:** la selección de canción y dificultad —las dificultades se recortaron en R14—,
el estilo visual general, y los wireframes de pantallas que no se van a implementar.

## 5. Lo que se protege, y lo que se añade

### QA conserva 28 de 42, a propósito

El informe final (`QI.1`–`QI.5`) **es la entrega** de una materia de administración de
proyectos: nada lo sigue en la red y su ausencia no se compensa con prototipo. Las pruebas con
usuarios (`QV`, `QE`) son las únicas actividades que pueden ganar las medidas 6 y 10.

**Se recorta de ahí:** las ocho de documentación de arquitectura —ya existen la guía de ocho
capítulos y los documentos de diseño— y cinco planes de prueba para componentes que el recorte
deja fuera.

### Una medida que se gana barata

La medida 9, registro de métricas, pide exportar por sesión **precisión temporal, amplitud de
movimiento y constancia del pulso**. El marcador del juego de ritmo **ya calcula la precisión
temporal y la constancia**; falta volcarlas a un archivo.

Son una o dos actividades nuevas y cierran una medida que hoy está en cero. Es el único punto
donde este documento **añade** alcance mientras recorta, y la razón es la desproporción entre
el costo y lo que gana.

## 6. La medida 8 se retira formalmente

El asesor terapéutico externo tenía fecha límite de confirmación el **10 de septiembre** y
nunca se concretó. No es cuestión de tiempo disponible: sin asesor no hay dictamen, y sin
dictamen la medida no se puede verificar por ningún camino.

**Se declara retirada**, se sustituye el respaldo por protocolos publicados de Neurologic Music
Therapy, y se documenta la ausencia de validación terapéutica externa como **limitación
explícita del proyecto**.

Es exactamente la contingencia que el acta constitutiva ya había previsto para este caso. Que
el plan anticipara el fallo y nombrara la salida es, en sí mismo, evidencia de gestión.

## 7. Entregables de este diseño

| Archivo | Qué es |
|---|---|
| `entregables/10_Recorte_de_Alcance.docx` | El documento formal, con firmas |
| `entregables/Cronograma_ProjectLibre.xml` | Las 113 actividades recortadas marcadas como tales |
| `scripts/recorte.py` | Qué sobrevive y qué se recorta, con la medida que lo justifica |
| `scripts/gen_recorte.py` | Generador del documento |

Las cifras se **leen** del cronograma en tiempo de generación, nunca se escriben a mano.

## 8. Cómo se marcan las actividades recortadas

**No se borran.** Una actividad borrada no deja rastro de que existió ni de por qué se quitó, y
el valor de este documento está justamente en que el recorte sea auditable.

Se marcan en el campo de notas de cada tarea con el motivo y la medida que no sirven, y se
agrupan bajo un resumen «Fuera de alcance» para que el Gantt las muestre aparte sin contarlas
en el avance.

**Decisión pendiente de confirmar al implementar:** si ProjectLibre no respeta ese agrupamiento
al recalcular —ya ha costado tres intentos entender su manejo del avance—, la alternativa es
dejarlas en su sitio con la nota y excluirlas del conteo desde `validacion.py`. El documento se
genera igual en los dos casos.

## 9. Fuera de alcance de este diseño

No se toca la carta sponsor ni el acta constitutiva. El recorte es un control de cambios sobre
el alcance vigente, no una reescritura de los documentos fundacionales; la carta conserva sus
diez medidas y este documento declara cuál se retira y por qué.

No se renegocia la fecha de entrega. El recorte busca caber en la ventana existente, no moverla.
