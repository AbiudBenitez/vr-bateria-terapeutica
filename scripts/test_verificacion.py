# -*- coding: utf-8 -*-
"""Pruebas del documento 19, la lista de verificacion de compromisos.

ES UN DOCUMENTO QUE SE FIRMA, y eso cambia lo que hay que vigilar. No basta con que las
cifras cuadren: hay que impedir que el papel nuevo contradiga al que la docente ya tiene.

Lo que estas pruebas impiden:

  - que una de las 257 tareas se pierda, se duplique o cambie de texto
  - que una tarea marcada como hecha a medio curso aparezca aqui sin su marca, o sea que la
    firma retire trabajo ya reportado
  - que una recortada aparezca como pendiente, o sea que la firma comprometa trabajo que el
    proyecto decidio no hacer
  - que una tarea fuera de alcance salga sin la razon del recorte
  - que las cifras del texto se escriban a mano y se desfasen de los datos
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cierres
import gen_verificacion as G
import recorte
import verificacion as V

from docx import Document


DOC = Document(G.DOC)


def texto():
    trozos = [p.text for p in DOC.paragraphs]
    for t in DOC.tables:
        for r in t.rows:
            for c in r.cells:
                trozos.append(c.text)
    return "\n".join(trozos)


TXT = texto()

# Las tablas por responsable son las de seis columnas con esa cabecera exacta.
TABLAS_RESP = [t for t in DOC.tables
               if len(t.columns) == 6 and t.rows[0].cells[0].text == "Clave"
               and t.rows[0].cells[3].text == "Estado"]

FILAS = {}
for _t in TABLAS_RESP:
    for _f in _t.rows[1:]:
        _c = [x.text.strip() for x in _f.cells]
        assert _c[0] not in FILAS, "la tarea %s sale dos veces en el documento" % _c[0]
        FILAS[_c[0]] = _c


# ------------------------------------------------------------------ las 257

def test_estan_las_doscientas_cincuenta_y_siete_una_sola_vez():
    assert len(V.TAREAS) == V.TOTAL
    assert len(FILAS) == V.TOTAL, "el documento lleva %d tareas, no %d" % (
        len(FILAS), V.TOTAL)
    assert set(FILAS) == set(V.TAREAS)


def test_el_texto_de_cada_tarea_es_el_de_la_hoja_de_control():
    """Se copian del original. Si alguna se reescribe, el papel deja de ser verificable."""
    for clave, fila in FILAS.items():
        assert fila[1] == V.TAREAS[clave]["tarea"], clave


def test_las_ocho_secciones_son_las_del_papel_entregado():
    assert len(TABLAS_RESP) == 8
    assert len(V.ORDEN_RESPONSABLES) == 8
    for resp in V.ORDEN_RESPONSABLES:
        assert "Responsable: %s" % resp in TXT, resp


def test_cada_tarea_va_con_el_responsable_de_la_hoja_de_control():
    grupos = V.por_responsable()
    assert sum(len(g) for g in grupos.values()) == V.TOTAL
    for resp, tareas in grupos.items():
        for t in tareas:
            assert t["responsable"] == resp


def test_todas_las_fechas_de_compromiso_salen_en_el_mismo_formato():
    """El papel entregado mezclaba 7/09/2026 con 07/09/2026 y traia dos celdas corruptas."""
    for clave, fila in FILAS.items():
        assert re.fullmatch(r"\d\d/\d\d/\d{4}", fila[2]), "%s: fecha %r" % (clave, fila[2])


# ------------------------------------------------------------------ los estados

def test_los_cuatro_estados_reparten_las_doscientas_cincuenta_y_siete():
    r = V.resumen()
    assert r[V.HECHO] + r[V.PENDIENTE] + r[V.HECHO_FUERA] + r[V.FUERA] == V.TOTAL


def test_cada_tarea_lleva_uno_de_los_cuatro_estados():
    for clave, fila in FILAS.items():
        estado = fila[3]
        # Las hechas llevan la fecha real entre parentesis.
        base = estado.split(" (")[0]
        assert base in V.ESTADOS, "%s: estado %r" % (clave, estado)


def test_ninguna_recortada_aparece_como_pendiente():
    """Firmarla como pendiente es comprometerse a hacer lo que el proyecto decidio no hacer."""
    for clave in recorte.RECORTADAS:
        if clave not in FILAS:
            continue
        assert FILAS[clave][3] != V.PENDIENTE, \
            "%s esta fuera de alcance y sale como pendiente" % clave


def test_ninguna_hecha_a_medio_curso_pierde_su_marca():
    """LA PRUEBA CENTRAL. El papel nuevo no puede retirar trabajo que el anterior reporto.

    32 de las recortadas estaban marcadas como hechas a medio curso: el Audio Mixer se
    construyo y luego se descarto, el agarre de baquetas se implemento y murio cuando
    quedaron solidarias al control. Si el recorte les borrara la marca, la docente veria 32
    tareas pasar de hechas a no hechas al cruzar los dos documentos.
    """
    perdidas = [c for c, t in V.TAREAS.items()
                if t["medio_curso"] and "Hecho" not in FILAS[c][3]]
    assert not perdidas, "estas perdieron la marca de hechas: %s" % sorted(perdidas)


def test_las_hechas_y_recortadas_declaran_las_dos_cosas():
    hf = [c for c, t in V.TAREAS.items() if t["estado"] == V.HECHO_FUERA]
    assert len(hf) == 32, "cambiaron las hechas-y-recortadas: %d" % len(hf)
    for clave in hf:
        estado = FILAS[clave][3]
        assert "Hecho" in estado and "fuera de alcance" in estado, "%s: %r" % (clave, estado)
    for clave in ("SM.1", "DO", "IT.1", "JK"):
        assert V.TAREAS[clave]["estado"] == V.HECHO_FUERA, clave


def test_las_hechas_llevan_la_fecha_de_cierre_real_no_la_del_plan():
    """La fecha de compromiso es del plan; la del parentesis es la del artefacto que la cierra."""
    distintas = 0
    for clave, t in V.TAREAS.items():
        if t["estado"] != V.HECHO:
            continue
        assert t["cerrada_el"], "%s esta hecha y no dice cuando" % clave
        aaaa, mm, dd = t["cerrada_el"].split("-")
        assert "%s/%s/%s" % (dd, mm, aaaa) in FILAS[clave][3], clave
        if "%s/%s/%s" % (dd, mm, aaaa) != t["compromiso"]:
            distintas += 1
    assert distintas > 100, \
        "casi ninguna fecha real difiere de la planeada: se esta copiando el plan"


def test_no_se_lee_la_columna_estado_del_xlsx():
    """Quedo congelada en septiembre: 235 de 257 dicen Bloqueada y el proyecto lleva 137 hechas.

    DP.1 es el caso que lo demuestra: la hoja dice «Sin empezar» y es la primera actividad
    del proyecto, cerrada con el commit que crea el proyecto de Unity.
    """
    assert V.TAREAS["DP.1"]["estado"] == V.HECHO
    assert V.resumen()[V.HECHO] > 100


# ------------------------------------------------------------------ lo que se firma

def test_las_pendientes_son_las_del_cronograma():
    vivas = set(V.TAREAS) - set(recorte.RECORTADAS)
    esperadas = sorted(vivas - set(cierres.CIERRES))
    obtenidas = sorted(c for c, t in V.TAREAS.items() if t["estado"] == V.PENDIENTE)
    assert obtenidas == esperadas
    assert len(obtenidas) == 17


def test_toda_pendiente_sale_en_la_seccion_de_lo_que_queda_abierto():
    tabla = next(t for t in DOC.tables
                 if [c.text for c in t.rows[0].cells] ==
                 ["Clave", "Tarea", "Responsable", "Fecha compromiso"])
    claves = {f.cells[0].text.strip() for f in tabla.rows[1:]}
    pendientes = {c for c, t in V.TAREAS.items() if t["estado"] == V.PENDIENTE}
    assert claves == pendientes


def test_el_documento_dice_a_que_compromete_la_firma():
    assert "Con mi firma" in TXT
    assert "Firma de la encargada del proyecto" in TXT
    r = V.resumen()
    assert str(r[V.PENDIENTE]) in TXT
    assert str(r["recortadas"]) in TXT


# ------------------------------------------------------------------ el anexo

def test_el_anexo_lleva_las_ciento_tres_con_su_razon():
    anexo = next(t for t in DOC.tables
                 if [c.text for c in t.rows[0].cells] ==
                 ["Clave", "Tarea", "Estado", "Razón del recorte"])
    filas = {f.cells[0].text.strip(): f.cells[3].text.strip() for f in anexo.rows[1:]}
    assert set(filas) == set(recorte.RECORTADAS)
    assert len(filas) == 103
    for clave, razon in filas.items():
        assert len(razon) > 15, "%s sale fuera de alcance sin razon: %r" % (clave, razon)


def test_toda_razon_del_anexo_se_lee_sola():
    """EL ANEXO VA ALFABETICO, no agrupado por area como el documento 10.

    Alli «Misma razon» y «Depende de AB.1» funcionan porque la de arriba esta a la vista. Aqui
    cada fila se lee sola, asi que una razon que remite a otra actividad tiene que traerse la
    razon de aquella, y una que solo repite el nombre de la tarea tiene que dar el motivo.
    """
    # NO SE MIDE POR LARGO. «Combo. Recortada en R14» son 23 caracteres y dice todo lo que
    # hay que decir, mientras que «Sonidos de interfaz» son 19 y no dice nada: repite el
    # nombre de la tarea. Lo que se exige es que haya un motivo ADEMAS del nombre, o sea una
    # segunda oracion, que es justo lo que las doce razones ampliadas no tenian.
    for clave in recorte.RECORTADAS:
        r = V.razon(clave)
        assert not re.fullmatch(r"Depende de [A-Z.\d]+", r), clave
        assert not r.rstrip(". ").endswith("Misma razón"), \
            "%s remite a la razon anterior y aqui no hay anterior: %r" % (clave, r)

        partes = re.split(r"(?:\.\s+|:\s+|\s—\s)", r, maxsplit=1)
        assert len(partes) == 2 and len(partes[1].strip()) >= 12, \
            "%s solo nombra la tarea, no dice por que se recorto: %r" % (clave, r)

        # La razon original nunca se pierde: se amplia, no se sustituye.
        assert recorte.RECORTADAS[clave].rstrip(". ") in r, clave


def test_cada_remision_apunta_a_una_recortada_de_verdad():
    for clave, destino in V.REMITE_A.items():
        assert clave in recorte.RECORTADAS, clave
        assert destino in recorte.RECORTADAS, \
            "%s remite a %s, que no esta recortada" % (clave, destino)
        assert destino not in V.REMITE_A, \
            "%s remite a %s, que remite a su vez: la cadena no se resuelve" % (clave, destino)


def test_toda_ampliacion_es_de_una_recortada():
    for clave in V.RAZON_AMPLIADA:
        assert clave in recorte.RECORTADAS, clave


def test_el_anexo_explica_r14_porque_varias_razones_lo_nombran():
    assert any("R14" in v for v in recorte.RECORTADAS.values())
    assert "baja de un integrante" in TXT
    assert V.R14[:60] in TXT


def test_el_anexo_remite_al_documento_del_recorte():
    assert "10_Recorte_de_Alcance.docx" in TXT


# ------------------------------------------------------------------ las correcciones

def test_las_tres_correcciones_al_papel_entregado_estan_nombradas():
    assert len(V.CORRECCIONES) == 3
    for clave, campo, razon in V.CORRECCIONES:
        assert clave in TXT
        assert len(razon) > 60, "la correccion de %s no se explica" % clave
        assert razon[:50] in TXT


def test_al_uno_queda_con_el_responsable_de_la_hoja_de_control():
    """El papel entregado la pone con Sarai; la hoja de control, con Kimberly."""
    assert V.TAREAS["AL.1"]["responsable"] == "Kimberly"
    grupos = V.por_responsable()
    assert any(t["clave"] == "AL.1" for t in grupos["Kimberly"])
    assert len(grupos["Sarai"]) == 31
    assert len(grupos["Kimberly"]) == 32


def test_las_fechas_corruptas_no_llegan_al_documento():
    for basura in ("f2a0lt2a6", "7/09/2026 1", "sust"):
        assert basura not in FILAS["EB.3"][2]
        assert basura not in FILAS["ML.1"][2]
    assert FILAS["EB.3"][2] == "07/09/2026"
    assert FILAS["ML.1"][2] == "07/09/2026"


# ------------------------------------------------------------------ las cifras del texto

def test_las_cifras_del_resumen_por_responsable_salen_de_los_datos():
    tabla = next(t for t in DOC.tables if t.rows[0].cells[0].text == "Responsable")
    for fila in tabla.rows[1:]:
        c = [x.text.strip() for x in fila.cells]
        if c[0] == "TOTAL":
            r = V.resumen()
            assert c[1:] == [str(r["total"]), str(r[V.HECHO]), str(r[V.PENDIENTE]),
                             str(r[V.HECHO_FUERA]), str(r[V.FUERA])]
            continue
        cu = V.cuenta(V.por_responsable()[c[0]])
        assert c[1] == str(len(V.por_responsable()[c[0]]))
        assert c[2:] == [str(cu[V.HECHO]), str(cu[V.PENDIENTE]),
                         str(cu[V.HECHO_FUERA]), str(cu[V.FUERA])]


def test_el_documento_declara_el_avance_nuevo_desde_medio_curso():
    r = V.resumen()
    assert r["hechas_medio_curso"] == 131
    assert r["cerradas_despues"] == 38
    assert str(r["hechas_medio_curso"]) in TXT
    assert str(r["cerradas_despues"]) in TXT
    assert V.FECHA_CORTE in TXT
    assert V.FECHA_MEDIO_CURSO in TXT


def test_el_alcance_vigente_cuadra_con_el_recorte():
    r = V.resumen()
    assert r["vigentes"] == V.TOTAL - len(recorte.RECORTADAS)
    assert r["vigentes"] == 154, \
        "las 257 originales menos las recortadas; las 155 del cronograma incluyen DM.1, que " \
        "no esta en la hoja de control"


# ------------------------------------------------------------------ las fuentes

def test_el_papel_entregado_sigue_guardado_como_evidencia():
    """Es el unico registro de que las 32 se hicieron. Sin el, el estado no se puede derivar."""
    assert os.path.isfile(V.ENTREGADO), V.ENTREGADO
    assert os.path.isfile(V.HOJA), V.HOJA
