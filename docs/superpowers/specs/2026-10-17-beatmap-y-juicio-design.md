# Diseño — Beatmap y juicio del golpe

**Fecha:** 17 de octubre de 2026 · **Estado:** aprobado, pendiente de plan
**Cubre:** `JA.2` datos de una nota · `JA.3` estructura de canciones y beatmaps ·
`JB.1` prototipo de beatmap · `JB.2` cargar un beatmap · `JB.3` sincronizar con la música ·
`JN.1` representación visual de las notas · `JN.2` indicar qué componente golpear ·
`JW.1` ventanas Perfect/Good/Miss · `JW.2` detección de golpes correctos ·
`JW.5` detección de notas no golpeadas · `JP.1` puntuación · `JP.3` precisión ·
`JI.1` integrar el evento DrumHit

---

## 1. Qué se construye

El juego de ritmo sobre el reloj musical ya verificado. Notas colocadas en beats, que aparecen
antes de su momento, caen hacia la pieza que les toca, y se juzgan contra el golpe real del
jugador.

**Restricción de fecha:** hay una demostración el miércoles 21 de octubre, con dos días hábiles
por delante. El alcance está acotado a lo que se puede demostrar funcionando, y el orden de
construcción va por valor demostrable, no por elegancia.

**No depende del equipo.** El metrónomo de 120 BPM exactos ya en el repositorio es pista válida
para autorizar y demostrar un beatmap completo. Si el área de música no entrega a tiempo, la
demostración existe igual.

## 2. Arquitectura

| Pieza | Responsabilidad | Probable sin hardware |
|---|---|---|
| `Beatmap` | `ScriptableObject` con la lista de notas y los metadatos de la pista | — |
| `HitJudge` | Clase pura: desfase en milisegundos → Perfect, Good o Miss | Sí |
| `NoteSpawner` | Saca las notas antes de su beat y las mueve hacia su pieza | En play |
| `Scoreboard` | Cuenta aciertos y precisión, y los muestra | En play |

Se sigue el patrón del proyecto: `DrumKitPiece` ya es un `ScriptableObject` creado desde el
menú **Batería**, y `CrossSolver` y `HitIntensity` ya son clases puras probadas sin escena.

### 2.1 Por qué ScriptableObject y no un formato de texto

Se evaluó un formato de texto que el área de música pudiera editar sin intervención del
desarrollo. **Se descarta**: el equipo no va a autorizar beatmaps por su cuenta en la ventana
que queda, de modo que la autonomía que compraba el parser no se usaría, y su coste —parseo,
validación, mensajes de error con número de línea— sí se pagaría.

Queda anotado como la decisión que habría que revisar si el proyecto continuara: con tres
dificultades por pista más las correcciones de comodidad, el desarrollo se vuelve el cuello de
botella de un área que no es suya.

## 3. Las ventanas van en milisegundos

Decisión con consecuencias, y es la que da criterio al juego.

```
Perfect   ±25 ms
Good      ±60 ms
Miss      más allá
```

**No en fracciones de beat.** Una ventana expresada como «un dieciseisavo de pulso» se encoge
al subir el tempo, y la precisión de una persona no escala con el BPM: se acierta a ±30 ms a 60
BPM y a ±30 ms a 160. Atar la ventana al tempo castigaría al jugador por una propiedad de la
pista y no por su ejecución.

**El ±25 no es arbitrario.** Es el mismo número del criterio Go/No-Go del acta, y la medición
del hito dio un percentil 90 de +4.07 ms. La ventana es por tanto **seis veces el error del
sistema**: lo que se mide es la precisión del jugador, no el jitter del motor. Esa relación es
la que hace defendible la cifra ante la docente.

## 4. La comparación se hace en tiempo

```csharp
double desfaseMs = (hit.ImpactDsp - reloj.DspDelBeat(nota.beat)) * 1000.0;
```

Ambos valores ya están expresados en el reloj DSP: `DrumHit.ImpactDsp` desde el capítulo 4, y
`MusicalClock.DspDelBeat` desde el reloj musical.

Consecuencia de diseño: **`HitJudge` no necesita saber el tempo**. Recibe un número en
milisegundos y devuelve un veredicto. Queda como función pura, probable sin Unity, sin audio y
sin reloj — y sigue valiendo si más adelante llega la rampa de tempo del iso-principio.

## 5. La anticipación va en segundos

Las notas aparecen **1.5 segundos antes** de su golpe, no «dos pulsos antes».

En beats, la velocidad visual cambiaría con el tempo y el jugador tendría que recalibrar el ojo
en cada pista. En segundos, una nota siempre tarda lo mismo en recorrer su camino, que es lo
que permite aprender a anticipar.

El reloj hace la conversión: `DspDelBeat(beat) - anticipacionSegundos`.

## 6. Emparejar golpe con nota

Un golpe en una pieza busca la nota **de esa misma pieza** más cercana en el tiempo que todavía
no se haya juzgado, dentro de la ventana de Miss.

| Caso | Comportamiento |
|---|---|
| Hay nota candidata | Se juzga y se marca como ya juzgada |
| No hay ninguna en ventana | El golpe se ignora, sin penalizar |
| Una nota pasa su ventana sin golpe | Se marca Miss sola |

**No se penalizan los golpes libres.** En un prototipo, castigar al jugador por tocar fuera del
patrón frustra sin enseñar nada, y la batería tiene que seguir siendo tocable.

## 7. Casos borde

| Caso | Comportamiento |
|---|---|
| Golpe antes de que arranque la canción | El reloj da beats negativos; no hay notas, se ignora |
| Dos notas de la misma pieza muy juntas | Se elige la más cercana no juzgada; la otra sigue disponible |
| Beatmap vacío | Arranca y no pasa nada. Se avisa una vez en consola |
| Beatmap con notas fuera de orden | Se ordena al cargar; el autor no tiene por qué cuidarlo |
| Umbrales cruzados en el inspector | Se corrigen al vuelo, como ya hace `HitIntensity` |

## 8. Pruebas

Sobre `HitJudge`, en EditMode sin audio ni escena:

1. 0 ms da Perfect.
2. 24 ms da Perfect; 26 ms da Good; 61 ms da Miss.
3. **Simetría**: −24 ms da Perfect igual que +24. Adelantarse y atrasarse valen lo mismo.
4. Las fronteras exactas —25.0 y 60.0— caen del lado generoso.
5. Umbrales cruzados por error no invierten la escala.

Sobre el emparejado, también puro:

6. Dada una lista de notas y un golpe, elige la de la pieza correcta y más cercana.
7. Una nota ya juzgada no se vuelve a elegir.
8. Sin candidata en ventana, devuelve «ninguna» en lugar de la más cercana de cualquier pieza.

## 9. Orden de construcción

Por valor demostrable, no por elegancia. Si la ventana se acorta, lo de abajo es lo que cae.

1. **`Beatmap` + `NoteSpawner`** — las notas aparecen y caen. Sin esto no hay demostración.
2. **`HitJudge`** — golpear a tiempo produce un veredicto. Es el corazón.
3. **`Scoreboard`** — aciertos y precisión en pantalla.
4. **Detección de Miss** — lo último.

Con los dos primeros ya hay algo que enseñar el miércoles.

## 10. Fuera de alcance

Niveles de dificultad, combo, pausa y reanudación, pantalla de resultados y modo libre: los
recortó la respuesta al riesgo R14 y no se reincorporan aquí.

La rampa de tempo del iso-principio tampoco: el reloj la admite por diseño, y no hace falta
para la demostración.
