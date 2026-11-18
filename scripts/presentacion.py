# -*- coding: utf-8 -*-
"""Guion de la presentacion y demostracion final. Unica fuente del documento 17. Cierra QX.

QX ES LA ULTIMA ACTIVIDAD DEL PROYECTO y cuelga del informe integrado, de la build definitiva
y de la corrida completa: la demo se hace con esa build y las conclusiones salen de ese
informe. Este documento es el guion, no las diapositivas: de aqui sale el .pptx en una pasada,
y lo que se revisa y se corrige es esto.

LAS CIFRAS NO SE ESCRIBEN AQUI. Salen de estado.py, costos.py, sesiones.py, manual_datos.py y
replan.py. Un guion de presentacion con numeros tecleados es el sitio donde una cifra vieja
llega al proyector.

QUE SE CUENTA Y EN QUE ORDEN
----------------------------
El arco no es cronologico. Es: que se prometio, que se descubrio, que se entrego, que se
aprendio. La parte interesante para la materia NO es el prototipo: son las tres decisiones que
reorientaron el proyecto y como se sostuvieron. Un proyecto que cumple su plan original no
ensena administracion de proyectos; uno que lo cambia tres veces con la razon escrita, si.
"""

# (numero, titulo, que se dice, que se muestra, minutos)
#
# EL TIEMPO ES EL DATO QUE MAS SE IGNORA Y EL QUE MAS DUELE. El total NO se escribe aqui: se
# suma de los bloques, y el generador lo imprime. Si la asignacion es menor, el orden en que se
# recorta esta en RECORTE_SI_FALTA_TIEMPO, abajo, y no es por tamano: hay bloques que sostienen
# el arco y sin ellos los resultados dejan de entenderse.

BLOQUES = [
    (1, "Qué es", [
        "Una batería que se toca de verdad en realidad virtual, siete piezas al alcance de los "
        "brazos, pensada como apoyo a la regulación emocional: tocar y desahogarse.",
        "Equipo A, ocho integrantes al arrancar. Meta Quest 3 y 3S, standalone, sin PC.",
        "Dos entregables desde el primer día: la documentación de administración conforme a "
        "PMBOK, y un prototipo demostrable validado con usuarios.",
     ], "Portada y una foto del kit en el visor.", 2),

    (2, "Qué se prometió", [
        "La carta sponsor comprometió diez resultados verificables, no una lista de tareas. Esa "
        "distinción es la que después permitió recortar sin perder el rumbo.",
        "El riesgo dominante se identificó desde el acta: la latencia entre el golpe y el "
        "sonido. Por encima de 30 milisegundos el golpe deja de sentirse causal y el valor del "
        "producto se cae.",
        "Y se fechó como hito Go/No-Go en la semana 4, no al final. Medir el riesgo dominante "
        "cuando ya no se puede hacer nada es un informe, no una decisión.",
     ], "La tabla de las diez medidas de éxito, sin estado todavía.", 3),

    (3, "Las tres decisiones que reorientaron el proyecto", [
        "Esto es lo que de verdad enseña el proyecto, y va antes de los resultados a propósito: "
        "los resultados se entienden a partir de aquí.",
        "Cada una tiene su documento, su fecha y su razón escrita. Ninguna se tomó para que un "
        "número cuadrara.",
     ], "Las tres decisiones con su fecha y su efecto medido.", 4),

    (4, "Qué se entregó: el prototipo", [
        "No una lista de funciones: los hitos, que es cada punto a partir del cual el proyecto "
        "pudo hacer algo que antes no podía.",
        "Y los números que lo sostienen, cada uno con el archivo que lo demuestra.",
     ], "Los hitos en línea de tiempo, y la tabla de cifras medidas.", 3),

    (5, "La demostración", [
        "Tres minutos, en el orden del guion de demo. Se enseña el recorrido completo, no la "
        "parte que mejor queda.",
     ], "El visor, con la aplicación. Ver el guion de demo.", 3),

    (6, "Qué se midió", [
        "Las diez medidas con su estado real: ocho cerradas, una en curso y una retirada, con "
        "la razón de la retirada.",
        "Las sesiones registradas y qué se puede concluir de ellas. Y qué no, que importa igual.",
     ], "Las diez medidas con estado, y el resumen de sesiones.", 3),

    (7, "Qué costó", [
        "El presupuesto y por qué se corrigió tres veces. Cada corrección acercó la estimación "
        "a lo que el proyecto realmente es: practicantes bajo convenio escolar, no empleados.",
        "Ningún riesgo tiene impacto monetario porque el proyecto no compra ni contrata: la "
        "reserva se valora en días hábiles, no en pesos.",
     ], "La evolución del presupuesto en tres versiones.", 2),

    (8, "Qué no salió, y qué se hizo con eso", [
        "El asesor terapéutico nunca llegó. La medida 8 se retiró y se documentó la ausencia de "
        "validación externa como limitación explícita: era la contingencia que el acta ya había "
        "previsto.",
        "El cronograma mostraba el proyecto terminado en octubre porque llevaba las fechas del "
        "plan y no las reales. Se rebaseó con la fecha de registro de cada actividad y su "
        "evidencia.",
        "El plan de cierre no cabe en la reserva, y el documento lo dice con el número de días. "
        "No se recortó para que la fecha cuadrara.",
     ], "El antes y después del rebaseline del cronograma.", 3),

    (9, "Lo que este proyecto enseñó", [
        "Tener la respuesta a un riesgo escrita ANTES convirtió la baja de un integrante en una "
        "tarde de reasignación. Sin el registro habría sido una semana de decidir qué hacer.",
        "Recortar con un criterio —sobrevive lo que sirve a una medida de éxito— es distinto de "
        "recortar lo que no dio tiempo. Lo primero se defiende; lo segundo se nota.",
        "Un cronograma con las fechas del plan no sirve para dirigir. Y una cifra escrita a mano "
        "en dos sitios se desfasa en los dos.",
     ], "Tres frases, una por lección. Sin tabla.", 2),

    (10, "Cierre", [
        "Qué queda abierto, con fecha: no se presenta como terminado lo que no lo está.",
        "Dónde está todo: los dos repositorios y los diecisiete documentos.",
     ], "La lista de lo pendiente y los dos enlaces.", 1),
]


