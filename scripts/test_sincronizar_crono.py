# -*- coding: utf-8 -*-
"""
Los dos cronogramas pueden diferir en ALCANCE y no en AVANCE.

El de ProjectLibre lleva las 257 actividades de la lista original con las 100 recortadas
marcadas; el operativo lleva las 158 que sobrevivieron. Eso es deliberado. Lo que no puede
pasar es que una actividad este hecha en uno y no en el otro: es la misma actividad, y un
documento que dice 59 % mientras el otro dice 83 % deja a quien lo lea sin saber cual creer.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sincronizar_crono as sinc

# DM.1 la creo el recorte, asi que NO pertenece al cronograma anterior al recorte. Es la
# unica ausencia legitima; cualquier otra es un defecto.
AUSENCIAS_ESPERADAS = {"DM.1"}


def cargar():
    op = sinc.tareas(open(sinc.OPERATIVO, encoding="utf-8").read())
    pl = sinc.tareas(open(sinc.PROJECTLIBRE, encoding="utf-8").read())
    return op, pl


def test_ninguna_actividad_esta_hecha_en_uno_y_no_en_el_otro():
    op, pl = cargar()
    discrepan = sorted(k for k in set(op) & set(pl)
                       if sinc.hecha(op[k]) != sinc.hecha(pl[k]))
    assert not discrepan, (
        "estas difieren de avance entre los dos cronogramas: %s. "
        "Pasa scripts/sincronizar_crono.py" % ", ".join(discrepan))


def test_la_unica_ausencia_es_la_que_el_recorte_anadio():
    op, pl = cargar()
    ausentes = {k for k in op if k not in pl}
    assert ausentes == AUSENCIAS_ESPERADAS, (
        "ausencias del cronograma de ProjectLibre: %s, se esperaba %s"
        % (sorted(ausentes), sorted(AUSENCIAS_ESPERADAS)))


def test_el_alcance_de_cada_uno_es_el_que_le_toca():
    """Si estos numeros cambian, alguien movio el alcance y no solo el avance."""
    op, pl = cargar()
    assert len(op) == 158, "el operativo tiene %d actividades, se esperaban 158" % len(op)
    assert len(pl) == 257, "el de ProjectLibre tiene %d, se esperaban 257" % len(pl)


def test_el_porcentaje_vigente_coincide_en_los_dos():
    """Las recortadas salen del denominador del de ProjectLibre: medir contra trabajo
    cancelado da un porcentaje que no significa nada."""
    import recorte
    op, pl = cargar()
    fuera = set(recorte.RECORTADAS)

    h_op = sum(1 for b in op.values() if sinc.hecha(b))
    vig_pl = {k: b for k, b in pl.items() if k not in fuera}
    h_pl = sum(1 for b in vig_pl.values() if sinc.hecha(b))

    pct_op = 100.0 * h_op / len(op)
    pct_pl = 100.0 * h_pl / len(vig_pl)
    assert abs(pct_op - pct_pl) < 1.0, (
        "el operativo va al %.1f %% (%d de %d) y el de ProjectLibre al %.1f %% (%d de %d)"
        % (pct_op, h_op, len(op), pct_pl, h_pl, len(vig_pl)))


def test_sincronizar_es_idempotente():
    """Correrlo dos veces no debe tocar nada la segunda. Si tocara, estaria reescribiendo
    el archivo en cada pasada y el diff de git dejaria de significar algo."""
    sincronizadas, _, _ = sinc.main(escribir=False)
    assert not sincronizadas, (
        "quedan %d actividades por sincronizar: %s"
        % (len(sincronizadas), ", ".join(sincronizadas)))


def test_el_avance_no_va_al_reves():
    """Hecha solo en el de ProjectLibre significa que alguien marco en el archivo de la
    lista original en vez de en el que se trabaja."""
    _, _, al_reves = sinc.main(escribir=False)
    assert not al_reves, (
        "marcadas solo en el de ProjectLibre: %s. El operativo manda." % ", ".join(al_reves))
