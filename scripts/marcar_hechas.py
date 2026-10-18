# -*- coding: utf-8 -*-
"""
Marca como completas las actividades verificadas, en el dialecto de ProjectLibre.

ProjectLibre NO lee los campos Actual*. Su avance sale de tres cosas a la vez:

    <Stop> igual a <Finish>  +  PercentComplete 100  +  PercentWorkComplete 100

Poner solo los porcentajes deja la tarea al 0 % en la vista de Gantt; poner solo <Stop> la
deja a medias. Costó tres intentos entenderlo, así que está escrito aquí y no en la memoria
de nadie.

CADA ACTIVIDAD LLEVA SU EVIDENCIA. Marcar algo como hecho sin poder decir qué lo demuestra es
cómo se llega a un 70 % que nadie puede defender frente a la docente.
"""
import os
import re
import sys

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "entregables", "Cronograma_Operativo.xml")

# clave -> (fecha de cierre, evidencia verificable)
HECHAS = {
    "AA.3": ("2026-10-18",
             "Assets elegidos y copiados: Stage y Stadium Seats de Poly Pizza, "
             "skybox de Kenney, arbol y textura de tierra de Fantasy Forest"),
    "AA.4": ("2026-10-18",
             "Licencia de cada asset verificada en su pagina de origen. "
             "Dos regimenes distintos: CC0/CC BY 3.0 y Standard Unity Asset Store EULA"),
    "AP.1": ("2026-10-18",
             "Escena compuesta por script: Assets/Editor/ConstruirBosque.cs. "
             "Claro de bosque con 20 arboles en tres anillos y suelo texturizado"),
    "AL.2": ("2026-10-18",
             "Iluminacion y ambiente definidos: sol bajo calido o luna rasante, "
             "ambiente de tres tonos, niebla exponencial y sombras suaves"),
    "QC.4": ("2026-10-18",
             "Registro de assets y licencias en Assets/Entorno/ATRIBUCION.txt y "
             "entregables/ATRIBUCION_entorno.txt, con las restricciones de cada EULA"),
    "QT.6": ("2026-10-17",
             "42 pruebas EditMode de bateria: CrossSolver 7, DrumPad 6, PadVisual 7, "
             "SampleSelector 8, HitIntensity 5, KitLayout 4, DrumHitFanout 2, EscenaRig 3"),
    "QT.7": ("2026-10-17",
             "52 pruebas EditMode de ritmo: SessionStats 11, MusicalTime 8, TempoMap 8, "
             "HitJudge 7, HitRing 6, NoteMatcher 6, JuegoDeRitmo 6"),
}

# Escritas pero SIN VERIFICAR. No se marcan: el codigo existe, la medicion no.
# Marcar una medicion que nadie ha hecho es exactamente el tipo de dato que luego
# no se puede sostener.
PENDIENTES_DE_MEDIR = {
    "AO.5": "FpsProbe.cs escrito; falta correrlo en el visor y volcar el JSON",
    "QV.3": "misma medicion desde QA; depende de AO.5",
    "AS":   "LimiteSeguro.cs escrito; falta montarlo en la escena y verificarlo",
}


def clave(nombre):
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre or "")
    return m.group(1) if m else None


def main():
    texto = open(RUTA, encoding="utf-8").read()
    bloques = re.findall(r"<Task>.*?</Task>", texto, re.S)

    marcadas, nohay, yaestaban = [], [], []

    for b in bloques:
        nm = re.search(r"<Name>(.*?)</Name>", b, re.S)
        if not nm:
            continue
        k = clave(nm.group(1))
        if k not in HECHAS:
            continue

        pc = re.search(r"<PercentComplete>(\d+)</PercentComplete>", b)
        if pc and pc.group(1) == "100":
            yaestaban.append(k)
            continue

        fin = re.search(r"<Finish>(.*?)</Finish>", b)
        if not fin:
            nohay.append(k)
            continue

        nuevo = b
        # Stop = Finish: es de donde ProjectLibre deduce que la tarea cerro.
        if "<Stop>" in nuevo:
            nuevo = re.sub(r"<Stop>.*?</Stop>", "<Stop>%s</Stop>" % fin.group(1), nuevo)
        else:
            nuevo = nuevo.replace("<Finish>", "<Stop>%s</Stop><Finish>" % fin.group(1), 1)

        nuevo = re.sub(r"<PercentComplete>\d+</PercentComplete>",
                       "<PercentComplete>100</PercentComplete>", nuevo)
        nuevo = re.sub(r"<PercentWorkComplete>\d+</PercentWorkComplete>",
                       "<PercentWorkComplete>100</PercentWorkComplete>", nuevo)

        # La evidencia va en las notas: sin ella, un 100 % es una afirmacion sin respaldo.
        ev = "[HECHA %s] %s" % HECHAS[k]
        if "<Notes>" in nuevo:
            nuevo = re.sub(r"<Notes>(.*?)</Notes>",
                           lambda m: "<Notes>%s\n%s</Notes>" % (m.group(1), ev), nuevo, flags=re.S)
        else:
            nuevo = nuevo.replace("</Task>", "<Notes>%s</Notes></Task>" % ev)

        texto = texto.replace(b, nuevo, 1)
        marcadas.append(k)

    open(RUTA, "w", encoding="utf-8").write(texto)

    print("Marcadas %d:" % len(marcadas))
    for k in sorted(marcadas):
        print("  %-6s %s" % (k, HECHAS[k][1][:66]))
    if yaestaban:
        print("\nYa estaban al 100 %%: %s" % ", ".join(sorted(yaestaban)))
    if nohay:
        print("\nNO ENCONTRADAS: %s" % ", ".join(sorted(nohay)))
    print("\nSin marcar a proposito, falta medirlas:")
    for k, por in sorted(PENDIENTES_DE_MEDIR.items()):
        print("  %-6s %s" % (k, por))


if __name__ == "__main__":
    main()
