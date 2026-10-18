# -*- coding: utf-8 -*-
"""Comprobaciones del cambio de enfoque. Que el documento no se contradiga a sí mismo."""
import os
import re
import sys
import unittest
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enfoque

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def texto(docx):
    x = zipfile.ZipFile(os.path.join(RAIZ, "entregables", docx)).read("word/document.xml")
    t = re.sub(r"<[^>]+>", " ", x.decode("utf8"))
    return re.sub(r"\s+", " ", t)


class Pasajes(unittest.TestCase):
    def test_el_texto_original_existe_en_el_documento_que_se_cita(self):
        """Si el pasaje citado no está, la sustitución es inverificable.

        Es el defecto más fácil de cometer aquí: citar de memoria algo parecido a lo que dice
        el documento, y que el lector no pueda encontrarlo para comprobarlo.
        """
        fuentes = {"Carta sponsor": "01_Carta_Sponsor.docx",
                   "Acta constitutiva": "02_Acta_Constitutiva.docx"}
        for doc, seccion, antes, _ in enfoque.PASAJES:
            t = texto(fuentes[doc])
            limpio = re.sub(r"\s+", " ", antes).strip()
            self.assertIn(limpio, t,
                          "No encuentro en %s (%s) el texto citado: %r" % (doc, seccion, limpio[:70]))

    def test_el_texto_nuevo_no_repite_el_marco_retirado(self):
        retirado = re.compile(
            r"rehabilitaci[oó]n motri|motri[zc] de miembro|amplitud de movimiento|"
            r"validaci[oó]n cl[ií]nica|asesor terap[eé]utico externo", re.I)
        for doc, seccion, _, despues in enfoque.PASAJES:
            # El caso del asesor habla del retiro, que es legítimo nombrarlo.
            if "retirado" in despues.lower():
                continue
            self.assertIsNone(retirado.search(despues),
                              "El texto nuevo de %s (%s) sigue usando el marco retirado" % (doc, seccion))

    def test_cada_pasaje_cambia_de_verdad(self):
        for doc, seccion, antes, despues in enfoque.PASAJES:
            self.assertNotEqual(antes.strip(), despues.strip(),
                                "%s (%s) declara un cambio que no cambia nada" % (doc, seccion))


class Coherencia(unittest.TestCase):
    def test_la_medida_8_consta_como_retirada_en_el_recorte(self):
        """El documento 10 ya la retiró. Si no fuera así, este documento la retiraría dos veces."""
        import recorte
        self.assertEqual(recorte.MEDIDA_RETIRADA, 8)

    def test_no_se_declara_sin_cambio_algo_que_si_cambia(self):
        """Las medidas 8 y 9 cambian, así que no pueden aparecer en la lista de lo que no cambia."""
        texto_no_cambia = " ".join(a + " " + b for a, b in enfoque.NO_CAMBIA).lower()
        self.assertNotIn("medida de éxito 8", texto_no_cambia)
        self.assertNotIn("medida 9", texto_no_cambia)

    def test_hay_renuncias_declaradas(self):
        """Un cambio que solo tiene ventajas no se analizó, se justificó."""
        self.assertGreaterEqual(len(enfoque.RENUNCIAS), 3)

    def test_cada_accion_tiene_responsable_y_plazo(self):
        for accion, quien, cuando in enfoque.ACCIONES:
            self.assertTrue(quien.strip(), "Acción sin responsable: %s" % accion)
            self.assertTrue(cuando.strip(), "Acción sin plazo: %s" % accion)

    def test_cada_motivo_esta_argumentado(self):
        for titulo, cuerpo in enfoque.MOTIVOS:
            self.assertGreater(len(cuerpo), 120,
                               "El motivo %r es una afirmación, no un argumento" % titulo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
