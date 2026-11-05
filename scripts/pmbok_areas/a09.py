# -*- coding: utf-8 -*-
"""
Área 9 — Recursos.

LAS TARIFAS Y EL ESFUERZO SE IMPORTAN DE costos.py, no se recopian. Es el mismo módulo que
alimentó el 04 y el 05, así que la escala de perfiles, el esfuerzo y el presupuesto de este
documento no pueden decir algo distinto de lo que dicen aquellos.

EL DATO MÁS ELOCUENTE DEL ÁREA ESTÁ EN EL PROPIO CRONOGRAMA: Diana figura como SEIS recursos
distintos —directora, gerente, QA, analista, redactora y desarrolladora de realidad virtual—.
No es un error de captura: es la concentración que dejaron el riesgo R3 y la baja del R14,
visible en el archivo sin necesidad de interpretarlo.
"""
import costos

AREA = "9"

# Los seis roles con que una sola persona figura en Cronograma_Operativo.xml.
ROLES_DIANA = [
    "Director de proyecto",
    "Gerente de proyecto",
    "Analista de pruebas (QA)",
    "Analista e investigador",
    "Redactor técnico",
    "Desarrollador de realidad virtual",
]

RESUMEN = [
    "El equipo son practicantes bajo convenio escolar, no empleados, y de ahí sale toda la "
    f"gestión de recursos del proyecto. La tarifa se ancla al salario mínimo nominal "
    f"—${costos.SM_DIARIO:,.2f} diarios entre {costos.HDIA} horas = ${costos.SM_HORA}/h, que "
    "se toma como 1 SM— y cada perfil es un múltiplo de esa unidad según su responsabilidad, "
    "de 1.0 para el redactor técnico a 2.2 para la dirección.",

    f"El esfuerzo total es de {costos.HORAS_TOT:,.0f} horas y la mano de obra "
    f"${costos.MANO_OBRA:,.0f}, con una tarifa media de ${costos.TARIFA_MED:.2f}/h, es decir "
    f"{costos.TARIFA_MED/costos.SM_HORA:.2f} SM. El proyecto no tiene costos no laborales: los "
    "visores son prestados, las licencias libres y Unity gratuito. Los recursos físicos son "
    "dos visores Meta Quest y los equipos de cómputo de los integrantes.",

    "La gestión real del área, sin embargo, no fue la asignación inicial sino la "
    "redistribución. La baja de un integrante activó el riesgo R14 y dejó la dirección y la "
    "coordinación sin titular; esa carga se absorbió dentro de QA. El resultado es verificable "
    f"en el cronograma: una sola persona figura como {len(ROLES_DIANA)} recursos distintos.",
]

PROCESOS = {
    "9.1": (
        "Se definió una escala de tarifas por responsabilidad, anclada al salario mínimo "
        "nominal y con la justificación escrita de cada múltiplo. Se documentó además qué "
        "recursos no cuestan y por qué, para que el presupuesto no tuviera partidas "
        "inventadas.",
        "scripts/costos.py, diccionario PERFIL_BASE con el múltiplo y la razón de cada "
        "perfil; acta constitutiva §4.9 plan de recursos y §4.10.3 recursos que no cuestan.",
    ),
    "9.2": (
        "La estimación se hizo actividad por actividad, en horas, y se agregó de forma "
        f"ascendente: {costos.HORAS_TOT:,.0f} horas en total. El perfil se asignó por grupo de "
        "actividades, no por persona, de modo que la estimación no cambia si cambia quién "
        "ejecuta.",
        "05_Analisis_Costos_Calidad_Riesgos.docx, §5 matriz de tiempos y §6 asignación de "
        "perfil; anexo A con el costeo de las 257 actividades.",
    ),
    "9.3": (
        "No hubo adquisición de recursos humanos: el equipo lo determina la inscripción a la "
        "materia. Los recursos físicos se obtuvieron en préstamo de la Facultad —dos visores, "
        "para que las pruebas de dos integrantes no se bloqueen entre sí— y el software por "
        "licencia gratuita o libre.",
        "Área 12 de adquisiciones, tabla de acuerdos vigentes; riesgo R5 sobre el préstamo de "
        "los visores en 04_Planes.",
    ),
    "9.4": (
        "El equipo no tenía experiencia previa en Unity, y eso determinó la elección del "
        "motor. El instrumento de desarrollo de capacidades fue una guía propia de ocho "
        "capítulos, construida mientras se construía el prototipo, de modo que el "
        "conocimiento quedara en el repositorio y no solo en quien lo ejecutó.",
        "entregables/guia/Guia_Bateria_VR_A.md, ocho capítulos; decisión del motor registrada "
        "en el acta con la comparación contra Unreal.",
    ),
    "9.5": (
        "La dirección del equipo se ejerció sobre la carga, no sobre las personas: ante la "
        "baja del R14 se redistribuyó y se recortó en vez de reemplazar, porque la respuesta "
        "estaba escrita antes de necesitarla. También se rebalanceó el paquete 3.3, que pasó "
        "del artista 3D al diseñador UX-XR para sacar la rama 3D de la ruta crítica.",
        "09_Respuesta_Riesgo_R14.docx; acta constitutiva §4.9.1 nota sobre la reasignación del "
        "paquete 3.3.",
    ),
    "9.6": (
        "El control detectó sobreasignación en 7 de las 8 áreas y un límite real por carga de "
        "70.9 días contra una red de 38.25, con una persona al 157 %. La respuesta fue el "
        "recorte de alcance: se redujo el trabajo en vez de suponer que la gente rendiría más.",
        "Ruta_Critica_257_Tareas_v3.docx, análisis de carga; 10_Recorte_de_Alcance.docx, que "
        "es la respuesta ejecutada.",
    ),
}

