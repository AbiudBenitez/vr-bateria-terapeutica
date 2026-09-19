# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["font.family"] = "DejaVu Sans"
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np
import rc257 as R, costos as K, compresion as C

SAL = "/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/figuras_costos/"
os.makedirs(SAL, exist_ok=True)
ROJO="#b00020"; AZUL="#0b5394"; GRIS="#444444"; VERDE="#4a7c1f"
COL = {"D":"#4472C4","J":"#7030A0","E":"#2E9BB5","M":"#ED7D31","S":"#BF9000",
       "I":"#C00060","A":"#8FBC3F","Q":"#808080"}
def guarda(fig,n):
    for e in ("svg","png"): fig.savefig(SAL+n+"."+e,dpi=200,bbox_inches="tight",facecolor="white")
    plt.close(fig); print("OK",n)

M = R.V2
def miles(x,_=None): return f"${x/1000:,.0f}k"

# ============================================ FIG 1 — curva S y valor ganado
def fig1():
    T = M["TOTAL"]; dias = np.arange(0, T+0.5, 0.25)
    acum = np.zeros_like(dias)
    for k in R.ORD:
        es, ef, c = M["ES"][k], M["EF"][k], K.costo(k)
        if ef <= es: acum += np.where(dias >= es, c, 0); continue
        acum += c*np.clip((dias-es)/(ef-es), 0, 1)
    fig, ax = plt.subplots(figsize=(12.5, 6.6))
    ax.plot(dias, acum, color=AZUL, lw=2.6, label="Valor planificado acumulado")
    ax.fill_between(dias, 0, acum, color=AZUL, alpha=0.10)
    c9 = K.corte(9.0)
    ax.axvline(9.0, color=GRIS, ls="--", lw=1.3)
    ax.plot([9.0],[c9["PV"]], "o", color=AZUL, ms=8, zorder=5)
    ax.plot([9.0],[c9["EV"]], "s", color=VERDE, ms=8, zorder=5,
            label="Valor ganado al corte de medio curso")
    ax.annotate(f"corte del {K.fecha(8):%d-%b}\nPV ${c9['PV']:,.0f}\nEV ${c9['EV']:,.0f}\nSPI {c9['EV']/c9['PV']:.3f}",
                xy=(9.0, c9["EV"]), xytext=(12.5, c9["EV"]*0.42), fontsize=8.6, color=GRIS,
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=0.9))
    ax.plot([0,T*1.02],[K.PRESUPUESTO]*2, color="#7030A0", ls="-", lw=1.8,
            label=f"Presupuesto hasta la conclusión  ${K.PRESUPUESTO:,.0f}")
    ax.text(T*0.02, K.PRESUPUESTO*0.955, "sin reserva monetaria: el proyecto no realiza compras",
            fontsize=8.2, color="#7030A0", style="italic")
    ax.set_xlabel("Días hábiles desde el 7 de septiembre de 2026", fontsize=9.5)
    ax.set_ylabel("Costo acumulado (MXN)", fontsize=9.5)
    ax.yaxis.set_major_formatter(miles)
    ax.set_xlim(0, T*1.06); ax.set_ylim(0, K.PRESUPUESTO*1.12)
    ax.grid(alpha=0.22, lw=0.6); ax.set_axisbelow(True)
    for sp in ("top","right"): ax.spines[sp].set_visible(False)
    ax.legend(loc="upper left", fontsize=8.6, framealpha=1)
    ax.set_title("FIG. 1  CURVA S Y VALOR GANADO", fontsize=13, fontweight="bold", pad=22)
    ax.text(0.5,1.03,f"Presupuesto ${K.PRESUPUESTO:,.0f} sobre {K.HORAS_TOT:,.0f} horas  ·  "
            f"regla de medición 0/100  ·  duración de la red {T:.2f} días hábiles",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.2, color=GRIS)
    fig.tight_layout(); guarda(fig,"Fig1_Curva_S")

