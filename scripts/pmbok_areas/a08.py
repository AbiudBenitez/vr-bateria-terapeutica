# -*- coding: utf-8 -*-
"""
Área 8 — Calidad. El catálogo de casos se importa de pruebas.py.

LA CALIDAD DE ESTE PROYECTO SE MIDE, NO SE DECLARA. Cada medida de éxito tiene un número y un
criterio, y las que están cerradas lo están contra una medición en el visor: latencia p90 de
+4.07 ms, 12 946 de 12 949 fotogramas en vsync. Eso es lo que separa un plan de calidad de una
lista de buenas intenciones.
"""
import pruebas

AREA = "8"

PRUEBAS_UNITARIAS = 210      # EditMode, repositorio Unity, al 4-nov-2026

RESUMEN = [
    "La política de calidad del proyecto es que un criterio sin número no es un criterio. Las "
    "diez medidas de éxito de la carta sponsor llevan cada una su umbral verificable, y la "
    "verificación es una medición en el visor o una prueba automatizada, no una opinión del "
    "equipo.",

    f"La calidad se controla en tres niveles. {PRUEBAS_UNITARIAS} pruebas automatizadas de "
    f"EditMode corren sin abrir el editor y en dos minutos; "
    f"{len(pruebas.CAJA_BLANCA)} casos de caja blanca cubren decisiones y caminos del código; "
    f"y {len(pruebas.CAJA_NEGRA)} casos de caja negra prueban el comportamiento desde el punto "
    "de vista del usuario. Los tres niveles tienen criterios de entrada y de salida escritos.",

    "El hallazgo del área es que las pruebas de código no ven los defectos de montaje. Cinco "
    "pruebas con el visor de un solo día se fueron en cableado mal hecho, no en lógica mal "
    "escrita: referencias vacías, componentes duplicados, valores corregidos en el código que "
    "nunca llegaron a la escena. La respuesta fue un nivel de prueba nuevo que valida la "
    "escena guardada, y es el que más defectos ha cazado desde entonces.",
]

PROCESOS = {
    "8.1": (
        "Se planificó con política, objetivos y métricas de calidad, cada métrica atada a una "
        "medida de éxito de la carta sponsor y con su umbral. Se definieron los estándares "
        "aplicables y el costo de la calidad, y se declararon los roles de verificación.",
        "04_Planes, Parte II §5 a §12: política, objetivos, métricas, roles, estándares y "
        "costo de la calidad.",
    ),
    "8.2": (
        "La gestión de la calidad se ejerció sobre el proceso, no sobre el producto "
        "terminado: reglas de código que no se negocian —el reloj de audio como única fuente "
        "de tiempo, cero asignaciones de memoria en el camino del golpe—, y la obligación de "
        "que cada defecto corregido deje escrita la causa y cómo se detectó.",
        "04_Planes §10 gestionar la calidad; historial del repositorio Unity, donde cada "
        "corrección explica el defecto y su síntoma.",
    ),
    "8.3": (
        f"El control se ejecuta en tres niveles: {PRUEBAS_UNITARIAS} pruebas automatizadas, "
        f"{len(pruebas.CAJA_BLANCA)} casos de caja blanca y {len(pruebas.CAJA_NEGRA)} de caja "
        "negra, más las mediciones en el visor que cierran las medidas de éxito. Los defectos "
        "encontrados tienen un procedimiento de registro, clasificación y verificación de "
        "cierre.",
        "04_Planes, Parte III completa: estrategia, catálogos, calendario y gestión de los "
        "defectos; entregables/mediciones/ con los archivos de latencia y de fotogramas.",
    ),
}

