# -*- coding: utf-8 -*-
"""Que la carta de validación no vuelva a traer lo que el equipo retiró, ni se regenere sola.

DOS DECISIONES QUE SOLO VIVIAN EN COMENTARIOS. La sección 3.1 de la carta —la nota que
conciliaba las cifras del documento de medio curso con las del cronograma— la retiró el
equipo el 21-sep, y durante un mes el generador la siguió produciendo con un comentario que
pedía quitarla a mano al regenerar. Se arregló el 21-oct. Lo segundo es que los documentos 07
y 08 están fechados el 21-sep con corte del 18-sep, pero sus cifras se leen del cronograma,
que avanza: regenerarlos hoy pone el avance de hoy bajo una fecha de hace dos meses, con una
línea de firma debajo.

Las dos estaban protegidas por código y por prosa, no por pruebas. Esta las fija.
"""
import os
import re
import subprocess
import sys
import unittest
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import validacion

ENTREGABLES = os.path.join(AQUI, "..", "entregables")
CARTA = "07_Carta_Validacion_Entregables.docx"


def texto(docx):
    x = zipfile.ZipFile(os.path.join(ENTREGABLES, docx)).read("word/document.xml")
    t = re.sub(r"<[^>]+>", " ", x.decode("utf8"))
    return re.sub(r"\s+", " ", t)


class LaSeccionRetirada(unittest.TestCase):
    def test_el_generador_no_escribe_la_seccion_tres_uno(self):
        """Se mira el CODIGO, no el documento: el documento no se regenera y pasaría igual."""
        with open(os.path.join(AQUI, "gen_validacion.py"), encoding="utf-8") as f:
            fuente = f.read()
        # Se buscan las dos formas en que se escribiría un encabezado de sección.
        for patron in (r'"3\.1[^"]*"', r"'3\.1[^']*'"):
            for hallado in re.findall(patron, fuente):
                self.fail("gen_validacion.py volvió a escribir una sección 3.1: %s" % hallado)

    def test_la_carta_entregada_no_la_lleva(self):
        self.assertNotIn("3.1", texto(CARTA))


class NoSeRegeneraSola(unittest.TestCase):
    def test_sin_el_argumento_no_escribe_nada_y_lo_explica(self):
        """Correrlo sin --regenerar tiene que salir con error y decir los tres pasos."""
        antes = os.path.getmtime(os.path.join(ENTREGABLES, CARTA))
        r = subprocess.run([sys.executable, os.path.join(AQUI, "gen_validacion.py")],
                           capture_output=True, text=True)
        despues = os.path.getmtime(os.path.join(ENTREGABLES, CARTA))

        self.assertNotEqual(r.returncode, 0, "salió con éxito sin pedirlo a propósito")
        self.assertEqual(antes, despues, "reescribió la carta sin --regenerar")
        self.assertIn("No se ha escrito nada", r.stdout)
        self.assertIn("superados", r.stdout, "no dice que hay que conservar el anterior")

    def test_las_cifras_de_hoy_ya_no_son_las_de_la_carta(self):
        """ES LA RAZON DE SER DEL SEGURO, y se comprueba en vez de suponerse.

        Si algún día volvieran a coincidir, el seguro seguiría siendo correcto pero esta
        prueba dejaría de demostrar por qué. Entonces habría que mirarla, no borrarla.
        """
        t = texto(CARTA)
        self.assertIn("77 de 257", t, "la carta entregada ya no declara el corte del 18-sep")

        r = validacion.resumen()
        self.assertNotEqual((r["hechas"], r["total"]), (77, 257),
                            "el cronograma sigue en el corte del 18 de septiembre")


if __name__ == "__main__":
    unittest.main(verbosity=2)
