# -*- coding: utf-8 -*-
"""Genera el documento de estado del proyecto."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estado
import neutro

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")


def doc():
    d = neutro.nuevo()

    neutro.portada(
        d,
        "Estado del proyecto",
        "Simulación de Batería en Realidad Virtual con Enfoque Terapéutico",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha", estado.FECHA),
         ("Procesos", "PMBOK 4.5 Monitorear y Controlar · 4.6 Control Integrado de Cambios")],
    )

    # ---------------------------------------------------------------- 1
    neutro.H(d, "1. Para qué existe este documento", 1)
    neutro.P(d,
             "Los once documentos anteriores son correctos y siguen vigentes, pero cada uno "
             "responde a su momento: la carta sponsor es de septiembre, el recorte de alcance "
             "del 17 de octubre, el cambio de enfoque del 18. Tres de ellos reorientan lo que "
             "dicen los anteriores, de modo que leerlos en orden no reconstruye el proyecto.")
    neutro.P(d,
             "Este reúne el estado VIGENTE y dice qué documento tiene el detalle de cada cosa. "
             "No repite su contenido: remite a él.")
    neutro.P(d,
             "Las cifras no están escritas a mano. Salen del cronograma y de los archivos de "
             "medición del visor, y hay pruebas automatizadas que comprueban que cuadran. Un "
             "documento de estado con números tecleados queda desfasado el mismo día, y lo "
             "peor es que nadie sabe cuándo dejó de ser cierto.", italic=True)

    # ---------------------------------------------------------------- 2
    neutro.H(d, "2. Qué es el proyecto hoy", 1)
    neutro.P(d,
             "Una simulación de batería en realidad virtual para Meta Quest, construida como "
             "herramienta de regulación emocional por medio de la ejecución rítmica. El "
             "usuario golpea pads virtuales con los controles, el sistema responde con sonido "
             "y vibración, y un juego de ritmo guía qué tocar y cuándo.")
    neutro.P(d,
             "El proyecto mide lo que afirma. Cada sesión exporta la precisión temporal del "
             "jugador y la constancia de su pulso, y esos datos son los que sostienen las "
             "medidas de éxito en lugar de una impresión.")

    # ---------------------------------------------------------------- 3
    neutro.H(d, "3. Las tres decisiones que lo reorientaron", 1)
    neutro.P(d,
             "Ninguna de las tres fue un cambio de rumbo improvisado. Dos estaban previstas en "
             "el plan de riesgos y la tercera corrige un supuesto que el proyecto no podía "
             "sostener.")

    for i, dec in enumerate(estado.DECISIONES, 1):
        neutro.H(d, f"3.{i} {dec['titulo']}", 2)
        neutro.campo(d, "Cuándo", dec["cuando"])
        neutro.campo(d, "Detalle en", dec["doc"])
        neutro.P(d, "Causa", bold=True, after=2)
        neutro.P(d, dec["causa"])
        neutro.P(d, "Efecto", bold=True, after=2)
        neutro.P(d, dec["efecto"])
        neutro.P(d, "Lo que deja para la próxima vez", bold=True, after=2)
        neutro.P(d, dec["leccion"], italic=True)

    # ---------------------------------------------------------------- 4
    neutro.H(d, "4. Las medidas de éxito", 1)
    neutro.P(d,
             "La carta sponsor comprometió diez resultados verificables. Es contra esto, y no "
             "contra un número de tareas, como se juzga si el proyecto cumplió.")
    neutro.table(
        d, ["#", "Medida", "Estado", "Evidencia"],
        [[str(n), t, e, ev] for n, t, e, ev in estado.MEDIDAS],
        widths=[0.8, 3.2, 1.6, 9.9], fs=8.5)
    neutro.P(d)
    cerradas = sum(1 for _, _, e, _ in estado.MEDIDAS if e == "cerrada")
    neutro.P(d,
             f"{cerradas} cerradas con evidencia medida, 1 en curso a falta de las pruebas con "
             "usuarios, y 1 retirada formalmente. La retirada es la 8: sin asesor externo no "
             "hay dictamen, y una medida que no se puede verificar por ningún camino no se "
             "sostiene dejándola abierta.")

    # ---------------------------------------------------------------- 5
    neutro.H(d, "5. Avance", 1)
    filas = [[a, str(h), str(p), str(h + p),
              f"{100.0 * h / max(1, h + p):.0f} %"] for a, h, p in estado.AVANCE]
    th = sum(h for _, h, _ in estado.AVANCE)
    tp = sum(p for _, _, p in estado.AVANCE)
    filas.append(["TOTAL", str(th), str(tp), str(th + tp), f"{100.0 * th / (th + tp):.0f} %"])
    neutro.table(d, ["Área", "Hechas", "Faltan", "Total", "Avance"], filas,
                 widths=[5.5, 2.2, 2.2, 2.2, 2.4], fs=9.0)
    neutro.P(d)
    pend_q = next(p for a, _, p in estado.AVANCE if a.startswith("QA"))
    pend_tot = sum(p for _, _, p in estado.AVANCE)
    neutro.P(d,
             f"Seis de las ocho áreas están cerradas. De las {pend_tot} actividades "
             f"pendientes, {pend_q} son de QA, documentación y gestión: el "
             f"{100.0 * pend_q / max(1, pend_tot):.0f} %. Al cerrarse interfaz y sonido la "
             "concentración empeoró en proporción aunque bajara en número absoluto. Es la "
             "misma concentración que el análisis de ruta crítica señaló en septiembre, y la "
             "baja del riesgo R14 la agravó al dejar la dirección y la coordinación dentro "
             "de QA.")

    # ---------------------------------------------------------------- 6
    neutro.H(d, "6. Hitos alcanzados", 1)
    neutro.P(d,
             "Un hito no es una tarea terminada: es un punto a partir del cual el proyecto "
             "puede hacer algo que antes no podía. Por eso cada uno dice qué habilita y no "
             "solo qué se hizo. De las "
             f"{sum(h for _, h, _ in estado.AVANCE) + pend_tot} actividades del cronograma "
             f"hay {sum(h for _, h, _ in estado.AVANCE)} cerradas; estos son los "
             f"{len(estado.HITOS)} momentos en que el proyecto cambió de estado.")
    neutro.P(d)
    neutro.P(d,
             "Las fechas son las de la evidencia, no las del plan. El hito de latencia estaba "
             "fechado en la semana 4, el 25 de septiembre, y se cerró el 17 de octubre: tres "
             "semanas tarde. Ponerlo en su fecha real es lo que permite ver dónde se gastó la "
             "holgura.")
    neutro.table(d, ["Fecha", "Hito", "Qué habilita", "Evidencia"],
                 [[f, t, q, e] for f, t, q, e in estado.HITOS],
                 widths=[1.5, 3.3, 5.0, 5.7], fs=8.0)
    neutro.P(d)
    neutro.P(d,
             "El cronograma marca además 21 hitos formales de duración cero, de los que 17 "
             "están cerrados. Conviene revisarlos tras cada guardado desde ProjectLibre: la "
             "herramienta deriva el porcentaje de la duración, así que un hito sin duración "
             "vuelve a cero solo. Para eso está scripts/hitos.py.")

    # ---------------------------------------------------------------- 7
    neutro.H(d, "7. Qué hace el prototipo", 1)
    neutro.table(d, ["Pieza", "Estado verificado"],
                 [[a, b] for a, b in estado.PROTOTIPO],
                 widths=[4.2, 11.3], fs=9.0)

    # ---------------------------------------------------------------- 7
    neutro.H(d, "8. Lo que queda, por riesgo", 1)
    neutro.table(d, ["Bloque", "Riesgo", "Qué falta", "Responsable"],
                 [[a, b, c, e] for a, b, c, e in estado.PENDIENTE],
                 widths=[3.4, 1.4, 8.0, 2.7], fs=8.5)

    # ---------------------------------------------------------------- 8
    neutro.H(d, "9. Riesgos vivos", 1)
    neutro.table(d, ["Riesgo", "Nivel", "Situación y mitigación"],
                 [[a, b, c] for a, b, c in estado.RIESGOS],
                 widths=[3.6, 1.4, 10.5], fs=8.5)

    # ---------------------------------------------------------------- 9
    neutro.H(d, "10. Dónde está cada cosa", 1)
    neutro.P(d,
             "Los doce documentos del proyecto y qué responde cada uno. Los marcados como "
             "vigentes con sustituciones siguen valiendo: lo que cambió está en el documento "
             "11, no reescrito encima del original.")
    neutro.table(d, ["Documento", "Qué contiene"],
                 [[a, b] for a, b in estado.DOCUMENTOS],
                 widths=[5.0, 10.5], fs=8.5)

    # ---------------------------------------------------------------- 10
    neutro.H(d, "11. Firmas", 1)
    neutro.P(d,
             "Con la firma de este documento el equipo deja constancia del estado del proyecto "
             "a la fecha indicada.")
    neutro.P(d)
    neutro.table(d, ["Rol", "Nombre", "Firma"],
                 [["Patrocinadora", "Dra. Leticia Amalia Neira Tovar", "_" * 26],
                  ["Dirección de proyecto", "Sarai Galindo García", "_" * 26],
                  ["Gerencia de proyecto", "Abiud Misael Benítez Franco", "_" * 26],
                  ["QA y documentación", "Diana Laura Tello Salinas", "_" * 26],
                  ["Entorno 3D", "Kimberly González Sepúlveda", "_" * 26],
                  ["Sonido", "Christian Salvador Valadez Gallegos", "_" * 26],
                  ["Música", "Javier Alejandro Hernández Caloca", "_" * 26],
                  ["Experiencia emocional", "María Fernanda Montoya Valdez", "_" * 26]],
                 widths=[4.4, 6.6, 5.0], fs=9.0)

    ruta = os.path.join(SALIDA, "12_Estado_del_Proyecto.docx")
    d.save(ruta)
    return ruta


if __name__ == "__main__":
    print(doc())
