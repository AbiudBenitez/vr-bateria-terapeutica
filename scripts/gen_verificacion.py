# -*- coding: utf-8 -*-
"""Genera el documento 19: la lista de verificacion de compromisos, al corte del 18-nov.

Mismo papel que el entregado a medio curso —las 257 tareas por responsable, con su fecha de
compromiso y espacio para firmar— con la columna de estado puesta al dia y las que salieron
del alcance declaradas como tales.

    python3 scripts/gen_verificacion.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import neutro
import verificacion as V

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")
DOC = os.path.join(SALIDA, "19_Lista_de_Verificacion_Compromisos.docx")

# Anchos en cm. En horizontal con margen de 1.5 quedan 24.9 cm utiles.
COLS = [1.5, 9.0, 2.3, 4.0, 5.0, 3.0]
COLS_ANEXO = [1.5, 8.0, 4.0, 11.3]

CABECERA = ["Clave", "Tarea", "Fecha compromiso", "Estado",
            "Firma de recibido", "Fecha recibida"]

QUE_SIGNIFICA = [
    (V.HECHO,
     "Terminada y con evidencia en el repositorio: un commit, un entregable o una medición "
     "con su archivo. La fecha entre paréntesis es la del cierre real, no la del plan."),
    (V.PENDIENTE,
     "Sigue dentro del alcance y sigue sin hacerse. Es lo único que esta firma compromete "
     "hacia adelante."),
    (V.HECHO_FUERA,
     "Se hizo, y el recorte de alcance del 18 de octubre la dejó después sin objeto. "
     "Estaba marcada como hecha en el documento de medio curso y lo sigue estando aquí. "
     "La razón del recorte va en el anexo A."),
    (V.FUERA,
     "El recorte de alcance la sacó del proyecto antes de empezarla. No se hizo y no se va "
     "a hacer. La razón de cada una va en el anexo A."),
]


def _fila(t):
    estado = t["estado"]
    if estado == V.HECHO and t["cerrada_el"]:
        aaaa, mm, dd = t["cerrada_el"].split("-")
        estado = "%s (%s/%s/%s)" % (V.HECHO, dd, mm, aaaa)
    return [t["clave"], t["tarea"], t["compromiso"], estado, "", ""]


def doc():
    r = V.resumen()
    grupos = V.por_responsable()

    d = neutro.nuevo()
    neutro.portada(
        d,
        "Lista de verificación de compromisos",
        "Simulación de Batería en Realidad Virtual con Enfoque Terapéutico",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Institución", "UANL · Facultad de Ingeniería Mecánica y Eléctrica"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha de corte", V.FECHA_CORTE),
         ("Tareas", "%d, las de la hoja de control del proyecto" % r["total"]),
         ("Sustituye a", "la lista entregada a medio curso, del %s" % V.FECHA_MEDIO_CURSO)],
        sub2="Estado de las %d tareas al %s" % (r["total"], V.FECHA_CORTE))

    # ------------------------------------------------------------------ 1
    neutro.H(d, "1. Qué cambia respecto a la lista de medio curso")
    neutro.P(d,
             "A medio curso se entregó esta misma lista con %d tareas marcadas como hechas "
             "y el resto como pendientes. Desde entonces pasaron dos cosas que aquel papel no "
             "podía recoger, y son las que explican todas las diferencias entre uno y otro."
             % r["hechas_medio_curso"])

    neutro.P(d,
             "La primera es el recorte de alcance del 18 de octubre, documentado en "
             "«10_Recorte_de_Alcance.docx». El criterio fue uno solo: sobrevive lo que sirve a "
             "una medida de éxito de la carta sponsor, y se recorta lo que no sirve a "
             "ninguna. %d de las %d tareas quedaron fuera. Dejarlas en la lista como "
             "pendientes equivaldría a firmar un compromiso de hacer trabajo que el proyecto "
             "decidió no hacer, con la razón escrita de cada caso."
             % (r["recortadas"], r["total"]))

    neutro.P(d,
             "La segunda es el avance: %d tareas más cerraron después de aquel corte y no "
             "aparecían marcadas. El alcance vigente son %d tareas, de las cuales %d están "
             "terminadas y %d siguen abiertas."
             % (r["cerradas_despues"], r["vigentes"], r[V.HECHO], r[V.PENDIENTE]))

    neutro.P(d,
             "De las %d que salieron del alcance, %d ya se habían hecho y el recorte las "
             "dejó sin objeto después: el Audio Mixer se construyó y luego se descartó "
             "para no tener que volver a medir la latencia, el agarre de las baquetas se "
             "implementó y murió cuando quedaron solidarias al control por el presupuesto de "
             "latencia, y la investigación musical se completó antes de que el alcance "
             "bajara a una sola pista. Esas %d conservan aquí la marca de hechas que ya "
             "tenían, con el recorte declarado al lado. No se retira trabajo reportado."
             % (r["recortadas"], r[V.HECHO_FUERA], r[V.HECHO_FUERA]))

    # ------------------------------------------------------------------ 2
    neutro.H(d, "2. Qué significa cada estado")
    neutro.table(d, ["Estado", "Cuántas", "Qué quiere decir"],
                 [[e, r[e], texto] for e, texto in QUE_SIGNIFICA],
                 widths=[4.2, 1.8, 9.5], fs=9.5)

    neutro.P(d,
             "Los cuatro estados reparten las %d tareas sin solaparse y sin dejar ninguna "
             "fuera: %d + %d + %d + %d = %d."
             % (r["total"], r[V.HECHO], r[V.PENDIENTE], r[V.HECHO_FUERA], r[V.FUERA],
                r["total"]))

    # ------------------------------------------------------------------ 3
    neutro.H(d, "3. Resumen por responsable")
    filas = []
    for resp, tareas in grupos.items():
        c = V.cuenta(tareas)
        filas.append([resp, len(tareas), c[V.HECHO], c[V.PENDIENTE],
                      c[V.HECHO_FUERA], c[V.FUERA]])
    filas.append(["TOTAL", r["total"], r[V.HECHO], r[V.PENDIENTE],
                  r[V.HECHO_FUERA], r[V.FUERA]])
    neutro.table(d, ["Responsable", "Tareas", "Hechas", "Pendientes",
                     "Hechas y fuera de alcance", "Fuera de alcance"],
                 filas, widths=[3.2, 1.8, 1.8, 2.2, 3.4, 2.6], fs=9.5,
                 negritas_col0=True)

    pendientes = [t for t in V.TAREAS.values() if t["estado"] == V.PENDIENTE]
    duenos = sorted({t["responsable"] for t in pendientes})
    neutro.P(d,
             "Las %d tareas abiertas están todas en %s, y todas son del área de QA, "
             "documentación y gestión: pruebas con usuarios, registro de errores, informe "
             "final, build definitiva y presentación. Las siete áreas técnicas cerraron lo "
             "que les quedaba dentro del alcance."
             % (r[V.PENDIENTE], " y ".join(duenos)))

    # ------------------------------------------------------------------ 4
    neutro.H(d, "4. Lo que queda abierto")
    neutro.P(d,
             "Es a lo que compromete esta firma. Ninguna otra tarea de las %d sigue "
             "pendiente." % r["total"])
    neutro.table(d, ["Clave", "Tarea", "Responsable", "Fecha compromiso"],
                 [[t["clave"], t["tarea"], t["responsable"], t["compromiso"]]
                  for t in sorted(pendientes, key=lambda x: (x["compromiso"][3:],
                                                             x["compromiso"][:2],
                                                             x["clave"]))],
                 widths=[1.6, 9.0, 2.4, 2.6], fs=9.5)

    # ------------------------------------------------------------------ 5
    neutro.H(d, "5. Correcciones a la lista entregada")
    neutro.P(d,
             "Tres datos del papel de medio curso no coincidían con la hoja de control del "
             "proyecto. Aquí salen corregidos, porque las tareas se leen directamente del "
             "original. Se nombran para que la diferencia entre los dos documentos no quede "
             "sin explicación.")
    neutro.table(d, ["Clave", "Qué estaba mal", "Corrección"],
                 [[k, campo, razon] for k, campo, razon in V.CORRECCIONES],
                 widths=[1.6, 2.8, 11.1], fs=9.5)
    neutro.P(d,
             "Además, cuatro tareas (%s) llevaban la fecha con el día escrito de dos formas "
             "distintas. Aquí todas las fechas salen en el mismo formato dd/mm/aaaa. El texto "
             "de las %d tareas, su agrupamiento y sus fechas de compromiso son los de la hoja "
             "de control, sin un solo cambio."
             % (", ".join(V.SIN_FORMATO), r["total"]))

    # ------------------------------------------------------------------ las tablas
    neutro.H(d, "6. Verificación por responsable")
    neutro.P(d,
             "En cada sección las tareas van agrupadas por estado, en este orden: hechas, "
             "pendientes, hechas y después fuera de alcance, y fuera de alcance. Dentro de "
             "cada grupo, por fecha de compromiso.")

    neutro.landscape(d)

    for resp, tareas in grupos.items():
        c = V.cuenta(tareas)
        neutro.H(d, "Responsable: %s" % resp, lvl=2)
        neutro.P(d,
                 "%d tareas · %d hechas · %d pendientes · %d fuera de alcance, %d de ellas "
                 "hechas antes del recorte."
                 % (len(tareas), c[V.HECHO], c[V.PENDIENTE],
                    c[V.HECHO_FUERA] + c[V.FUERA], c[V.HECHO_FUERA]),
                 size=10, after=6)
        neutro.table(d, CABECERA, [_fila(t) for t in tareas], widths=COLS, fs=8.5)

    # ------------------------------------------------------------------ firma
    neutro.portrait(d)
    neutro.H(d, "7. Validación")
    neutro.P(d,
             "Con mi firma doy por válido el estado de las %d tareas reportado en este "
             "documento al %s: %d hechas, %d pendientes y %d fuera del alcance del proyecto "
             "por el recorte del 18 de octubre de 2026, de las cuales %d se habían hecho "
             "antes de quedar fuera."
             % (r["total"], V.FECHA_CORTE, r[V.HECHO], r[V.PENDIENTE], r["recortadas"],
                r[V.HECHO_FUERA]))
    for _ in range(3):
        d.add_paragraph()
    neutro.P(d, "_________________________________________")
    neutro.P(d, "Firma de la encargada del proyecto", size=10)
    neutro.P(d, "Fecha de firma: _______________", size=10)

    # ------------------------------------------------------------------ anexo A
    neutro.landscape(d)
    neutro.H(d, "Anexo A. Las %d tareas fuera de alcance, con su razón" % r["recortadas"])
    neutro.P(d,
             "Una por una, con el motivo por el que el recorte del 18 de octubre la sacó del "
             "proyecto. El desarrollo completo del criterio y de sus efectos está en "
             "«10_Recorte_de_Alcance.docx».", size=10)
    neutro.P(d,
             "Varias razones nombran R14. %s Otras remiten a la actividad de la que dependían, "
             "y en esas la razón de aquella va a continuación, después del guión."
             % V.R14, size=10)
    neutro.table(d, ["Clave", "Tarea", "Estado", "Razón del recorte"],
                 [[t["clave"], t["tarea"], t["estado"], t["razon"]]
                  for t in V.fuera_de_alcance()],
                 widths=COLS_ANEXO, fs=8.5)

    return d


if __name__ == "__main__":
    d = doc()
    d.save(DOC)
    r = V.resumen()
    print("Escrito %s" % DOC)
    print("  %d tareas: %d hechas, %d pendientes, %d hechas y fuera, %d fuera"
          % (r["total"], r[V.HECHO], r[V.PENDIENTE], r[V.HECHO_FUERA], r[V.FUERA]))
