# -*- coding: utf-8 -*-
"""
Revisa y restaura los hitos que ProjectLibre devuelve a cero.

ProjectLibre deriva el porcentaje de avance de la duración de la tarea. Un hito tiene duración
cero, así que el cociente es cero y la herramienta lo reescribe a 0 % en CADA guardado. Hay 38
hitos en este cronograma y ninguno puede quedar marcado como completo por sí solo.

No es un defecto que se pueda arreglar en el archivo: es cómo funciona la herramienta. Lo que
sí se puede es detectar la caída y restaurarla, que es lo que hace este script.

    hitos.py            lista los hitos y su estado
    hitos.py --guardar  guarda qué hitos están al 100 % ahora
    hitos.py --restaurar restaura los que cayeron desde el último guardado
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://schemas.microsoft.com/project}"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRONO = os.path.join(RAIZ, "entregables", "Cronograma_ProjectLibre.xml")
ESTADO = os.path.join(RAIZ, "scripts", ".hitos_completos.json")


def clave(nombre):
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre)
    return m.group(1) if m else None


def leer():
    """Devuelve {clave: (es_hito, porcentaje)} de las tareas reales."""
    raiz = ET.parse(CRONO).getroot()
    out = {}
    for t in raiz.iter(NS + "Task"):
        nm = t.find(NS + "Name")
        sm = t.find(NS + "Summary")
        if nm is None or not nm.text or (sm is not None and sm.text == "1"):
            continue
        k = clave(nm.text)
        if not k:
            continue
        du = t.find(NS + "Duration")
        pc = t.find(NS + "PercentComplete")
        out[k] = (du is not None and du.text == "PT0H0M0S",
                  int(pc.text) if pc is not None and pc.text else 0)
    return out


def guardar():
    """Anota qué hitos están completos ahora, para poder detectar caídas después."""
    completos = sorted(k for k, (hito, pct) in leer().items() if hito and pct == 100)
    with open(ESTADO, "w", encoding="utf-8") as fh:
        json.dump(completos, fh, indent=2, ensure_ascii=False)
    return completos


def caidos():
    """Hitos que estaban completos la última vez y ahora no."""
    if not os.path.exists(ESTADO):
        return None
    with open(ESTADO, encoding="utf-8") as fh:
        antes = set(json.load(fh))
    ahora = leer()
    return sorted(k for k in antes if ahora.get(k, (False, 0))[1] != 100)


def restaurar(claves):
    """Vuelve a poner al 100 % los hitos indicados."""
    if not claves:
        return 0
    with open(CRONO, encoding="utf-8", errors="ignore") as fh:
        s = fh.read()

    objetivo = set(claves)
    n = [0]

    def f(m):
        t = m.group(1)
        nm = re.search(r"<Name>(.*?)</Name>", t)
        if not nm:
            return m.group(0)
        if clave(nm.group(1)) not in objetivo:
            return m.group(0)
        t = re.sub(r"<PercentComplete>\d+</PercentComplete>",
                   "<PercentComplete>100</PercentComplete>", t)
        t = re.sub(r"<PercentWorkComplete>\d+</PercentWorkComplete>",
                   "<PercentWorkComplete>100</PercentWorkComplete>", t)
        n[0] += 1
        return "<Task>" + t + "</Task>"

    s2 = re.sub(r"<Task>(.*?)</Task>", f, s, flags=re.S)
    with open(CRONO, "w", encoding="utf-8") as fh:
        fh.write(s2)

    ET.parse(CRONO)      # si el archivo quedó roto, revienta aquí y no en silencio
    return n[0]


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""

    if arg == "--guardar":
        c = guardar()
        print(f"  anotados {len(c)} hitos completos")
        if c:
            print(f"  {' '.join(c)}")
        return

    if arg == "--restaurar":
        c = caidos()
        if c is None:
            print("  No hay estado guardado. Corre primero: hitos.py --guardar")
            return
        if not c:
            print("  Ningún hito cayó. Nada que restaurar.")
            return
        n = restaurar(c)
        print(f"  restaurados {n}: {' '.join(c)}")
        print("  XML verificado tras la escritura")
        return

    # Sin argumentos: informe
    d = leer()
    hitos = {k: p for k, (h, p) in d.items() if h}
    completos = [k for k, p in hitos.items() if p == 100]
    print(f"  hitos de duración cero: {len(hitos)} de {len(d)} tareas")
    print(f"  al 100 %: {len(completos)}")

    c = caidos()
    if c is None:
        print("\n  Sin estado guardado. Corre: hitos.py --guardar")
    elif c:
        print(f"\n  CAYERON {len(c)} desde el último guardado:")
        print(f"    {' '.join(c)}")
        print("  Restaura con: hitos.py --restaurar")
    else:
        print("\n  Ningún hito cayó desde el último guardado.")


if __name__ == "__main__":
    main()
