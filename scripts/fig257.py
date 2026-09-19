# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"        # el texto sigue siendo texto en Inkscape
matplotlib.rcParams["font.family"] = "DejaVu Sans"
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D
import rc257 as R

SAL = "/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/figuras-ruta-critica/"
os.makedirs(SAL, exist_ok=True)
ROJO = "#b00020"; GRIS = "#444444"
COL = {"D":"#4472C4","J":"#7030A0","E":"#2E9BB5","M":"#ED7D31","S":"#BF9000",
       "I":"#C00060","A":"#8FBC3F","Q":"#808080"}
NOMA = {"D":"Desarrollo VR y batería","J":"Juego de ritmo","E":"Experiencia emocional",
        "M":"Música","S":"Sonido","I":"Interfaz / UX-UI","A":"Entorno 3D y assets",
        "Q":"QA, documentación y gestión"}

def guarda(fig, nombre):
    for ext in ("svg", "png"):
        fig.savefig(SAL+nombre+"."+ext, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig); print("OK", nombre+".svg / .png")

def corta(t, n):
    if len(t) <= n: return t
    pal = t.split(); l = [""]
    for p in pal:
        if len(l[-1])+len(p)+1 <= n: l[-1] = (l[-1]+" "+p).strip()
        else: l.append(p)
    return "\n".join(l[:3])

# ===================================================== FIG 1 — matriz de dependencias
def fig1():
    M = R.V2
    from collections import Counter
    cnt = Counter()
    for k in R.ORD:
        for p in M["pre"][k]:
            cnt[(R.T[p]["sig"], R.T[k]["sig"])] += 1
    sig = list(COL)                                   # D J E M S I A Q
    n = len(sig)
    crit = {R.T[k]["sig"] for k in M["CRIT"]}
    fig, ax = plt.subplots(figsize=(13.2, 8.4))
    mx = max(v for (a,b),v in cnt.items() if a != b) or 1
    for r, a in enumerate(sig):
        for c, b in enumerate(sig):
            v = cnt.get((a,b), 0)
            x, y = c, n-1-r
            if a == b:
                fc, ec, tc = "#eeeeee", "#cccccc", "#999999"
            elif v == 0:
                fc, ec, tc = "white", "#dddddd", "#bbbbbb"
            else:
                al = 0.16 + 0.62*min(v, mx)/mx
                fc, ec, tc = COL[b] + f"{int(al*255):02X}", COL[b], "black"
            ax.add_patch(Rectangle((x-0.46, y-0.46), 0.92, 0.92, fc=fc, ec=ec, lw=1.0, zorder=3))
            if v:
                ax.text(x, y, str(v), ha="center", va="center", fontsize=11,
                        fontweight="bold" if a != b else "normal", color=tc, zorder=4)
    for c, b in enumerate(sig):
        col = ROJO if b in crit else "black"
        ax.text(c, n+0.70, b, ha="center", va="center", fontsize=13, fontweight="bold", color=COL[b])
        ax.text(c, n+0.44, corta(NOMA[b], 15), ha="center", va="top", fontsize=6.6, color=col, linespacing=1.3)
    for r, a in enumerate(sig):
        y = n-1-r
        col = ROJO if a in crit else "black"
        ax.text(-0.62, y+0.14, a, ha="right", va="center", fontsize=13, fontweight="bold", color=COL[a])
        ax.text(-0.62, y-0.20, NOMA[a][:26], ha="right", va="center", fontsize=7.2, color=col)
        nom = [z for z in R.AREAS if R.SIGLA[z] == a][0]
        ax.text(n-0.35, y, f"{R.NTAR[nom]:>3} tareas   {R.CARGA[nom]:>5.1f} d   {R.RESP[nom]}",
                ha="left", va="center", fontsize=8, color=GRIS)
    ax.text(-0.62, n+0.70, "PREDECESORA", ha="right", va="center", fontsize=8.5,
            fontweight="bold", color=GRIS)
    ax.text((n-1)/2.0, n+1.45, "SUCESORA  →  el número es cuántas dependencias van de la fila a la columna",
            ha="center", va="center", fontsize=9, fontweight="bold", color=GRIS)
    hs = [Line2D([0],[0], marker="s", color="white", markerfacecolor="#eeeeee",
                 markeredgecolor="#cccccc", markersize=12, label="Diagonal: dependencias internas del área"),
          Line2D([0],[0], marker="s", color="white", markerfacecolor="white",
                 markeredgecolor="#dddddd", markersize=12, label="Sin dependencia"),
          Line2D([0],[0], color="white", lw=0, label="Clave en rojo: el área tiene actividades en la ruta crítica")]
    ax.legend(handles=hs, loc="lower center", bbox_to_anchor=(0.42,-0.13), ncol=3, fontsize=8.2, framealpha=1)
    ax.set_title("FIG. 1  MATRIZ DE DEPENDENCIAS ENTRE ÁREAS", fontsize=13.5, fontweight="bold", pad=26)
    ax.text(0.5, 1.035, "257 tareas agrupadas en 8 áreas  ·  se lee: el área de la fila debe terminar antes que el área de la columna",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.2, color=GRIS)
    ax.set_xlim(-3.6, n+2.7); ax.set_ylim(-1.1, n+1.9)
    ax.set_aspect("equal"); ax.axis("off")
    guarda(fig, "Fig1_Matriz_dependencias_areas")

