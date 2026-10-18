# -*- coding: utf-8 -*-
"""
Devuelve al cronograma el avance que tenia en un commit anterior.

POR QUE HACE FALTA. ProjectLibre no puede sostener el 100 % en hitos de duracion cero: deriva
el porcentaje de la duracion, y sin duracion el cociente es cero. Cada vez que alguien abre y
guarda el archivo, los hitos completos vuelven a cero. Hay 38 hitos asi en este cronograma.

POR QUE DESDE GIT Y NO DESDE UN ARCHIVO DE ESTADO. `hitos.py --guardar` anota el estado en un
archivo local, y si se corre DESPUES de una caida anota la caida como si fuera lo correcto.
Paso exactamente eso el 18 de octubre: el guardado quedo anclado a cinco hitos cuando habia
doce. El historial de git no tiene ese problema porque no se puede sobrescribir por accidente.

NO TOCA FECHAS NI DEPENDENCIAS. Solo devuelve <Stop>, <PercentComplete> y
<PercentWorkComplete> a las tareas que estaban completas en la referencia y ya no lo estan.
"""
import os
import re
import subprocess
import sys

RELATIVA = "entregables/Cronograma_Operativo.xml"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RUTA = os.path.join(RAIZ, RELATIVA)


def tareas(texto):
    """nombre -> (bloque, porcentaje, fin)"""
    fuera = {}
    for b in re.findall(r"<Task>.*?</Task>", texto, re.S):
        nm = re.search(r"<Name>(.*?)</Name>", b, re.S)
        if not nm:
            continue
        pc = re.search(r"<PercentComplete>(\d+)</PercentComplete>", b)
        fin = re.search(r"<Finish>(.*?)</Finish>", b)
        fuera[nm.group(1)] = (b, pc.group(1) if pc else "0", fin.group(1) if fin else None)
    return fuera


def completar(bloque, fin):
    """Marca el bloque como completo en el dialecto de ProjectLibre."""
    b = bloque
    if "<Stop>" in b:
        b = re.sub(r"<Stop>.*?</Stop>", "<Stop>%s</Stop>" % fin, b)
    else:
        b = b.replace("<Finish>", "<Stop>%s</Stop><Finish>" % fin, 1)
    b = re.sub(r"<PercentComplete>\d+</PercentComplete>",
               "<PercentComplete>100</PercentComplete>", b)
    b = re.sub(r"<PercentWorkComplete>\d+</PercentWorkComplete>",
               "<PercentWorkComplete>100</PercentWorkComplete>", b)
    return b


def main(ref):
    crudo = subprocess.run(["git", "show", "%s:%s" % (ref, RELATIVA)],
                           capture_output=True, cwd=RAIZ)
    if crudo.returncode or not crudo.stdout:
        print("No pude leer %s en %s" % (RELATIVA, ref))
        return 1

    antes = tareas(crudo.stdout.decode("utf-8"))
    texto = open(RUTA, encoding="utf-8").read()
    ahora = tareas(texto)

    caidas = [n for n, (_, pc, _) in antes.items()
              if pc == "100" and ahora.get(n, (None, "0", None))[1] != "100"]

    if not caidas:
        print("Nada que restaurar: el avance coincide con %s." % ref)
        return 0

    restauradas = 0
    for n in caidas:
        bloque, _, fin = ahora[n]
        if not fin:
            print("  SIN FECHA DE FIN, se omite: %s" % n[:60])
            continue
        texto = texto.replace(bloque, completar(bloque, fin), 1)
        restauradas += 1

    open(RUTA, "w", encoding="utf-8").write(texto)

    print("Restauradas %d de %d respecto a %s:\n" % (restauradas, len(caidas), ref))
    for n in sorted(caidas):
        dur = re.search(r"<Duration>(.*?)</Duration>", ahora[n][0])
        hito = "  (hito de duracion cero)" if dur and dur.group(1) == "PT0H0M0S" else ""
        print("  %s%s" % (n[:62], hito))
    print("\nSi vuelve a pasar, es que alguien abrio ProjectLibre y guardo.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "HEAD~2"))
