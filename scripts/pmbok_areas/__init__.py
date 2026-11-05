# -*- coding: utf-8 -*-
"""
Un módulo por área de conocimiento del PMBOK 6.ª edición. El cronograma no está: ya lo
cubren Cronograma_ProjectLibre.xml, Cronograma_Operativo.xml y 03_Ruta_Critica.docx.

Cada módulo exporta la MISMA forma, y por eso hay un solo renderizador: la carpeta tiene
que leerse como un conjunto y no como nueve documentos sueltos.

    AREA      el número del área. El nombre y el grupo de cada proceso NO se escriben aquí:
              se leen de pmbok.py, que ya tiene las 10 áreas y los 49 procesos.
    RESUMEN   un párrafo. Qué decidió el proyecto en esta área.
    PROCESOS  {numero: (que_hizo, evidencia)}. Uno por cada proceso del área, sin faltar
              ninguno y sin inventar ninguno; hay una prueba que lo comprueba.
    TABLAS    [(titulo, [encabezados], [[filas]])]
    LECCIONES [(titulo, texto)]. Qué salió mal y qué enseñó.
    REMITE_A  [(archivo, qué detalle lleva)]. El anexo vive en el documento vigente, no se
              recopia aquí.
"""

ORDEN = ["04", "05", "07", "08", "09", "10", "11", "12", "13"]


def modulos():
    """Los módulos que existen, en orden de área.

    TOLERANTE A PROPÓSITO, para poder renderizar mientras se escriben. Lo que garantiza que
    estén los nueve es test_pmbok_areas.py, no esta función: una excepción aquí solo diría
    que falta un archivo, y la prueba dice además cuál y contra qué lista.
    """
    import importlib
    out = []
    for n in ORDEN:
        try:
            out.append(importlib.import_module(f"pmbok_areas.a{n}"))
        except ModuleNotFoundError:
            pass
    return out


def faltantes():
    """Las áreas de ORDEN que todavía no tienen módulo."""
    import importlib.util
    return [n for n in ORDEN
            if importlib.util.find_spec(f"pmbok_areas.a{n}") is None]


def avance_vigente():
    """(actividades, hechas) del alcance vigente, leídas de Cronograma_Operativo.xml.

    SE LEE, NO SE ESCRIBE. Es la cifra que más veces ha divergido en este proyecto: durante
    dos semanas los dos cronogramas declararon 59 % y 83 % por marcarse a mano cada uno.

    OJO CON EL 155 CONTRA EL 156. El operativo tiene 156 actividades; el de ProjectLibre, una
    vez descontadas las 102 recortadas, tiene 155. La diferencia es exactamente DM.1, que la
    creó el recorte y por eso no existe en el cronograma anterior a él. La red de la ruta
    crítica v3 también cuenta 155, porque DM.1 no entra en el cálculo de CPM. Las tres cifras
    son correctas y miden cosas distintas.
    """
    import os
    import re

    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "entregables", "Cronograma_Operativo.xml")
    texto = open(ruta, encoding="utf-8").read()

    reales = hechas = 0
    for bloque in re.findall(r"<Task>.*?</Task>", texto, re.S):
        nombre = re.search(r"<Name>(.*?)</Name>", bloque, re.S)
        resumen = re.search(r"<Summary>(\d)</Summary>", bloque)
        pct = re.search(r"<PercentComplete>(\d+)</PercentComplete>", bloque)
        if not nombre or (resumen and resumen.group(1) == "1"):
            continue
        reales += 1
        if pct and pct.group(1) == "100":
            hechas += 1
    return reales, hechas
