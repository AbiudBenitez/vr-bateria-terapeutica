# -*- coding: utf-8 -*-
"""
Marca las actividades recortadas en el cronograma, sin borrarlas.

NO SE BORRAN. Una actividad borrada no deja rastro de que existió ni de por qué se quitó, y
el valor de este recorte está justamente en que sea auditable.

Se escribe la razón en el campo de notas de cada tarea. NO se tocan los porcentajes ni las
fechas: ProjectLibre usa su propio <Stop> para el avance y al recalcular mueve fechas; editar
eso a mano ya costó tres intentos entenderlo.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recorte

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "entregables", "Cronograma_ProjectLibre.xml")
MARCA = "[FUERA DE ALCANCE]"


def clave(nombre):
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre)
    return m.group(1) if m else None


def escapar(t):
    """XML seguro: una razón con & o < rompería el archivo en silencio."""
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def marcar():
    with open(RUTA, encoding="utf-8", errors="ignore") as fh:
        s = fh.read()

    marcadas = []

    def arregla(m):
        t = m.group(1)
        nm = re.search(r"<Name>(.*?)</Name>", t)
        if not nm:
            return m.group(0)
        k = clave(nm.group(1))
        if k not in recorte.RECORTADAS:
            return m.group(0)
        if MARCA in t:
            return m.group(0)

        nota = f"{MARCA} {recorte.RECORTADAS[k]}"

        if "<Notes>" in t:
            t = re.sub(r"<Notes>.*?</Notes>", f"<Notes>{escapar(nota)}</Notes>", t, flags=re.S)
        else:
            # Notes va justo después de Name en el esquema MSPDI.
            t = t.replace(nm.group(0), nm.group(0) + f"\n\t\t\t<Notes>{escapar(nota)}</Notes>", 1)

        marcadas.append(k)
        return "<Task>" + t + "</Task>"

    s2 = re.sub(r"<Task>(.*?)</Task>", arregla, s, flags=re.S)

    with open(RUTA, "w", encoding="utf-8") as fh:
        fh.write(s2)

    return marcadas


if __name__ == "__main__":
    # `marcar()` solo devuelve las que ESCRIBIO en esta corrida: salta las que ya tenian la
    # marca. La version anterior restaba esas del total y las imprimia como "NO ENCONTRADAS EN
    # EL CRONOGRAMA", asi que una corrida normal -donde solo cambia una- sacaba una lista de
    # 102 claves con pinta de error. El script es idempotente a proposito; lo que hay que
    # distinguir es lo que se escribio, lo que ya estaba y lo que de verdad falta.
    ms = marcar()
    with open(RUTA, encoding="utf-8", errors="ignore") as fh:
        texto = fh.read()
    presentes, ausentes = set(), []
    for bloque in re.findall(r"<Task>.*?</Task>", texto, re.S):
        nm = re.search(r"<Name>(.*?)</Name>", bloque, re.S)
        if not nm:
            continue
        k = clave(nm.group(1))
        if k in recorte.RECORTADAS and MARCA in bloque:
            presentes.add(k)
    ausentes = sorted(set(recorte.RECORTADAS) - presentes)

    print("  marcadas en esta corrida: %d" % len(ms))
    if ms:
        for k in sorted(ms):
            print("     %-6s %s" % (k, recorte.RECORTADAS[k][:72]))
    print("  ya estaban marcadas:      %d" % (len(presentes) - len(set(ms))))
    print("  total con marca:          %d de %d" % (len(presentes), len(recorte.RECORTADAS)))
    if ausentes:
        print("  SIN MARCA O AUSENTES DEL ARCHIVO: %s" % ausentes)
    else:
        print("  Todas las recortadas llevan su razon en el campo de notas.")
