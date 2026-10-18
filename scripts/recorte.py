# -*- coding: utf-8 -*-
"""
Qué sobrevive al recorte de alcance, qué se recorta, y qué estaba hecho sin registrar.

Es la única fuente de verdad del recorte. El documento, el marcado del cronograma y las
pruebas leen de aquí; si una clave cambia de lista, cambia en los tres sitios a la vez.

El criterio no es «lo que dio tiempo»: sobrevive lo que sirve a una medida de éxito de la
carta sponsor, y se recorta lo que no sirve a ninguna.
"""

# Las diez medidas de la carta sponsor, con su criterio de verificación resumido.
MEDIDAS = {
    1: "El usuario distingue y alcanza los componentes sin indicación externa",
    2: "El sistema registra el golpe en el componente correcto en ≥95 % de los intentos",
    3: "El sonido reproducido corresponde siempre al componente golpeado",
    4: "El retardo entre golpe y sonido se mantiene por debajo de 30 ms",
    5: "La simulación sostiene 72 fps durante una sesión completa",
    6: "Un usuario sin experiencia comprende el uso sin instrucción escrita",
    7: "El sistema distingue golpe suave, medio y fuerte y modifica el sonido",
    8: "El asesor externo dictamina pertinencia terapéutica de las rutinas",
    9: "El sistema exporta precisión temporal, amplitud y constancia por sesión",
    10: "Ningún participante reporta mareo, fatiga ni molestia articular",
}

MEDIDA_RETIRADA = 8

# Actividades terminadas que el área responsable nunca registró.
#
# Se hicieron desde desarrollo VR mientras se construía la batería, y el área de sonido las
# seguía marcando como bloqueadas. Contarlas como recortadas daría por perdido trabajo real.
YA_HECHAS = {
    "SI.1": "DrumVoice reproduce la muestra de la pieza golpeada",
    "SI.2": "SampleSelector elige la muestra por intensidad, con dinámica timbral",
    "SI.3": "Audio 2D por decisión de diseño: la espacialización cuesta y no aporta aquí",
    "SI.4": "Medido en el hito Go/No-Go: p90 de +4.07 ms",
    "SE.1": "Las 82 muestras no tienen silencio inicial",
    "SE.3": "Ganancia de normalización por muestra, calculada al analizar el kit",
    "SE.4": "48 kHz, mono, PCM: el formato nativo del visor",
    "SB.1": "Bombo del pack Dustyroom, CC BY 4.0",
    "SB.2": "Tarola del mismo pack",
    "SB.3": "Dos toms del mismo pack",
    "SB.4": "Hi-hat del mismo pack",
    "SB.6": "Tres niveles por pieza, desde la velocidad de la baqueta",
}

