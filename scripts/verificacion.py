# -*- coding: utf-8 -*-
"""Estado de las 257 tareas de la hoja de control. Unica fuente del documento 19.

QUE ES ESTE DOCUMENTO
---------------------
A medio curso se entrego a la docente una lista de verificacion de compromisos: las 257
tareas de la hoja de control del lider, agrupadas por responsable, con una marca de hecho y
un espacio para firmar. Ese papel esta en
`referencia/Lista_de_verificacion_compromisos_medio_curso.docx` y declaraba 131 hechas.

Despues de aquel corte pasaron dos cosas que el papel no puede contar:

  1. El recorte de alcance del 18-oct dejo FUERA a 103 de las 257. Firmarlas como pendientes
     seria comprometerse a trabajo que el proyecto decidio no hacer, con su razon escrita.
  2. Cerraron 38 actividades mas.

Asi que este modulo reconstruye el estado de cada una de las 257 al 18-nov-2026.

DE DONDE SALE CADA COSA
-----------------------
  tarea, responsable, area, fecha de compromiso  ->  la hoja de control (xlsx), que es el
                                                     original y no se toca
  fuera de alcance y su razon                    ->  recorte.RECORTADAS
  hecha y cuando de verdad                       ->  cierres.CIERRES
  hecha a medio curso                            ->  el docx entregado

LA COLUMNA `Estado` DEL XLSX NO SE LEE. Quedo congelada en septiembre: 235 de las 257 dicen
"Bloqueada" y solo 9 "Completado", cuando el proyecto lleva 138 cerradas. Leerla daria un
informe que contradice al cronograma. El estado se DERIVA de recorte y cierres.

POR QUE HACE FALTA EL DOCX ENTREGADO
------------------------------------
Es el unico registro de que 32 de las recortadas SI se hicieron antes de que el recorte las
dejara sin objeto: el Audio Mixer se creo y luego se descarto para no remedir la latencia, el
agarre de baquetas se implemento y murio cuando quedaron solidarias al control, la
investigacion musical se hizo y el alcance bajo a una pista. `cierres.CIERRES` no las tiene y
no puede tenerlas: por construccion solo cubre las 155 vivas.

Marcarlas solo como "fuera de alcance" haria que el documento nuevo contradijera al que la
docente ya tiene, con 32 tareas pasando de hechas a no hechas sin explicacion. Llevan los dos
hechos: se hicieron, y despues salieron del alcance.
"""
import datetime as D
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cierres
import recorte

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
HOJA = os.path.join(RAIZ, "referencia", "Hoja de control de tareas.xlsx")
ENTREGADO = os.path.join(RAIZ, "referencia",
                         "Lista_de_verificacion_compromisos_medio_curso.docx")

CORTE = D.date(2026, 11, 18)
FECHA_CORTE = "18 de noviembre de 2026"
FECHA_MEDIO_CURSO = "18 de septiembre de 2026"

TOTAL = 257

# Los cuatro estados posibles, en el orden en que se listan dentro de cada responsable.
#
# LAS VIVAS VAN PRIMERO porque son lo que se firma: lo hecho y lo que falta. Las que salieron
# del alcance van al final, que es donde no estorban a la lectura y siguen estando.
HECHO = "Hecho"
PENDIENTE = "Pendiente"
HECHO_FUERA = "Hecho · después fuera de alcance"
FUERA = "Fuera de alcance"

ESTADOS = [HECHO, PENDIENTE, HECHO_FUERA, FUERA]

