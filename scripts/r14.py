# -*- coding: utf-8 -*-
"""
Datos de la respuesta al riesgo R14. Las cifras se leen del cronograma, no se escriben a mano.
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validacion

HOY = datetime.date(2026, 10, 6)
CIERRE = datetime.date(2026, 10, 30)
PERIODO = datetime.date(2026, 11, 13)


def habiles(a, b):
    return sum(1 for i in range((b - a).days)
               if (a + datetime.timedelta(i)).weekday() < 5)


# Juego de ritmo: qué se conserva y qué se recorta.
#
# El criterio no es «lo que da tiempo» sino «lo mínimo que demuestra que el juego existe».
# Un juego de ritmo sin dificultades sigue siendo un juego de ritmo; sin reloj musical ni
# ventanas de precisión no es nada.
CONSERVA = [
    ("JT.1", "Reloj musical independiente de los FPS"),
    ("JT.2", "Cálculo de BPM y duración de cada beat"),
    ("JA.2", "Datos para representar una nota musical"),
    ("JA.3", "Estructura de datos de canciones y beatmaps"),
    ("JB.1", "Prototipo de beatmap manual"),
    ("JB.2", "Sistema que carga un beatmap"),
    ("JB.3", "Sincronizar beatmap con la música"),
    ("JN.1", "Representación visual de las notas"),
    ("JN.2", "Indicar qué componente debe golpearse"),
    ("JW.1", "Ventanas temporales Perfect, Good y Miss"),
    ("JW.2", "Detección de golpes correctos"),
    ("JW.5", "Detección de notas no golpeadas"),
    ("JP.1", "Sistema básico de puntuación"),
    ("JP.3", "Cálculo de precisión porcentual"),
    ("JI.1", "Integrar el evento DrumHit con el juego"),
]

RECORTA = [
    ("JL.1 JL.2", "Niveles de dificultad y su selección",
     "El prototipo se demuestra a una dificultad. Añadir más no prueba nada nuevo."),
    ("JM.1 JM.2 JM.3", "Modo libre con y sin música",
     "La batería ya es tocable libremente fuera del juego de ritmo: el modo libre existe "
     "de facto en la escena actual."),
    ("JC.1 a JC.4", "Cuenta regresiva, pausa, reinicio y abandono",
     "Flujo de aplicación, no mecánica. Depende de los menús, que son del área de interfaz."),
    ("JP.2 JP.4", "Combo y resumen de resultados",
     "La pantalla de resultados existe como diseño; implementarla es trabajo de interfaz."),
    ("JW.3 JW.4", "Detección de golpes anticipados y atrasados por separado",
     "Se registran como fallo. Distinguirlos afina el dato, no la experiencia."),
    ("JW.6", "Ajustar ventanas tras pruebas de usuarios",
     "Requiere pruebas con usuarios, que son de la semana 7."),
    ("JF.1 JF.2", "Feedback visual y auditivo de acierto y error",
     "El indicador de golpes ya muestra pieza e intensidad en cada golpe."),
    ("JI.2 a JI.5", "Sustituir teclado por VR e integrar con el flujo general",
     "La interacción VR ya existe: el juego se monta sobre DrumHit, no sobre teclado. "
     "Las tareas quedan sin objeto."),
    ("JK", "Sistema provisional de golpes con teclado",
     "Sin objeto por la misma razón."),
    ("JY", "Calibración de latencia entre golpe y música",
     "Ya resuelta por otra vía: la latencia se midió y quedó en +4.07 ms de p90."),
]

# Segundos conocedores. El plan de R14 los daba por designados y nunca lo estuvieron.
SEGUNDOS = [
    ("Desarrollo VR y batería", "Misael", "Christian",
     "Ya integra audio con el sistema de golpe; conoce DrumHit desde el lado del sonido."),
    ("Juego de ritmo", "Misael (reasignado)", "Diana",
     "Documenta el área y redacta sus pruebas."),
    ("Entorno 3D", "Kimberly", "Sarai",
     "Comparte criterio visual y la paleta con el entorno."),
    ("Interfaz / UX-UI", "Sarai", "Kimberly",
     "Misma razón, en sentido inverso."),
    ("Sonido", "Christian", "Javier",
     "Música y sonido comparten formato, licencias y mezcla."),
    ("Música", "Javier", "Christian",
     "Misma razón, en sentido inverso."),
    ("Experiencia emocional", "María", "Diana",
     "La fundamentación alimenta el informe final."),
    ("QA, documentación y gestión", "Diana", "Misael",
     "Mantiene el cronograma y el repositorio."),
]

# Trabajo que ya está hecho y el área responsable no había registrado.
YA_HECHO = [
    ("Christian", "SI.1 a SI.4",
     "Integrar sonidos de batería con el sistema DrumHit",
     "Hecho. DrumVoice selecciona la muestra por pieza y por intensidad, con dinámica "
     "timbral y round-robin. Verificar y marcar."),
    ("Christian", "SE.1 a SE.4",
     "Editar y normalizar las muestras",
     "Hecho. Las 82 muestras están a 48 kHz, mono, PCM, sin silencio inicial."),
    ("Christian", "SB.1 a SB.6",
     "Buscar sonidos de cada pieza",
     "Parcial. Bombo, tarola, dos toms, hi-hat y ride están. FALTA EL CRASH: el pack "
     "de Dustyroom no incluye ninguno."),
    ("Sarai", "IM.1 IM.2 · IW.1 a IW.5 · IG.1 a IG.3",
     "Mapa de pantallas, wireframes e indicadores",
     "Hecho. Las pantallas existen como prototipo navegable."),
    ("Sarai", "IR.1",
     "Revisar legibilidad de textos dentro del visor",
     "Investigado. El panel claro tiene 94 % de luminancia y cinco de los nueve colores "
     "de la paleta no alcanzan el contraste mínimo AA sobre él. Falta corregir, no "
     "investigar."),
    ("Kimberly", "AC.1 a AC.3",
     "Investigar teoría del color y percepción emocional",
     "Hecho por otra vía: existe el documento de paleta con los ocho colores definidos "
     "y su función. No rehacerlo."),
]

# Qué investigar, por persona. Concreto: dónde buscar y con qué criterio.
INVESTIGAR = {
    "Kimberly": [
        ("Assets de entorno en lugar de modelado propio",
         "Poly Pizza, Kenney.nl, Unity Asset Store filtrando por gratuitos, y Sketchfab "
         "filtrando por CC0.",
         "Low poly, licencia CC0 o CC BY explícita, y que el conjunto de la escena quepa "
         "en menos de 300 000 triángulos."),
        ("Presupuesto de rendimiento en Quest",
         "Ya está escrito en el diseño técnico del proyecto.",
         "Menos de 500 draw calls, menos de 300 000 triángulos, texturas ASTC, iluminación "
         "bakeada sin GI en tiempo real, single-pass instanced."),
        ("Registro de licencias",
         "Mismo criterio que se usó con el pack de percusión.",
         "La atribución se escribe al descargar, no al final. Un asset sin licencia "
         "localizable no entra."),
    ],
    "Diana": [
        ("Plantilla de plan de pruebas",
         "El protocolo de medición de latencia del proyecto sirve de modelo.",
         "Montaje, criterio de aceptación numérico, procedimiento y veredicto. Un plan sin "
         "criterio numérico no se puede aprobar ni reprobar."),
        ("Estructura del informe final",
         "Es la cola crítica del proyecto: nada la sigue.",
         "Arrancar el esqueleto ahora y llenarlo conforme cierran las áreas, en lugar de "
         "esperar a que todo termine."),
        ("Builds verificables",
         "El proyecto ya tiene un comando de compilación que valida la configuración.",
         "Comprueba IL2CPP, ARM64 y Vulkan antes de compilar, y se detiene si alguno "
         "no cuadra."),
    ],
    "Sarai": [
        ("Interfaz world-space en Unity",
         "El indicador de golpes del prototipo ya es un ejemplo funcionando.",
         "TextMeshPro 3D: el tamaño de fuente va en METROS, no en puntos. Conviene el "
         "autoajuste, porque el texto de prueba engaña sobre el tamaño real."),
        ("Corrección de contraste antes de implementar",
         "El análisis ya está hecho.",
         "Invertir la paleta para los paneles: fondo oscuro y texto claro. Los pasteles "
         "funcionan en el entorno 3D, no sobre un panel que emite luz a los ojos."),
        ("Interacción con mando",
         "XR Interaction Toolkit, componentes de ray interactor.",
         "Botones grandes, apuntables a distancia. Ya está en los diseños."),
    ],
    "Javier": [
        ("BPM exacto de las pistas",
         "Bloquea el juego de ritmo. Es lo primero.",
         "Un beatmap sin BPM exacto se desincroniza a los pocos compases."),
        ("Estilos musicales anclados al acta",
         "El acta define el iso-principio como marco.",
         "La sesión arranca en el tempo espontáneo del usuario y desciende hasta 60 BPM. "
         "Los estilos deben admitir ese descenso."),
        ("Licencias de las pistas",
         "Mismo criterio que el resto de los recursos.",
         "CC0 o CC BY con atribución escrita. Nada de uso incierto."),
    ],
    "Christian": [
        ("Conseguir un crash",
         "Es lo único que falta del kit.",
         "48 kHz, licencia explícita. Alternativa ya documentada: usar el ride como "
         "sexta pieza, que es lo que hace el prototipo actual."),
        ("Audio Mixer, con reserva",
         "Un mixer añade un nodo al camino del audio.",
         "Si se implementa, hay que volver a medir la latencia con el protocolo del "
         "proyecto. El hito Go/No-Go se midió sin mixer."),
        ("Verificar lo ya integrado",
         "Antes de trabajar, comprobar qué está hecho.",
         "La integración con DrumHit y la normalización de muestras ya están."),
    ],
    "María": [
        ("Actualizar la fundamentación al prototipo real",
         "Es su única tarea pendiente.",
         "El prototipo mide precisión temporal e intensidad de golpe. La fundamentación "
         "debe apoyarse en lo que el sistema realmente registra."),
    ],
}
