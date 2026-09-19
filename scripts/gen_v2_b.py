# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
from docx.shared import Cm
import rc257 as R
M, O = R.V2, R.ORIG
f = R.fnum
FIG = "/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/figuras-ruta-critica/"
doc = Document('/tmp/_v2_a.docx')

# ================================================================ 4
H(doc,"4. Matriz de secuencias",1)
P(doc,"La matriz de secuencias registra, para cada actividad, cuáles deben terminar antes de que ella pueda "
  "iniciar y cuáles pueden iniciar después de que ella termine. Se presenta en ambas formas porque juntas "
  "permiten verificarse mutuamente: si una actividad aparece como antecedente de otra, esa otra debe "
  "aparecer entre sus consecuentes.")
P(doc,"Las 38 actividades marcadas con asterisco son las modificadas por el documento de cambios. Sus "
  "antecedentes incluyen tanto los originales como los agregados.")
rows=[]
for k in R.ORD:
    ant = ", ".join(M["pre"][k]) or "—"
    con = ", ".join(sorted(M["suc"].get(k, []))) or "— (actividad final)"
    rows.append(((k+"  *") if k in R.CAMBIOS else k, R.T[k]["sig"], ant, con))
table(doc,["Clave","Área","Antecedentes","Consecuentes"],rows,widths=[1.6,1.0,5.6,7.8],fs=7.5)

doc.add_page_break()
# ================================================================ 5
H(doc,"5. Matriz de información",1)
P(doc,"La matriz de información consolida en un solo cuadro la lista de actividades, sus áreas, sus "
  "responsables, sus duraciones y sus secuencias. Es el insumo directo para construir la red.")
rows=[(k, R.T[k]["desc"], R.T[k]["sig"], R.T[k]["resp"], f(R.T[k]["dur"]),
       ", ".join(M["pre"][k]) or "—") for k in R.ORD]
table(doc,["Clave","Descripción","Á.","Responsable","Días","Antecedentes"],rows,
      widths=[1.4,7.0,0.8,2.0,0.9,3.9],fs=7)

doc.add_page_break()
# ================================================================ 6
H(doc,"6. Verificación de la consistencia de la red",1)
P(doc,"Antes de calcular tiempos se comprobaron las condiciones que debe cumplir toda red de actividades. "
  "En la versión 1.0 del análisis dos de ellas no se cumplían. Con los cambios aplicados, las cinco se "
  "cumplen.")
table(doc,["Condición","Versión 1.0","Versión 2.0"],[
 ("La red no contiene ciclos: ninguna actividad depende indirectamente de sí misma.",
  "Se cumple.","Se cumple."),
 ("Toda dependencia declarada apunta a una clave existente.",
  "Se cumple.","Se cumple, incluidas las 93 dependencias añadidas."),
 ("Las actividades sin antecedente son las que pueden arrancar el primer día.",
  f"{len(R.SIN_PRE)} actividades.", f"{len(R.SIN_PRE)} actividades, sin cambio. Corresponden al arranque simultáneo de las ocho áreas."),
 ("Solo la actividad final carece de consecuentes.",
  f"No se cumple. {len(R.TERMINALES_V1)} actividades sin consecuente.",
  f"Se cumple. Queda {len(R.TERMINALES)}: QX, la presentación final."),
 ("Toda actividad contribuye, directa o indirectamente, al entregable final.",
  "No se cumple. Solo 91 de 257 actividades alcanzaban QX.",
  "Se cumple. Las 257 alcanzan QX."),
],widths=[6.2,4.6,5.2],fs=9)
P(doc,"Las actividades sin antecedente son " + ", ".join(R.SIN_PRE) + ". Todas corresponden al inicio de "
  "alguna de las ocho áreas y pueden ejecutarse simultáneamente el primer día del proyecto.")
P(doc,"La red ahora está bien formada. Esto es lo que permite tomar la duración calculada como una "
  "estimación y no solo como una cota inferior, que era la limitación de la versión anterior.")

# ================================================================ 7
H(doc,"7. Cálculo de tiempos próximos",1)
P(doc,"El recorrido hacia adelante calcula, para cada actividad, lo más pronto que puede iniciar y terminar. "
  "Se parte del día cero y se avanza siguiendo el ordenamiento de la red.")
H(doc,"7.1 Reglas de cálculo",2)
table(doc,["Magnitud","Regla"],[
 ("Tiempo próximo de iniciación (TPI)","El mayor de los tiempos próximos de terminación de sus antecedentes. Cero si no tiene antecedentes."),
 ("Tiempo próximo de terminación (TPT)","El tiempo próximo de iniciación más la duración."),
 ("Duración del proyecto","El mayor tiempo próximo de terminación de toda la red."),
],widths=[5.4,10.6],fs=9.5)
P(doc,"Se toma el mayor de los antecedentes porque la actividad no puede comenzar mientras alguno de ellos "
  "siga en curso. Es precisamente este «mayor» el que hace crecer la duración al agregar dependencias: una "
  "actividad que antes esperaba a tres predecesoras ahora espera a diecisiete, y basta con que una de ellas "
  "termine tarde para desplazarla.")
H(doc,"7.2 Resultado",2)
P(doc,f"El mayor tiempo próximo de terminación de la red es {M['TOTAL']:.2f}, correspondiente a la actividad "
  "QX, «Preparar presentación y demostración final del proyecto». La duración de la ruta crítica del proyecto "
  f"es por tanto de {M['TOTAL']:.2f} días hábiles, frente a los {O['TOTAL']:.2f} de la versión anterior.")
P(doc,"Los valores por actividad se presentan en la matriz de elasticidad de la sección 10, junto con los "
  "tiempos remotos y las holguras, para no repetir el mismo cuadro dos veces.")

# ================================================================ 8
H(doc,"8. Cálculo de tiempos remotos",1)
P(doc,"El recorrido hacia atrás calcula, para cada actividad, lo más tarde que puede iniciar y terminar sin "
  "desplazar la fecha final. Se parte del último día y se retrocede.")
table(doc,["Magnitud","Regla"],[
 ("Tiempo remoto de terminación (TRT)","El menor de los tiempos remotos de iniciación de sus consecuentes. Si no tiene consecuentes, la duración del proyecto."),
 ("Tiempo remoto de iniciación (TRI)","El tiempo remoto de terminación menos la duración."),
],widths=[5.4,10.6],fs=9.5)
P(doc,"Se toma el menor de los consecuentes porque la actividad debe estar terminada a tiempo para la más "
  "exigente de las que dependen de ella.")
P(doc,"En la versión 1.0 este recorrido estaba distorsionado: las noventa actividades sin consecuentes "
  "recibían automáticamente como tiempo remoto de terminación la duración del proyecto, lo que les asignaba "
  "toda la holgura disponible y las excluía de cualquier trayectoria crítica. Con la red cerrada, cada "
  "actividad recibe el tiempo remoto que le corresponde por sus verdaderas sucesoras, y las holguras "
  "calculadas son ahora significativas.")

doc.save('/tmp/_v2_b.docx'); print("B OK")
