# -*- coding: utf-8 -*-
"""
Las dos trampas que tenia el generador de los documentos 07 y 08.

Ninguna daba error: las dos producian un documento equivocado en silencio, que es la unica
clase de defecto que llega a una entrega con firma debajo.
"""
import os
import sys

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_validacion.py")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def fuente():
    return open(RUTA, encoding="utf-8").read()


def test_ya_no_genera_la_seccion_retirada():
    """El equipo retiro la seccion 3.1 el 21-sep. El generador la siguio produciendo un mes,
    compensandolo con un comentario que decia que habia que quitarla a mano."""
    assert "3.1 Nota sobre las cifras" not in fuente(), \
        "el generador vuelve a producir la seccion 3.1, que el equipo retiro"


def test_los_dos_documentos_son_alcanzables_desde_la_linea_de_comandos():
    """El __main__ estaba colocado ANTES de def lista(), asi que el documento 08 no se podia
    regenerar en absoluto: la funcion ni existia cuando main corria."""
    src = fuente()
    i_main = src.index('if __name__ == "__main__":')
    for fn in ("def carta():", "def lista():", "def main("):
        assert src.index(fn) < i_main, f"{fn} se define despues del __main__"


def test_regenerar_un_entregable_fechado_exige_pedirlo_a_proposito():
    """Las cifras se leen del cronograma, que avanza; la fecha del documento no. Correr el
    generador sin mas produciria las cifras de hoy bajo la fecha de la entrega."""
    import gen_validacion
    antes = {}
    for nombre in ("07_Carta_Validacion_Entregables.docx",
                   "08_Lista_Verificacion_Compromisos.docx"):
        ruta = os.path.join(gen_validacion.SALIDA, nombre)
        antes[nombre] = os.path.getmtime(ruta) if os.path.exists(ruta) else None

    assert gen_validacion.main([]) == 1, "sin --regenerar deberia negarse y devolver 1"

    for nombre, mtime in antes.items():
        ruta = os.path.join(gen_validacion.SALIDA, nombre)
        ahora = os.path.getmtime(ruta) if os.path.exists(ruta) else None
        assert ahora == mtime, f"{nombre} se reescribio sin pedirlo"


def test_la_fecha_del_documento_esta_declarada_y_no_es_la_de_hoy():
    """Si alguien pone HOY en datetime.now(), el seguro deja de tener sentido: el documento
    se fecharia solo y nadie notaria que cambio de cifras."""
    import gen_validacion
    assert isinstance(gen_validacion.HOY, str) and gen_validacion.HOY.strip()
    import datetime
    assert str(datetime.date.today().year) not in gen_validacion.HOY or \
        "septiembre" in gen_validacion.HOY, \
        "HOY parece calcularse sola; debe ser la fecha con la que se entrego"
