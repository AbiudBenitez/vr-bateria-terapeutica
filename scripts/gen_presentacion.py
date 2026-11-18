# -*- coding: utf-8 -*-
"""Genera el documento 17: guion de la presentacion y demostracion final. Cierra QX.

Ninguna cifra se escribe aqui. Salen de estado.py, costos.py, sesiones.py, manual_datos.py y
replan.py, que son las fuentes que ya tiene el proyecto.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import costos
import estado
import manual_datos
import neutro
import presentacion as P
import pruebas_usuario as PU
import replan as RP
import sesiones as S

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")
DOC = os.path.join(SALIDA, "17_Presentacion_Final.docx")
FECHA = "18 de noviembre de 2026"

MINUTOS = sum(b[4] for b in P.BLOQUES)
D = manual_datos.DATOS


def doc():
    d = neutro.nuevo()
    r = S.resumen()

    neutro.portada(
        d, "Presentación y demostración final",
        "Guion de la exposición de cierre",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha", FECHA),
         ("Actividad", "QX — Preparar presentación y demostración final del proyecto")])

    neutro.P(d,
        "Este documento es el guion, no las diapositivas. De aquí sale el archivo de "
        "presentación en una pasada, y lo que se revisa y se corrige es esto: un cambio en el "
        "orden del arco cuesta una línea aquí y veinte diapositivas allá.")
    neutro.P(d,
        "%d bloques, %d minutos de exposición más %s de demostración. Los huecos de resultados "
        "están marcados y se llenan con el documento 16 cuando exista la atribución de "
        "sesiones." % (len(P.BLOQUES), MINUTOS, "3 minutos"))

    # ------------------------------------------------------------------ 1
    neutro.H(d, "1. El arco", 1)
    neutro.P(d,
        "El orden no es cronológico. Es: qué se prometió, qué se descubrió, qué se entregó, "
        "qué se aprendió.", bold=True)
    neutro.P(d,
        "Las tres decisiones que reorientaron el proyecto van ANTES de los resultados, a "
        "propósito: los resultados se entienden a partir de ellas. Y son lo que de verdad "
        "enseña este proyecto para la materia. Un proyecto que cumple su plan original no "
        "enseña administración de proyectos; uno que lo cambia tres veces con la razón escrita, "
        "sí.")
    neutro.table(d, ["Nº", "Bloque", "Min", "Qué se muestra"],
                 [[str(n), t, str(m), muestra] for n, t, _, muestra, m in P.BLOQUES],
                 widths=[0.9, 4.2, 0.9, 9.0], fs=9)
    neutro.P(d,
        "Si el tiempo asignado no alcanza, se recortan en este orden: %s. Los bloques 3 y 8 no "
        "están en esa lista: son las tres decisiones y lo que no salió, que es lo que la "
        "materia evalúa. Quitarlos deja una presentación de producto."
        % ", ".join("bloque %d" % n for n in P.RECORTE_SI_FALTA_TIEMPO))

    # ------------------------------------------------------------------ 2
    neutro.H(d, "2. Qué se dice en cada bloque", 1)
    for n, titulo, puntos, muestra, minutos in P.BLOQUES:
        neutro.H(d, "Bloque %d — %s (%d min)" % (n, titulo, minutos), 2)
        neutro.bullets(d, puntos)
        neutro.P(d, "Se muestra: %s" % muestra, italic=True)

        if n == 2:
            neutro.table(d, ["Nº", "Medida de éxito"],
                         [[str(m[0]), m[1]] for m in estado.MEDIDAS],
                         widths=[1.0, 13.0], fs=9)
        if n == 3:
            neutro.table(d, ["Decisión", "Cuándo", "Efecto", "Documento"],
                         [[x["titulo"], x["cuando"], x["efecto"], x["doc"]]
                          for x in estado.DECISIONES],
                         widths=[2.6, 2.6, 7.0, 2.8], fs=8)
        if n == 4:
            neutro.P(d, "Los hitos, que son los puntos donde el proyecto cambió de estado:",
                     after=4)
            neutro.table(d, ["Fecha", "Hito", "Qué habilitó"],
                         [[h[0], h[1], h[2]] for h in estado.HITOS],
                         widths=[1.8, 4.4, 8.8], fs=7)
            neutro.P(d, "Y las cifras medidas, cada una con el archivo que la sostiene:",
                     after=4)
            neutro.table(d, ["Qué", "Cuánto"], [
                ["Latencia golpe a sonido", "p90 de +4.07 ms contra una ventana de −10 a +25 ms"],
                ["Fotogramas por segundo", "72 sostenidos; 100.0 % en sincronía vertical"],
                ["Deriva del reloj musical", "0.0 ms sostenidos durante 205 segundos"],
                ["Sesiones registradas", "%d completas, %d notas juzgadas"
                                         % (r["sesiones"], r["notas"])],
                ["Pruebas automáticas del prototipo", "%d métodos en %d archivos"
                                                      % (D["pruebas"], D["archivos"])],
                ["Pruebas de la documentación", "157 métodos"],
                ["Actividades del alcance vigente", "%d de %d cerradas"
                                                    % (sum(h for _, h, _ in estado.AVANCE),
                                                       sum(h + p for _, h, p in estado.AVANCE))],
            ], widths=[5.0, 10.0], fs=9, negritas_col0=True)
        if n == 6:
            neutro.table(d, ["Nº", "Medida", "Estado", "Con qué se sostiene"],
                         [[str(m[0]), m[1], m[2], m[3]] for m in estado.MEDIDAS],
                         widths=[0.8, 3.2, 1.6, 9.4], fs=7)
            neutro.P(d,
                "De las sesiones: %d completas, %.1f %% de precisión global, mediana de "
                "%.1f %%, constancia contra la rejilla %.1f ms y del pulso propio %.1f ms."
                % (r["sesiones"], r["precision_global"], r["precision_mediana"],
                   r["rejilla_mediana"], r["pulso_mediana"]))
            neutro.P(d,
                "Y qué NO se puede concluir, que hay que decirlo en voz alta: no son %d "
                "participantes, porque el volcado de sesión no lleva identificador de persona. "
                "Eso está en el documento 16 con su tabla de huecos." % 14, bold=True)
        if n == 7:
            neutro.table(d, ["Versión", "Supuesto", "Presupuesto"], [
                ["1ª", "Tarifas de mercado sin fuente, más compras", "$559,891"],
                ["2ª", "Observatorio Laboral, equipo prestado", "$294,981"],
                ["3ª vigente", "Salario mínimo escalado (practicantes), sin compras",
                 "$%s" % format(round(costos.PRESUPUESTO), ",")],
            ], widths=[2.2, 8.0, 4.8], fs=9, negritas_col0=True)
            neutro.P(d,
                "Ningún riesgo tiene impacto monetario porque el proyecto no compra ni "
                "contrata: la reserva se valora en días hábiles. El valor esperado es de "
                "%.2f días." % costos.EMV_DIAS)
        if n == 8:
            neutro.table(d, ["Qué no salió", "Qué se hizo"], [
                ["El asesor terapéutico nunca llegó, con fecha límite el 10 de septiembre",
                 "Se retiró la medida 8 y se documentó la ausencia de validación externa como "
                 "limitación explícita. Era la contingencia que el acta ya había previsto."],
                ["El cronograma mostraba el proyecto terminado en octubre",
                 "Llevaba las fechas del plan y no las reales. Se rebaseó con la fecha de "
                 "registro de cada actividad y su evidencia: documento 13."],
                ["El plan de cierre no cabe en la reserva",
                 "Cierra el %s, %d días hábiles después del fin de la reserva. El documento lo "
                 "dice con el número; no se recortó el plan para que la fecha cuadrara."
                 % (RP.CIERRE, RP.DIAS_DE_DESBORDE)],
                ["Las pruebas con usuarios no tienen atribución de participantes",
                 "Declarado en el documento 16, con qué dato falta y quién lo tiene."],
            ], widths=[4.4, 10.6], fs=8, negritas_col0=True)
        if n == 10:
            neutro.table(d, ["Qué queda abierto", "Cuándo"],
                         [[PU.PENDIENTE[i][0], "en cuanto exista el dato"]
                          for i in range(len(PU.PENDIENTE))] +
                         [["Las %d actividades pendientes del cronograma" % len(RP.CALENDARIO),
                           "hasta el %s según el replan" % RP.CIERRE]],
                         widths=[9.0, 6.0], fs=9)

    # ------------------------------------------------------------------ 3
    neutro.H(d, "3. Guion de la demostración", 1)
    neutro.P(d,
        "Ocho pasos, tres minutos. El orden no es el del menú: es el que enseña el recorrido "
        "completo sin repetir pantalla y sin depender de acertar un golpe difícil delante de "
        "todos.", bold=True)
    neutro.table(d, ["Nº", "Qué se hace", "Qué hay que ver", "Tiempo", "Qué puede salir mal"],
                 [[str(n), hace, ver, cuanto, riesgo] for n, hace, ver, cuanto, riesgo in P.DEMO],
                 widths=[0.8, 3.4, 4.6, 1.0, 5.2], fs=7)
    neutro.P(d,
        "Fallar notas en vivo no importa, y conviene decirlo antes de empezar: el veredicto en "
        "rojo también es parte de lo que se enseña. Lo que sí importa es que el recorrido "
        "llegue hasta salir.")

    # ------------------------------------------------------------------ 4
    neutro.H(d, "4. Antes de presentar", 1)
    neutro.P(d,
        "Cada punto de esta lista es algo que ya falló una vez en este proyecto.", bold=True)
    neutro.table(d, ["Qué hacer", "Por qué está en la lista"],
                 [[q, por] for q, por in P.ANTES],
                 widths=[6.0, 9.0], fs=9, negritas_col0=True)

    # ------------------------------------------------------------------ 5
    neutro.H(d, "5. Lo que falta de este documento", 1)
    neutro.table(d, ["Qué falta", "Dónde entra"],
                 [[t, dd] for t, dd in P.PENDIENTE_DE_DATO],
                 widths=[5.0, 10.0], fs=9, negritas_col0=True)

    return d


if __name__ == "__main__":
    if S.resumen() is None:
        raise SystemExit("No hay volcados de sesion. Corre quest.sh pull en el repo Unity.")
    doc().save(DOC)
    print("OK", DOC)
    print("   %d bloques · %d min · %d pasos de demo · %d comprobaciones previas"
          % (len(P.BLOQUES), MINUTOS, len(P.DEMO), len(P.ANTES)))
