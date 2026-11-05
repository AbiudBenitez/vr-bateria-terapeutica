# -*- coding: utf-8 -*-
"""
Área 13 — Interesados.

DOS INTERESADOS DECIDIERON EL PROYECTO Y NINGUNO ESTABA EN EL EQUIPO. La patrocinadora, por
la vía de las diez medidas de éxito que comprometió la carta sponsor; y el asesor terapéutico,
por su ausencia, que retiró una de esas diez. Un registro de interesados que solo listara al
equipo no explicaría ninguna de las dos cosas.
"""

AREA = "13"

RESUMEN = [
    "El proyecto tiene una patrocinadora con poder y con interés altos a la vez —la docente de "
    "la materia, que es quien define el criterio de aceptación y quien lo evalúa— y eso "
    "determina casi toda la gestión del área: las diez medidas de éxito de la carta sponsor "
    "son el acuerdo con ella, y cada desviación respecto de ellas se tramitó por escrito.",

    "El interesado más consecuente, sin embargo, fue el que nunca llegó. El asesor terapéutico "
    "era la única validación externa prevista, tenía fecha límite el 10 de septiembre y no se "
    "concretó. Sin dictamen clínico la medida de éxito 8 no se podía verificar por ningún "
    "camino, así que se retiró formalmente y el proyecto cambió de encuadre: de herramienta de "
    "apoyo a la rehabilitación motriz a herramienta de regulación emocional por medio del "
    "ritmo. Un interesado ausente reescribió el alcance.",

    "Queda un grupo de interesados sin asegurar a siete días del cierre: los usuarios de las "
    "pruebas QT.8. Es el riesgo R18 y es el único que todavía puede mover la fecha final, "
    "porque el informe completo depende de esas pruebas.",
]

PROCESOS = {
    "13.1": (
        "Se identificaron ocho grupos de interesados, incluidos dos que no son personas del "
        "equipo ni de la Facultad: los usuarios de prueba, que todavía no están reclutados, y "
        "los usuarios finales potenciales, que no participan pero cuyo beneficio es el que "
        "justifica el proyecto.",
        "Acta constitutiva §3.1 «Clientes y partes intervinientes»; registro de interesados de "
        "este documento.",
    ),
    "13.2": (
        "La estrategia se fijó por cuadrante de poder e interés. Con la patrocinadora: gestión "
        "estrecha por documento formal, nunca verbal, para toda desviación de alcance. Con la "
        "Facultad: mantener satisfecha, su única exigencia es la devolución de los visores. "
        "Con el equipo: informar de forma continua por artefactos consultables.",
        "Matriz de poder e interés y tabla de estrategia de este documento.",
    ),
    "13.3": (
        "Con la patrocinadora se ejecutó por tres solicitudes de cambio formales: la respuesta "
        "al riesgo R14 por la baja de un integrante, el recorte de alcance de 257 a 155 "
        "actividades, y el cambio de encuadre terapéutico. Las tres están redactadas y "
        "esperan firma.",
        "09_Respuesta_Riesgo_R14.docx, 10_Recorte_de_Alcance.docx y "
        "11_Cambio_de_Enfoque.docx.",
    ),
    "13.4": (
        "El involucramiento se monitoreó por el estado de los acuerdos, no por percepción. El "
        "indicador que falló fue el del asesor: se bajó su riesgo de alto a medio por tener un "
        "contacto identificado, y eso no era un acuerdo. El de los usuarios de prueba sigue "
        "abierto y declarado como riesgo vivo.",
        "Registro de riesgos R5, R7, R14 y R18 en 04_Planes; sección de riesgos vivos de "
        "12_Estado_del_Proyecto.docx.",
    ),
}