# ============================================ FIG 2 — curva de compresión
def fig2():
    pts,_ = C.curva()
    T = [p[0] for p in pts]; G = [p[1] for p in pts]
    fig, ax = plt.subplots(figsize=(12.5, 6.4))
    ax.step(T, G, where="post", color=ROJO, lw=2.4)
    ax.plot(T, G, "o", color=ROJO, ms=3.2)
    ax.invert_xaxis()
    ax.axvline(49, color=AZUL, ls=":", lw=1.8)
    ax.text(47, max(G)*0.93, " 49 días hábiles\n disponibles hasta 13-nov",
            fontsize=8.6, color=AZUL, va="top")
    ax.annotate(f"duración normal\n{T[0]:.2f} d, sin sobrecosto",
                xy=(T[0],G[0]), xytext=(T[0]-1.0, max(G)*0.30),
                fontsize=8.4, color=GRIS, ha="left",
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=0.9))
    ax.annotate(f"compresión máxima\n{T[-1]:.2f} d por ${G[-1]:,.0f}",
                xy=(T[-1],G[-1]), xytext=(T[-1]+2.4, max(G)*0.72),
                fontsize=8.4, color=ROJO, ha="left",
                arrowprops=dict(arrowstyle="->", color=ROJO, lw=0.9))
    ax.set_xlabel("Duración del proyecto en días hábiles  (la escala avanza hacia la izquierda)", fontsize=9.5)
    ax.set_ylabel("Sobrecosto acumulado por compresión (MXN)", fontsize=9.5)
    ax.yaxis.set_major_formatter(lambda x,_: f"${x:,.0f}")
    ax.grid(alpha=0.22, lw=0.6); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.set_title("FIG. 2  CURVA DE COMPRESIÓN TIEMPO-COSTO", fontsize=13, fontweight="bold", pad=22)
    ax.text(0.5,1.03,"Cada escalón es una actividad crítica comprimida. La pendiente sube conforme se vuelven críticas más trayectorias",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.2, color=GRIS)
    fig.tight_layout(); guarda(fig,"Fig2_Curva_compresion")

# ============================================ FIG 3 — distribución del costo
def fig3():
    fig, (a1,a2) = plt.subplots(1,2, figsize=(15.5,6.4))
    areas = sorted(R.AREAS, key=lambda x: K.POR_AREA[x][2])
    y = range(len(areas))
    a1.barh(list(y), [K.POR_AREA[a][2] for a in areas],
            color=[COL[R.SIGLA[a]]+"BB" for a in areas],
            edgecolor=[COL[R.SIGLA[a]] for a in areas])
    for i,a in zip(y,areas):
        c = K.POR_AREA[a][2]
        a1.text(c+900, i, f"${c:,.0f}  ({100*c/K.MANO_OBRA:.1f}%)", va="center", fontsize=8.4)
    a1.set_yticks(list(y))
    a1.set_yticklabels([f"{R.SIGLA[a]} — {R.RESP[a]}\n{a.split(',')[0][:26]}" for a in areas], fontsize=8)
    a1.set_xlabel("Costo de mano de obra (MXN)", fontsize=9.2)
    a1.xaxis.set_major_formatter(miles)
    a1.set_xlim(0, max(K.POR_AREA[a][2] for a in areas)*1.42)
    a1.set_title("Por área de trabajo", fontsize=10.5, fontweight="bold")
    perf = sorted(K.POR_PERFIL, key=lambda x: K.POR_PERFIL[x][2])
    y2 = range(len(perf))
    a2.barh(list(y2), [K.POR_PERFIL[p][2] for p in perf], color="#8FA8C8BB", edgecolor="#5b7699")
    for i,p in zip(y2,perf):
        c = K.POR_PERFIL[p][2]
        a2.text(c+700, i, f"${c:,.0f}   {K.POR_PERFIL[p][1]:,.0f} h a ${K.PERFIL[p][0]:.0f}/h",
                va="center", fontsize=7.8)
    a2.set_yticks(list(y2)); a2.set_yticklabels(perf, fontsize=8)
    a2.set_xlabel("Costo de mano de obra (MXN)", fontsize=9.2)
    a2.xaxis.set_major_formatter(miles)
    a2.set_xlim(0, max(K.POR_PERFIL[p][2] for p in perf)*1.62)
    a2.set_title("Por perfil profesional", fontsize=10.5, fontweight="bold")
    for ax in (a1,a2):
        ax.grid(axis="x", alpha=0.22, lw=0.6); ax.set_axisbelow(True)
        for s in ("top","right","left"): ax.spines[s].set_visible(False)
    fig.suptitle("FIG. 3  DISTRIBUCIÓN DEL COSTO DE MANO DE OBRA", fontsize=13, fontweight="bold", y=1.01)
    fig.text(0.5,0.975,f"Total ${K.MANO_OBRA:,.0f} sobre {K.HORAS_TOT:,.0f} horas  ·  tarifa media ponderada ${K.TARIFA_MED:.2f}/h",
             ha="center", fontsize=9.2, color=GRIS)
    fig.tight_layout(); guarda(fig,"Fig3_Distribucion_costo")

