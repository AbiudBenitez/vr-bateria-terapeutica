# Diseño — Dinámica y variación del kit, etapa B

**Fecha:** 16 de septiembre de 2026 · **Estado:** aprobado, en implementación

---

## 1. El hallazgo que cambió el diseño

El plan original (capítulo 7 de la guía) suponía **3 capas de velocity × 2–3 round-robin** por
pieza. El pack de Dustyroom no tiene eso, y averiguarlo costó una conclusión equivocada por el
camino.

La primera revisión afirmó que `Tom2` eran "7 niveles de velocity × 2 round-robin", basándose en
una correlación de **0.97** entre índice y pico. Esa correlación es real, pero se midió sobre un
rango de **3.2 dB**. Unas capas de velocity abarcan 20–30 dB: una rampa perfecta de 3 dB no es
dinámica, es el orden en que el autor guardó tomas equivalentes.

Al medir el **brillo** —que es lo que de verdad distingue un golpe suave de uno fuerte, más que
el volumen— la hipótesis se cae:

| Pieza | corr. índice↔pico | corr. índice↔**brillo** | Rango de brillo |
|---|---|---|---|
| TomAlto | +0.97 | **−0.92** | 439 – 818 Hz |
| TomBajo | +0.71 | **−0.93** | 156 – 397 Hz |
| Tarola | +0.87 | −0.66 | 1745 – 3883 Hz |
| HiHat | +0.53 | **+0.86** | 4752 – 8674 Hz |
| Platillo | +0.61 | −0.26 | 11509 – 12080 Hz (**0.4 dB**) |
| Bombo | −0.52 | −0.05 | sin orden |

En un tambor real, pegar más fuerte da un sonido más alto **y** más brillante. En `TomAlto` sube
el pico y **baja** el brillo: es el patrón contrario. El índice del archivo no ordena por
dinámica.

**Pero el pack sí tiene un eje timbral aprovechable.** Factores de 2× en centroide son un rango
real. Solo hay que ordenarlo por medición en vez de por nombre.

## 2. Decisión

Se evaluaron tres caminos:

| | Camino | Veredicto |
|---|---|---|
| A | Round-robin y ganancia, nada más | Descartado: es el "mismo golpe más fuerte" que el diseño quería evitar |
| B | Ganancia más filtro paso-bajo que abre con la velocidad | Descartado: mete un componente más en el camino del audio |
| C | **Ordenar cada serie por brillo medido y mapear la velocidad a ese eje** | **Elegido** |

**Una sola lista ordenada resuelve las dos necesidades.** El índice da el timbre; una ventana de
±1 alrededor del índice da la variación. No hacen falta estructuras separadas de capas y
round-robin — que es justo lo que este pack no tiene.

## 3. El problema de nivel, y por qué la solución es un compromiso

Los picos **entre** piezas difieren 19 dB: Platillo 0.106 contra Bombo 0.939. Sin normalizar, el
platillo es inaudible al lado del bombo y la curva de velocidad no controla nada.

**`AudioSource.volume` está limitado a [0, 1]: no se puede amplificar.** Poner ganancia 8.9 al
platillo no funciona, Unity la recorta. Sin recurrir a un AudioMixer, la única normalización
posible es **atenuar hacia la pieza más floja**:

```
ganancia = min( rmsObjetivo / rms_muestra ,  0.98 / pico_muestra ,  1.0 )
```

con `rmsObjetivo` = el RMS más bajo del kit. Dos topes: el segundo evita recorte digital, el
tercero respeta el límite de Unity.

**Coste: unos 19 dB de headroom.** Todo el kit suena a un nivel bajo que se compensa con el
volumen del visor. Es un compromiso aceptado, no una elección libre. La alternativa —un
`AudioMixerGroup` por pieza con ganancia en dB— añade un nodo de mezcla al camino del audio, y
este proyecto lleva semanas acortando ese camino.

Se normaliza por **RMS y no por pico** porque el RMS se corresponde con la sonoridad percibida:
igualar picos deja una tarola, que tiene factor de cresta alto, sonando más floja que un bombo.

## 4. Componentes

```
Assets/Audio/Kit/<Pieza>/*.wav
          │
          │  Batería → Analizar kit   (editor, una vez)
          ▼
   DrumKitPiece  (ScriptableObject, uno por pieza)
     ├── muestras[] ORDENADAS POR BRILLO ascendente
     │     ├── clip
     │     ├── centroideHz
     │     └── ganancia          normalización horneada
     └── rangoDeBrillo           max/min; < 1.3 ⇒ sin eje timbral
          │
          ▼
   DrumVoice  ──usa──>  SampleSelector  (estático, sin MonoBehaviour, probable sin visor)
```

### `SampleSelector`

Función pura. Recibe cuántas muestras hay, la posición en el eje `t ∈ [0,1]`, cuál se reprodujo
la última vez, el ancho de ventana, si la pieza tiene eje timbral, y un número aleatorio en
`[0,1)`. Devuelve el índice.

Recibe el aleatorio como **parámetro** en lugar de llamar a `Random` por dentro: así la función
es determinista y las pruebas no dependen de una semilla global.

- Con eje timbral: centro = `round(t × (n−1))`, ventana `[centro−v, centro+v]` acotada, se
  excluye la última reproducida y se elige entre las restantes.
- Sin eje timbral: se elige entre todas menos la última.
- Si excluir la última deja el conjunto vacío —solo puede pasar con `n = 1`— se devuelve la
  única que hay.

### `DrumVoice` v2

Dos curvas editables en el inspector, no constantes en código:

- **velocidad → posición** en el eje de brillo
- **velocidad → ganancia**

El `clip` suelto **se conserva como respaldo** cuando `pieza` está vacío. La escena `Cap04_Pad`
sigue funcionando igual, y con ella la configuración exacta con la que se midió el hito
Go/No-Go. Un resultado que costó tres corridas no se invalida por comodidad.

## 5. Pruebas

Sobre `SampleSelector`, en EditMode, sin audio ni visor:

1. Con una sola muestra siempre devuelve 0.
2. `t = 0` cae dentro de la ventana de la muestra más opaca; `t = 1`, de la más brillante.
3. El índice nunca se sale de `[0, n−1]`, con 1 muestra y con 20.
4. **Nunca repite la anterior** cuando hay más de una disponible.
5. Una pieza sin eje timbral puede devolver cualquier índice, no solo los cercanos a `t`.

## 6. Fuera de alcance

Hi-hat abierto y cerrado con pedal, filtro paso-bajo por voz, audio espacializado, mezclador,
y el filtro de proximidad por collider para las seis piezas — ése va después, cuando haya seis
pads en la escena.
