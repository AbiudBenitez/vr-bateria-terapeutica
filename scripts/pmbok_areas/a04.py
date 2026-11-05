# -*- coding: utf-8 -*-
"""
Área 4 — Integración, incluida el acta de constitución.

ES EL ÁREA QUE DECLARA POR QUÉ FALTA EL 06. Esta carpeta tiene nueve documentos para diez
áreas de conocimiento: el cronograma no lleva documento propio porque ya está cubierto por los
dos archivos de cronograma y por los dos documentos de ruta crítica. Decirlo aquí es parte de
integrar: un entregable con un hueco sin explicación obliga a quien lo recibe a suponer.

EL CONTROL INTEGRADO DE CAMBIOS ES LO MÁS EJECUTADO DEL PROYECTO. Tres solicitudes formales en
trece días: la baja de un integrante, el recorte de 257 a 155 actividades y el cambio del
encuadre terapéutico.
"""
import enfoque
import pmbok_areas

AREA = "4"

# SE LEEN DEL CRONOGRAMA, no se escriben aquí. Hay una prueba que las recuenta por su cuenta
# y otra que comprueba que el área 5 diga lo mismo.
VIGENTES, HECHAS = pmbok_areas.avance_vigente()

# Las tres solicitudes de cambio formales, en orden.
CAMBIOS = [
    ("6 de octubre de 2026", "Respuesta al riesgo R14: baja de un integrante",
     "09_Respuesta_Riesgo_R14.docx",
     "El área de juego de ritmo pasó a desarrollo VR. De sus 22 actividades sobrevivieron 15. "
     "La dirección y la coordinación quedaron sin titular y su carga se absorbió en QA."),
    ("17 de octubre de 2026", "Recorte de alcance",
     "10_Recorte_de_Alcance.docx",
     "De 257 a 156 actividades, contando la que el recorte añadió. El criterio: sobrevive lo "
     "que sirve a una medida de éxito de la carta sponsor. Se retiró la medida 8 por la "
     "ausencia del asesor terapéutico, y dos actividades más —DT.4 y DT.5— se recortaron el "
     "22 de octubre al revisar los enlaces que el recorte rompía."),
    ("18 de octubre de 2026", "Cambio del encuadre terapéutico",
     "11_Cambio_de_Enfoque.docx",
     "De herramienta de apoyo a la rehabilitación motriz a herramienta de regulación emocional "
     "por medio del ritmo. Cambia el encuadre, no el producto: el prototipo es el mismo."),
]

RESUMEN = [
    "El acta de constitución es el documento rector del proyecto y va por su versión 3.0. "
    "Contiene el objetivo, los entregables, la estructura de desglose del trabajo con sus 42 "
    "paquetes, el plan de recursos, el plan financiero, el plan de calidad y los criterios de "
    "terminación. Las versiones anteriores se conservan en entregables/superados/: no se "
    "reescribe encima del original.",

    f"La integración real del proyecto, sin embargo, no ocurrió en el acta sino en el control "
    f"de cambios. En trece días se tramitaron {len(CAMBIOS)} solicitudes formales que "
    "reorientaron el proyecto: la baja de un integrante, el recorte de alcance y el cambio del "
    "encuadre terapéutico. Ninguna se resolvió reescribiendo los documentos anteriores; las "
    "tres produjeron un documento nuevo que declara qué sustituye y por qué.",

    f"El avance vigente es de {HECHAS} de {VIGENTES} actividades, el "
    f"{100.0*HECHAS/VIGENTES:.0f} %. El estado consolidado vive en el documento 12, que existe "
    "precisamente porque once documentos correctos, cada uno escrito en su momento, no "
    "permiten a nadie reconstruir el proyecto leyéndolos en orden: tres de ellos reorientan lo "
    "que dicen los anteriores.",
]

