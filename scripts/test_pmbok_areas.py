# -*- coding: utf-8 -*-
"""
Pruebas de los nueve apartados del PMBOK.

LO QUE VIGILAN ES LO QUE NO SE VE AL ABRIR EL DOCUMENTO: que no falte un proceso del
estándar, que ninguna afirmación vaya sin evidencia, que las cifras no hayan divergido de su
fuente viva y que cada remisión apunte a un archivo que existe. Un documento con un proceso
de menos se lee perfectamente bien; solo falla cuando alguien lo cruza con el PMBOK.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import costos
import pmbok
import pmbok_areas
import pruebas
import recorte

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# El área 6 es la única sin documento propio: ya la cubren los dos cronogramas y los dos
# documentos de ruta crítica.
SIN_DOCUMENTO = {"6"}


def test_estan_los_nueve_modulos():
    faltan = pmbok_areas.faltantes()
    assert not faltan, f"faltan los modulos de las areas {faltan}"
    assert len(pmbok_areas.modulos()) == 9


def test_las_nueve_areas_son_las_diez_menos_cronograma():
    cubiertas = {m.AREA for m in pmbok_areas.modulos()}
    todas = {n for n, _ in pmbok.AREAS}
    assert cubiertas == todas - SIN_DOCUMENTO, (
        f"cubiertas {sorted(cubiertas)}, se esperaban {sorted(todas - SIN_DOCUMENTO)}")


def test_cada_area_cubre_exactamente_sus_procesos():
    """Ni uno de menos ni uno inventado. El numero y el nombre salen de pmbok.py, asi que un
    proceso que sobre aqui es uno que no existe en la 6.a edicion."""
    for m in pmbok_areas.modulos():
        del_estandar = {p[0] for p in pmbok.de_area(m.AREA)}
        declarados = set(m.PROCESOS)
        assert declarados == del_estandar, (
            f"area {m.AREA}: faltan {sorted(del_estandar - declarados)}, "
            f"sobran {sorted(declarados - del_estandar)}")


def test_ningun_proceso_va_sin_evidencia():
    """Un «que hizo el proyecto» sin «con que se demuestra» es una afirmacion, y es justo lo
    que la docente va a mirar primero."""
    for m in pmbok_areas.modulos():
        for num, (que_hizo, evidencia) in m.PROCESOS.items():
            assert len(que_hizo) > 80, f"{num}: dice poco sobre lo que hizo el proyecto"
            assert len(evidencia) > 25, f"{num}: no trae evidencia verificable"


def test_cada_area_tiene_resumen_y_lecciones():
    """Un area de conocimiento sin lecciones es un area que se planeo y no se ejecuto."""
    for m in pmbok_areas.modulos():
        assert len(m.RESUMEN) >= 2, f"area {m.AREA}: el resumen no llega a dos parrafos"
        for p in m.RESUMEN:
            assert len(p) > 150, f"area {m.AREA}: un parrafo del resumen es demasiado corto"
        assert len(m.LECCIONES) >= 2, f"area {m.AREA}: menos de dos lecciones"
        for titulo, texto in m.LECCIONES:
            assert len(texto) > 180, f"area {m.AREA}, leccion '{titulo}': es una frase"


def test_cada_area_trae_al_menos_una_tabla():
    for m in pmbok_areas.modulos():
        assert m.TABLAS, f"area {m.AREA}: sin tablas"
        for titulo, encabezados, filas in m.TABLAS:
            assert encabezados, f"area {m.AREA}, tabla '{titulo}': sin encabezados"
            assert filas, f"area {m.AREA}, tabla '{titulo}': sin filas"
            for i, f in enumerate(filas):
                assert len(f) == len(encabezados), (
                    f"area {m.AREA}, tabla '{titulo}', fila {i}: "
                    f"{len(f)} celdas contra {len(encabezados)} encabezados")


def test_las_remisiones_apuntan_a_archivos_que_existen():
    for m in pmbok_areas.modulos():
        for ruta, _ in m.REMITE_A:
            completa = os.path.join(RAIZ, ruta)
            assert os.path.exists(completa), (
                f"area {m.AREA} remite a '{ruta}', que no existe")


# ----------------------------------------------------------------- las cifras no divergen

def test_el_presupuesto_de_costos_sale_de_costos_py():
    import pmbok_areas.a07 as a07
    texto = " ".join(a07.RESUMEN) + " ".join(
        c for _, _, filas in a07.TABLAS for f in filas for c in f)
    assert f"{costos.MANO_OBRA:,.0f}" in texto, (
        f"el area 7 no cita el presupuesto vigente de {costos.MANO_OBRA:,.0f}")


def test_el_esfuerzo_de_recursos_sale_de_costos_py():
    import pmbok_areas.a09 as a09
    assert f"{costos.HORAS_TOT:,.0f}" in " ".join(a09.RESUMEN), (
        "el area 9 no cita el esfuerzo que calcula costos.py")


def test_la_medida_retirada_coincide_con_el_recorte():
    import pmbok_areas.a05 as a05
    retiradas = [n for n, _ in a05.TABLAS[0][2] and
                 [(f[0], f[2]) for f in a05.TABLAS[0][2]] if _ == "RETIRADA"]
    assert retiradas == [str(recorte.MEDIDA_RETIRADA)], (
        f"el area 5 declara retiradas {retiradas} y el recorte dice "
        f"{recorte.MEDIDA_RETIRADA}")


def test_el_alcance_vigente_coincide_con_el_cronograma():
    """Si alguien cierra actividades y no actualiza el area 5, el documento miente."""
    import re
    import pmbok_areas.a05 as a05
    t = open(os.path.join(RAIZ, "entregables", "Cronograma_Operativo.xml"),
             encoding="utf-8").read()
    reales = hechas = 0
    for b in re.findall(r"<Task>.*?</Task>", t, re.S):
        nm = re.search(r"<Name>(.*?)</Name>", b, re.S)
        sm = re.search(r"<Summary>(\d)</Summary>", b)
        pc = re.search(r"<PercentComplete>(\d+)</PercentComplete>", b)
        if not nm or (sm and sm.group(1) == "1"):
            continue
        reales += 1
        if pc and pc.group(1) == "100":
            hechas += 1
    assert (a05.VIGENTES, a05.HECHAS) == (reales, hechas), (
        f"el area 5 dice {a05.HECHAS} de {a05.VIGENTES} y el cronograma {hechas} de {reales}")


def test_el_registro_de_riesgos_coincide_con_pruebas_py():
    import pmbok_areas.a11 as a11
    filas = a11.TABLAS[0][2]
    assert len(filas) == len(pruebas.RIESGOS), (
        f"el area 11 tabula {len(filas)} riesgos y pruebas.py tiene "
        f"{len(pruebas.RIESGOS)}")
    assert str(len(pruebas.RIESGOS)) in " ".join(a11.RESUMEN)


def test_los_catalogos_de_calidad_coinciden_con_pruebas_py():
    import pmbok_areas.a08 as a08
    blanca = next(f for t, _, f in a08.TABLAS if "caja blanca" in t.lower())
    negra = next(f for t, _, f in a08.TABLAS if "caja negra" in t.lower())
    assert len(blanca) == len(pruebas.CAJA_BLANCA)
    assert len(negra) == len(pruebas.CAJA_NEGRA)


def test_integracion_declara_por_que_falta_el_cronograma():
    """La carpeta tiene nueve documentos para diez areas. El hueco tiene que estar explicado
    dentro, no solo en el mensaje de quien la entrega."""
    import pmbok_areas.a04 as a04
    texto = " ".join(c for _, _, filas in a04.TABLAS for f in filas for c in f)
    assert "SIN DOCUMENTO PROPIO" in texto, (
        "el area 4 no declara que el cronograma no lleva documento propio")
    assert "Cronograma_Operativo.xml" in texto


def test_integracion_y_alcance_dicen_el_mismo_avance():
    """Dos documentos de la misma carpeta que declaran avances distintos es el defecto que
    este proyecto ya cometió con los dos cronogramas. Aqui no puede repetirse: los dos leen
    avance_vigente(), y esta prueba lo comprueba."""
    import pmbok_areas.a04 as a04
    import pmbok_areas.a05 as a05
    assert (a04.VIGENTES, a04.HECHAS) == (a05.VIGENTES, a05.HECHAS), (
        f"integracion dice {a04.HECHAS} de {a04.VIGENTES} y alcance "
        f"{a05.HECHAS} de {a05.VIGENTES}")


def test_ninguna_area_escribe_el_avance_a_mano():
    """El numero literal del avance no debe aparecer asignado en el codigo de ningun modulo:
    tiene que venir de avance_vigente()."""
    import glob
    vig, hechas = pmbok_areas.avance_vigente()
    for ruta in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "pmbok_areas", "a*.py")):
        src = open(ruta, encoding="utf-8").read()
        for mal in (f"VIGENTES = {vig}", f"HECHAS = {hechas}",
                    f"VIGENTES, HECHAS = {vig}, {hechas}"):
            assert mal not in src, (
                f"{os.path.basename(ruta)} escribe el avance a mano: '{mal}'. "
                "Usa pmbok_areas.avance_vigente().")
