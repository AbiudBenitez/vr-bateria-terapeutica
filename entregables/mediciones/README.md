# Evidencia: métricas de sesión y recuperación de la predicción

Cuatro sesiones del 17-oct-2026 sobre el beatmap de demostración: 64 notas, 120 BPM.
Las tres primeras corrieron con dos defectos; la última, ya corregidos.

| Hora | Aciertos | Desfase medio | Desviación | Constancia | |
|---|---|---|---|---|---|
| 22:41:15 | 56/64 | -12.3 ms | 20.3 ms | **259.8 ms** | con los defectos |
| 22:43:23 | 57/64 | -17.9 ms | 23.4 ms | **225.8 ms** | con los defectos |
| 22:51:13 | 52/64 | -16.7 ms | 29.2 ms | **347.3 ms** | con los defectos |
| 23:01:03 | 63/64 | +1.0 ms | 29.8 ms | **24.2 ms** | corregido |

## Los dos defectos

### 1. La predicción estaba apagada

`armDistance = 0` en los seis pads, heredado de la plantilla que usa `ConstruirKit`. Sin
distancia de armado, el instante de impacto se calcula cuando ya pasó y el audio nunca se
agenda.

| | Antes | Después |
|---|---|---|
| Agendas tardías | **419 de 419 — 100 %** | **0 de 67 — 0 %** |
| Lead mediano | −6.9 ms | **+27.0 ms** |

El −6.9 ms es medio frame a 72 Hz, y no dependía de la velocidad: correlación de +0.08 con la
inversa de la velocidad cuando el modelo predice +1.00. Firma de cuantización de frame, no de
predicción.

### 2. La constancia del pulso medía los fallos

De **278 ms de media a 24.2 ms**, 11 veces menor.

Se medía el intervalo contra el golpe anterior a secas. Al fallar una nota, el intervalo
siguiente valía 1000 ms en vez de 500 y la métrica lo leía como pulso irregular. Con 8 fallos
de 64 notas, los huecos aportaban unos 165 ms por sí solos.

Ahora cada intervalo se compara con el que pedía la partitura.

## Una observación que queda abierta

El desfase medio pasó de −16 ms a **+1.0 ms**. Hay una explicación plausible —con
`armDistance = 0` se registraba el cruce del plano de golpe en vez del impacto predicho— pero
**es una sola sesión y además se tocó mejor** (63 aciertos contra 52–57).

No se afirma que la asincronía negativa anterior fuera artefacto. Hacen falta dos o tres
corridas más para separarlo de la ejecución del jugador.

## Cómo se detectaron

Ninguno de los dos se vio jugando: el sistema sonaba bien y los números eran plausibles. Los
dos aparecieron **revisando los archivos exportados**, que es justamente para lo que la medida
9 pedía exportarlos.

Ambos tienen ahora una prueba que los vigila:
`KitLayoutTests.NingunPadTieneLaPrediccionApagada` y
`SessionStatsTests.UnaNotaFALLADANoCuentaComoIrregularidad`.
