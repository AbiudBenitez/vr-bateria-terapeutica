# Revisión de los dos packs de samples para la etapa B

**Fecha:** 16 de septiembre de 2026
**Pregunta:** ¿cuál de los dos sirve como base del kit de 6 piezas?

**Respuesta corta: Dustyroom.** Clark Audio no tiene la forma que hace falta, aunque los
sonidos sean buenos.

---

## 1. Qué necesita la etapa B

Del capítulo 7 de la guía: 6 piezas × 3 capas de velocity × 2–3 variantes de round-robin, o sea
**36 a 54 samples**. A 48 kHz, la tasa nativa del Quest, para no remuestrear en tiempo real.

Y el bombo tiene un requisito extra que salió del capítulo 5: debe conservar energía **entre 80
y 200 Hz**. Por debajo de 80 Hz las bocinas del visor no reproducen y el micrófono de un celular
no capta, de modo que un bombo muy profundo desaparece de la grabación y la medición de latencia
deja de ser posible.

## 2. Comparativa

| | Dustyroom — Fake Acoustic Drum Kit | Clark Audio — Boom Bap Drum Kit |
|---|---|---|
| Archivos de audio | 573 | 125 |
| Sample rate | **48 kHz** (399 de 400 comprobados) | **44.1 kHz** (116 de 125) |
| Profundidad | 24 bits | 24 bits |
| Estructura | **Series indexadas**: `Kick3-1`, `Kick3-2`… | One-shots con nombre propio |
| Capas de velocity | **Sí** | No |
| Round-robin | **Sí** | No |
| Crash | **No tiene** | 2 |
| Licencia | `LICENSE.pdf` incluido | **Ninguna** |

### Por qué Clark Audio no sirve como base

Tiene 42 bombos, pero son **42 bombos distintos**, no 42 capas del mismo bombo. Los nombres lo
dicen: "Dusty Foley", "Heartbeater", "Sum Diff". Es un pack para hacer beats, donde eliges *un*
sonido por pista. Lo que la etapa B necesita es lo contrario: **el mismo tambor grabado a
distintas fuerzas**, para que golpear suave y golpear fuerte den sonidos genuinamente distintos
y no el mismo sonido a distinto volumen.

Súmale 44.1 kHz —remuestreo en tiempo real, que el capítulo 6 pide evitar— y la ausencia total
de archivo de licencia, que para un entregable académico es un problema por sí solo.

### Por qué Dustyroom sí

La estructura `Instrumento{kit}-{índice}` son series de capas. Verificado midiendo el pico de
cada archivo contra su índice:

`Tom2` tiene 14 archivos cuyos picos suben en **parejas**: (0.247, 0.247), (0.275, 0.279),
(0.299, 0.302) … (0.359, 0.358). Son **7 niveles de velocity × 2 round-robin**. Y las duraciones
alternan corto/largo dentro de cada pareja, así que son tomas distintas y no copias.

Eso supera lo que pedía el diseño.

## 3. Mejor kit por instrumento

Ordenados por correlación entre índice y pico: 1.00 sería una rampa de velocity perfecta.

| Instrumento | Kit | Muestras | Fuerza de rampa |
|---|---|---|---|
| Tom | **Tom2** | 14 | **0.97** |
| Tarola | **Snare7** | 14 | **0.87** |
| Tom (segundo) | **Tom4** | 15 | 0.71 |
| Bombo | Kick1 | 16 | 0.63 |
| Ride | **Ride2** | 12 | 0.61 |
| Hi-hat | **Hat5** | 20 | 0.53 |

## 4. La trampa del bombo

Energía por banda en los primeros 40 ms, muestra central de cada kit:

| Kit | <80 Hz | **80–200 Hz** | 200–500 | >500 | |
|---|---|---|---|---|---|
| Kick1 | 82% | **15%** | 2% | 1% | ramp mejor, **inaudible en el visor** |
| Kick3 | 90% | **10%** | 1% | 0% | el peor para este hardware |
| **Kick8** | 23% | **51%** | 10% | 16% | **el bueno** |
| Kick7 | 62% | **32%** | 5% | 2% | aceptable |
| Kick2 | 65% | **30%** | 4% | 1% | aceptable |

**El bombo con la mejor rampa de velocity, `Kick1`, es el peor para este proyecto.** El 82% de su
energía está por debajo de 80 Hz: es exactamente la trampa que ya costó una corrida de medición
inválida con `bass drum.wav`. Suena magnífico por audífonos y desaparece por las bocinas del
visor.

**Usar `Kick8`**, que concentra el 51% en la banda que el hardware sí reproduce. Tiene 7 muestras
en lugar de 16, que siguen siendo más de las 3 capas × 2 variantes que pide el diseño.

## 5. El hueco: no hay crash

Dustyroom tiene Hat y Ride, pero **ningún crash, china ni splash**. Dos salidas:

| Opción | A favor | En contra |
|---|---|---|
| **Sustituir el crash por `Ride2`** | 12 muestras, rampa 0.61, mismo pack, mismo carácter sonoro, 48 kHz | No es un crash; el acento fuerte suena distinto |
| Tomar los 2 crashes de Clark Audio | Es un crash de verdad | 44.1 kHz (remuestreo), sin capas ni round-robin, y **sin licencia** |

**Recomendado: `Ride2`.** Mezclar packs trae dos tasas de muestreo, dos caracteres de grabación y
dos situaciones de licencia al mismo proyecto, a cambio de un platillo. El valor terapéutico del
proyecto es motriz —coordinación y precisión rítmica— y no depende de que el sexto elemento sea
crash y no ride.

## 6. Kit propuesto

| Pieza | Fuente | Muestras |
|---|---|---|
| Bombo | `Kick8-*` | 7 |
| Tarola | `Snare7-*` | 14 |
| Hi-hat | `Hat5-*` | 20 |
| Tom alto | `Tom2-*` | 14 |
| Tom bajo | `Tom4-*` | 15 |
| Platillo | `Ride2-*` | 12 |
| **Total** | | **82** |

Ochenta y dos contra las 36–54 previstas. Sobran, y sobrar está bien: permite elegir las mejores
de cada serie en vez de conformarse.

## 7. Ajustes de importación en Unity

Los archivos son estéreo de 24 bits. `DrumVoice` usa `spatialBlend = 0`, así que el canal
derecho no aporta nada y duplica la memoria.

| Ajuste | Valor | Por qué |
|---|---|---|
| Force To Mono | **Sí** | Mitad de memoria, cero pérdida: el audio no está espacializado |
| Load Type | **Decompress On Load** | Son golpes cortos; descomprimir al vuelo mete latencia |
| Compression Format | **PCM** o ADPCM | PCM no tiene coste de decodificación |
| Preload Audio Data | **Sí** | Evita el tirón del primer golpe de cada pieza |
| Sample Rate Setting | **Preserve Sample Rate** | Ya están a 48 kHz; cualquier conversión sobra |

## 8. Pendiente antes de usarlos

**Leer `LICENSE.pdf` de Dustyroom.** No se pudo extraer su texto —usa fuentes con subconjunto— y
**no se ha verificado qué permite**. Es requisito del entregable, no un trámite: hay que saber si
exige atribución y si permite uso en un trabajo académico publicado.

Clark Audio **no trae ningún archivo de licencia**, lo que es razón suficiente para no
construir sobre él aunque los sonidos gusten.