# Lo que sobrevive, con la medida de éxito a la que sirve.
SOBREVIVEN = {
    # Entorno 3D — el área deja de modelar y pasa a integrar
    "AA.3": (None, "Assets de entorno con licencia libre. Sin esto no hay escenario"),
    "AA.4": (None, "Revisar licencias. Obligación legal, no opcional"),
    "AL.2": (6,    "Iluminación: un escenario oscuro no se entiende sin instrucción"),
    "AP.1": (1,    "Composición del escenario con los assets"),
    "AO.5": (5,    "Medir FPS en el visor. Es la medida 5 y hoy está sin verificar"),
    "AS":   (10,   "Límites visuales de seguridad del espacio de interacción"),

    # Sonido — solo falta una pieza del kit
    "SB.5": (3,    "Falta el crash. El pack no incluye ninguno"),

    # Música — lo mínimo que alimenta un beatmap real
    "MP.1": (None, "Una pista de prueba con licencia"),
    "MP.2": (None, "Su BPM exacto. Un BPM aproximado desincroniza a los pocos compases"),
    "MP.3": (None, "Su estructura: dónde cae el primer beat y el compás"),
    "MB.1": (None, "El patrón de batería de esa pista"),
    "MB.4": (None, "Convertir el patrón en beatmap"),

    # Interfaz — solo el flujo que se demuestra
    "II.2": (6,    "Menú principal dentro de Unity"),
    "II.3": (6,    "Interacción con botones por mando"),
    "II.6": (9,    "Pantalla de resultados: es donde se ven las métricas"),
    "IR.1": (6,    "Legibilidad en el visor. El análisis ya existe; falta corregir"),
    "IR.2": (6,    "Tamaño, distancia y posición de los paneles"),
    "IT.1": (6,    "Tutorial: cómo sujetar las baquetas"),
    "IT.2": (6,    "Tutorial: cómo seguir el ritmo"),
    "IT.3": (6,    "Tutorial: cómo funciona la intensidad del golpe"),
    "IT.4": (6,    "Implementar el flujo del tutorial"),

    # QA — el informe final ES la entrega
    "QB.1": (None, "Build candidata"),
    "QB.2": (None, "Probarla en el visor"),
    "QB.3": (None, "Corregir lo crítico"),
    "QB.4": (None, "Versión definitiva"),
    "QC.1": (None, "Registro de versiones"),
    "QC.4": (None, "Registro de assets y licencias. Obligación legal"),
    "QE.2": (None, "Registrar lo que reporten los usuarios"),
    "QE.3": (None, "Clasificar por gravedad"),
    "QE.4": (None, "Asignar a su área"),
    "QE.5": (None, "Verificar la corrección de lo crítico"),
    "QG.2": (None, "Acciones de mitigación por riesgo"),
    "QI.1": (None, "Analizar los resultados de las pruebas"),
    "QI.2": (None, "Redactar resultados"),
    "QI.3": (None, "Redactar conclusiones y limitaciones"),
    "QI.4": (None, "Integrar el informe"),
    "QI.5": (None, "Revisión final de redacción y formato"),
    "QM.1": (6,    "Manual de usuario"),
    "QM.2": (None, "Manual técnico de instalación"),
    "QT.1": (2,    "Plan de pruebas de la batería: es donde se mide el 95 %"),
    "QT.6": (2,    "Ejecutar las pruebas de batería"),
    "QT.7": (None, "Pruebas del sistema de ritmo"),
    "QT.8": (6,    "Pruebas con usuarios del prototipo"),
    "QV.1": (None, "Sesión completa de principio a fin"),
    "QV.2": (5,    "Estabilidad y cierres inesperados"),
    "QV.3": (5,    "Medir FPS en la build final: es el criterio de la medida 5"),
    "QV.4": (4,    "Evaluar la latencia en la build final"),
    "QV.5": (10,   "Comodidad de la experiencia"),
    "QX":   (None, "Presentación y demostración final"),

    # Desarrollo VR
    "DT.4": (None, "Incorporar el modelo 3D cuando llegue del área de entorno"),
    "DT.5": (None, "Reajustar los planos de golpe a ese modelo"),

    # Experiencia emocional
    "ET.2": (None, "Actualizar la fundamentación a lo que el prototipo realmente mide"),
}

# Actividad que NO existía en el plan original y se añade.
#
# Es el único sitio donde este recorte suma alcance, y la razón es la desproporción: el
# marcador del juego de ritmo ya calcula precisión temporal y constancia del pulso, así que
# volcarlas a un archivo cierra la medida 9, que hoy está en cero.
NUEVAS = {
    "DM.1": (9, "Exportar las métricas de sesión a JSON: precisión temporal y constancia"),
}

