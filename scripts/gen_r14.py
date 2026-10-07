# -*- coding: utf-8 -*-
"""Genera el documento de respuesta al riesgo R14."""
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import neutro
import r14
import validacion

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")


def doc():
    res = validacion.resumen()
    f = validacion.fusion()
    hab = r14.habiles(r14.HOY, r14.CIERRE)
    pend_ben = [t for t in f.values() if t["responsable"] == "Benjamin" and not t["hecha"]]

    d = neutro.nuevo()
    neutro.portada(
        d,
        "Respuesta al riesgo R14",
        "Baja de un integrante del equipo · Redistribución y recorte de alcance",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha", "6 de octubre de 2026"),
         ("Riesgo", "R14 — Un integrante abandona el equipo o da de baja la materia"),
         ("Proceso", "PMBOK 11.6 Implementar la Respuesta a los Riesgos")],
    )

    # ------------------------------------------------------------------ 1
    neutro.H(d, "1. El riesgo se materializó", 1)
    neutro.P(d,
             "El plan de gestión de riesgos del proyecto registra R14 con el disparador "
             "«un integrante comunica su baja o deja de presentarse dos semanas seguidas». "
             "El disparador se cumplió: Benjamín Ignacio Villalón Bobadilla lleva más de dos "
             "semanas sin presentarse y no ha comunicado su situación.")
    neutro.table(
        d,
        ["Campo", "Lo previsto en el plan", "Lo observado"],
        [["Probabilidad", "15 %", "Ocurrió"],
         ["Impacto estimado", "6.0 días hábiles", f"{len(pend_ben)} actividades sin responsable"],
         ["Estrategia", "Mitigar", "Se aplica: redistribuir y recortar"],
         ["Responsable del riesgo", "Benjamín",
          "El responsable designado es el integrante que causó el riesgo. "
          "Se reasigna en la sección 2."],
         ["Segundo conocedor del área", "«Cada área tiene un segundo conocedor designado»",
          "Nunca se designó. Se corrige en la sección 4."]],
        widths=[4.0, 5.6, 6.4], fs=8.5,
    )
    neutro.P(d,
             "Se documentan los dos defectos del plan en lugar de corregirlos en silencio: un "
             "registro de riesgos cuyo dueño es la propia fuente del riesgo, y una respuesta "
             "que da por existente una designación que nunca se hizo. Ambos se subsanan en "
             "este documento.", italic=True)

    # ------------------------------------------------------------------ 2
    neutro.H(d, "2. Reasignación de responsabilidades", 1)
    neutro.table(
        d,
        ["Función", "Antes", "Ahora", "Razón"],
        [["Dirección de proyecto", "Benjamín", "Sarai Galindo García",
          "La coordinación ya concentra la comunicación del equipo."],
         ["Área Juego de ritmo", "Benjamín", "Abiud Misael Benítez Franco",
          "El juego se monta sobre el evento DrumHit, que es del área de desarrollo VR "
          "y ya está construido."],
         ["Responsable del riesgo R14", "Benjamín", "Sarai Galindo García",
          "Un riesgo de equipo corresponde a quien coordina el equipo."]],
        widths=[3.6, 2.6, 4.2, 5.6], fs=8.5,
    )

    # ------------------------------------------------------------------ 3
    neutro.H(d, "3. Recorte de alcance del juego de ritmo", 1)
    neutro.P(d,
             f"El plan de respuesta de R14 indica redistribuir el trabajo restante "
             f"y recortar el alcance secundario del área afectada. Se hacen las dos cosas: "
             f"redistribuir sin recortar trasladaría {len(pend_ben)} actividades a una persona "
             f"que dispone de {hab} días hábiles.")
    neutro.P(d,
             "El criterio del recorte no es qué cabe en el tiempo disponible, sino qué es lo "
             "mínimo que demuestra que el juego de ritmo existe y funciona. Un juego sin "
             "niveles de dificultad sigue siendo un juego de ritmo; sin reloj musical ni "
             "ventanas de precisión no es nada.")

    neutro.H(d, "3.1 Se conserva", 2)
    neutro.table(
        d,
        ["Clave", "Actividad"],
        [[k, v] for k, v in r14.CONSERVA],
        widths=[2.4, 13.6], fs=8.5,
    )
    neutro.P(d, f"Total conservado: {len(r14.CONSERVA)} actividades.")

    neutro.H(d, "3.2 Se recorta, con su justificación", 2)
    neutro.table(
        d,
        ["Claves", "Actividad", "Por qué se recorta"],
        [[a, b, c] for a, b, c in r14.RECORTA],
        widths=[2.6, 4.4, 9.0], fs=8.0,
    )
    neutro.P(d,
             "Cuatro de los recortes no son pérdida de alcance sino actividades que quedaron "
             "sin objeto: la interacción VR ya existe, de modo que sustituir un sistema "
             "provisional de teclado que nunca se construyó carece de sentido; y la "
             "calibración de latencia ya se resolvió por otra vía, con un resultado medido de "
             "+4.07 ms en el percentil 90.", italic=True)

    # ------------------------------------------------------------------ 4
    neutro.H(d, "4. Segundos conocedores por área", 1)
    neutro.P(d,
             "El plan de R14 los daba por designados. No lo estaban. Se designan ahora, con el "
             "compromiso de que el segundo conocedor pueda continuar el área si su responsable "
             "principal falta.")
    neutro.table(
        d,
        ["Área", "Responsable", "Segundo conocedor", "Razón"],
        [[a, b, c, e] for a, b, c, e in r14.SEGUNDOS],
        widths=[3.8, 3.2, 3.2, 5.8], fs=8.0,
    )

    # ------------------------------------------------------------------ 5
    neutro.H(d, "5. Trabajo ya hecho que no estaba registrado", 1)
    neutro.P(d,
             "Al revisar el estado real del proyecto se encontró trabajo terminado que el área "
             "responsable no había registrado. Verificarlo antes de empezar evita repetirlo.")
    neutro.table(
        d,
        ["Área", "Claves", "Actividad", "Estado real"],
        [[a, b, c, e] for a, b, c, e in r14.YA_HECHO],
        widths=[2.2, 3.0, 4.4, 6.4], fs=8.0,
    )

    # ------------------------------------------------------------------ 6
    neutro.H(d, "6. Qué investigar cada área", 1)
    neutro.P(d,
             "Indicaciones concretas por responsable: dónde buscar y con qué criterio decidir. "
             "No sustituyen el juicio de cada quien; acortan el arranque.")
    def sin_acentos(x):
        # La hoja de control escribe «Maria» sin acento y aquí se usa «María»; comparar
        # literalmente daba cero pendientes para ella.
        return "".join(c for c in unicodedata.normalize("NFD", x)
                       if unicodedata.category(c) != "Mn").lower()

    for persona, items in r14.INVESTIGAR.items():
        pend = sum(1 for t in f.values()
                   if sin_acentos(t["responsable"]) == sin_acentos(persona)
                   and not t["hecha"])
        neutro.H(d, f"{persona} — {pend} actividades pendientes", 2)
        neutro.table(
            d,
            ["Qué", "Dónde", "Criterio"],
            [[a, b, c] for a, b, c in items],
            widths=[4.2, 5.2, 6.6], fs=8.0,
        )

    # ------------------------------------------------------------------ 7
    neutro.H(d, "7. Situación del proyecto", 1)
    neutro.table(
        d,
        ["Concepto", "Valor"],
        [["Avance registrado", f"{res['hechas']} de {res['total']} actividades "
                               f"({res['pct']:.0f} %)"],
         ["Días hábiles al cierre del cronograma", f"{hab} (30 de octubre)"],
         ["Días hábiles al cierre del periodo", f"{r14.habiles(r14.HOY, r14.PERIODO)} "
                                                f"(13 de noviembre)"],
         ["Reserva de gestión disponible", "10.75 días hábiles, más la semana del 16 al 20 "
                                           "de noviembre"],
         ["Actividades sin responsable tras la baja", str(len(pend_ben))],
         ["Actividades reasignadas", str(len(r14.CONSERVA))],
         ["Actividades recortadas del alcance", str(len(pend_ben) - len(r14.CONSERVA))]],
        widths=[7.0, 9.0], fs=9.0,
    )
    neutro.P(d,
             "Conviene declararlo con claridad: 180 actividades pendientes en 18 días hábiles "
             "no caben al ritmo actual. Este documento recorta el alcance de un área. Si el "
             "ritmo de las demás no cambia, habrá que decidir entre recortar más alcance o "
             "consumir la reserva de gestión. Ambas decisiones son del equipo y se toman "
             "antes, no después.")

    # ------------------------------------------------------------------ 8
    neutro.H(d, "8. Acuerdos y firmas", 1)
    neutro.P(d, "El equipo acuerda lo contenido en este documento:")
    neutro.bullets(d, [
        "La dirección de proyecto y la titularidad del riesgo R14 pasan a la coordinación.",
        "El área de juego de ritmo pasa a desarrollo VR, con el alcance recortado de la "
        "sección 3.",
        "Cada área cuenta con un segundo conocedor designado, según la sección 4.",
        "Cada responsable verifica la sección 5 antes de iniciar trabajo que pueda estar hecho.",
        "El recorte de alcance se comunica a la docente como parte del informe de avance.",
    ])
    neutro.P(d)
    neutro.table(
        d,
        ["Rol", "Nombre", "Firma"],
        [["Dirección de proyecto", "Sarai Galindo García", "_" * 26],
         ["Gerencia de proyecto", "Abiud Misael Benítez Franco", "_" * 26],
         ["QA y documentación", "Diana Laura Tello Salinas", "_" * 26],
         ["Entorno 3D", "Kimberly González Sepúlveda", "_" * 26],
         ["Sonido", "Christian Salvador Valadez Gallegos", "_" * 26],
         ["Música", "Javier Alejandro Hernández Caloca", "_" * 26],
         ["Experiencia emocional", "María Fernanda Montoya Valdez", "_" * 26]],
        widths=[4.4, 6.6, 5.0], fs=9.0,
    )
    neutro.P(d)
    neutro.P(d, "Fecha del acuerdo: " + "_" * 30)

    ruta = os.path.join(SALIDA, "09_Respuesta_Riesgo_R14.docx")
    d.save(ruta)
    return ruta


if __name__ == "__main__":
    print("  " + os.path.basename(doc()))
