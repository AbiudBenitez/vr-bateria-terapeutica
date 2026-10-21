# -*- coding: utf-8 -*-
"""
Copia el AVANCE del cronograma operativo al de ProjectLibre, actividad por actividad.

LOS DOS CRONOGRAMAS SON DOS DOCUMENTOS DISTINTOS, NO UNO DESFASADO

    Cronograma_ProjectLibre.xml   las 257 actividades de la lista original, con las 100
                                  recortadas marcadas [FUERA DE ALCANCE] en sus notas.
                                  Es la evidencia de lo que se planeo y de que se quito.

    Cronograma_Operativo.xml      las 158 que sobrevivieron al recorte. Es el que se
                                  trabaja.

El ALCANCE de cada uno es distinto a proposito y no se toca. Lo que no puede diferir es el
AVANCE: si una actividad esta hecha, lo esta en los dos, porque es la misma actividad. El
operativo manda, porque es donde se marca.

DM.1 NO SE AÑADE AL DE PROJECTLIBRE, Y ES DELIBERADO

DM.1 la creo el recorte -su nota lo dice: [AÑADIDA POR EL RECORTE]-. Meterla en el cronograma
anterior al recorte lo convertiria en un documento que ya no representa lo que se planeo, que
es justo su unica razon de existir. Por eso el de ProjectLibre llega a 130 de 157 y el
operativo a 131 de 158: el mismo 83 %, con un numerador y un denominador mas.

OJO CON LOS HITOS DE DURACION CERO

ProjectLibre deriva el porcentaje de la duracion, asi que un hito sin duracion vuelve a cero
en cuanto alguien abre y guarda el archivo. Tras correr esto conviene pasar hitos.py --guardar.
"""
import os
import re
import sys

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OPERATIVO = os.path.join(RAIZ, "entregables", "Cronograma_Operativo.xml")
PROJECTLIBRE = os.path.join(RAIZ, "entregables", "Cronograma_ProjectLibre.xml")


def clave(nombre):
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre or "")
    return m.group(1) if m else None


def tareas(texto):
    """{clave: bloque} de las tareas reales, sin resumenes."""
    out = {}
    for b in re.findall(r"<Task>.*?</Task>", texto, re.S):
        nm = re.search(r"<Name>(.*?)</Name>", b, re.S)
        sm = re.search(r"<Summary>(\d)</Summary>", b)
        if not nm or (sm and sm.group(1) == "1"):
            continue
        k = clave(nm.group(1).strip())
        if k:
            out[k] = b
    return out


def hecha(bloque):
    pc = re.search(r"<PercentComplete>(\d+)</PercentComplete>", bloque)
    return bool(pc) and pc.group(1) == "100"


def evidencia(bloque):
    """La linea [HECHA ...] de las notas, si la hay."""
    no = re.search(r"<Notes>(.*?)</Notes>", bloque, re.S)
    if not no:
        return None
    for linea in no.group(1).split("\n"):
        if linea.strip().startswith("[HECHA "):
            return linea.strip()
    return None


def cerrar(bloque, nota):
    """Devuelve el bloque marcado como completo, en el dialecto de ProjectLibre.

    Los tres a la vez: Stop igual a Finish, PercentComplete y PercentWorkComplete. Con solo
    los porcentajes la tarea sale al 0 % en el Gantt; con solo Stop, a medias.
    """
    fin = re.search(r"<Finish>(.*?)</Finish>", bloque)
    if not fin:
        return None

    if "<Stop>" in bloque:
        bloque = re.sub(r"<Stop>.*?</Stop>", "<Stop>%s</Stop>" % fin.group(1), bloque)
    else:
        bloque = bloque.replace("<Finish>", "<Stop>%s</Stop><Finish>" % fin.group(1), 1)

    bloque = re.sub(r"<PercentComplete>\d+</PercentComplete>",
                    "<PercentComplete>100</PercentComplete>", bloque)
    bloque = re.sub(r"<PercentWorkComplete>\d+</PercentWorkComplete>",
                    "<PercentWorkComplete>100</PercentWorkComplete>", bloque)

    # La evidencia viaja con el avance. Un 100 % sin poder decir que lo demuestra es como se
    # llega a un porcentaje que nadie puede defender.
    if nota:
        if "<Notes>" in bloque:
            if nota not in bloque:
                bloque = re.sub(r"<Notes>(.*?)</Notes>",
                                lambda m: "<Notes>%s\n%s</Notes>" % (m.group(1), nota),
                                bloque, flags=re.S)
        else:
            bloque = bloque.replace("</Task>", "<Notes>%s</Notes></Task>" % nota)
    return bloque


def main(escribir=True):
    op_txt = open(OPERATIVO, encoding="utf-8").read()
    pl_txt = open(PROJECTLIBRE, encoding="utf-8").read()

    op, pl = tareas(op_txt), tareas(pl_txt)

    sincronizadas, ausentes, ya = [], [], []

    for k, bloque_op in sorted(op.items()):
        if not hecha(bloque_op):
            continue
        if k not in pl:
            ausentes.append(k)
            continue
        if hecha(pl[k]):
            ya.append(k)
            continue

        nuevo = cerrar(pl[k], evidencia(bloque_op))
        if nuevo is None:
            continue
        pl_txt = pl_txt.replace(pl[k], nuevo, 1)
        sincronizadas.append(k)

    # El camino inverso: hecha en ProjectLibre y no en el operativo. No se toca -el operativo
    # manda- pero se avisa, porque significa que alguien marco en el archivo equivocado.
    al_reves = sorted(k for k, b in pl.items()
                      if hecha(b) and k in op and not hecha(op[k]))

    if escribir and sincronizadas:
        open(PROJECTLIBRE, "w", encoding="utf-8").write(pl_txt)

    print("Sincronizadas %d:" % len(sincronizadas))
    for k in sincronizadas:
        print("  %s" % k)
    if ya:
        print("\nYa estaban hechas en los dos: %d" % len(ya))
    if ausentes:
        print("\nHechas en el operativo y AUSENTES del de ProjectLibre: %s" %
              ", ".join(ausentes))
        print("  DM.1 es el caso esperado: la creo el recorte, asi que no pertenece al")
        print("  cronograma anterior al recorte. Cualquier otra clave aqui es un defecto.")
    if al_reves:
        print("\nAVISO, hechas solo en el de ProjectLibre: %s" % ", ".join(al_reves))
        print("  El operativo manda. Si de verdad estan hechas, marcalas alli.")
    return sincronizadas, ausentes, al_reves


if __name__ == "__main__":
    main(escribir="--dry-run" not in sys.argv)