# ===================================================== FIG 2 — ruta crítica en detalle
def fig2():
    M = R.V2; cad = R.CADENA
    porf = 8
    filas = [cad[i:i+porf] for i in range(0, len(cad), porf)]
    W, H, DX, DY = 2.55, 1.5, 3.05, 2.5
    fig, ax = plt.subplots(figsize=(17, 2.0+DY*len(filas)*0.62))
    P = {}
    for r, fila in enumerate(filas):
        for c, k in enumerate(fila):
            P[k] = (c*DX, -r*DY)
    for i in range(len(cad)-1):
        a, b = cad[i], cad[i+1]
        (x1,y1),(x2,y2) = P[a], P[b]
        if abs(y1-y2) < 0.01:                   # mismo renglón: flecha recta
            ax.add_patch(FancyArrowPatch((x1+W/2,y1),(x2-W/2,y2), arrowstyle="-|>",
                mutation_scale=13, linewidth=2.2, color=ROJO, zorder=3, shrinkA=0, shrinkB=0))
        else:                                   # salto de renglón: conector ortogonal
            ym = (y1-H/2 + y2+H/2)/2.0
            sx, ex = x1+W/2+0.42, x2-W/2-0.42
            px = [x1+W/2, sx, sx, ex, ex, x2-W/2-0.16]
            py = [y1,     y1, ym, ym, y2, y2]
            ax.plot(px, py, color=ROJO, lw=2.2, solid_capstyle="round",
                    solid_joinstyle="round", zorder=3)
            ax.add_patch(FancyArrowPatch((x2-W/2-0.16,y2),(x2-W/2,y2), arrowstyle="-|>",
                mutation_scale=13, linewidth=2.2, color=ROJO, zorder=3, shrinkA=0, shrinkB=0))
    for k in cad:
        x, y = P[k]; s = R.T[k]["sig"]
        ax.add_patch(Rectangle((x-W/2, y-H/2), W, H, fc=COL[s]+"2A", ec=ROJO, lw=2.0, zorder=4))
        ax.plot([x-W/2, x+W/2], [y+H/2-0.30, y+H/2-0.30], color=ROJO, lw=0.8, zorder=5)
        ax.plot([x-W/2, x+W/2], [y-H/2+0.26, y-H/2+0.26], color=ROJO, lw=0.8, zorder=5)
        ax.text(x, y+H/2-0.15, k, ha="center", va="center", fontsize=10, fontweight="bold", zorder=6)
        ax.text(x, y+0.08, corta(R.T[k]["desc"], 30), ha="center", va="center",
                fontsize=5.9, color="#222222", zorder=6, linespacing=1.25)
        ax.text(x, y-H/2+0.13, f"{R.fnum(R.T[k]['dur'])} d   ·   acum {M['EF'][k]:.2f} d",
                ha="center", va="center", fontsize=6.8, color=GRIS, zorder=6)
    ax.add_patch(FancyBboxPatch((-W/2-1.55, -0.35), 1.0, 0.7, boxstyle="round,pad=0.05",
                                fc="white", ec=GRIS, lw=1.3, zorder=4))
    ax.text(-W/2-1.05, 0, "INICIO", ha="center", va="center", fontsize=8, fontweight="bold", zorder=5)
    ax.add_patch(FancyArrowPatch((-W/2-0.55, 0), (-W/2, 0), arrowstyle="-|>", mutation_scale=13,
                                 linewidth=2.2, color=ROJO, zorder=3))
    ux, uy = P[cad[-1]]
    ax.add_patch(FancyBboxPatch((ux+W/2+0.55, uy-0.35), 1.0, 0.7, boxstyle="round,pad=0.05",
                                fc="white", ec=GRIS, lw=1.3, zorder=4))
    ax.text(ux+W/2+1.05, uy, "FIN", ha="center", va="center", fontsize=8, fontweight="bold", zorder=5)
    ax.add_patch(FancyArrowPatch((ux+W/2, uy), (ux+W/2+0.55, uy), arrowstyle="-|>",
                                 mutation_scale=13, linewidth=2.2, color=ROJO, zorder=3))
    vis = sorted({R.T[k]["sig"] for k in cad}, key=lambda s: list(COL).index(s))
    hs = [Line2D([0],[0], marker="s", color="white", markerfacecolor=COL[s]+"55",
                 markeredgecolor=COL[s], markersize=12, label=f"{s} = {NOMA[s]}") for s in vis]
    ax.legend(handles=hs, loc="lower center", bbox_to_anchor=(0.5,-0.10),
              ncol=len(vis), fontsize=8.5, framealpha=1)
    ax.set_title("FIG. 2  RUTA CRÍTICA EN DETALLE", fontsize=13.5, fontweight="bold", pad=12)
    ax.text(0.5, 1.004, f"{len(cad)} actividades  ·  duración {M['TOTAL']:.2f} días hábiles  ·  "
            "criterio: 8 h = 1 día, los rangos se toman en su valor mayor",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.2, color=GRIS)
    xs=[p[0] for p in P.values()]; ys=[p[1] for p in P.values()]
    ax.set_xlim(min(xs)-W/2-2.0, max(xs)+W/2+2.0); ax.set_ylim(min(ys)-H, max(ys)+H)
    ax.set_aspect("equal"); ax.axis("off")
    guarda(fig, "Fig2_Ruta_critica_detalle")