# Correcciones al papel entregado, cada una con lo que la sostiene.
#
# Son defectos del documento de medio curso, no de la hoja de control: este modulo lee las
# tareas del xlsx, asi que los tres quedan corregidos por el solo hecho de leer el original.
# Se declaran para que el documento los nombre y la docente no tenga que encontrarlos.
CORRECCIONES = [
    ("AL.1", "responsable",
     "El papel entregado la lista con Sarai. La hoja de control la asigna a Kimberly, y es "
     "coherente: «Configurar iluminación inicial considerando la paleta de colores "
     "establecida» es del área de Entorno 3D, que lleva Kimberly. Sarai baja de 32 a 31 "
     "tareas y Kimberly sube de 31 a 32."),
    ("EB.3", "fecha de compromiso",
     "El papel entregado dice «7/09/f2a0lt2a6 sust»: la fecha 7/09/2026 quedó interleada "
     "con la observación de la hoja de control, «falta sustentar mas la investagacion sobre "
     "los juegos de ritmo». La fecha correcta es el 7/09/2026."),
    ("ML.1", "fecha de compromiso",
     "El papel entregado dice «7/09/2026 1», con un 1 de sobra. La fecha correcta es el "
     "7/09/2026."),
]

# Y una cuarta diferencia que no es un defecto, solo falta de formato: cuatro tareas llevaban
# el dia con cero delante y el resto no. Aqui todas salen con el mismo formato.
SIN_FORMATO = ["DP.1", "EB.1", "EO.1", "JA.1"]


# --------------------------------------------------------------- razones que no se sostienen
#
# LAS RAZONES DE `recorte.RECORTADAS` SE ESCRIBIERON PARA LEERSE EN ORDEN. En el documento 10
# van agrupadas por area, bajo un encabezado que ya trae el criterio, asi que «Misma razon» y
# «Depende de AB.1» funcionan: la de arriba esta a la vista.
#
# Aqui el anexo va alfabetico y cada fila se lee sola. «Depende de AB.1» obliga a buscar
# AB.1, y «Diseñar menu de configuracion» repite el texto de la tarea sin dar ningun motivo.
# Las dos cosas se arreglan sin tocar `recorte.py`, que es la fuente del documento 10 y
# cambiarla moveria aquel documento.

# Razones que remiten a otra actividad. Se resuelven pegando la razon de la que apuntan.
# `IS.3` dice «Depende de SC», que no es una clave: la que corresponde es SC.1.
REMITE_A = {
    "AB.2": "AB.1", "AB.4": "AB.1", "AB.5": "AB.1", "AB.6": "AB.1",
    # AC.2 dice «ya esta definida en ese documento» sin decir cual: es el de AC.1.
    "AC.2": "AC.1",
    "AD.2": "AD.1", "AE.2": "AE.1", "AE.3": "AE.1",
    "IS.3": "SC.1", "IS.4": "II.5", "JL.2": "JL.1",
    "JM.2": "JM.1", "JM.3": "JM.1", "JW.4": "JW.3", "QF.2": "QF.1",
    "SA.2": "SA.1", "SC.2": "SC.1", "SM.2": "SM.1",
}

# Razones que solo repiten el nombre de la tarea. Se les añade el motivo, sin quitar lo que
# ya decian. Cada una sale de una decision ya documentada del proyecto.
RAZON_AMPLIADA = {
    "AD.1": "Ninguna medida de éxito pide ambientación secundaria, y el claro de bosque "
            "de AP.1 ya quedó compuesto con assets libres",
    "AR.1": "La dirección artística propia se recortó con AE.3: no queda criterio artístico "
            "del equipo que cruzar con el responsable de experiencia emocional",
    "AR.2": "El escenario es un conjunto de assets libres ya integrados, no una ambientación "
            "propia en iteración",
    "IS.2": "No queda nada que configurar: los controles de volumen por canal se recortaron "
            "con SC.1 y ninguna medida los pide",
    "IS.5": "El menú sale por un pad rotulado SALIR que sale directo; una pantalla de "
            "confirmación no sirve a ninguna medida",
    "MB.2": "El alcance musical bajó a una sola pista, y el patrón se recortó a una nota "
            "por pulso para que fuera jugable con dos baquetas",
    "MR.1": "Se hizo, y el alcance musical bajó después a una sola pista: no queda "
            "catálogo que caracterizar",
    "MR.2": "Misma razón que MR.1: con una sola pista no hay referencias que comparar, y su "
            "BPM se fijó en MP.2",
    "MR.3": "Misma razón que MR.1: el compás y la subdivisión quedaron fijados al crear el "
            "patrón de la única pista",
    "MR.5": "Misma razón que MR.1: la duración es la de la pista que existe",
    "SA.1": "Ninguna medida de éxito pide ambiente sonoro, y una fuente más en el camino "
            "del audio toca el presupuesto de latencia, que es la medida 4",
    "SU": "Los pads del menú suenan con las muestras de la batería: no hace falta un banco "
          "de sonidos aparte",
}

