# -*- coding: utf-8 -*-
"""Genera el documento de cambio de enfoque terapéutico."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enfoque
import neutro

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")


def doc():
    d = neutro.nuevo()

    neutro.portada(
        d,
        "Solicitud de cambio: enfoque terapéutico del proyecto",
        "Simulación de Batería en Realidad Virtual con Enfoque Terapéutico",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha de registro", enfoque.FECHA_REGISTRO),
         ("Proceso", "PMBOK 4.6 Control Integrado de Cambios")],
    )

    # ---------------------------------------------------------------- 1
    neutro.H(d, "1. Qué cambia", 1)
    neutro.P(d,
             "El proyecto deja de declararse como herramienta de apoyo a la rehabilitación "
             "motriz de miembro superior y pasa a declararse como herramienta de regulación "
             "emocional por medio de la ejecución rítmica.")
    neutro.P(d,
             "El cambio es de ENCUADRE, no de producto. El prototipo que se construye es el "
             "mismo: una batería virtual que suena al golpearla, con un juego de ritmo y un "
             "registro de métricas. Lo que cambia es qué afirma el proyecto sobre el beneficio "
             "que produce, y por tanto qué tiene que demostrar.")
    neutro.P(d,
             "La revisión 1 de la carta sponsor había situado el beneficio emocional como "
             "secundario. Pasa a ser el único declarado.")

    # ---------------------------------------------------------------- 2
    neutro.H(d, "2. Por qué se cambia", 1)
    for titulo, cuerpo in enfoque.MOTIVOS:
        neutro.P(d, titulo, bold=True, after=2)
        neutro.P(d, cuerpo)

    # ---------------------------------------------------------------- 3
    neutro.H(d, "3. Cuándo se decidió, y por qué se registra ahora", 1)
    neutro.P(d,
             f"La decisión se tomó {enfoque.FECHA_DECISION}. No se registró en ese momento: "
             "se habló, se actuó en consecuencia y el acuerdo no llegó a ningún documento.")
    neutro.P(d,
             "Entre la decisión y este registro median alrededor de cuatro semanas. Durante "
             "ellas, la carta sponsor y el acta constitutiva siguieron afirmando un marco que "
             "el equipo ya había abandonado, y el prototipo se construyó conforme al marco "
             "nuevo. Cualquiera que hubiera cruzado los documentos con el avance habría "
             "encontrado la contradicción sin explicación.")
    neutro.P(d,
             "Se deja constancia de la brecha en lugar de fechar hoy la decisión. Una decisión "
             "no registrada no es una decisión del proyecto, es un acuerdo de pasillo: no se "
             "puede auditar, no obliga a nadie y no sobrevive a que cambie quien la tomó. El "
             "hallazgo de gestión de este documento no es el cambio de enfoque, es haber "
             "tardado un mes en escribirlo.", italic=True)

    # ---------------------------------------------------------------- 4
    neutro.H(d, "4. Qué pasajes se sustituyen", 1)
    neutro.P(d,
             "Los documentos originales NO se editan. Un acta aprobada que se reescribe borra "
             "la evidencia de que hubo una decisión, que es justamente lo que el control de "
             "cambios conserva. Este documento se anexa a ellos y sustituye los pasajes "
             "siguientes.")
    neutro.table(
        d, ["Documento", "Sección", "Dice", "Pasa a decir"],
        [[doc_, sec, antes, despues] for doc_, sec, antes, despues in enfoque.PASAJES],
        widths=[2.3, 2.0, 5.6, 5.6], fs=8.0)
    neutro.caption(d, "Tabla 1. Pasajes sustituidos. El texto de la columna «Dice» es literal; "
                      "hay una prueba automatizada que lo verifica contra el archivo original.")

    # ---------------------------------------------------------------- 5
    neutro.H(d, "5. Qué no cambia", 1)
    neutro.P(d,
             "Acotar el cambio importa tanto como declararlo: sin esta sección, un lector "
             "razonable supondría que se movió más de lo que se movió.")
    neutro.table(d, ["Elemento", "Por qué no cambia"],
                 [[a, b] for a, b in enfoque.NO_CAMBIA],
                 widths=[4.0, 11.5], fs=9.0)

    # ---------------------------------------------------------------- 6
    neutro.H(d, "6. Qué pierde el proyecto", 1)
    neutro.P(d,
             "Un cambio que solo enumera ventajas no es un análisis, es una justificación. "
             "Estas son las renuncias.")
    neutro.table(d, ["Se pierde", "Alcance de la pérdida"],
                 [[a, b] for a, b in enfoque.RENUNCIAS],
                 widths=[4.0, 11.5], fs=9.0)

    # ---------------------------------------------------------------- 7
    neutro.H(d, "7. Efecto sobre las medidas de éxito", 1)
    neutro.table(
        d, ["#", "Medida", "Efecto"],
        [["1-7", "Identificación, detección, sonido, latencia, estabilidad, interacción, "
                 "intensidad", "Sin cambio. Se verifican igual bajo cualquier enfoque."],
         ["8", "Pertinencia terapéutica",
          "Retirada. Ya consta en el documento 10, Recorte de alcance."],
         ["9", "Registro de métricas",
          "Se reduce: salen precisión temporal y constancia del pulso; sale la amplitud de "
          "movimiento. Cerrada el 18 de octubre."],
         ["10", "Seguridad de uso", "Sin cambio."]],
        widths=[1.0, 4.5, 10.0], fs=9.0)
    neutro.P(d)
    neutro.P(d,
             "De las diez medidas originales quedan nueve verificables. Ocho dependen solo del "
             "sistema; la décima depende de lo que reporten los usuarios de prueba.")

    # ---------------------------------------------------------------- 8
    neutro.H(d, "8. Acciones derivadas", 1)
    neutro.table(d, ["Acción", "Responsable", "Plazo"],
                 [[a, b, c] for a, b, c in enfoque.ACCIONES],
                 widths=[8.0, 4.0, 3.5], fs=9.0)

    # ---------------------------------------------------------------- 9
    neutro.H(d, "9. Aprobación", 1)
    neutro.P(d,
             "Con la firma de este documento, el equipo deja constancia del cambio de enfoque "
             "y de la fecha en que se decidió, y la patrocinadora lo autoriza como anexo a la "
             "carta sponsor y al acta constitutiva.")
    neutro.P(d)
    neutro.table(d, ["Rol", "Nombre", "Firma"],
                 [["Patrocinadora", "Dra. Leticia Amalia Neira Tovar", "_" * 26],
                  ["Dirección de proyecto", "Sarai Galindo García", "_" * 26],
                  ["Gerencia de proyecto", "Abiud Misael Benítez Franco", "_" * 26],
                  ["QA y documentación", "Diana Laura Tello Salinas", "_" * 26],
                  ["Entorno 3D", "Kimberly González Sepúlveda", "_" * 26],
                  ["Sonido", "Christian Salvador Valadez Gallegos", "_" * 26],
                  ["Música", "Javier Alejandro Hernández Caloca", "_" * 26],
                  ["Experiencia emocional", "María Fernanda Montoya Valdez", "_" * 26]],
                 widths=[4.4, 6.6, 5.0], fs=9.0)

    ruta = os.path.join(SALIDA, "11_Cambio_de_Enfoque.docx")
    d.save(ruta)
    return ruta


if __name__ == "__main__":
    print(doc())
