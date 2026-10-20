# -*- coding: utf-8 -*-
"""
Datos del estado del proyecto. Única fuente de verdad del documento 12.

POR QUE UN DOCUMENTO MAS, Y NO UN REFRITO

Los once documentos anteriores son correctos y siguen valiendo, pero cada uno responde a su
momento: la carta sponsor es de septiembre, el recorte del 17 de octubre, el cambio de enfoque
del 18. Nadie que llegue nuevo puede reconstruir el proyecto leyendolos en orden, porque tres
de ellos reorientan lo que dicen los anteriores.

Este reune el estado VIGENTE y dice que documento tiene el detalle de cada cosa. No repite su
contenido: remite a el.

LAS CIFRAS NO SE ESCRIBEN A MANO

Salen de los archivos de medicion del visor y del cronograma. Un documento de estado con
numeros tecleados queda desfasado el mismo dia, y peor: nadie sabe cuando dejo de ser cierto.
"""

FECHA = "20 de octubre de 2026"

# --- las tres decisiones que reorientaron el proyecto ------------------------------------

DECISIONES = [
    {
        "titulo": "Baja de un integrante",
        "cuando": "6 de octubre de 2026",
        "doc": "09_Respuesta_Riesgo_R14.docx",
        "causa":
            "El director de proyecto dejo de asistir. El registro de riesgos lo tenia previsto "
            "como R14, con su respuesta ya redactada: redistribuir y recortar, no reemplazar.",
        "efecto":
            "El area de juego de ritmo paso a desarrollo VR. De sus 22 actividades sobrevivieron "
            "15, las que servian a una medida de exito; las otras 7 se retiraron. La direccion "
            "y la coordinacion quedaron sin titular, y esa carga se absorbio dentro de QA.",
        "leccion":
            "Tener la respuesta escrita ANTES convirtio una baja en una tarde de reasignacion. "
            "Sin el registro habria sido una semana de decidir que hacer.",
    },
    {
        "titulo": "Recorte de alcance",
        "cuando": "17 de octubre de 2026",
        "doc": "10_Recorte_de_Alcance.docx",
        "causa":
            "Con diecinueve dias habiles por delante, las 257 actividades de la lista original "
            "no cabian. El reparto ademas era desigual: dos areas cerradas y tres apenas "
            "arrancadas.",
        "efecto":
            "De 257 a 158 actividades. 100 recortadas, 12 que ya estaban hechas sin registrar y "
            "1 anadida. Los tres recortes grandes: entorno 3D de 31 a 6 porque el area deja de "
            "modelar y pasa a integrar assets libres, juego de ritmo de 22 a 0 porque R14 ya las "
            "habia retirado, y sonido de 22 a 1 porque doce estaban hechas.",
        "leccion":
            "El criterio NO fue lo que dio tiempo. Sobrevive lo que sirve a una medida de exito "
            "de la carta sponsor, porque lo que se comprometio fueron diez resultados "
            "verificables, no 257 tareas.",
    },
    {
        "titulo": "Cambio de enfoque terapeutico",
        "cuando": "decidido antes del 18 de septiembre, registrado el 18 de octubre",
        "doc": "11_Cambio_de_Enfoque.docx",
        "causa":
            "El marco de rehabilitacion motriz exigia que alguien con credencial clinica validara "
            "las rutinas. El asesor terapeutico tenia fecha limite el 10 de septiembre y no se "
            "concreto. Ademas, la amplitud de movimiento de miembro superior se mide con "
            "goniometria o captura corporal: un control de mano da la posicion del control, no "
            "la del hombro ni la del codo.",
        "efecto":
            "El proyecto pasa de herramienta de apoyo a la rehabilitacion motriz a herramienta de "
            "regulacion emocional por medio del ritmo. Es un cambio de ENCUADRE, no de producto: "
            "el prototipo es el mismo. La medida 8 se retira y la 9 pierde la amplitud de "
            "movimiento.",
        "leccion":
            "La decision se tomo en conversacion y tardo un mes en llegar a un documento. "
            "Durante ese mes la carta sponsor afirmaba un marco que el equipo ya habia "
            "abandonado. Una decision no registrada no obliga a nadie y no sobrevive a que "
            "cambie quien la tomo.",
    },
]