# ===================================================== FIG 3 — red medida (holgura <= 5 d)
def fig3():
    M = R.V2
    sel = [k for k in M["topo"] if M["HT"][k] <= 5.0]
    W, H, ESC, DY = 1.72, 1.02, 0.66, 1.46
    sig = list(COL)
    P = {}
    for li, s_ in enumerate(sig):                     # un carril por área
        y = -li*DY
        ks = sorted([k for k in sel if R.T[k]["sig"] == s_], key=lambda k: M["ES"][k])
        xprev = -1e9
        for k in ks:
            x = max(M["ES"][k]*ESC, xprev + W + 0.28)   # evita traslape dentro del carril
            P[k] = (x, y); xprev = x
    fig, ax = plt.subplots(figsize=(22, 9.0))
    for k in sel:
        for p in M["pre"][k]:
            if p not in P: continue
            (x1,y1),(x2,y2) = P[p], P[k]
            cr = M["HT"][p] == 0 and M["HT"][k] == 0
            a = (x1+W/2, y1) if x2 > x1 else (x1, y1-H/2 if y2 < y1 else y1+H/2)
            b = (x2-W/2, y2) if x2 > x1 else (x2, y2+H/2 if y2 < y1 else y2-H/2)
            rad = 0.0 if abs(y1-y2) < 0.05 else (0.10 if y2 < y1 else -0.10)
            ax.add_patch(FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}",
                arrowstyle="-|>", mutation_scale=9,
                linewidth=2.0 if cr else 0.6, color=ROJO if cr else "#00000055",
                zorder=3 if cr else 2, shrinkA=0, shrinkB=0))
    for k in sel:
        x, y = P[k]; s_ = R.T[k]["sig"]; cr = M["HT"][k] == 0
        ec = ROJO if cr else COL[s_]
        ax.add_patch(Rectangle((x-W/2, y-H/2), W, H, fc=COL[s_]+"22", ec=ec,
                               lw=1.9 if cr else 0.9, zorder=4))
        y1_, y2_ = y+H/2-0.30*H, y-H/2+0.30*H
        ax.plot([x-W/2,x+W/2],[y1_,y1_], color=ec, lw=0.55, zorder=5)
        ax.plot([x-W/2,x+W/2],[y2_,y2_], color=ec, lw=0.55, zorder=5)
        ax.plot([x,x],[y1_,y+H/2], color=ec, lw=0.4, zorder=5)
        f = R.fnum
        ax.text(x-W/4, y+H/2-0.15*H, f(M['ES'][k]), ha="center", va="center", fontsize=5.2, zorder=6)
        ax.text(x+W/4, y+H/2-0.15*H, f(M['EF'][k]), ha="center", va="center", fontsize=5.2, zorder=6)
        ax.text(x, y+0.065, k, ha="center", va="center", fontsize=8.0, fontweight="bold",
                color=ROJO if cr else "black", zorder=6)
        ax.text(x, y-H/2+0.15*H, f"{f(R.T[k]['dur'])} d   h {f(M['HT'][k])}",
                ha="center", va="center", fontsize=5.2,
                fontweight="bold" if cr else "normal", color=ROJO if cr else GRIS, zorder=6)

    xmin = min(p[0] for p in P.values())
    for li, s_ in enumerate(sig):
        if not any(R.T[k]["sig"] == s_ for k in sel): continue
        ax.text(xmin-W/2-0.45, -li*DY, f"{s_}", ha="right", va="center",
                fontsize=13, fontweight="bold", color=COL[s_])
        ax.text(xmin-W/2-1.05, -li*DY, corta(NOMA[s_], 16), ha="right", va="center",
                fontsize=7.2, color=GRIS)
    hs = [Line2D([0],[0], color=ROJO, lw=2.2, label="Ruta crítica (holgura total = 0)"),
          Line2D([0],[0], color="#00000055", lw=0.8, label="Otras dependencias"),
          Line2D([0],[0], color="white", lw=0,
                 label="Caja:  arriba TPI | TPT   ·   centro clave   ·   abajo duración y holgura total (h)")]
    ax.legend(handles=hs, loc="lower center", bbox_to_anchor=(0.5,-0.10), ncol=3, fontsize=8.6, framealpha=1)
    ax.set_title("FIG. 3  RED MEDIDA — actividades con holgura total menor o igual a 5 días",
                 fontsize=13.5, fontweight="bold", pad=14)
    ax.text(0.5, 1.006, f"{len(sel)} de las 257 actividades, en carriles por área  ·  "
            f"duración de la red {M['TOTAL']:.2f} días hábiles  ·  el eje horizontal es aproximadamente el tiempo",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.2, color=GRIS)
    px=[p[0] for p in P.values()]; py=[p[1] for p in P.values()]
    ax.set_xlim(min(px)-W/2-4.2, max(px)+W); ax.set_ylim(min(py)-H, max(py)+H)
    ax.set_aspect("equal"); ax.axis("off")
    guarda(fig, "Fig3_Red_medida")

