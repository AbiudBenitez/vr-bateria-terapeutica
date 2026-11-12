# -*- coding: utf-8 -*-
"""Replanificacion de las 25 actividades pendientes, del 12 al 20 de noviembre de 2026.

EL PROBLEMA QUE RESUELVE
------------------------
Al 11-nov-2026 las 25 pendientes siguen al 0 % y su red son 14 dias habiles. Del corte del
22-oct a hoy pasaron 14 dias habiles exactos: el presupuesto entero de lo que falta se gasto
sin arrancar la cadena. Al 13-nov comprometido quedan 2 dias habiles; con la reserva de
gestion del 16 al 20 quedan 7.

14 dias de cadena no caben en 7 por el camino normal. Caben solo traslapando, y traslapar no
es recortar: cada actividad conserva su duracion y su alcance, lo que cambia es que arranca
antes de que su antecedente termine. Cada traslape de aqui lleva escrito por que se sostiene.
Los que no se sostienen no estan.

LO QUE ESTE PLAN NO DISIMULA
----------------------------
Sale con holgura cero en todas las actividades. Cualquier retraso de un dia empuja el cierre
al 23-nov, que es el inicio de examenes. Y arranca con `QT.8`, pruebas con usuarios, que al
11-nov siguen sin reclutar: es el riesgo R18 y es el unico punto de falla que importa.
"""
import datetime as D
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import rc257 as R
import rc_recorte as RC

ARRANQUE = D.date(2026, 11, 12)   # primer dia habil disponible
COMPROMETIDA = D.date(2026, 11, 13)
RESERVA = D.date(2026, 11, 20)    # fin de la reserva de gestion
EXAMENES = D.date(2026, 11, 23)

# --- traslapes declarados ------------------------------------------------------------------
#
# (sucesora, antecedente) -> (tipo, demora, razon)
#
#   FS  la sucesora arranca cuando el antecedente termina, mas la demora. Es el valor por
#       omision de toda la red y no hace falta declararlo.
#   SS  la sucesora arranca cuando el antecedente ARRANCA, mas la demora. Es el traslape.
#
# La demora va en dias habiles.

TRASLAPES = {
    ("QE.2", "QT.8"): ("SS", 1,
        "El registro de errores y observaciones se hace durante las sesiones de prueba, no "
        "despues: arranca con la segunda sesion"),
    ("QV.5", "QT.8"): ("SS", 1,
        "La comodidad de la experiencia VR se pregunta al usuario al terminar su sesion, "
        "dentro de la misma prueba"),
    ("QI.1", "QT.8"): ("SS", 1,
        "Cada sesion se analiza el mismo dia que se corre; el analisis no espera a que "
        "terminen todas"),
    ("QI.1", "QE.2"): ("SS", 0,
        "El analisis consume el registro de observaciones conforme se escribe: son la misma "
        "persona mirando la misma sesion, una anotando y otra interpretando"),
    ("QI.2", "QI.1"): ("SS", 1,
        "El apartado de resultados se redacta sobre el analisis de las primeras sesiones; "
        "las ultimas se agregan al texto ya empezado"),
    ("QI.3", "QI.2"): ("SS", 1,
        "Conclusiones y limitaciones se redactan junto con los resultados: son dos secciones "
        "distintas del mismo documento y las limitaciones ya estan identificadas desde el "
        "recorte de alcance"),
    ("QI.5", "QI.4"): ("SS", 1,
        "La revision de redaccion y referencias empieza por las secciones ya integradas"),
    ("QX", "QI.5"): ("SS", 0,
        "La presentacion se arma de las secciones integradas en QI.4; la revision final de "
        "redaccion corre en paralelo sobre el documento, que es otro artefacto"),
    ("QX", "QB.4"): ("SS", 0,
        "La demostracion se prepara sobre la build candidata; la version definitiva solo "
        "cambia el numero de version"),
    ("QX", "QM.1"): ("SS", 0,
        "El manual de usuario y la presentacion se escriben del mismo guion"),
    ("QV.2", "QV.1"): ("SS", 0,
        "QV.2 evalua la estabilidad y los cierres inesperados DE la corrida completa que "
        "QV.1 ejecuta: es la misma sesion observada por dos criterios, no una posterior"),
    ("QX", "QI.4"): ("SS", 1,
        "La presentacion se arma de las secciones del informe conforme se integran, no "
        "cuando el documento entero esta cerrado"),
    ("QB.1", "QV.2"): ("SS", 0,
        "La build candidata ES la build que QV.2 evalua: generarla es el primer paso de "
        "evaluarla, no un paso posterior"),
    ("QB.3", "QB.2"): ("SS", 0,
        "Los errores criticos se corrigen conforme la prueba en el visor los encuentra"),
    ("QB.4", "QB.3"): ("SS", 0,
        "La version definitiva se genera al cerrar la ultima correccion"),
}

