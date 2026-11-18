# -*- coding: utf-8 -*-
"""Genera el documento 18: revision de la fundamentacion contra el prototipo. Cierra ET.2."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fundamentacion as F
import neutro

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")
DOC = os.path.join(SALIDA, "18_Revision_Fundamentacion.docx")


def doc():
    d = neutro.nuevo()
    pv = F.por_veredicto()

    neutro.portada(
        d, "Revisión de la fundamentación",
        "Qué se sostiene con el prototipo construido, y qué no",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha", F.FECHA_ET2),
         ("Actividad", "ET.2 — Revisar y actualizar la fundamentación según el funcionamiento")])

    # ------------------------------------------------------------------ 1
    neutro.H(d, "1. Para qué existe este documento", 1)
    neutro.P(d,
        "La fundamentación teórica se redactó el %s, antes de que el prototipo existiera. Esta "
        "revisión vuelve sobre cada una de sus afirmaciones ahora que sí existe, y dice una por "
        "una si se sostiene con lo construido, si hay que acotarla o si hay que retirarla."
        % F.FECHA_ET1)
    neutro.P(d,
        "La fundamentación original no se edita. Igual que con el acta y con el cambio de "
        "enfoque, lo que modifica algo ya escrito entra como revisión con su fecha: reescribir "
        "el original borraría la evidencia de que hubo una revisión, que es justo lo que el "
        "control de cambios existe para conservar.", bold=True)
    neutro.table(d, ["", ""], [
        ["Fundamentación original", F.FUENTE],
        ["Redactada", "%s, actividad ET.1" % F.FECHA_ET1],
        ["Revisada", "%s, actividad ET.2" % F.FECHA_ET2],
        ["Afirmaciones revisadas", str(len(F.AFIRMACIONES))],
    ], widths=[4.4, 10.6], fs=9, negritas_col0=True)

    # ------------------------------------------------------------------ 2
    neutro.H(d, "2. El resultado en una tabla", 1)
    neutro.table(d, ["Veredicto", "Cuántas", "Cuáles", "Qué significa"], [
        ["Sostenida", str(len(pv["sostenida"])), ", ".join(a[0] for a in pv["sostenida"]),
         "El prototipo hace lo que la afirmación dice, y hay con qué demostrarlo."],
        ["Acotada", str(len(pv["acotada"])), ", ".join(a[0] for a in pv["acotada"]),
         "Hace una parte. Se dice cuál, y la afirmación se reescribe más estrecha."],
        ["Retirada", str(len(pv["retirada"])), ", ".join(a[0] for a in pv["retirada"]),
         "No lo hace y no lo va a hacer en este alcance."],
    ], widths=[2.0, 1.4, 2.6, 9.0], fs=9, negritas_col0=True)
    neutro.P(d,
        "Ninguna afirmación se añadió para esta revisión. Las %d son las que la fundamentación "
        "declara: los cuatro marcos formales de referencia, las dos ventajas que prometen algo "
        "verificable y las dos limitaciones reconocidas." % len(F.AFIRMACIONES))

    # ------------------------------------------------------------------ 3
    neutro.H(d, "3. Afirmación por afirmación", 1)
    for aid, afirmacion, fuente, veredicto, hace, comprueba in F.AFIRMACIONES:
        neutro.H(d, "%s — %s" % (aid, veredicto.upper()), 2)
        neutro.table(d, ["", ""], [
            ["La afirmación", afirmacion],
            ["De dónde sale", fuente],
            ["Qué hace el prototipo", hace],
            ["Cómo se comprueba", comprueba],
        ], widths=[3.6, 11.4], fs=9, negritas_col0=True)

    # ------------------------------------------------------------------ 4
    neutro.H(d, "4. Qué cambia esto en la fundamentación", 1)
    neutro.P(d,
        "Cuatro consecuencias, para quien redacte las conclusiones y limitaciones del informe "
        "final.")
    for titulo, detalle in F.CONSECUENCIAS:
        neutro.P(d, titulo, bold=True, after=3)
        neutro.P(d, detalle)

    # ------------------------------------------------------------------ 5
    neutro.H(d, "5. La fundamentación reescrita, en un párrafo", 1)
    neutro.P(d,
        "El proyecto se ancla en Patterned Sensory Enhancement: una guía visual sincronizada "
        "con el patrón rítmico, que el prototipo implementa con un aro de anticipación por nota "
        "sobre la pieza que toca golpear y un aviso periférico para las piezas fuera del campo "
        "de visión. Sobre esa guía se apoyan dos medidas observables sin respaldo clínico: si "
        "la persona golpea a tiempo y si su pulso es estable. El antecedente que justifica "
        "estudiar la percusión con este fin es la evidencia psicosocial —drum circles, "
        "bienestar y regulación emocional—, y no la evidencia motriz, que describe poblaciones "
        "y resultados que este proyecto no declara.")
    neutro.P(d,
        "La validación es un estudio de factibilidad y usabilidad: muestra pequeña, de "
        "conveniencia, sesión única, sin grupo control, sin validación de un profesional y sin "
        "posibilidad de atribuir las sesiones registradas a participantes concretos. El hueco "
        "conocido del medio sigue siendo la ausencia de retroalimentación háptica real, "
        "compensada en parte con vibración del mando, respuesta sonora por debajo de los 30 "
        "milisegundos y respuesta visual del pad golpeado.")
    neutro.P(d,
        "Ese párrafo es lo que la fundamentación puede sostener hoy. Lo que decía antes está "
        "en el documento original, que se conserva.", italic=True)

    return d


if __name__ == "__main__":
    doc().save(DOC)
    pv = F.por_veredicto()
    print("OK", DOC)
    print("   %d afirmaciones: %d sostenidas, %d acotadas, %d retiradas · %d consecuencias"
          % (len(F.AFIRMACIONES), len(pv["sostenida"]), len(pv["acotada"]),
             len(pv["retirada"]), len(F.CONSECUENCIAS)))
