# -*- coding: utf-8 -*-
"""Pruebas de los patrones de práctica."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patrones


def test_el_acompanamiento_y_el_jugador_no_se_solapan():
    """
    Si la pista tocara lo mismo que el jugador, este no distinguiría su golpe del de la pista
    y el juego dejaría de enseñar nada.
    """
    for nombre, p in patrones.PATRONES.items():
        piezas_acc = set(p["acompanamiento"])
        piezas_jug = set(p["jugador"])
        assert not (piezas_acc & piezas_jug), \
            f"{nombre}: la pieza {piezas_acc & piezas_jug} suena y se toca a la vez"


def test_los_beats_se_calculan_desde_el_compas():
    """
    A 120 BPM el compás 10 empieza exactamente en el beat 40. Si se acumulara el intervalo,
    el error se arrastraría.
    """
    p = patrones.PATRONES["04_Rock_120"]
    ev = patrones.eventos(p, "jugador")
    beats = sorted({b for b, _ in ev})
    assert 40.0 in beats, "el compás 10 no empieza en el beat 40"
    assert 124.0 in beats, "el compás 31 no empieza en el beat 124"


def test_el_rock_basico_tiene_la_forma_de_la_partitura():
    """Bombo en 1, caja en 2, bombo en 3 y su corchea, caja en 4."""
    p = patrones.PATRONES["04_Rock_120"]
    primer_compas = sorted((b, n) for b, n in patrones.eventos(p, "jugador") if b < 4.0)
    assert primer_compas == [
        (0.0, "Bombo"), (1.0, "Tarola"), (2.0, "Bombo"), (2.5, "Bombo"), (3.0, "Tarola")
    ], f"el patrón no coincide con la partitura: {primer_compas}"


def test_el_hihat_va_en_corcheas_en_los_patrones_de_rock():
    for nombre in ("02_Rock_80", "03_Rock_100", "04_Rock_120"):
        p = patrones.PATRONES[nombre]
        assert p["acompanamiento"]["HiHat"] == patrones.CORCHEAS, \
            f"{nombre}: el hi-hat no marca las ocho corcheas"


def test_la_progresion_sube_de_densidad():
    """Cada pista debe pedir más golpes por segundo que la anterior."""
    orden = ["01_Pulso_80", "02_Rock_80", "03_Rock_100", "04_Rock_120"]
    densidades = []
    for n in orden:
        p = patrones.PATRONES[n]
        densidades.append(len(patrones.eventos(p, "jugador")) / patrones.duracion_segundos(p))
    assert densidades == sorted(densidades), \
        f"la progresión no es creciente: {[f'{d:.2f}' for d in densidades]}"


def test_la_primera_pista_es_de_verdad_facil():
    """Menos de un golpe por segundo: es la que existe para poder empezar."""
    p = patrones.PATRONES["01_Pulso_80"]
    d = len(patrones.eventos(p, "jugador")) / patrones.duracion_segundos(p)
    assert d < 1.0, f"la pista de entrada pide {d:.2f} golpes por segundo"
