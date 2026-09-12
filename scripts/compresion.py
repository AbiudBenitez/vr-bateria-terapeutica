# -*- coding: utf-8 -*-
"""Compresión de la red (etapa 7 del método) y tabla de simultaneidad."""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rc257 as R, costos as K

M = R.V2
# --- modelo de compresión: tiempo extra
# Jornada normal 8 h. Se admite extender a 10 h/día; las 2 h extra se pagan a 1.5x.
# La actividad conserva sus horas de trabajo, pero se reparten en menos días.
FRAC = 0.20            # reducción máxima de duración: 8/10 -> 20 % menos días
PRIMA = 0.50           # sobreprecio de la hora extra

def comprimible(k):
    """Días que se pueden recortar de la actividad."""
    return round(R.T[k]["dur"] * FRAC, 4)

def sobrecosto(k):
    """Costo adicional de trabajar esa actividad en jornada extendida."""
    return K.horas(k) * FRAC * K.tarifa(k) * PRIMA

def pendiente(k):
    d = comprimible(k)
    return sobrecosto(k)/d if d > 0 else float("inf")

CAD = R.CADENA
CANDIDATAS = [k for k in CAD if comprimible(k) > 0]
CANDIDATAS.sort(key=pendiente)

# --- ¿hasta dónde se puede comprimir antes de que otra trayectoria se vuelva crítica?
holguras = sorted({round(M["HT"][k],2) for k in R.ORD if M["HT"][k] > 1e-9})

# --- simultaneidad por tramos
TRAMOS = [(0,5),(5,10),(10,15),(15,20),(20,25),(25,30),(30,35),(35,40),(40,45.25)]
def activas(a,b):
    d = defaultdict(list)
    for k in R.ORD:
        if M["ES"][k] < b and M["EF"][k] > a:
            d[R.T[k]["sig"]].append(k)
    return d

if __name__ == "__main__":
    print(f"duración normal de la red: {M['TOTAL']:.2f} d")
    print(f"holguras positivas más pequeñas: {holguras[:8]}")
    print()
    print("PENDIENTES DE COSTO — actividades críticas, de la más barata a la más cara")
    print(f"{'clave':<8}{'dur':>6}{'recorte':>9}{'costo norm':>12}{'sobrecosto':>12}{'$/día':>10}  perfil")
    acum_d = acum_c = 0.0
    for k in CANDIDATAS[:20]:
        acum_d += comprimible(k); acum_c += sobrecosto(k)
        print(f"{k:<8}{R.T[k]['dur']:>6.2f}{comprimible(k):>9.2f}{K.costo(k):>12,.0f}"
              f"{sobrecosto(k):>12,.0f}{pendiente(k):>10,.0f}  {K.perfil(k)[:30]}")
    print()
    print(f"si se comprimieran TODAS las {len(CANDIDATAS)} críticas:")
    td = sum(comprimible(k) for k in CANDIDATAS); tc = sum(sobrecosto(k) for k in CANDIDATAS)
    print(f"  recorte teórico {td:.2f} d   sobrecosto ${tc:,.0f}   promedio ${tc/td:,.0f}/día")
    print()
    print("TABLA DE SIMULTANEIDAD — áreas activas por tramo")
    for a,b in TRAMOS:
        d = activas(a,b)
        tot = sum(len(v) for v in d.values())
        print(f"  días {a:>5.1f}-{b:<5.1f} {len(d)} áreas, {tot:>3} tareas: " +
              " ".join(f"{s}({len(v)})" for s,v in sorted(d.items())))

# ---------------------------------------------------------------- curva de compresión
def cpm(dur):
    pre = M["pre"]; suc = M["suc"]
    ES={}; EF={}
    for k in M["topo"]:
        ES[k]=max([EF[p] for p in pre[k]], default=0.0); EF[k]=ES[k]+dur[k]
    T=max(EF.values())
    LF={}; LS={}
    for k in reversed(M["topo"]):
        LF[k]=min([LS[s] for s in suc.get(k,[]) if s in LS], default=T); LS[k]=LF[k]-dur[k]
    return T, {k: round(LS[k]-ES[k],6) for k in dur}

def curva(step=0.25, max_iter=400):
    dur = {k: R.T[k]["dur"] for k in R.ORD}
    lim = {k: R.T[k]["dur"]*(1-FRAC) for k in R.ORD}     # duración mínima alcanzable
    T0,_ = cpm(dur)
    puntos = [(T0, 0.0, None)]
    gasto = 0.0
    for _ in range(max_iter):
        T, HT = cpm(dur)
        crit = [k for k in R.ORD if abs(HT[k])<1e-9 and dur[k]-lim[k] > 1e-9]
        if not crit: break
        mejor=None
        for k in sorted(crit, key=K.tarifa):
            s = min(step, dur[k]-lim[k])
            d2 = dict(dur); d2[k] = round(dur[k]-s, 6)
            T2,_ = cpm(d2)
            g = T - T2
            if g > 1e-9:
                costo_ = K.horas(k)*(s/R.T[k]["dur"])*K.tarifa(k)*PRIMA if R.T[k]["dur"]>0 else 0
                ef = costo_/g
                if mejor is None or ef < mejor[0]: mejor=(ef,k,s,costo_,T2)
        if mejor is None: break
        _,k,s,c,T2 = mejor
        dur[k] = round(dur[k]-s, 6); gasto += c
        puntos.append((T2, gasto, k))
    return puntos, dur

if __name__ == "__main__":
    print()
    print("CURVA DE COMPRESIÓN (tiempo-costo)")
    pts, durf = curva()
    print(f"{'duración':>10}{'recorte':>10}{'sobrecosto':>13}{'$/día marginal':>16}  última actividad")
    ant=None
    for T,g,k in pts:
        if ant is None: marg=""
        else:
            dd = ant[0]-T; marg = f"${(g-ant[1])/dd:,.0f}" if dd>1e-9 else "—"
        print(f"{T:>10.2f}{pts[0][0]-T:>10.2f}{g:>13,.0f}{marg:>16}  {k or '(normal)'}")
        ant=(T,g)
    print()
    print(f"compresión máxima alcanzable: {pts[0][0]-pts[-1][0]:.2f} d por ${pts[-1][1]:,.0f}")
    print(f"iteraciones: {len(pts)-1}")