# Si el tiempo asignado no alcanza, se recortan EN ESTE ORDEN. El 3 y el 8 no estan: son las
# tres decisiones y lo que no salio, que es lo que la materia evalua. Quitarlos deja una
# presentacion de producto, no de administracion de proyectos.
RECORTE_SI_FALTA_TIEMPO = [7, 1, 9, 4, 6]


# --------------------------------------------------------------------------- guion de la demo
#
# (paso, que se hace, que hay que ver, cuanto, riesgo)
#
# EL ORDEN NO ES EL DEL MENU, es el que ensena el recorrido completo sin repetir pantalla y sin
# depender de acertar un golpe difícil delante de todos. Cada paso dice su riesgo: lo que puede
# salir mal en vivo y que hacer si sale.

DEMO = [
    (1, "Abrir la aplicación con la marca de tutorial borrada",
     "La cortinilla y el tutorial arrancando solo, sin que nadie toque nada.",
     "20 s",
     "Si la marca de tutorial visto está puesta, entra directo al menú y se pierde el paso. "
     "Borrarla ANTES con el comando del visor."),

    (2, "Hacer el primer paso del tutorial y saltar el resto",
     "La baqueta fantasma demostrando, y el golpe propio registrándose con su vibración.",
     "30 s",
     "El tutorial completo son cuatro pasos y no caben. Se enseña el primero y se explica que "
     "hay tres más."),

    (3, "Ir al menú y entrar a información",
     "Que las opciones son pads que se golpean, no botones. Y que el texto dice que mide si "
     "tocas a tiempo y que no sustituye a un terapeuta.",
     "20 s",
     "Ninguno. Es el paso más seguro y por eso va temprano."),

    (4, "Elegir TOCAR, un ritmo y una velocidad",
     "Que el selector son dos pasos y que el segundo es la dificultad del mismo ejercicio.",
     "20 s",
     "Elegir el ritmo de pulso básico a tempo lento. El rápido no perdona delante de nadie."),

    (5, "Tocar unos compases",
     "Los aros cerrándose sobre cada pieza, el veredicto en verde o amarillo sobre el pad "
     "golpeado, y el borde de la pantalla iluminándose cuando la pieza queda fuera de la vista.",
     "60 s",
     "Lo que puede salir mal es fallar notas en vivo. No importa y conviene decirlo: el "
     "veredicto rojo también es parte de lo que se enseña."),

    (6, "Dejar que la pista termine y leer los resultados",
     "Que el resumen va dicho en palabras además de en números, y las dos constancias.",
     "30 s",
     "La pista completa dura más de lo que cabe. Usar una pista corta, o explicar que se corta "
     "y pasar a resultados con una sesión ya grabada."),

    (7, "Volver al menú y entrar a modo libre",
     "El kit completo sin notas ni puntuación, y que la salida cuelga del kit.",
     "20 s",
     "Es el único sitio donde la salida no está en la fila de pads. Si no se encuentra en vivo, "
     "es un hallazgo honesto y está en el registro como OBS-18."),

    (8, "Volver al menú y golpear el pad que dice SALIR",
     "Que el pad que dice SALIR hace salir, y la cortinilla de despedida.",
     "10 s",
     "Ninguno ahora. Es el caso CU-14 y existe porque este defecto ya ocurrió una vez."),
]


# ------------------------------------------------------------------ antes de presentar
#
# Lista de comprobacion. Cada punto es algo que ya fallo una vez en este proyecto.

ANTES = [
    ("Compilar e instalar la build definitiva, no la última que había",
     "El APK en disco llegó a tener dos días menos que el último commit: se instaló una build "
     "vieja creyendo que era la nueva."),
    ("Borrar la marca de tutorial visto en el visor",
     "Sin eso el paso 1 de la demo no se puede enseñar."),
    ("Cargar el visor y comprobar que no entra en suspensión",
     "El modo inalámbrico se pierde al reiniciarse."),
    ("Pasar las pruebas en batchmode y revisar ProjectSettings después",
     "Batchmode sin realidad virtual borra las referencias de OpenXR y la build siguiente sale "
     "sin VR."),
    ("Correr el recorrido completo de la demo una vez, de principio a fin",
     "Es la actividad QV.1 y existe precisamente para esto."),
    ("Tener el espacio: metro y medio alrededor, sin obstáculos",
     "El límite de seguridad se dibuja, pero la mesa no se mueve sola."),
    ("Llevar las métricas ya bajadas del visor",
     "Si la demo se cae, los números siguen estando y se presentan igual."),
]


# ------------------------------------------------------------------ huecos declarados

PENDIENTE_DE_DATO = [
    ("Resultados de las pruebas con los 14 participantes",
     "El bloque 6 los nombra y quedan en blanco hasta que exista la atribución de sesiones. "
     "Ver el documento 16."),
    ("Las capturas de pantalla para las diapositivas",
     "Las trece del manual de usuario sirven igual aquí. Se toman en el visor."),
]