# ============================================ FIG 4 — matriz probabilidad-impacto (días)
def fig4():
    PROB = [(0.10,"Muy baja"),(0.30,"Baja"),(0.50,"Media"),(0.70,"Alta"),(0.90,"Muy alta")]
    IMP  = [(1.0,"Muy bajo"),(2.0,"Bajo"),(3.0,"Medio"),(5.0,"Alto"),(8.0,"Muy alto")]
    def bp(p): return min(range(5), key=lambda i:(abs(p-PROB[i][0]), -i))
    def bi(x): return min(range(5), key=lambda i:(abs(x-IMP[i][0]), -i))
    fig, ax = plt.subplots(figsize=(11.5,7.6))
    for r in range(5):
        for c in range(5):
            sev = (r+1)*(c+1)
            fc = "#d7ecd1" if sev<=4 else "#fdf3cf" if sev<=9 else "#fbdcc4" if sev<=15 else "#f5c6c6"
            ax.add_patch(Rectangle((c-0.5,r-0.5),1,1,fc=fc,ec="white",lw=1.6,zorder=1))
    en = {}
    for rg in K.RIESGOS: en.setdefault((bi(rg[3]),bp(rg[2])), []).append(rg)
    for (c,r),lst in en.items():
        for j,rg in enumerate(lst):
            dx = (j-(len(lst)-1)/2)*0.26
            ax.plot(c+dx, r, "o", ms=21, color="white", mec=ROJO, mew=1.9, zorder=3)
            ax.text(c+dx, r, rg[0], ha="center", va="center", fontsize=8.2,
                    fontweight="bold", color=ROJO, zorder=4)
    ax.set_xticks(range(5)); ax.set_xticklabels([f"{n}\n≈ {v:g} d" for v,n in IMP], fontsize=8.4)
    ax.set_yticks(range(5)); ax.set_yticklabels([f"{n}\n{v:.0%}" for v,n in PROB], fontsize=8.4)
    ax.set_xlabel("Impacto sobre el cronograma, en días hábiles", fontsize=9.6)
    ax.set_ylabel("Probabilidad de ocurrencia", fontsize=9.6)
    ax.set_xlim(-0.5,4.5); ax.set_ylim(-0.5,4.5)
    for sp in ("top","right","bottom","left"): ax.spines[sp].set_visible(False)
    ax.tick_params(length=0)
    hs=[Line2D([0],[0],marker="s",color="white",markerfacecolor=c,markeredgecolor="white",markersize=13,label=l)
        for c,l in (("#d7ecd1","Bajo"),("#fdf3cf","Moderado"),("#fbdcc4","Alto"),("#f5c6c6","Muy alto"))]
    ax.legend(handles=hs, loc="lower center", bbox_to_anchor=(0.5,-0.20), ncol=4, fontsize=8.6,
              framealpha=1, title="Nivel de severidad", title_fontsize=8.6)
    ax.set_title("FIG. 4  MATRIZ DE PROBABILIDAD E IMPACTO", fontsize=13, fontweight="bold", pad=22)
    ax.text(0.5,1.03,f"Nueve riesgos  ·  el impacto se mide en días porque ninguno tiene efecto monetario  ·  "
            f"valor esperado {K.EMV_DIAS:.2f} días contra una reserva de {K.RESERVA_CRONO:.2f}",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.2, color=GRIS)
    fig.tight_layout(); guarda(fig,"Fig4_Matriz_riesgos")

fig1(); fig2(); fig3(); fig4()