TABLAS = [
    ("Casos de prueba de caja blanca",
     ["ID", "Técnica", "Qué cubre", "Criterio de aprobación", "Responsable"],
     [[c[0], c[1], c[2], c[4], c[5]] for c in pruebas.CAJA_BLANCA]),

    ("Casos de prueba de caja negra",
     ["ID", "Técnica", "Qué cubre", "Criterio de aprobación", "Responsable"],
     [[c[0], c[1], c[2], c[4], c[5]] for c in pruebas.CAJA_NEGRA]),

    ("Las mediciones que cierran una medida de éxito",
     ["Medida", "Umbral comprometido", "Medición obtenida"],
     [["4. Latencia golpe → sonido",
       "Entre −10 y +25 ms en el percentil 90, protocolo del clic físico",
       "p90 de +4.07 ms. Ocho corridas registradas el 17 de octubre."],
      ["5. Fotogramas sostenidos",
       "Menos del 5 % de vsync perdidos a 72 Hz",
       "12 946 de 12 949 fotogramas en vsync. 3 perdidos: 0.02 %."],
      ["9. Registro de métricas",
       "Precisión temporal y constancia del pulso por sesión",
       "31 sesiones volcadas a JSON con los desfases crudos. La mejor: 148 de 160 notas, "
       "desviación 24.5 ms, constancia 23.4 ms."],
      ["2. Detección del contacto",
       "El golpe se registra en el componente correcto en ≥95 % de los intentos",
       "84 golpes registrados sin una sola agenda de audio tardía."],
      ["6. Interacción intuitiva",
       "El usuario completa el tutorial sin ayuda externa",
       "El tutorial registra intentos y tiempo por paso: de 11 intentos a 6, y de 74 a 37 "
       "segundos entre la primera corrida y la última. Pendiente de recoger con usuarios "
       "reales en QT.8."]]),

    ("Niveles de control, y qué defecto caza cada uno",
     ["Nivel", "Cuántos", "Qué detecta", "Qué NO detecta"],
     [["Pruebas automatizadas de EditMode", str(PRUEBAS_UNITARIAS),
       "Lógica: juicio rítmico, conversión de tiempo musical, estadísticas de sesión, pasos "
       "del tutorial.",
       "Nada de lo que dependa de cómo está montada la escena."],
      ["Pruebas de la escena guardada", "incluidas en las anteriores",
       "Cableado: referencias vacías, componentes duplicados, valores afinados que no llegaron "
       "a la escena, pads que no conoce algún componente.",
       "Lo que solo se ve con el visor puesto: legibilidad, comodidad, mareo."],
      ["Caja blanca", str(len(pruebas.CAJA_BLANCA)),
       "Cobertura de decisiones y de caminos en el código de detección y de audio.",
       "El comportamiento percibido por el usuario."],
      ["Caja negra", str(len(pruebas.CAJA_NEGRA)),
       "Comportamiento desde el punto de vista del usuario, por particiones y valores límite.",
       "La causa de un fallo: dice que falla, no por qué."],
      ["Medición en el visor", "por medida de éxito",
       "Latencia, fotogramas, precisión rítmica: todo lo que tiene umbral numérico.",
       "Nada que no se haya decidido medir antes."]]),
]

LECCIONES = [
    ("Las pruebas de código no ven los defectos de montaje",
     "En un solo día, cinco pruebas con el visor se fueron en defectos de cableado y no de "
     "diseño: dos componentes arrancaban el tutorial a la vez, los pads del menú no tenían "
     "geometría, los tamaños de texto corregidos en el código nunca llegaron a la escena. "
     "Ninguna prueba existente podía verlos, porque viven en la lógica y esos defectos viven en "
     "la escena. Cada uno costaba compilar, instalar, ponerse el visor y volver. La respuesta "
     "fue un nivel de prueba que valida el montaje guardado en dos minutos de proceso por "
     "lotes, y es el que más defectos ha cazado desde entonces."),

    ("Cambiar un valor por defecto en el código no cambia lo que ya está en la escena",
     "Se aprendió dos veces. La primera con los tamaños de texto: tres correcciones seguidas "
     "no llegaron nunca y se pidieron tres pruebas en el visor de cambios que no existían. La "
     "segunda, un mes después, con los parámetros de un indicador visual: el código decía 0.60 "
     "segundos y la escena conservaba 0, de modo que el indicador recorría su camino en "
     "cincuenta milisegundos. La defensa que quedó es doble: el valor vive en una constante "
     "única, el cableador lo escribe en la escena, y una prueba comprueba que llegó."),

    ("Un criterio de calidad sin número no se puede incumplir ni cumplir",
     "La medida de éxito 4 dice «entre −10 y +25 ms en el percentil 90, con el protocolo del "
     "clic físico». Por eso se pudo cerrar con un dato y no con una impresión. Las medidas que "
     "siguen abiertas son exactamente las que dependen de personas —que nadie reporte "
     "molestias, que la interacción resulte intuitiva—, y para esas el instrumento es la prueba "
     "con usuarios, no una afirmación del equipo."),
]

REMITE_A = [
    ("entregables/04_Planes_Costos_Calidad_Riesgos.docx",
     "La Parte II con el plan de calidad completo y la Parte III con la estrategia de pruebas, "
     "los dos catálogos, el calendario de ejecución y la gestión de los defectos."),
    ("entregables/05_Analisis_Costos_Calidad_Riesgos.docx",
     "§11, el análisis del costo de la calidad."),
    ("entregables/mediciones/",
     "Los archivos crudos de cada medición: ocho corridas de latencia, la de fotogramas y las "
     "sesiones de juego con sus desfases."),
    ("scripts/pruebas.py",
     "Los dos catálogos de casos como única fuente de verdad, con su técnica, criterio, "
     "responsable y la actividad del cronograma que cierra cada uno."),
]
