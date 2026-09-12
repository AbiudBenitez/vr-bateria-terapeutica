# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import aoa

NODOS = {
 0:(0.0,0.0), 1:(1.3,0.0), 2:(2.3,2.4), 3:(3.0,0.0),
 4:(4.35,-1.15), 5:(4.35,0.35), 6:(5.5,2.0), 7:(6.6,2.0),
 8:(7.6,3.2), 9:(9.0,3.2), 10:(10.2,1.9), 11:(11.4,1.9),
 12:(4.2,-2.6), 13:(5.6,-3.9), 14:(7.0,-3.9), 15:(8.4,-2.6), 16:(9.8,-2.6),
 17:(12.7,-1.7), 18:(13.9,-1.7), 19:(15.1,0.6), 20:(16.3,0.6),
}
# (clave, i, j, rad, ficticia)
ARCOS = [
 ("A",0,1,0.0,0),("B",1,2,0.0,0),("C",1,3,0.0,0),("",2,3,0.0,1),
 ("D",3,6,0.0,0),("E",3,5,0.0,0),("F",3,4,0.0,0),("",5,6,0.0,1),("",4,6,0.0,1),
 ("G-2",3,12,0.0,0),("G-1",6,7,0.0,0),
 ("H-1",7,10,0.0,0),("I-1",7,8,0.0,0),("J-1",8,9,0.0,0),("K-1",9,10,0.0,0),
 ("L-1",10,11,0.0,0),("M-1",9,17,0.22,0),("N-1",11,19,0.12,0),("O-1",11,17,0.0,0),
 ("H-2",12,15,0.0,0),("I-2",12,13,0.0,0),("J-2",13,14,0.0,0),("K-2",14,15,0.0,0),
 ("L-2",15,16,0.0,0),("M-2",14,17,0.20,0),("N-2",16,19,-0.30,0),("O-2",16,17,0.0,0),
 ("P",17,18,0.0,0),("Q",18,19,0.0,0),("R",19,20,0.0,0),
]
TPOS = {"O-1":0.70, "N-2":0.72, "M-1":0.58, "M-2":0.60, "N-1":0.42, "D":0.70, "H-1":0.42}
RN = 0.30

def bezier(P0,P1,rad,t):
    x1,y1=P0; x2,y2=P1; dx,dy=x2-x1,y2-y1
    cx,cy=(x1+x2)/2+rad*dy,(y1+y2)/2-rad*dx
    u=1-t
    return (u*u*x1+2*u*t*cx+t*t*x2, u*u*y1+2*u*t*cy+t*t*y2)

def recorta(P0,P1,r):
    import math
    x1,y1=P0; x2,y2=P1; L=math.hypot(x2-x1,y2-y1)
    if L==0: return P0,P1
    ux,uy=(x2-x1)/L,(y2-y1)/L
    return (x1+ux*r,y1+uy*r),(x2-ux*r,y2-uy*r)

def dibuja(salida, titulo, sub, modo):
    """modo: 'logico' | 'medida' | 'critica'"""
    fig,ax=plt.subplots(figsize=(17.5,8.9))
    crit_ev = {e for e in range(aoa.NEV) if aoa.TPI[e]==aoa.TRT[e]}
    for clave,i,j,rad,fic in ARCOS:
        p0,p1=NODOS[i],NODOS[j]
        a,b=recorta(p0,p1,RN)
        es_crit = (modo=="critica") and (clave in aoa.CRIT)
        if fic:
            col,ls,lw,zo="0.55","--",1.4,1
        elif es_crit:
            col,ls,lw,zo="#b00020","-",3.0,3
        else:
            col,ls,lw,zo="0.15","-",1.5,2
        ax.add_patch(FancyArrowPatch(a,b,connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>",mutation_scale=15,linewidth=lw,linestyle=ls,color=col,zorder=zo))
        if clave:
            t=TPOS.get(clave,0.5)
            mx,my=bezier(p0,p1,rad,t)
            if modo=="logico": txt=clave
            else: txt=f"{clave}\n{aoa.DUR[clave]}"
            ax.text(mx,my,txt,ha="center",va="center",fontsize=8.2,
                    fontweight="bold" if es_crit else "normal",
                    color="#b00020" if es_crit else "black",zorder=5,
                    bbox=dict(boxstyle="round,pad=0.18",fc="white",
                              ec="#b00020" if es_crit else "0.7",lw=0.9,alpha=0.95))
    for e,(x,y) in NODOS.items():
        cr = (modo=="critica" and e in crit_ev)
        ax.add_patch(Circle((x,y),RN,fc="white",
                            ec="#b00020" if cr else "0.15",
                            lw=2.2 if cr else 1.4,zorder=6))
        ax.text(x,y,str(e),ha="center",va="center",fontsize=9,fontweight="bold",zorder=7)
        if modo in ("medida","critica"):
            ax.text(x,y+RN+0.20,f"{aoa.TPI[e]}",ha="center",va="bottom",fontsize=7.5,
                    color="#0b5394",zorder=7)
            ax.text(x,y-RN-0.20,f"{aoa.TRT[e]}",ha="center",va="top",fontsize=7.5,
                    color="#7f6000",zorder=7)
    hs=[]
    from matplotlib.lines import Line2D
    hs.append(Line2D([0],[0],color="0.15",lw=1.5,label="Actividad real"))
    hs.append(Line2D([0],[0],color="0.55",lw=1.4,ls="--",label="Actividad ficticia (duración 0)"))
    if modo=="critica":
        hs.append(Line2D([0],[0],color="#b00020",lw=3.0,label="Ruta crítica"))
    if modo in ("medida","critica"):
        hs.append(Line2D([0],[0],color="#0b5394",lw=0,marker="$T\\!P\\!I$",markersize=16,
                         label="Arriba del nodo: tiempo próximo"))
        hs.append(Line2D([0],[0],color="#7f6000",lw=0,marker="$T\\!R\\!T$",markersize=16,
                         label="Abajo del nodo: tiempo remoto"))
    ax.legend(handles=hs,loc="lower right",fontsize=8.5,framealpha=0.95)
    ax.set_title(titulo,fontsize=13,fontweight="bold",pad=14)
    ax.text(0.5,1.005,sub,transform=ax.transAxes,ha="center",va="bottom",fontsize=9.5,color="0.3")
    ax.set_xlim(-0.9,17.3); ax.set_ylim(-4.9,4.3)
    ax.set_aspect("equal"); ax.axis("off")
    plt.tight_layout()
    plt.savefig(salida,dpi=200,bbox_inches="tight",facecolor="white")
    plt.close()
    print("OK",salida)

D="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/tareas/2026-09-04-ejemplo-ruta-critica/"
SUB="Obtención de aceites esenciales de hierbabuena y menta"
dibuja(D+"Fig1_Arreglo_Logico.png","FIG. 1  ARREGLO LÓGICO",SUB,"logico")
dibuja(D+"Fig2_Red_Medida.png","FIG. 2  RED MEDIDA — tiempos próximos y remotos de los eventos",
       SUB+"   ·   duración total: 220 días","medida")
dibuja(D+"Fig3_Ruta_Critica.png","FIG. 3  RUTA CRÍTICA",
       "A → C → D → G-1 → I-1 → J-1 → K-1 → L-1 → N-1 → R   ·   220 días","critica")
