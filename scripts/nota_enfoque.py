# -*- coding: utf-8 -*-
"""Pinta la nota de revisión del enfoque al principio de un documento alcanzado por ella.

ESTA SEPARADO DE `enfoque.py` A PROPOSITO. Ahi vive el dato -que cambio, por que, que
pasajes- y aqui el formato. Es la misma division que el resto del proyecto: si manana la
nota tiene que entrar tambien en el documento 04, se llama a `poner` y nadie reescribe el
texto; y si cambia la redaccion, cambia en un solo sitio y los dos documentos la reflejan.

LA NOTA VA AL PRINCIPIO Y NO EN UN APENDICE. El defecto que arregla es que alguien lea la
carta sponsor o el acta y no se entere de que el encuadre cambio. Una advertencia al final
de cuarenta paginas no arregla eso.
"""
import enfoque
from neutro import H, P, table


def poner(doc, documento, salto=True):
    """Añade la nota al documento abierto. `documento` es la clave de `enfoque.PASAJES`.

    Devuelve el número de pasajes listados, para que quien la pone pueda imprimirlo y se vea
    en la consola si un documento se queda sin pasajes por un cambio de redacción.
    """
    titulo, parrafos, filas = enfoque.nota_de_revision(documento)

    H(doc, titulo, 1)
    for t in parrafos:
        P(doc, t)

    if filas:
        P(doc, "Pasajes de este documento que quedaron sustituidos", bold=True, after=4)
        table(doc, ["Sección", "Lo que pasa a decir"], filas,
              widths=[4.0, 11.5], fs=9)

    P(doc, "Dónde está el registro del cambio", bold=True, after=4)
    table(doc, ["Documento", "Qué contiene"], enfoque.REVISIONES,
          widths=[4.6, 10.9], fs=9)

    if salto:
        doc.add_page_break()

    return len(filas)
