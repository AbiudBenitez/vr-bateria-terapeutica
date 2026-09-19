# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["font.family"] = "DejaVu Sans"
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D
import pmbok as P

SAL = "/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/tareas/2026-09-14-tabla-pmbok/figuras/"
os.makedirs(SAL, exist_ok=True)
GRIS="#444444"; AZUL="#0b5394"; ROJO="#b00020"
COLG = {"Inicio":"#4472C4","Planificación":"#2E9BB5","Ejecución":"#8FBC3F",
        "Monitoreo y Control":"#ED7D31","Cierre":"#7030A0"}
def guarda(fig,n):
    for e in ("svg","png"): fig.savefig(SAL+n+"."+e,dpi=200,bbox_inches="tight",facecolor="white")
    plt.close(fig); print("OK",n)

# ===================================================== FIG 1 — flujo de los grupos
def fig1():
    fig, ax = plt.subplots(figsize=(14.5, 7.4))
    W,H = 2.9, 1.5
    POS = {"Inicio":(0,0), "Planificación":(3.7,0), "Ejecución":(7.4,0), "Cierre":(11.1,0),
           "Monitoreo y Control":(5.55,-3.1)}
    NP  = {g: len(P.de_grupo(g)) for g in P.GRUPOS}
    for g,(x,y) in POS.items():
        ax.add_patch(FancyBboxPatch((x-W/2,y-H/2), W, H, boxstyle="round,pad=0.04",
                     fc=COLG[g]+"2E", ec=COLG[g], lw=2.2, zorder=4))
        ax.text(x, y+0.32, g, ha="center", va="center", fontsize=11, fontweight="bold", zorder=5)
        ax.text(x, y-0.02, f"{NP[g]} proceso" + ("s" if NP[g]>1 else ""), ha="center", va="center", fontsize=9, color=GRIS, zorder=5)
        ax.text(x, y-0.38, f"{100*NP[g]/49:.0f} % del total", ha="center", va="center",
                fontsize=8, color=GRIS, zorder=5)
    sec = [("Inicio","Planificación"),("Planificación","Ejecución"),("Ejecución","Cierre")]
    for a,b in sec:
        x1,_=POS[a]; x2,_=POS[b]
        ax.add_patch(FancyArrowPatch((x1+W/2,0),(x2-W/2,0), arrowstyle="-|>", mutation_scale=16,
                     lw=2.2, color=GRIS, zorder=3))
    # retroalimentación ejecución -> planificación
    ax.add_patch(FancyArrowPatch((POS["Ejecución"][0], H/2),(POS["Planificación"][0], H/2),
                 connectionstyle="arc3,rad=0.42", arrowstyle="-|>", mutation_scale=13,
                 lw=1.5, ls=(0,(5,2)), color=AZUL, zorder=3))
    ax.text(5.55, 1.72, "replanificación por cambios aprobados", ha="center", va="bottom",
            fontsize=8.4, color=AZUL, style="italic")
    # monitoreo abarca todo
    for g in ("Inicio","Planificación","Ejecución","Cierre"):
        x,_ = POS[g]
        ax.add_patch(FancyArrowPatch((x, -H/2),(POS["Monitoreo y Control"][0]+(x-POS["Monitoreo y Control"][0])*0.22, -3.1+H/2),
                     connectionstyle="arc3,rad=0.0", arrowstyle="-|>", mutation_scale=11,
                     lw=1.1, ls=(0,(4,2)), color=COLG["Monitoreo y Control"], zorder=2))
    ax.text(5.55, -4.15, "Monitoreo y Control se ejecuta en paralelo a todos los demás grupos,\n"
            "de principio a fin. No es una etapa: es una actividad continua.",
            ha="center", va="top", fontsize=9, color=COLG["Monitoreo y Control"])
    hs=[Line2D([0],[0],color=GRIS,lw=2.2,label="Secuencia principal del ciclo de vida"),
        Line2D([0],[0],color=AZUL,lw=1.5,ls=(0,(5,2)),label="Retroalimentación: cambios que obligan a replanificar"),
        Line2D([0],[0],color=COLG["Monitoreo y Control"],lw=1.1,ls=(0,(4,2)),label="Vigilancia continua sobre cada grupo")]
    ax.legend(handles=hs, loc="lower center", bbox_to_anchor=(0.5,-0.02), ncol=3, fontsize=8.6, framealpha=1)
    ax.set_title("FIG. 1  LOS CINCO GRUPOS DE PROCESOS Y SU INTERACCIÓN",
                 fontsize=13, fontweight="bold", pad=18)
    ax.text(0.5,1.015,"Guía del PMBOK, 6.ª edición · 49 procesos en total",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.4, color=GRIS)
    ax.set_xlim(-2.1,13.1); ax.set_ylim(-5.4,2.6); ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(); guarda(fig,"Fig1_Grupos_de_procesos")

