# -*- coding: utf-8 -*-
"""Casos de uso y registro de observaciones de QT.8. Unica fuente del documento 16.

QUE ES REAL Y QUE NO, PORQUE IMPORTA
------------------------------------
REALES, y de ahi sale todo este archivo:

  - Los 30 hallazgos de `OBSERVACIONES`. Cada uno ocurrio de verdad, lleva su fecha y el
    commit que lo corrige, y varios llevan el reporte LITERAL de quien lo encontro. Son
    hallazgos de uso: aparecieron usando la aplicacion en el visor, no leyendo codigo.
  - Las 39 sesiones con pista completa registradas en el visor, del 17-oct al 11-nov.
  - Los casos de uso de `CASOS`. Son producto de trabajo: se derivan del flujo de la
    aplicacion y de las medidas de exito de la carta sponsor.

NO ESTA AQUI, Y SE DECLARA EN VEZ DE RELLENARSE:

  - La atribucion a los 14 participantes. El volcado de sesion no lleva identificador de
    participante: lleva fecha, BPM, notas, precision, constancia y los desfases crudos. Con
    los archivos se puede agrupar por sesion, no por persona. Eso sale de la lista que llevo
    quien facilito las pruebas.
  - Las respuestas de comodidad de QV.5. Las contesta la persona, no el sistema.

Los campos sin dato van como PENDIENTE y el generador los marca. INVENTAR participantes y
numeros y presentarlos como medidos seria fabricar el registro que este documento existe para
sostener: si la docente lo cruza con los archivos del visor, no cuadra.
"""

# --------------------------------------------------------------------------- casos de uso
#
# (id, titulo, precondicion, pasos, resultado esperado, criterio de aceptacion, medida)
#
# LA MEDIDA es el numero de la medida de exito de la carta sponsor que el caso cobra. Un caso
# que no cobra ninguna medida no deberia estar: es el mismo criterio con el que se hizo el
# recorte de alcance del 18-oct.

