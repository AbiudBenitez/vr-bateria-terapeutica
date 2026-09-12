# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
import pdm

W, H = 2.30, 1.26          # tamano de caja
COLS = sorted(set(pdm.ES.values()))
CX = {es: i*3.00 for i, es in enumerate(COLS)}
LANE = {
 "A":7.2,"B":5.6,"C":4.0,"D":4.0,"E":4.0,"F":4.0,"G":4.0,
 "H":1.6,"I":2.4,"J":0.8,"K":1.6,"L":1.6,
 "M":-0.8,"N":-0.8,"O":-0.8,"P":-0.8,"Q":-0.8,"R":-0.8,"S":-0.8,
 "T":-2.4,"U":-2.4,"V":-2.4,
 "W":-4.0,"Y-1":-4.0,
 "X":-0.8,"Y-2":-2.4,"Z":-1.6,
}
POS = {k: (CX[pdm.ES[k]], LANE[k]) for k in pdm.ORD}
ROJO = "#b00020"

CORTO = {
 "A":"Gestión inicial","B":"Investig. musicoterapia","C":"Perfil del asesor",
 "D":"Confirmación asesor","E":"Rutinas rítmicas","F":"Métricas motrices",
 "G":"Protocolo de sesión","H":"Diseño conceptual","I":"Modelado batería",
 "J":"Baquetas y entorno","K":"Texturizado","L":"Optimización VR",
 "M":"Unity + SDK Meta","N":"Spike de latencia","O":"Mapeo de controles",
 "P":"Colisiones","Q":"Velocidad de impacto","R":"Integración 3D+físicas",
 "S":"Ergonomía","T":"Samples y velocity","U":"Audio + físicas",
 "V":"Rutinas en simulador","W":"Menús, UI y métricas","X":"Build candidata",
 "Y-1":"Plan de pruebas","Y-2":"Pruebas rendimiento","Z":"Pruebas y cierre",
}

def caja(ax, k, medida):
    x, y = POS[k]
    cr = medida and pdm.HT[k] == 0
    ec = ROJO if cr else "0.15"
    lw = 2.2 if cr else 1.2
    ax.add_patch(Rectangle((x-W/2, y-H/2), W, H, fc="white", ec=ec, lw=lw, zorder=4))
    if medida:
        y1, y2 = y+H/2-0.30*H, y-H/2+0.30*H
        ax.plot([x-W/2, x+W/2], [y1, y1], color=ec, lw=0.8, zorder=5)
        ax.plot([x-W/2, x+W/2], [y2, y2], color=ec, lw=0.8, zorder=5)
        for xx in (x-W/6, x+W/6):
            ax.plot([xx, xx], [y1, y+H/2], color=ec, lw=0.6, zorder=5)
            ax.plot([xx, xx], [y-H/2, y2], color=ec, lw=0.6, zorder=5)
        ax.text(x-W/3, y+H/2-0.15*H, str(pdm.ES[k]), ha="center", va="center", fontsize=7, zorder=6)
        ax.text(x,     y+H/2-0.15*H, str(pdm.DUR[k]), ha="center", va="center", fontsize=7,
                fontweight="bold", zorder=6)
        ax.text(x+W/3, y+H/2-0.15*H, str(pdm.EF[k]), ha="center", va="center", fontsize=7, zorder=6)
        ax.text(x-W/3, y-H/2+0.15*H, str(pdm.LS[k]), ha="center", va="center", fontsize=7, zorder=6)
        ax.text(x,     y-H/2+0.15*H, str(pdm.HT[k]), ha="center", va="center", fontsize=7,
                color=ROJO if cr else "0.35", fontweight="bold", zorder=6)
        ax.text(x+W/3, y-H/2+0.15*H, str(pdm.LF[k]), ha="center", va="center", fontsize=7, zorder=6)
        ax.text(x, y+0.085, k, ha="center", va="center", fontsize=9.5, fontweight="bold",
                color=ROJO if cr else "black", zorder=6)
        ax.text(x, y-0.135, CORTO[k], ha="center", va="center", fontsize=5.9, color="0.3", zorder=6)
    else:
        ax.text(x, y+0.20, k, ha="center", va="center", fontsize=11, fontweight="bold", zorder=6)
        ax.text(x, y-0.05, CORTO[k], ha="center", va="center", fontsize=6.2, color="0.25", zorder=6)
        ax.text(x, y-0.30, f"{pdm.DUR[k]} d", ha="center", va="center", fontsize=7.5,
                color="0.35", zorder=6)

