# -*- coding: utf-8 -*-
"""Pruebas del documento 16.

LA PRUEBA QUE IMPORTA es la ultima: que el documento no presente las 39 sesiones registradas
como si fueran las de los 14 participantes. Es la unica forma de que el hueco siga visible
cuando alguien regenere esto dentro de una semana y ya no recuerde cual era el hueco.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gen_pruebas_usuario as G
import pruebas_usuario as PU
import sesiones as S

from docx import Document

DOC = G.DOC
R = S.resumen()


def texto():
    d = Document(DOC)
    trozos = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                trozos.append(c.text)
    return "\n".join(trozos)


TXT = texto()


# ------------------------------------------------------------------ los casos de uso

def test_cada_caso_esta_completo():
    for cid, titulo, pre, pasos, esperado, criterio, medida in PU.CASOS:
        assert re.fullmatch(r"CU-\d\d", cid), cid
        assert len(titulo) > 10, cid
        assert len(pre) > 15, "%s no declara precondición" % cid
        assert pasos and all(len(p) > 10 for p in pasos), "%s no tiene pasos útiles" % cid
        assert len(esperado) > 25, "%s no dice qué se espera" % cid
        assert len(criterio) > 25, "%s no tiene criterio de aceptación" % cid
        assert medida in G.MEDIDAS, "%s cobra una medida que no existe: %r" % (cid, medida)


def test_no_hay_casos_repetidos():
    ids = [c[0] for c in PU.CASOS]
    assert len(ids) == len(set(ids))


def test_todo_caso_sale_en_el_documento_con_su_criterio():
    for cid, _, _, _, _, criterio, _ in PU.CASOS:
        assert cid in TXT, "%s no aparece en el documento" % cid
        assert criterio[:40] in TXT, "%s aparece sin su criterio de aceptación" % cid


def test_cada_medida_de_exito_tiene_al_menos_un_caso():
    cubiertas = {c[6] for c in PU.CASOS}
    assert cubiertas == set(G.MEDIDAS), \
        "hay medidas declaradas sin caso, o casos que cobran una medida sin nombre: %s" \
        % (cubiertas ^ set(G.MEDIDAS))


def test_el_caso_del_pad_de_salir_existe():
    """CU-14 existe porque ese defecto ya ocurrio. Si alguien lo borra, vuelve a poder pasar."""
    cu14 = next((c for c in PU.CASOS if c[0] == "CU-14"), None)
    assert cu14 is not None
    assert "OBS-01" in cu14[5], "CU-14 no remite a la observación que lo motivó"


# ------------------------------------------------------------------ las observaciones

def test_cada_observacion_esta_completa():
    for o in PU.OBSERVACIONES:
        oid, fecha, que, causa, grav, area, estado, ev = o
        assert re.fullmatch(r"OBS-\d\d", oid), oid
        assert re.fullmatch(r"2026-\d\d-\d\d", fecha), "%s: fecha %r" % (oid, fecha)
        assert len(que) > 40, "%s no describe qué se observó" % oid
        assert len(causa) > 25, "%s no declara la causa" % oid
        assert grav in PU.GRAVEDADES, "%s: gravedad %r" % (oid, grav)
        assert len(area) > 5, oid
        assert estado in ("Corregida", "Abierta", "En curso"), "%s: estado %r" % (oid, estado)
        assert len(ev) > 30, "%s no lleva evidencia verificable" % oid


def test_no_hay_observaciones_repetidas():
    ids = [o[0] for o in PU.OBSERVACIONES]
    assert len(ids) == len(set(ids))


def test_las_fechas_de_las_observaciones_caen_en_el_desarrollo():
    for o in PU.OBSERVACIONES:
        assert "2026-10-17" <= o[1] <= "2026-11-18", \
            "%s está fechada el %s, fuera del periodo de desarrollo" % (o[0], o[1])


def test_toda_observacion_sale_en_el_documento_con_su_causa():
    for o in PU.OBSERVACIONES:
        assert o[0] in TXT, "%s no aparece en el documento" % o[0]
        assert o[3][:40] in TXT, "%s aparece sin su causa" % o[0]
        assert o[7][:40] in TXT, "%s aparece sin su evidencia" % o[0]


def test_las_clasificaciones_suman_el_total():
    assert sum(len(v) for v in PU.por_gravedad().values()) == len(PU.OBSERVACIONES)
    assert sum(len(v) for v in PU.por_area().values()) == len(PU.OBSERVACIONES)


def test_los_reportes_literales_van_entre_comillas():
    """Distinguir lo que alguien dijo de lo que nosotros interpretamos."""
    literales = [o for o in PU.OBSERVACIONES if "Reporte literal" in o[2]]
    assert len(literales) >= 4, \
        "solo %d observaciones llevan el reporte literal; hay varias más con cita textual" \
        % len(literales)
    for o in literales:
        assert "«" in o[2] and "»" in o[2], "%s dice llevar reporte literal y no lo acota" % o[0]


# ------------------------------------------------------------------ las cifras

def test_las_cifras_del_documento_salen_de_los_volcados():
    assert R is not None, "no hay volcados de sesión: corre quest.sh pull"
    assert str(R["sesiones"]) in TXT
    assert str(R["notas"]) in TXT
    assert str(R["aciertos"]) in TXT
    assert "%.1f" % R["precision_global"] in TXT
    assert "%.1f" % R["rejilla_mediana"] in TXT
    assert "%.1f" % R["pulso_mediana"] in TXT


def test_solo_se_cuentan_pistas_completas():
    for s in S.SESIONES:
        assert s["notas"]["total"] >= S.MINIMO_NOTAS


def test_las_dos_constancias_no_se_confunden():
    assert R["rejilla_mediana"] != R["pulso_mediana"], \
        "las dos constancias dan el mismo número: o es casualidad o están implementadas igual"
    assert "constancia contra la rejilla" in TXT.lower()
    assert "pulso propio" in TXT.lower()


# ------------------------------------------------------------------ el hueco sigue visible

def test_el_documento_declara_lo_que_falta():
    for titulo, _, actividad in PU.PENDIENTE:
        assert titulo in TXT, "el documento no declara que falta: %s" % titulo
    assert "PENDIENTE" in TXT


def test_el_documento_no_atribuye_las_sesiones_a_los_catorce():
    """La prueba que impide que esto se convierta en un registro fabricado.

    Si alguien regenera el documento dentro de una semana y rellena los huecos con numeros
    inventados, esta prueba no lo detecta -no puede-. Lo que si garantiza es que el aviso de
    que las sesiones NO son de los 14 sigue en el documento, y que el documento no afirma lo
    contrario en ningun sitio.
    """
    assert "no miden a 14 participantes" in TXT.lower() or \
           "no son una curva de aprendizaje" in TXT.lower(), \
        "el documento perdió el aviso de que las sesiones registradas no son de los 14"
    assert "no lleva identificador de participante" in TXT.lower()
    prohibidas = [
        r"14 participantes (?:tocaron|completaron|reportaron|obtuvieron)",
        r"los 14 participantes (?:lograron|alcanzaron|promediaron)",
        r"cada (?:uno de los )?14",
    ]
    for pat in prohibidas:
        m = re.search(pat, TXT, re.I)
        assert m is None, \
            "el documento atribuye resultados a los 14 participantes sin el dato: %r" \
            % m.group(0)


def test_las_observaciones_se_declaran_del_desarrollo_y_no_de_las_sesiones():
    assert "no son hallazgos de las sesiones" in TXT.lower(), \
        "el documento no distingue las observaciones del desarrollo de las de los participantes"
