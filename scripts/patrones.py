# -*- coding: utf-8 -*-
"""
Los patrones de práctica, como datos.

Cada patrón declara QUÉ pieza suena en QUÉ beat, y de aquí salen las dos cosas que tienen que
coincidir: el audio del acompañamiento y el beatmap de lo que el jugador toca.

Una sola fuente a propósito. El 18 de octubre el reloj corría a 80 BPM mientras el beatmap
declaraba 79.98, porque eran dos sitios donde escribir el mismo número; con una sola
definición esa clase de error deja de ser posible, no solo menos probable.

CONVENIO DE REPARTO
    acompanamiento  lo que SUENA en la pista: el hi-hat, que marca el pulso
    jugador         lo que el jugador debe GOLPEAR: bombo y caja

No se solapan. Si el acompañamiento tocara lo mismo que el jugador, este no distinguiría su
propio golpe del de la pista.
"""

# Posiciones dentro de un compás de 4/4, en beats desde su inicio.
CORCHEAS = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
PULSOS = [0.0, 1.0, 2.0, 3.0]

# El acompañamiento marca los PULSOS, no las corcheas.
#
# La partitura de referencia lleva hi-hat en corcheas, pero eso es lo que TOCA un baterista,
# no lo que necesita de referencia. Medido: en corcheas el fondo suena 2.67 veces por segundo
# contra 1.67 del jugador —1.6 golpes de fondo por cada uno propio—, y en lugar de guiar
# compite. En pulsos baja a 1.33/s y sigue marcando cada tiempo, que es lo que hace un
# metrónomo.

PATRONES = {
    "01_Pulso_80": dict(
        titulo="Pulso básico",
        bpm=80.0,
        pulsos_por_compas=4,
        compases=32,
        # Hi-hat solo en los pulsos: a 80 BPM son 1.33 golpes por segundo de referencia.
        acompanamiento={"HiHat": PULSOS},
        # Lo mínimo que se puede tocar: una pieza cada dos pulsos, alternando manos.
        jugador={"Bombo": [0.0], "Tarola": [2.0]},
    ),
    "02_Rock_80": dict(
        titulo="Rock básico, lento",
        bpm=80.0,
        pulsos_por_compas=4,
        compases=32,
        acompanamiento={"HiHat": PULSOS},
        jugador={"Bombo": [0.0, 2.0, 2.5], "Tarola": [1.0, 3.0]},
    ),
    "03_Rock_100": dict(
        titulo="Rock básico, medio",
        bpm=100.0,
        pulsos_por_compas=4,
        compases=32,
        acompanamiento={"HiHat": PULSOS},
        jugador={"Bombo": [0.0, 2.0, 2.5], "Tarola": [1.0, 3.0]},
    ),
    "04_Rock_120": dict(
        titulo="Rock básico",
        bpm=120.0,
        pulsos_por_compas=4,
        compases=32,
        acompanamiento={"HiHat": PULSOS},
        jugador={"Bombo": [0.0, 2.0, 2.5], "Tarola": [1.0, 3.0]},
    ),
}


def eventos(patron, cual):
    """
    Todos los golpes de `cual` ("acompanamiento" o "jugador"), como (beat, pieza).

    El beat se calcula desde el NÚMERO DE COMPÁS, nunca sumando intervalos: acumular un
    intervalo cien veces introduce la deriva que esto viene a evitar.
    """
    fuera = []
    ppc = patron["pulsos_por_compas"]
    for c in range(patron["compases"]):
        base = c * ppc
        for pieza, posiciones in patron[cual].items():
            for p in posiciones:
                fuera.append((base + p, pieza))
    fuera.sort(key=lambda e: (e[0], e[1]))
    return fuera


def duracion_segundos(patron):
    return patron["compases"] * patron["pulsos_por_compas"] * 60.0 / patron["bpm"]


if __name__ == "__main__":
    for nombre, p in PATRONES.items():
        acc = eventos(p, "acompanamiento")
        jug = eventos(p, "jugador")
        dur = duracion_segundos(p)
        print(f"  {nombre:14s} {p['bpm']:5.1f} BPM · {dur:5.1f} s · "
              f"{len(acc):3d} de acompañamiento · {len(jug):3d} del jugador "
              f"({len(jug)/dur:.2f}/s)")
