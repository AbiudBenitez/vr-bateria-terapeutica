# -*- coding: utf-8 -*-
"""Saca del cronograma operativo las actividades que ya no estan en el alcance.

POR QUE ESTO ES UNA REGLA Y NO UN PARCHE
----------------------------------------
Los dos cronogramas no son dos copias: son dos cosas distintas a proposito.

  Cronograma_ProjectLibre.xml   la linea base anterior, 257 actividades. Las recortadas se
                                QUEDAN, con su nota [FUERA DE ALCANCE] y la razon. Una
                                actividad borrada no deja rastro de por que se quito.
  Cronograma_Operativo.xml      SOLO lo que se va a ejecutar. Aqui una recortada no se marca:
                                se saca.

Cuando algo sale del alcance despues del recorte -como IT.1 el 18-nov- hay que tocar los dos,
y de dos maneras distintas. Este modulo es la del operativo. Sin el, el operativo acumula
actividades fuera de alcance y deja de ser lo que su nombre dice.

QUE SE LLEVA CONSIGO UNA TAREA AL SALIR. Tres cosas, y olvidar cualquiera deja el archivo
roto en silencio:

  1. su bloque <Task>
  2. los <PredecessorLink> de OTRAS tareas que la apuntan: un enlace a un UID que ya no
     existe es un archivo que ProjectLibre abre con las fechas movidas y sin decir por que
  3. sus <Assignment>: una asignacion a un UID inexistente arrastra su coste al total

EL PUENTE. La regla del recorte es que al cortar B en A -> B -> C se conecta A -> C. Aqui NO
se reconstruye el enlace en el XML, y la razon se comprueba antes de borrar: solo se saca una
tarea cuyas sucesoras esten TODAS cerradas. Una sucesora cerrada no espera a nadie, asi que
el puente no moveria ninguna fecha. Si alguna sucesora estuviera abierta, el modulo se niega
y lo dice: ahi el puente si importa y es una decision, no una limpieza.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cierres as CI
import recorte as C

AQUI = os.path.dirname(os.path.abspath(__file__))
RUTA = os.path.join(AQUI, "..", "entregables", "Cronograma_Operativo.xml")


def clave(nombre):
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre or "")
    return m.group(1) if m else None


def _tareas(texto):
    """[(bloque, clave, uid)] de las hojas con clave."""
    out = []
    for b in re.findall(r"<Task>.*?</Task>", texto, re.S):
        nm = re.search(r"<Name>(.*?)</Name>", b, re.S)
        uid = re.search(r"<UID>(\d+)</UID>", b)
        if not nm or not uid:
            continue
        k = clave(nm.group(1))
        if k:
            out.append((b, k, uid.group(1)))
    return out


def sobrantes(texto):
    """Claves presentes en el operativo que ya no estan en el alcance."""
    return [(b, k, u) for b, k, u in _tareas(texto) if k in C.RECORTADAS]


def sucesoras(texto, uid):
    """Claves de las tareas que declaran `uid` como predecesora."""
    out = []
    for b, k, _ in _tareas(texto):
        for pl in re.findall(r"<PredecessorLink>.*?</PredecessorLink>", b, re.S):
            m = re.search(r"<PredecessorUID>(\d+)</PredecessorUID>", pl)
            if m and m.group(1) == uid:
                out.append(k)
    return out


def sacar(texto, bloque, uid):
    """Quita la tarea, los enlaces que la apuntan y sus asignaciones."""
    texto = texto.replace(bloque, "", 1)
    # Los enlaces: se quita el <PredecessorLink> COMPLETO, no solo el UID.
    patron = re.compile(
        r"\s*<PredecessorLink>(?:(?!</PredecessorLink>).)*?"
        r"<PredecessorUID>%s</PredecessorUID>.*?</PredecessorLink>" % re.escape(uid), re.S)
    texto, enlaces = patron.subn("", texto)
    # Las asignaciones.
    pat_a = re.compile(
        r"\s*<Assignment>(?:(?!</Assignment>).)*?"
        r"<TaskUID>%s</TaskUID>.*?</Assignment>" % re.escape(uid), re.S)
    texto, asignaciones = pat_a.subn("", texto)
    return texto, enlaces, asignaciones


def main():
    texto = open(RUTA, encoding="utf-8").read()
    pendientes = sobrantes(texto)
    if not pendientes:
        print("El operativo ya solo tiene actividades del alcance vigente.")
        return 0

    problemas = []
    for _, k, uid in pendientes:
        abiertas = [s for s in sucesoras(texto, uid) if s not in CI.CIERRES]
        if abiertas:
            problemas.append((k, abiertas))
    if problemas:
        print("NO SACO NADA. Hay recortadas con sucesoras todavia abiertas, y ahi el puente")
        print("es una decision y no una limpieza:")
        for k, ab in problemas:
            print("  %-6s sucesoras abiertas: %s" % (k, ", ".join(ab)))
        return 1

    total_e = total_a = 0
    for bloque, k, uid in pendientes:
        suc = sucesoras(texto, uid)
        texto, e, a = sacar(texto, bloque, uid)
        total_e += e
        total_a += a
        print("Sacada %s (UID %s): %d enlace(s), %d asignacion(es)" % (k, uid, e, a))
        print("   razon: %s" % C.RECORTADAS[k])
        if suc:
            print("   sus sucesoras %s ya estaban cerradas: el puente no mueve ninguna fecha."
                  % ", ".join(suc))

    # Nadie debe quedar apuntando a un UID que ya no existe.
    vivos = {u for _, _, u in _tareas(texto)}
    huerfanos = sorted({m for m in re.findall(r"<PredecessorUID>(\d+)</PredecessorUID>", texto)
                        if m not in vivos})
    assert not huerfanos, "quedaron enlaces a UID inexistentes: %s" % huerfanos

    open(RUTA, "w", encoding="utf-8").write(texto)
    print()
    print("Hojas restantes: %d" % len(_tareas(texto)))
    print("Enlaces retirados %d, asignaciones retiradas %d" % (total_e, total_a))
    return 0


if __name__ == "__main__":
    sys.exit(main())
