# -*- coding: utf-8 -*-
"""Las capturas del manual de usuario: que pantallas hacen falta y como se insertan.

UN HUECO ROTULADO SE ARREGLA; UN HUECO SILENCIOSO SE ENTREGA. El manual de usuario se genera
con el visor desconectado, asi que `inserta()` pone la imagen si el archivo existe y, si no, un
recuadro que dice que pantalla falta y como tomarla. Nunca deja el sitio vacio sin avisar.

EL CICLO
    1. En el visor, dentro de la aplicacion: boton de Oculus + gatillo derecho.
    2. ./scripts/quest.sh capturas          las baja a entregables/capturas/
    3. python3 scripts/capturas.py          dice que nombre va en cada pantalla
    4. Renombrar cada archivo a ese nombre.
    5. python3 scripts/gen_manual_usuario.py

LOS NOMBRES NO SON LIBRES. El generador busca exactamente estos, porque la alternativa -que el
generador adivine por orden de fecha- pone la pantalla de resultados donde va el tutorial y
nadie lo nota hasta que el documento esta impreso.
"""
import os

from docx.shared import Cm

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join(AQUI, "..", "entregables", "capturas")

# (archivo sin extension, seccion del manual, pie de figura, como llegar a esa pantalla)
MANIFIESTO = [
    ("01_bienvenida", 2,
     "La cortinilla de bienvenida. Aparece sola al abrir la aplicación.",
     "Abre la aplicación y captura durante el fundido de entrada."),

    ("02_tutorial_primer_golpe", 2,
     "Primer paso del tutorial: una baqueta fantasma baja y golpea, y luego te toca a ti.",
     "La primera vez que se abre la aplicación el tutorial arranca solo. Si ya lo viste: "
     "./scripts/quest.sh tutorial y vuelve a abrir."),

    ("03_tutorial_recorrer_kit", 2,
     "Segundo paso: recorrer el kit. Se marca la pieza que toca y se espera tu golpe.",
     "Sigue el tutorial hasta el segundo paso."),

    ("04_tutorial_pulso", 2,
     "Tercer paso: seguir el pulso. El acompañamiento marca el tiempo y tú respondes.",
     "Sigue el tutorial hasta el tercer paso."),

    ("05_tutorial_intensidades", 2,
     "Cuarto paso: las tres intensidades. El rótulo dice qué pieza se registró y con qué "
     "fuerza.",
     "Sigue el tutorial hasta el cuarto paso."),

    ("06_menu", 3,
     "El menú. Cinco pads en fila: TUTORIAL, INFO, TOCAR, LIBRE y SALIR.",
     "Al terminar el tutorial se llega aquí. Captura de frente, con los cinco pads a la vista."),

    ("07_info", 3,
     "La pantalla de información: qué es la aplicación, para qué sirve y los créditos.",
     "En el menú, golpea INFO."),

    ("08_seleccion_ritmo", 4,
     "Primera pantalla del selector: qué ritmo quieres tocar.",
     "En el menú, golpea TOCAR."),

    ("09_seleccion_velocidad", 4,
     "Segunda pantalla del selector: qué tan rápido. Es el mismo ritmo a tres tempos.",
     "En el selector, elige un ritmo."),

    ("10_tocando", 4,
     "Tocando. El aro sobre cada pieza se cierra hasta el momento de golpear.",
     "Elige ritmo y velocidad. Captura con un aro a medio cerrar."),

    ("11_veredicto", 4,
     "El veredicto aparece sobre la pieza que golpeaste, no en un panel lejano.",
     "Mientras tocas, captura justo después de un golpe."),

    ("12_libre", 5,
     "Modo libre: el kit completo, sin notas y sin medición.",
     "En el menú, golpea LIBRE."),

    ("13_resultados", 6,
     "Los resultados de la sesión, dichos en palabras además de en números.",
     "Toca una pista hasta el final."),
]


def ruta(nombre):
    return os.path.join(CARPETA, nombre + ".png")


def existe(nombre):
    for ext in (".png", ".jpg", ".jpeg"):
        p = os.path.join(CARPETA, nombre + ext)
        if os.path.isfile(p):
            return p
    return None


def faltantes():
    return [m for m in MANIFIESTO if existe(m[0]) is None]


def inserta(doc, neutro, nombre):
    """Pone la captura en el documento, o un recuadro que dice cual falta."""
    entrada = next((m for m in MANIFIESTO if m[0] == nombre), None)
    if entrada is None:
        raise KeyError("captura no declarada en el manifiesto: %r" % nombre)
    _, _, pie, como = entrada
    p = existe(nombre)
    if p:
        doc.add_picture(p, width=Cm(14.0))
        doc.paragraphs[-1].alignment = neutro.C
        neutro.caption(doc, pie)
        return True
    # El recuadro se dibuja como una tabla de una celda: en Word se ve como un hueco con
    # borde, que es exactamente lo que es, y se borra de una vez al pegar la imagen.
    neutro.table(doc, ["FALTA ESTA CAPTURA — %s" % nombre],
                 [[pie], ["Cómo tomarla: %s" % como]],
                 widths=[14.0], fs=9)
    return False


if __name__ == "__main__":
    print("Carpeta: %s" % os.path.abspath(CARPETA))
    print("%d capturas declaradas, %d faltan\n" % (len(MANIFIESTO), len(faltantes())))
    print("%-28s %-4s %s" % ("archivo que debe existir", "§", "qué pantalla es"))
    for nombre, seccion, pie, como in MANIFIESTO:
        marca = "ok " if existe(nombre) else "FALTA"
        print("%-28s %-4s %-5s %s" % (nombre + ".png", seccion, marca, pie[:64]))
    if faltantes():
        print("\nPara tomarlas: boton de Oculus + gatillo derecho dentro de la aplicacion,")
        print("luego ./scripts/quest.sh capturas en el repo Unity, y renombra cada archivo")
        print("al nombre de la izquierda.")