# --- las medidas de exito, con la evidencia que las cierra -------------------------------

MEDIDAS = [
    (1, "Identificacion de componentes", "cerrada",
     "Siete pads con geometria y color propios. La separacion entre centros se calcula, no se "
     "estima: 0.344 m en el par mas cercano sobre los 0.320 que exige el radio mas la holgura."),
    (2, "Deteccion de contacto", "cerrada",
     "Deteccion por plano armado con prediccion. 84 golpes registrados sin una sola agenda "
     "tardia."),
    (3, "Correspondencia del sonido", "cerrada",
     "Cada pad lleva su DrumKitPiece y hay una prueba que impide que dos compartan la misma."),
    (4, "Latencia por debajo de 30 ms", "cerrada",
     "Hito Go/No-Go del acta. Medido con el protocolo del clic fisico: p90 de +4.07 ms, dentro "
     "de la ventana de -10 a +25 ms."),
    (5, "72 fps sostenidos", "cerrada",
     "12949 fotogramas medidos en el visor: 12946 en vsync, 3 vsync perdidos. 0.02 % contra un "
     "criterio del 5 %."),
    (6, "Interaccion intuitiva", "en curso",
     "El tutorial registra cuantos intentos cuesta cada paso. De 11 intentos en la primera "
     "corrida a 6 en la ultima, y de 74 a 37 segundos. Falta recoger el dato con usuarios "
     "reales en QT.8."),
    (7, "Sensibilidad a la intensidad", "cerrada",
     "SampleSelector elige la muestra por energia del golpe. Las siete piezas tienen eje de "
     "intensidad aprovechable, de 1.40x a 2.56x."),
    (8, "Pertinencia terapeutica", "retirada",
     "Sin asesor no hay dictamen, asi que la medida no se puede verificar por ningun camino. "
     "Retirada formalmente en el documento 10, con la contingencia que el acta ya preveia."),
    (9, "Registro de metricas", "cerrada",
     "31 sesiones volcadas a JSON con precision temporal, constancia del pulso y los desfases "
     "crudos. La mejor: 148 de 160 notas, desviacion 24.5 ms, constancia 23.4 ms."),
    (10, "Seguridad de uso", "cerrada",
     "LimiteSeguro dibuja el perimetro con radio calculado del pad mas lejano. Verificado en el "
     "visor. Falta el reporte de los participantes de QT.8."),
]

# --- el avance, por area ------------------------------------------------------------------

AVANCE = [
    ("Desarrollo VR",               28,  2),
    ("Entorno 3D",                   7,  0),
    ("Experiencia emocional",       18,  1),
    ("Interfaz",                     9,  9),
    ("Juego de ritmo",              17,  0),
    ("Musica",                       7,  0),
    ("QA, documentacion y gestion", 22, 24),
    ("Sonido",                      13,  1),
]

# --- lo que el prototipo hace hoy, con numeros -------------------------------------------

PROTOTIPO = [
    ("Reloj musical sin deriva",
     "Desvio de 0.0 ms sostenido durante 205 segundos contra un metronomo de 120 BPM exactos. "
     "El criterio era menos de 20 ms sin crecer."),
    ("Juego de ritmo jugable",
     "Beatmap sobre musica real medida. Ventanas de juicio en milisegundos y no en fracciones "
     "de pulso, porque la precision humana no escala con el tempo."),
    ("Kit de siete piezas",
     "AVL Drumkits Red Zeppelin, CC BY-SA 3.0. Cinco capas de velocidad por pieza."),
    ("Entorno de bosque al amanecer",
     "Assets libres, 72 fps sostenidos. Coherente con el enfoque emocional: un escenario de "
     "concierto empuja a la activacion, que es lo contrario de lo que se busca."),
    ("Tutorial por demostracion",
     "Cuatro pasos con baqueta fantasma y rotulos. Registra intentos y tiempo por paso, que es "
     "la evidencia de la medida 6."),
    ("Metricas de sesion",
     "Precision temporal y constancia del pulso, con los desfases crudos para poder reanalizar."),
]

