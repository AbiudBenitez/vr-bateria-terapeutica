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


def test_el_total_del_alcance_no_depende_del_avance():
    """El defecto: total = hechas + sobreviven + nuevas.

    `hechas` se leia del cronograma de HOY, asi que cada actividad cerrada sumaba una al TOTAL
    del alcance. El 17-oct daba 155 y el 18-nov daba 197. El total sale del alcance: 257 menos
    las recortadas, mas las nuevas.
    """
    r = recorte.resumen()
    assert 257 - r["recortadas"] + r["nuevas"] == 155


def test_el_avance_del_dia_del_recorte_esta_declarado_y_no_se_recalcula():
    assert recorte.HECHAS_AL_RECORTE == 93
    assert "octubre" in recorte.FECHA_RECORTE


def test_todo_recorte_posterior_esta_declarado_con_su_razon():
    """Si el alcance cambia otra vez, va aqui: es lo que explica 155 contra las 158 de aquel dia."""
    declaradas = [k for _, claves, _ in recorte.RECORTES_POSTERIORES for k in claves]
    assert declaradas, "no hay recortes posteriores declarados"
    assert len(declaradas) == len(set(declaradas))
    for cuando, claves, razon in recorte.RECORTES_POSTERIORES:
        assert "2026" in cuando, cuando
        assert claves
        assert len(razon) > 30, "el recorte de %s no dice por que" % ", ".join(claves)
        for k in claves:
            assert k in recorte.RECORTADAS, \
                "%s se declara recortada despues y no esta en RECORTADAS" % k
    assert 158 - len(declaradas) == 257 - recorte.resumen()["recortadas"] + \
        recorte.resumen()["nuevas"], \
        "las 158 de aquel dia menos los recortes posteriores no dan el alcance vigente"