CASOS = [
    ("CU-01", "Abrir la aplicacion por primera vez",
     "Aplicacion recien instalada. La marca de tutorial visto no existe.",
     ["Ponerse el visor y abrir la aplicacion.",
      "Esperar sin tocar nada."],
     "Aparece la cortinilla de bienvenida y el tutorial arranca solo, sin que nadie le diga "
     "al participante que hacer.",
     "El participante no pregunta que hacer antes de que arranque el tutorial.", 6),

    ("CU-02", "Completar el tutorial sin ayuda externa",
     "El tutorial acaba de arrancar. El facilitador no interviene salvo por seguridad.",
     ["Seguir los cuatro pasos tal como los presenta la aplicacion.",
      "Anotar cada vez que el participante pregunta algo."],
     "El tutorial termina y la aplicacion pasa al menu.",
     "Lo completa sin que el facilitador tenga que explicar ningun paso. Se registra el numero "
     "de preguntas: el objetivo es cero.", 6),

    ("CU-03", "Reconocer las piezas del recorrido",
     "Paso 2 del tutorial.",
     ["Golpear cada pieza que la aplicacion marca, en el orden en que las marca."],
     "Las cuatro piezas se golpean sin golpear antes una equivocada.",
     "Menos de dos golpes a una pieza no marcada en todo el paso.", 6),

    ("CU-04", "Seguir el pulso dentro de la ventana de juicio",
     "Paso 3 del tutorial. Las ventanas son las mismas que usa el juego.",
     ["Escuchar el acompanamiento y golpear al mismo tiempo."],
     "El paso se supera con los aciertos que pide.",
     "Lo supera en tres intentos o menos. Si falla los tres, el paso es demasiado exigente "
     "para un primer contacto y es un hallazgo, no un fallo del participante.", 1),

    ("CU-05", "Distinguir las tres intensidades",
     "Paso 4 del tutorial, con el lector de golpes encendido.",
     ["Golpear suave, luego medio, luego fuerte, mirando el rotulo."],
     "El rotulo refleja los tres niveles distintos.",
     "El participante consigue los tres niveles. Si no logra el suave, el umbral esta mal "
     "calibrado para su fuerza de brazo.", 1),

    ("CU-06", "Navegar el menu golpeando pads",
     "El tutorial ha terminado. La fila de cinco pads esta a la vista.",
     ["Pedirle que vaya a la pantalla de informacion y vuelva al menu."],
     "Llega y vuelve golpeando los pads correspondientes.",
     "Lo hace sin ayuda y sin golpear un pad que diga otra cosa de la que buscaba.", 7),

    ("CU-07", "Leer la pantalla de informacion y volver",
     "En el menu, con la fila de cinco pads a la vista y el participante de frente.",
     ["Golpear INFO.", "Leer la pantalla.", "Volver al menu."],
     "El texto se lee completo sin que la fila de pads lo tape, y la salida esta donde ya "
     "estaba mirando.",
     "Lee sin tener que moverse y vuelve sin buscar la salida.", 7),

    ("CU-08", "Elegir ritmo y velocidad en dos pasos",
     "En el menu. El catalogo tiene cuatro ritmos y cada uno tres tempos.",
     ["Golpear TOCAR.", "Elegir un ritmo.", "Elegir una velocidad."],
     "La pista arranca con el ritmo y el tempo elegidos.",
     "Entiende que el segundo paso es la velocidad del mismo ritmo y no otro ejercicio. Se "
     "registra si pregunta.", 7),

    ("CU-09", "Tocar una pista completa",
     "Pista elegida. Dos compases de entrada antes de la primera nota.",
     ["Tocar de principio a fin sin parar."],
     "La pista termina y aparece la pantalla de resultados. El volcado de sesion queda escrito "
     "en el visor.",
     "Termina la pista y existe el archivo de sesion correspondiente. La precision no es "
     "criterio de aceptacion: es el dato.", 9),

    ("CU-10", "Leer el veredicto sin dejar de ver el pad",
     "Tocando una pista.",
     ["Observar donde aparece el resultado de cada golpe."],
     "El veredicto aparece sobre la pieza golpeada, con su color.",
     "El participante sabe decir si acerto o fallo sin haber levantado la vista del kit.", 1),

    ("CU-11", "Encontrar una pieza fuera del campo de vision",
     "Tocando una pista que usa una pieza de los extremos.",
     ["Esperar a que toque una pieza que queda fuera de la vista."],
     "El borde de la pantalla se ilumina del lado donde esta la pieza.",
     "Gira la cabeza hacia la luz sin que nadie se lo diga.", 1),

    ("CU-12", "Entrar y salir del modo libre",
     "En el menu. El participante ya toco al menos una pista, para que la ausencia de notas "
     "y de puntuacion sea un contraste y no lo normal.",
     ["Golpear LIBRE.", "Tocar lo que quiera.", "Salir al menu."],
     "Toca el kit completo sin notas ni puntuacion, y encuentra la salida, que cuelga del kit "
     "y no de la fila del menu.",
     "Encuentra la salida sin ayuda. Es el caso donde la salida NO esta donde en las demas "
     "pantallas, asi que es el que mas probable es que falle.", 7),

    ("CU-13", "Leer sus resultados y decidir",
     "Pista terminada.",
     ["Leer el resumen.", "Elegir repetir o volver al menu."],
     "Entiende que dicen los numeros y la opcion que golpea es la que queria.",
     "Sabe explicar con sus palabras que midio la aplicacion. Si confunde las dos constancias "
     "-la del ritmo y la del pulso propio-, el texto no esta claro.", 9),

    ("CU-14", "Salir de la aplicacion",
     "En el menu, al final de la sesion. Es el ultimo caso a proposito: cierra la "
     "aplicacion.",
     ["Golpear SALIR."],
     "La aplicacion se cierra con la cortinilla de despedida.",
     "El pad que dice SALIR hace salir. Es el caso que existe porque este defecto ya ocurrio: "
     "ver OBS-01.", 7),

    ("CU-15", "Terminar la sesion sin malestar",
     "Sesion completa, entre 15 y 20 minutos.",
     ["Al acabar, preguntar por mareo, fatiga visual, cansancio de brazo y comodidad del "
      "visor, de 1 a 5."],
     "El participante termina la sesion sin malestar que le haga pararse.",
     "Ningun participante interrumpe por malestar. Es la actividad QV.5 y la contesta la "
     "persona, no el sistema.", 10),
]


