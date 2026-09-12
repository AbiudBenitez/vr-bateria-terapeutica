# -*- coding: utf-8 -*-
"""Ruta crítica de las 257 tareas de la nomenclatura del equipo.

Dos modelos:
  ORIG  la red tal como se entregó            -> 36.88 días
  CORR  con las dependencias de integración   -> 39.88 días
"""
import json, re, os, sys
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = json.load(open(os.path.join(BASE, "tareas_lider.json")))

RESP = {"Desarrollo VR y batería":"Misael","Juego de ritmo":"Benjamín",
        "Experiencia emocional":"María","Música":"Javier","Sonido":"Christian",
        "Interfaz / UX/UI":"Sarai","Entorno 3D y assets":"Kimberly",
        "QA, documentación y gestión":"Diana"}
SIGLA = {"Desarrollo VR y batería":"D","Juego de ritmo":"J","Experiencia emocional":"E",
         "Música":"M","Sonido":"S","Interfaz / UX/UI":"I","Entorno 3D y assets":"A",
         "QA, documentación y gestión":"Q"}
AREAS = list(SIGLA)

def _dur(txt):
    """8 h = 1 día. Los rangos se toman en su valor MENOR.

    Criterio adoptado el 11-sep-2026 para alinearse con la hoja de control de tareas
    que el equipo mantiene. Hasta el 11-sep se empleaba el valor mayor, que daba una
    red de 45.25 días; con el menor son 38.25.
    """
    t = txt.lower().replace("í","i").replace("á","a")
    n = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)", t)]
    if not n: return 0.0                     # 'durante todo el proyecto' -> seguimiento continuo
    v = min(n)
    if "hora" in t: return round(v/8.0, 4)
    if "semana" in t: return v*5.0
    return v

def _pre(txt):
    t = txt.strip()
    if not t or t.lower().startswith("sin dependencia"): return []
    t = t.replace(" y ", ",").replace(";", ",")
    return [m.group(1) for m in
            (re.match(r"^([A-Z]{2}(?:\.\d+)?)$", p.strip().rstrip(".")) for p in t.split(","))
            if m]

T = {}; ORD = []
for clave, desc, area, tiempo, dep in RAW:
    k = clave.strip()
    T[k] = dict(clave=k, desc=desc, area=area, sig=SIGLA[area], resp=RESP[area],
                dur=_dur(tiempo), durtxt=tiempo.strip(), pre=_pre(dep), pretxt=dep.strip())
    ORD.append(k)
for k in ORD:                                 # dependencias a claves inexistentes
    T[k]["pre"] = [p for p in T[k]["pre"] if p in T]

CONTINUAS = [k for k in ORD if T[k]["dur"] == 0.0]

# ---- dependencias de integración que faltaban en la red recibida (análisis del 7-sep)
# Quedan superadas por CAMBIOS: ya no aportan duración. Se conservan para el contraste.
INTEGRACION = ["DR.2","JM.2","MN.2","SC.2","AO.6","EG.3"]

# ---- cambios de dependencias del líder (9-sep). Son ADICIONES, no reemplazos.
CAMBIOS = json.load(open(os.path.join(BASE, "cambios_dep.json")))
ORDEN_CAMBIOS = [c for c in ORD if c in CAMBIOS] if False else None

def calcula(extra=None):
    pre = {k: list(T[k]["pre"]) for k in ORD}
    for k, ps in (extra or {}).items():
        for p in ps:
            if p not in pre[k]: pre[k].append(p)
    suc = defaultdict(list)
    for k in ORD:
        for p in pre[k]: suc[p].append(k)
    grado = {k: len(pre[k]) for k in ORD}
    cola = [k for k in ORD if grado[k] == 0]; topo = []
    while cola:
        k = cola.pop(0); topo.append(k)
        for s in suc[k]:
            grado[s] -= 1
            if grado[s] == 0: cola.append(s)
    assert len(topo) == len(ORD), "la red contiene un ciclo"
    ES = {}; EF = {}
    for k in topo:
        ES[k] = max([EF[p] for p in pre[k]], default=0.0); EF[k] = ES[k] + T[k]["dur"]
    TOT = max(EF.values())
    LF = {}; LS = {}
    for k in reversed(topo):
        LF[k] = min([LS[s] for s in suc[k] if s in LS], default=TOT)
        LS[k] = LF[k] - T[k]["dur"]
    HT = {k: round(LS[k]-ES[k], 4) for k in ORD}
    HL = {k: round(min([ES[s] for s in suc[k]], default=TOT) - EF[k], 4) for k in ORD}
    HI = {k: round(HT[k]-HL[k], 4) for k in ORD}
    HN = {k: round(max(0.0, min([ES[s] for s in suc[k]], default=TOT)
                       - max([LF[p] for p in pre[k]], default=0.0) - T[k]["dur"]), 4) for k in ORD}
    return dict(pre=pre, suc=dict(suc), topo=topo, ES=ES, EF=EF, LS=LS, LF=LF,
                HT=HT, HL=HL, HI=HI, HN=HN, TOTAL=TOT,
                CRIT=[k for k in topo if abs(HT[k]) < 1e-6])

