# -*- coding: utf-8 -*-
"""Revision de la fundamentacion contra lo que el prototipo hace. Cierra ET.2.

QUE ES ET.2 Y POR QUE NO ES REESCRIBIR ET.1
-------------------------------------------
`ET.1` redacto la fundamentacion teorica. `ET.2` es «revisar y actualizar la fundamentacion
segun el funcionamiento»: volver sobre cada afirmacion AHORA QUE EL PROTOTIPO EXISTE y decir,
una por una, si se sostiene con lo construido, si hay que acotarla, o si hay que retirarla.

La fundamentacion original esta en `docs/investigacion/evidencia-musicoterapia.md` y se cerro
el 18-oct. No se edita: igual que con el acta, lo que modifica algo ya escrito entra como
revision con su fecha. Reescribir el original borra la evidencia de que hubo una revision.

EL VEREDICTO DE CADA AFIRMACION
    sostenida   el prototipo hace lo que la afirmacion dice, y hay con que demostrarlo
    acotada     hace una parte. Se dice cual, y la afirmacion se reescribe mas estrecha
    retirada    no lo hace y no lo va a hacer en este alcance

NO SE INVENTA NINGUNA. Las ocho de abajo son las que la fundamentacion declara: los cuatro
marcos de NMT, las dos ventajas que prometen algo verificable y las dos limitaciones.
"""

# (id, afirmacion, de donde sale, veredicto, que hace el prototipo, como se comprueba)

AFIRMACIONES = [
    ("F-01", "RAS, Rhythmic Auditory Stimulation: base del metronomo y de la rampa de tempo",
     "Marcos formales de referencia, tabla de NMT",
     "acotada",
     "El metronomo existe y esta verificado. La RAMPA DE TEMPO no: la unica implementacion de "
     "la interfaz de tempo es de tempo constante, y las doce pistas van a 80, 100 y 120 pulsos "
     "por minuto fijos, elegidos por el usuario. No hay desplazamiento gradual de tempo dentro "
     "de una sesion.",
     "Desvio de 0.0 ms sostenido 205 s contra un metronomo de 120 BPM exactos. Y "
     "TempoConstante es la unica clase que implementa ITempoMap en todo el proyecto."),

    ("F-02", "TIMP, Therapeutic Instrumental Music Performance: colocacion espacial de los pads "
             "para forzar alcance y rango articular",
     "Marcos formales de referencia, tabla de NMT",
     "retirada",
     "Las siete piezas estan colocadas en el espacio al alcance de los brazos, pero «forzar "
     "alcance y rango articular» es una afirmacion de rehabilitacion de miembro superior, y "
     "ese marco se retiro antes del corte de medio curso. La disposicion que hay es la de una "
     "bateria, elegida para que se toque como una bateria, no para forzar un rango.",
     "La disposicion vive en DisposicionKit y la consume el constructor de la escena. "
     "El cambio de marco esta en el documento 11."),

    ("F-03", "PSE, Patterned Sensory Enhancement: guia visual sincronizada con el patron ritmico",
     "Marcos formales de referencia, tabla de NMT",
     "sostenida",
     "Es la afirmacion mejor sostenida de toda la fundamentacion, y el prototipo hace MAS de lo "
     "que prometia: un aro por nota que se cierra sobre la pieza hasta el instante de golpear, "
     "acumulando hasta cuatro notas seguidas, mas un aviso en el borde de la vision cuando la "
     "pieza que toca queda fuera del campo visual.",
     "AroDeNota y AvisoPeriferico, con sus pruebas. La sincronia se mide contra el mismo reloj "
     "de audio que agenda la musica, no contra el tiempo de fotograma."),

    ("F-04", "Iso-principio: medir el tempo espontaneo del usuario, empatarlo y desplazarlo "
             "gradualmente",
     "Marcos formales de referencia, tabla de NMT",
     "retirada",
     "No esta implementado y no entra en este alcance. El usuario elige entre tempos fijos; "
     "nada mide su tempo espontaneo. La herramienta de tempo que el proyecto tiene mide el BPM "
     "de una PISTA y si es estable, que es otra cosa. El protocolo que el acta describia "
     "-arrancar en el tempo propio, descender a 60 y cerrar con una fase respiratoria a 6 "
     "respiraciones por minuto- no llego a ser ninguna actividad del cronograma.",
     "La puerta queda abierta y verificada: ITempoMap son dos metodos de conversion, y hay una "
     "prueba con un mapa de dos tramos que pasa sin tocar codigo de produccion. Falta la "
     "implementacion y la interfaz, no la arquitectura."),

    ("F-05", "Configurabilidad clinica: pads reposicionables, alejar para forzar rango "
             "articular, reducir para trabajar precision",
     "Ventajas de la bateria virtual sobre la real",
     "acotada",
     "La disposicion se cambia en el codigo y se reconstruye la escena por menu, asi que es "
     "configurable para quien desarrolla. NO es reposicionable por el usuario ni por nadie "
     "durante una sesion: no hay ninguna pantalla para eso. Y la mitad sobre el rango articular "
     "cae con F-02.",
     "DisposicionKit y el comando del menu que construye el kit. No hay estado de la "
     "aplicacion para configurar el kit: son diez pantallas y ninguna es esa."),

    ("F-06", "Metricas que la bateria acustica no da: timing en milisegundos, fuerza de golpe, "
             "alcance, simetria izquierda/derecha y adherencia",
     "Ventajas de la bateria virtual sobre la real",
     "acotada",
     "Dos de las cinco. El timing en milisegundos esta, con los desfases crudos de cada golpe. "
     "La fuerza esta, en tres niveles por pieza. Las otras tres NO: el alcance se retiro con el "
     "marco motriz; la simetria izquierda/derecha necesitaria que el registro guardara de que "
     "mano o de que pieza vino cada golpe, y no lo guarda; y la adherencia necesita varias "
     "sesiones del mismo usuario, que es justo el dato que el registro no permite atribuir.",
     "El volcado de sesion lleva notas, aciertos, precision, las dos constancias y el arreglo "
     "de desfases. SessionStats.Resumen no tiene ningun campo de pieza, de mano ni de alcance."),

    ("F-07", "Limitacion: ausencia de retroalimentacion haptica real, compensada "
             "parcialmente con vibracion del mando, respuesta sonora inmediata y respuesta "
             "visual del pad",
     "Limitaciones reconocidas",
     "sostenida",
     "Se sostiene entera, y las tres compensaciones que nombra existen y estan medidas. La "
     "baqueta sigue atravesando el pad sin resistencia: es el hueco conocido y declararlo de "
     "antemano sigue siendo lo correcto.",
     "Vibracion del mando con intensidad por fuerza del golpe; respuesta sonora con un p90 de "
     "+4.07 ms contra una ventana de -10 a +25 ms; y destello en el pad golpeado."),

    ("F-08", "Limitacion: la validacion es un estudio de factibilidad y usabilidad, no un "
             "ensayo clinico controlado. Muestra pequena, de conveniencia, sesion unica y sin "
             "grupo control",
     "Limitaciones reconocidas",
     "sostenida",
     "Se sostiene, y hay que anadirle una limitacion mas que aparecio al recoger los datos: el "
     "volcado de sesion no lleva identificador de participante, asi que las sesiones "
     "registradas se pueden agrupar por sesion pero no por persona. Eso impide tanto la curva "
     "de aprendizaje como cualquier comparacion entre participantes.",
     "Documento 16, con la tabla de lo que falta de dato y quien lo tiene."),
]


