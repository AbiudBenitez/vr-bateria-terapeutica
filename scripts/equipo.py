# -*- coding: utf-8 -*-
"""Quién es quién en el Equipo A. Fuente única de los nombres.

POR QUE EXISTE ESTE MODULO. Los nombres estaban escritos a mano en cada generador, y en el
del acta estaban MAL: la tabla de aprobación y el anexo A nombraban a «Ricardo Alejandro
Rodríguez Ríos» como gerente, a «Jesús Eduardo Rodríguez Salinas» como coordinador —ninguno
de los dos está en el equipo— y a Abiud Misael Benítez como director con el apellido
equivocado, «Muñoz» en vez de «Franco». El acta es el documento que se firma y el que lleva
el anexo de asignación por paquete, así que el error aparecía 42 veces y en el bloque de
firmas.

Es el mismo defecto que este proyecto ya pagó dos veces con cifras —el presupuesto con dos
valores en dos documentos y el cronograma declarando fechas que no eran— y la misma solución:
el dato vive en un sitio y los documentos lo leen. `gen_validacion.py` y `gen_r14.py` tenían
la plantilla correcta; ahora los tres leen de aquí.

LOS ROLES SON LOS DEL ACTA, no los del trabajo que acabó haciendo cada quien. La diferencia
está documentada: el acta asigna el desarrollo de realidad virtual a María Fernanda y lo
ejecutó Misael. Un acta no se reescribe para que coincida con lo que pasó después; se anota
la desviación. Ver la nota de revisión del enfoque para el mismo criterio.
"""

# (rol como lo escribe el acta, nombre completo, nombre de pila, forma abreviada)
PLANTILLA = [
    ("Director de proyecto", "Benjamín Ignacio Villalón Bobadilla",
     "Benjamín", "Benjamín I. Villalón"),
    ("Coordinador", "Sarai Galindo García",
     "Sarai", "Sarai Galindo"),
    ("Gerente de proyecto", "Abiud Misael Benítez Franco",
     "Misael", "Abiud M. Benítez"),
    ("Desarrollador VR", "María Fernanda Montoya Valdez",
     "Fernanda", "M. Fernanda Montoya"),
    ("Diseñador UX-XR", "Diana Laura Tello Salinas",
     "Diana", "Diana L. Tello"),
    ("Artista 3D", "Christian Salvador Valadez Gallegos",
     "Christian", "Christian S. Valadez"),
    ("Diseñador de audio", "Javier Alejandro Hernández Caloca",
     "Javier", "Javier A. Hernández"),
    ("Analista de métricas", "Kimberly González Sepúlveda",
     "Kimberly", "Kimberly González"),
]

PATROCINADORA = "Dra. Leticia Amalia Neira Tovar"

#: Nombre completo por rol del acta.
NOMBRE = {rol: completo for rol, completo, _, _ in PLANTILLA}

#: Forma abreviada por rol del acta.
ABREVIADO = {rol: corto for rol, _, _, corto in PLANTILLA}

#: Nombre de pila, que es como los nombran la hoja de control y el cronograma.
PILA = {rol: pila for rol, _, pila, _ in PLANTILLA}

#: Todos los nombres completos, para comprobar que un documento no nombre a nadie más.
NOMBRES = [completo for _, completo, _, _ in PLANTILLA]

# El asesor nunca se concretó: la medida de éxito 8 quedó retirada en el documento 10. Se
# conserva la entrada porque el acta lo declara como rol requerido y el anexo A le asigna
# paquetes; lo que no se puede es poner un nombre donde no hubo persona.
ASESOR_ROL = "Asesor terapéutico"
ASESOR = "Externo, por confirmar"
ASESOR_ABREVIADO = "Externo"

# La función de aseguramiento de calidad no es un rol de dedicación exclusiva: cada entregable
# lo revisa un integrante distinto de quien lo produjo.
QA_ABREVIADO = "rotativo entre el equipo"

#: Claves cortas que usan las columnas de responsable de la EDT, a forma abreviada.
#: Se resuelven por coincidencia parcial, así que el orden importa cuando una clave es
#: subcadena de otra.
CLAVES_CORTAS = [
    ("Gerente", ABREVIADO["Gerente de proyecto"]),
    ("Director", ABREVIADO["Director de proyecto"]),
    ("Coordinador", ABREVIADO["Coordinador"]),
    ("Dev RV", ABREVIADO["Desarrollador VR"]),
    ("UX-XR", ABREVIADO["Diseñador UX-XR"]),
    ("Artista 3D", ABREVIADO["Artista 3D"]),
    ("Audio", ABREVIADO["Diseñador de audio"]),
    ("Métricas", ABREVIADO["Analista de métricas"]),
    ("Asesor", ASESOR_ABREVIADO),
    ("QA", QA_ABREVIADO),
]

#: Nombre completo por rol, incluido el asesor, como lo pide el anexo A del acta.
NOMBRE_CON_ASESOR = dict(NOMBRE, **{ASESOR_ROL: ASESOR})

#: Filas del bloque de aprobación del acta: quién firma y con qué rol.
APROBACION = [
    (PATROCINADORA, "Patrocinadora"),
    (NOMBRE["Director de proyecto"], "Director de proyecto"),
    (NOMBRE["Gerente de proyecto"], "Gerente de proyecto"),
]

# NOMBRES QUE NO SON DEL EQUIPO Y ESTUVIERON EN EL ACTA HASTA EL 25-NOV-2026.
#
# Están aquí para que una prueba los busque. No volverán por mala fe: volverían porque alguien
# copie una tabla de una versión anterior del documento, que es exactamente cómo llegaron.
RETIRADOS = [
    "Ricardo Alejandro Rodríguez Ríos", "Ricardo A. Rodríguez",
    "Jesús Eduardo Rodríguez Salinas", "Jesús E. Rodríguez",
    "Benítez Muñoz",
]
