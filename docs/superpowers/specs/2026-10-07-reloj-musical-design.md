# Diseño — Reloj musical del juego de ritmo

**Fecha:** 7 de octubre de 2026 · **Estado:** aprobado, pendiente de plan
**Cubre:** `JT.1` reloj independiente de los FPS · `JT.2` cálculo de BPM y duración de beat ·
`JT.3` compases y subdivisiones

---

## 1. Por qué existe

El juego de ritmo necesita saber, en todo momento, en qué punto de la música está. Esa posición
no puede derivarse del tiempo de frame: el frame es irregular y acumula deriva, y a lo largo de
una canción de tres minutos la desincronización se vuelve audible.

Es el mismo problema que el capítulo 4 de la guía resolvió para el golpe, y se resuelve con la
misma herramienta: `AudioSettings.dspTime`, el reloj del hardware de audio.

### 1.1 Procedencia

`JT.1` y `JT.2` eran de Benjamín. Pasan a desarrollo VR por la respuesta al riesgo R14.

`JT.3` quedó fuera de aquel reparto por un error de conteo: las 38 actividades se repartieron
en 15 conservadas y 22 recortadas, y la suma da 37. Se incorpora aquí, que es su sitio natural:
los compases son la descomposición de un beat.

## 2. Arquitectura

Se sigue el patrón que el proyecto ya usa —`CrossSolver` es matemática pura y `StickTracker` el
MonoBehaviour que la consume—, porque permite probar la parte difícil sin visor y sin audio.

| Pieza | Responsabilidad | Probable sin hardware |
|---|---|---|
| `TempoMap` | Convierte segundos ↔ beats | Sí |
| `MusicalTime` | Descompone un beat en compás, pulso y subdivisión | Sí |
| `MusicalClock` | MonoBehaviour: arranca la canción y expone la posición | En play |

## 3. La puerta abierta al tempo variable

`TempoMap` expone exactamente dos operaciones:

```csharp
double SegundosABeats(double segundos);
double BeatsASegundos(double beats);
```

La implementación de hoy es de **tempo constante**. El acta describe el iso-principio —la sesión
mide el tempo espontáneo del usuario, arranca ahí y desciende hasta 60 BPM—, de modo que una
implementación en rampa llegará. Cuando llegue, nada de lo que consume el reloj cambia: ni el
beatmap, ni el marcador, ni las ventanas de precisión.

Esa es toda la puerta: dos métodos en lugar de multiplicar por `bpm / 60` repartido por el
código. No cuesta implementación extra ahora y evita reescribir después.

**Decisión explícita:** la primera implementación es de tempo constante. No se construye la
rampa hasta que haya un requisito concreto que la pida.

## 4. Arranque de la canción

El punto donde los juegos de ritmo se desincronizan.

```csharp
double inicio = AudioSettings.dspTime + MargenArranque;   // 0.1 s
musica.PlayScheduled(inicio);
reloj.Comenzar(inicio);
```

**Lo que NO se hace:** llamar a `Play()` y anotar `dspTime` a continuación. Entre ambas líneas
transcurre un tiempo desconocido que queda como desfase constante durante toda la pieza; no se
nota al principio y es evidente al minuto dos.

El margen de arranque cumple dos funciones: da al sistema de audio tiempo para preparar la
reproducción, y abre espacio para una cuenta regresiva. **Los beats negativos son válidos** y
significan «antes de que la canción empiece».

## 5. Integración con el golpe

```csharp
double beatDelGolpe = reloj.BeatEn(hit.ImpactDsp);
```

Sin compensaciones ni corrección de latencia. `DrumHit.ImpactDsp` ya está expresado en el reloj
DSP, que es el mismo que mide la canción.

Esto es lo que cobra el trabajo de latencia del hito Go/No-Go: medir +4.07 ms de percentil 90 no
sirvió solo para que el golpe se sintiera causal, sino para que esta integración sea una línea
en lugar de un sistema de calibración. La actividad `JY` del plan original —«crear sistema de
calibración de latencia entre golpe y música»— quedó sin objeto por esta razón.

## 6. Compases y subdivisiones

`MusicalTime` descompone una posición en beats:

```
beat 6.5 · compás de 4/4  →  compás 1, pulso 2, mitad del pulso
```

El compás se expresa como pulsos por compás (4 para 4/4, 3 para 3/4). La subdivisión es la
fracción del pulso, útil para colocar corcheas y semicorcheas en un beatmap.

## 7. Casos borde

| Caso | Comportamiento |
|---|---|
| Tiempo anterior al arranque | Beats negativos. No se recorta: es la cuenta regresiva |
| BPM cero o negativo | Se rechaza al construir el mapa, con mensaje explícito |
| Pulsos por compás menor que 1 | Se rechaza igual |
| Reloj consultado antes de arrancar | Devuelve posición cero y avisa una sola vez |

## 8. Pruebas

Sobre las dos clases puras, en EditMode, sin audio ni escena:

1. A 120 BPM un beat dura exactamente 0.5 s.
2. Ida y vuelta: `beats → segundos → beats` devuelve el valor original.
3. Beat 4.0 en compás de 4/4 es compás 1, pulso 0.
4. Beat 6.5 en 4/4 es compás 1, pulso 2, subdivisión 0.5.
5. Un tiempo negativo produce beats negativos sin excepción.
6. BPM inválido se rechaza al construir.
7. **La ida y vuelta se mantiene con un mapa de tempo simulado no constante.** Es la prueba
   que verifica que la abstracción de la sección 3 realmente aísla: si alguien implementa la
   conversión asumiendo tempo fijo, esta prueba falla.

## 9. Fuera de alcance

El beatmap y su formato (`JA.2`, `JA.3`, `JB.1` a `JB.3`), las notas visuales (`JN.1`, `JN.2`),
las ventanas de precisión (`JW.1`, `JW.2`, `JW.5`) y la puntuación (`JP.1`, `JP.3`). Todas
consumen este reloj y se construyen después.

No se implementa la rampa de tempo del iso-principio. La interfaz la admite; la implementación
espera a tener un requisito concreto.
