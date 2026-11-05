# -*- coding: utf-8 -*-
"""
Área 10 — Comunicaciones. La única área sin ningún dato previo en el repositorio.

SE DOCUMENTA LO VERIFICABLE Y SE DECLARA EL HUECO. Los canales que dejan rastro se pueden
describir con precisión porque están ahí: commits, porcentajes del cronograma, documentos
fechados. La cadencia de la comunicación interna no existe en ninguna parte, y escribir un
plan con reuniones semanales y matriz de escalamiento describiría prácticas que el equipo no
tuvo. A siete días del cierre tampoco podría empezar a cumplirlas.

La evidencia de que la informalidad costó algo es medible: 74 actividades terminadas que la
hoja de control del equipo no reflejaba. Eso es el riesgo R15 materializado.
"""

AREA = "10"

# La hoja de control del equipo contra el cronograma. Lo calcula validacion.resumen().
DESFASE_HOJA = 74

RESUMEN = [
    "La comunicación del proyecto se apoyó en artefactos, no en reuniones. Cada canal que el "
    "proyecto usó de verdad deja un rastro consultable: el repositorio registra el avance "
    "técnico commit por commit, el cronograma es el plan único con los porcentajes, los doce "
    "documentos son el canal formal con la patrocinadora, y la traza en archivo es el único "
    "canal por el que un fallo en el visor llega al equipo.",

    "La comunicación interna, en cambio, fue informal y sin cadencia fija. Este documento lo "
    "declara en vez de inventar un plan: no hubo periodicidad establecida de reportes, ni "
    "convocante designado, ni ruta de escalamiento escrita. El avance se reportaba cuando "
    "alguien preguntaba.",

    f"Eso tuvo un costo medible. La hoja de control del equipo quedó desincronizada del "
    f"cronograma en {DESFASE_HOJA} actividades terminadas y verificables: trabajo hecho que el "
    "registro del equipo no reflejaba. No es un defecto de herramienta —las dos fuentes "
    "funcionaban— sino de comunicación, y es exactamente lo que el riesgo R15 describía: un "
    "integrante que no reporta deja el cronograma ciego.",
]

PROCESOS = {
    "10.1": (
        "No se redactó un plan de comunicaciones al inicio. Los canales se establecieron por "
        "uso y quedaron estabilizados: seis canales con rastro, cada uno con un propietario "
        "de hecho. Este documento los formaliza a posteriori, que es cuando se pudieron "
        "describir con precisión.",
        "Tabla de canales de este documento, con el artefacto consultable de cada uno.",
    ),
    "10.2": (
        "La comunicación con la patrocinadora se ejecutó por documentos fechados y firmados: "
        "doce entregables, tres de ellos solicitudes de cambio formales. La comunicación "
        "técnica interna se ejecutó por el repositorio, con mensajes de commit que explican la "
        "causa y no solo el cambio.",
        "Los doce documentos de entregables/; el historial del repositorio Unity y del "
        "repositorio de documentación.",
    ),
    "10.3": (
        f"El seguimiento se hizo comparando fuentes entre sí, no preguntando. Así se detectó "
        f"el desfase de {DESFASE_HOJA} actividades entre la hoja del equipo y el cronograma, y "
        "así se detectó que los dos cronogramas declaraban avances distintos. Ambos se "
        "corrigieron con scripts que ahora tienen pruebas y vigilan la divergencia.",
        "scripts/validacion.py, que calcula el desfase; scripts/sincronizar_crono.py y sus "
        "seis pruebas, que impiden que los dos cronogramas vuelvan a separarse.",
    ),
}

