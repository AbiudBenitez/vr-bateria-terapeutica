# -*- coding: utf-8 -*-
"""Comprobaciones del documento de estado. Que las cifras cuadren con las fuentes."""
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estado
import recorte

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NS = {"m": "http://schemas.microsoft.com/project"}


def cronograma():
    r = ET.parse(os.path.join(RAIZ, "entregables", "Cronograma_Operativo.xml")).getroot()
    hechas = total = 0
    for x in r.findall(".//m:Task", NS):
        if x.findtext("m:Summary", default="0", namespaces=NS) == "1":
            continue
        if not (x.findtext("m:Name", default="", namespaces=NS) or ""):
            continue
        total += 1
        if x.findtext("m:PercentComplete", default="0", namespaces=NS) == "100":
            hechas += 1
    return hechas, total


def test_el_avance_por_area_suma_el_del_cronograma():
    """Si alguien actualiza una cifra y no la otra, el documento miente sin que se note."""
    hechas = sum(h for _, h, _ in estado.AVANCE)
    total = sum(h + p for _, h, p in estado.AVANCE)
    real_h, real_t = cronograma()
    assert (hechas, total) == (real_h, real_t), \
        f"el documento dice {hechas}/{total} y el cronograma {real_h}/{real_t}"


def test_las_diez_medidas_estan_y_solo_una_esta_retirada():
    numeros = [n for n, _, _, _ in estado.MEDIDAS]
    assert numeros == list(range(1, 11)), f"faltan o sobran medidas: {numeros}"

    retiradas = [n for n, _, e, _ in estado.MEDIDAS if e == "retirada"]
    assert retiradas == [recorte.MEDIDA_RETIRADA], \
        f"retiradas {retiradas}, y el recorte dice {recorte.MEDIDA_RETIRADA}"


def test_cada_medida_lleva_su_evidencia():
    """Un estado sin evidencia es una opinion, y es justo lo que la docente va a mirar."""
    for n, titulo, _, evidencia in estado.MEDIDAS:
        assert len(evidencia) > 60, f"la medida {n} ({titulo}) no explica que la cierra"


def test_cada_decision_dice_causa_efecto_y_leccion():
    for d in estado.DECISIONES:
        for campo in ("causa", "efecto", "leccion"):
            assert len(d[campo]) > 80, f"{d['titulo']}: {campo} es una afirmacion, no un argumento"


def test_cada_decision_remite_a_su_documento():
    """Este documento NO repite el contenido de los otros: remite a ellos."""
    nombres = {n for n, _ in estado.DOCUMENTOS}
    for d in estado.DECISIONES:
        assert d["doc"] in nombres, f"{d['titulo']} remite a {d['doc']}, que no esta en el mapa"


def test_los_documentos_del_mapa_existen():
    for nombre, _ in estado.DOCUMENTOS:
        if nombre.startswith("12_"):
            continue      # es este, se crea al generarlo
        ruta = os.path.join(RAIZ, "entregables", nombre)
        assert os.path.exists(ruta), f"el mapa cita {nombre} y no existe"


def test_cada_pendiente_tiene_responsable_y_riesgo():
    niveles = {"alto", "medio", "bajo"}
    for titulo, riesgo, detalle, quien in estado.PENDIENTE:
        assert riesgo in niveles, f"{titulo}: riesgo '{riesgo}' no es uno de {niveles}"
        assert quien.strip(), f"{titulo} no tiene responsable"
        assert len(detalle) > 50, f"{titulo} no explica que falta"


def test_cada_riesgo_dice_su_mitigacion():
    """Un riesgo sin mitigacion es una queja."""
    for titulo, nivel, detalle in estado.RIESGOS:
        assert nivel in {"alto", "medio", "bajo", "asumido"}, f"{titulo}: nivel '{nivel}'"
        assert len(detalle) > 60, f"{titulo} no explica el riesgo ni que se hace con el"


def test_hay_al_menos_un_riesgo_alto_declarado():
    """Un estado de proyecto sin riesgos altos a tres semanas del cierre no se creeria."""
    altos = [t for t, r, _ in estado.RIESGOS if r == "alto"]
    assert len(altos) >= 1, "no hay ningun riesgo alto declarado"