ORIG = calcula()                       # red tal como se entregó      36.88 d
CORR = calcula({"QT.8": INTEGRACION})  # corrección mínima del 7-sep  39.88 d
V2   = calcula(CAMBIOS)                # con los 38 cambios del líder 45.25 d

def cadena(M):
    """Reconstruye la cadena crítica desde el final hacia atrás."""
    fin = max(M["CRIT"], key=lambda k: M["EF"][k]); cad = [fin]
    while M["pre"][cad[-1]]:
        ant = [p for p in M["pre"][cad[-1]]
               if abs(M["EF"][p]-M["ES"][cad[-1]]) < 1e-6 and abs(M["HT"][p]) < 1e-6]
        if not ant: break
        cad.append(max(ant, key=lambda p: M["EF"][p]))
    return list(reversed(cad))

CADENA = cadena(V2)

# ---- carga de trabajo por área
CARGA = defaultdict(float); NTAR = defaultdict(int)
for k in ORD:
    CARGA[T[k]["area"]] += T[k]["dur"]; NTAR[T[k]["area"]] += 1
VENTANA = {a: max(V2["EF"][k] for k in ORD if T[k]["area"] == a) -
              min(V2["ES"][k] for k in ORD if T[k]["area"] == a) for a in AREAS}
VENTANA_V1 = {a: max(ORIG["EF"][k] for k in ORD if T[k]["area"] == a) -
              min(ORIG["ES"][k] for k in ORD if T[k]["area"] == a) for a in AREAS}

TERMINALES    = [k for k in ORD if not V2["suc"].get(k)]
TERMINALES_V1 = [k for k in ORD if not ORIG["suc"].get(k)]
SIN_PRE    = [k for k in ORD if not T[k]["pre"]]

def fnum(x):
    return f"{x:.2f}".rstrip("0").rstrip(".") if x % 1 else f"{int(x)}"

if __name__ == "__main__":
    print(f"tareas: {len(ORD)}   suma de duraciones: {sum(T[k]['dur'] for k in ORD):.1f} d")
    print(f"red recibida  : {ORIG['TOTAL']:.2f} d   criticas {len(ORIG['CRIT']):>3}   terminales {len(TERMINALES_V1)}")
    print(f"correcc. 7-sep: {CORR['TOTAL']:.2f} d   criticas {len(CORR['CRIT']):>3}")
    print(f"CAMBIOS 9-sep : {V2['TOTAL']:.2f} d   criticas {len(V2['CRIT']):>3}   terminales {len(TERMINALES)}")
    print(f"cambios aplicados: {len(CAMBIOS)} actividades, {sum(len(v) for v in CAMBIOS.values())} dependencias nuevas")
    print(f"sin antecedente: {len(SIN_PRE)}")
    print(f"seguimiento continuo (duración no acotada): {CONTINUAS}")
    print(f"cadena crítica: {len(CADENA)} actividades")
    print(f"holgura <=5 d: {sum(1 for k in ORD if CORR['HT'][k] <= 5)}")
    print()
    for a in sorted(AREAS, key=lambda x: -CARGA[x]):
        print(f"  {a[:28]:<30}{RESP[a]:<10}{NTAR[a]:>4} tar {CARGA[a]:>7.1f} d  ventana {VENTANA[a]:>6.1f} d")
