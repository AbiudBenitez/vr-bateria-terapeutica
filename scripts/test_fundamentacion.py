# -*- coding: utf-8 -*-
"""Pruebas de la revision de la fundamentacion, documento 18.

LO QUE IMPIDEN: que una afirmacion quede sin veredicto, que un veredicto quede sin con que
comprobarlo, y que la revision contradiga lo que el resto del proyecto ya declaro.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fundamentacion as F
import gen_fundamentacion as G

from docx import Document


def texto():
    d = Document(G.DOC)
    trozos = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                trozos.append(c.text)
    return "\n".join(trozos)


TXT = texto()


def test_cada_afirmacion_esta_completa():
    for aid, afirmacion, fuente, veredicto, hace, comprueba in F.AFIRMACIONES:
        assert re.fullmatch(r"F-\d\d", aid), aid
        assert len(afirmacion) > 40, "%s: la afirmación es demasiado corta" % aid
        assert len(fuente) > 10, "%s no dice de dónde sale" % aid
        assert veredicto in F.VEREDICTOS, "%s: veredicto %r" % (aid, veredicto)
        assert len(hace) > 80, "%s no explica qué hace el prototipo" % aid
        assert len(comprueba) > 40, "%s no dice con qué se comprueba" % aid


def test_no_hay_afirmaciones_repetidas():
    ids = [a[0] for a in F.AFIRMACIONES]
    assert len(ids) == len(set(ids))


def test_los_veredictos_suman_el_total():
    pv = F.por_veredicto()
    assert sum(len(v) for v in pv.values()) == len(F.AFIRMACIONES)


def test_hay_de_los_tres_veredictos():
    """Si salieran las ocho sostenidas, la revision no reviso nada."""
    pv = F.por_veredicto()
    for v in F.VEREDICTOS:
        assert pv[v], "ninguna afirmación quedó %r: eso no es una revisión" % v


def test_toda_afirmacion_sale_en_el_documento_con_su_veredicto():
    for aid, _, _, veredicto, hace, comprueba in F.AFIRMACIONES:
        assert aid in TXT, "%s no aparece" % aid
        assert "%s — %s" % (aid, veredicto.upper()) in TXT, \
            "%s aparece sin su veredicto" % aid
        assert hace[:50] in TXT
        assert comprueba[:40] in TXT


def test_las_cuatro_siglas_de_nmt_estan_revisadas():
    """La fundamentacion se anclaba en cuatro marcos. Los cuatro llevan veredicto."""
    junto = " ".join(a[1] for a in F.AFIRMACIONES)
    for sigla in ("RAS", "TIMP", "PSE", "Iso-principio"):
        assert sigla in junto, "el marco %s quedó sin revisar" % sigla


def test_el_iso_principio_esta_retirado_y_dice_que_falta():
    iso = next(a for a in F.AFIRMACIONES if "Iso-principio" in a[1])
    assert iso[3] == "retirada"
    assert "ITempoMap" in iso[5], \
        "se retira el iso-principio sin decir que la arquitectura lo deja abierto"


def test_pse_esta_sostenida():
    """Es la unica que el prototipo hace entera, y el parrafo final del documento se apoya en ella."""
    pse = next(a for a in F.AFIRMACIONES if a[1].startswith("PSE"))
    assert pse[3] == "sostenida"
    assert "Patterned Sensory Enhancement" in TXT


def test_las_consecuencias_estan_razonadas():
    assert len(F.CONSECUENCIAS) >= 3
    for titulo, detalle in F.CONSECUENCIAS:
        assert len(titulo) > 20, titulo
        assert len(detalle) > 120, "la consecuencia %r no está razonada" % titulo
        assert titulo in TXT


def test_el_documento_remite_a_la_fuente_original_y_no_la_reescribe():
    assert F.FUENTE in TXT, "el documento no dice dónde está la fundamentación original"
    assert "no se edita" in TXT.lower()
    original = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", F.FUENTE)
    assert os.path.isfile(original), "la fundamentación original ya no está donde se dice"


def test_el_parrafo_reescrito_no_promete_lo_retirado():
    """El parrafo final es lo que la fundamentacion puede sostener hoy.

    SE LEEN SOLO LOS PARRAFOS, en orden de documento. `texto()` pega todas las celdas de tabla
    AL FINAL, asi que cortar por la posicion en esa cadena arrastraba las tablas de secciones
    anteriores -incluida la de F-02, que cita «rango articular» justamente para retirarlo- y la
    prueba fallaba con el documento correcto.
    """
    parrafos = [p.text for p in Document(G.DOC).paragraphs]
    corte = next((i for i, t in enumerate(parrafos)
                  if "La fundamentación reescrita" in t), None)
    assert corte is not None, "no encuentro la sección del párrafo reescrito"
    parrafo = "\n".join(parrafos[corte:])
    for prohibida in ("rango articular", "rehabilitación motriz", "tempo espontáneo",
                      "amplitud de movimiento"):
        assert prohibida not in parrafo, \
            "el párrafo reescrito sigue prometiendo %r" % prohibida


def test_las_dos_metricas_que_no_existen_estan_nombradas():
    f06 = next(a for a in F.AFIRMACIONES if a[0] == "F-06")
    assert f06[3] == "acotada"
    assert "simetria" in f06[4].lower() or "simetría" in f06[4].lower()
    assert "adherencia" in f06[4].lower()
