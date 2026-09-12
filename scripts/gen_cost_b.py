# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import rc257 as R, costos as K
M = R.V2
def d(x): return f"${x:,.0f}"
def d2(x): return f"${x:,.2f}"
f = R.fnum
doc = Document('/tmp/_cost_a.docx')

# ================================================================ 5
H(doc,"5. Asignación de perfil a cada grupo de actividades",1)
P(doc,"La estimación ascendente exige asignar a cada actividad el recurso que efectivamente la ejecuta. Se "
  "asignó por grupo de claves y no por área, porque dentro de un área conviven trabajos de perfiles "
  "distintos. El caso más claro es el área de QA, documentación y gestión, que reúne planificación del "
  "proyecto, pruebas y redacción de manuales: cobrar las tres al mismo precio distorsionaría el resultado.")
rows=[]
for s in "DJEMSIAQ":
    gs = sorted({g for (sig,g) in K.POR_GRUPO if sig==s})
    for n,g in enumerate(gs):
        cnt,h,c = K.POR_GRUPO[(s,g)]
        rows.append((s if n==0 else "", g, K.perfil(g+".1") if (g+".1") in R.T else K.GRUPO[g],
                     d2(K.PERFIL[K.GRUPO[g]][0]), cnt, f"{h:,.0f}", d(c)))
table(doc,["Á.","Grupo","Perfil asignado","$/hora","Tareas","Horas","Costo"],rows,
      widths=[0.8,1.3,4.6,1.7,1.4,1.5,2.3],fs=7.5)
P(doc,"Son 68 grupos. La asignación completa por actividad individual está en el anexo A.")

# ================================================================ 6
H(doc,"6. Agregación ascendente del costo",1)
P(doc,"El costo sube por tres niveles: de la actividad al grupo de claves, del grupo al área y del área al "
  "proyecto. Cada nivel es una cuenta de control sobre la que se mide el desempeño.")
H(doc,"6.1 Por área de trabajo",2)
rows=[]
for a in sorted(R.AREAS, key=lambda x:-K.POR_AREA[x][2]):
    n,h,c = K.POR_AREA[a]
    rows.append((R.SIGLA[a], a, R.RESP[a], n, f"{h:,.0f}", d(c), f"{100*c/K.MANO_OBRA:.1f} %"))
rows.append(("","Total de mano de obra","", sum(K.POR_AREA[a][0] for a in R.AREAS),
             f"{K.HORAS_TOT:,.0f}", d(K.MANO_OBRA), "100.0 %"))
table(doc,["Á.","Área","Responsable","Tareas","Horas","Costo","%"],rows,
      widths=[0.8,4.4,2.6,1.4,1.6,2.4,1.4],fs=9.5)
P(doc,"El área de QA, documentación y gestión concentra la cuarta parte del costo de mano de obra. No es "
  "un error de estimación: reúne 60 de las 257 actividades y, además de las pruebas, absorbe la "
  "planificación, el seguimiento y toda la documentación del proyecto, porque la organización del equipo no "
  "asignó a nadie los roles de dirección, gerencia y coordinación.")

H(doc,"6.2 Por perfil profesional",2)
rows=[]
for p in sorted(K.POR_PERFIL, key=lambda x:-K.POR_PERFIL[x][2]):
    n,h,c = K.POR_PERFIL[p]
    rows.append((p, d2(K.PERFIL[p][0]), n, f"{h:,.0f}", d(c), f"{100*c/K.MANO_OBRA:.1f} %"))
table(doc,["Perfil","$/hora","Tareas","Horas","Costo","%"],rows,
      widths=[5.6,1.8,1.6,1.8,2.4,1.4],fs=9.5)

H(doc,"6.3 Distribución del costo",2)
from docx.shared import Cm
FIG="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/figuras_costos/"
if os.path.exists(FIG+"Fig3_Distribucion_costo.png"):
    doc.add_picture(FIG+"Fig3_Distribucion_costo.png", width=Cm(16.4)); doc.paragraphs[-1].alignment=C
caption(doc,"Fig. 3 — Distribución del costo de mano de obra por área y por perfil profesional.")

# ================================================================ 7
H(doc,"7. Costos no laborales",1)
P(doc,"Además de la mano de obra, el proyecto requiere equipo, licencias y gastos de operación.")
H(doc,"7.1 Recursos proporcionados por la Facultad",2)
P(doc,"Los visores de realidad virtual y el espacio para las sesiones de prueba los proporciona la Facultad "
  "en calidad de préstamo. Conforme a la guía PMBOK, los recursos que aporta la organización ejecutante no "
  "se cargan al presupuesto del proyecto, pero deben quedar registrados: su valor es real y su "
  "disponibilidad es un supuesto del que depende el proyecto.")
table(doc,["Recurso","Descripción","Valor de referencia","Condición"],
 [(n,des,d(v) if v else "No aplica",cond) for n,des,v,cond in K.PROPORCIONADOS] +
 [("Valor total proporcionado","","",d(K.VALOR_PROPORCIONADO))],
 widths=[4.0,6.4,2.8,2.8],fs=9.5)
P(doc,"Este supuesto genera el riesgo R5 del registro de la sección 11. Si el préstamo no se concreta, el "
  f"proyecto debe absorber {d(K.VALOR_PROPORCIONADO)} adicionales o rentar el equipo.")

H(doc,"7.2 Costos que sí desembolsa el proyecto",2)
rows=[]
cat_ant=None
for cat,nom,det,c in K.NO_LABORAL:
    rows.append((cat if cat!=cat_ant else "", nom, det, d(c) if c else "Sin costo"))
    cat_ant=cat
rows.append(("","Total de costos no laborales","",d(K.NO_LAB_TOT)))
table(doc,["Categoría","Concepto","Detalle","Costo"],rows,widths=[2.0,4.2,7.4,2.4],fs=9)
P(doc,"Dos partidas quedaron en cero respecto de la estimación preliminar. Los recursos gráficos y la "
  "librería de muestras de audio se sustituyen por bancos con licencia libre, del tipo CC0, que cubren las "
  "necesidades del proyecto. Las licencias musicales no se sustituyen: la oferta de música libre con la "
  "estructura rítmica que exige el juego de ritmo es insuficiente, y usar pistas de licencia dudosa "
  "generaría un riesgo mayor que el ahorro. El software de gestión del proyecto tampoco representa costo, "
  "conforme al análisis de herramientas que acompaña a este documento.")

doc.add_page_break()
doc.save('/tmp/_cost_b.docx'); print("B OK")
