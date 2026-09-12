# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
from docx.shared import Cm
import rc257 as R, costos as K, compresion as CP
M = R.V2
def d(x): return f"${x:,.0f}"
f = R.fnum
FIG="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/figuras_costos/"
doc = Document('/tmp/_cost_d.docx')

# ================================================================ 12
H(doc,"12. Análisis del costo de la calidad",1)
P(doc,"El costo de la calidad reúne todo el esfuerzo dedicado a que el producto cumpla sus requisitos, más "
  "el que se gasta cuando no los cumple. La guía PMBOK lo divide en costos de conformidad, que se invierten "
  "para evitar fallos, y costos de no conformidad, que se pagan cuando el fallo ya ocurrió.")
table(doc,["Categoría","Tipo","Qué comprende en este proyecto"],[
 ("Prevención","Conformidad","Planificación y gestión del proyecto, gestión de riesgos, definición de requisitos y trazabilidad, y registro del avance. Es el trabajo que evita que los defectos lleguen a existir."),
 ("Evaluación","Conformidad","Planes y ejecución de pruebas, y validación integral con métricas. Es el trabajo de comprobar que el producto cumple."),
 ("Fallos internos","No conformidad","Gestión y corrección de errores, correcciones de la batería, de la interfaz y de la ambientación. Son defectos detectados antes de la entrega."),
 ("Fallos externos","No conformidad","No aplica. El proyecto entrega un prototipo académico que no llega a usuarios finales fuera del entorno de prueba."),
],widths=[2.6,2.4,11.0],fs=9.5)

rows=[]
for cat,gs in K.COQ.items():
    for n,g in enumerate(gs):
        rows.append((cat if n==0 else "", g, K.GRUPO[g][:28], d(K.costo_grupo(g))))
    rows.append(("", f"Subtotal {cat.lower()}", "", d(K.COQ_TOT[cat])))
rows.append(("Total del costo de la calidad","","",d(sum(K.COQ_TOT.values()))))
table(doc,["Categoría","Grupo","Perfil","Costo"],rows,widths=[3.4,1.8,6.4,2.8],fs=9)

table(doc,["Categoría","Costo","% de la mano de obra","% del costo de la calidad"],
 [(c, d(v), f"{100*v/K.MANO_OBRA:.1f} %", f"{100*v/sum(K.COQ_TOT.values()):.1f} %") for c,v in K.COQ_TOT.items()]+
 [("Total", d(sum(K.COQ_TOT.values())), f"{100*sum(K.COQ_TOT.values())/K.MANO_OBRA:.1f} %","100.0 %")],
 widths=[4.4,3.2,4.2,4.2],fs=10)

H(doc,"12.1 Lectura del resultado",2)
P(doc,f"El costo de la calidad representa el {100*sum(K.COQ_TOT.values())/K.MANO_OBRA:.1f} % de la mano de "
  "obra. Es una proporción alta comparada con la referencia habitual de la industria del software, que "
  "ronda el 15 %, y tiene una explicación concreta: el proyecto es un trabajo académico cuya documentación "
  "es en sí misma un entregable evaluable, de modo que el esfuerzo de prevención incluye tareas que en un "
  "proyecto comercial no existirían.")
P(doc,"La proporción entre categorías sí es sana. Se invierte más en prevención que en corregir fallos, "
  f"{d(K.COQ_TOT['Prevención'])} contra {d(K.COQ_TOT['Fallos internos'])}, que es la relación que se busca: "
  "cuesta menos evitar un defecto que repararlo. Si la relación fuera la inversa, indicaría que el proyecto "
  "está descubriendo los problemas demasiado tarde.")
P(doc,"La ausencia de costos por fallos externos no debe leerse como una virtud del proyecto, sino como una "
  "consecuencia de su alcance: el prototipo no se entrega a usuarios finales fuera del entorno controlado "
  "de prueba, de modo que no hay oportunidad de que un defecto llegue al cliente.")