# Lo que esta revision cambia en la fundamentacion, para quien venga a redactar QI.3.

CONSECUENCIAS = [
    ("El proyecto se ancla en PSE, no en los cuatro marcos",
     "De los cuatro marcos de NMT que la fundamentacion citaba, uno se sostiene entero (PSE), "
     "dos quedan acotados a una parte (RAS sin la rampa, y TIMP sin el rango articular) y uno "
     "se retira (iso-principio). Decir que el proyecto «se ancla en NMT» sin precisar cual es "
     "lo que haria que la fundamentacion no se sostenga al primer examen."),

    ("La evidencia motriz pasa de fundamento a antecedente",
     "Las filas de la tabla de evidencia que hablan de marcha, balance, hemiparesia y "
     "miembro superior post-EVC describen poblaciones y resultados que este proyecto ya no "
     "declara. No se borran -son el antecedente que justifica por que la percusion se estudia-, "
     "pero dejan de ser el fundamento de lo que el prototipo hace. El que lo sostiene es la "
     "fila psicosocial: regulacion emocional y bienestar en drum circles."),

    ("Los meta-analisis de RV en rehabilitacion post-EVC dejan de aplicar",
     "Se citaban para respaldar la eficacia del medio. Con el marco motriz retirado, respaldan "
     "una pregunta que el proyecto no hace. Lo que sigue valiendo de esa seccion es que ya "
     "existen sistemas que combinan RV con NMT con evaluaciones positivas de usabilidad, que "
     "es la clase de resultado que este proyecto si busca."),

    ("Dos metricas prometidas no existen y hay que decirlo en el informe",
     "La simetria izquierda/derecha y la adherencia aparecen en la fundamentacion como ventaja "
     "de la bateria virtual y el prototipo no las produce. La simetria es la mas cercana: "
     "bastaria con que el registro guardara de que pieza vino cada golpe. No se hace ahora "
     "porque cambiar el formato del volcado a estas alturas invalidaria las sesiones ya "
     "registradas."),
]


VEREDICTOS = ["sostenida", "acotada", "retirada"]

FUENTE = "docs/investigacion/evidencia-musicoterapia.md"
FECHA_ET1 = "18 de octubre de 2026"
FECHA_ET2 = "18 de noviembre de 2026"


def por_veredicto():
    out = {v: [] for v in VEREDICTOS}
    for a in AFIRMACIONES:
        out[a[3]].append(a)
    return out


if __name__ == "__main__":
    pv = por_veredicto()
    print("%d afirmaciones revisadas" % len(AFIRMACIONES))
    for v in VEREDICTOS:
        print("  %-10s %d  %s" % (v, len(pv[v]), ", ".join(a[0] for a in pv[v])))
    print()
    print("%d consecuencias para QI.3" % len(CONSECUENCIAS))
    for t, _ in CONSECUENCIAS:
        print("  -", t)
