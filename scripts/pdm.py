# -*- coding: utf-8 -*-
"""Red PDM (AON) del proyecto de bateria VR terapeutica.
Dependencias: (predecesora, tipo, demora)  tipo in {FS, SS, FF}
"""
import datetime as dt

FER = {dt.date(2026,9,16)}          # dia inhabil dentro de la ventana
INICIO = dt.date(2026,9,1)          # dia habil 0

def dia(n):
    """n-esimo dia habil contado desde INICIO (0-based)."""
    c = INICIO; k = 0
    while True:
        if c.weekday() < 5 and c not in FER:
            if k == n: return c
            k += 1
        c += dt.timedelta(days=1)

def habiles(a, b):
    n = 0; c = a
    while c <= b:
        if c.weekday() < 5 and c not in FER: n += 1
        c += dt.timedelta(days=1)
    return n

# clave, nombre, paquetes EDT, responsable, duracion, [(pred, tipo, demora)]
ACT = [
("A","Gestión inicial del proyecto","1.1, 1.2, 1.3, 1.4","Gerente de proyecto",9,[]),
("B","Investigación de musicoterapia y percusión","2.1","Analista de métricas",9,[]),
("C","Definición de perfil y gestión del asesor","2.2","Coordinador",5,[]),
("D","Confirmación y contratación del asesor","2.3","Director de proyecto",3,[("C","FS",0)]),
("E","Diseño y validación de rutinas rítmicas","2.4, 2.5","Asesor terapéutico",10,[("D","FS",0),("B","FS",0)]),
("F","Definición y validación de métricas motrices","2.6, 2.7","Analista de métricas",10,[("E","SS",5)]),
("G","Protocolo de sesión y validación final","2.8, 2.9","Analista de métricas",10,[("F","FS",0)]),
("H","Diseño conceptual y referencias visuales","3.1","Artista 3D / UX-XR",4,[]),
("I","Modelado de la batería","3.2","Artista 3D",10,[("H","FS",0)]),
("J","Modelado de baquetas y entorno","3.3","Diseñador UX-XR",10,[("H","FS",0)]),
("K","Texturizado y materiales","3.4","Artista 3D",10,[("I","SS",5),("J","SS",5)]),
("L","Optimización de geometría para VR","3.5","Artista 3D / Dev RV",10,[("K","SS",5)]),
("M","Configuración de Unity y SDK de Meta","4.1","Desarrollador VR",5,[]),
("N","Spike de latencia (Go / No-Go)","4.2","Dev RV / Audio",5,[("M","FS",0)]),
("O","Mapeo de controles VR","4.3","Dev RV / UX",10,[("N","FS",0)]),
("P","Detección de colisiones","4.4","Desarrollador VR",10,[("O","SS",5)]),
("Q","Medición de velocidad de impacto","4.5","Desarrollador VR",5,[("P","SS",5)]),
("R","Integración de modelos 3D con físicas","4.6","Dev RV / Artista 3D",5,[("Q","FS",0),("L","FS",0)]),
("S","Ergonomía y prevención de motion sickness","4.7","UX-XR / Dev RV",5,[("R","FS",0)]),
("T","Librería de samples, velocity y round-robin","5.1, 5.2","Diseñador de audio",15,[("N","FS",0)]),
("U","Integración de audio con físicas","5.3","Audio / Dev RV",10,[("Q","FS",0),("T","FS",0)]),
("V","Rutinas rítmicas y guía visual en el simulador","5.4, 5.5","Dev RV / Audio",10,[("U","SS",5),("E","FS",0)]),
("W","Menús, interfaz adaptativa y registro de métricas","6.1, 6.2, 6.3","UX-XR / Métricas",10,[("R","SS",5),("S","SS",0),("F","FS",0)]),
("X","Integración general y build candidata","6.4","Dev RV / UX-XR",5,[("V","FS",0),("W","FS",0),("S","FS",0)]),
("Y-1","Plan de pruebas y casos","7.1","QA / Métricas",5,[("W","SS",5),("F","FS",0)]),
("Y-2","Pruebas de rendimiento y latencia","7.2","QA / Dev RV",5,[("X","SS",0),("Y-1","FS",0)]),
("Z","Pruebas con usuarios, corrección, documentación y cierre","7.3, 7.4, 7.5, 7.6, 1.6","Equipo completo",5,[("Y-2","FS",0),("G","FS",0)]),
]

DUR={k:d for k,_,_,_,d,_ in ACT}
PRE={k:p for k,_,_,_,_,p in ACT}
NOM={k:n for k,n,_,_,_,_ in ACT}
PAQ={k:p for k,_,p,_,_,_ in ACT}
RES={k:r for k,_,_,r,_,_ in ACT}
ORD=[k for k,_,_,_,_,_ in ACT]
SUC={k:[] for k in ORD}
for k in ORD:
    for p,t,l in PRE[k]: SUC[p].append((k,t,l))

# ---- recorrido hacia adelante
ES={}; EF={}
for k in ORD:
    c=[0]
    for p,t,l in PRE[k]:
        if   t=="FS": c.append(EF[p]+l)
        elif t=="SS": c.append(ES[p]+l)
        elif t=="FF": c.append(EF[p]+l-DUR[k])
    ES[k]=max(c); EF[k]=ES[k]+DUR[k]
TOTAL=max(EF.values())

# ---- recorrido hacia atras
LF={}; LS={}
for k in reversed(ORD):
    c=[TOTAL]
    for s,t,l in SUC[k]:
        if   t=="FS": c.append(LS[s]-l)
        elif t=="SS": c.append(LS[s]-l+DUR[k])
        elif t=="FF": c.append(LF[s]-l)
    LF[k]=min(c); LS[k]=LF[k]-DUR[k]

HT={k:LS[k]-ES[k] for k in ORD}
HL={}
for k in ORD:
    c=[TOTAL]
    for s,t,l in SUC[k]:
        if   t=="FS": c.append(ES[s]-l)
        elif t=="SS": c.append(ES[s]-l+DUR[k])
        elif t=="FF": c.append(EF[s]-l)
    HL[k]=min(c)-EF[k]
HI={k:HT[k]-HL[k] for k in ORD}
HIND={}
for k in ORD:
    mx=max([LF[p] for p,_,_ in PRE[k]], default=0)
    mn=min([ES[s] for s,_,_ in SUC[k]], default=TOTAL)
    HIND[k]=max(0, mn-mx-DUR[k])

if __name__=="__main__":
    print("DURACION DE LA RED:", TOTAL, "dias habiles")
    print("Fin:", dia(TOTAL-1), " (limite 2026-11-13 =", habiles(INICIO,dt.date(2026,11,13)),"d habiles)")
    print()
    print(f"{'C':<3}{'dur':>4}{'ES':>5}{'EF':>5}{'LS':>5}{'LF':>5}{'HT':>5}{'HL':>5}{'HI':>5}{'Hind':>6}  crit  inicio      fin")
    for k in ORD:
        cr="***" if HT[k]==0 else "   "
        print(f"{k:<3}{DUR[k]:>4}{ES[k]:>5}{EF[k]:>5}{LS[k]:>5}{LF[k]:>5}{HT[k]:>5}{HL[k]:>5}{HI[k]:>5}{HIND[k]:>6}  {cr}  {dia(ES[k])}  {dia(EF[k]-1)}")
    print()
    print("RUTA CRITICA:", " -> ".join(k for k in ORD if HT[k]==0))
    print("suma duraciones:", sum(DUR.values()))
