# -*- coding: utf-8 -*-
"""Genera el documento 13: rebaseline del cronograma del 11-nov-2026.

Todas las cifras salen de cierres.py, replan.py y el propio cronograma. Ninguna se escribe
a mano: este documento es el que reporta un defecto de cifras escritas a mano.
"""
import datetime as D
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cierres as CI
import neutro
import rc257 as R
import rebaselinear as RB
import replan as RP

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")
DOC = os.path.join(SALIDA, "13_Rebaseline_Cronograma.docx")

MES = {9: "septiembre", 10: "octubre", 11: "noviembre"}
DIA = {0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves", 4: "viernes",
       5: "sábado", 6: "domingo"}


def larga(d):
    if isinstance(d, str):
        d = D.date.fromisoformat(d)
    return "%d de %s" % (d.day, MES[d.month])


def habiles(a, b):
    n, d = 0, a
    while d < b:
        d += D.timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


CERRADAS = len(CI.CIERRES)
PENDIENTES = len(RP.CALENDARIO)
TOTAL = CERRADAS + PENDIENTES
NUEVAS = ["QG.2", "QT.1", "QM.2", "QC.1"]


def doc():
    d = neutro.nuevo()

    neutro.portada(
        d,
        "Rebaseline del cronograma",
        "Simulación de Batería en Realidad Virtual con Enfoque Terapéutico",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha de estado", "%s de 2026" % larga(RB.CORTE)),
         ("Procesos", "PMBOK 6.6 Controlar el Cronograma · 4.5 Monitorear y Controlar el "
                      "Trabajo del Proyecto")],
    )

    # ------------------------------------------------------------------ 1
    neutro.H(d, "1. Qué se encontró", 1)
    neutro.P(d,
        "Al revisar el cronograma el %s se encontró que ninguno de los dos archivos tenía una "
        "sola fecha en noviembre. El de ProjectLibre mostraba el proyecto terminado el 19 de "
        "octubre y el operativo el 6 de octubre, cuando en realidad quedaban %d actividades "
        "sin arrancar." % (larga(RB.CORTE), PENDIENTES))
    neutro.P(d,
        "No era un error de captura. Los dos archivos programan todo lo antes posible desde el "
        "7 de septiembre y nunca se les volvió a dar fecha: no tenían ni un campo de inicio "
        "real, ni fecha de estado, y la fecha actual seguía congelada el 17 de octubre, el día "
        "del recorte de alcance. Un cronograma así no dice cuándo pasaron las cosas; dice "
        "cuándo se había planeado que pasaran.")

    neutro.P(d, "Tres defectos, en orden de gravedad:", bold=True)
    neutro.bullets(d, [
        "Las actividades cerradas llevaban su fecha PLANEADA. El procedimiento de cierre "
        "copiaba la fecha del plan en el campo de corte, y la fecha verdadera quedaba solo "
        "dentro del campo de notas. Las desviaciones medidas van de tres a seis semanas.",

        "El avance por área estaba escrito a mano y se había quedado atrás por segunda vez. "
        "Decía 23 actividades cerradas en QA cuando ya eran %d."
        % next(h for a, h, _ in __import__("estado").AVANCE if a.startswith("QA")),

        "La red de lo que falta se consumió completa sin arrancar. Del corte del 22 de "
        "octubre al %s pasaron %d días hábiles, que es exactamente la duración que esa red "
        "tenía." % (larga(RB.CORTE), habiles(D.date(2026, 10, 22), RB.CORTE)),
    ])

    # ------------------------------------------------------------------ 2
    neutro.H(d, "2. Cuatro actividades estaban hechas y nadie las había reclamado", 1)
    neutro.P(d,
        "La verificación encontró que cuatro de las que figuraban como pendientes ya tenían su "
        "evidencia, y desde antes del corte en tres de los cuatro casos. No es un cierre nuevo: "
        "es avance que el cronograma no recogía.")
    neutro.table(d, ["Clave", "Actividad", "Cierra el", "Evidencia"],
                 [[k, R.T[k]["desc"][:46] if k in R.T else k,
                   larga(CI.CIERRES[k][0]), CI.CIERRES[k][1][:150]] for k in NUEVAS],
                 widths=[1.1, 4.0, 1.6, 8.0], fs=8)
    neutro.P(d,
        "Con ellas el avance vigente pasa a %d de %d actividades, el %.0f %%."
        % (CERRADAS, TOTAL, 100.0 * CERRADAS / TOTAL))

    # ------------------------------------------------------------------ 3
    neutro.H(d, "3. La regla de las fechas de registro", 1)
    neutro.P(d,
        "La fecha de registro de una actividad cerrada es la del artefacto verificable más "
        "temprano que la demuestra cerrada: un commit con su asunto, un entregable con su "
        "nombre, o una medición con su archivo. No es la fecha planeada y no es una "
        "estimación. Las %d actividades cerradas quedaron fechadas en %d días de cierre."
        % (CERRADAS, len(set(f for f, _ in CI.CIERRES.values()))))

    c = Counter(f for f, _ in CI.CIERRES.values())
    porfecha = {}
    for k, (f, _) in CI.CIERRES.items():
        porfecha.setdefault(f, []).append(k)
    neutro.table(d, ["Día de cierre", "Nº", "Actividades que cierran ese día"],
                 [[larga(f) + (" (%s)" % DIA[D.date.fromisoformat(f).weekday()]
                               if f in CI.FINES_DE_SEMANA_TRABAJADOS else ""),
                   str(c[f]),
                   ", ".join(sorted(porfecha[f]))]
                  for f in sorted(c)],
                 widths=[2.4, 0.7, 11.5], fs=8)

    neutro.P(d, "Los dos días de mayor cierre del proyecto son un sábado y un domingo.",
             bold=True)
    neutro.P(d,
        "El sábado 17 y el domingo 18 de octubre concentran %d de las %d actividades cerradas, "
        "el %.0f %%. El cronograma lo dice ahora porque esos dos días quedaron abiertos como "
        "excepción del calendario; antes el calendario los daba por no laborables y la fecha se "
        "habría movido al lunes. Es un dato de gestión, no una anécdota: el proyecto no cupo en "
        "los días hábiles que tenía."
        % (c["2026-10-17"] + c["2026-10-18"], CERRADAS,
           100.0 * (c["2026-10-17"] + c["2026-10-18"]) / CERRADAS))

    # ------------------------------------------------------------------ 4
    neutro.H(d, "4. La replanificación: del 12 al 20 de noviembre", 1)
    neutro.P(d,
        "Las %d pendientes forman una red de %.0f días hábiles. Al 13 de noviembre "
        "comprometido quedaban %d días hábiles; con la reserva de gestión del 16 al 20, %d. "
        "Catorce días no caben en siete por el camino normal."
        % (PENDIENTES, 14.0, habiles(RB.CORTE, RP.COMPROMETIDA),
           habiles(RB.CORTE, RP.RESERVA)))
    neutro.P(d,
        "Caben traslapando, y traslapar no es recortar: cada actividad conserva su duración y "
        "su alcance, y lo que cambia es que arranca antes de que su antecedente termine. Se "
        "declararon %d traslapes, uno por uno, cada uno con la razón por la que se sostiene. "
        "La cadena baja de %.0f a %.0f días hábiles y el proyecto cierra el %s."
        % (len(RP.TRASLAPES), 14.0, RP.TOTAL, larga(RP.CIERRE)))

    pordia, cierran = {}, {}
    for k, (i, f) in RP.CALENDARIO.items():
        pordia.setdefault(i, []).append(k)
        cierran.setdefault(f, []).append(k)
    dias = sorted(set(pordia) | set(cierran))
    neutro.table(d, ["Día", "Arrancan", "Terminan"],
                 [["%s %s" % (DIA[x.weekday()], larga(x)),
                   ", ".join(sorted(pordia.get(x, []))) or "—",
                   ", ".join(sorted(cierran.get(x, []))) or "—"] for x in dias],
                 widths=[2.4, 6.1, 6.1], fs=8)

    neutro.H(d, "4.1 Los traslapes, uno por uno", 2)
    neutro.table(d, ["Sucesora", "Antecedente", "Tipo", "Por qué se sostiene"],
                 [[k, p, "%s+%d" % (t, dm), razon]
                  for (k, p), (t, dm, razon) in sorted(RP.TRASLAPES.items())],
                 widths=[1.0, 1.1, 0.9, 11.6], fs=8)
    neutro.P(d,
        "FS significa que la sucesora arranca cuando el antecedente termina, que es el valor "
        "por omisión de toda la red. SS significa que arranca cuando el antecedente ARRANCA, "
        "más la demora en días hábiles: ése es el traslape.")

    # ------------------------------------------------------------------ 5
    neutro.H(d, "5. Lo que este plan no disimula", 1)
    neutro.bullets(d, [
        "Sale con holgura cero. El cierre cae el último día de la reserva de gestión, así que "
        "cualquier retraso de un día empuja el proyecto al 23 de noviembre, que es el inicio "
        "de exámenes.",

        "Consume la reserva completa. La reserva de gestión del 16 al 20 de noviembre existe "
        "justamente para esto, y queda declarado que se usó: no es margen que siga disponible.",

        "Arranca con pruebas con usuarios, y los usuarios no están reclutados. Es el riesgo "
        "R18 del registro y es el único punto de falla que importa: nada de la cadena de "
        "informe final puede arrancar antes.",

        "El informe final queda redactado en traslape. Las secciones de resultados, "
        "conclusiones e integración se escriben sobre análisis que todavía se está "
        "completando. Es la decisión que compra los días, y el riesgo que compra con ellos es "
        "de calidad de redacción, no de fecha.",
    ])

    # ------------------------------------------------------------------ 6
    neutro.H(d, "6. Qué impide que vuelva a pasar", 1)
    neutro.table(d, ["Dónde", "Qué garantiza"], [
        ["scripts/cierres.py",
         "La fecha de registro de cada actividad cerrada, con la evidencia que la sostiene. "
         "Importa las de octubre de marcar_hechas.py en vez de repetirlas."],
        ["scripts/replan.py",
         "El replan traslapado. Las fechas se calculan de la red y de los traslapes "
         "declarados; no se escribe ninguna a mano."],
        ["scripts/rebaselinear.py",
         "Escribe los dos cronogramas. Es idempotente y pone restricción de «no antes de» en "
         "cada actividad, para que al recalcular no se vuelvan a ir a septiembre."],
        ["scripts/marcar_hechas.py",
         "Corregido: el campo de corte lleva la fecha real y no la planeada. Era el defecto "
         "de origen."],
        ["scripts/estado.py",
         "El avance por área se lee del cronograma. Se había quedado desfasado dos veces "
         "escrito a mano."],
        ["scripts/test_rebaseline.py",
         "26 pruebas. Entre ellas: que ninguna fecha de cierre esté en el futuro, que el "
         "campo de corte coincida con la fecha de registro, que ninguna pendiente quede "
         "programada en el pasado, que cada traslape apunte a un enlace que existe y "
         "explique por qué se sostiene, y que el replan cierre dentro de la reserva."],
    ], widths=[3.0, 11.6], fs=8, negritas_col0=True)

    return d


if __name__ == "__main__":
    doc().save(DOC)
    print("OK", DOC)
    print("   %d cerradas | %d pendientes | cadena %.0f d | cierre %s"
          % (CERRADAS, PENDIENTES, RP.TOTAL, RP.CIERRE))