TABLAS = [
    ("Registro de interesados",
     ["Interesado", "Rol respecto del proyecto", "Poder", "Interés", "Expectativa principal"],
     [
         ["Dra. Leticia Amalia Neira Tovar",
          "Patrocinadora y docente de la materia. Define y evalúa el criterio de aceptación.",
          "Alto", "Alto",
          "Documentación conforme a PMBOK y un prototipo demostrable validado con usuarios."],
         ["Equipo A (7 integrantes activos)",
          "Ejecutan el proyecto. Eran 8 hasta la baja que activó el riesgo R14.",
          "Medio", "Alto",
          "Acreditar la materia con trabajo defendible y verificable."],
         ["FIME, UANL",
          "Presta los dos visores Meta Quest. No participa en el desarrollo.",
          "Medio", "Bajo",
          "Devolución del equipo prestado en buen estado al cierre."],
         ["Usuarios de las pruebas (QT.8)",
          "Validan el prototipo. NO RECLUTADOS al 4 de noviembre.",
          "Bajo", "Alto",
          "Una sesión corta, cómoda y sin molestias atribuibles al uso."],
         ["Asesor terapéutico externo",
          "Validación clínica prevista. NUNCA SE CONCRETÓ.",
          "Alto", "Bajo",
          "No llegó a expresar ninguna. Su ausencia retiró la medida de éxito 8."],
         ["Integrante que dio de baja la materia",
          "Era director de proyecto. Su salida activó el riesgo R14.",
          "Bajo", "Bajo",
          "Sin expectativa vigente. Su carga se redistribuyó dentro de QA."],
         ["Autores de los assets de licencia libre",
          "No participan. Imponen obligaciones por licencia.",
          "Bajo", "Bajo",
          "Atribución correcta, y que no se redistribuya lo que su licencia no permite."],
         ["Usuarios finales potenciales",
          "No participan en el proyecto. Son el beneficiario que lo justifica.",
          "Bajo", "Alto",
          "Una herramienta que sirva para regular el estado emocional por medio del ritmo."],
     ]),

    ("Matriz de poder e interés, y estrategia por cuadrante",
     ["Cuadrante", "Quién", "Estrategia", "Cómo se ejecutó"],
     [
         ["Poder alto, interés alto — gestionar de cerca",
          "Patrocinadora",
          "Documento formal para toda desviación de alcance, enfoque o entregable. Nunca "
          "verbal.",
          "Tres solicitudes de cambio por escrito: R14, recorte de alcance y cambio de "
          "enfoque."],
         ["Poder alto, interés bajo — mantener satisfecho",
          "Asesor terapéutico (previsto), FIME",
          "Contacto puntual, con un compromiso concreto y una fecha.",
          "Con FIME funcionó. Con el asesor falló: hubo contacto pero no compromiso."],
         ["Poder bajo, interés alto — mantener informado",
          "Equipo, usuarios de prueba, usuarios finales",
          "Artefactos consultables en vez de reportes: repositorio y cronograma.",
          "Ejecutado con el equipo. Pendiente con los usuarios de prueba."],
         ["Poder bajo, interés bajo — monitorear",
          "Autores de los assets, integrante dado de baja",
          "Cumplir la obligación y registrarla. Sin gestión activa.",
          "Licencias verificadas una por una en su origen y atribución registrada."],
     ]),

    ("Los dos interesados que cambiaron el proyecto",
     ["Interesado", "Qué cambió", "Cómo se tramitó"],
     [
         ["Asesor terapéutico, por su ausencia",
          "Sin dictamen clínico la medida de éxito 8 no se podía verificar. El proyecto pasó "
          "del encuadre de rehabilitación motriz al de regulación emocional.",
          "Retiro formal de la medida 8 en el recorte de alcance, con la contingencia que el "
          "acta ya preveía: protocolos publicados de Neurologic Music Therapy y la ausencia de "
          "validación externa documentada como limitación explícita del informe final."],
         ["Integrante dado de baja, riesgo R14",
          "El área de juego de ritmo pasó a desarrollo VR. De sus 22 actividades sobrevivieron "
          "15. La dirección y la coordinación quedaron sin titular y su carga se absorbió "
          "dentro de QA.",
          "La respuesta estaba escrita ANTES en el registro de riesgos —redistribuir y "
          "recortar, no reemplazar—, así que una baja se resolvió en una tarde de "
          "reasignación en vez de una semana de decidir qué hacer."],
     ]),
]

LECCIONES = [
    ("Un interesado ausente puede reescribir el alcance",
     "El asesor terapéutico no asistió a una sola sesión y es el interesado que más cambió el "
     "proyecto: retiró una medida de éxito y obligó a reencuadrar el objetivo terapéutico "
     "entero. La gestión de interesados no trata solo de quienes participan, sino de quienes "
     "deberían participar y no lo hacen, porque el alcance comprometido puede depender de "
     "ellos. La contingencia estaba prevista en el acta, y por eso el proyecto no se detuvo."),

    ("Una decisión no registrada no obliga a nadie",
     "El equipo decidió el cambio de encuadre terapéutico antes del corte de medio curso, en "
     "conversación, y tardó un mes en llegar a un documento. Durante ese mes la carta sponsor "
     "afirmaba un marco que el equipo ya había abandonado, y cualquiera que cruzara los dos "
     "habría encontrado la contradicción sin explicación. Una decisión que solo existe en la "
     "memoria de quienes estuvieron presentes no sobrevive a que cambie quién la tomó."),

    ("El interesado que falta identificar a tiempo es el que puede mover la fecha",
     "Los usuarios de las pruebas QT.8 llevan todo el proyecto en el registro de riesgos como "
     "R18, y a siete días del cierre siguen sin reclutar. No es un olvido: es que el prototipo "
     "no estuvo listo para probar hasta finales de octubre. Pero el informe final depende por "
     "completo de esas pruebas, así que un grupo de interesados sin asegurar es hoy el único "
     "riesgo que puede arrastrar la fecha comprometida."),
]

REMITE_A = [
    ("entregables/02_Acta_Constitutiva.docx",
     "§3.1 clientes y partes intervinientes, §3.2 roles y responsabilidades, y el anexo A con "
     "la asignación nominal por paquete de trabajo."),
    ("entregables/01_Carta_Sponsor.docx",
     "Las diez medidas de éxito, que son el acuerdo con la patrocinadora."),
    ("entregables/09_Respuesta_Riesgo_R14.docx",
     "La baja del integrante y la redistribución completa de su carga."),
    ("entregables/11_Cambio_de_Enfoque.docx",
     "La solicitud de cambio del marco terapéutico, PMBOK 4.6, con su justificación."),
    ("entregables/10_Recorte_de_Alcance.docx",
     "El retiro de la medida de éxito 8 por la ausencia del asesor."),
]
