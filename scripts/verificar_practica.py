# -*- coding: utf-8 -*-
"""
Comprueba que los ataques del WAV caen donde el beatmap dice.

El generador y el beatmap salen de la misma definición, así que en teoría no pueden
discrepar. Esto lo comprueba sobre el ARCHIVO, que es lo que de verdad va al visor: un error
de redondeo al escribir las muestras, o una muestra que empiece con silencio, aparecerían
aquí y no en las pruebas del generador.
"""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import latencia
import patrones

UNITY = "/Users/abiudbenitez/Documents/code/Unity/BateriaVR"
SALIDA = os.path.join(UNITY, "Assets", "Audio", "Practica")
TOLERANCIA_MS = 5.0


def verificar(nombre):
    with open(os.path.join(SALIDA, f"{nombre}.json"), encoding="utf-8") as fh:
        bm = json.load(fh)
    sr, x = latencia.load_wav(os.path.join(SALIDA, f"{nombre}.wav"))
    detectados = latencia.onset_times(x, sr)

    patron = patrones.PATRONES[nombre]
    spb = 60.0 / bm["bpm"]
    esperados = np.array([b * spb for b, _ in patrones.eventos(patron, "acompanamiento")])
    esperados = np.unique(np.round(esperados, 6))

    errores = []
    for e in esperados:
        if len(detectados) == 0:
            break
        errores.append((detectados[np.argmin(np.abs(detectados - e))] - e) * 1000.0)
    errores = np.array(errores)

    return dict(
        nombre=nombre,
        esperados=len(esperados),
        detectados=len(detectados),
        error_max=float(np.max(np.abs(errores))) if len(errores) else float("inf"),
        error_medio=float(np.mean(np.abs(errores))) if len(errores) else float("inf"),
    )


def main():
    nombres = sorted(os.path.basename(p)[:-5]
                     for p in glob.glob(os.path.join(SALIDA, "*.json"))
                     if not p.endswith("indice.json"))
    if not nombres:
        raise SystemExit("No hay pistas generadas. Corre antes gen_practica.py")

    print(f"  {'pista':16s}{'esperados':>11s}{'detectados':>12s}"
          f"{'error medio':>13s}{'error máx':>11s}")
    fallos = 0
    for n in nombres:
        r = verificar(n)
        ok = r["error_max"] <= TOLERANCIA_MS
        fallos += 0 if ok else 1
        print(f"  {n:16s}{r['esperados']:>11d}{r['detectados']:>12d}"
              f"{r['error_medio']:>12.2f} ms{r['error_max']:>9.2f} ms"
              f"  {'OK' if ok else 'FALLA'}")

    if fallos:
        raise SystemExit(f"\n  {fallos} pistas fuera de la tolerancia de {TOLERANCIA_MS} ms")
    print(f"\n  Las {len(nombres)} pistas dentro de {TOLERANCIA_MS} ms")


if __name__ == "__main__":
    main()