TABLAS = [
    ("Los canales que el proyecto usó, y qué rastro deja cada uno",
     ["Canal", "Para qué", "Qué rastro deja", "Quién lo mantiene"],
     [
         ["Repositorio git (dos repos)",
          "Avance técnico y la razón de cada cambio",
          "Un commit por cambio, con el defecto que corrige y cómo se detectó",
          "Gerencia de proyecto"],
         ["Cronograma en ProjectLibre",
          "Plan único: fechas, dependencias, porcentajes y evidencia por actividad",
          "Porcentaje y nota de evidencia en cada una de las 155 actividades vigentes",
          "Gerencia de proyecto"],
         ["Hoja de control del equipo",
          "Reporte de avance de cada integrante",
          "Estado declarado por responsable",
          "Coordinación"],
         ["Los doce documentos entregables",
          "Canal formal con la patrocinadora",
          "Documentos fechados, con línea de firma y control de versiones",
          "Gerencia y QA"],
         ["Traza en archivo del visor",
          "Fallos que ocurren con el visor puesto",
          "Archivo de texto que se recoge con quest.sh pull",
          "Desarrollo VR"],
         ["Revisión semanal en clase",
          "Validación con la docente y solicitudes de cambio",
          "Las propias solicitudes de cambio cuando se formalizan",
          "Dirección de proyecto"],
     ]),

    ("Requisitos de información por interesado",
     ["Interesado", "Qué necesita saber", "Por qué canal", "Cuándo"],
     [
         ["Patrocinadora y docente",
          "Avance contra lo comprometido, y toda desviación de alcance o de enfoque",
          "Documentos entregables y revisión en clase",
          "En cada entrega, y de forma inmediata ante un cambio de alcance"],
         ["Equipo de desarrollo",
          "Qué está hecho, qué está roto y qué bloquea a quién",
          "Repositorio y cronograma",
          "Continuo: cada commit y cada marcado de actividad"],
         ["Coordinación",
          "Quién va retrasado y contra qué compromiso",
          "Hoja de control y cronograma",
          "Al cierre de cada actividad"],
         ["Usuarios de prueba",
          "Qué se les pide hacer y para qué se usan sus datos",
          "Guion de la prueba QT.8 y manual de usuario",
          "Antes de cada sesión de prueba"],
     ]),

    ("Lo que NO hubo, declarado explícitamente",
     ["Práctica que el PMBOK espera", "Estado en este proyecto"],
     [
         ["Plan de comunicaciones redactado al inicio",
          "No existió. Los canales se establecieron por uso."],
         ["Cadencia fija de reuniones de equipo",
          "No existió. No hubo periodicidad establecida ni convocante designado."],
         ["Matriz de escalamiento de bloqueos",
          "No existió. Los bloqueos se resolvieron por contacto directo."],
         ["Informes de desempeño periódicos",
          "No existieron como informe. El corte de medio curso y el documento 12 son los dos "
          "únicos puntos en que el avance se consolidó por escrito."],
         ["Registro de incidencias de comunicación",
          f"No existió en su momento. El desfase de {DESFASE_HOJA} actividades se detectó "
          "comparando fuentes, no por reporte."],
     ]),
]

LECCIONES = [
    ("Sin cadencia fija, el avance se reporta cuando alguien pregunta",
     f"La hoja de control del equipo quedó {DESFASE_HOJA} actividades por detrás del "
     "cronograma. Ninguna de las dos herramientas falló: lo que faltó fue el hábito de "
     "actualizar. El riesgo R15 lo había previsto con esas palabras —«un integrante no reporta "
     "su avance y el cronograma queda ciego»— y la respuesta planificada era que la gerencia "
     "verificara contra el repositorio, que es exactamente lo que acabó pasando. Funcionó, "
     "pero convirtió la comunicación en una auditoría en vez de un reporte."),

    ("Una cifra que vive en dos sitios acaba diciendo dos cosas",
     "Durante dos semanas el cronograma operativo declaraba un 83 % de avance y el de "
     "ProjectLibre un 59 %, porque cada uno se marcaba a mano por separado. Las dos cifras "
     "eran defendibles y ninguna era la misma. Se resolvió con un script que sincroniza el "
     "avance y seis pruebas que fallan si vuelven a separarse. La lección no es sobre "
     "herramientas: cualquier dato que dos personas mantengan por separado divergirá, y la "
     "única defensa es que una de las dos copias se genere de la otra."),

    ("Un canal de diagnóstico que no se puede leer no es un canal",
     "Durante semanas el equipo creyó que los mensajes de diagnóstico del visor se podían leer "
     "con adb logcat. No se podían: se verificó contra 293 líneas de registro sin una sola "
     "entrada de Unity, y las excepciones comparten ese mismo canal invisible. Cada hipótesis "
     "sobre un fallo costaba compilar, instalar, ponerse el visor y volver sin información. "
     "Hasta que el canal se sustituyó por un archivo, el equipo estaba comunicándose con un "
     "destinatario que no recibía nada."),
]

REMITE_A = [
    ("entregables/12_Estado_del_Proyecto.docx",
     "El estado vigente consolidado y el mapa de qué documento responde cada cosa: es el "
     "artefacto de comunicación que reúne lo que los once anteriores dispersan."),
    ("entregables/04_Planes_Costos_Calidad_Riesgos.docx",
     "El riesgo R15 con su respuesta planificada, y el R17 sobre cambios solicitados por la "
     "docente."),
    ("scripts/validacion.py",
     f"El cálculo del desfase de {DESFASE_HOJA} actividades entre la hoja de control y el "
     "cronograma."),
]