# Riesgo que varias razones nombran sin explicar. Se declara una vez en el anexo.
R14 = ("R14 es la baja de un integrante del equipo. Su respuesta, aplicada el 17 de octubre, "
       "conservó del área de juego de ritmo las 15 actividades que sostienen un juego "
       "jugable y recortó el resto.")


def razon(clave):
    """La razon del recorte, en condiciones de leerse sola.

    Se amplia primero y se resuelve la referencia despues, para que la actividad que apunta a
    otra reciba la razon ya ampliada de aquella y no la escueta.
    """
    base = recorte.RECORTADAS[clave]
    if clave in RAZON_AMPLIADA:
        base = "%s. %s" % (base.rstrip(". "), RAZON_AMPLIADA[clave])
    destino = REMITE_A.get(clave)
    if destino:
        apoyo = recorte.RECORTADAS[destino]
        if destino in RAZON_AMPLIADA:
            apoyo = "%s. %s" % (apoyo.rstrip(". "), RAZON_AMPLIADA[destino])
        base = "%s — %s: %s" % (base.rstrip(". "), destino, apoyo)
    return base


def _normalizar(texto):
    return re.sub(r"\s+", " ", str(texto or "")).strip()


def _tareas_de_la_hoja():
    """Las 257 tareas del original: clave, texto, responsable, area y fecha de compromiso."""
    import openpyxl

    libro = openpyxl.load_workbook(HOJA, data_only=True)
    filas = list(libro["Tareas"].iter_rows(values_only=True))

    # LA CABECERA NO ESTA EN LA PRIMERA FILA. Se busca la que trae la columna `Clave` en vez
    # de suponer la fila 0, que en este archivo esta vacia.
    cab = next(i for i, f in enumerate(filas)
               if any(_normalizar(c) == "Clave" for c in f if c is not None))
    col = {_normalizar(n): i for i, n in enumerate(filas[cab]) if n is not None}

    tareas = {}
    for fila in filas[cab + 1:]:
        clave = _normalizar(fila[col["Clave"]])
        if not clave:
            continue
        fin = fila[col["Fecha de Termino"]]
        tareas[clave] = {
            "clave": clave,
            "tarea": _normalizar(fila[col["Tarea"]]),
            "responsable": _normalizar(fila[col["Responsable"]]),
            "area": _normalizar(fila[col["Area"]]),
            "compromiso": fin.strftime("%d/%m/%Y") if hasattr(fin, "strftime") else "",
            "observacion": _normalizar(fila[col["observaciones"]]),
        }
    return tareas


def _marcas_de_medio_curso():
    """Las claves que el papel entregado declara hechas, y el orden de sus secciones."""
    from docx import Document

    doc = Document(ENTREGADO)
    responsables = [p.text.replace("Responsable:", "").strip()
                    for p in doc.paragraphs if p.text.startswith("Responsable:")]

    hechas = set()
    for tabla in doc.tables:
        for fila in tabla.rows[1:]:
            celdas = [c.text.strip() for c in fila.cells]
            if celdas[3] == "✓":
                hechas.add(celdas[0])
    return hechas, responsables


