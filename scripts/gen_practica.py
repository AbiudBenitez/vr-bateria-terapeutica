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
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITY = "/Users/abiudbenitez/Documents/code/Unity/BateriaVR"
KIT = os.path.join(UNITY, "Assets", "Audio", "Kit")
SALIDA = os.path.join(UNITY, "Assets", "Audio", "Practica")

# Una muestra fija por pieza, no sorteada: la pista debe sonar igual cada vez que se genere,
# para que una medición de hoy valga para el archivo de mañana.
MUESTRAS = {"HiHat": "Hat5-1.wav", "Bombo": "Kick8-1.wav", "Tarola": "Snare7-1.wav"}


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


def leer_muestra(pieza):
    ruta = os.path.join(KIT, pieza, MUESTRAS[pieza])
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
    return x / pico if pico else x


def sintetizar(patron):
    """Mezcla el acompañamiento sobre silencio y devuelve la señal."""
    dur = patrones.duracion_segundos(patron)
    spb = 60.0 / patron["bpm"]
    cola = 1.0                                   # margen para que el último golpe no se corte
    senal = np.zeros(int((dur + cola) * SR))

    muestras = {p: leer_muestra(p) for p in patron["acompanamiento"]}
    for beat, pieza in patrones.eventos(patron, "acompanamiento"):
        # Desde el beat, NO acumulando.
        i = int(round(beat * spb * SR))
        m = muestras[pieza]
        fin = min(i + len(m), len(senal))
        senal[i:fin] += m[:fin - i] * 0.7        # deja sitio a lo que toca el jugador
    return senal


def escribir_wav(ruta, senal):
    pico = np.max(np.abs(senal))
    datos = (np.clip(senal / pico * 0.9, -1, 1) * 32767).astype("<i2") if pico else \
            np.zeros(len(senal), dtype="<i2")
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