# Lo que se recorta, agrupado por la razón.
RECORTADAS = {
    # --- Entorno 3D: el área deja de modelar ---
    "AA.1": "Catálogo de assets. Se buscan directamente los que se van a usar",
    "AA.2": "Límites de polígonos. Ya están escritos en el diseño técnico del proyecto",
    "AB.1": "Modelo de batería. El kit de primitivas ya funciona y está medido",
    "AB.2": "Depende de AB.1",
    "AB.3": "Modelos de baquetas. Las actuales cumplen",
    "AB.4": "Depende de AB.1",
    "AB.5": "Depende de AB.1",
    "AB.6": "Depende de AB.1",
    "AC.1": "Teoría del color. YA EXISTE el documento de paleta del equipo",
    "AC.2": "La paleta ya está definida en ese documento",
    "AC.3": "Moodboard. No sirve a ninguna medida",
    "AD.1": "Elementos ambientales secundarios",
    "AD.2": "Depende de AD.1",
    "AE.1": "Investigar tipo de entorno. Se decide al elegir los assets",
    "AE.2": "Comparar ambientes. Misma razón",
    "AE.3": "Dirección artística. Misma razón",
    "AO.1": "Optimizar texturas. Se cubre eligiendo assets ya optimizados",
    "AO.2": "LOD. Innecesario con una escena de pocos objetos",
    "AO.3": "Revisar luces en tiempo real. Se cubre en AL.2",
    "AO.4": "Iluminación horneada. Se cubre en AL.2",
    "AO.6": "Optimizar hasta cumplir. Se cubre en AO.5 si la medición falla",
    "AP.2": "Posición del jugador. Ya resuelta: el kit está medido y calibrado",
    "AP.3": "Aplicar la paleta. Se cubre al componer en AP.1",
    "AR.1": "Revisión cruzada con experiencia emocional",
    "AR.2": "Ajustes finales de ambientación",

    # --- Sonido ---
    "SA.1": "Sonidos ambientales del escenario",
    "SA.2": "Depende de SA.1",
    "SC.1": "Controles de volumen por canal. Ninguna medida los pide",
    "SC.2": "Mezcla general. Misma razón",
    "SE.2": "Eliminar ruidos. Las muestras del pack vienen limpias",
    "SM.1": "AUDIO MIXER: añade un nodo al camino del audio y obligaría a remedir la "
            "latencia, que es la medida 4 y la única ya ganada con margen",
    "SM.2": "Depende de SM.1",
    "SP.2": "Investigar bancos de sonidos. El pack actual ya cubre el kit",
    "SU":   "Sonidos de interfaz",

    # --- Música ---
    "MA.1": "Pistas adicionales. Con una basta para demostrar",
    "MA.2": "Pistas para modo libre. El modo libre se recortó en R14",
    "MB.2": "Momentos de intensidad en el patrón",
    "MB.3": "Tres versiones de dificultad. Las dificultades se recortaron en R14",
    "MB.5": "Probar el beatmap con el desarrollador. Se cubre en QT.7",
    "MB.6": "Corregir patrones. Requiere iteración que no cabe",
    "MN.1": "Normalizar todas las pistas. Solo hay una",
    "MN.2": "Documentar BPM y compás de cada pista. Se cubre en MP.2 y MP.3",
    "MR.1": "Investigar características musicales",
    "MR.2": "Analizar BPM de referencias",
    "MR.3": "Analizar compases para principiantes",
    "MR.4": "Definir estilos musicales. Se recorta a una pista",
    "MR.5": "Definir duración de las pistas",

    # --- Interfaz ---
    "IE":   "Estilo visual general. Las pantallas ya existen como diseño",
    "II.1": "Importar recursos de Canva/Figma. Se implementa directo en Unity",
    "II.4": "Configuración de volumen. Depende de los canales recortados en SC",
    "II.5": "Menú de pausa. La pausa se recortó en R14",
    "IR.3": "Corregir navegación tras pruebas. Requiere iteración que no cabe",
    "IS.1": "Selección de canción y dificultad. Hay una canción y no hay dificultades",
    "IS.2": "Diseñar menú de configuración",
    "IS.3": "Diseñar controles de volumen. Depende de SC",
    "IS.4": "Diseñar menú de pausa. Depende de II.5",
    "IS.5": "Pantalla de confirmación de salida",
    "IS.6": "Diseñar resultados. La pantalla ya existe como prototipo",
    "IW.4": "Wireframe del tutorial. Se implementa directo",
    "IW.6": "Wireframe de resultados. Ya existe como prototipo",

    # --- QA ---
    "QD.1": "Documentación de arquitectura. YA EXISTEN la guía de 8 capítulos y los specs",
    "QD.2": "Diagrama de flujo. Se cubre en el informe final",
    "QD.3": "Documentar detección de golpes. Está en la guía y en el spec",
    "QD.4": "Documentar el juego de ritmo. Está en su spec y su plan",
    "QD.5": "Documentar intensidad. Está en la guía",
    "QD.6": "Documentar el entorno. El entorno se recortó a integración",
    "QD.7": "Documentar la música. Se cubre con MP.3",
    "QD.8": "Documentar la interfaz. Se cubre en el informe final",
    "QF.1": "Capturas de pantalla. Se obtienen al preparar QX",
    "QF.2": "Video de evidencia. Misma razón",
    "QT.2": "Plan de pruebas del juego de ritmo. Se cubre con QT.7",
    "QT.3": "Plan de pruebas de interfaz. Se cubre con QT.8",
    "QT.4": "Plan de pruebas de audio. La latencia ya se midió con su protocolo",
    "QT.5": "Plan de pruebas de rendimiento. Se cubre con QV.3",

    # --- Desarrollo VR ---
    "DB.2": "Baquetas interactuables. Van solidarias al control, decisión del acta",
    "DB.4": "Física de baquetas. No hay física que ajustar",
    "DO":   "Agarrar y soltar objetos. Misma decisión del acta",
    "DT.3": "Colliders por componente. La detección es por plano armado",

    # --- Juego de ritmo: ya recortadas por R14 ---
    "JC.1": "Cuenta regresiva. Recortada en R14; los compases de entrada la cubren",
    "JC.2": "Pausa y reanudación. Recortada en R14",
    "JC.3": "Reiniciar actividad. Recortada en R14",
    "JC.4": "Abandonar actividad. Recortada en R14",
    "JF.1": "Feedback visual. Lo cubre JudgePopup",
    "JF.2": "Feedback auditivo. La batería ya suena al golpear",
    "JI.2": "Sustituir teclado por VR. El teclado nunca se construyó",
    "JI.3": "Intensidad dentro del juego. DrumHit ya la lleva",
    "JI.4": "Mecánicas por intensidad. Recortada en R14",
    "JI.5": "Integrar con el flujo general. Depende de los menús",
    "JK":   "Sistema de teclado. Sin objeto: la interacción VR ya existe",
    "JL.1": "Niveles de dificultad. Recortada en R14",
    "JL.2": "Selección de dificultad. Depende de JL.1",
    "JM.1": "Modo libre. La batería ya es tocable fuera del juego",
    "JM.2": "Música de fondo en modo libre. Depende de JM.1",
    "JM.3": "Tocar sin música. Depende de JM.1",
    "JP.2": "Combo. Recortada en R14",
    "JP.4": "Resumen de resultados. Lo cubre II.6",
    "JW.3": "Detectar golpes anticipados por separado. Se registran como fallo",
    "JW.4": "Detectar golpes atrasados por separado. Misma razón",
    "JW.6": "Ajustar ventanas tras pruebas. Requiere iteración que no cabe",
    "JY":   "Calibración de latencia. Ya resuelta: p90 de +4.07 ms",
}


def resumen():
    """Cifras del recorte, calculadas de las listas. Nunca escritas a mano."""
    return dict(
        ya_hechas=len(YA_HECHAS),
        sobreviven=len(SOBREVIVEN),
        nuevas=len(NUEVAS),
        recortadas=len(RECORTADAS),
    )


if __name__ == "__main__":
    r = resumen()
    for k, v in r.items():
        print(f"  {k:12s} {v}")
    print(f"  {'clasificadas':12s} "
          f"{r['ya_hechas'] + r['sobreviven'] + r['recortadas']}")