def flecha(ax, p, k, tipo, demora, medida):
    x1, y1 = POS[p]; x2, y2 = POS[k]
    crit = pdm.HT[p] == 0 and pdm.HT[k] == 0
    col = ROJO if (medida and crit) else ("0.25" if tipo == "FS" else "#0b5394")
    lw  = 2.4 if (medida and crit) else 1.2
    ls  = "-" if tipo == "FS" else (0, (5, 2))
    if abs(x1-x2) < 0.01:                       # misma columna: vertical
        a = (x1, y1-H/2 if y1 > y2 else y1+H/2)
        b = (x2, y2+H/2 if y1 > y2 else y2-H/2)
        # arquear solo si hay una caja intermedia en la misma columna
        estorbo = any(abs(px-x1) < 0.01 and min(y1,y2) < py < max(y1,y2)
                      for px, py in POS.values())
        if estorbo:
            rad = 3.4/abs(y2-y1) * (-1 if y1 > y2 else 1)
        else:
            rad = 0.0
    else:
        a = (x1+W/2, y1); b = (x2-W/2, y2)
        dy = abs(y2-y1)
        rad = 0.0 if dy < 0.1 else (0.10 if y2 < y1 else -0.10)
        if abs(x2-x1) > 6: rad *= 1.6
    ax.add_patch(FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}",
        arrowstyle="-|>", mutation_scale=11, linewidth=lw, linestyle=ls,
        color=col, zorder=3, shrinkA=0, shrinkB=0))
    if tipo != "FS" or demora:
        et = tipo + (f"+{demora}" if demora else "")
        if abs(a[0]-b[0]) < 0.01:
            mx, my = a[0] + rad*(b[1]-a[1])/2, (a[1]+b[1])/2
        else:
            mx, my = (a[0]+b[0])/2 + rad*(b[1]-a[1]), (a[1]+b[1])/2 - rad*(b[0]-a[0])
        ax.text(mx, my, et, ha="center", va="center", fontsize=6.2, color=col,
                zorder=7, bbox=dict(boxstyle="round,pad=0.14", fc="white", ec=col, lw=0.6))

def dibuja(salida, titulo, sub, medida):
    fig, ax = plt.subplots(figsize=(24, 7.6))
    for k in pdm.ORD:
        for p, t, l in pdm.PRE[k]:
            flecha(ax, p, k, t, l, medida)
    for k in pdm.ORD:
        caja(ax, k, medida)
    hs = [Line2D([0],[0], color="0.25", lw=1.2, label="Dependencia fin → inicio (FS)"),
          Line2D([0],[0], color="#0b5394", lw=1.2, ls=(0,(5,2)),
                 label="Dependencia inicio → inicio (SS) con demora, en días")]
    if medida:
        hs.append(Line2D([0],[0], color=ROJO, lw=2.4, label="Ruta crítica (holgura total = 0)"))
        hs.append(Line2D([0],[0], color="white", lw=0,
                 label="Caja:  arriba TPI · duración · TPT   /   abajo TRI · holgura total · TRT"))
    ax.legend(handles=hs, loc="upper right", fontsize=8, framealpha=0.96)
    ax.set_title(titulo, fontsize=14, fontweight="bold", pad=12)
    ax.text(0.5, 1.006, sub, transform=ax.transAxes, ha="center", va="bottom",
            fontsize=10, color="0.3")
    xs = [p[0] for p in POS.values()]; ys = [p[1] for p in POS.values()]
    ax.set_xlim(min(xs)-W, max(xs)+W+0.4); ax.set_ylim(min(ys)-H, max(ys)+H+0.5)
    ax.set_aspect("equal"); ax.axis("off")
    plt.tight_layout()
    plt.savefig(salida, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(); print("OK", salida)

D = "/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/figuras/"
os.makedirs(D, exist_ok=True)
dibuja(D+"Fig1_Red_PDM.png", "FIG. 1  RED DE PRECEDENCIAS (PDM / AON)",
       "Simulador de batería en realidad virtual con enfoque de musicoterapia  ·  27 actividades", False)
dibuja(D+"Fig2_Red_Medida_Ruta_Critica.png",
       "FIG. 2  RED MEDIDA Y RUTA CRÍTICA",
       f"Duración de la red: {pdm.TOTAL} días hábiles  ·  1-sep-2026 a 10-nov-2026", True)