TABLAS = [
    ("Escala de tarifas por responsabilidad",
     ["Perfil", "Múltiplo del SM", "Tarifa por hora", "Por qué ese múltiplo"],
     [[p, f"{m:.1f}", f"${costos.PERFIL[p][0]:,.2f}", razon]
      for p, (m, razon) in costos.PERFIL_BASE.items()]),

    ("Recursos del cronograma",
     ["Recurso", "Tarifa por hora"],
     [["Benjamín — Desarrollador de gameplay", "$59.07"],
      ["Misael — Desarrollador de realidad virtual", "$59.07"],
      ["Kimberly — Artista y modelador 3D", "$51.19"],
      ["Sarai — Diseñador de interacción UX-XR", "$51.19"],
      ["María — Analista e investigador", "$51.19"],
      ["Javier — Compositor y diseñador musical", "$47.26"],
      ["Christian — Diseñador de audio", "$47.26"],
      ["Diana — Director de proyecto", "$86.64"],
      ["Diana — Gerente de proyecto", "$70.88"],
      ["Diana — Desarrollador de realidad virtual", "$59.07"],
      ["Diana — Analista e investigador", "$51.19"],
      ["Diana — Analista de pruebas (QA)", "$43.32"],
      ["Diana — Redactor técnico", "$39.38"]]),

    ("Recursos que no cuestan, y por qué",
     ["Recurso", "Régimen", "Efecto en el presupuesto"],
     [["Dos visores Meta Quest 3 y 3S", "Préstamo de la Facultad",
       "Ninguno. Habría sido la mayor partida de compra del proyecto."],
      ["Unity 6000.5.10f1", "Licencia Personal gratuita",
       "Ninguno. El proyecto no alcanza el umbral de ingresos que obliga a Pro."],
      ["Kit de batería, música y assets del entorno", "Creative Commons",
       "Ninguno. Obligan a atribuir, no a pagar."],
      ["Equipos de cómputo de los integrantes", "Propiedad de cada integrante",
       "Ninguno. Es también el riesgo R12: una falla no tiene reemplazo presupuestado."],
      ["Servidor o backend", "No se usa",
       "Ninguno. La aplicación es autónoma y las métricas van a archivos en el visor."]]),
]

LECCIONES = [
    ("Anclar la tarifa a una fuente oficial, y no estimarla",
     "El presupuesto se calculó tres veces. La primera dio $559,891 con tarifas de mercado sin "
     "fuente y compras que el proyecto no iba a hacer; la segunda $294,981 con datos del "
     "Observatorio Laboral; la vigente da "
     f"${costos.MANO_OBRA:,.0f} anclando la tarifa al salario mínimo nominal publicado por la "
     "CONASAMI y reconociendo que el equipo son practicantes, no empleados. Cada corrección "
     "acercó la estimación a lo que el proyecto realmente es. La regla que quedó: no estimar "
     "tarifas sin fuente oficial."),

    ("El error de dividir el salario mensual entre 173.33 horas",
     "Hacerlo da $55.25 por hora en vez de $39.38, y parece más preciso. No lo es: ese número "
     "es el costo patronal de un trabajador de planta que cobra los días de descanso. Un "
     "practicante bajo convenio escolar no los cobra, así que la división correcta es el "
     f"salario diario entre {costos.HDIA} horas trabajadas. La diferencia inflaba el "
     "presupuesto un 40 % sin que nada en la hoja de cálculo pareciera mal."),

    ("Una persona con seis roles no es versatilidad, es un punto único de falla",
     f"En el cronograma Diana figura como {len(ROLES_DIANA)} recursos distintos: "
     f"{', '.join(ROLES_DIANA[:3]).lower()} y tres más. No fue una decisión de diseño: es lo "
     "que quedó cuando la baja del R14 dejó la dirección y la coordinación sin titular y esa "
     "carga cayó dentro de QA, que ya era el área más cargada. El control de recursos lo "
     "detectó como un 157 % de asignación, y la única respuesta honesta fue recortar alcance: "
     "redistribuir otra vez habría sido mover el problema de sitio."),
]

REMITE_A = [
    ("entregables/05_Analisis_Costos_Calidad_Riesgos.docx",
     "La matriz de tiempos completa, la asignación de perfil por grupo de actividades y el "
     "anexo A con el costeo de las 257 actividades."),
    ("entregables/02_Acta_Constitutiva.docx",
     "§3.2 roles y responsabilidades, §3.3 perfiles requeridos, §4.9 plan de recursos y el "
     "anexo A con la asignación nominal por paquete."),
    ("entregables/Ruta_Critica_257_Tareas_v3.docx",
     "El análisis de carga por persona y el límite real impuesto por la sobreasignación."),
    ("entregables/09_Respuesta_Riesgo_R14.docx",
     "La redistribución completa de la carga del integrante dado de baja."),
    ("scripts/costos.py",
     "La escala de perfiles con la justificación de cada múltiplo, y el cálculo del esfuerzo y "
     "de la mano de obra."),
]
