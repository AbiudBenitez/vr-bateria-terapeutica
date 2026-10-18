# -*- coding: utf-8 -*-
"""
Mide el BPM real de una pista y, sobre todo, SI ES ESTABLE.

El BPM que declara el autor no basta. Una pista hecha con cuadrícula tiene tempo exacto; una
grabada en vivo flota, y un "92 BPM" que en realidad sea 91.7 desincroniza el beatmap a los
pocos compases — y el fallo parecería del reloj, que ya sabemos que no deriva.

Método: envolvente de energía -> flujo espectral -> autocorrelación sobre ventanas, para poder
comparar el tempo del principio con el del final. Solo numpy y la biblioteca estándar, como
latencia.py: scipy no carga en este macOS ARM.
"""
import sys
import wave

import numpy as np

SR_ANALISIS = 11025          # basta para el ritmo; acelera la autocorrelación
BPM_MIN, BPM_MAX = 50.0, 190.0
VENTANA_S = 20.0             # tramo sobre el que se mide un tempo local
PASO_S = 10.0


def leer(ruta):
    with wave.open(ruta, "rb") as w:
        sr, n, ancho, canales = (w.getframerate(), w.getnframes(),
                                 w.getsampwidth(), w.getnchannels())
        crudo = w.readframes(n)
    x = np.frombuffer(crudo, dtype={1: np.int8, 2: "<i2", 4: "<i4"}[ancho]).astype(np.float64)
    if canales > 1:
        x = x.reshape(-1, canales).mean(axis=1)
    pico = np.max(np.abs(x))
    return sr, (x / pico if pico else x)


def envolvente(x, sr, sr_env=200):
    """
    Flujo espectral: cuánta energía NUEVA aparece en cada instante.

    Se usa el flujo y no la amplitud porque un acorde sostenido tiene energía alta pero no
    marca pulso; lo que marca pulso es el ataque, o sea el incremento.
    """
    salto = max(1, sr // sr_env)
    ventana = salto * 4
    n = (len(x) - ventana) // salto
    if n < 4:
        return np.array([]), sr_env

    w = np.hanning(ventana)
    espec = np.abs(np.fft.rfft(
        np.lib.stride_tricks.sliding_window_view(x, ventana)[::salto][:n] * w, axis=1))

    flujo = np.diff(espec, axis=0, prepend=espec[:1])
    flujo = np.maximum(flujo, 0.0).sum(axis=1)      # solo los incrementos
    flujo -= flujo.mean()
    return flujo, sr / salto


def tempo_de(env, sr_env):
    """BPM por autocorrelación de la envolvente, con interpolación del pico."""
    if len(env) < sr_env * 4:
        return None, 0.0
    ac = np.correlate(env, env, mode="full")[len(env) - 1:]
    ac /= (ac[0] or 1.0)

    lag_min = int(sr_env * 60.0 / BPM_MAX)
    lag_max = min(int(sr_env * 60.0 / BPM_MIN), len(ac) - 2)
    if lag_max <= lag_min:
        return None, 0.0

    tramo = ac[lag_min:lag_max]
    i = int(np.argmax(tramo)) + lag_min

    # Interpolación parabólica: sin esto la resolución queda atada al paso de la envolvente,
    # que a 200 Hz da saltos de más de 1 BPM alrededor de 120.
    if 0 < i < len(ac) - 1:
        a, b, c = ac[i - 1], ac[i], ac[i + 1]
        denom = a - 2 * b + c
        if denom != 0:
            i = i + 0.5 * (a - c) / denom
    return 60.0 * sr_env / i, float(ac[int(round(i))])


def plegar(locales, referencia):
    """
    Lleva cada medida local a la misma octava que la referencia.

    La autocorrelación confunde el pulso con su mitad o su doble: en una pista de 80 BPM unas
    ventanas dan 80 y otras 160, según dónde caiga el acento. Contarlo como variación de tempo
    es un error de método — medí Maccary Bay como «flota 40 BPM» cuando lo que flotaba era mi
    elección de octava, no la pista.
    """
    if referencia is None or len(locales) == 0:
        return locales
    salida = []
    for b in locales:
        mejor, dist = b, abs(np.log2(b / referencia))
        for factor in (0.25, 0.5, 2.0, 4.0):
            cand = b * factor
            if not (BPM_MIN * 0.5 <= cand <= BPM_MAX * 2):
                continue
            d = abs(np.log2(cand / referencia))
            if d < dist:
                mejor, dist = cand, d
        salida.append(mejor)
    return np.array(salida)


def analizar(ruta):
    sr, x = leer(ruta)
    dur = len(x) / sr

    if sr > SR_ANALISIS:                      # diezmar: el ritmo no vive en los agudos
        paso = sr // SR_ANALISIS
        x = x[::paso]
        sr = sr // paso

    env, sr_env = envolvente(x, sr)
    bpm_global, fuerza = tempo_de(env, sr_env)

    # Tempo local, para ver si flota
    locales = []
    n_v = int(VENTANA_S * sr_env)
    n_p = int(PASO_S * sr_env)
    for ini in range(0, max(1, len(env) - n_v), n_p):
        b, f = tempo_de(env[ini:ini + n_v], sr_env)
        if b and f > 0.05:
            locales.append(b)

    loc = plegar(np.array(locales), bpm_global) if locales else np.array([])
    return dict(duracion=dur, bpm=bpm_global, fuerza=fuerza,
                locales=loc,
                mediana=float(np.median(loc)) if len(loc) else None,
                desv=float(np.std(loc)) if len(loc) else None,
                n_ventanas=len(loc))


if __name__ == "__main__":
    for ruta in sys.argv[1:]:
        r = analizar(ruta)
        nombre = ruta.split("/")[-1]
        print(f"\n=== {nombre} ===")
        print(f"  duración   {r['duracion']:.1f} s")
        if not r["bpm"]:
            print("  no pude medir el tempo")
            continue
        print(f"  BPM global {r['bpm']:.2f}   (fuerza del pulso {r['fuerza']:.2f})")
        if r["n_ventanas"] >= 2:
            print(f"  BPM local  mediana {r['mediana']:.2f} · desviación {r['desv']:.2f} "
                  f"sobre {r['n_ventanas']} ventanas de {VENTANA_S:.0f} s")
            est = r["desv"] < 1.0
            print(f"  tempo      {'ESTABLE' if est else 'FLOTA'}")