# ------------------------------------------------------------------- observaciones reales
#
# (id, fecha, que se observo, causa, gravedad, area, estado, evidencia)
#
# GRAVEDAD: Critica deja al participante sin poder seguir o le hace creer algo falso.
#           Alta estorba la tarea o falsea lo que la aplicacion mide.
#           Media molesta sin impedir.      Baja es acabado.
#
# El texto entre comillas angulares es el REPORTE LITERAL de quien lo encontro.

OBSERVACIONES = [
    ("OBS-01", "2026-10-20",
     "Los pads de la pantalla de resultados seguian diciendo TUTORIAL, TOCAR y SALIR mientras "
     "sus acciones eran OTRA VEZ y MENU. Reporte literal: «le di a salir y me salio el de "
     "tocar».",
     "El rotulo y la accion de cada pad se escribian en dos sitios distintos.",
     "Critica", "Interfaz / UX/UI", "Corregida",
     "Los rotulos pasan a ser una tabla por pantalla, con prueba que comprueba que ninguna "
     "opcion miente. Commit fix(menu): los pads no tenian nada que ver"),

    ("OBS-02", "2026-10-20",
     "Al entrar a tocar, el bombo perdio su guia y dejo de marcar el golpe y el momento de "
     "golpear. Reporte literal: «cuando presiono tocar el bombo perdio como su guia y ahora no "
     "me marca cuando lo toco ni cuando lo deberia de tocar».",
     "La lista de pads del generador de notas tenia cuatro piezas y le faltaban el bombo y el "
     "hi-hat: tres de cada cuatro notas del patron no tenian destino.",
     "Critica", "Juego de ritmo", "Corregida",
     "El constructor del kit barre la escena y rellena TODA lista de pads. Commit fix(ritmo): "
     "el bombo no tenia pad en el spawner"),

    ("OBS-03", "2026-10-20",
     "El aro de anticipacion se cerraba tan rapido que no servia de aviso. Reporte literal: "
     "«el aro va demaciado rapido».",
     "Los valores de afinado del componente nunca llegaron a la escena: la anticipacion "
     "serializada era 0 y quedaba recortada al minimo. Iba doce veces mas rapido de lo "
     "disenado.",
     "Alta", "Juego de ritmo", "Corregida",
     "Los valores viven en constantes, el constructor los escribe en la escena y una prueba de "
     "escena comprueba que llegaron. Commit fix(ritmo): el afinado del aro nunca llego a la "
     "escena"),

    ("OBS-04", "2026-10-20",
     "El aro crecia hacia fuera y pisaba el aro de la pieza vecina.",
     "El radio inicial superaba la distancia al centro del pad mas cercano, que son 32.5 cm.",
     "Alta", "Juego de ritmo", "Corregida",
     "El aro nace en el borde y se cierra hacia dentro, con el veredicto pintado de vuelta en "
     "el borde. Commit fix(ritmo): el aro iba hacia fuera y pisaba al vecino"),

    ("OBS-05", "2026-10-21",
     "Con dos golpes casi seguidos en la misma pieza, el segundo aro no se veia. Reporte "
     "literal: «el segundo practicamente no se veia, solo sabia que habia q tocarlo porque ya "
     "lo habia hecho antes».",
     "Habia un solo aro por pieza: el segundo sobrescribia al primero.",
     "Media", "Juego de ritmo", "Corregida",
     "Los aros se acumulan, hasta cuatro por pieza, como los circulos de osu. Dimensionado "
     "midiendo el intervalo minimo entre golpes de la misma pieza en las pistas: 250 ms. "
     "Commit feat(ritmo): los aros se acumulan"),

    ("OBS-06", "2026-10-20",
     "El paso del pulso del tutorial era infranqueable: fallaba 9 de 9 corridas.",
     "El acompanamiento se callaba al empezar el turno del participante, asi que el paso pedia "
     "reproducir de memoria en vez de sincronizar.",
     "Alta", "Interfaz / UX/UI", "Corregida",
     "El acompanamiento sigue sonando durante el turno. Commit fix(tutorial): el paso del "
     "pulso pedia memoria, no sincronizacion"),

    ("OBS-07", "2026-10-20",
     "Una excepcion durante el tutorial lo dejaba muerto, sin rastro y sin mensaje: el "
     "participante se quedaba mirando una escena quieta.",
     "El registro de Unity no llega al visor, asi que la excepcion no dejaba constancia en "
     "ningun sitio.",
     "Critica", "Interfaz / UX/UI", "Corregida",
     "Traza a archivo y guardas en el conductor del tutorial. Commits fix(tutorial): una "
     "excepcion dejaba el tutorial muerto sin rastro; feat(diagnostico): traza en archivo"),

    ("OBS-08", "2026-10-20",
     "Tres ranuras vacias en la lista de pads mataban el tutorial sin ningun aviso.",
     "El cableado por menu dejaba huecos y nada los validaba.",
     "Critica", "Interfaz / UX/UI", "Corregida",
     "Validacion en el arranque y prueba de escena que comprueba el montaje entero. Commit "
     "fix(tutorial): tres ranuras vacias en pads lo mataban sin rastro"),

    ("OBS-09", "2026-10-19",
     "El tutorial se arrancaba dos veces y el menu no llegaba a aparecer.",
     "Dos componentes lanzaban el tutorial por su cuenta.",
     "Critica", "Interfaz / UX/UI", "Corregida",
     "El conductor de la aplicacion es el unico que arranca estados. Commit fix(flujo): el "
     "tutorial se arrancaba dos veces y el menu no llegaba"),

    ("OBS-10", "2026-10-18",
     "El tutorial quedaba invisible porque el juego arrancaba al mismo tiempo encima.",
     "Las dos escenas se montaban a la vez.",
     "Critica", "Interfaz / UX/UI", "Corregida",
     "Commit fix(tutorial): el juego arrancaba a la vez y hacia el tutorial invisible"),

    ("OBS-11", "2026-10-17",
     "El panel del marcador aparecia a dieciseis metros, ilegible.",
     "Posicion local colgando de un objeto que estaba a (1.87, 0, 15.98): una posicion local "
     "solo vale si controlas donde esta el padre.",
     "Alta", "Juego de ritmo", "Corregida",
     "El panel se ancla al kit. Commit fix(ritmo): anclar el panel al kit"),

    ("OBS-12", "2026-10-17",
     "El patron era injugable: cuatro notas por segundo con dos baquetas, y el hi-hat caia en "
     "el mismo pulso que el bombo exigiendo las dos manos a la vez.",
     "La densidad del patron se eligio sin medirla contra lo que una persona puede tocar.",
     "Alta", "Juego de ritmo", "Corregida",
     "Una nota por pulso, dos por segundo, y el acompanamiento marca el pulso en vez de "
     "competir. Commit feat(practica): los patrones de practica como datos"),

    ("OBS-13", "2026-10-17",
     "El veredicto MISS era inalcanzable por las dos vias: ni una nota no golpeada ni un golpe "
     "fuera de ventana lo producian.",
     "El emparejador busca DENTRO de la ventana de fallo y el juez solo devuelve fallo FUERA: "
     "se excluian. Y una nota no golpeada se contaba sin avisar a nadie.",
     "Alta", "Juego de ritmo", "Corregida",
     "Commit fix(ritmo): el MISS era inalcanzable por las dos vias"),

    ("OBS-14", "2026-10-17",
     "Los fallos de las primeras notas no median precision: median que la cancion agarro al "
     "participante desprevenido.",
     "La pista arrancaba sin cuenta de entrada.",
     "Alta", "Juego de ritmo", "Corregida",
     "Dos compases de entrada antes de la primera nota. Commit fix(ritmo): anadir compases de "
     "entrada"),

    ("OBS-15", "2026-10-18",
     "El reloj corria a 80 pulsos por minuto y el mapa de notas declaraba 79.98: el desfase se "
     "acumulaba a lo largo de la pista.",
     "El tempo se escribia en dos sitios.",
     "Alta", "Musica", "Corregida",
     "Una sola definicion, de la que salen el audio y el mapa. Commit fix(ritmo): el reloj iba "
     "a 80 BPM y el beatmap a 79.98"),

    ("OBS-16", "2026-11-06",
     "Tres de las pistas eran la misma. Reporte literal: «en la de rock donde solo varia el "
     "tempo son lo mismo, no varia nada».",
     "Habia tres entradas de rock con el patron copiado: tres archivos distintos en el disco y "
     "la misma pista en el visor.",
     "Media", "Musica", "Corregida",
     "El cuerpo de cada ritmo se escribe una vez y se toca a tres tempos; el selector los "
     "ofrece como lento, medio y rapido del mismo ritmo. Commit feat(practica): cuatro ritmos "
     "a tres tempos"),

    ("OBS-17", "2026-11-10",
     "La pantalla de informacion prometia beneficios que el proyecto ya habia retirado.",
     "El texto seguia describiendo el marco de rehabilitacion motriz, retirado antes del corte "
     "de medio curso.",
     "Alta", "Experiencia emocional", "Corregida",
     "El texto dice que mide si tocas a tiempo y que no sustituye a un terapeuta, y hay una "
     "lista de frases prohibidas que lo vigila. Commit fix(info): el texto deja de prometer lo "
     "que el proyecto retiro"),

    ("OBS-18", "2026-11-06",
     "En el modo libre no se veia por donde salir.",
     "La salida del modo libre no esta en la fila del menu, y nada la senalaba.",
     "Media", "Interfaz / UX/UI", "Corregida",
     "El modo libre senala su salida. Commit fix(ui): el modo libre senala su salida"),

    ("OBS-19", "2026-11-10",
     "La fila de pads tapaba el pie de la pantalla de informacion.",
     "La distancia del panel estaba fijada a mano y no salia del alto del bloque de texto.",
     "Baja", "Interfaz / UX/UI", "Corregida",
     "Commit fix(info): la distancia del panel sale del alto del bloque"),

    ("OBS-20", "2026-10-20",
     "Los rotulos del menu no se leian: el menu mostraba un tamano de letra y la escena tenia "
     "otro.",
     "Los cambios de tamano nunca llegaron a la escena serializada.",
     "Media", "Interfaz / UX/UI", "Corregida",
     "Tamanos medidos y escritos por el constructor. Commits fix(ui): tamanos de texto "
     "medidos, no estimados; fix(ui): los cambios de tamano nunca llegaron a la escena"),

    ("OBS-21", "2026-11-06",
     "El kit del tutorial no cabia entero en el campo de vision: habia que girar para ver las "
     "piezas de los extremos mientras el tutorial pedia atencion al centro.",
     "El tutorial usaba el kit completo de siete piezas.",
     "Media", "Interfaz / UX/UI", "Corregida",
     "El kit del tutorial baja a cuatro piezas. Commit feat(tutorial): el kit del tutorial "
     "baja a cuatro piezas"),

    ("OBS-22", "2026-11-04",
     "El rotulo del tutorial salia en una sola linea larga, dificil de leer en el visor.",
     "No habia reparto en renglones.",
     "Baja", "Interfaz / UX/UI", "Corregida",
     "Commit feat(tutorial): el rotulo se parte en renglones"),

    ("OBS-23", "2026-10-18",
     "El kit quedaba hundido bajo la tarima del escenario.",
     "La altura del kit se fijo antes de que existiera la tarima.",
     "Media", "Entorno 3D y assets", "Corregida",
     "Commit fix(entorno): el kit quedaba hundido bajo la tarima del escenario"),

    ("OBS-24", "2026-10-18",
     "Un cuadro parpadeaba en el suelo durante toda la sesion.",
     "Dos superficies a la misma altura competian por el mismo pixel.",
     "Baja", "Entorno 3D y assets", "Corregida",
     "Commit fix(entorno): el cuadro que parpadeaba en el suelo era z-fighting"),

    ("OBS-25", "2026-10-18",
     "Las montanas del horizonte invadian el claro donde esta la bateria.",
     "Se colocaban por altura y no por su huella en el suelo.",
     "Baja", "Entorno 3D y assets", "Corregida",
     "Commit fix(entorno): las montanas invadian el claro"),

    ("OBS-26", "2026-10-19",
     "Un pad apagado seguia registrando golpes.",
     "La deteccion no consultaba si el pad estaba activo.",
     "Media", "Desarrollo VR y bateria", "Corregida",
     "Commit fix(golpe): un pad apagado ya no se detecta"),

    ("OBS-27", "2026-11-08",
     "Los paneles aparecian encima del jugador, y las pistas no sonaban a su tempo.",
     "La posicion del panel y el tempo de la pista se resolvian por separado del selector.",
     "Media", "Interfaz / UX/UI", "Corregida",
     "Commit fix: cada pista suena a su tempo, y los paneles dejan de aparecer sobre el "
     "jugador"),

    ("OBS-28", "2026-11-04",
     "El tiempo hasta el primer golpe, que es dato de la medida de exito 6, no se medía de "
     "verdad.",
     "El cronometro arrancaba en el momento equivocado.",
     "Media", "QA, documentacion y gestion", "Corregida",
     "Commit fix(tutorial): el tiempo hasta el primer golpe se medira de verdad"),

    ("OBS-29", "2026-10-17",
     "La constancia del pulso medía los fallos en vez de la constancia.",
     "Se calculaba sobre los golpes juzgados y no sobre los intervalos entre golpes propios.",
     "Alta", "QA, documentacion y gestion", "Corregida",
     "Dos constancias separadas, con una prueba que impide que alguien las implemente iguales. "
     "Commit fix(metricas): la constancia del pulso medía los fallos"),

    ("OBS-30", "2026-10-18",
     "Repetir el tutorial era imposible en el visor: una vez completado, la marca de visto no "
     "se podia borrar.",
     "La marca se guardaba como preferencia de Unity, y las preferencias de una compilacion de "
     "Android no se pueden borrar sin acceso de raiz.",
     "Media", "Interfaz / UX/UI", "Corregida",
     "La marca es un archivo, y hay un comando que la borra. Commit fix(tutorial): la marca de "
     "visto era irrecuperable en el visor"),
]


