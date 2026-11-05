# -*- coding: utf-8 -*-
"""
Área 11 — Riesgos. El registro completo se importa de pruebas.py.

EL IMPACTO SE MIDE EN DÍAS Y NO EN PESOS, y es la decisión que define el área. El proyecto no
compra ni contrata, así que ningún riesgo tiene impacto monetario: valorarlos en dinero habría
producido una columna de ceros. Se valoran en días hábiles y en degradación de alcance.

DOS DE LOS DIECIOCHO SE MATERIALIZARON. R14 y R18 no son hipótesis: uno ya ocurrió y el otro
sigue abierto a siete días del cierre. Eso es lo que convierte el registro en un instrumento
de dirección y no en un anexo.
"""
import pruebas

AREA = "11"

MATERIALIZADOS = {
    "R14": "Un integrante dio de baja la materia el 6 de octubre. La respuesta estaba escrita "
           "antes: redistribuir y recortar, no reemplazar.",
    "R15": "La hoja de control del equipo quedó 74 actividades por detrás del cronograma. La "
           "respuesta prevista —que la gerencia verifique contra el repositorio— se ejecutó.",
}

RESUMEN = [
    f"El registro tiene {len(pruebas.RIESGOS)} riesgos, cada uno con probabilidad, impacto en "
    "días, categoría, estrategia, responsable, disparador y respuesta planificada. El valor "
    f"monetario esperado agregado es de {pruebas.EMV_DIAS:.2f} días hábiles, de los cuales "
    f"{pruebas.EMV_RESERVA:.2f} consumirían reserva de cronograma: tres riesgos "
    f"—{', '.join(sorted(pruebas.ABSORBIDOS))}— se absorben sin tocarla.",

    "El impacto se mide en días hábiles y no en pesos porque el proyecto no compra ni "
    "contrata: visores prestados, licencias libres y mano de obra de practicantes bajo "
    "convenio escolar. Un registro con el impacto en dinero habría tenido dieciocho ceros en "
    "esa columna y no habría servido para decidir nada.",

    "Dos riesgos se materializaron. El R14 —la baja de un integrante— ocurrió el 6 de octubre, "
    "y su respuesta estaba redactada antes de necesitarla, lo que convirtió una baja en una "
    "tarde de reasignación en vez de una semana de decidir qué hacer. El R15 —un integrante no "
    "reporta y el cronograma queda ciego— se materializó como un desfase de 74 actividades "
    "entre la hoja del equipo y el cronograma. Y el R18, los usuarios para las pruebas, sigue "
    "abierto: es hoy el único que puede mover la fecha final.",
]

PROCESOS = {
    "11.1": (
        "Se definió la metodología con una decisión que gobierna todo el área: el impacto se "
        "valora en días hábiles y en degradación de alcance, no en dinero, porque el proyecto "
        "no tiene desembolsos. Se fijaron escalas de probabilidad e impacto y umbrales de "
        "acción.",
        "04_Planes, Parte IV §18 metodología y §19 escalas de valoración, con los umbrales.",
    ),
    "11.2": (
        f"Se identificaron {len(pruebas.RIESGOS)} riesgos en "
        f"{len(pruebas.CATEGORIAS)} categorías: técnicos, de cronograma, de recursos, "
        "externos, de herramientas y de equipo. La identificación incluyó riesgos de proceso "
        "que no suelen aparecer, como la corrupción del archivo del cronograma por la propia "
        "herramienta, que después resultó real.",
        "04_Planes §20 categorías y §21 registro de riesgos; scripts/pruebas.py, lista "
        "RIESGOS.",
    ),
    "11.3": (
        "Cada riesgo se calificó con probabilidad e impacto y se ubicó en la matriz de "
        "probabilidad e impacto, que es la que ordena la atención. El análisis cualitativo es "
        "el que separó los tres riesgos que se absorben sin tocar reserva de los que la "
        "consumen.",
        "05_Analisis §12.2 escalas y §12.4 matriz de probabilidad e impacto.",
    ),
    "11.4": (
        f"El análisis cuantitativo da un valor esperado agregado de {pruebas.EMV_DIAS:.2f} "
        f"días, y {pruebas.EMV_RESERVA:.2f} si se descuentan los absorbidos. El documento 04 "
        "concluye que la reserva es insuficiente y dice qué hacer al respecto, en vez de "
        "ajustar el número hasta que cuadrara.",
        "05_Analisis §12.3 análisis cuantitativo; 04_Planes §22 suficiencia de la reserva, "
        "incluido §22.2 «la reserva es insuficiente, y qué hacer al respecto».",
    ),
    "11.5": (
        f"Los {len(pruebas.RIESGOS)} riesgos tienen respuesta planificada con estrategia "
        "—mitigar, evitar, transferir o aceptar—, responsable nombrado y disparador explícito: "
        "la condición concreta que activa la respuesta, para que no dependa del criterio de "
        "quien esté mirando.",
        "04_Planes §23 respuestas a los riesgos, R1 a R18, cada una con su disparador.",
    ),
    "11.6": (
        "Se implementaron dos respuestas. La del R14 produjo un documento propio y una "
        "redistribución completa de la carga. La del R15 convirtió el reporte de avance en una "
        "verificación contra el repositorio, que es lo que después detectó el desfase.",
        "09_Respuesta_Riesgo_R14.docx; 04_Planes §24 implementar la respuesta, con la regla de "
        "activación y el registro de ejecución.",
    ),
    "11.7": (
        "El monitoreo se hizo por indicadores y por cierre explícito de riesgos, no por "
        "revisión general. Riesgos como el R1 de latencia se cerraron con una medición: p90 de "
        "+4.07 ms contra una ventana de −10 a +25 ms. El R18 sigue declarado como vivo en el "
        "documento de estado.",
        "04_Planes §25 monitorear los riesgos, con el cierre y los indicadores; "
        "12_Estado_del_Proyecto.docx, sección de riesgos vivos.",
    ),
}

