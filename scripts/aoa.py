# -*- coding: utf-8 -*-
"""Red AOA del ejemplo de aceites esenciales (hierbabuena y menta)."""

DESC = {
"A":"Elaboración de un guión para la formulación del proyecto de producción de hierbabuena y menta y otro para el estudio de mercado de aceites esenciales",
"B":"Estudio de mercado de los aceites esenciales de hierbabuena y menta en México",
"C":"Formulación de dos proyectos agrícolas para la producción de hierbabuena y menta respectivamente",
"D":"Investigación bibliográfica sobre la industrialización de hierbabuena y menta",
"E":"Revisión y montaje de métodos analíticos para la caracterización de las materias primas",
"F":"Revisión y montaje de métodos analíticos para la caracterización de productos",
"G-1":"Adquisición de hierbabuena","G-2":"Adquisición de menta",
"H-1":"Caracterización de la hierbabuena","H-2":"Caracterización de la menta",
"I-1":"Preparación de la hierbabuena","I-2":"Preparación de la menta",
"J-1":"Pruebas de extracción en planta piloto de aceite de hierbabuena",
"J-2":"Pruebas de extracción en planta piloto de aceite de menta",
"K-1":"Análisis del extracto de hierbabuena","K-2":"Análisis del extracto de menta",
"L-1":"Purificación del extracto de hierbabuena","L-2":"Purificación del extracto de menta",
"M-1":"Estudio de aprovechamiento de residuos de la extracción de aceites de hierbabuena",
"M-2":"Estudio de aprovechamiento de residuos de la extracción de aceites de menta",
"N-1":"Pruebas de estabilidad del aceite purificado de hierbabuena",
"N-2":"Pruebas de estabilidad del aceite purificado de menta",
"O-1":"Evaluación de la calidad del aceite purificado de hierbabuena",
"O-2":"Evaluación de la calidad del aceite purificado de menta",
"P":"Pruebas organolépticas de los aceites","Q":"Análisis económico del proyecto","R":"Informe final",
}
ORD=["A","B","C","D","E","F","G-1","G-2","H-1","H-2","I-1","I-2","J-1","J-2",
     "K-1","K-2","L-1","L-2","M-1","M-2","N-1","N-2","O-1","O-2","P","Q","R"]
DUR={"A":5,"B":30,"C":60,"D":15,"E":10,"F":10,"G-1":5,"G-2":5,"H-1":10,"H-2":10,
     "I-1":5,"I-2":5,"J-1":10,"J-2":10,"K-1":10,"K-2":10,"L-1":5,"L-2":5,
     "M-1":30,"M-2":30,"N-1":90,"N-2":90,"O-1":5,"O-2":5,"P":5,"Q":5,"R":15}
EV={"A":(0,1),"B":(1,2),"C":(1,3),"D":(3,6),"E":(3,5),"F":(3,4),"G-2":(3,12),"G-1":(6,7),
    "H-1":(7,10),"I-1":(7,8),"J-1":(8,9),"K-1":(9,10),"L-1":(10,11),"M-1":(9,17),
    "N-1":(11,19),"O-1":(11,17),
    "H-2":(12,15),"I-2":(12,13),"J-2":(13,14),"K-2":(14,15),"L-2":(15,16),"M-2":(14,17),
    "N-2":(16,19),"O-2":(16,17),
    "P":(17,18),"Q":(18,19),"R":(19,20)}
FICT=[(2,3),(5,6),(4,6)]           # actividades ficticias, duracion 0
NEV=21

ARCOS=[(EV[k][0],EV[k][1],DUR[k],k) for k in ORD]+[(i,j,0,None) for i,j in FICT]

# ---- tiempos proximos de los eventos (recorrido hacia adelante)
TPI=[0]*NEV
for _ in range(NEV):
    for i,j,d,_k in ARCOS:
        if TPI[i]+d > TPI[j]: TPI[j]=TPI[i]+d
TOTAL=TPI[NEV-1]

# ---- tiempos remotos de los eventos (recorrido hacia atras)
TRT=[TOTAL]*NEV
for _ in range(NEV):
    for i,j,d,_k in ARCOS:
        if TRT[j]-d < TRT[i]: TRT[i]=TRT[j]-d

# ---- por actividad
A_TPI={k:TPI[EV[k][0]] for k in ORD}
A_TPT={k:A_TPI[k]+DUR[k] for k in ORD}
A_TRT={k:TRT[EV[k][1]] for k in ORD}
A_TRI={k:A_TRT[k]-DUR[k] for k in ORD}
HT={k:A_TRT[k]-A_TPI[k]-DUR[k] for k in ORD}
HL={k:TPI[EV[k][1]]-A_TPT[k] for k in ORD}
HI={k:HT[k]-HL[k] for k in ORD}
HIND={k:max(0, TPI[EV[k][1]]-TRT[EV[k][0]]-DUR[k]) for k in ORD}
CRIT=[k for k in ORD if HT[k]==0]

# antecedentes / consecuentes derivados de la red
ANT={k:[] for k in ORD}; CONS={k:[] for k in ORD}
def alcanza_desde(ev):
    """actividades reales que salen de ev, siguiendo ficticias hacia adelante"""
    out=[]; vis={ev}; pila=[ev]
    while pila:
        e=pila.pop()
        for i,j,d,kk in ARCOS:
            if i==e:
                if kk: out.append(kk)
                elif j not in vis: vis.add(j); pila.append(j)
    return out
def llega_a(ev):
    out=[]; vis={ev}; pila=[ev]
    while pila:
        e=pila.pop()
        for i,j,d,kk in ARCOS:
            if j==e:
                if kk: out.append(kk)
                elif i not in vis: vis.add(i); pila.append(i)
    return out
for k in ORD:
    ANT[k]=sorted(set(llega_a(EV[k][0])), key=ORD.index)
    CONS[k]=sorted(set(alcanza_desde(EV[k][1])), key=ORD.index)

if __name__=="__main__":
    print("DURACION TOTAL:", TOTAL, "dias")
    print("suma duraciones:", sum(DUR.values()))
    print()
    print("EVENTOS  TPI / TRT")
    for e in range(NEV): print(f"  {e:>2}: {TPI[e]:>4} / {TRT[e]:>4}  {'CRITICO' if TPI[e]==TRT[e] else ''}")
    print()
    print(f"{'C':<5}{'t':>4}{'TPI':>6}{'TPT':>6}{'TRI':>6}{'TRT':>6}{'HT':>6}{'HL':>6}{'HI':>6}{'Hind':>6}  crit")
    for k in ORD:
        print(f"{k:<5}{DUR[k]:>4}{A_TPI[k]:>6}{A_TPT[k]:>6}{A_TRI[k]:>6}{A_TRT[k]:>6}{HT[k]:>6}{HL[k]:>6}{HI[k]:>6}{HIND[k]:>6}  {'***' if HT[k]==0 else ''}")
    print()
    print("RUTA CRITICA:", " -> ".join(CRIT))
    print("suma ruta critica:", sum(DUR[k] for k in CRIT))
