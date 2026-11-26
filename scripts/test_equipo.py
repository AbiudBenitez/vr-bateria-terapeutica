# -*- coding: utf-8 -*-
"""Que los documentos no nombren a quien no está en el equipo.

POR QUE ESTA PRUEBA EXISTE. El acta -el documento que se firma- nombraba gerente a «Ricardo
Alejandro Rodríguez Ríos» y coordinador a «Jesús Eduardo Rodríguez Salinas», que no están en
el Equipo A, y daba a Abiud Misael Benítez el rol de director con el apellido equivocado.
Salía en la tabla de roles, en el bloque de aprobación y en las 42 filas del anexo de
asignación por paquete. Se detectó el 25-nov-2026, dos días antes de entregar la
documentación, al revisar el cierre.

No volverá por mala fe: volvería porque alguien copie una tabla de una versión anterior del
documento, que es exactamente cómo llegó. Por eso la comprobación es automática y por eso
`equipo.RETIRADOS` lleva los nombres que estuvieron ahí.
"""
import os
import re
import sys
import unittest
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import equipo

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ENTREGABLES = os.path.join(RAIZ, "entregables")


def texto(docx):
    x = zipfile.ZipFile(os.path.join(ENTREGABLES, docx)).read("word/document.xml")
    t = re.sub(r"<[^>]+>", " ", x.decode("utf8"))
    return re.sub(r"\s+", " ", t)


def todos_los_docx():
    return sorted(f for f in os.listdir(ENTREGABLES) if f.endswith(".docx"))


class NadieDeFuera(unittest.TestCase):
    def test_ningun_entregable_nombra_a_quien_no_esta_en_el_equipo(self):
        """Recorre TODOS los .docx, no una lista escrita a mano.

        Una lista de documentos a revisar se queda corta en cuanto entra uno nuevo, y el
        nuevo es justo el que nadie revisó.
        """
        for archivo in todos_los_docx():
            t = texto(archivo)
            for nombre in equipo.RETIRADOS:
                self.assertNotIn(nombre, t,
                                 "%s nombra a «%s», que no es del equipo" % (archivo, nombre))

    def test_la_plantilla_no_tiene_nombres_repetidos_ni_roles_repetidos(self):
        roles = [rol for rol, _, _, _ in equipo.PLANTILLA]
        self.assertEqual(len(set(roles)), len(roles), "hay un rol duplicado en la plantilla")
        self.assertEqual(len(set(equipo.NOMBRES)), len(equipo.NOMBRES),
                         "hay un nombre duplicado en la plantilla")
        self.assertEqual(len(equipo.PLANTILLA), 8, "el Equipo A son ocho integrantes")

    def test_ningun_retirado_coincide_con_alguien_de_la_plantilla(self):
        """Si un retirado fuera en realidad del equipo, la prueba de arriba lo expulsaría."""
        for nombre in equipo.RETIRADOS:
            for real in equipo.NOMBRES:
                self.assertNotEqual(nombre, real, nombre)


class ElActaNombraBien(unittest.TestCase):
    ACTA = "02_Acta_Constitutiva.docx"

    def test_el_bloque_de_aprobacion_lleva_los_roles_y_los_nombres_de_la_plantilla(self):
        t = texto(self.ACTA)
        for nombre, rol in equipo.APROBACION:
            self.assertIn(nombre, t, "el acta no nombra a %s" % nombre)
            self.assertIn(rol, t, "el acta no declara el rol %s" % rol)

    def test_el_gerente_es_quien_firma_como_gerente(self):
        """Era el error concreto: Abiud Misael Benítez figuraba como director."""
        self.assertEqual(equipo.NOMBRE["Gerente de proyecto"],
                         "Abiud Misael Benítez Franco")
        firmas = dict((rol, nombre) for nombre, rol in equipo.APROBACION)
        self.assertEqual(firmas["Gerente de proyecto"],
                         equipo.NOMBRE["Gerente de proyecto"])
        self.assertEqual(firmas["Director de proyecto"],
                         equipo.NOMBRE["Director de proyecto"])

    def test_los_ocho_integrantes_salen_en_la_tabla_de_roles(self):
        t = texto(self.ACTA)
        for nombre in equipo.NOMBRES:
            self.assertIn(nombre, t, "el acta no nombra a %s" % nombre)

    def test_el_anexo_usa_las_formas_abreviadas_de_la_plantilla(self):
        """El anexo A tiene 42 filas y las resuelve por clave corta."""
        t = texto(self.ACTA)
        for clave, abreviado in equipo.CLAVES_CORTAS:
            if abreviado in (equipo.ASESOR_ABREVIADO, equipo.QA_ABREVIADO):
                continue
            self.assertIn(abreviado, t,
                          "el anexo no usa «%s» para la clave %s" % (abreviado, clave))


# LA CARTA DE VALIDACION (documento 07) NO SE COMPRUEBA CONTRA LA PLANTILLA, a proposito.
#
# Su generador produce una seccion que el equipo decidio retirar el 21-sep, asi que el
# documento entregado NO se regenera -hay un aviso en `gen_validacion.py` y otro en
# `CLAUDE.md`-. La version entregada lleva un bloque de firmas con una sola fila, la de la
# docente, y exigirle los tres nombres de la plantilla seria exigir un estado al que solo se
# llega regenerandolo, o sea deshaciendo una decision del equipo para que pase una prueba.
#
# Lo que si se le exige es lo unico que importa aqui: que no nombre a nadie de fuera, y eso
# lo cubre `test_ningun_entregable_nombra_a_quien_no_esta_en_el_equipo`, que recorre todos
# los .docx. La tabla de firmas de su generador quedo conectada a `equipo.py` para cuando
# alguien resuelva lo de la seccion 3.1 y vuelva a generarlo.


if __name__ == "__main__":
    unittest.main(verbosity=2)
