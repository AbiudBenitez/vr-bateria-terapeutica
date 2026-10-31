# -*- coding: utf-8 -*-
"""Figuras de la ruta critica v3: las tres redes y la red remanente.

Escala de grises, sin color. SVG con texto editable, igual que el resto del
proyecto. Todo sale de `rc_recorte.py`: si una decision del recorte cambia,
las figuras cambian al regenerarse.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"
import matplotlib.pyplot as plt

import rc257 as R
import rc_recorte as X

SAL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "entregables", "figuras-ruta-critica-v3")
os.makedirs(SAL, exist_ok=True)

NEGRO = "0.15"


def guardar(fig, nombre):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(SAL, "%s.%s" % (nombre, ext)),
                    dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  OK", nombre)


def comparacion():
    """Las cuatro lecturas de la red, de la linea base anterior a lo que falta."""
    datos = [
        ("Línea base anterior\n257 actividades", R.V2["TOTAL"], "0.55"),
        ("Recortada, enlaces\nreconectados", X.PUENTE["TOTAL"], "0.25"),
        ("Recortada, borrando\nsin reconectar", X.INGENUA["TOTAL"], "0.80"),
        ("Lo que falta\ndesde el 22 de octubre", X.REMANENTE["TOTAL"], "0.10"),
    ]
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    for i, (etq, val, col) in enumerate(datos):
        ax.barh(len(datos) - i, val, height=0.56, color=col, edgecolor=NEGRO, linewidth=0.8)
        ax.text(val + 0.5, len(datos) - i, "%.2f d" % val, va="center", fontsize=10,
                fontweight="bold")
        ax.text(-0.6, len(datos) - i, etq, va="center", ha="right", fontsize=9)
    ax.set_xlim(0, max(v for _, v, _ in datos) + 6)
    ax.set_ylim(0.3, len(datos) + 0.8)
    ax.set_yticks([])
    ax.set_xlabel("Días hábiles", fontsize=9)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="0.9", linewidth=0.6)
    ax.set_axisbelow(True)
    guardar(fig, "Fig1_Comparacion_de_redes")


def remanente():
    """Red medida de lo que falta, con la holgura de cada actividad."""
    M = X.REMANENTE
    orden = sorted(X.PENDIENTES, key=lambda k: (M["ES"][k], -M["EF"][k], k))
    fig, ax = plt.subplots(figsize=(11.5, 7.4))
    for i, k in enumerate(orden):
        y = len(orden) - i
        crit = abs(M["HT"][k]) < 1e-6
        dur = R.T[k]["dur"]
        ax.barh(y, dur if dur else 0.12, left=M["ES"][k], height=0.6,
                color="0.2" if crit else "0.75", edgecolor=NEGRO, linewidth=0.6, zorder=3)
        if M["HT"][k] > 0:
            ax.barh(y, M["HT"][k], left=M["EF"][k], height=0.6, color="white",
                    edgecolor="0.6", linewidth=0.6, linestyle=(0, (3, 2)), zorder=2)
        ax.text(M["ES"][k] - 0.25, y, k, ha="right", va="center", fontsize=8.5,
                fontweight="bold" if crit else "normal")
        ax.text(M["ES"][k] + max(dur, 0.12) + M["HT"][k] + 0.3, y,
                R.T[k]["desc"][:62], ha="left", va="center", fontsize=7.4, color="0.25")
    ax.axvline(M["TOTAL"], color=NEGRO, linewidth=1.1, linestyle=(0, (5, 3)), zorder=1)
    ax.text(M["TOTAL"], len(orden) + 1.0, "fin de la red: %.0f días hábiles (11-nov)"
            % M["TOTAL"], fontsize=8.5, ha="center", color="0.15")
    ax.axvline(16, color="0.35", linewidth=1.0, zorder=1)
    ax.text(16.25, 1.2, "entrega comprometida\n13-nov", fontsize=8, ha="left",
            va="center", color="0.3")
    ax.set_xlim(-3.2, 26)
    ax.set_ylim(0.2, len(orden) + 1.6)
    ax.set_yticks([])
    ax.set_xticks(range(0, 17, 2))
    ax.set_xlabel("Días hábiles desde la fecha de corte (23 de octubre de 2026)", fontsize=9)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="0.9", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    guardar(fig, "Fig2_Red_remanente")


def criticidad():
    """De donde salio y adonde se fue la criticidad, por area."""
    antes = {}
    despues = {}
    for k in R.V2["CRIT"]:
        antes[R.T[k]["area"]] = antes.get(R.T[k]["area"], 0) + 1
    for k in X.PUENTE["CRIT"]:
        despues[R.T[k]["area"]] = despues.get(R.T[k]["area"], 0) + 1
    areas = sorted(set(antes) | set(despues), key=lambda a: -(antes.get(a, 0) + despues.get(a, 0)))
    fig, ax = plt.subplots(figsize=(9.8, 4.6))
    y = range(len(areas))
    ax.barh([i + 0.2 for i in y], [antes.get(a, 0) for a in areas], height=0.38,
            color="0.72", edgecolor=NEGRO, linewidth=0.7, label="Antes del recorte")
    ax.barh([i - 0.2 for i in y], [despues.get(a, 0) for a in areas], height=0.38,
            color="0.22", edgecolor=NEGRO, linewidth=0.7, label="Después del recorte")
    ax.set_yticks(list(y))
    ax.set_yticklabels([a[:30] for a in areas], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel("Actividades con holgura total cero", fontsize=9)
    ax.legend(fontsize=8.5, frameon=False, loc="lower right")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="0.9", linewidth=0.6)
    ax.set_axisbelow(True)
    guardar(fig, "Fig3_Criticidad_por_area")


if __name__ == "__main__":
    comparacion()
    remanente()
    criticidad()
