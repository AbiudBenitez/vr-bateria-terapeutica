# -*- coding: utf-8 -*-
"""
Genera la carta de validación de entregables y la lista de verificación corregida.

Las cifras se leen del cronograma en tiempo de generación (ver validacion.py). Si el
cronograma cambia, se vuelve a correr esto y los documentos quedan al día. Escribir las cifras
a mano es cómo se llega a tener tres números distintos para la misma cosa.
"""
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import neutro
import validacion

HOY = "21 de septiembre de 2026"
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")

ENTREGABLES = [
    ("01_Carta_Sponsor.docx", "Carta del patrocinador",
     "Justificación, objetivos medibles y medidas de éxito del proyecto.",
     "Declara diez medidas de éxito, cada una con su método de comprobación."),
    ("02_Acta_Constitutiva.docx", "Acta constitutiva",
     "Autorización formal del proyecto y estructura de desglose del trabajo.",
     "42 paquetes de trabajo, cada uno con criterio de aceptación verificable, "
     "responsable, recursos y duración. Reglas del 100 % y 8/80."),
    ("03_Ruta_Critica.docx", "Ruta crítica",
     "Secuenciación de actividades y cálculo de la ruta crítica.",
     "Red PDM de 257 actividades y 417 dependencias. La ruta se recalcula sola "
     "al abrir el cronograma en ProjectLibre."),
    ("04_Planes_Costos_Calidad_Riesgos.docx", "Planes de gestión",
     "Planes de costos, calidad y riesgos.",
     "Cobertura PMBOK 7.1 a 7.4, 8.1 a 8.3 y 11.1 a 11.7."),
    ("05_Analisis_Costos_Calidad_Riesgos.docx", "Análisis de costos",
     "Costeo ascendente, presupuesto, compresión y costo de la calidad.",
     "Tarifas tomadas de fuentes oficiales mexicanas: STPS/ENOE-INEGI, CONASAMI e IMSS. "
     "Ninguna tarifa estimada sin fuente."),
    ("06_Entregable_Medio_Curso.docx", "Compromiso de medio curso",
     "Declaración de lo que el equipo entrega el 21 de septiembre.",
     "Cada compromiso remite a las claves de tarea que lo respaldan."),
    ("Cronograma_ProjectLibre.xml", "Cronograma",
     "Plan del proyecto con el avance cargado.",
     "Abrible en ProjectLibre. El avance por tarea es consultable con la columna "
     "«% Complete» y visible en las barras del diagrama de Gantt."),
]

LIMITACIONES = [
    ("Asesor terapéutico externo",
     "No se concretó. La fecha límite de confirmación era el 10 de septiembre.",
     "Se documenta la ausencia de validación externa como limitación explícita y se "
     "trabaja con protocolos publicados de Neurologic Music Therapy."),
    ("Entorno tridimensional definitivo",
     "Solo dirección artística y criterios de rendimiento.",
     "Su cadena tiene 17 actividades estrictamente seriales y es la ruta crítica. "
     "No admite adelanto sin comprometer la calidad."),
    ("Interfaz dentro del motor",
     "Existen el mapa de pantallas y los prototipos de diseño; la implementación en Unity no.",
     "La interfaz se construye sobre el esquema de interacción, que se integró en este corte."),
    ("Rutinas terapéuticas dentro del simulador",
     "Guion y flujo definidos, sin implementar.",
     "Requieren el sistema de audio integrado con la interacción, que concluyó en este corte."),
    ("Pruebas con usuarios",
     "Planes de prueba redactados.",
     "Necesitan el prototipo integrado completo."),
    ("Baquetas con física de agarre",
     "No se implementan y no se implementarán.",
     "Las baquetas van solidarias al control. El acta descartó el agarre porque los "
     "controles entregan háptico y una lectura confiable de velocidad; añadir física "
     "introduciría el paso de simulación en el camino del golpe y degradaría la latencia."),
]


# LA SECCION 3.1 YA NO SE GENERA.
#
# El equipo decidió el 21-sep retirar la nota que conciliaba las cifras del documento de medio
# curso con las del cronograma. Durante un mes este generador la siguió produciendo y el aviso
# que había aquí decía que, si alguien regeneraba, tenía que volver a quitarla a mano. Un
# generador que contradice una decisión del equipo y lo compensa con un comentario es una
# trampa: funciona hasta que la pisa quien no leyó el comentario.
#
# Además su premisa caducó. Conciliaba 117 contra la cifra del cronograma porque la hoja de
# control y el cronograma se habían desincronizado; los dos cronogramas se sincronizan ahora
# con scripts/sincronizar_crono.py, que tiene sus propias pruebas.


