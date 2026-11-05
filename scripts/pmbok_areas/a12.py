# -*- coding: utf-8 -*-
"""
Área 12 — Adquisiciones. El proyecto no compró nada, y eso se documenta, no se disimula.

LA ÚNICA ADQUISICIÓN PLANIFICADA FUE EL ASESOR TERAPÉUTICO, Y FALLÓ. Es lo que hace que esta
área no sea un «no aplica» vacío: había una contratación prevista, con alcance, horas y
monto, tenía fecha límite, no se concretó, y eso costó una medida de éxito. Un documento que
dijera solamente «no hay adquisiciones» ocultaría el único hecho relevante del área.
"""

AREA = "12"

RESUMEN = [
    "El proyecto no adquiere bienes ni servicios. Los visores son un préstamo de la Facultad, "
    "Unity es gratuito en su licencia Personal, el kit de batería y la música están bajo "
    "licencias Creative Commons, y los dos paquetes del Asset Store que se usan ya estaban en "
    "poder del equipo. El presupuesto de $104,013 es mano de obra en su totalidad: no tiene "
    "una sola línea de compra.",

    "Eso no convierte el área en inaplicable. Hubo un análisis de hacer-o-comprar real, con "
    "seis decisiones que podrían haberse resuelto comprando y se resolvieron construyendo o "
    "usando contenido libre. Y hubo una contratación planificada —los servicios del asesor "
    "terapéutico, 4 sesiones, 24 horas, $21,600— que tenía fecha límite el 10 de septiembre y "
    "nunca se concretó. Esa falla retiró la medida de éxito 8 de la carta sponsor.",

    "Lo que sí existe son acuerdos de licencia y de préstamo. Se documentan con el mismo rigor "
    "que tendría un contrato, porque imponen obligaciones verificables: uno de ellos prohíbe "
    "redistribuir los archivos, y por eso dos paquetes están excluidos del repositorio.",
]

PROCESOS = {
    "12.1": (
        "Se hizo el análisis de hacer-o-comprar de seis decisiones técnicas y se registró la "
        "razón de cada una. Se planificó una sola contratación: los servicios del asesor "
        "terapéutico, con alcance, horas, monto y fecha límite de confirmación.",
        "Tabla de hacer-o-comprar de este documento; acta constitutiva §4.10.3 «Recursos que "
        "no cuestan»; carta sponsor, partida del asesor terapéutico.",
    ),
    "12.2": (
        "No se efectuó ninguna adquisición. La única planificada no se concretó: el contacto "
        "del asesor estaba identificado y no llegó a confirmarse antes del 10 de septiembre. "
        "Los acuerdos que sí se formalizaron son de licencia y de préstamo.",
        "Tabla de acuerdos vigentes de este documento; 10_Recorte_de_Alcance.docx, retiro de "
        "la medida 8; ATRIBUCION_entorno.txt y ATRIBUCION_musica.txt.",
    ),
    "12.3": (
        "Cada licencia se verificó en su página de origen, no en la descripción del paquete, y "
        "se registró la restricción que impone. Dos paquetes con EULA del Asset Store quedaron "
        "excluidos del repositorio porque permiten usar el contenido pero no redistribuirlo. "
        "El cierre del área es la atribución en los créditos de la aplicación.",
        "Actividades QC.4 y AA.4 del cronograma, cerradas el 18 de octubre; .gitignore del "
        "repositorio Unity, que documenta la exclusión y cómo reponer los paquetes.",
    ),
}

