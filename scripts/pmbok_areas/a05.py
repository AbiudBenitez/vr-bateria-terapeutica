# -*- coding: utf-8 -*-
"""
Área 5 — Alcance.

LAS CIFRAS DEL ALCANCE SE IMPORTAN DE recorte.py, que es su única fuente de verdad. Las diez
medidas de éxito, cuál se retiró, cuántas actividades sobreviven y cuántas se recortaron salen
de ahí; si una clave cambia de lista, cambia en este documento, en el del recorte, en el
marcado del cronograma y en las pruebas, todo a la vez.

EL CRITERIO DE RECORTE ES LO QUE HACE DEFENDIBLE ESTA ÁREA: sobrevive lo que sirve a una
medida de éxito de la carta sponsor y se recorta lo que no sirve a ninguna. No fue «lo que dio
tiempo».
"""
import pmbok_areas
import recorte

AREA = "5"

# SE LEEN DEL CRONOGRAMA, no se escriben aquí. Una prueba las vuelve a contar por su cuenta.
VIGENTES, HECHAS = pmbok_areas.avance_vigente()
ORIGINALES = 257

RESUMEN = [
    "El alcance del proyecto son dos entregables simultáneos: la documentación de "
    "administración de proyectos conforme a PMBOK y un prototipo de realidad virtual "
    "demostrable y validado con usuarios. Lo que define si el alcance se cumplió no es la "
    "lista de tareas, sino las diez medidas de éxito que comprometió la carta sponsor: diez "
    "resultados verificables.",

    f"Esa distinción es la que permitió recortar sin romper el compromiso. El proyecto pasó de "
    f"{ORIGINALES} a {VIGENTES} actividades: {recorte.resumen()['recortadas']} recortadas, "
    f"{recorte.resumen()['ya_hechas']} que estaban hechas sin registrar y "
    f"{recorte.resumen()['nuevas']} añadida. El criterio no fue el tiempo disponible: sobrevive "
    "lo que sirve a una medida de éxito y se recorta lo que no sirve a ninguna.",

    f"De las diez medidas, una se retiró —la número {recorte.MEDIDA_RETIRADA}, pertinencia "
    "terapéutica— porque sin el asesor externo no había forma de verificarla por ningún "
    "camino. Las otras nueve siguen vigentes. El alcance vigente va al "
    f"{100.0*HECHAS/VIGENTES:.0f} %: {HECHAS} de {VIGENTES} actividades.",
]

PROCESOS = {
    "5.1": (
        "El alcance se planificó en el acta constitutiva, con el objetivo, los entregables y "
        "los criterios de terminación del proyecto. La regla que gobierna los cambios quedó "
        "fijada ahí: toda variación de alcance se tramita por documento formal con la "
        "patrocinadora, nunca de palabra.",
        "Acta constitutiva §2.3 alcance, §2.4 entregables y §4.12 criterios de terminación.",
    ),
    "5.2": (
        "Los requisitos se recopilaron como diez medidas de éxito verificables en la carta "
        "sponsor, cada una con su criterio de comprobación, en vez de como una lista de "
        "funciones. Esa forma es la que después permitió decidir qué recortar.",
        f"01_Carta_Sponsor.docx, las {len(recorte.MEDIDAS)} medidas de éxito; "
        "scripts/recorte.py, diccionario MEDIDAS con el criterio de cada una.",
    ),
    "5.3": (
        "El alcance se definió y se redefinió dos veces por escrito: el recorte de alcance del "
        "17 de octubre y el cambio de encuadre terapéutico del 18. Las dos son solicitudes de "
        "cambio formales, no reescrituras del documento original, que se conserva.",
        "10_Recorte_de_Alcance.docx y 11_Cambio_de_Enfoque.docx; las versiones anteriores en "
        "entregables/superados/.",
    ),
    "5.4": (
        "La EDT se descompone por entregables —sustantivos— y no por fases, con las reglas del "
        "100 % y del 8/80. Son 42 paquetes de trabajo en siete ramas, cada uno con criterio de "
        "aceptación verificable, responsable, recursos y duración.",
        "Acta constitutiva §4.2 estructura de desglose del trabajo y §4.3 paquetes de trabajo, "
        "ramas 1 a 7.",
    ),
    "5.5": (
        "La validación del alcance se instrumentó con dos documentos para firma: la carta de "
        "validación de entregables y la lista de verificación de compromisos, que contrasta lo "
        "comprometido contra lo entregado. La validación final del prototipo depende de las "
        "pruebas con usuarios, que es la actividad QT.8.",
        "07_Carta_Validacion_Entregables.docx y 08_Lista_Verificacion_Compromisos.docx, ambos "
        "fechados el 21 de septiembre con línea de firma.",
    ),
    "5.6": (
        "El control del alcance se ejerció sobre el cronograma: las actividades recortadas no "
        "se borran, llevan la marca [FUERA DE ALCANCE] y la razón en el campo de notas. Así el "
        "alcance retirado sigue siendo consultable y el avance se mide contra el vigente, no "
        "contra trabajo cancelado.",
        f"Cronograma_Operativo.xml y Cronograma_ProjectLibre.xml, con las "
        f"{recorte.resumen()['recortadas']} marcadas; scripts/validacion.py, que las excluye "
        "del denominador.",
    ),
}