def carta():
    r = validacion.resumen()
    doc = neutro.nuevo()

    neutro.portada(
        doc,
        "Carta de validación de entregables",
        "Simulación de Batería en Realidad Virtual con Enfoque Terapéutico",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha", HOY),
         ("Periodo que cubre", "7 de septiembre a 18 de septiembre de 2026"),
         ("Proceso", "PMBOK 5.5 Validar el Alcance")],
    )

    neutro.H(doc, "1. Propósito", 1)
    neutro.P(doc,
             "Este documento solicita la validación formal de los entregables producidos por el "
             "Equipo A hasta el corte del 18 de septiembre de 2026. La validación del alcance es "
             "el proceso mediante el cual se formaliza la aceptación de los entregables "
             "terminados; su salida son entregables aceptados.")
    neutro.P(doc,
             "Cada entregable se presenta con un criterio de aceptación verificable de forma "
             "independiente, sin necesidad de tomar como cierta ninguna afirmación del equipo. "
             "La sección 5 declara lo que no se entrega y por qué.")

    neutro.H(doc, "2. Entregables sometidos a validación", 1)
    neutro.table(
        doc,
        ["Archivo", "Entregable", "Contenido", "Criterio de aceptación"],
        [[a, b, c, d] for a, b, c, d in ENTREGABLES],
        widths=[3.6, 3.0, 4.0, 5.4], fs=8.0,
    )

    neutro.H(doc, "2.1 Prototipo funcional", 2)
    neutro.P(doc,
             "Además de los documentos, se somete a validación el prototipo ejecutable instalado "
             "en el visor Meta Quest 3S. Se demuestra en vivo.")
    neutro.table(
        doc,
        ["Función", "Criterio de aceptación"],
        [["Batería de seis piezas",
          "Se golpea cada pieza y suena el instrumento correspondiente."],
         ["Identificación de la pieza golpeada",
          "Un indicador dentro del visor muestra el nombre de la pieza en cada golpe."],
         ["Tres niveles de intensidad",
          "El mismo indicador muestra la intensidad; un golpe suave y uno fuerte en la "
          "misma pieza producen indicación y sonido distintos."],
         ["Respuesta háptica proporcional",
          "El control vibra con amplitud proporcional a la velocidad del golpe."],
         ["Verificación automatizada",
          "50 pruebas automatizadas que se ejecutan sin visor desde el editor."]],
        widths=[4.8, 11.2], fs=8.5,
    )

    neutro.H(doc, "3. Estado del avance", 1)
    neutro.P(doc,
             f"Al corte del 18 de septiembre, el cronograma registra "
             f"{r['hechas']} de {r['total']} actividades terminadas "
             f"({r['pct']:.0f} %). Esta cifra es la que arroja el archivo del cronograma al "
             f"abrirlo, y puede comprobarse sin intermediarios.")
    neutro.table(
        doc,
        ["Área", "Actividades terminadas"],
        [[k, str(v)] for k, v in r["por_area"].items()],
        widths=[10.0, 6.0], fs=9.0,
    )
    neutro.table(
        doc,
        ["Responsable", "Terminadas", "Asignadas"],
        [[k, str(v["hechas"]), str(v["total"])] for k, v in r["por_responsable"].items()],
        widths=[6.0, 5.0, 5.0], fs=9.0,
    )


    neutro.H(doc, "4. Hito Go/No-Go de latencia", 1)
    neutro.P(doc,
             "El acta constitutiva identifica la latencia entre el golpe físico y el sonido como "
             "el riesgo dominante del proyecto, y fija su medición como hito de decisión "
             "Go/No-Go en la semana 4. Es el único resultado del proyecto obtenido por medición "
             "y no por estimación.")
    neutro.table(
        doc,
        ["Concepto", "Valor"],
        [["Criterio de aceptación", "−10 ms ≤ Δ(p90) ≤ +25 ms"],
         ["Resultado medido", "+4.07 ms (percentil 90 sobre 20 golpes)"],
         ["Mediana", "+3.29 ms"],
         ["Veredicto", "APRUEBA, con un margen de seis veces"],
         ["Fecha de medición", "16 de septiembre de 2026"],
         ["Fecha comprometida en el acta", "25 de septiembre de 2026"],
         ["Método", "Protocolo de clic físico: el golpe del control contra una superficie "
                    "real sirve de referencia temporal, con precisión de muestra a 48 kHz"],
         ["Contraste", "Dos corridas, con y sin la mitigación de predicción"]],
        widths=[5.2, 10.8], fs=8.5,
    )
    neutro.P(doc,
             "La medición arrojó un hallazgo que contradice el supuesto del diseño y que se "
             "documenta como tal: la predicción del plano armado no reduce la latencia media "
             "sino su dispersión, a un tercio. La diferencia es estadísticamente sólida "
             "(prueba de permutación con 20 000 remuestreos, p = 0.0001) y se confirmó de forma "
             "independiente con la instrumentación interna de la aplicación.")

    neutro.H(doc, "5. Limitaciones declaradas", 1)
    neutro.P(doc,
             "Se declara explícitamente lo que no se entrega en este corte. Declararlo evita "
             "que se interprete como retraso lo que es secuencia planificada, y acota el "
             "alcance de la validación que se solicita.")
    neutro.table(
        doc,
        ["Componente", "Estado", "Razón"],
        [[a, b, c] for a, b, c in LIMITACIONES],
        widths=[3.8, 5.2, 7.0], fs=8.0,
    )
    neutro.P(doc,
             "El proyecto no cuenta con supervisión clínica ni validación diagnóstica. No se "
             "presenta como tratamiento de ninguna condición de salud, y la literatura "
             "consultada respalda hablar de apoyo a la coordinación y la regulación, no de "
             "efecto terapéutico comprobado.", italic=True)

    neutro.H(doc, "6. Dictamen de la docente", 1)
    neutro.P(doc, "Marque la opción que corresponda:")
    neutro.table(
        doc,
        ["", "Dictamen", "Significado"],
        [["☐", "Entregables aceptados",
          "Los entregables cumplen los criterios de aceptación declarados."],
         ["☐", "Aceptados con observaciones",
          "Se aceptan y las observaciones se atienden antes del siguiente corte."],
         ["☐", "No aceptados",
          "No cumplen los criterios. Se indica cuáles y qué falta."]],
        widths=[1.2, 5.0, 9.8], fs=9.0,
    )
    neutro.P(doc)
    neutro.P(doc, "Observaciones:", bold=True)
    for _ in range(5):
        neutro.P(doc, "_" * 108)

    neutro.H(doc, "7. Firmas", 1)
    neutro.P(doc)
    neutro.table(
        doc,
        ["Rol", "Nombre", "Firma"],
        [["Gerente de proyecto", "Abiud Misael Benítez Franco", "_" * 30],
         ["Coordinadora", "Sarai Galindo García", "_" * 30],
         ["Director de proyecto", "Benjamín Ignacio Villalón Bobadilla", "_" * 30],
         ["Docente", "Dra. Leticia Amalia Neira Tovar", "_" * 30]],
        widths=[4.4, 6.6, 5.0], fs=9.5,
    )
    neutro.P(doc)
    neutro.P(doc, f"Fecha de validación: {'_' * 30}")

    ruta = os.path.join(SALIDA, "07_Carta_Validacion_Entregables.docx")
    doc.save(ruta)
    return ruta, r