def construir():
    """Las 257 tareas con su estado al corte. Cada una cae en uno y solo uno de los cuatro."""
    tareas = _tareas_de_la_hoja()
    hechas_medio_curso, orden = _marcas_de_medio_curso()

    assert len(tareas) == TOTAL, "la hoja de control trae %d tareas, no %d" % (
        len(tareas), TOTAL)

    for clave, t in tareas.items():
        recortada = clave in recorte.RECORTADAS
        cerrada = cierres.CIERRES.get(clave)

        if recortada and clave in hechas_medio_curso:
            t["estado"] = HECHO_FUERA
            t["razon"] = razon(clave)
            t["cerrada_el"] = ""
        elif recortada:
            t["estado"] = FUERA
            t["razon"] = razon(clave)
            t["cerrada_el"] = ""
        elif cerrada:
            t["estado"] = HECHO
            t["razon"] = cerrada[1]
            t["cerrada_el"] = cerrada[0]
        else:
            t["estado"] = PENDIENTE
            t["razon"] = ""
            t["cerrada_el"] = ""

        t["medio_curso"] = clave in hechas_medio_curso

    # UNA ACTIVIDAD CERRADA Y RECORTADA A LA VEZ SERIA UN DEFECTO, no un caso. `cierres` solo
    # cubre las vivas; si alguna apareciera en las dos, una de las dos tablas esta mal.
    cruce = sorted(set(cierres.CIERRES) & set(recorte.RECORTADAS))
    assert not cruce, "estas estan cerradas Y recortadas: %s" % cruce

    return tareas, orden


TAREAS, ORDEN_RESPONSABLES = construir()


def por_responsable():
    """Las tareas agrupadas por responsable, en el orden del papel entregado."""
    grupos = {r: [] for r in ORDEN_RESPONSABLES}
    for t in TAREAS.values():
        grupos.setdefault(t["responsable"], []).append(t)

    def orden(t):
        return (ESTADOS.index(t["estado"]), t["compromiso"][3:], t["compromiso"][:2],
                t["clave"])

    return {r: sorted(g, key=orden) for r, g in grupos.items() if g}


def cuenta(tareas):
    return {e: sum(1 for t in tareas if t["estado"] == e) for e in ESTADOS}


def resumen():
    c = cuenta(TAREAS.values())
    c["total"] = len(TAREAS)
    c["hechas_medio_curso"] = sum(1 for t in TAREAS.values() if t["medio_curso"])
    c["vigentes"] = c[HECHO] + c[PENDIENTE]
    c["recortadas"] = c[FUERA] + c[HECHO_FUERA]
    # Avance nuevo que el papel de medio curso no reportaba.
    c["cerradas_despues"] = sum(1 for t in TAREAS.values()
                                if t["estado"] == HECHO and not t["medio_curso"])
    return c


def fuera_de_alcance():
    """Las recortadas con su razon, para el anexo. Ordenadas por clave."""
    return sorted((t for t in TAREAS.values() if t["estado"] in (FUERA, HECHO_FUERA)),
                  key=lambda t: t["clave"])


if __name__ == "__main__":
    r = resumen()
    print("Corte: %s" % FECHA_CORTE)
    for e in ESTADOS:
        print("  %-34s %3d" % (e, r[e]))
    print("  %-34s %3d" % ("TOTAL", r["total"]))
    print()
    print("Hechas en el papel de medio curso:   %3d" % r["hechas_medio_curso"])
    print("Cerradas desde entonces:             %3d" % r["cerradas_despues"])
    print("Alcance vigente (hechas+pendientes): %3d" % r["vigentes"])
    print("Fuera de alcance:                    %3d" % r["recortadas"])
    print()
    for resp, tareas in por_responsable().items():
        c = cuenta(tareas)
        print("%-10s %3d tareas · %d hechas, %d pendientes, %d fuera de alcance (%d de ellas hechas)"
              % (resp, len(tareas), c[HECHO], c[PENDIENTE], c[FUERA] + c[HECHO_FUERA],
                 c[HECHO_FUERA]))
