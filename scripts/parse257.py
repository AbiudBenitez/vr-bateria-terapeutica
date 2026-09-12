# -*- coding: utf-8 -*-
"""Parsea las 257 tareas del documento del lider y calcula la ruta critica."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RAW = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tareas_lider.json")))

def dur(txt):
    """Convierte '3 horas', '1 dia', '1 a 2 dias' a dias de 8 h. Rango -> valor mayor."""
    t = txt.lower().replace("í","i").replace("á","a")
    nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)", t)]
    if not nums: return None, txt
    v = max(nums)
    if "hora" in t: return v/8.0, txt
    if "semana" in t: return v*5.0, txt
    return v, txt                       # dias

def deps(txt):
    t = txt.strip()
    if not t or t.lower().startswith("sin dependencia"): return []
    t = t.replace(" y ", ",").replace(";", ",")
    out = []
    for p in t.split(","):
        p = p.strip().rstrip(".")
        m = re.match(r"^([A-Z]{2}(?:\.\d+)?)$", p)
        if m: out.append(m.group(1))
        elif p: out.append(("?" , p))
    return out

TAREAS = {}
ORD = []
PROB = []
for clave, descr, area, tiempo, dep in RAW:
    k = clave.strip()
    d, orig = dur(tiempo)
    if d is None: PROB.append(("duracion ilegible", k, tiempo))
    ds = []
    for x in deps(dep):
        if isinstance(x, tuple): PROB.append(("dependencia ilegible", k, x[1]))
        else: ds.append(x)
    TAREAS[k] = dict(clave=k, desc=descr, area=area, dur=d or 0.0, durtxt=tiempo, pre=ds)
    ORD.append(k)

# dependencias a claves inexistentes
for k in ORD:
    for p in list(TAREAS[k]["pre"]):
        if p not in TAREAS:
            PROB.append(("dependencia inexistente", k, p))
            TAREAS[k]["pre"].remove(p)

# ciclos
def orden_topologico():
    grado = {k: len(TAREAS[k]["pre"]) for k in ORD}
    suc = {k: [] for k in ORD}
    for k in ORD:
        for p in TAREAS[k]["pre"]: suc[p].append(k)
    lista = [k for k in ORD if grado[k] == 0]
    out = []
    while lista:
        k = lista.pop(0); out.append(k)
        for s in suc[k]:
            grado[s] -= 1
            if grado[s] == 0: lista.append(s)
    return out, suc

TOPO, SUC = orden_topologico()
CICLO = [k for k in ORD if k not in TOPO]

# CPM
ES = {}; EF = {}
for k in TOPO:
    ES[k] = max([EF[p] for p in TAREAS[k]["pre"]], default=0.0)
    EF[k] = ES[k] + TAREAS[k]["dur"]
TOTAL = max(EF.values()) if EF else 0.0
LF = {}; LS = {}
for k in reversed(TOPO):
    LF[k] = min([LS[s] for s in SUC[k] if s in LS], default=TOTAL)
    LS[k] = LF[k] - TAREAS[k]["dur"]
HT = {k: round(LS[k]-ES[k], 4) for k in TOPO}
CRIT = [k for k in TOPO if abs(HT[k]) < 1e-6]

def ruta_larga():
    """Reconstruye una cadena critica desde el final hacia atras."""
    fin = max(CRIT, key=lambda k: EF[k])
    cad = [fin]
    while TAREAS[cad[-1]]["pre"]:
        ant = [p for p in TAREAS[cad[-1]]["pre"] if abs(EF[p]-ES[cad[-1]]) < 1e-6 and abs(HT[p]) < 1e-6]
        if not ant: break
        cad.append(max(ant, key=lambda p: EF[p]))
    return list(reversed(cad))

if __name__ == "__main__":
    print(f"tareas leidas: {len(ORD)}")
    print(f"suma de duraciones: {sum(t['dur'] for t in TAREAS.values()):.1f} dias de 8 h")
    print(f"tareas sin dependencia (arrancan el dia 0): {sum(1 for k in ORD if not TAREAS[k]['pre'])}")
    print(f"tareas sin sucesora (terminales): {sum(1 for k in ORD if not SUC[k])}")
    print(f"ciclos detectados: {len(CICLO)}  {CICLO[:12]}")
    print()
    print(f"*** DURACION DE LA RUTA CRITICA: {TOTAL:.1f} dias habiles ***")
    print(f"actividades criticas: {len(CRIT)} de {len(ORD)}")
    print()
    cad = ruta_larga()
    print("CADENA CRITICA (una de ellas):")
    ac = 0.0
    for k in cad:
        ac += TAREAS[k]["dur"]
        print(f"  {k:<7}{TAREAS[k]['dur']:>5.2f} d  acum {ac:>6.2f}  [{TAREAS[k]['area'][:22]:<22}] {TAREAS[k]['desc'][:58]}")
    print()
    from collections import Counter
    print("areas presentes en la ruta critica:")
    for a, n in Counter(TAREAS[k]["area"] for k in CRIT).most_common():
        print(f"  {n:>3}  {a}")
    print()
    if PROB:
        print(f"PROBLEMAS EN LOS DATOS: {len(PROB)}")
        from collections import Counter as C2
        for tipo, n in C2(p[0] for p in PROB).most_common(): print(f"  {n:>3}  {tipo}")
        for p in PROB[:25]: print("   ", p)
