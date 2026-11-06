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
CONTRATIEMPOS = [0.5, 1.5, 2.5, 3.5]

# El acompañamiento marca los PULSOS, no las corcheas.
#
# La partitura de referencia lleva hi-hat en corcheas, pero eso es lo que TOCA un baterista,
# no lo que necesita de referencia. Medido: en corcheas el fondo suena 2.67 veces por segundo
# contra 1.67 del jugador —1.6 golpes de fondo por cada uno propio—, y en lugar de guiar
# compite. En pulsos baja a 1.33/s y sigue marcando cada tiempo, que es lo que hace un
# metrónomo.

# ---------------------------------------------------------------------------- LOS CUATRO RITMOS
#
# EL CUERPO DE CADA RITMO SE ESCRIBE UNA VEZ y se toca a tres tempos. Antes había tres entradas
# de rock con el mismo patrón copiado, y el resultado se reportó así: «en la de rock donde solo
# varía el tempo son lo mismo, no varía nada». Eran tres pistas distintas en el disco y la misma
# en el visor; ahora el selector las ofrece como LENTO, MEDIO y RÁPIDO de un solo ritmo, que es
# lo que de verdad son.
#
# DE DÓNDE SALEN LOS DOS NUEVOS. De cinco videos de práctica de batería que el equipo reunió y
# pasó por un notebook. De los cinco ejercicios, estos dos son los que encajan con el reparto de
# aquí -hi-hat de referencia, bombo y tarola para el jugador- sin pedirle al jugador que toque el
# hi-hat, que es la pieza que marca el pulso.
#
# El de semicorcheas quedó fuera con un dato de este mismo archivo: a 2.67 golpes por segundo el
# acompañamiento deja de guiar y compite. Los de ride y crash, fuera porque esas piezas están en
# el kit pero ninguna pista las usa todavía.

PULSO = dict(
    # Hi-hat solo en los pulsos: a 80 BPM son 1.33 golpes por segundo de referencia.
    acompanamiento={"HiHat": PULSOS},
    # Lo mínimo que se puede tocar: una pieza cada dos pulsos, alternando manos.
    jugador={"Bombo": [0.0], "Tarola": [2.0]},
)

ROCK = dict(
    acompanamiento={"HiHat": PULSOS},
    jugador={"Bombo": [0.0, 2.0, 2.5], "Tarola": [1.0, 3.0]},
)

# EL ACOMPAÑAMIENTO SE VA AL CONTRATIEMPO, y eso es todo el ejercicio.
#
# Del tutorial de ska: la secuencia es bombo, hi-hat, tarola, hi-hat en bucle. Aquí el hi-hat lo
# pone la pista, así que lo que el jugador toca son los pulsos y lo que oye cae ENTRE ellos.
#
# Es el salto de dificultad que faltaba y no cuesta una nota más: con la referencia en el pulso,
# golpear a tiempo es imitar lo que se oye; con la referencia a contratiempo hay que sostener el
# pulso propio mientras suena algo que no coincide con él. Misma densidad, otra tarea.
CONTRA = dict(
    acompanamiento={"HiHat": CONTRATIEMPOS},
    jugador={"Bombo": [0.0, 2.0], "Tarola": [1.0, 3.0]},
)

