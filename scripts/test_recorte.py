# -*- coding: utf-8 -*-
"""
Consistencia de las listas del recorte.

Un error aquí no se ve leyendo: una clave en dos listas a la vez, o una que no existe en el
cronograma, produce un documento que afirma algo falso con toda seriedad.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recorte
import validacion


def test_ninguna_clave_en_dos_listas():
    ya = set(recorte.YA_HECHAS)
    sob = set(recorte.SOBREVIVEN)
    rec = set(recorte.RECORTADAS)
    nue = set(recorte.NUEVAS)

    assert not (ya & sob), f"en YA_HECHAS y SOBREVIVEN: {ya & sob}"
    assert not (ya & rec), f"en YA_HECHAS y RECORTADAS: {ya & rec}"
    assert not (sob & rec), f"en SOBREVIVEN y RECORTADAS: {sob & rec}"
    assert not (nue & (ya | sob | rec)), f"NUEVAS choca: {nue & (ya | sob | rec)}"


def test_las_listas_cubren_todo_lo_pendiente():
    """Cada actividad pendiente del cronograma tiene que estar en exactamente una lista."""
    f = validacion.fusion()
    pendientes = {k for k, t in f.items() if not t["hecha"]}
    clasificadas = set(recorte.YA_HECHAS) | set(recorte.SOBREVIVEN) | set(recorte.RECORTADAS)

    sin_clasificar = pendientes - clasificadas
    assert not sin_clasificar, \
        f"{len(sin_clasificar)} pendientes sin clasificar: {sorted(sin_clasificar)}"


def test_no_se_clasifica_algo_que_no_existe():
    """Una clave inventada produciría un documento que habla de trabajo imaginario."""
    f = validacion.fusion()
    clasificadas = set(recorte.YA_HECHAS) | set(recorte.SOBREVIVEN) | set(recorte.RECORTADAS)

    inexistentes = clasificadas - set(f)
    assert not inexistentes, f"claves que no están en el cronograma: {sorted(inexistentes)}"


def test_no_se_clasifica_algo_ya_terminado():
    """Recortar una actividad terminada sería borrar trabajo hecho."""
    f = validacion.fusion()
    hechas = {k for k, t in f.items() if t["hecha"]}

    choque = hechas & set(recorte.RECORTADAS)
    assert not choque, f"actividades terminadas marcadas como recortadas: {sorted(choque)}"


def test_cada_recortada_tiene_razon():
    vacias = [k for k, v in recorte.RECORTADAS.items() if not v or len(v.strip()) < 10]
    assert not vacias, f"recortadas sin razón escrita: {vacias}"


def test_cada_superviviente_tiene_justificacion():
    malas = [k for k, (m, j) in recorte.SOBREVIVEN.items() if not j or len(j.strip()) < 10]
    assert not malas, f"supervivientes sin justificación: {malas}"


def test_las_medidas_citadas_existen():
    citadas = {m for m, _ in recorte.SOBREVIVEN.values() if m is not None}
    citadas |= {m for m, _ in recorte.NUEVAS.values() if m is not None}
    assert citadas <= set(recorte.MEDIDAS), \
        f"medidas citadas que no existen: {citadas - set(recorte.MEDIDAS)}"


def test_la_medida_retirada_no_la_sirve_nadie():
    """Si una actividad sirviera a la medida 8, retirarla sería incoherente."""
    sirven = [k for k, (m, _) in recorte.SOBREVIVEN.items() if m == recorte.MEDIDA_RETIRADA]
    assert not sirven, \
        f"estas sobreviven sirviendo a la medida retirada: {sirven}"