TABLAS = [
    ("Las diez medidas de éxito: el alcance real del compromiso",
     ["N.º", "Medida", "Estado"],
     [[str(n), texto,
       "RETIRADA" if n == recorte.MEDIDA_RETIRADA else "Vigente"]
      for n, texto in recorte.MEDIDAS.items()]),

    ("Por qué hay tres cifras de alcance vigente, y las tres son correctas",
     ["Fuente", "Cuenta", "Qué mide"],
     [["Cronograma_Operativo.xml", str(VIGENTES),
       "El alcance vigente completo. Es el cronograma que se trabaja."],
      ["Cronograma_ProjectLibre.xml, descontadas las recortadas",
       str(ORIGINALES - recorte.resumen()['recortadas']),
       "El alcance vigente SIN DM.1: esa actividad la creó el recorte, así que no existe en "
       "el cronograma anterior a él."],
      ["Red de la ruta crítica v3",
       str(ORIGINALES - recorte.resumen()['recortadas']),
       "La red del método de la ruta crítica, que no incluye DM.1 en el cálculo."],
      ["Diferencia", "1",
       "Exactamente DM.1, exportar las métricas de sesión. Las tres cifras miden cosas "
       "distintas y ninguna contradice a las otras."]]),

    ("Qué pasó con el alcance",
     ["Concepto", "Actividades", "Criterio aplicado"],
     [["Alcance original", str(ORIGINALES),
       "La lista de tareas con que arrancó el proyecto."],
      ["Recortadas", str(recorte.resumen()['recortadas']),
       "No servían a ninguna medida de éxito. Se marcan, no se borran."],
      ["Ya estaban hechas sin registrar", str(recorte.resumen()['ya_hechas']),
       "Trabajo ejecutado que el registro no reflejaba, sobre todo del área de sonido."],
      ["Añadidas", str(recorte.resumen()['nuevas']),
       "DM.1, exportar las métricas de sesión: cerraba la medida de éxito 9, que estaba en "
       "cero."],
      ["Alcance vigente", str(VIGENTES),
       f"Lo que sirve a las nueve medidas vigentes. Avance: {HECHAS} de {VIGENTES} "
       f"({100.0*HECHAS/VIGENTES:.0f} %)."]]),

    ("Los tres recortes grandes, y su razón",
     ["Área", "De", "A", "Por qué"],
     [["Entorno 3D", "31", "6",
       "El área deja de modelar y pasa a integrar assets de licencia libre. Diecisiete tareas "
       "seriales de modelado no caben en diecinueve días."],
      ["Juego de ritmo", "22", "0",
       "Ya estaban retiradas por la respuesta al riesgo R14. El recorte solo lo refleja."],
      ["Sonido", "22", "1",
       "Doce ya estaban hechas sin registrar. Solo faltaba el crash, que entró el 19 de "
       "octubre."]]),
]

LECCIONES = [
    ("Comprometer resultados verificables, no una lista de tareas",
     "La carta sponsor comprometió diez medidas de éxito y no 257 actividades. Cuando el "
     "tiempo no alcanzó, eso permitió recortar el 40 % del trabajo sin incumplir el "
     "compromiso: bastaba demostrar que lo recortado no servía a ninguna medida. Si el "
     "compromiso hubiera sido la lista de tareas, cualquier recorte habría sido un "
     "incumplimiento, y la única salida habría sido entregar tarde o entregar mal."),

    ("Una actividad borrada no deja rastro de por qué se quitó",
     f"Las {recorte.resumen()['recortadas']} recortadas siguen en los dos cronogramas con la "
     "marca [FUERA DE ALCANCE] y la razón en sus notas. Fue una decisión deliberada: un "
     "cronograma del que desaparecen cien tareas no se puede auditar, y a quien pregunte «¿y "
     "esto por qué no se hizo?» hay que poder responderle con el archivo, no con la memoria."),

    ("Doce actividades estaban hechas y nadie lo sabía",
     "Al revisar el alcance para recortarlo aparecieron doce actividades del área de sonido ya "
     "ejecutadas y sin registrar. No se descubrieron antes porque nadie las había preguntado: "
     "es el mismo defecto de comunicación que dejó la hoja de control del equipo 74 "
     "actividades por detrás del cronograma. Recortar alcance obligó a auditar el avance, y la "
     "auditoría encontró trabajo regalado."),
]

REMITE_A = [
    ("entregables/10_Recorte_de_Alcance.docx",
     "El recorte completo con la razón de cada una de las actividades retiradas, y el retiro "
     "formal de la medida de éxito 8."),
    ("entregables/02_Acta_Constitutiva.docx",
     "La EDT de 42 paquetes con criterio de aceptación, responsable, recursos y duración, en "
     "siete ramas."),
    ("entregables/01_Carta_Sponsor.docx",
     "Las diez medidas de éxito tal como se comprometieron, con su criterio de verificación."),
    ("entregables/11_Cambio_de_Enfoque.docx",
     "La redefinición del encuadre terapéutico, que cambió el objetivo sin cambiar el "
     "producto."),
    ("entregables/07_Carta_Validacion_Entregables.docx",
     "El instrumento de validación del alcance, para firma de la patrocinadora."),
]
