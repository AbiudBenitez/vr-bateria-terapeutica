# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import pmbok as PB
doc = Document('/tmp/_tarea_a.docx')

# ================================================================ 3
H(doc,"3. Desarrollo de los temas",1)

H(doc,"3.1 La estructura del método en dos dimensiones",2)
P(doc,"El PMBOK organiza la dirección de proyectos cruzando dos clasificaciones independientes. Entender que "
  "son independientes es la clave para leer el estándar: un mismo proceso pertenece a la vez a un grupo y a "
  "un área, igual que una casilla de una tabla pertenece a la vez a una fila y a una columna.")
table(doc,["Dimensión","Qué responde","Cuántas divisiones","Naturaleza"],[
 ("Grupos de procesos","¿Cuándo se hace el trabajo?","5","Responden al ciclo de vida. No son fases secuenciales rígidas: se traslapan y se repiten a lo largo del proyecto."),
 ("Áreas de conocimiento","¿Qué se gestiona?","10","Agrupan los procesos por especialidad. Cada una reúne los procesos que tratan un mismo asunto, sin importar el momento en que se ejecuten."),
],widths=[3.0,3.4,2.2,7.4],fs=10)
P(doc,"Del cruce de ambas dimensiones resultan los 49 procesos de la sexta edición. La matriz completa se "
  "presenta en la sección 3.6 y se representa gráficamente en la figura 3.")

H(doc,"3.2 El modelo de entradas, herramientas y salidas",2)
P(doc,"Cada uno de los 49 procesos se describe con la misma estructura de tres partes, conocida por sus "
  "siglas en inglés como modelo ITTO. Es el mecanismo que da coherencia a todo el estándar.")
table(doc,["Componente","Qué es","Ejemplo"],[
 ("Entradas","Los documentos, datos o resultados que el proceso necesita para poder ejecutarse. Provienen de procesos anteriores, del entorno de la organización o de fuentes externas.",
  "Para determinar el presupuesto hacen falta las estimaciones de costos y la estructura de desglose del trabajo."),
 ("Herramientas y técnicas","Los métodos que se aplican para transformar las entradas en salidas. Algunas son generales, como el juicio de expertos o las reuniones; otras son propias de un proceso.",
  "El método de la ruta crítica es una técnica exclusiva del proceso de desarrollar el cronograma."),
 ("Salidas","Los documentos o resultados que el proceso produce. Casi siempre se convierten en entrada de otro proceso.",
  "El acta de constitución es la salida del primer proceso y la entrada de casi todos los de planificación."),
],widths=[2.6,7.4,6.0],fs=10)
P(doc,"La consecuencia práctica de este modelo es que los procesos quedan encadenados: la salida de uno es "
  "la entrada del siguiente. Esa cadena es la que se ilustra en la figura 2 y la que hace que un error de "
  "planificación se propague hacia adelante.")

doc.add_page_break()
H(doc,"3.3 Entradas y salidas de cada grupo de procesos",2)
P(doc,"Esta es la tabla central de la actividad. Presenta, para cada uno de los cinco grupos, su propósito, "
  "las entradas que lo alimentan y las salidas que produce. Se describen las entradas y salidas "
  "características del grupo en su conjunto, no las de cada proceso individual, que sumarían varios "
  "centenares.")
rows=[]
for g in PB.GRUPOS:
    d = PB.GRUPO_IO[g]; n = len(PB.de_grupo(g))
    rows.append((g, f"{n}", d["proposito"],
                 "\n".join("· "+e for e in d["entradas"]),
                 "\n".join("· "+s for s in d["salidas"])))
table(doc,["Grupo de procesos","N.º","Propósito","Entradas características","Salidas características"],rows,
      widths=[2.4,0.8,3.6,4.6,4.6],fs=9)

