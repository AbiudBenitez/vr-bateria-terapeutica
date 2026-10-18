# Diseño — Pistas de práctica y anillos de aproximación

**Fecha:** 18 de octubre de 2026 · **Estado:** aprobado, pendiente de plan

---

## 1. Qué se resuelve

Dos problemas que aparecieron al probar el juego con música real.

**No hay pulso audible.** La pista elegida, *Maccary Bay*, tiene 1.33 pulsos por segundo y
**9.39 ataques audibles por segundo**: siete eventos sonoros por cada pulso. El tempo existe
—medido a 79.98 BPM con fase estable a lo largo de 180 segundos— pero no destaca entre todo lo
demás que suena. El jugador no tiene contra qué sincronizarse, y falla casi todo.

**La guía visual no basta para acertar.** Una esfera que cae hacia un plano exige juzgar
distancia, que en realidad virtual es justo lo peor calibrado de la percepción.

## 2. El acompañamiento es percusión, no música

El pulso lo marca la propia batería: **hi-hat en corcheas, ocho por compás.** Es como se
practica de verdad, y resuelve tres cosas a la vez.

| Problema | Cómo se resuelve |
|---|---|
| No hay pulso audible | El hi-hat marca cada corchea |
| El acompañamiento compite con lo que se toca | Toca solo lo que el jugador NO toca |
| No hay material de práctica | El patrón es el contenido |

El acompañamiento se sintetiza **con las muestras del propio kit** —las mismas `Hat5-*` que
suenan al golpear—, de modo que no entra ninguna licencia nueva y el timbre es el mismo.

*Maccary Bay* no se descarta: queda como la pista medida y documentada que cierra `MP.1` a
`MP.3`, y sirve para modo libre o fondo. Pero para el juego de ritmo, un patrón de práctica es
mejor contenido.

## 3. Audio y beatmap salen del mismo dato

Un solo archivo de definición genera **las dos cosas**: el WAV del acompañamiento y el
`Beatmap` de lo que hay que tocar.

Es la decisión que más cambia el resultado. Hoy mismo el reloj corría a 80 BPM mientras el
beatmap declaraba 79.98, porque eran dos sitios donde escribir el mismo número. Con una sola
fuente esa clase de error **deja de ser posible**, no solo menos probable.

## 4. Cuatro pistas, en progresión

| # | Patrón | BPM | Notas/s del jugador |
|---|---|---|---|
| 1 | Bombo en 1, caja en 3 | 80 | 0.7 |
| 2 | Rock básico | 80 | 1.3 |
| 3 | Rock básico | 100 | 1.7 |
| 4 | Rock básico | 120 | 2.0 |

**Rock básico:** bombo en el pulso 1, caja en el 2, bombo en el 3 y en su corchea, caja en el
4. Hi-hat en las ocho corcheas.

La primera existe porque empezar por el patrón completo a 120 es exactamente lo que falló.

**No son niveles de dificultad** —esos se recortaron en la respuesta al riesgo R14— sino pistas
distintas, que es como el beatmap las entiende.

## 5. Los anillos de aproximación

Sobre cada pad, un anillo que empieza al **triple del radio** y se cierra hasta el radio exacto
en el instante de la nota.

```
t = nota − 1.5 s     ○     anillo grande
t = nota − 0.5 s     ◎
t = nota             ◉     los bordes coinciden: golpear AQUÍ
```

**El radio es lineal en el tiempo**, como en osu!. El ojo lee la velocidad de cierre mucho
mejor que la posición, y la coincidencia de dos bordes es un instante inequívoco; no una
estimación de profundidad.

En realidad virtual la diferencia pesa más que en pantalla: el anillo vive **sobre el pad**,
que es donde el jugador ya está mirando, y es información bidimensional sobre una superficie.

Color por pieza. Todo el conjunto se reserva en `Awake`, como el resto de lo que toca el camino
del golpe.

## 6. Las notas que caen pasan a secundarias

El anillo aparece 1.5 segundos antes y ya dice de qué pieza se trata, de modo que la esfera
cayendo añade ruido visual sin añadir información.

**Quedan apagadas por defecto**, con casilla para encenderlas. Si en el visor resultan útiles
para anticipar desde lejos, se encienden; la decisión se toma mirando, no antes.

## 7. Casos borde

| Caso | Comportamiento |
|---|---|
| La nota ya pasó | El anillo no baja del radio del pad; se apaga tras un margen |
| Dos notas seguidas en la misma pieza | Dos anillos concéntricos, cada uno con su tiempo |
| Se agota el conjunto reservado | Se deja de dibujar antes que realocar en el camino del golpe |
| Pieza sin pad en la escena | Se avisa una vez y esa nota no dibuja anillo |

## 8. Pruebas

Sobre el generador, en Python:

1. Cada golpe se coloca desde su número de beat, **no sumando intervalos**: acumular 0.5 s
   cuatrocientas veces introduce la deriva que esto viene a evitar.
2. Verificación con `latencia.py`: los ataques del WAV caen donde el beatmap dice, con la
   misma tolerancia con que se verificó el metrónomo.
3. El beatmap y el audio declaran el mismo BPM, por construcción.

Sobre `ApproachRing`, en EditMode sin escena:

4. A mitad de camino el radio está a mitad entre el inicial y el del pad.
5. En el instante de la nota el radio es exactamente el del pad.
6. Pasado ese instante el radio no sigue bajando.

## 9. Fuera de alcance

El modo libre y la selección de pista desde un menú: la interfaz se recortó al flujo mínimo.

Los patrones con platillos, toms o redobles. Cuatro pistas con bombo, caja y hi-hat bastan para
demostrar el mecanismo y son lo que el patrón de referencia pide.