def lista():
    """
    La lista de verificación, regenerada desde el cronograma.

    La versión anterior se generó solo de la hoja de control, que nunca se actualizó para el
    área de desarrollo: declaraba 6 tareas terminadas de 30 cuando eran 27. Un documento con
    línea de firma no puede declarar como pendiente trabajo que está hecho y es verificable.
    """
    f = validacion.fusion()
    r = validacion.resumen()
    doc = neutro.nuevo()
    neutro.landscape(doc, margen=1.6)

    neutro.portada(
        doc,
        "Lista de verificación de compromisos",
        "Simulación de Batería en Realidad Virtual con Enfoque Terapéutico",
        [("Equipo", "Equipo A"),
         ("Fecha", HOY),
         ("Corte del avance", "18 de septiembre de 2026"),
         ("Fuente", "Cronograma del proyecto y hoja de control"),
         ("Anexo de", "Carta de validación de entregables")],
    )

    neutro.P(doc,
             f"Las {r['total']} actividades del proyecto, agrupadas por responsable. El estado "
             "procede del cronograma, que es el plan único del proyecto. Se marca como "
             "terminada la actividad que el cronograma registra al 100 %.")
    neutro.P(doc,
             f"Respecto de la versión anterior de esta lista, {len(r['desfase'])} actividades "
             "pasan de pendientes a terminadas. Corresponden al área de desarrollo VR, cuyo "
             "avance la hoja de control no había registrado. Todas son verificables en el "
             "repositorio del proyecto.", italic=True)

    orden = sorted(r["por_responsable"].items(), key=lambda kv: -kv[1]["hechas"])
    for resp, cuenta in orden:
        neutro.H(doc, f"{resp} — {cuenta['hechas']} de {cuenta['total']} terminadas", 1)
        filas = sorted((t for t in f.values() if t["responsable"] == resp),
                       key=lambda t: (not t["hecha"], t["clave"]))
        neutro.table(
            doc,
            ["Clave", "Actividad", "Estado", "Compromiso", "Hecho"],
            [[t["clave"], t["tarea"][:78],
              "Terminada" if t["hecha"] else t["estado_hoja"],
              t["compromiso"].strftime("%d/%m/%Y") if hasattr(t["compromiso"], "strftime")
              else (str(t["compromiso"])[:10] if t["compromiso"] else "—"),
              "X" if t["hecha"] else ""]
             for t in filas],
            widths=[1.8, 12.5, 3.2, 3.0, 1.5], fs=7.5,
        )

    neutro.H(doc, "Resumen", 1)
    neutro.table(
        doc,
        ["Responsable", "Terminadas", "Asignadas", "Avance"],
        [[k, str(v["hechas"]), str(v["total"]),
          f"{100.0 * v['hechas'] / max(v['total'], 1):.0f} %"]
         for k, v in orden]
        + [["TOTAL", str(r["hechas"]), str(r["total"]), f"{r['pct']:.0f} %"]],
        widths=[5.0, 4.0, 4.0, 4.0], fs=9.0, negritas_col0=True,
    )
    neutro.P(doc)
    neutro.P(doc, "Firma de la coordinadora del proyecto: " + "_" * 34 +
                  "     Fecha: " + "_" * 18)

    ruta = os.path.join(SALIDA, "08_Lista_Verificacion_Compromisos.docx")
    doc.save(ruta)
    return ruta