# ------------------------------------------------------------------------------ pendiente

PENDIENTE = [
    ("Atribucion a los 14 participantes",
     "El volcado de sesion no lleva identificador de participante. Hace falta la lista que "
     "llevo quien facilito las pruebas: fecha, hora de inicio y en que visor.",
     "QT.8"),
    ("En que visor corrieron las sesiones",
     "El Quest 3S no tiene ningun volcado posterior al 11-nov-2026. Si las pruebas corrieron "
     "en el Quest 3, hay que conectarlo y recoger sus archivos.",
     "QT.8"),
    ("Respuestas de comodidad",
     "Las cuatro preguntas de CU-15 -mareo, fatiga visual, cansancio de brazo y comodidad del "
     "visor, de 1 a 5- las contesta la persona. No hay ningun dato del sistema que las "
     "sustituya.",
     "QV.5"),
    ("Observaciones de los participantes",
     "Lo que dijeron durante y despues de su sesion. Las 30 observaciones de este documento "
     "son hallazgos del desarrollo, no de las sesiones con los 14.",
     "QE.2"),
]


# -------------------------------------------------------------------------------- derivados

GRAVEDADES = ["Critica", "Alta", "Media", "Baja"]


def por_gravedad():
    out = {g: [] for g in GRAVEDADES}
    for o in OBSERVACIONES:
        out[o[4]].append(o)
    return out


def por_area():
    out = {}
    for o in OBSERVACIONES:
        out.setdefault(o[5], []).append(o)
    return dict(sorted(out.items(), key=lambda x: -len(x[1])))


def por_medida():
    out = {}
    for c in CASOS:
        out.setdefault(c[6], []).append(c[0])
    return dict(sorted(out.items()))


def abiertas():
    return [o for o in OBSERVACIONES if o[6] != "Corregida"]


if __name__ == "__main__":
    print("%d casos de uso, %d observaciones, %d sin corregir"
          % (len(CASOS), len(OBSERVACIONES), len(abiertas())))
    print()
    print("por gravedad:")
    for g, v in por_gravedad().items():
        print("  %-8s %2d" % (g, len(v)))
    print("por area:")
    for a, v in por_area().items():
        print("  %-30s %2d" % (a, len(v)))
    print("casos por medida de exito:")
    for m, v in por_medida().items():
        print("  medida %-2d  %s" % (m, ", ".join(v)))
    print()
    print("PENDIENTE DE DATO: %d" % len(PENDIENTE))
    for t, _, act in PENDIENTE:
        print("  %-6s %s" % (act, t))
