# -*- coding: utf-8 -*-
"""
Sintetiza el acompañamiento de cada patrón y escribe su beatmap.

El audio se construye con las muestras del PROPIO kit, de modo que no entra ninguna licencia
nueva y el timbre del acompañamiento es el mismo que suena al golpear.

Cada golpe se coloca desde su número de beat y nunca sumando intervalos: acumular un intervalo
cuatrocientas veces introduce la deriva que esto viene a evitar, y es el mismo criterio con el
que se generó el metrónomo, que midió 499.999 ms de intervalo medio.
"""
import json
import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patrones

SR = 48000          # tasa nativa del visor, la misma del kit

# Nivel del acompañamiento. Es REFERENCIA, no protagonista: tiene que oírse sin tapar los
# golpes del jugador, que suenan a nivel completo.
NIVEL_FONDO = 0.35
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITY = "/Users/abiudbenitez/Documents/code/Unity/BateriaVR"
KIT = os.path.join(UNITY, "Assets", "Audio", "Kit")
SALIDA = os.path.join(UNITY, "Assets", "Audio", "Practica")

# Se rota entre varias muestras de cada pieza, con SEMILLA FIJA.
#
# Una sola muestra repetida 128 veces suena a máquina: el kit tiene veinte hi-hats y el motor
# ya hace round-robin al tocar, así que el acompañamiento sonaba más artificial que lo que el
# jugador golpea. Con semilla fija la pista sigue siendo idéntica cada vez que se genera, que
# es lo que permite que una medición de hoy valga para el archivo de mañana.
SEMILLA = 20261018
MUESTRAS = {"HiHat": "Hat5-", "Bombo": "Kick8-", "Tarola": "Snare7-"}
CUANTAS = 6          # de cada pieza; más variedad no se nota y alarga la carga


def decodificar(crudo, ancho):
    """
    Bytes de un WAV a muestras en coma flotante.

    Las muestras del kit son de 24 BITS —lo dice la atribución del pack— y numpy no tiene un
    tipo de tres bytes. Hay que reconstruirlas a mano: se toma cada terna, se coloca en los
    tres bytes altos de un entero de 32 bits, y se desplaza. El desplazamiento conserva el
    signo, que es justo lo que hace falta en audio con signo.
    """
    if ancho in (1, 2, 4):
        return np.frombuffer(crudo, dtype={1: np.int8, 2: "<i2", 4: "<i4"}[ancho]).astype(np.float64)
    if ancho == 3:
        b = np.frombuffer(crudo, dtype=np.uint8).reshape(-1, 3)
        v = (b[:, 0].astype(np.int32)
             | (b[:, 1].astype(np.int32) << 8)
             | (b[:, 2].astype(np.int32) << 16))
        v = np.where(v & 0x800000, v - 0x1000000, v)      # signo de 24 bits
        return v.astype(np.float64)
    raise SystemExit(f"ancho de muestra no soportado: {ancho} bytes")


def muestras_de(pieza):
    """Las primeras CUANTAS muestras de la pieza, ordenadas por nombre."""
    import glob as _glob
    rutas = sorted(_glob.glob(os.path.join(KIT, pieza, MUESTRAS[pieza] + "*.wav")))
    if not rutas:
        raise SystemExit(f"No encontré muestras de {pieza} en {KIT}")
    return [leer_muestra(r) for r in rutas[:CUANTAS]]


def leer_muestra(ruta):
    with wave.open(ruta, "rb") as w:
        sr, n, ancho, canales = (w.getframerate(), w.getnframes(),
                                 w.getsampwidth(), w.getnchannels())
        crudo = w.readframes(n)
    x = decodificar(crudo, ancho)
    if canales > 1:
        x = x.reshape(-1, canales).mean(axis=1)
    if sr != SR:
        raise SystemExit(f"{ruta} está a {sr} Hz y se esperaba {SR}")
    pico = np.max(np.abs(x))
    if pico:
        x = x / pico
    return recortar_al_ataque(x)