# -----------------------------------------------------------------------------------------
# SEGURO CONTRA REGENERAR UN ENTREGABLE YA FECHADO
#
# Los documentos 07 y 08 llevan fecha del 21 de septiembre de 2026, corte del 18, y lineas de
# firma. Las cifras, en cambio, se LEEN del cronograma, que avanza: hoy el mismo generador
# produciria 130 de 157 bajo una fecha de hace un mes. Eso no es actualizar un documento, es
# fabricar uno incoherente, y con una firma debajo.
#
# La convencion del proyecto es la contraria: lo que cambia va en un documento nuevo y el
# original se conserva en entregables/superados/. Asi se hizo con el recorte y con el cambio
# de enfoque.
#
# Por eso hay que pedirlo a proposito, y diciendo con que fecha.
#
# El __main__ estaba ADEMAS colocado antes de def lista(), de modo que el documento 08 no se
# podia regenerar desde la linea de comandos en absoluto.

def main(argv):
    if "--regenerar" not in argv:
        r = validacion.resumen()
        print("  No se ha escrito nada. Los documentos 07 y 08 estan fechados el "
              f"{HOY}, con corte del 18 de septiembre.")
        print(f"  El cronograma va hoy por {r['hechas']} de {r['total']} "
              f"({r['pct']:.0f} %), que NO es la cifra con la que se entregaron.")
        print()
        print("  Si de verdad quieres reescribirlos con las cifras de hoy:")
        print("      1. copia los actuales a entregables/superados/")
        print("      2. cambia HOY y el corte del avance en este script")
        print("      3. vuelve a correrlo con --regenerar")
        print()
        print("  El avance vigente se publica en 12_Estado_del_Proyecto.docx, que para eso")
        print("  existe: scripts/gen_estado.py.")
        return 1

    for ruta in (carta()[0], lista()):
        print(f"  {os.path.basename(ruta)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