H(doc,"3.4 Observaciones sobre cada grupo",2)
for g in PB.GRUPOS:
    d = PB.GRUPO_IO[g]; procs = PB.de_grupo(g)
    H(doc, f"{g} — {len(procs)} de 49 procesos", 3)
    P(doc, d["clave"])
    if len(procs) <= 12:
        table(doc,["N.º","Proceso","Área"],
              [(n, nom, dict(PB.AREAS)[a].replace("del Proyecto","").strip()) for n,nom,a,_ in procs],
              widths=[1.2,8.4,6.4],fs=9.5)
    else:
        P(doc,"Por tratarse del grupo más numeroso, sus 24 procesos se listan en la matriz de la sección "
          "3.6, junto con los del resto de los grupos.",italic=True)

doc.add_page_break()
H(doc,"3.5 Las diez áreas de conocimiento",2)
P(doc,"Cada área agrupa los procesos que tratan un mismo asunto. La tabla indica cuántos procesos contiene "
  "cada una y cuál es su salida más representativa.")
SALIDA_AREA = {
 "4":"Acta de constitución del proyecto y plan para la dirección del proyecto",
 "5":"Línea base del alcance, que incluye el enunciado del alcance y la estructura de desglose del trabajo",
 "6":"Línea base del cronograma y el diagrama de red del proyecto",
 "7":"Línea base de costos y requisitos de financiamiento del proyecto",
 "8":"Plan de gestión de la calidad, métricas de calidad e informes de calidad",
 "9":"Plan de gestión de los recursos, asignaciones del equipo y evaluaciones de desempeño",
 "10":"Plan de gestión de las comunicaciones y comunicaciones del proyecto",
 "11":"Plan de gestión de los riesgos, registro de riesgos e informe de riesgos",
 "12":"Estrategia de las adquisiciones, documentos de licitación y contratos",
 "13":"Registro de interesados y plan de involucramiento de los interesados",
}
table(doc,["N.º","Área de conocimiento","Procesos","Salida más representativa"],
 [(a, nom, str(len(PB.de_area(a))), SALIDA_AREA[a]) for a,nom in PB.AREAS] +
 [("","Total","49","")],
 widths=[1.0,5.2,1.4,8.4],fs=9.5)
P(doc,"La gestión de la integración es la única área con procesos en los cinco grupos, porque su función es "
  "precisamente unificar y coordinar lo que las demás producen. En el extremo opuesto, la gestión de la "
  "calidad, de las comunicaciones y de las adquisiciones tienen solo tres procesos cada una, uno por cada "
  "momento del ciclo: planificar, ejecutar y controlar.")

doc.add_page_break()
H(doc,"3.6 Matriz de los 49 procesos",2)
P(doc,"La matriz cruza las dos dimensiones y ubica cada uno de los 49 procesos. Se lee como una tabla de "
  "doble entrada: la fila indica de qué se ocupa el proceso y la columna, en qué momento del ciclo se "
  "ejecuta.")
M = PB.matriz()
rows=[]
for a,nom in PB.AREAS:
    fila=[a+". "+nom.replace(" del Proyecto","").replace("Gestión de la ","").replace("Gestión de los ","").replace("Gestión de las ","").replace("Gestión del ","").replace("Gestión ","")]
    for g in PB.GRUPOS:
        ps = M.get((a,g), [])
        fila.append("  ".join(ps) if ps else "—")
    fila.append(str(len(PB.de_area(a))))
    rows.append(tuple(fila))
rows.append(("Procesos por grupo",) + tuple(str(len(PB.de_grupo(g))) for g in PB.GRUPOS) + ("49",))
table(doc,["Área"]+[g.replace(" y ","\ny ") for g in PB.GRUPOS]+["Total"], rows,
      widths=[3.2,1.3,4.3,2.2,2.5,1.3,1.2],fs=9.5)
P(doc,"Las celdas contienen el número con que la guía identifica cada proceso. Los nombres completos "
  "aparecen en la sección 3.4, agrupados por grupo de procesos, y en la figura 3.",italic=True,size=10)

doc.add_page_break()
doc.save('/tmp/_tarea_b.docx'); print("B OK")
