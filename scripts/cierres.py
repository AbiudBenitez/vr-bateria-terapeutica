# -*- coding: utf-8 -*-
"""Fecha de registro de cada actividad cerrada, con su evidencia.

POR QUE EXISTE ESTE MODULO
--------------------------
Hasta el 11-nov-2026 los dos cronogramas no tenian ni una fecha real. `marcar_hechas.py`
cerraba cada actividad escribiendo `Stop = Finish`, o sea copiaba la fecha PLANEADA, y la
fecha verdadera quedaba solo dentro de la nota `[HECHA aaaa-mm-dd]`. El resultado es que las
131 actividades cerradas aparecian entre 3 y 6 semanas antes de cuando pasaron, y el proyecto
entero se veia terminado el 6-oct (operativo) o el 19-oct (ProjectLibre). Ninguna de las dos
XML tenia una sola fecha en noviembre.

LA REGLA
--------
La fecha de registro de una actividad cerrada es la del **artefacto verificable mas temprano
que la demuestra cerrada**: un commit con su asunto, un entregable con su nombre, o una
medicion con su archivo. No es la fecha planeada y no es una estimacion.

Donde la evidencia cae en fin de semana se registra el fin de semana. El equipo trabajo
sabados y domingos y el cronograma lo tiene que decir: los dos dias de mayor cierre del
proyecto fueron el sabado 17 y el domingo 18 de octubre. `rebaselinear.py` abre esos siete
dias como excepciones del calendario para que la fecha no se mueva al lunes.

ESTE MODULO NO INVENTA CIERRES. Solo fecha los que ya estaban marcados al 100 %. Las 20
actividades cerradas durante octubre ya traian su fecha en `marcar_hechas.HECHAS` y se
importan de ahi: no se repiten aqui.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import marcar_hechas as MH

# Dias de fin de semana en que si se trabajo, segun el historial de los dos repositorios.
# `rebaselinear.py` los abre en el calendario del cronograma.
# Solo van los tres en que ALGUNA actividad cierra. Abrir un dia que nadie usa le agrega un
# dia habil al calendario del cronograma y mueve el calculo de los inicios hacia atras sin
# que ninguna evidencia lo pida; hay una prueba que lo impide.
FINES_DE_SEMANA_TRABAJADOS = [
    "2026-09-12",  # sabado: etapa A del prototipo, 19 commits
    "2026-10-17",  # sabado: juego de ritmo jugable, 25 commits aqui y 26 en Unity
    "2026-10-18",  # domingo: entorno, musica y metricas, 17 commits aqui y 29 en Unity
]

# Tambien se trabajo estos cuatro fines de semana, y no estan arriba porque ninguna actividad
# del cronograma cierra en ellos: el 19 y el 20 de septiembre fue el ejercicio de ramas y
# pull requests del equipo (FIRMAS.md), el 10 de octubre el reloj musical que cerro el 17, y
# el 8 de noviembre el ajuste de tempo por pista, que es afinado de actividades ya cerradas.
OTROS_FINES_DE_SEMANA_CON_COMMITS = ["2026-09-19", "2026-09-20", "2026-10-10", "2026-11-08"]

# --- grupos de evidencia -------------------------------------------------------------------
#
# Cada grupo es un artefacto o un dia de cierre con su rastro verificable. La clave del grupo
# es la fecha; el texto describe donde se comprueba.

_GRUPOS = [
    ("2026-09-03",
     "Acta constitutiva v3.0 y carta sponsor v2.0: alcance, objetivos, entregables, EDT de "
     "42 paquetes con criterio de aceptacion, responsable por paquete y secuenciacion",
     ["QP.1", "QP.2", "QP.3", "QP.4", "QP.5", "QP.6", "QR.1", "QR.2", "QR.3"]),

    ("2026-09-09",
     "Cronograma_257_MindView.xml y Ruta_Critica_257_Tareas: 257 tareas, 417 vinculos, los 38 "
     "cambios de dependencias del lider, red que cierra con 257 de 257 llegando al final",
     ["QP.7", "QP.8", "QP.9"]),

    ("2026-09-12",
     "Etapa A del prototipo, 19 commits: DrumPad con plano armado, DrumHit y reparto a "
     "multiples receptores, StickTracker con deteccion de cruce y rearme por posicion, "
     "audio agendado y haptico diferido, herramienta de latencia solo con numpy",
     ["DG.1", "DG.3", "DG.6", "DG.7", "DG.8", "DH.1"]),

    ("2026-09-16",
     "Repositorio Unity inicializado y capitulo 4 cerrado: el pad suena al golpearlo con "
     "haptico y volumen por fuerza. Kit de samples elegido, atribuido e importado; "
     "normalizacion y centroide corregidos; dinamica timbral con round-robin",
     ["DP.1", "DP.2", "DX.1", "DX.2", "DX.3", "DX.4", "DX.5", "DX.6", "DB.1", "DT.1",
      "DG.2", "DG.4", "DG.5", "DG.9", "DH.2", "DR.1",
      "SP.1", "SB.1", "SB.2", "SB.3", "SB.4", "SB.6", "SE.1", "SE.3", "SE.4",
      "SI.1", "SI.2"]),

    ("2026-09-17",
     "Kit de seis piezas y escena jugable: identidad del proyecto y .gitignore, agarre de "
     "baquetas en los controles, balance de niveles entre las seis piezas, pool de voces a 32",
     ["DP.3", "DB.3", "DT.2", "DT.6", "DR.2", "SI.3"]),

    ("2026-09-18",
     "04_Planes_Costos_Calidad_Riesgos.docx: calidad 8.1 a 8.3, riesgos 11.1 a 11.7, "
     "registro de 18 riesgos con su respuesta y el formato de documentacion de errores",
     ["QG.1", "QE.1"]),

    ("2026-09-21",
     "Carta de validacion de entregables y lista de verificacion corregida, con la matriz "
     "que cruza cada entregable contra la medida de exito que lo cobra",
     ["QR.4"]),

    ("2026-10-17",
     "Tres cierres el mismo sabado. Reloj musical: desvio de 0.0 ms sostenido 205 s contra un "
     "metronomo de 120 BPM exactos. Juego de ritmo jugable: Beatmap, HitJudge, NoteMatcher, "
     "NoteSpawner, Scoreboard, JudgePopup, 79 pruebas en verde. Y la latencia remedida tras "
     "descubrir que la prediccion llevaba apagada desde que se construyo el kit",
     ["JA.1", "JA.2", "JA.3", "JT.1", "JT.2", "JT.3", "JB.1", "JB.2", "JB.3",
      "JN.1", "JN.2", "JW.1", "JW.2", "JW.5", "JP.1", "JP.3", "JI.1",
      "SI.4", "IG.1"]),

    ("2026-10-18",
     "Domingo de cierre grande. Enfoque emocional documentado en scripts/enfoque.py y en la "
     "solicitud de cambio: objetivo, limites, bibliografia seleccionada, emociones y "
     "actividades, ergonomia, guiones y fundamentacion teorica. Musica real medida: "
     "Maccary Bay a 79.98 BPM con su estructura y su patron de bateria. Metricas de sesion "
     "exportadas a JSON. Iluminacion del entorno y guion del tutorial",
     ["EO.1", "EO.2", "EB.1", "EB.2", "EB.3", "EB.4", "EB.5", "EE.1", "EE.2", "EE.3",
      "ER", "EG.1", "EG.2", "EG.3", "EI", "ET.1",
      "ML.1", "ML.2", "MP.1", "MP.2", "MP.3", "MB.1", "MB.4",
      "DM.1", "AL.1", "QC.3", "QC.5"]),

    ("2026-10-19",
     "Flujo completo de la aplicacion: tabla de transiciones, mapa de pantallas, navegacion "
     "entre menu, tutorial, juego y resultados, los cuatro wireframes y el guion de cierre "
     "dicho en palabras en la pantalla de resultados",
     ["IM.1", "IM.2", "IW.1", "IW.2", "IW.3", "IW.5", "EF", "EG.4"]),

    ("2026-10-21",
     "Pistas visuales de anticipacion: AroDeNota con los aros que se acumulan como los "
     "circulos de osu, y el aviso periferico que ilumina el borde de la vision cuando la "
     "pieza que toca queda fuera del campo de vision",
     ["IG.2", "IG.3"]),

    ("2026-10-21",
     "12_Estado_del_Proyecto.docx, informe semanal de avance con los hitos alcanzados",
     ["QC.2"]),
]

# clave -> (fecha, evidencia)
ANTERIORES = {}
for _fecha, _ev, _claves in _GRUPOS:
    for _k in _claves:
        assert _k not in ANTERIORES, "%s fechada dos veces" % _k
        ANTERIORES[_k] = (_fecha, _ev)

# Las 20 de octubre ya traen fecha y evidencia en marcar_hechas: no se duplican.
CIERRES = dict(MH.HECHAS)
for _k, _v in ANTERIORES.items():
    assert _k not in CIERRES, "%s ya venia fechada en marcar_hechas.HECHAS" % _k
    CIERRES[_k] = _v


def fecha(clave):
    """Fecha de registro de una actividad cerrada, o None si no esta fechada."""
    v = CIERRES.get(clave)
    return v[0] if v else None


if __name__ == "__main__":
    from collections import Counter
    c = Counter(f for f, _ in CIERRES.values())
    print("%d actividades fechadas en %d dias de cierre" % (len(CIERRES), len(c)))
    for f in sorted(c):
        fds = " (fin de semana)" if f in FINES_DE_SEMANA_TRABAJADOS else ""
        print("  %s  %3d%s" % (f, c[f], fds))
