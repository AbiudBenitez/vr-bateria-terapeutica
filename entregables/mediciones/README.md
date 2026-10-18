# Evidencia: la predicción estaba apagada

Seis volcados del `LatencyProbe` bajados del visor el 17-oct-2026, con el kit de seis
piezas y `armDistance = 0` en los seis pads.

| Volcado | Golpes | Tardías | % | Lead mediano | Vel. mediana | Vel. p90 |
|---|---|---|---|---|---|---|
| `261017_182528` | 59 | 59 | 100 % | -7.7 ms | 2.67 m/s | 3.03 m/s |
| `261017_182612` | 62 | 62 | 100 % | -6.9 ms | 3.21 m/s | 3.65 m/s |
| `261017_183846` | 80 | 80 | 100 % | -6.6 ms | 1.31 m/s | 2.73 m/s |
| `261017_184744` | 81 | 81 | 100 % | -4.5 ms | 2.75 m/s | 4.56 m/s |
| `261017_224115` | 69 | 69 | 100 % | -5.7 ms | 2.76 m/s | 4.19 m/s |
| `261017_224323` | 68 | 68 | 100 % | -7.0 ms | 2.46 m/s | 3.93 m/s |

**419 de 419 golpes (100 %) salieron por el camino de respaldo.**

## Por qué es concluyente

El lead mediano de −6.7 ms es **medio frame a 72 Hz** (6.94 ms). Y la correlación entre el
lead y la inversa de la velocidad es **+0.08**, cuando el modelo `lead = armDistance ÷
velocidad` predice +1.00.

Un lead constante que no depende de la velocidad no viene de la predicción: viene de la
cuantización de frame. Es la misma firma que en septiembre separó las dos corridas del hito
Go/No-Go, donde la corrida con predicción daba 0 % de agendas tardías y +52 ms de lead.

## Consecuencia

El hito se midió con la predicción encendida, de modo que su p90 de +4.07 ms describe un
sistema distinto del que corrió estas semanas. **Hay que volver a medir con `armDistance`
corregido, o declarar la diferencia en el informe.**

## Causa

`ConstruirKit` toma un pad existente como plantilla; el original tenía `armDistance = 0` y los
seis lo heredaron. El sistema seguía sonando, así que no se notó: solo cambiaba *cuándo*.

Lo vigila ahora `KitLayoutTests.NingunPadTieneLaPrediccionApagada`.