PROCESOS = {
    "4.1": (
        "El acta se desarrolló y se revisó tres veces. La versión vigente, la 3.0, lleva "
        "control de documento con los cambios respecto de la 2.0 y de la 3.0 anterior, de modo "
        "que la evolución del proyecto se puede leer en el propio acta.",
        "02_Acta_Constitutiva.docx, sección «Control del documento» y «Cambios respecto de la "
        "versión 3.0»; versiones anteriores en entregables/superados/.",
    ),
    "4.2": (
        "El plan para la dirección del proyecto no es un documento único: son los planes "
        "subsidiarios de cada área, repartidos entre el acta —recursos, financiero, calidad— y "
        "los documentos 04 y 05 —costos, calidad y riesgos en detalle—. Esta carpeta de nueve "
        "documentos es su reorganización por área de conocimiento.",
        "02_Acta §4.9 a §4.11; 04_Planes_Costos_Calidad_Riesgos.docx; esta carpeta "
        "entregables/pmbok/.",
    ),
    "4.3": (
        "La dirección del trabajo se ejerció sobre artefactos consultables: el cronograma como "
        "plan único con porcentaje y evidencia por actividad, y el repositorio como registro "
        "técnico. Cada actividad cerrada lleva en sus notas qué la demuestra.",
        "Cronograma_Operativo.xml, con la nota de evidencia en cada actividad cerrada; "
        "historial de los dos repositorios.",
    ),
    "4.4": (
        "El conocimiento se gestionó escribiéndolo donde se usa y no en un documento aparte: "
        "una guía propia de ocho capítulos construida mientras se construía el prototipo, y la "
        "regla de que cada corrección explique la causa y el síntoma, no solo el cambio. Es lo "
        "que permite que un defecto no se diagnostique dos veces.",
        "entregables/guia/Guia_Bateria_VR_A.md; CLAUDE.md del repositorio, que acumula las "
        "lecciones y las reglas que no se negocian; README.md del repositorio Unity.",
    ),
    "4.5": (
        "El monitoreo comparó fuentes entre sí en vez de preguntar por el avance. Así se "
        "detectaron las dos divergencias del proyecto: la hoja de control 74 actividades por "
        "detrás del cronograma, y los dos cronogramas declarando avances distintos. Las dos se "
        "corrigieron con scripts que ahora tienen pruebas.",
        "scripts/validacion.py y scripts/sincronizar_crono.py con sus pruebas; "
        "12_Estado_del_Proyecto.docx.",
    ),
    "4.6": (
        f"Se ejecutaron {len(CAMBIOS)} solicitudes de cambio formales en trece días, cada una "
        "con su causa, su efecto y su lección. Ninguna reescribió el documento anterior: cada "
        "una declara qué sustituye, y el original se conserva.",
        "09_Respuesta_Riesgo_R14.docx, 10_Recorte_de_Alcance.docx y "
        "11_Cambio_de_Enfoque.docx.",
    ),
    "4.7": (
        "El cierre está en curso. Los instrumentos ya existen: la carta de validación de "
        "entregables y la lista de verificación de compromisos, ambas para firma. Lo que falta "
        "es la cadena de pruebas con usuarios e informe final, que es la única que todavía "
        "puede mover la fecha comprometida del 13 de noviembre.",
        "07_Carta_Validacion_Entregables.docx y 08_Lista_Verificacion_Compromisos.docx; "
        "Ruta_Critica_257_Tareas_v3.docx, cadena crítica QT.8 → QE.2 → QI.1 a QI.5 → QX.",
    ),
}

