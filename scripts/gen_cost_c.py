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
doc = Document('/tmp/_cost_b.docx')

# ================================================================ 8
H(doc,"8. Determinar el presupuesto",1)
P(doc,"Este proceso suma los costos estimados para establecer la línea base de costos autorizada. La guía "
  "PMBOK distingue con precisión entre cuatro niveles, y la distinción importa porque cada uno lo autoriza "
  "una figura distinta.")
table(doc,["Nivel","Qué incluye","Quién dispone de él"],[
 ("Costos directos","Mano de obra más costos no laborales. Es la suma de las estimaciones de las 257 actividades y de las partidas de equipo, licencias y operación.","El gerente del proyecto, dentro de cada cuenta de control."),
 ("Línea base de costos","Costos directos más la reserva de contingencia.","El gerente del proyecto. La reserva se aplica ante riesgos identificados que se materialicen."),
 ("Presupuesto total","Línea base más la reserva de gestión.","La patrocinadora. La reserva de gestión cubre trabajo imprevisto no identificado y su uso requiere autorización expresa."),
],widths=[3.2,8.8,4.0],fs=9.5)

H(doc,"8.1 Integración del presupuesto",2)
table(doc,["Concepto","Monto","% del total"],[
 ("Mano de obra", d(K.MANO_OBRA), f"{100*K.MANO_OBRA/K.PRESUPUESTO:.1f} %"),
 ("Costos no laborales", d(K.NO_LAB_TOT), f"{100*K.NO_LAB_TOT/K.PRESUPUESTO:.1f} %"),
 ("Costos directos", d(K.DIRECTOS), f"{100*K.DIRECTOS/K.PRESUPUESTO:.1f} %"),
 ("Reserva de contingencia", d(K.CONTINGENCIA), f"{100*K.CONTINGENCIA/K.PRESUPUESTO:.1f} %"),
 ("Línea base de costos", d(K.LINEA_BASE), f"{100*K.LINEA_BASE/K.PRESUPUESTO:.1f} %"),
 ("Reserva de gestión", d(K.GESTION), f"{100*K.GESTION/K.PRESUPUESTO:.1f} %"),
 ("Presupuesto total del proyecto", d(K.PRESUPUESTO), "100.0 %"),
],widths=[8.0,4.0,4.0],fs=10)
P(doc,"La reserva de contingencia no es un porcentaje arbitrario: se obtiene del valor monetario esperado "
  "de los riesgos identificados, según el cálculo de la sección 11. La reserva de gestión sí se fija como "
  "porcentaje, el 5 % de la línea base, que es el valor habitual para proyectos de esta duración.")

H(doc,"8.2 Curva S",2)
P(doc,"La curva S muestra cómo se acumula el costo a lo largo del proyecto. Es la referencia contra la que "
  "se compara el gasto real durante la ejecución.")
if os.path.exists(FIG+"Fig1_Curva_S.png"):
    doc.add_picture(FIG+"Fig1_Curva_S.png", width=Cm(16.4)); doc.paragraphs[-1].alignment=C
caption(doc,"Fig. 1 — Curva S del presupuesto.")
P(doc,"La curva es marcadamente frontal: cerca del 60 % del costo se acumula en la primera mitad del "
  "proyecto. La razón está en la red de precedencias: las ocho áreas arrancan simultáneamente el primer día "
  "y el trabajo se concentra en las primeras cuatro semanas, mientras que la última parte del proyecto "
  "corresponde casi por completo al área de QA. Tiene una consecuencia práctica: el desembolso se necesita "
  "temprano, no de forma uniforme.")

# ================================================================ 9
H(doc,"9. Escenarios de sensibilidad",1)
P(doc,"El presupuesto de la sección anterior valora el trabajo del equipo a tarifas de profesionista "
  "titulado. Es una decisión metodológica que conviene explicitar, porque existen otras dos formas "
  "legítimas de costear un proyecto académico, y la diferencia entre ellas es grande.")
rows=[]
for nom,t,just in K.ESCENARIOS:
    mo,dir_,lb,pt = K.escenario(t)
    rows.append((nom, d(mo), d(dir_), d(pt), just))
table(doc,["Escenario","Mano de obra","Costos directos","Presupuesto","Fundamento"],rows,
      widths=[3.4,2.2,2.2,2.2,6.0],fs=9)
P(doc,"El escenario C es la línea base de este documento. Responde a la pregunta «cuánto costaría que una "
  "empresa ejecutara este proyecto con personal calificado», que es la que da sentido a un ejercicio de "
  "administración de proyectos.")
P(doc,"El escenario A responde a «cuánto dinero sale efectivamente del bolsillo del equipo», y es la cifra "
  "real de un proyecto escolar: el trabajo se cursa por créditos y no se remunera. Se documenta porque es "
  "la única cifra que el equipo desembolsará de verdad.")
P(doc,"El escenario B es intermedio y corresponde a lo que una empresa pagaría a este equipo por su nivel "
  "de experiencia. Su cercanía con el escenario C, una diferencia del 22 %, indica que la estimación "
  "principal no está inflada.")

# ================================================================ 10
H(doc,"10. Tabla de simultaneidad",1)
P(doc,"La tabla indica qué trabajo puede ejecutarse al mismo tiempo. Se deriva directamente de la red de "
  "precedencias: dos actividades pueden ser simultáneas cuando sus intervalos entre tiempo próximo de "
  "iniciación y de terminación se traslapan y ninguna depende de la otra.")
rows=[]
for a,b in CP.TRAMOS:
    act = CP.activas(a,b)
    tot = sum(len(v) for v in act.values())
    det = " · ".join(f"{s}: {len(v)}" for s,v in sorted(act.items()))
    rows.append((f"{a:.0f} – {b:.0f}", len(act), tot, det))
table(doc,["Días","Áreas activas","Tareas en curso","Detalle por área"],rows,
      widths=[2.0,2.2,2.4,9.4],fs=9.5)
P(doc,"Las claves de área son D desarrollo VR, J juego de ritmo, E experiencia emocional, M música, "
  "S sonido, I interfaz, A entorno tridimensional y Q aseguramiento de calidad.",italic=True)
P(doc,"El proyecto alcanza su máximo paralelismo en los primeros diez días hábiles, con las ocho áreas "
  "activas a la vez y hasta 77 tareas en curso. A partir del día 35 solo queda activa el área de QA, lo que "
  "explica tanto la forma de la curva S como la sobrecarga de esa área.")

H(doc,"10.1 Implicación para la asignación de recursos",2)
P(doc,"La simultaneidad de las primeras semanas no representa un problema mientras cada área tenga una "
  "persona dedicada, porque las tareas simultáneas pertenecen a áreas distintas. El problema aparece "
  "dentro de cada área: la carga individual excede la ventana disponible en siete de las ocho, según el "
  "análisis del documento de ruta crítica.")

doc.add_page_break()
doc.save('/tmp/_cost_c.docx'); print("C OK")