# ===================================================== FIG 4 — carga por persona
def fig4():
    M = R.V2
    orden = sorted(R.AREAS, key=lambda a: -R.CARGA[a])
    carga = [R.CARGA[a] for a in orden]
    vent  = [R.VENTANA[a] for a in orden]
    etiq  = [f"{R.RESP[a]}\n{R.SIGLA[a]} — {a.split(chr(44))[0][:26]}" for a in orden]
    y = range(len(orden))[::-1]
    fig, ax = plt.subplots(figsize=(13.5, 6.6))
    ax.barh([i+0.19 for i in y], vent, height=0.36, color="#cfd8e3",
            edgecolor="#7a8ba0", label="Ventana que le concede el cronograma")
    for i, (c, v) in zip(y, zip(carga, vent)):
        sob = c > v
        ax.barh(i-0.19, c, height=0.36, color=(ROJO+"CC") if sob else "#8FBC3F",
                edgecolor=ROJO if sob else "#5f8524")
    ax.axvline(M["TOTAL"], color=GRIS, ls="--", lw=1.4)
    ax.text(M["TOTAL"], len(orden)-0.35, f" ruta crítica\n {M['TOTAL']:.1f} d",
            fontsize=8.2, color=GRIS, va="top")
    ax.axvline(49, color="#0b5394", ls=":", lw=1.8)
    ax.text(47, len(orden)-0.35, " disponible hasta\n 13-nov: 49 d",
            fontsize=8.2, color="#0b5394", va="top")
    for i, (c, v) in zip(y, zip(carga, vent)):
        pct = 100*c/v if v else 0
        ax.text(c+0.9, i-0.19, f"{c:.1f} d   ({pct:.0f} % de su ventana)",
                va="center", fontsize=8.2, color=ROJO if c > v else "#3d5c16", fontweight="bold")
        ax.text(v+0.9, i+0.19, f"{v:.1f} d", va="center", fontsize=7.6, color="#5a6b80")
    ax.set_yticks(list(y)); ax.set_yticklabels(etiq, fontsize=8.4)
    ax.set_xlabel("Días hábiles", fontsize=9.5)
    ax.set_xlim(0, 82)
    hs = [Line2D([0],[0], marker="s", color="white", markerfacecolor=ROJO+"CC",
                 markeredgecolor=ROJO, markersize=12, label="Carga de trabajo — excede su ventana"),
          Line2D([0],[0], marker="s", color="white", markerfacecolor="#8FBC3F",
                 markeredgecolor="#5f8524", markersize=12, label="Carga de trabajo — cabe en su ventana"),
          Line2D([0],[0], marker="s", color="white", markerfacecolor="#cfd8e3",
                 markeredgecolor="#7a8ba0", markersize=12, label="Ventana que concede el cronograma")]
    ax.legend(handles=hs, loc="lower right", fontsize=8.5, framealpha=1)
    ax.set_title("FIG. 4  CARGA DE TRABAJO POR PERSONA CONTRA LA VENTANA DISPONIBLE",
                 fontsize=13, fontweight="bold", pad=24)
    ax.text(0.5, 1.028, "La ruta crítica supone recursos ilimitados. Con una persona por área, el límite real es la carga individual.",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.2, color=GRIS)
    ax.grid(axis="x", alpha=0.25, lw=0.6); ax.set_axisbelow(True)
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    fig.tight_layout()
    guarda(fig, "Fig4_Carga_por_persona")

fig1(); fig2(); fig3(); fig4()