TABLAS = [
    ("Las tres solicitudes de cambio formales",
     ["Fecha", "Cambio", "Documento", "Efecto"],
     [[f, c, d, e] for f, c, d, e in CAMBIOS]),

    ("Por qué el proyecto cambió de encuadre",
     ["Motivo", "Detalle"],
     [[titulo, detalle] for titulo, detalle in enfoque.MOTIVOS]),

    ("Los documentos del proyecto, y qué responde cada uno",
     ["Documento", "Qué contiene"],
     [["01_Carta_Sponsor.docx", "Justificación, objetivo, las diez medidas de éxito y el "
       "presupuesto. Vigente con las sustituciones del 11."],
      ["02_Acta_Constitutiva.docx", "El documento rector: EDT de 42 paquetes con criterio de "
       "aceptación, responsable y duración. Vigente con las sustituciones del 11."],
      ["03_Ruta_Critica.docx", "La red PDM completa con su justificación."],
      ["04_Planes_Costos_Calidad_Riesgos.docx", "Planes de costos, calidad y riesgos, con los "
       "dos catálogos de pruebas y el registro de dieciocho riesgos."],
      ["05_Analisis_Costos_Calidad_Riesgos.docx", "El área 7 completa, de 7.1 a 7.4, incluido "
       "el valor ganado."],
      ["06_Entregable_Medio_Curso.docx", "El corte del 18 de septiembre: 117 actividades, "
       "SPI 0.969."],
      ["07_Carta_Validacion_Entregables.docx", "Instrumento de validación del alcance, para "
       "firma. Fechado el 21 de septiembre."],
      ["08_Lista_Verificacion_Compromisos.docx", "Lo comprometido contra lo entregado."],
      ["09_Respuesta_Riesgo_R14.docx", "La baja del integrante y la redistribución de su "
       "carga."],
      ["10_Recorte_de_Alcance.docx", "De 257 a 155 actividades, con la razón de cada recorte."],
      ["11_Cambio_de_Enfoque.docx", "Solicitud de cambio del marco terapéutico, PMBOK 4.6."],
      ["12_Estado_del_Proyecto.docx", "El estado vigente, los hitos alcanzados y el mapa de "
       "dónde está cada cosa."],
      ["Ruta_Critica_257_Tareas_v3.docx", "La ruta crítica recalculada sobre el alcance "
       "vigente, con las cuatro lecturas de la red."],
      ["Cronograma_Operativo.xml", "Las 155 actividades del alcance vigente. Es el que se "
       "trabaja."],
      ["Cronograma_ProjectLibre.xml", "Las 257 originales, con las recortadas marcadas. Es la "
       "evidencia de lo que se planeó."]]),

    ("Las diez áreas de conocimiento y su documento en esta carpeta",
     ["Área", "Documento"],
     [["4. Integración", "04_Integracion_Acta.docx — este documento"],
      ["5. Alcance", "05_Alcance.docx"],
      ["6. Cronograma", "SIN DOCUMENTO PROPIO. Cubierta por Cronograma_Operativo.xml, "
       "Cronograma_ProjectLibre.xml, 03_Ruta_Critica.docx y Ruta_Critica_257_Tareas_v3.docx."],
      ["7. Costos", "07_Costos.docx"],
      ["8. Calidad", "08_Calidad.docx"],
      ["9. Recursos", "09_Recursos.docx"],
      ["10. Comunicaciones", "10_Comunicaciones.docx"],
      ["11. Riesgos", "11_Riesgos.docx"],
      ["12. Adquisiciones", "12_Adquisiciones.docx"],
      ["13. Interesados", "13_Interesados.docx"]]),
]

LECCIONES = [
    ("Una decisión no registrada no obliga a nadie",
     f"El cambio de encuadre terapéutico se decidió {enfoque.FECHA_DECISION} y se registró el "
     f"{enfoque.FECHA_REGISTRO}: un mes después. Durante ese mes la carta sponsor afirmaba un "
     "marco que el equipo ya había abandonado, y cualquiera que cruzara los dos documentos "
     "habría encontrado la contradicción sin explicación. El control integrado de cambios no "
     "es burocracia: es lo que hace que una decisión sobreviva a que cambie quién la tomó."),

    ("No reescribir encima del original",
     "Las tres solicitudes de cambio produjeron un documento nuevo cada una, y los anteriores "
     "se conservan: la carta sponsor y el acta siguen diciendo lo que decían, con una nota de "
     "qué los sustituye. Es más trabajo que corregir el original, y es lo que permite "
     "responder «¿por qué cambió esto?» con un documento en vez de con una explicación oral. "
     "La misma regla se aplicó a las actividades recortadas, que se marcan y no se borran."),

    ("Doce documentos correctos no equivalen a un proyecto legible",
     "Cada uno de los once primeros documentos es correcto y sigue valiendo, pero tres de "
     "ellos reorientan lo que dicen los anteriores, así que nadie que llegue nuevo puede "
     "reconstruir el proyecto leyéndolos en orden. Por eso existe el documento 12, y por eso "
     "existe esta carpeta: la integración no termina al escribir los documentos, termina "
     "cuando alguien puede entrar por una puerta y encontrar lo que busca."),
]

REMITE_A = [
    ("entregables/02_Acta_Constitutiva.docx",
     "El documento rector completo: definición, organización, plan de implementación con la "
     "EDT y los 42 paquetes, consideraciones y apéndices."),
    ("entregables/12_Estado_del_Proyecto.docx",
     "El estado vigente consolidado, los doce hitos alcanzados y el mapa de qué documento "
     "responde cada cosa."),
    ("entregables/11_Cambio_de_Enfoque.docx",
     "La solicitud de cambio del encuadre terapéutico, con sus motivos, lo que no cambia y las "
     "renuncias que implica."),
    ("entregables/Ruta_Critica_257_Tareas_v3.docx",
     "La red recalculada sobre el alcance vigente y la cadena crítica que queda hasta el "
     "cierre."),
]
