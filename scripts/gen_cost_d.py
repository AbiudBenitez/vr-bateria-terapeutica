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
doc = Document('/tmp/_cost_c.docx')

# ================================================================ 11
H(doc,"11. Compresión de la red",1)
P(doc,"La compresión es la etapa del método de la ruta crítica que responde a una pregunta económica: si "
  "hiciera falta terminar antes, ¿cuánto costaría cada día ganado y qué actividades conviene acelerar? "
  "Solo tiene sentido comprimir actividades de la ruta crítica: acelerar una actividad con holgura no "
  "adelanta la fecha final y sí cuesta dinero.")

H(doc,"11.1 Modelo de compresión adoptado",2)
P(doc,"Cada área del proyecto tiene una sola persona asignada, de modo que no es posible comprimir "
  "añadiendo un segundo recurso: no hay a quién añadir sin quitarlo de otra área. La única vía disponible "
  "es extender la jornada.")
table(doc,["Parámetro","Valor","Fundamento"],[
 ("Jornada normal","8 horas diarias","Es la base sobre la que se estimaron todas las duraciones."),
 ("Jornada extendida","10 horas diarias","Dos horas de tiempo extraordinario, que es el máximo que la Ley Federal del Trabajo permite de forma habitual sin recargo doble."),
 ("Reducción máxima de la duración","20 %","Una actividad de diez días ejecutada a diez horas diarias termina en ocho."),
 ("Sobreprecio de la hora extra","50 % sobre la tarifa ordinaria","Corresponde al pago de tiempo extraordinario simple: hora doble, es decir la ordinaria más una vez más, aplicada solo a la fracción extra."),
],widths=[4.0,3.4,8.6],fs=9.5)

H(doc,"11.2 Pendiente de costo por actividad",2)
P(doc,"La pendiente de costo es el sobrecosto dividido entre los días que se ganan. Indica cuánto cuesta "
  "cada día de adelanto en esa actividad.")
rows=[]
for k in CP.CANDIDATAS[:22]:
    rows.append((k, R.T[k]["desc"][:44], f(R.T[k]["dur"]), f"{CP.comprimible(k):.2f}",
                 d(K.costo(k)), d(CP.sobrecosto(k)), d(CP.pendiente(k)), K.perfil(k)[:26]))
table(doc,["Clave","Actividad","Dur.","Recorte","Costo normal","Sobrecosto","$/día","Perfil"],rows,
      widths=[1.3,5.0,1.0,1.3,1.8,1.6,1.4,2.6],fs=8)
P(doc,"Se muestran las 22 actividades críticas más baratas de comprimir, de un total de "
  f"{len(CP.CANDIDATAS)}. La tabla completa está en el anexo B.")
P(doc,"Obsérvese que la pendiente es idéntica dentro de cada perfil: 401 pesos por día en las actividades "
  "de QA, 450 en las de análisis, 520 en las del entorno tridimensional. No es casualidad. Bajo el modelo "
  "de tiempo extraordinario, la pendiente resulta ser exactamente cuatro veces la tarifa horaria del "
  "perfil, con independencia de cuánto dure la actividad. La conclusión práctica es directa: conviene "
  "comprimir primero el trabajo de los perfiles más baratos que estén sobre la ruta crítica.")

H(doc,"11.3 Curva de compresión",2)
P(doc,"Comprimir una actividad crítica acorta el proyecto solo hasta que otra trayectoria se vuelve "
  "crítica. A partir de ahí hay que comprimir dos trayectorias a la vez, y el costo por día ganado sube. "
  "La curva se construyó aplicando el procedimiento de forma iterativa: en cada paso se comprime la "
  "actividad crítica más barata que efectivamente reduzca la duración, y se vuelve a calcular la red.")
if os.path.exists(FIG+"Fig2_Curva_compresion.png"):
    doc.add_picture(FIG+"Fig2_Curva_compresion.png", width=Cm(16.4)); doc.paragraphs[-1].alignment=C
caption(doc,"Fig. 2 — Curva de compresión tiempo-costo. Cada escalón corresponde a una actividad comprimida.")
pts,_ = CP.curva()
table(doc,["Punto","Duración","Sobrecosto acumulado","Costo por día ganado"],[
 ("Duración normal", f"{pts[0][0]:.2f} días", "Sin sobrecosto", "—"),
 ("Primeros días ganados", f"{pts[5][0]:.2f} días", d(pts[5][1]), d(pts[5][1]/(pts[0][0]-pts[5][0]))),
 ("Mitad de la compresión", f"{pts[len(pts)//2][0]:.2f} días", d(pts[len(pts)//2][1]),
  d(pts[len(pts)//2][1]/(pts[0][0]-pts[len(pts)//2][0]))),
 ("Compresión máxima", f"{pts[-1][0]:.2f} días", d(pts[-1][1]), d(pts[-1][1]/(pts[0][0]-pts[-1][0]))),
],widths=[4.4,3.0,4.2,4.4],fs=9.5)
P(doc,f"El proyecto puede reducirse de {pts[0][0]:.2f} a {pts[-1][0]:.2f} días hábiles, es decir "
  f"{pts[0][0]-pts[-1][0]:.2f} días, con un sobrecosto de {d(pts[-1][1])}. El costo marginal arranca en "
  "401 pesos por día y llega a superar los 2,500 en los últimos tramos.")

H(doc,"11.4 Conclusión sobre la compresión",2)
P(doc,"El proyecto no necesita comprimirse para cumplir el calendario: la ruta crítica mide 38.25 días "
  "hábiles y hay 47 disponibles hasta el 13 de noviembre. La compresión es, por tanto, un instrumento de "
  "contingencia y no una necesidad del plan.")
P(doc,f"Su utilidad práctica es que {d(pts[-1][1])}, un 1.5 % del presupuesto, compran hasta "
  f"{pts[0][0]-pts[-1][0]:.2f} días hábiles de margen. Es una relación favorable, y conviene tenerla "
  "documentada por si alguno de los riesgos de la sección siguiente llegara a materializarse.")
P(doc,"Hay que advertir su límite: la compresión resuelve problemas de la ruta crítica, no de carga de "
  "trabajo. La restricción dominante del proyecto es que el área de QA tiene 511 horas asignadas y su "
  "ventana solo permite unas 362. Comprimir la ruta crítica no corrige eso; redistribuir trabajo, sí.")

doc.add_page_break()
doc.save('/tmp/_cost_d.docx'); print("D OK")