TABLAS = [
    ("Análisis de hacer-o-comprar",
     ["Decisión", "Alternativa de compra", "Qué se eligió", "Por qué"],
     [
         ["Motor de desarrollo",
          "Unreal Engine, o licencia Unity Pro",
          "Unity 6, licencia Personal gratuita",
          "La ventaja visual de Unreal no aporta valor terapéutico y su canal de Android "
          "cuesta horas que el proyecto no tiene. Unity Personal es gratuita por debajo del "
          "umbral de ingresos, que el proyecto no alcanza."],

         ["Visores",
          "Compra de dos Meta Quest 3",
          "Préstamo de la Facultad",
          "Dos visores permiten que las pruebas no se bloqueen entre sí. Comprarlos habría "
          "sido el mayor costo del proyecto y no era necesario: la Facultad los presta."],

         ["Seguimiento de las manos",
          "Guantes o sensores externos",
          "Los controles que vienen con el visor",
          "Los controles dan háptico y velocidad confiable; el seguimiento de manos no da "
          "ninguno de los dos, y la velocidad del golpe es la que determina la intensidad."],

         ["Almacenamiento de métricas",
          "Hospedaje de un backend",
          "Archivos JSON en el propio visor",
          "La aplicación es autónoma. Un backend habría añadido un costo recurrente y un "
          "perfil de desarrollo que el equipo no tiene."],

         ["Entorno tridimensional",
          "Compra de un paquete de entorno, o modelado propio",
          "Integración de assets de licencia libre",
          "Diecisiete tareas seriales de modelado no caben en diecinueve días. Decidido en el "
          "recorte de alcance del 17 de octubre."],

         ["Mezclador de audio",
          "Audio Mixer de Unity, sin costo monetario",
          "Descartado",
          "Añade un nodo al camino del audio y obligaría a remedir la latencia, que es la "
          "medida de éxito 4 y la única ganada con margen. Ninguna medida pide un mezclador."],
     ]),

    ("Acuerdos vigentes: licencias y préstamos",
     ["Recurso", "Origen", "Régimen", "Obligación que impone"],
     [
         ["Dos visores Meta Quest 3 y 3S", "Facultad", "Préstamo",
          "Devolución al cierre del proyecto. Sin contraprestación económica."],
         ["Unity 6000.5.10f1", "Unity Technologies", "Licencia Personal",
          "Válida por debajo del umbral de ingresos anuales, que el proyecto no alcanza."],
         ["Kit de batería AVL Drumkits Red Zeppelin", "Audio Vintage Library", "CC BY-SA 3.0",
          "Atribución, y los WAV derivados quedan bajo la misma licencia. La aplicación NO "
          "queda obligada a licenciarse así: incluir la obra en una colección no obliga a "
          "licenciar la colección."],
         ["Música «Maccary Bay»", "Kevin MacLeod, incompetech.com", "CC BY 4.0",
          "Atribución en los créditos de la aplicación y en el informe final. El autor "
          "conserva el copyright de la obra original."],
         ["Escenario, gradas y cielos", "Poly Pizza y Kenney", "CC0 y CC BY 3.0",
          "Los CC0 no exigen nada. Los CC BY 3.0 exigen nombrar al autor: J-Toastie, Zsky y "
          "jeremy."],
         ["Fantasy Forest Environment", "Unity Asset Store, paquete 35361",
          "Standard Unity Asset Store EULA",
          "Permite usar el contenido dentro de la aplicación pero NO redistribuir los "
          "archivos originales. EXCLUIDO del repositorio por esa razón."],
         ["Low Poly Trees and Vegetation", "Unity Asset Store, paquete 265300",
          "Standard Unity Asset Store EULA",
          "Misma restricción. EXCLUIDO del repositorio."],
         ["Muestra de bombo", "Dustyroom", "CC BY 4.0",
          "Atribución. Registrada en entregables/ATRIBUCION.txt."],
     ]),

    ("La adquisición que se planificó y no se concretó",
     ["Concepto", "Lo planificado", "Lo ocurrido"],
     [
         ["Servicio", "Asesoría de un fisioterapeuta, terapeuta ocupacional o musicoterapeuta "
          "certificado, con experiencia en rehabilitación de miembro superior",
          "No se contrató"],
         ["Alcance", "4 sesiones, 24 horas", "Ninguna sesión"],
         ["Monto", "$21,600", "No ejecutado"],
         ["Fecha límite de confirmación", "10 de septiembre de 2026", "Vencida sin confirmar"],
         ["Estado del riesgo", "El líder tenía un contacto identificado, por lo que el riesgo "
          "se bajó de alto a medio", "El contacto no se concretó"],
         ["Consecuencia", "Contingencia prevista en el acta: usar protocolos publicados de "
          "Neurologic Music Therapy y documentar la ausencia de validación externa",
          "Ejecutada. La medida de éxito 8 se retiró formalmente en el recorte de alcance del "
          "17 de octubre"],
     ]),
]

LECCIONES = [
    ("Bajar un riesgo porque hay un contacto identificado no es lo mismo que tenerlo cerrado",
     "El riesgo del asesor terapéutico se bajó de alto a medio cuando el líder dijo tener un "
     "contacto. Eso no era una confirmación, era una intención, y la diferencia solo se vio al "
     "vencer la fecha límite. Un riesgo de adquisición se cierra con un acuerdo, no con una "
     "gestión en curso: hasta que la contraparte dice sí por escrito, el riesgo sigue alto."),

    ("Una licencia gratuita puede imponer una restricción que una compra no impondría",
     "Los dos paquetes del Asset Store no costaron dinero y aun así son el único recurso del "
     "proyecto que no puede viajar en el repositorio. El resultado es que un compañero que "
     "clona obtiene la escena con el entorno roto. Se descubrió cuando pasó: el precio de un "
     "recurso y las obligaciones que trae son dos cosas distintas, y la segunda hay que leerla "
     "antes de integrarlo, no después."),

    ("Verificar la licencia en su origen y no en la descripción del paquete",
     "La actividad AA.4 consistió en abrir la página de origen de cada asset y leer su licencia "
     "real. Aparecieron dos regímenes distintos donde se suponía que había uno, y uno de ellos "
     "—CC BY-SA— obliga sobre las obras derivadas, lo que afecta a los WAV que el proyecto "
     "genera a partir del kit. Eso no está en la ficha del paquete."),
]

REMITE_A = [
    ("entregables/ATRIBUCION_entorno.txt",
     "El registro completo de cada asset del entorno con su autor, su URL de origen, su "
     "licencia y el texto de atribución exigido."),
    ("entregables/ATRIBUCION_musica.txt",
     "La atribución de la música y del kit de batería, con la lectura de CC BY-SA sobre las "
     "obras derivadas."),
    ("entregables/10_Recorte_de_Alcance.docx",
     "El retiro formal de la medida de éxito 8 por la ausencia del asesor, con la contingencia "
     "que el acta ya preveía."),
    ("entregables/01_Carta_Sponsor.docx",
     "La partida presupuestal del asesor terapéutico tal como se comprometió."),
]
