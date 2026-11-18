# -*- coding: utf-8 -*-
"""Genera el manual de usuario. Cierra QM.1.

EL LECTOR ES EL PARTICIPANTE DE LAS PRUEBAS, no el equipo. Alguien que se pone el visor
quince minutos y quiza nunca uso realidad virtual. De ahi tres reglas de redaccion:

  - Nada de nombres de archivo, de clase ni de comando. Si hace falta decirlo, va en el
    manual tecnico.
  - Una accion por paso, y el paso dice que vas a VER, no que hace el sistema.
  - La seccion de problemas esta escrita por sintoma -«no suena»-, no por causa, porque el
    sintoma es lo unico que el lector tiene.

Los rotulos de los pads salen de la cache de datos del repo Unity, no se teclean: un manual
que diga TOCAR donde el pad dice JUGAR es peor que no tener manual.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import capturas
import manual_datos
import neutro

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")
DOC = os.path.join(SALIDA, "15_Manual_Usuario.docx")
D = manual_datos.DATOS
FECHA = "18 de noviembre de 2026"

# Nombre que el usuario ve, por pieza del recorrido del tutorial.
PIEZAS = {
    "HiHat": "el hi-hat, el platillo de dos piezas que está a tu izquierda",
    "Tarola": "la tarola, el tambor del centro",
    "Bombo": "el bombo, el tambor grande de abajo",
    "Platillo": "el platillo grande de la derecha",
}

PASOS = {
    "PasoPrimerGolpe": (
        "Tu primer golpe",
        "Una baqueta transparente baja sola y golpea un tambor para enseñarte el movimiento. "
        "Después te toca a ti: golpea ese mismo tambor. No hay prisa y no se puede fallar."),
    "PasoRecorrerKit": (
        "Conocer la batería",
        "Se ilumina una pieza a la vez y tú la golpeas. Así recorres las piezas principales y "
        "aprendes dónde está cada una sin tener que buscarlas después."),
    "PasoSeguirPulso": (
        "Seguir el pulso",
        "Suena un pulso constante, como un metrónomo, y tú golpeas al mismo tiempo. Con "
        "acertar unos cuantos basta para pasar: no hace falta hacerlo perfecto."),
    "PasoIntensidades": (
        "Suave, medio y fuerte",
        "Aquí se trata de la fuerza, no del tiempo. Golpea suave, luego medio, luego fuerte. "
        "Un rótulo te dice qué pieza registró y con cuánta fuerza, así que puedes ver si el "
        "sistema te está entendiendo."),
}


def doc():
    d = neutro.nuevo()

    neutro.portada(
        d, "Manual de usuario",
        "Batería virtual — cómo usarla",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Equipo", "Equipo A"),
         ("Versión de la aplicación", D["version"]),
         ("Fecha", FECHA),
         ("Actividad", "QM.1 — Manual básico de usuario")])

    neutro.P(d,
        "Esto es una batería que se toca de verdad, con las manos, dentro de unas gafas de "
        "realidad virtual. Siete piezas al alcance de los brazos. Sirve para tocar y "
        "desahogarse: golpear con ritmo descarga tensión, y la música da a dónde ir cuando uno "
        "no sabría por dónde empezar.")
    neutro.P(d,
        "No mide tu salud ni sustituye a un terapeuta. Lo único que mide es si tocas a tiempo.",
        bold=True)
    neutro.P(d,
        "No hace falta saber tocar la batería. No hace falta haber usado gafas de realidad "
        "virtual. La aplicación empieza enseñándote.")

    # ------------------------------------------------------------------ 1
    neutro.H(d, "1. Antes de empezar", 1)
    neutro.table(d, ["Qué", "Cuánto"], [
        ["Tiempo", "Entre 15 y 20 minutos, contando el tutorial"],
        ["Espacio", "Un metro y medio alrededor de ti, de pie o sentado en un banco sin "
                    "respaldo. No hace falta caminar."],
        ["Qué llevas puesto", "Las gafas y un control en cada mano"],
        ["Si usas lentes", "Caben debajo de las gafas. Si molestan, dilo y se ajusta la "
                           "separación."],
    ], widths=[4.0, 11.0], fs=9, negritas_col0=True)

    neutro.H(d, "1.1 Cómo ponerte las gafas", 2)
    neutro.bullets(d, [
        "Pásate la cinta por la cabeza y ajústala hasta que las gafas se sostengan solas, sin "
        "que tengas que apretarlas contra la cara.",
        "Mueve las gafas un poco arriba y abajo hasta que la imagen se vea nítida. Si se ve "
        "borrosa, casi siempre es que están demasiado altas.",
        "Los controles se agarran como se agarraría una baqueta: la correa en la muñeca, para "
        "que no salgan volando.",
    ], num=True)

    neutro.H(d, "1.2 Las dos cosas que hacen los controles", 2)
    neutro.P(d,
        "Solo dos, y ninguna es un botón. Los controles son las baquetas:")
    neutro.bullets(d, [
        "Mover el brazo para golpear una pieza. El golpe cuenta por el movimiento, no por "
        "apretar nada.",
        "Golpear fuerte o suave cambia el volumen, igual que en una batería de verdad.",
    ])
    neutro.P(d,
        "Vas a sentir una vibración en la mano cada vez que golpees. Es la confirmación de que "
        "el golpe se registró.")

    neutro.H(d, "1.3 Un aviso sobre el malestar", 2)
    neutro.P(d,
        "Algunas personas sienten mareo o náusea en realidad virtual. Aquí el riesgo es bajo "
        "porque no te mueves por el espacio: estás quieto y la batería está delante de ti. "
        "Aun así, si notas mareo, calor o incomodidad, quítate las gafas y dilo. No hay que "
        "aguantarlo y detenerse no arruina nada.", bold=True)
    neutro.P(d,
        "Verás también un círculo dibujado en el suelo a tu alrededor. Es el límite de tu "
        "espacio: mientras estés dentro, no vas a chocar con nada.")

    # ------------------------------------------------------------------ 2
    neutro.H(d, "2. Lo primero que vas a ver", 1)
    neutro.P(d,
        "La aplicación abre con un fundido y, la primera vez, entra directa al tutorial. No "
        "tienes que elegir nada todavía.")
    capturas.inserta(d, neutro, "01_bienvenida")

    neutro.H(d, "2.1 El tutorial son cuatro pasos", 2)
    neutro.P(d,
        "Cada paso te enseña antes de pedirte nada: primero lo ves hecho, luego lo haces tú. "
        "Si no sale, se repite; el tutorial no te deja atrás.")
    archivos = ["02_tutorial_primer_golpe", "03_tutorial_recorrer_kit",
                "04_tutorial_pulso", "05_tutorial_intensidades"]
    for i, paso in enumerate(D["tutorial"]["pasos"]):
        titulo, texto = PASOS.get(paso, (paso, ""))
        neutro.P(d, "Paso %d — %s" % (i + 1, titulo), bold=True, after=4)
        neutro.P(d, texto)
        if paso == "PasoRecorrerKit":
            neutro.P(d, "Las piezas que recorre, en orden:", after=4)
            neutro.bullets(d, [PIEZAS.get(p, p) for p in D["tutorial"]["recorrido"]], num=True)
        if i < len(archivos):
            capturas.inserta(d, neutro, archivos[i])

    neutro.P(d,
        "Al terminar los cuatro pasos pasas al menú. El tutorial no vuelve a salir solo, pero "
        "puedes repetirlo cuando quieras desde el menú.")

    # ------------------------------------------------------------------ 3
    neutro.H(d, "3. El menú: una fila de pads que se golpean", 1)
    neutro.P(d,
        "No hay botones ni punteros. Las opciones son %d discos en fila delante de ti, cada "
        "uno con su palabra escrita, y se eligen golpeándolos con la baqueta, igual que una "
        "pieza de la batería." % D["plazas"])
    neutro.P(d,
        "Los discos no se mueven de sitio entre pantallas. El que está a la izquierda sigue "
        "estando a la izquierda siempre; lo único que cambia es lo que dice.", bold=True)
    capturas.inserta(d, neutro, "06_menu")

    menu = D["filas"].get("Menu", {})
    neutro.table(d, ["Dice", "Qué pasa si lo golpeas"],
                 [[menu.get(i, ["—"])[0], QUE_HACE.get(menu.get(i, ["—"])[0], "")]
                  for i in range(D["plazas"])],
                 widths=[3.0, 12.0], fs=9, negritas_col0=True)

    neutro.H(d, "3.1 La pantalla de información", 2)
    neutro.P(d,
        "Cuenta qué es la aplicación, para qué sirve y a quién se le deben los sonidos y el "
        "escenario. Se sale golpeando el disco del centro, que dice MENÚ.")
    capturas.inserta(d, neutro, "07_info")

    # ------------------------------------------------------------------ 4
    neutro.H(d, "4. Tocar una pista", 1)
    neutro.P(d, "Se elige en dos pasos, y en los dos puedes volver al menú.")

    neutro.H(d, "4.1 Primero, qué ritmo", 2)
    neutro.P(d,
        "Cuatro ritmos, de más sencillo a más difícil. El primero es un pulso básico: una "
        "pieza cada dos tiempos. Si nunca has tocado, empieza por ése.")
    capturas.inserta(d, neutro, "08_seleccion_ritmo")

    neutro.H(d, "4.2 Después, qué tan rápido", 2)
    neutro.P(d,
        "El mismo ritmo a tres velocidades: lento, medio y rápido. No son tres ejercicios "
        "distintos, es el mismo más o menos difícil. Empieza por el lento aunque te parezca "
        "fácil: el rápido no perdona.")
    capturas.inserta(d, neutro, "09_seleccion_velocidad")

    neutro.H(d, "4.3 Qué ves mientras toca la música", 2)
    neutro.P(d,
        "Antes de la primera nota suenan dos compases de entrada, para que te enganches al "
        "ritmo. Después, sobre cada pieza que vas a tener que golpear aparece un aro que se va "
        "cerrando hacia el centro. Cuando el aro llega al centro, es el momento de golpear.")
    neutro.P(d,
        "Si la pieza que toca está fuera de tu campo de visión, el borde de la pantalla se "
        "ilumina del lado donde está. Gira la cabeza hacia la luz.")
    capturas.inserta(d, neutro, "10_tocando")

    neutro.H(d, "4.4 El color te dice cómo fue", 2)
    neutro.P(d,
        "El resultado aparece sobre la pieza que acabas de golpear, no en un panel lejano, "
        "para que no tengas que dejar de ver lo que estás tocando.")
    neutro.table(d, ["Color", "Palabra", "Qué significa"], [
        ["Verde", "PERFECT", "Diste justo a tiempo."],
        ["Amarillo", "GOOD", "Un poco antes o un poco después, pero cuenta."],
        ["Rojo", "MISS", "Demasiado lejos del tiempo, o no golpeaste."],
    ], widths=[2.6, 2.6, 9.8], fs=9, negritas_col0=True)
    neutro.P(d,
        "Fallar no interrumpe nada: la pista sigue y la siguiente nota llega igual. Nadie "
        "hace una pista entera en verde la primera vez.")
    capturas.inserta(d, neutro, "11_veredicto")
    neutro.P(d,
        "Una pista empezada se toca hasta el final. No hay salida al menú a mitad de la "
        "canción, porque lo que se compara entre participantes es la misma pista tocada "
        "entera. Si quieres tocar sin que se mida nada, eso es el modo libre, y se elige antes.")

    # ------------------------------------------------------------------ 5
    neutro.H(d, "5. Modo libre: tocar sin que te midan", 1)
    neutro.P(d,
        "La batería completa, sin notas que seguir, sin aros y sin puntuación. Nada se mide y "
        "nada se guarda. Es para golpear lo que quieras, al ritmo que quieras, el tiempo que "
        "quieras.")
    neutro.P(d,
        "La salida está señalada junto a la batería, no en la fila de discos del menú.")
    capturas.inserta(d, neutro, "12_libre")

    # ------------------------------------------------------------------ 6
    neutro.H(d, "6. Tus resultados", 1)
    neutro.P(d,
        "Al acabar una pista aparece un resumen. Va dicho en palabras además de en números, "
        "porque un número suelto no dice si estuvo bien.")
    capturas.inserta(d, neutro, "13_resultados")
    neutro.table(d, ["Lo que dice", "Qué significa"], [
        ["Cuántas notas acertaste",
         "De todas las que pasaron, cuántas golpeaste dentro de tiempo."],
        ["Tu precisión",
         "Lo mismo en porcentaje. Sirve para compararte contigo mismo en la siguiente pista, "
         "no con nadie más."],
        ["Qué tan parejo le diste al ritmo",
         "Si tus golpes caen siempre a la misma distancia del tiempo marcado. Un número "
         "pequeño es mejor."],
        ["Qué tan estable es tu pulso",
         "Si el espacio entre tus propios golpes es regular. Se puede ir un poco atrasado todo "
         "el tiempo y tener un pulso perfectamente estable: son dos cosas distintas y se miden "
         "aparte."],
    ], widths=[5.0, 10.0], fs=9, negritas_col0=True)
    res = D["filas"].get("Resultados", {})
    etiquetas = [res[i][0] for i in sorted(res)]
    neutro.P(d,
        "Desde aquí puedes golpear %s para repetir la misma pista, o %s para volver al menú."
        % (etiquetas[0] if etiquetas else "OTRA VEZ",
           etiquetas[1] if len(etiquetas) > 1 else "MENÚ"))

    # ------------------------------------------------------------------ 7
    neutro.H(d, "7. Si algo va mal", 1)
    neutro.P(d,
        "Por síntoma, que es lo que tú puedes ver. Si nada de esto lo arregla, dilo: es "
        "información útil para el equipo y no es culpa tuya.")
    neutro.table(d, ["Lo que notas", "Qué hacer"], [
        ["Golpeo y no suena nada",
         "Comprueba que estás golpeando la pieza y no el aire delante de ella. Las piezas "
         "están más cerca de lo que parecen. Si sigue sin sonar, avisa."],
        ["Suena pero no me marca el golpe",
         "Puede que el movimiento sea demasiado corto. Levanta más el brazo antes de bajar: "
         "el golpe se mide por la velocidad con la que entras."],
        ["No encuentro la pieza que me pide",
         "Mira el borde de la pantalla: se ilumina del lado donde está. Gira la cabeza hacia "
         "esa luz."],
        ["La imagen se ve borrosa",
         "Mueve las gafas un poco arriba y abajo hasta que se enfoque. Suele ser que están "
         "demasiado altas."],
        ["Siento mareo, calor o náusea",
         "Quítate las gafas y dilo. No hay que aguantarlo. Parar no arruina la prueba."],
        ["Me salí del círculo del suelo",
         "Vuelve al centro. Ese círculo es tu espacio libre de obstáculos."],
        ["Le di a un disco y pasó otra cosa",
         "Avísalo diciendo qué decía el disco y qué pasó. Es exactamente el tipo de fallo que "
         "estas pruebas buscan."],
        ["Quiero volver a ver el tutorial",
         "Golpea el primer disco del menú, el que dice %s." % (
             D["filas"].get("Menu", {}).get(0, ["TUTORIAL"])[0])],
    ], widths=[5.0, 10.0], fs=9, negritas_col0=True)

    # ------------------------------------------------------------------ 8
    neutro.H(d, "8. Qué se guarda de ti y qué no", 1)
    neutro.P(d,
        "La aplicación guarda, dentro del propio visor, los datos de cómo tocaste: en qué "
        "momento cayó cada golpe, con cuánta fuerza, y los resúmenes de cada pista. Eso es lo "
        "que se analiza.")
    neutro.table(d, ["Se guarda", "No se guarda"], [
        ["Los tiempos y la fuerza de tus golpes", "Tu nombre"],
        ["El resumen de cada pista que toques", "Ninguna grabación de audio"],
        ["Cuánto tardaste en cada paso del tutorial", "Ningún video ni imagen tuya"],
        ["Qué pistas elegiste", "Nada de lo que hagas en modo libre"],
    ], widths=[7.5, 7.5], fs=9)
    neutro.P(d,
        "Los archivos no salen del visor hasta que alguien del equipo los descarga, y van "
        "identificados por la fecha y hora de la sesión, no por quién la hizo. Si prefieres "
        "que no se usen tus datos, dilo y se descartan.")

    faltan = capturas.faltantes()
    if faltan:
        neutro.H(d, "Nota para el equipo, no para el lector", 1)
        neutro.P(d,
            "Faltan %d de las %d capturas de pantalla. Cada hueco de este documento dice qué "
            "pantalla va ahí y cómo tomarla. El ciclo es: tomar las capturas en el visor, "
            "bajarlas con la herramienta del repositorio, renombrarlas y regenerar este "
            "documento. Esta sección desaparece sola cuando no falte ninguna."
            % (len(faltan), len(capturas.MANIFIESTO)))
        neutro.bullets(d, ["%s — %s" % (m[0], m[2]) for m in faltan])

    return d


QUE_HACE = {
    "TUTORIAL": "Repite la explicación de cuatro pasos. Puedes volver a ella cuando quieras.",
    "INFO": "Cuenta qué es la aplicación y de dónde salen los sonidos y el escenario.",
    "TOCAR": "Elegir una pista y tocarla. Esto es lo que se mide.",
    "LIBRE": "La batería sin notas y sin puntuación, para tocar lo que quieras.",
    "SALIR": "Cierra la aplicación.",
}


if __name__ == "__main__":
    if D is None:
        raise SystemExit("No hay cache de datos. Corre: python3 manual_datos.py --refrescar")
    doc().save(DOC)
    faltan = capturas.faltantes()
    print("OK", DOC)
    if faltan:
        print("   FALTAN %d de %d capturas. Cada hueco queda rotulado en el documento."
              % (len(faltan), len(capturas.MANIFIESTO)))
        print("   Corre: python3 capturas.py  para ver qué nombre lleva cada una.")