TABLAS = [
    ("Registro de riesgos",
     ["ID", "Riesgo", "Prob.", "Impacto (días)", "Categoría", "Estrategia", "Responsable"],
     [[r[0], r[1], f"{float(r[2]):.2f}", f"{float(r[3]):.1f}", r[5], r[6], r[7]]
      for r in pruebas.RIESGOS]),

    ("Riesgos que se materializaron, y qué pasó",
     ["ID", "Qué ocurrió"],
     [[rid, texto] for rid, texto in MATERIALIZADOS.items()]),

    ("Por qué el impacto va en días y no en pesos",
     ["Concepto", "Situación del proyecto"],
     [["Compras", "Ninguna. El presupuesto es mano de obra en su totalidad."],
      ["Contrataciones", "Una prevista —el asesor terapéutico— que no se concretó."],
      ["Equipo", "Visores en préstamo, computadoras propias de los integrantes."],
      ["Licencias", "Gratuitas o libres."],
      ["Consecuencia", "Ningún riesgo tiene impacto monetario. El impacto que un riesgo "
       "produce en este proyecto es retraso o pérdida de alcance, y así se valora."],
      ["Reserva", "De cronograma, en días hábiles. No hay reserva monetaria porque no hay "
       "nada que comprar con ella."]]),
]

LECCIONES = [
    ("Tener la respuesta escrita antes convierte una crisis en una tarde de trabajo",
     "El R14 —un integrante abandona el equipo— estaba en el registro con su respuesta ya "
     "redactada: redistribuir y recortar, no reemplazar. Cuando ocurrió, el 6 de octubre, no "
     "hubo que decidir qué hacer: hubo que ejecutarlo. Sin ese registro, la misma baja habría "
     "costado una semana de deliberación en un proyecto que ya iba justo. Es el argumento más "
     "fuerte que este proyecto puede dar a favor de gestionar riesgos por escrito."),

    ("Un riesgo que se baja de nivel por una gestión en curso sigue siendo alto",
     "El riesgo del asesor terapéutico se bajó de alto a medio porque el líder tenía un "
     "contacto identificado. Eso no era un acuerdo, y la diferencia solo se vio cuando venció "
     "la fecha límite del 10 de septiembre. El resultado fue retirar una medida de éxito. Un "
     "riesgo de dependencia externa se cierra cuando la contraparte se compromete, no cuando "
     "se la encuentra."),

    ("El registro acertó en un riesgo que parecía paranoia",
     "El R10 preveía que ProjectLibre dejara de abrir o corrompiera el archivo del cronograma. "
     "Parecía exagerado y resultó estructural: la herramienta deriva el porcentaje de la "
     "duración, así que los hitos de duración cero vuelven a cero solos cada vez que alguien "
     "abre y guarda. Costó tres sustos antes de entenderlo, y la respuesta fue un script "
     "guardián que anota el estado bueno y restaura los que caen."),
]

REMITE_A = [
    ("entregables/04_Planes_Costos_Calidad_Riesgos.docx",
     "La Parte IV completa: metodología, escalas, categorías, el registro con las dieciocho "
     "respuestas y sus disparadores, la suficiencia de la reserva y el monitoreo."),
    ("entregables/05_Analisis_Costos_Calidad_Riesgos.docx",
     "§12: el análisis cuantitativo, la matriz de probabilidad e impacto y el cálculo de "
     "suficiencia de la reserva."),
    ("entregables/09_Respuesta_Riesgo_R14.docx",
     "La implementación completa de la respuesta al único riesgo de equipo que se "
     "materializó."),
    ("entregables/12_Estado_del_Proyecto.docx",
     "Los riesgos vivos al cierre, con su nivel y su mitigación."),
    ("scripts/pruebas.py",
     "El registro de riesgos como única fuente de verdad, con el cálculo del valor esperado."),
]