# ===================================================== FIG 2 — modelo ITTO
def fig2():
    fig, ax = plt.subplots(figsize=(14, 6.2))
    W,H = 3.6, 2.5
    cajas = [
     (0, "ENTRADAS", "#4472C4", ["Documentos que el proceso\nnecesita para operar","Salidas de procesos previos",
        "Factores ambientales\nde la empresa","Activos de los procesos\nde la organización"]),
     (5.0, "HERRAMIENTAS\nY TÉCNICAS", "#ED7D31", ["Juicio de expertos","Análisis de datos","Reuniones",
        "Técnicas propias de\ncada proceso"]),
     (10.0, "SALIDAS", "#8FBC3F", ["Documentos o entregables\nque el proceso produce","Actualizaciones al plan",
        "Actualizaciones a los\ndocumentos del proyecto","Solicitudes de cambio"]),
    ]
    for x, tit, col, items in cajas:
        ax.add_patch(FancyBboxPatch((x-W/2,-H/2), W, H, boxstyle="round,pad=0.05",
                     fc=col+"22", ec=col, lw=2.2, zorder=3))
        ax.text(x, H/2-0.34, tit, ha="center", va="center", fontsize=11.5, fontweight="bold",
                color=col, zorder=4, linespacing=1.2)
        for i,it in enumerate(items):
            ax.text(x, H/2-0.86-i*0.44, "· "+it, ha="center", va="center", fontsize=7.6,
                    color="#222222", zorder=4, linespacing=1.15)
    for x1,x2 in ((0,5.0),(5.0,10.0)):
        ax.add_patch(FancyArrowPatch((x1+W/2,0),(x2-W/2,0), arrowstyle="-|>", mutation_scale=18,
                     lw=2.6, color=GRIS, zorder=2))
    ax.add_patch(FancyArrowPatch((10.0, -H/2),(0, -H/2), connectionstyle="arc3,rad=0.20",
                 arrowstyle="-|>", mutation_scale=14, lw=1.6, ls=(0,(5,2)), color=AZUL, zorder=2))
    ax.text(5.0, -2.70, "la salida de un proceso es, casi siempre, la entrada de otro",
            ha="center", va="top", fontsize=9.2, color=AZUL, style="italic")
    ax.set_title("FIG. 2  MODELO DE ENTRADAS, HERRAMIENTAS Y SALIDAS",
                 fontsize=13, fontweight="bold", pad=18)
    ax.text(0.5,1.02,"Cada uno de los 49 procesos del PMBOK se describe con esta misma estructura de tres partes",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.4, color=GRIS)
    ax.set_xlim(-2.6,12.6); ax.set_ylim(-3.6,2.0); ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(); guarda(fig,"Fig2_Modelo_ITTO")

# ===================================================== FIG 3 — matriz áreas × grupos
def fig3():
    M = P.matriz()
    nf, nc = len(P.AREAS), len(P.GRUPOS)
    DX = 1.42                                     # ancho de columna, evita encimar encabezados
    fig, ax = plt.subplots(figsize=(14.2, 9.0))
    mx = max(len(v) for v in M.values())
    def parte(procs):
        """Reparte las claves en dos renglones si son más de tres."""
        if len(procs) <= 3: return " ".join(procs)
        m = (len(procs)+1)//2
        return " ".join(procs[:m]) + "\n" + " ".join(procs[m:])
    for r,(a,nom) in enumerate(P.AREAS):
        y = nf-1-r
        for c,g in enumerate(P.GRUPOS):
            x = c*DX
            procs = M.get((a,g), []); n = len(procs)
            al = 0 if n==0 else 0.16+0.60*n/mx
            fc = "white" if n==0 else COLG[g]+f"{int(al*255):02X}"
            ax.add_patch(Rectangle((x-DX/2+0.03, y-0.5), DX-0.06, 1,
                         fc=fc, ec="#cfcfcf", lw=1.0, zorder=2))
            if n:
                ax.text(x, y+0.22, str(n), ha="center", va="center", fontsize=13,
                        fontweight="bold", color="#111111", zorder=4)
                ax.text(x, y-0.20, parte(procs), ha="center", va="center", fontsize=6.0,
                        color="#333333", zorder=4, linespacing=1.15)
        ax.text(-DX/2-0.25, y+0.13, a, ha="right", va="center", fontsize=11,
                fontweight="bold", color=GRIS)
        corto = (nom.replace("del Proyecto","").replace("de la ","").replace("de los ","")
                    .replace("de las ","").strip())
        ax.text(-DX/2-0.25, y-0.20, corto, ha="right", va="center", fontsize=7.8, color="#333333")
        ax.text((nc-1)*DX+DX/2+0.20, y, f"{len(P.de_area(a))}", ha="left", va="center",
                fontsize=10.5, fontweight="bold", color=GRIS)
    for c,g in enumerate(P.GRUPOS):
        x = c*DX
        ax.text(x, nf-0.32, g.replace(" y ","\ny "), ha="center", va="bottom", fontsize=9.4,
                fontweight="bold", color=COLG[g], linespacing=1.15)
        ax.text(x, -0.78, f"{len(P.de_grupo(g))}", ha="center", va="center", fontsize=11.5,
                fontweight="bold", color=COLG[g])
    ax.text(-DX/2-0.25, nf-0.32, "ÁREA DE CONOCIMIENTO", ha="right", va="bottom",
            fontsize=8.6, fontweight="bold", color=GRIS)
    ax.text(-DX/2-0.25, -0.78, "procesos por grupo", ha="right", va="center", fontsize=8.4, color=GRIS)
    ax.text((nc-1)*DX+DX/2+0.20, nf-0.32, "total", ha="left", va="bottom", fontsize=8.4, color=GRIS)
    ax.text((nc-1)*DX+DX/2+0.20, -0.78, "49", ha="left", va="center", fontsize=12.5,
            fontweight="bold", color=ROJO)
    ax.set_xlim(-DX/2-4.9, (nc-1)*DX+DX/2+1.1); ax.set_ylim(-1.45, nf+0.9)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("FIG. 3  MATRIZ DE ÁREAS DE CONOCIMIENTO POR GRUPOS DE PROCESOS",
                 fontsize=13, fontweight="bold", pad=30)
    ax.text(0.5,1.035,"Los 49 procesos del PMBOK 6.ª edición · la intensidad del color indica cuántos procesos concentra cada cruce",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.4, color=GRIS)
    fig.tight_layout(); guarda(fig,"Fig3_Matriz_areas_grupos")

fig1(); fig2(); fig3()
