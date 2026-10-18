# -*- coding: utf-8 -*-
"""
Genera el cronograma PODADO: solo las actividades que el proyecto va a ejecutar.

El cronograma completo se conserva como evidencia histórica —se ve lo que se planeó, lo que se
recortó y por qué—, y este es el operativo, el que el equipo abre para trabajar.

Borrar tareas a secas rompe la red: 125 de los 395 vínculos apuntan a tareas recortadas. En vez
de tirarlos, se REENCADENAN: si B dependía de A y A se recorta, B pasa a depender de lo que
dependía A. Así la red sigue cerrada y las fechas siguen teniendo sentido.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recorte

NS = "{http://schemas.microsoft.com/project}"
ET.register_namespace("", "http://schemas.microsoft.com/project")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEN = os.path.join(RAIZ, "entregables", "Cronograma_ProjectLibre.xml")
DESTINO = os.path.join(RAIZ, "entregables", "Cronograma_Operativo.xml")


def clave(nombre):
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre or "")
    return m.group(1) if m else None


def podar():
    arbol = ET.parse(ORIGEN)
    raiz = arbol.getroot()
    tasks = raiz.find(NS + "Tasks")

    # --- qué se va ---
    fuera = set()
    por_uid = {}
    for t in tasks.findall(NS + "Task"):
        uid = t.findtext(NS + "UID")
        nom = t.findtext(NS + "Name") or ""
        res = t.findtext(NS + "Summary") == "1"
        por_uid[uid] = t
        if not res and clave(nom) in recorte.RECORTADAS:
            fuera.add(uid)

    # --- predecesoras directas de cada tarea, antes de tocar nada ---
    preds = {}
    for uid, t in por_uid.items():
        preds[uid] = [pl.findtext(NS + "PredecessorUID") for pl in t.findall(NS + "PredecessorLink")]

    def resolver(uid, visto=None):
        """
        Predecesoras vivas de `uid`, saltando las recortadas.

        Si A se recorta y B dependía de A, B hereda las predecesoras de A. Se repite hacia
        atrás hasta encontrar tareas vivas, de modo que no queda ningún hueco en la cadena.
        """
        if visto is None:
            visto = set()
        vivas = []
        for p in preds.get(uid, []):
            if p is None or p in visto:
                continue
            visto.add(p)
            if p in fuera:
                vivas.extend(resolver(p, visto))      # salta la recortada
            else:
                vivas.append(p)
        return vivas

    nuevas_preds = {uid: resolver(uid) for uid in por_uid if uid not in fuera}

    # --- borrar las recortadas ---
    for uid in fuera:
        tasks.remove(por_uid[uid])

    # --- reescribir los vínculos de las que quedan ---
    reencadenados = 0
    for t in tasks.findall(NS + "Task"):
        uid = t.findtext(NS + "UID")
        antiguos = [pl.findtext(NS + "PredecessorUID") for pl in t.findall(NS + "PredecessorLink")]
        nuevos = nuevas_preds.get(uid, [])
        if antiguos == nuevos:
            continue
        # Se conserva el tipo y la demora del PRIMER vínculo como plantilla: todos los de este
        # cronograma son fin-comienzo sin demora, así que no se pierde información.
        plantilla = t.find(NS + "PredecessorLink")
        tipo = plantilla.findtext(NS + "Type") if plantilla is not None else "1"
        for pl in t.findall(NS + "PredecessorLink"):
            t.remove(pl)
        for p in dict.fromkeys(nuevos):         # sin duplicados, conservando el orden
            pl = ET.SubElement(t, NS + "PredecessorLink")
            ET.SubElement(pl, NS + "PredecessorUID").text = p
            ET.SubElement(pl, NS + "Type").text = tipo or "1"
            ET.SubElement(pl, NS + "CrossProject").text = "0"
        reencadenados += 1

    # --- renumerar el ID, que ProjectLibre usa para el orden de las filas ---
    for i, t in enumerate(tasks.findall(NS + "Task")):
        el = t.find(NS + "ID")
        if el is not None:
            el.text = str(i)

    arbol.write(DESTINO, encoding="utf-8", xml_declaration=True)
    return len(fuera), reencadenados, len(tasks.findall(NS + "Task"))


if __name__ == "__main__":
    f, r_, q = podar()
    print(f"  eliminadas:    {f}")
    print(f"  reencadenadas: {r_}")
    print(f"  quedan:        {q} tareas (incluidos los 8 resúmenes)")
    print(f"  -> {os.path.basename(DESTINO)}")
