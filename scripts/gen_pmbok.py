# -*- coding: utf-8 -*-
"""
Genera los nueve documentos de áreas del PMBOK en entregables/pmbok/.

UN SOLO RENDERIZADOR, NUEVE MÓDULOS DE DATOS. La carpeta es un entregable: nueve documentos
con portadas, numeración y tablas distintas se leen como nueve trabajos sueltos, y lo que se
entrega es un conjunto. Aquí vive la forma; en pmbok_areas/aNN.py, el contenido.

LA ESTRUCTURA DEL ESTÁNDAR SE LEE, NO SE TECLEA. El número, el nombre y el grupo de proceso
salen de pmbok.py. Ningún módulo de área vuelve a escribir "Planificar la Gestión de los
Costos", así que no puede escribirlo mal ni quedarse con el nombre de otra edición.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import neutro
import pmbok
import pmbok_areas

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SALIDA = os.path.join(RAIZ, "entregables", "pmbok")

FECHA = "4 de noviembre de 2026"
SUBTITULO = "Simulación de Batería en Realidad Virtual con Enfoque Terapéutico"

# El archivo de cada área, indexado por el NÚMERO DE ÁREA tal como lo escribe pmbok.py: "5" y
# no "05". El cero de relleno va solo en el nombre del archivo, para que la carpeta ordene en
# el orden del PMBOK y no alfabéticamente, donde el 10 iría antes del 4.
ARCHIVO = {
    "4":  "04_Integracion_Acta.docx",
    "5":  "05_Alcance.docx",
    "7":  "07_Costos.docx",
    "8":  "08_Calidad.docx",
    "9":  "09_Recursos.docx",
    "10": "10_Comunicaciones.docx",
    "11": "11_Riesgos.docx",
    "12": "12_Adquisiciones.docx",
    "13": "13_Interesados.docx",
}


def nombre_area(num):
    for n, nombre in pmbok.AREAS:
        if n == num:
            return nombre
    raise KeyError(f"el area {num} no existe en pmbok.py")


def documento(mod):
    num = mod.AREA
    procesos = pmbok.de_area(num)

    doc = neutro.nuevo()
    neutro.portada(
        doc,
        nombre_area(num),
        SUBTITULO,
        [("Equipo", "Equipo A"),
         ("Fecha", FECHA),
         ("Área de conocimiento", f"{num}. {nombre_area(num)}"),
         ("Procesos del área", f"{len(procesos)}, según el PMBOK 6.ª edición"),
         ("Documento", f"{ARCHIVO[num]} — uno de los nueve apartados del PMBOK")],
    )

    # ------------------------------------------------------------------ 1
    neutro.H(doc, "1. Qué decidió el proyecto en esta área", 1)
    for parrafo in mod.RESUMEN:
        neutro.P(doc, parrafo)

    # ------------------------------------------------------------------ 2
    neutro.H(doc, "2. Los procesos del área", 1)
    neutro.P(doc,
             f"Los {len(procesos)} procesos que el PMBOK 6.ª edición define para esta área, "
             "con lo que el proyecto hizo en cada uno y con qué se demuestra. El número, el "
             "nombre y el grupo de proceso se toman del estándar.")
    neutro.table(
        doc,
        ["Proceso", "Grupo", "Qué hizo el proyecto", "Evidencia"],
        [[f"{p[0]} {p[1]}", pmbok.GAB[p[3]],
          mod.PROCESOS[p[0]][0], mod.PROCESOS[p[0]][1]]
         for p in procesos],
        widths=[3.4, 0.9, 5.6, 5.6], fs=8.0,
    )

    # ------------------------------------------------------------------ 3..n
    n = 3
    for titulo, encabezados, filas in mod.TABLAS:
        neutro.H(doc, f"{n}. {titulo}", 1)
        anchos = [15.5 / len(encabezados)] * len(encabezados)
        neutro.table(doc, encabezados, filas, widths=anchos, fs=8.0)
        n += 1

    # ------------------------------------------------------------------ lecciones
    if mod.LECCIONES:
        neutro.H(doc, f"{n}. Lecciones aprendidas", 1)
        neutro.P(doc,
                 "Lo que salió mal y qué enseñó. Un área de conocimiento sin lecciones es un "
                 "área que no se ejecutó, solo se planeó.")
        for titulo, texto in mod.LECCIONES:
            neutro.H(doc, titulo, 2)
            neutro.P(doc, texto)
        n += 1

    # ------------------------------------------------------------------ remite
    if mod.REMITE_A:
        neutro.H(doc, f"{n}. Dónde está el detalle", 1)
        neutro.P(doc,
                 "Este documento es autocontenido para el área. El detalle de nivel anexo "
                 "—los catálogos completos, el costeo actividad por actividad— vive en los "
                 "documentos vigentes del proyecto y no se recopia aquí: una cifra que vive en "
                 "dos sitios acaba diciendo dos cosas.")
        neutro.table(doc, ["Documento", "Qué detalle lleva"],
                     [[a, b] for a, b in mod.REMITE_A],
                     widths=[5.5, 10.0], fs=8.5)

    return doc


def main():
    os.makedirs(SALIDA, exist_ok=True)
    escritos = []
    for mod in pmbok_areas.modulos():
        ruta = os.path.join(SALIDA, ARCHIVO[mod.AREA])
        documento(mod).save(ruta)
        escritos.append((mod.AREA, ARCHIVO[mod.AREA], len(pmbok.de_area(mod.AREA))))

    print(f"  {len(escritos)} documentos en entregables/pmbok/")
    for num, archivo, cuantos in escritos:
        print(f"    {archivo:34s} area {num:>2s}  {cuantos} procesos")
    faltan = [n for n, _ in pmbok.AREAS if n not in ARCHIVO]
    print(f"\n  Area sin documento: {', '.join(faltan)} (cronograma, ya cubierta por el "
          "ProjectLibre y el 03_Ruta_Critica)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
