# -*- coding: utf-8 -*-
"""Ruta critica despues del recorte de alcance del 18-oct-2026.

`rc257.py` sigue calculando sobre las 257 actividades, que es la linea base
anterior y hay que conservarla. Este modulo calcula la red que queda viva —158
actividades— sin tocar aquella, para poder comparar una contra otra.

EL PUNTO FINO: al quitar una actividad intermedia, sus sucesoras se quedan
colgando. Hay dos maneras de resolverlo y dan resultados distintos:

  INGENUA  se borran las actividades recortadas y sus enlaces. Las sucesoras
           que se quedan sin antecedente flotan al dia cero y la red se acorta
           sola. Es lo que pasa si uno borra filas del cronograma sin pensar.

  PUENTE   cuando se corta B en A -> B -> C, se conecta A -> C. La dependencia
           se hereda hacia arriba hasta encontrar una actividad viva. Parte del
           supuesto de que C necesitaba el producto que venia de aguas arriba,
           no la actividad B en si.

El puente es la lectura conservadora y la que se adopta como vigente: nunca
acorta la red por un descuido. Pero no es automatica — cada enlace heredado es
una afirmacion sobre por que C dependia de B, y las que no se sostengan hay que
quitarlas a mano en REVISADAS.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import recorte as C
import rc257 as R
import validacion as VAL

CORTADAS = set(C.RECORTADAS)
VIVAS = [k for k in R.ORD if k not in CORTADAS]

# Dependencias de la linea base anterior: las declaradas por el equipo mas los
# 38 cambios del 9-sep, que es la red V2 vigente antes del recorte.
PRE_BASE = {k: list(R.V2["pre"][k]) for k in R.ORD}

# Enlaces heredados que la revisión del 22-oct-2026 decidió NO conservar. El puente
# los propuso al subir por una cadena cortada, pero la dependencia no se sostiene:
# heredan trabajo de otra área que nunca habilitó a la sucesora.
REVISADAS = {
    ("AA.3", "EB.4"): "Seleccionar estudios científicos no habilita buscar assets de entorno. "
                      "El puente subió por AA.1, que colgaba del trabajo de experiencia emocional",
    ("AA.3", "EB.5"): "La matriz bibliográfica es evidencia científica, ajena a la elección de assets",
    ("AA.3", "DX.2"): "Configurar OpenXR es del área de desarrollo y no condiciona qué assets se eligen",
    ("QC.4", "DX.2"): "Llevar el registro de licencias no depende de la configuración del visor",
    ("II.2", "EB.5"): "La matriz bibliográfica no habilita implementar el menú principal",
    ("QT.7", "IW.1"): "El wireframe del menú no condiciona probar el sistema de ritmo",
    ("QT.7", "EI"):   "La definición del uso emocional del ritmo es marco conceptual, no insumo de prueba",
    ("QT.7", "IT.4"): "El flujo del tutorial es otro camino de la aplicación",
    ("QT.7", "SP.1"): "La lista de sonidos del proyecto no es insumo de las pruebas de ritmo",
    ("QT.7", "QR.4"): "La matriz de trazabilidad es documentación de gestión, no antecedente técnico",
}

# Dependencias que el recorte deja al descubierto y que hay que declarar de nuevo,
# porque el puente no las encuentra: la actividad que las habilita no era antecedente
# de la cortada, sino que ocupó su lugar en el alcance.
ANADIDAS = {
    "QC.4": [("AA.3", "El registro de licencias se levanta sobre los assets que se eligieron, "
                      "y elegirlos es ahora AA.3, no el catálogo AA.1 que se recortó")],
}


def puente(k, visto=None):
    """Antecedentes vivos de k, saltando por encima de las actividades cortadas."""
    visto = visto or set()
    out = []
    for p in PRE_BASE[k]:
        if p in visto:
            continue
        visto.add(p)
        if p not in CORTADAS:
            out.append(p)
        else:
            out.extend(puente(p, visto))
    return out


def red(modo="puente"):
    """Red de las actividades vivas. modo: 'puente' o 'ingenua'."""
    pre = {}
    for k in VIVAS:
        if modo == "ingenua":
            ps = [p for p in PRE_BASE[k] if p not in CORTADAS]
        else:
            ps = []
            for p in puente(k):
                if p not in ps and (k, p) not in REVISADAS:
                    ps.append(p)
            for p, _razon in ANADIDAS.get(k, []):
                if p not in ps and p not in CORTADAS:
                    ps.append(p)
        pre[k] = ps

    suc = {k: [] for k in VIVAS}
    for k in VIVAS:
        for p in pre[k]:
            suc[p].append(k)

    grado = {k: len(pre[k]) for k in VIVAS}
    cola = [k for k in VIVAS if grado[k] == 0]
    topo = []
    while cola:
        k = cola.pop(0)
        topo.append(k)
        for s in suc[k]:
            grado[s] -= 1
            if grado[s] == 0:
                cola.append(s)
    assert len(topo) == len(VIVAS), "la red recortada contiene un ciclo"

    ES, EF = {}, {}
    for k in topo:
        ES[k] = max([EF[p] for p in pre[k]], default=0.0)
        EF[k] = ES[k] + R.T[k]["dur"]
    TOT = max(EF.values())
    LF, LS = {}, {}
    for k in reversed(topo):
        LF[k] = min([LS[s] for s in suc[k] if s in LS], default=TOT)
        LS[k] = LF[k] - R.T[k]["dur"]
    HT = {k: round(LS[k] - ES[k], 4) for k in VIVAS}
    HL = {k: round(min([ES[s] for s in suc[k]], default=TOT) - EF[k], 4) for k in VIVAS}
    return dict(pre=pre, suc=suc, topo=topo, ES=ES, EF=EF, LS=LS, LF=LF, HT=HT, HL=HL,
                TOTAL=TOT, CRIT=[k for k in topo if abs(HT[k]) < 1e-6])


PUENTE = red("puente")
INGENUA = red("ingenua")

# ---- avance real y red de lo que falta
#
# Las dos redes de arriba programan desde el dia cero, como si no se hubiera hecho
# nada. Con 130 de 157 actividades cerradas eso ya no describe al proyecto: una
# actividad terminada tiene fecha real y no se reprograma detras de un antecedente.
# La red que sirve para dirigir es la de lo que falta, contada desde la fecha de corte.
AVANCE = {k: v["pct"] for k, v in VAL.cronograma().items()}
HECHAS = [k for k in VIVAS if AVANCE.get(k, 0) >= 100]
PENDIENTES = [k for k in VIVAS if AVANCE.get(k, 0) < 100]


def remanente():
    """Red de las actividades que faltan. Las cerradas ya no imponen fecha."""
    pre = {k: [p for p in PUENTE["pre"][k] if p in PENDIENTES] for k in PENDIENTES}
    suc = {k: [] for k in PENDIENTES}
    for k in PENDIENTES:
        for p in pre[k]:
            suc[p].append(k)
    grado = {k: len(pre[k]) for k in PENDIENTES}
    cola = [k for k in PENDIENTES if grado[k] == 0]
    topo = []
    while cola:
        k = cola.pop(0)
        topo.append(k)
        for x in suc[k]:
            grado[x] -= 1
            if grado[x] == 0:
                cola.append(x)
    assert len(topo) == len(PENDIENTES), "la red remanente contiene un ciclo"
    ES, EF = {}, {}
    for k in topo:
        ES[k] = max([EF[p] for p in pre[k]], default=0.0)
        EF[k] = ES[k] + R.T[k]["dur"]
    TOT = max(EF.values())
    LF, LS = {}, {}
    for k in reversed(topo):
        LF[k] = min([LS[x] for x in suc[k] if x in LS], default=TOT)
        LS[k] = LF[k] - R.T[k]["dur"]
    HT = {k: round(LS[k] - ES[k], 4) for k in PENDIENTES}
    return dict(pre=pre, suc=suc, topo=topo, ES=ES, EF=EF, LS=LS, LF=LF, HT=HT,
                TOTAL=TOT, CRIT=[k for k in topo if abs(HT[k]) < 1e-6])


REMANENTE = remanente()

# Enlaces que el recorte rompe, y qué pasa con cada sucesora.
ROTOS = {k: [p for p in PRE_BASE[k] if p in CORTADAS] for k in VIVAS}
ROTOS = {k: v for k, v in ROTOS.items() if v}
HUERFANAS = {k: v for k, v in ROTOS.items()
             if not [p for p in PRE_BASE[k] if p not in CORTADAS]}


def cadena(M):
    fin = max(M["CRIT"], key=lambda k: M["EF"][k])
    cad = [fin]
    while M["pre"][cad[-1]]:
        ant = [p for p in M["pre"][cad[-1]]
               if abs(M["EF"][p] - M["ES"][cad[-1]]) < 1e-6 and abs(M["HT"][p]) < 1e-6]
        if not ant:
            break
        cad.append(max(ant, key=lambda p: M["EF"][p]))
    return list(reversed(cad))


if __name__ == "__main__":
    print("LINEA BASE ANTERIOR (257 actividades)")
    print("  duracion %.2f d   criticas %d" % (R.V2["TOTAL"], len(R.V2["CRIT"])))
    print()
    print("DESPUES DEL RECORTE (%d vivas, %d cortadas)" % (len(VIVAS), len(CORTADAS)))
    print("  con puente : %.2f d   criticas %d" % (PUENTE["TOTAL"], len(PUENTE["CRIT"])))
    print("  ingenua    : %.2f d   criticas %d" % (INGENUA["TOTAL"], len(INGENUA["CRIT"])))
    print("  diferencia : %.2f d que la red ingenua se ahorra sin justificarlo"
          % (PUENTE["TOTAL"] - INGENUA["TOTAL"]))
    print()
    print("ENLACES QUE EL RECORTE ROMPE: %d, repartidos en %d actividades"
          % (sum(len(v) for v in ROTOS.values()), len(ROTOS)))
    print("  de ellas, %d se quedan sin ningun antecedente vivo:" % len(HUERFANAS))
    for k in sorted(HUERFANAS):
        heredados = PUENTE["pre"][k]
        print("   %-6s %-46s pierde %-22s -> hereda %s"
              % (k, R.T[k]["desc"][:46], ",".join(HUERFANAS[k])[:22],
                 ",".join(heredados) if heredados else "NADA: arranca el dia cero"))
    print()
    cad = cadena(PUENTE)
    print("CADENA CRITICA NUEVA (%d actividades):" % len(cad))
    print("  " + " -> ".join(cad))
    print()
    print("RED DE LO QUE FALTA (fecha de corte 22-oct-2026)")
    print("  cerradas %d de %d   pendientes %d" % (len(HECHAS), len(VIVAS), len(PENDIENTES)))
    print("  duracion %.2f d habiles   suma de duraciones %.2f d"
          % (REMANENTE["TOTAL"], sum(R.T[k]["dur"] for k in PENDIENTES)))
    print("  cadena critica: " + " -> ".join(REMANENTE["CRIT"]))
    porarea = {}
    for k in PENDIENTES:
        porarea.setdefault(R.T[k]["area"], []).append(k)
    for a, ks in sorted(porarea.items(), key=lambda x: -len(x[1])):
        print("    %-30s %2d pendientes" % (a[:30], len(ks)))
    print()
    antes = set(R.CADENA)
    print()
    print("  entran a la cadena:", ", ".join(k for k in cad if k not in antes) or "ninguna")
    print("  salen de la cadena:", ", ".join(k for k in R.CADENA if k not in set(cad)) or "ninguna")
