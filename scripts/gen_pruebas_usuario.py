# -*- coding: utf-8 -*-
"""Genera el documento 16: pruebas con usuarios, casos de uso y registro de observaciones.

Cubre QT.8 (protocolo y casos), QE.2 (registro), QE.3 (gravedad y prioridad), QE.4 (reparto
por area) y la parte cuantitativa de QI.1 que ya se puede sostener.

NINGUNA CIFRA SE ESCRIBE A MANO: las observaciones salen de pruebas_usuario.py y los numeros
de sesiones.py, que lee los volcados reales del visor.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import neutro
import pruebas_usuario as PU
import sesiones as S

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")
DOC = os.path.join(SALIDA, "16_Pruebas_con_Usuarios.docx")
FECHA = "18 de noviembre de 2026"

MEDIDAS = {
    1: "Precision ritmica medible en el golpe",
    6: "Un usuario nuevo aprende a usarlo sin ayuda",
    7: "La aplicacion se recorre entera sin quedarse encerrado",
    9: "Metricas de sesion exportables",
    10: "Seguridad y comodidad de uso",
}


def doc():
    d = neutro.nuevo()
    r = S.resumen()

    neutro.portada(
        d, "Pruebas con usuarios",
        "Casos de uso, protocolo y registro de observaciones",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha", FECHA),
         ("Actividades", "QT.8 · QE.2 · QE.3 · QE.4 · parte de QI.1")])

    # ------------------------------------------------------------------ 0
    neutro.H(d, "Qué contiene este documento y qué le falta", 1)
    neutro.P(d,
        "Este documento reúne los %d casos de uso con los que se prueba la aplicación, el "
        "protocolo de una sesión, el registro de las %d observaciones recogidas durante el "
        "desarrollo con su gravedad y su área responsable, y el análisis de las %d sesiones "
        "completas que quedaron registradas en el visor."
        % (len(PU.CASOS), len(PU.OBSERVACIONES), r["sesiones"]))
    neutro.P(d, "Lo que todavía no está, y se declara en vez de rellenarse:", bold=True)
    neutro.table(d, ["Qué falta", "Por qué no se puede deducir", "Actividad"],
                 [[t, p, a] for t, p, a in PU.PENDIENTE],
                 widths=[4.0, 8.6, 2.4], fs=8, negritas_col0=True)
    neutro.P(d,
        "El volcado de sesión lleva fecha, tempo, notas, precisión, constancia y los desfases "
        "crudos. No lleva identificador de participante, así que con los archivos se puede "
        "agrupar por sesión pero no por persona. Y la comodidad la contesta quien se pone el "
        "visor: no hay ningún dato del sistema que la sustituya. Atribuir sesiones a "
        "participantes o escribir respuestas de comodidad sin esos dos registros sería "
        "inventar la evidencia que este documento existe para sostener.")

    # ------------------------------------------------------------------ 1
    neutro.H(d, "1. Los casos de uso", 1)
    neutro.P(d,
        "Cada caso cobra una medida de éxito de la carta sponsor. Un caso que no cobra ninguna "
        "no está, que es el mismo criterio con el que se hizo el recorte de alcance.")
    neutro.table(d, ["Medida de éxito", "Casos"],
                 [["%d. %s" % (m, MEDIDAS.get(m, "")), ", ".join(cs)]
                  for m, cs in PU.por_medida().items()],
                 widths=[7.0, 8.0], fs=9, negritas_col0=True)

    for cid, titulo, pre, pasos, esperado, criterio, medida in PU.CASOS:
        neutro.H(d, "%s — %s" % (cid, titulo), 2)
        neutro.table(d, ["", ""], [
            ["Precondición", pre],
            ["Pasos", "\n".join("%d. %s" % (i + 1, p) for i, p in enumerate(pasos))],
            ["Resultado esperado", esperado],
            ["Criterio de aceptación", criterio],
            ["Cobra la medida", "%d. %s" % (medida, MEDIDAS.get(medida, ""))],
            ["Resultado observado", "PENDIENTE — se llena con la sesión de cada participante"],
        ], widths=[3.6, 11.4], fs=9, negritas_col0=True)

    # ------------------------------------------------------------------ 2
    neutro.H(d, "2. Protocolo de una sesión", 1)
    neutro.P(d,
        "Entre 15 y 20 minutos por participante. El facilitador no interviene salvo por "
        "seguridad: cada intervención se anota, porque una explicación de viva voz invalida el "
        "caso CU-02, que mide justamente si la aplicación se entiende sola.", bold=True)
    neutro.bullets(d, [
        "Antes: explicar en qué consiste, que se puede parar en cualquier momento sin "
        "consecuencias, y que no se graba audio ni vídeo. Anotar la hora de inicio y el visor.",
        "Comprobar que la marca de tutorial visto está borrada, para que el tutorial arranque "
        "solo. Sin eso, CU-01 y CU-02 no se pueden observar.",
        "Dejar que recorra los casos CU-01 a CU-14 en orden, sin guiarlo. Anotar cada pregunta "
        "y cada vez que se queda detenido más de diez segundos.",
        "Al terminar, las cuatro preguntas de comodidad de CU-15, de 1 a 5.",
        "Después: recoger los volcados del visor y anotar en la hoja de participantes la hora "
        "de inicio, para poder emparejar cada archivo con su sesión.",
    ], num=True)
    neutro.P(d,
        "El último paso es el que falta en las sesiones ya corridas, y es el que impide "
        "atribuir los archivos a los participantes.")

    # ------------------------------------------------------------------ 3
    neutro.H(d, "3. Registro de observaciones", 1)
    neutro.P(d,
        "Las %d observaciones recogidas usando la aplicación en el visor a lo largo del "
        "desarrollo, del 17 de octubre al 10 de noviembre. No son hallazgos de las sesiones "
        "con los participantes: son hallazgos de uso propios, y por eso cada uno lleva su "
        "fecha y la evidencia de su corrección. Varios llevan el reporte literal de quien lo "
        "encontró." % len(PU.OBSERVACIONES))
    neutro.table(d, ["Id", "Fecha", "Qué se observó", "Gravedad", "Área", "Estado"],
                 [[o[0], o[1], o[2], o[4], o[5], o[6]] for o in PU.OBSERVACIONES],
                 widths=[1.2, 1.6, 7.0, 1.4, 2.4, 1.4], fs=7)

    neutro.H(d, "3.1 Clasificación por gravedad", 2)
    neutro.P(d,
        "Crítica deja al participante sin poder seguir, o le hace creer algo falso. Alta "
        "estorba la tarea o falsea lo que la aplicación mide. Media molesta sin impedir. Baja "
        "es acabado.")
    pg = PU.por_gravedad()
    neutro.table(d, ["Gravedad", "Cuántas", "Cuáles"],
                 [[g, str(len(v)), ", ".join(o[0] for o in v)] for g, v in pg.items()],
                 widths=[2.2, 1.6, 11.2], fs=9, negritas_col0=True)
    neutro.P(d,
        "Las %d críticas comparten forma: ninguna se parecía a su causa. Un pad que decía "
        "SALIR y llevaba al menú, un tutorial que moría sin dejar rastro, el bombo que dejaba "
        "de marcar porque una lista tenía cuatro piezas en vez de seis. Por eso la respuesta a "
        "casi todas no fue corregir el síntoma sino poner una prueba que vigile la causa: los "
        "rótulos pasaron a ser una tabla comprobable, el cableado se verifica en batchmode, y "
        "los valores de afinado se escriben en la escena desde una sola constante."
        % len(pg["Critica"]))

    neutro.H(d, "3.2 Reparto por área", 2)
    neutro.table(d, ["Área", "Cuántas", "Cuáles"],
                 [[a, str(len(v)), ", ".join(o[0] for o in v)]
                  for a, v in PU.por_area().items()],
                 widths=[4.2, 1.4, 9.4], fs=9, negritas_col0=True)
    pa = PU.por_area()
    mayor = next(iter(pa))
    neutro.P(d,
        "%s concentra %d de las %d, el %.0f %%. No es casual: es el área que llegó al final "
        "del proyecto, y la que un participante ve antes que cualquier otra cosa. El entorno, "
        "la música y el desarrollo de la batería —lo que se construyó primero— suman %d."
        % (mayor, len(pa[mayor]), len(PU.OBSERVACIONES),
           100.0 * len(pa[mayor]) / len(PU.OBSERVACIONES),
           sum(len(v) for a, v in pa.items()
               if a in ("Entorno 3D y assets", "Musica", "Desarrollo VR y bateria"))))

    neutro.H(d, "3.3 Estado", 2)
    neutro.P(d,
        "Las %d están corregidas, cada una con su commit. No queda ninguna abierta, y eso es "
        "una afirmación verificable: el identificador de la corrección está en la columna de "
        "evidencia del anexo." % len(PU.OBSERVACIONES))

    # ------------------------------------------------------------------ 4
    neutro.H(d, "4. Las sesiones registradas en el visor", 1)
    neutro.P(d,
        "Datos reales, leídos de los volcados que la aplicación escribe en el visor. "
        "Se cuentan solo las pistas completas, de %d notas o más: las de menos son arranques "
        "de prueba y hundirían la media sin medir nada." % S.MINIMO_NOTAS)
    neutro.table(d, ["", ""], [
        ["Sesiones completas", str(r["sesiones"])],
        ["Fechas", "del %s al %s" % (fecha_larga(r["fechas"][0]), fecha_larga(r["fechas"][-1]))],
        ["Notas presentadas", str(r["notas"])],
        ["Notas acertadas", str(r["aciertos"])],
        ["Precisión global", "%.1f %%" % r["precision_global"]],
        ["Precisión por sesión", "mínima %.1f %% · mediana %.1f %% · máxima %.1f %%"
                                 % (r["precision_min"], r["precision_mediana"],
                                    r["precision_max"])],
        ["Constancia contra la rejilla", "mediana %.1f ms" % r["rejilla_mediana"]],
        ["Constancia del pulso propio", "mediana %.1f ms" % r["pulso_mediana"]],
        ["Tempos tocados", ", ".join("%g BPM" % b for b in r["bpm"])],
        ["Volcados de tutorial", str(len(S.tutoriales()))],
    ], widths=[5.0, 10.0], fs=9, negritas_col0=True)

    neutro.P(d, "Las dos constancias miden cosas distintas, y conviene no leerlas como una.",
             bold=True)
    neutro.P(d,
        "La constancia contra la rejilla dice qué tan parejo se pega el golpe al patrón. La "
        "del pulso propio dice qué tan regular es el espacio entre los golpes de la propia "
        "persona. Se puede ir treinta milisegundos atrasado todo el tiempo y tener un pulso "
        "perfectamente estable: son dos resultados distintos y la mediana de las sesiones los "
        "pone en %.1f y %.1f milisegundos."
        % (r["rejilla_mediana"], r["pulso_mediana"]))
    neutro.P(d,
        "La precisión mínima de %.1f %% es una sesión real y no un error de medición: "
        "corresponde a una corrida con el patrón que resultó injugable, el de cuatro notas por "
        "segundo que la observación OBS-12 documenta. Está en la muestra porque retirarla "
        "dejaría el dato más bonito y menos cierto." % r["precision_min"])

    neutro.H(d, "4.1 Qué no se puede concluir de estos números", 2)
    neutro.bullets(d, [
        "No miden a 14 participantes. Son %d sesiones sin identificador de persona, y la "
        "mayoría son de desarrollo: el 18 de octubre concentra una cuarta parte de ellas."
        % r["sesiones"],
        "No son una curva de aprendizaje. Para eso hace falta saber qué sesiones son del mismo "
        "participante y en qué orden, que es exactamente el dato que falta.",
        "Sí sostienen que el sistema registra lo que dice registrar, que es la medida de éxito "
        "9: hay %d notas juzgadas y %d archivos con sus desfases crudos, reanalizables."
        % (r["notas"], r["sesiones"]),
    ])

    # ------------------------------------------------------------------ 5
    neutro.H(d, "5. Qué hace falta para cerrar estas actividades", 1)
    neutro.table(d, ["Actividad", "Qué le falta", "Quién lo tiene"], [
        ["QT.8", "La lista de los 14 participantes con fecha y hora de inicio, y en qué visor "
                 "corrió cada sesión.", "Quien facilitó las pruebas"],
        ["QE.2", "Lo que los participantes reportaron durante y después de su sesión.",
         "Quien facilitó las pruebas"],
        ["QE.3", "Nada: se clasifica en cuanto QE.2 tenga contenido.", "Se deriva"],
        ["QE.4", "Nada: se reparte por área en cuanto QE.3 esté.", "Se deriva"],
        ["QV.5", "Las cuatro respuestas de comodidad de CU-15, de los 14.",
         "Quien facilitó las pruebas"],
        ["QI.1", "Las sesiones atribuidas. La parte del sistema ya está en la sección 4.",
         "Se deriva"],
    ], widths=[2.0, 9.0, 4.0], fs=9, negritas_col0=True)

    # ------------------------------------------------------------------ anexo
    neutro.H(d, "Anexo. Las observaciones con su causa y su evidencia", 1)
    for o in PU.OBSERVACIONES:
        neutro.P(d, "%s · %s · %s · %s" % (o[0], o[1], o[4], o[5]), bold=True, after=2)
        neutro.P(d, o[2], after=2)
        neutro.P(d, "Causa: %s" % o[3], after=2)
        neutro.P(d, "Evidencia: %s" % o[7], italic=True, after=10)

    return d


MES = {"09": "septiembre", "10": "octubre", "11": "noviembre"}


def fecha_larga(aaaammdd):
    return "%d de %s" % (int(aaaammdd[6:8]), MES.get(aaaammdd[4:6], aaaammdd[4:6]))


if __name__ == "__main__":
    if S.resumen() is None:
        raise SystemExit("No hay volcados de sesion. Corre quest.sh pull en el repo Unity.")
    doc().save(DOC)
    print("OK", DOC)
    print("   %d casos de uso · %d observaciones · %d sesiones reales · %d pendientes de dato"
          % (len(PU.CASOS), len(PU.OBSERVACIONES), S.resumen()["sesiones"], len(PU.PENDIENTE)))