# --- lo que queda, por riesgo -------------------------------------------------------------

PENDIENTE = [
    ("La cadena que decide si el proyecto cierra", "alto",
     "Flujo de la aplicacion acabado, pruebas con usuarios (QT.8), analisis de resultados y "
     "redaccion del informe final (QI.1 a QI.5). Es una cadena: nada empieza hasta que lo "
     "anterior termina, y el informe es la cola.",
     "Diana, con apoyo de gerencia"),
    ("Interfaz", "medio",
     "Nueve actividades. El menu ya esta construido; faltan la pantalla de resultados acabada y "
     "la revision de legibilidad con usuarios.",
     "Sarai"),
    ("Build final y correccion de errores", "medio",
     "QB.1 a QB.4 y QE.2 a QE.5. Dependen de que QT.8 produzca los errores que corregir.",
     "QA"),
    ("Manuales", "bajo",
     "Manual de usuario y manual tecnico. No dependen de nadie mas y se pueden escribir ya.",
     "QA"),
    ("Firmas pendientes", "bajo",
     "Respuesta al riesgo R14, recorte de alcance y cambio de enfoque. Los tres documentos "
     "estan escritos y esperan firma del equipo y de la patrocinadora.",
     "Direccion"),
]

# --- el mapa de los documentos -------------------------------------------------------------

DOCUMENTOS = [
    ("01_Carta_Sponsor.docx", "Justificacion, objetivo, las diez medidas de exito y el "
     "presupuesto. VIGENTE con las sustituciones del documento 11."),
    ("02_Acta_Constitutiva.docx", "EDT de 42 paquetes con criterio de aceptacion, responsable "
     "y duracion. VIGENTE con las sustituciones del documento 11."),
    ("03_Ruta_Critica.docx", "Red PDM completa con su justificacion."),
    ("04_Planes_Costos_Calidad_Riesgos.docx", "Calidad 8.1 a 8.3 y riesgos 11.1 a 11.7. "
     "Contiene el registro donde R14 estaba previsto."),
    ("05_Analisis_Costos_Calidad_Riesgos.docx", "Area 7 completa, de 7.1 a 7.4, incluido valor "
     "ganado."),
    ("06_Entregable_Medio_Curso.docx", "Corte del 18 de septiembre: 117 actividades, SPI 0.969."),
    ("07_Carta_Validacion_Entregables.docx", "Para firma de la docente, PMBOK 5.5."),
    ("08_Lista_Verificacion_Compromisos.docx", "Lo comprometido contra lo entregado."),
    ("09_Respuesta_Riesgo_R14.docx", "La baja del integrante y su redistribucion."),
    ("10_Recorte_de_Alcance.docx", "De 257 a 158 actividades, con la razon de cada recorte."),
    ("11_Cambio_de_Enfoque.docx", "Solicitud de cambio del marco terapeutico, PMBOK 4.6."),
    ("12_Estado_del_Proyecto.docx", "Este documento. El estado vigente y donde esta cada cosa."),
]

# --- riesgos vivos --------------------------------------------------------------------------

RIESGOS = [
    ("La cadena del informe final no tiene holgura", "alto",
     "QT.8 depende del flujo acabado, el analisis depende de QT.8 y el informe del analisis. Un "
     "retraso en cualquiera lo arrastra todo. Mitigacion: los manuales y la presentacion se "
     "pueden escribir en paralelo, sin esperar."),
    ("Carga concentrada en QA", "alto",
     "24 de las 37 actividades pendientes son de QA, documentacion y gestion. Es la misma "
     "concentracion que el analisis de ruta critica senalo en septiembre, y la baja de R14 la "
     "empeoro. Mitigacion: los manuales se pueden repartir."),
    ("Sin validacion externa", "asumido",
     "El asesor terapeutico nunca se concreto. Queda documentado como limitacion explicita del "
     "informe final, no como omision."),
]
