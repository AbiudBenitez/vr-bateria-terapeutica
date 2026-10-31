# -*- coding: utf-8 -*-
"""
Retira del cronograma operativo las actividades que un recorte posterior dejo fuera.

POR QUE NO SE VUELVE A CORRER podar.py

`podar.py` genera el operativo DESDE el de ProjectLibre. Volver a correrlo hoy tendria
dos efectos indeseados:

  1. Se perderia DM.1, que existe solo en el operativo —la creo el recorte y por eso
     no esta en el cronograma anterior al recorte—.
  2. Los UID cambiarian. El operativo trae UID compactados del 1 al 166, porque despues
     de generarlo se abrio y se guardo en ProjectLibre; el de origen llega a 265. Un
     archivo con otros UID no es el mismo documento para la herramienta.

Asi que cuando el recorte crece, lo que corresponde es una retirada quirurgica: quitar
solo las tareas que sobran y reencadenar a sus sucesoras, dejando intacto todo lo demas.

REENCADENAR, NO BORRAR EL VINCULO

Si C dependia de B y B se retira, C pasa a depender de lo que dependia B. Es la misma
regla que aplica `podar.py` y la que sostiene el calculo de `rc_recorte.py`. Sin ella la
sucesora se queda sin antecedente y ProjectLibre la adelanta al inicio del proyecto.

Es idempotente: si no hay nada que retirar, no escribe.
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
OPERATIVO = os.path.join(RAIZ, "entregables", "Cronograma_Operativo.xml")


def clave(nombre):
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre or "")
    return m.group(1) if m else None


def retirar(ruta=OPERATIVO):
    arbol = ET.parse(ruta)
    tasks = arbol.getroot().find(NS + "Tasks")

    por_uid, fuera, nombre = {}, set(), {}
    for t in tasks.findall(NS + "Task"):
        uid = t.findtext(NS + "UID")
        nom = t.findtext(NS + "Name") or ""
        por_uid[uid] = t
        nombre[uid] = nom
        if t.findtext(NS + "Summary") != "1" and clave(nom) in recorte.RECORTADAS:
            fuera.add(uid)

    if not fuera:
        return [], 0, len([t for t in tasks.findall(NS + "Task")
                           if t.findtext(NS + "Summary") != "1"])

    preds = {u: [pl.findtext(NS + "PredecessorUID") for pl in t.findall(NS + "PredecessorLink")]
             for u, t in por_uid.items()}

    def vivas(uid, visto=None):
        visto = visto or set()
        out = []
        for p in preds.get(uid, []):
            if p is None or p in visto:
                continue
            visto.add(p)
            out.extend(vivas(p, visto) if p in fuera else [p])
        return out

    nuevas = {u: vivas(u) for u in por_uid if u not in fuera}

    for uid in fuera:
        tasks.remove(por_uid[uid])

    recableadas = 0
    for t in tasks.findall(NS + "Task"):
        uid = t.findtext(NS + "UID")
        antes = [pl.findtext(NS + "PredecessorUID") for pl in t.findall(NS + "PredecessorLink")]
        ahora = list(dict.fromkeys(nuevas.get(uid, [])))
        if antes == ahora:
            continue
        plantilla = t.find(NS + "PredecessorLink")
        tipo = plantilla.findtext(NS + "Type") if plantilla is not None else "1"
        for pl in t.findall(NS + "PredecessorLink"):
            t.remove(pl)
        for p in ahora:
            pl = ET.SubElement(t, NS + "PredecessorLink")
            ET.SubElement(pl, NS + "PredecessorUID").text = p
            ET.SubElement(pl, NS + "Type").text = tipo or "1"
            ET.SubElement(pl, NS + "CrossProject").text = "0"
        recableadas += 1

    # El ID ordena las filas en ProjectLibre; el UID identifica la tarea y no se toca.
    for i, t in enumerate(tasks.findall(NS + "Task")):
        el = t.find(NS + "ID")
        if el is not None:
            el.text = str(i)

    arbol.write(ruta, encoding="utf-8", xml_declaration=True)
    reales = len([t for t in tasks.findall(NS + "Task") if t.findtext(NS + "Summary") != "1"])
    return [nombre[u] for u in sorted(fuera, key=int)], recableadas, reales


if __name__ == "__main__":
    quitadas, recableadas, quedan = retirar()
    if not quitadas:
        print("  nada que retirar: el operativo ya no tiene recortadas")
    else:
        for nom in quitadas:
            print("  retirada:    %s" % nom[:70])
        print("  recableadas: %d sucesoras" % recableadas)
    print("  quedan:      %d actividades reales" % quedan)