PENDIENTES = list(RC.PENDIENTES)
PRE = RC.REMANENTE["pre"]


def _topo():
    grado = {k: len(PRE[k]) for k in PENDIENTES}
    suc = {k: [] for k in PENDIENTES}
    for k in PENDIENTES:
        for p in PRE[k]:
            suc[p].append(k)
    cola = sorted(k for k in PENDIENTES if grado[k] == 0)
    orden = []
    while cola:
        k = cola.pop(0)
        orden.append(k)
        for x in suc[k]:
            grado[x] -= 1
            if grado[x] == 0:
                cola.append(x)
    assert len(orden) == len(PENDIENTES), "la red remanente tiene un ciclo"
    return orden, suc


ORDEN, SUC = _topo()


def resolver():
    """Pasada hacia adelante en dias habiles, con los traslapes declarados."""
    ES, EF = {}, {}
    for k in ORDEN:
        inicios = []
        for p in PRE[k]:
            tipo, demora, _ = TRASLAPES.get((k, p), ("FS", 0, ""))
            base = ES[p] if tipo == "SS" else EF[p]
            inicios.append(base + demora)
        ES[k] = max(inicios, default=0.0)
        EF[k] = ES[k] + R.T[k]["dur"]
    return ES, EF


ES, EF = resolver()
TOTAL = max(EF.values())


def habil(offset):
    """Convierte un desplazamiento en dias habiles a fecha, saltando fines de semana."""
    d = ARRANQUE
    n = int(offset)
    while n > 0:
        d += D.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    while d.weekday() >= 5:
        d += D.timedelta(days=1)
    return d


def calendario():
    """clave -> (fecha de inicio, fecha de fin). El fin es el ultimo dia trabajado."""
    cal = {}
    for k in PENDIENTES:
        ini = habil(ES[k])
        # Una actividad que termina en el offset EF trabaja hasta el dia habil anterior a EF
        # cuando EF cae justo en el limite; una de duracion cero termina el dia que arranca.
        fin = habil(max(EF[k] - 1e-9, ES[k]))
        cal[k] = (ini, fin)
    return cal


CALENDARIO = calendario()
CIERRE = max(f for _, f in CALENDARIO.values())
HOLGURA_DIAS = sum(1 for d in _dias_habiles(CIERRE, RESERVA)) if False else None


def _dias_habiles(a, b):
    d = a
    while d < b:
        d += D.timedelta(days=1)
        if d.weekday() < 5:
            yield d


HOLGURA_DIAS = len(list(_dias_habiles(CIERRE, RESERVA)))


if __name__ == "__main__":
    print("REPLANIFICACION DE LO QUE FALTA")
    print("  arranque      %s" % ARRANQUE)
    print("  cadena        %.2f d habiles traslapada, contra %.2f d sin traslapar"
          % (TOTAL, RC.REMANENTE["TOTAL"]))
    print("  cierre        %s" % CIERRE)
    print("  comprometida  %s   reserva %s   examenes %s"
          % (COMPROMETIDA, RESERVA, EXAMENES))
    print("  holgura contra el fin de la reserva: %d dias habiles" % HOLGURA_DIAS)
    print()
    pordia = {}
    for k, (i, f) in CALENDARIO.items():
        pordia.setdefault(i, []).append(k)
    for d in sorted(pordia):
        dias = {0: "lun", 1: "mar", 2: "mie", 3: "jue", 4: "vie"}[d.weekday()]
        print("  %s %s  arrancan: %s" % (d, dias, ", ".join(sorted(pordia[d]))))
    print()
    print("  %-6s %-5s %-12s %-12s %s" % ("clave", "dur", "inicio", "fin", "antecedentes"))
    for k in ORDEN:
        i, f = CALENDARIO[k]
        print("  %-6s %-5.2f %-12s %-12s %s"
              % (k, R.T[k]["dur"], i, f, ", ".join(PRE[k]) or "-"))
    print()
    print("TRASLAPES DECLARADOS: %d" % len(TRASLAPES))
    for (k, p), (tipo, demora, razon) in sorted(TRASLAPES.items()):
        print("  %-6s <- %-6s %s+%d  %s" % (k, p, tipo, demora, razon))