# EL ACENTO SE DESPLAZA POR EL COMPÁS.
#
# Del ejercicio de desplazamiento del acento: cuatro golpes de hi-hat continuos y el bombo
# acentuando el primero, luego el segundo, luego el tercero, luego el cuarto. El hi-hat continuo
# ya lo pone la pista en los cuatro pulsos, así que el ejercicio queda exacto: lo único que
# cambia es DÓNDE cae el golpe del jugador.
#
# LA TAROLA ES UNA ADAPTACIÓN NUESTRA, no está así en el video. Allí se añade en la primera mitad
# del compás; aquí va siempre dos pulsos después del bombo, de modo que acompaña el
# desplazamiento sin chocar nunca con él. Sin ella el ejercicio son 32 notas en 96 segundos y se
# siente vacío; con ella queda a la misma densidad que el pulso básico.
#
# OCHO COMPASES POR POSICIÓN. Cuatro no dan tiempo a automatizar antes de que cambie, y
# dieciséis dejan la segunda mitad de cada tramo sin nada que aprender.
ACENTOS = dict(
    acompanamiento={"HiHat": PULSOS},
    compases_por_paso=8,
    jugador_ciclo=[
        {"Bombo": [0.0], "Tarola": [2.0]},
        {"Bombo": [1.0], "Tarola": [3.0]},
        {"Bombo": [2.0], "Tarola": [0.0]},
        {"Bombo": [3.0], "Tarola": [1.0]},
    ],
)


# LOS NOMBRES NO SE TOCAN.
#
# 02_Rock_80, 03_Rock_100 y 04_Rock_120 conservan el prefijo que ya tenían aunque sean el mismo
# ritmo. Renombrarlos a 02_Rock_* habría quedado más limpio y habría dejado los tres archivos
# viejos en la carpeta, que el importador recogeria como pistas duplicadas: el selector enseñaría
# ROCK con seis velocidades, dos de cada. El prefijo solo ordena la carpeta; lo que agrupa es el
# trozo de en medio del nombre, y eso ya funciona.

def _ritmo(titulo, bpm, cuerpo, compases=32):
    return dict(titulo=titulo, bpm=bpm, pulsos_por_compas=4, compases=compases, **cuerpo)


PATRONES = {
    "01_Pulso_80":    _ritmo("Pulso básico, lento", 80.0, PULSO),
    "01_Pulso_100":   _ritmo("Pulso básico, medio", 100.0, PULSO),
    "01_Pulso_120":   _ritmo("Pulso básico, rápido", 120.0, PULSO),

    "02_Rock_80":     _ritmo("Rock básico, lento", 80.0, ROCK),
    "03_Rock_100":    _ritmo("Rock básico, medio", 100.0, ROCK),
    "04_Rock_120":    _ritmo("Rock básico, rápido", 120.0, ROCK),

    "05_Contra_80":   _ritmo("Contratiempo, lento", 80.0, CONTRA),
    "05_Contra_100":  _ritmo("Contratiempo, medio", 100.0, CONTRA),
    "05_Contra_120":  _ritmo("Contratiempo, rápido", 120.0, CONTRA),

    "06_Acentos_80":  _ritmo("Acentos, lento", 80.0, ACENTOS),
    "06_Acentos_100": _ritmo("Acentos, medio", 100.0, ACENTOS),
    "06_Acentos_120": _ritmo("Acentos, rápido", 120.0, ACENTOS),
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
        for pieza, posiciones in reparto(patron, cual, c).items():
            for p in posiciones:
                fuera.append((base + p, pieza))
    fuera.sort(key=lambda e: (e[0], e[1]))
    return fuera


def reparto(patron, cual, compas):
    """
    Lo que toca `cual` en ese compás.

    CASI TODOS LOS PATRONES REPITEN EL MISMO COMPÁS 32 VECES, y para esos esto devuelve siempre
    lo mismo. La excepción es el de acentos, donde el golpe del jugador se desplaza: ahí el
    patrón declara un CICLO de compases y cuántos compases dura cada paso.

    Un ciclo no es lo mismo que escribir 32 compases a mano: el ciclo dice la regla -cuatro
    posiciones, ocho compases cada una- y de la regla se ve si está completa. Treinta y dos
    entradas copiadas esconden un dedazo en la número 19.
    """
    ciclo = patron.get(cual + "_ciclo")
    if not ciclo:
        return patron[cual]

    por_paso = patron.get("compases_por_paso", 1)
    return ciclo[(compas // por_paso) % len(ciclo)]


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