def recortar_al_ataque(x, umbral=0.2):
    """
    Quita el silencio que precede al ataque.

    Las muestras del pack empiezan con cantidades distintas de silencio: medido en los hi-hats,
    de 0.40 a 4.21 ms. Al rotar entre varias, ese silencio desigual hace que el pulso tiemble
    casi cuatro milisegundos, que es audible y además rompe la verificación de sincronía.

    Alinear por el ataque es lo que permite usar round-robin sin perder precisión: la versión
    de una sola muestra evitaba el problema por accidente, no por diseño.
    """
    if len(x) == 0:
        return x
    pico = np.max(np.abs(x))
    if pico <= 0:
        return x
    i = int(np.argmax(np.abs(x) > umbral * pico))
    return x[i:] if i > 0 else x


def acortar(m, spb):
    """
    Recorta la muestra a poco menos de un pulso, con un desvanecido corto.

    Las muestras del pack duran de 2 a 5 segundos. A 120 BPM eso son hasta diez hi-hats
    sonando a la vez, y el zumbido acumulado enmascara los ataques siguientes: en la
    verificación dos golpes de 128 quedaron sin detectar, y lo que el detector no oye el
    jugador tampoco.

    Un hi-hat cerrado real no suena cinco segundos. Acortarlo es corregir el sonido, no hacer
    que pase una prueba.
    """
    largo = int(spb * 0.9 * SR)
    if len(m) <= largo:
        return m
    cortada = m[:largo].copy()
    # Desvanecido en el último 25 %: cortar en seco produce un chasquido.
    n = max(1, int(largo * 0.25))
    cortada[-n:] *= np.linspace(1.0, 0.0, n)
    return cortada


def sintetizar(patron):
    """Mezcla el acompañamiento sobre silencio y devuelve la señal."""
    dur = patrones.duracion_segundos(patron)
    spb = 60.0 / patron["bpm"]
    cola = 1.0                                   # margen para que el último golpe no se corte
    senal = np.zeros(int((dur + cola) * SR))

    banco = {p: muestras_de(p) for p in patron["acompanamiento"]}
    rng = np.random.default_rng(SEMILLA)

    for beat, pieza in patrones.eventos(patron, "acompanamiento"):
        # Desde el beat, NO acumulando.
        i = int(round(beat * spb * SR))
        opciones = banco[pieza]
        m = acortar(opciones[rng.integers(0, len(opciones))], spb)
        fin = min(i + len(m), len(senal))
        senal[i:fin] += m[:fin - i] * NIVEL_FONDO
    return senal


def escribir_wav(ruta, senal):
    """
    Escribe el WAV SIN normalizar al pico.

    La primera versión normalizaba, y eso devolvía el acompañamiento a tope por mucho que se
    hubiera mezclado al 70 %: en el visor el hi-hat sonaba más fuerte que los golpes del
    jugador. El nivel debe venir ya decidido del archivo, no depender de que alguien baje un
    control en el inspector.
    """
    datos = (np.clip(senal, -1, 1) * 32767).astype("<i2")
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(datos.tobytes())


def beatmap_de(nombre, patron):
    return dict(
        nombre=nombre,
        titulo=patron["titulo"],
        bpm=patron["bpm"],
        pulsosPorCompas=patron["pulsos_por_compas"],
        pista=f"{nombre}.wav",
        notas=[dict(beat=b, pieza=p) for b, p in patrones.eventos(patron, "jugador")],
    )


def main():
    os.makedirs(SALIDA, exist_ok=True)
    indice = []
    for nombre, patron in patrones.PATRONES.items():
        senal = sintetizar(patron)
        escribir_wav(os.path.join(SALIDA, f"{nombre}.wav"), senal)

        bm = beatmap_de(nombre, patron)
        with open(os.path.join(SALIDA, f"{nombre}.json"), "w", encoding="utf-8") as fh:
            json.dump(bm, fh, indent=2, ensure_ascii=False)

        indice.append(nombre)
        print(f"  {nombre:14s} {patron['bpm']:5.1f} BPM · "
              f"{len(senal)/SR:5.1f} s · {len(bm['notas']):3d} notas")

    with open(os.path.join(SALIDA, "indice.json"), "w", encoding="utf-8") as fh:
        json.dump(indice, fh, indent=2)
    print(f"\n  -> {SALIDA}")


if __name__ == "__main__":
    main()
