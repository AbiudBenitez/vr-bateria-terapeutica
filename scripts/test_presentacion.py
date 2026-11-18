# -*- coding: utf-8 -*-
"""Pruebas del documento 17, el guion de la presentacion final.

QX es la ultima actividad del proyecto y su documento es el que alguien lee con prisa el dia
antes. Lo que estas pruebas impiden: que el guion prometa una cifra que ya cambio, que pierda
los bloques que la materia evalua, y que un paso de la demo no diga que puede salir mal.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import costos
import estado
import gen_presentacion as G
import manual_datos
import presentacion as P
import replan as RP
import sesiones as S

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
R = S.resumen()


# ------------------------------------------------------------------ el arco

def test_los_bloques_estan_numerados_sin_huecos():
    nums = [b[0] for b in P.BLOQUES]
    assert nums == list(range(1, len(P.BLOQUES) + 1)), nums


def test_cada_bloque_dice_que_se_dice_que_se_muestra_y_cuanto_dura():
    for n, titulo, puntos, muestra, minutos in P.BLOQUES:
        assert len(titulo) > 3, n
        assert puntos and all(len(p) > 30 for p in puntos), \
            "el bloque %d tiene puntos demasiado vagos para guiar a nadie" % n
        assert len(muestra) > 10, "el bloque %d no dice qué se muestra" % n
        assert minutos > 0, "el bloque %d no tiene tiempo asignado" % n


def test_el_total_de_minutos_no_se_escribe_a_mano():
    assert G.MINUTOS == sum(b[4] for b in P.BLOQUES)
    assert str(G.MINUTOS) in TXT, "el documento no dice los %d minutos que suman" % G.MINUTOS


def test_el_orden_de_recorte_apunta_a_bloques_que_existen():
    nums = {b[0] for b in P.BLOQUES}
    for n in P.RECORTE_SI_FALTA_TIEMPO:
        assert n in nums, "se manda recortar el bloque %d y no existe" % n
    assert len(set(P.RECORTE_SI_FALTA_TIEMPO)) == len(P.RECORTE_SI_FALTA_TIEMPO)


def test_no_se_recortan_las_decisiones_ni_lo_que_no_salio():
    """Son los dos bloques que la materia evalua. Sin ellos es una presentacion de producto."""
    assert 3 not in P.RECORTE_SI_FALTA_TIEMPO, \
        "el bloque 3 son las tres decisiones que reorientaron el proyecto"
    assert 8 not in P.RECORTE_SI_FALTA_TIEMPO, \
        "el bloque 8 es lo que no salió y qué se hizo con eso"


def test_las_decisiones_van_antes_de_los_resultados():
    bloques = {b[0]: b[1] for b in P.BLOQUES}
    assert "decisiones" in bloques[3].lower()
    assert 3 < 6, "el bloque de decisiones tiene que ir antes del de resultados"


# ------------------------------------------------------------------ las cifras

def test_las_diez_medidas_salen_con_su_estado():
    for num, titulo, est, _ in estado.MEDIDAS:
        assert titulo in TXT, "la medida %d no aparece" % num
        assert est in TXT, "el estado %r no aparece en el documento" % est


def test_las_tres_decisiones_salen_con_su_documento():
    for x in estado.DECISIONES:
        assert x["titulo"] in TXT
        assert x["doc"] in TXT, "la decisión %r aparece sin su documento" % x["titulo"]


def test_todos_los_hitos_salen():
    for h in estado.HITOS:
        assert h[1] in TXT, "el hito %r no aparece" % h[1]


def test_el_presupuesto_es_el_vigente():
    assert format(round(costos.PRESUPUESTO), ",") in TXT, \
        "el guion no lleva el presupuesto vigente de %s" % costos.PRESUPUESTO


def test_las_cifras_del_prototipo_salen_de_sus_fuentes():
    assert str(manual_datos.DATOS["pruebas"]) in TXT
    assert str(R["sesiones"]) in TXT
    assert str(R["notas"]) in TXT


def test_el_guion_declara_el_desborde_del_plan():
    """Si el plan no cabe, la presentacion lo dice. Es el bloque 8."""
    if RP.DESBORDA:
        assert str(RP.DIAS_DE_DESBORDE) in TXT
        assert str(RP.CIERRE) in TXT, "el guion no dice la fecha de cierre calculada"


def test_el_guion_no_presenta_las_sesiones_como_de_los_catorce():
    assert "no son" in TXT.lower() and "participantes" in TXT.lower()
    prohibidas = [r"14 participantes (?:tocaron|obtuvieron|promediaron|reportaron)",
                  r"los 14 (?:lograron|alcanzaron)"]
    for pat in prohibidas:
        m = re.search(pat, TXT, re.I)
        assert m is None, "el guion atribuye resultados a los 14: %r" % m.group(0)


# ------------------------------------------------------------------ la demo

def test_la_demo_esta_numerada_sin_huecos():
    nums = [x[0] for x in P.DEMO]
    assert nums == list(range(1, len(P.DEMO) + 1)), nums


def test_cada_paso_de_la_demo_dice_que_puede_salir_mal():
    for n, hace, ver, cuanto, riesgo in P.DEMO:
        assert len(hace) > 15, "paso %d" % n
        assert len(ver) > 25, "el paso %d no dice qué hay que ver" % n
        assert re.fullmatch(r"\d+ s", cuanto), "paso %d: tiempo %r" % (n, cuanto)
        assert len(riesgo) > 15, "el paso %d no declara qué puede salir mal" % n


def test_la_demo_llega_hasta_salir():
    """El recorrido completo incluye salir. CU-14 existe porque ese defecto ya ocurrio."""
    assert "salir" in P.DEMO[-1][1].lower(), "la demo no termina saliendo de la aplicación"


def test_la_demo_cabe_en_tres_minutos():
    total = sum(int(x[3].split()[0]) for x in P.DEMO)
    assert total <= 210, "la demo suma %d segundos y se anuncian tres minutos" % total


def test_todo_paso_de_la_demo_sale_en_el_documento():
    for n, hace, _, _, _ in P.DEMO:
        assert hace[:40] in TXT, "el paso %d de la demo no aparece" % n


# ------------------------------------------------------------------ antes de presentar

def test_cada_comprobacion_previa_dice_por_que_esta():
    for q, por in P.ANTES:
        assert len(q) > 20, q
        assert len(por) > 30, "la comprobación %r no dice por qué está en la lista" % q
        assert q[:35] in TXT


def test_se_comprueba_la_build_y_la_marca_de_tutorial():
    junto = " ".join(q for q, _ in P.ANTES).lower()
    assert "build" in junto
    assert "tutorial" in junto, \
        "sin borrar la marca de tutorial visto, el paso 1 de la demo no se puede enseñar"


def test_el_documento_declara_lo_que_le_falta():
    for t, _ in P.PENDIENTE_DE_DATO:
        assert t in TXT, "el documento no declara que falta: %s" % t