# ================================================================ 13
H(doc,"13. Análisis de riesgos",1)
P(doc,"Esta sección identifica los riesgos del proyecto, los evalúa de forma cualitativa y cuantitativa, y "
  "obtiene de ahí la reserva de contingencia que aparece en el presupuesto. El tratamiento de cada riesgo, "
  "con su estrategia de respuesta, responsable y plan de contingencia, se desarrolla en el Plan de Gestión "
  "de los Riesgos.")

H(doc,"13.1 Escalas de valoración",2)
P(doc,"Para que el análisis cualitativo sea reproducible, la probabilidad y el impacto se valoran en "
  "escalas definidas de antemano.")
table(doc,["Nivel","Probabilidad","Impacto sobre el costo","Impacto sobre el cronograma"],[
 ("Muy bajo","10 %","Hasta $4,000","Menos de un día hábil"),
 ("Bajo","30 %","Hasta $8,000","De uno a dos días hábiles"),
 ("Medio","50 %","Hasta $14,000","De tres a cinco días hábiles"),
 ("Alto","70 %","Hasta $20,000","De seis a diez días hábiles"),
 ("Muy alto","90 %","Más de $20,000","Más de diez días hábiles, o compromete la fecha de entrega"),
],widths=[2.2,2.4,4.0,7.4],fs=9.5)

H(doc,"13.2 Registro de riesgos y análisis cuantitativo",2)
P(doc,"El valor monetario esperado de cada riesgo es el producto de su probabilidad por su impacto. La suma "
  "de todos ellos determina la reserva de contingencia.")
rows=[(r[0], r[1], r[4], f"{r[2]:.0%}", d(r[3]), d(r[2]*r[3])) for r in K.RIESGOS]
rows.append(("","Valor monetario esperado total","","","",d(K.EMV)))
rows.append(("","Reserva de contingencia adoptada, redondeada","","","",d(K.CONTINGENCIA)))
table(doc,["Id","Riesgo","Categoría","Prob.","Impacto","Valor esperado"],rows,
      widths=[0.9,7.0,2.0,1.3,2.0,2.8],fs=9)

H(doc,"13.3 Matriz de probabilidad e impacto",2)
if os.path.exists(FIG+"Fig4_Matriz_riesgos.png"):
    doc.add_picture(FIG+"Fig4_Matriz_riesgos.png", width=Cm(14.6)); doc.paragraphs[-1].alignment=C
caption(doc,"Fig. 4 — Matriz de probabilidad e impacto de los nueve riesgos identificados.")

H(doc,"13.4 Lectura del análisis",2)
P(doc,f"El valor monetario esperado de los riesgos identificados asciende a {d(K.EMV)}, equivalente al "
  f"{100*K.EMV/K.DIRECTOS:.1f} % de los costos directos. La reserva de contingencia se fija en ese valor, "
  "redondeado a la centena.")
P(doc,"Conviene señalar que este método asigna reserva en proporción al riesgo real y no mediante un "
  "porcentaje fijo. Un 10 % de los costos directos, que es la práctica habitual por defecto, habría "
  f"arrojado {d(K.DIRECTOS*0.10)}, una cifra distinta y sin sustento.")
P(doc,"Los tres riesgos de mayor valor esperado son el retraso de la cadena del entorno tridimensional, la "
  "sobrecarga del área de QA y el incumplimiento del umbral de latencia. Los dos primeros son de recursos y "
  "cronograma, y se atienden redistribuyendo trabajo; el tercero es técnico y se atiende con el hito de "
  "verificación temprana previsto en la planificación.")
P(doc,"El riesgo R5, que la Facultad no concrete el préstamo de los visores, merece atención particular "
  f"porque su impacto de {d(18998)} equivale al 80 % de todos los costos no laborales del proyecto. Es la "
  "contrapartida de haber excluido el equipo del presupuesto: el ahorro es real, pero traslada una "
  "dependencia externa al proyecto.")

doc.add_page_break()
doc.save('/tmp/_cost_e.docx'); print("E OK")
