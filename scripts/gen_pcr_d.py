# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
from docx.shared import Cm
from collections import Counter
import rc257 as R, costos as K, pruebas as PR, compresion as CP
doc = Document('/tmp/_pcr_c.docx')
FIG="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/figuras-costos/"

# ======================================================= PARTE IV
H(doc,"PARTE IV. PLAN DE GESTIÓN DE LOS RIESGOS",1)

H(doc,"18. Metodología",2)
table(doc,["Proceso","Cómo se aplica en este proyecto"],[
 ("Planificar la gestión de los riesgos","Esta parte del documento. Define escalas, categorías, roles, periodicidad y umbrales."),
 ("Identificar los riesgos","Sesión inicial con todo el equipo, más revisión en cada reunión semanal. Técnicas: tormenta de ideas, análisis de supuestos y revisión de la red de precedencias en busca de puntos de convergencia."),
 ("Análisis cualitativo","Valoración de probabilidad e impacto en escalas de cinco niveles y ubicación en la matriz."),
 ("Análisis cuantitativo","Valor esperado en días hábiles, cuyo total dimensiona la reserva de cronograma."),
 ("Planificar la respuesta","Estrategia, responsable, disparador y plan de contingencia por cada riesgo."),
 ("Implementar la respuesta","Regla de activación y registro de ejecución, en la sección 23."),
 ("Monitorear los riesgos","Revisión semanal del registro, cierre de riesgos superados e indicadores, en la sección 24."),
],widths=[4.4,11.6],fs=9.5)

H(doc,"18.1 Por qué el impacto se mide en días",3)
P(doc,"En la mayoría de los proyectos el impacto de un riesgo se expresa en dinero, porque materializarse "
  "significa comprar algo imprevisto, pagar horas adicionales o afrontar una penalización. Nada de eso "
  "ocurre aquí: el proyecto no compra, no contrata y no tiene cliente que penalice. Lo que sí puede perder "
  "es tiempo y alcance, y por eso el impacto se valora en días hábiles de retraso y en la degradación "
  "concreta que produciría sobre el producto.")

H(doc,"19. Escalas de valoración",2)
table(doc,["Nivel","Probabilidad","Impacto en cronograma","Impacto en alcance"],[
 ("Muy bajo","10 %","Alrededor de 1 día hábil","Ningún entregable afectado"),
 ("Bajo","30 %","Alrededor de 2 días hábiles","Un entregable secundario se degrada"),
 ("Medio","50 %","Alrededor de 3 días hábiles","Un entregable principal se degrada"),
 ("Alto","70 %","Alrededor de 5 días hábiles","Se pierde un entregable secundario"),
 ("Muy alto","90 %","8 días o más, o compromete la entrega","Se pierde un entregable principal"),
],widths=[2.0,2.2,4.8,7.0],fs=9.5)
H(doc,"19.1 Umbrales de acción",3)
table(doc,["Severidad","Definición","Acción obligatoria"],[
 ("Baja","Producto de los niveles menor o igual a 4","Se registra y se vigila. No requiere respuesta activa."),
 ("Moderada","Producto entre 5 y 9","Requiere estrategia de respuesta y responsable asignado."),
 ("Alta","Producto entre 10 y 15","Requiere respuesta activa, plan de contingencia y revisión semanal explícita."),
 ("Muy alta","Producto mayor a 15","Se escala al director. Requiere plan aprobado antes de continuar."),
],widths=[2.2,5.4,8.4],fs=9.5)
P(doc,"Tolerancia al riesgo del proyecto: la fecha de entrega es la restricción rígida, porque los exámenes "
  "del semestre no son negociables. El alcance es la variable con la que se absorben los imprevistos. En "
  "caso de conflicto, se sacrifica alcance antes que fecha.")

H(doc,"20. Categorías de riesgo",2)
P(doc,"La estructura de desglose de riesgos agrupa las fuentes de incertidumbre. Respecto de la versión "
  "anterior del plan se agregaron tres categorías: herramientas e infraestructura, equipo y organización, y "
  "alcance.")
cnt = Counter(r[5] for r in PR.RIESGOS)
table(doc,["Categoría","Qué agrupa","Riesgos"],
 [(c, desc, ", ".join(r[0] for r in PR.RIESGOS if r[5]==c)) for c,desc in PR.CATEGORIAS.items()],
 widths=[2.4,7.2,6.4],fs=9.5)

H(doc,"21. Registro de riesgos",2)
P(doc,f"Se identificaron {len(PR.RIESGOS)} riesgos. El valor esperado de cada uno es el producto de su "
  "probabilidad por su impacto en días.")
rows=[(r[0], r[1], r[5], f"{r[2]:.0%}", f"{r[3]:.1f} d", f"{r[2]*r[3]:.2f} d", r[6], r[7]) for r in PR.RIESGOS]
rows.append(("","Valor esperado total","","","",f"{PR.EMV_DIAS:.2f} d","",""))
table(doc,["Id","Riesgo","Categoría","Prob.","Impacto","Valor esp.","Estrategia","Responsable"],rows,
      widths=[0.8,5.6,1.8,1.1,1.3,1.4,1.8,2.2],fs=8)

doc.add_page_break()
H(doc,"22. Suficiencia de la reserva de cronograma",2)
P(doc,"La reserva de cronograma es la diferencia entre el tiempo disponible y la duración de la red de "
  "actividades. Es el colchón con que el proyecto absorbe los retrasos.")
table(doc,["Concepto","Días hábiles"],[
 ("Disponibles del 7 de septiembre al 13 de noviembre de 2026", f"{K.DIAS_DISPONIBLES}"),
 ("Duración de la red de actividades", f"{K.DURACION_RED:.2f}"),
 ("Reserva de cronograma", f"{K.RESERVA_CRONO:.2f}"),
],widths=[11.0,5.0],fs=10)

H(doc,"22.1 Qué parte del riesgo consume la reserva",3)
P(doc,"No todo retraso consume reserva. Si el riesgo afecta a un área que tiene holgura, esa holgura lo "
  "absorbe sin mover la fecha final. Solo consumen reserva los riesgos que golpean la ruta crítica o al "
  "equipo completo.")
table(doc,["Área","Responsable","Holgura mínima","¿Absorbe retrasos?"],
 [(a, R.RESP[a], f"{min(R.V2['HT'][k] for k in R.ORD if R.T[k]['area']==a):.2f} d",
   "No. Está sobre la ruta crítica" if min(R.V2['HT'][k] for k in R.ORD if R.T[k]['area']==a)<1e-9
   else "Sí, hasta ese margen")
  for a in sorted(R.AREAS, key=lambda x: min(R.V2['HT'][k] for k in R.ORD if R.T[k]['area']==x))],
 widths=[4.6,2.8,3.0,5.6],fs=9.5)
P(doc,"Con ese criterio, los riesgos R6, R7 y R13 quedan absorbidos por la holgura de las áreas de sonido, "
  "interfaz y desarrollo. Los quince restantes consumen reserva.")
table(doc,["Concepto","Días hábiles","Lectura"],[
 ("Valor esperado de los 18 riesgos", f"{PR.EMV_DIAS:.2f}","Suma completa del registro."),
 ("Valor esperado que consume reserva", f"{PR.EMV_RESERVA:.2f}","Descontando los tres riesgos que absorbe la holgura de área."),
 ("Reserva de cronograma disponible", f"{K.RESERVA_CRONO:.2f}","Cubre el "+f"{100*K.RESERVA_CRONO/PR.EMV_RESERVA:.0f} % del valor esperado."),
 ("Brecha", f"{PR.EMV_RESERVA-K.RESERVA_CRONO:.2f}","Lo que la reserva no alcanza a cubrir."),
],widths=[6.0,3.0,7.0],fs=10)

H(doc,"22.2 La reserva es insuficiente, y qué hacer al respecto",3)
P(doc,"Conviene decirlo sin rodeos: al ampliar el registro de nueve a dieciocho riesgos, el valor esperado "
  f"subió a {PR.EMV_RESERVA:.2f} días y la reserva disponible es de {K.RESERVA_CRONO:.2f}. La reserva cubre "
  f"alrededor de dos tercios de la exposición del proyecto.")
pts,_ = CP.curva()
comp = pts[0][0]-pts[-1][0]
table(doc,["Medida","Días que aporta","Costo","Observación"],[
 ("Reserva de cronograma actual", f"{K.RESERVA_CRONO:.2f}","Ninguno","Ya disponible."),
 ("Comprimir la red mediante jornada extendida", f"{comp:.2f}", f"${pts[-1][1]:,.0f}",
  "Analizada en el documento de costos. Es la medida más barata."),
 ("Suma de ambas", f"{K.RESERVA_CRONO+comp:.2f}", f"${pts[-1][1]:,.0f}",
  f"Cubre el {100*(K.RESERVA_CRONO+comp)/PR.EMV_RESERVA:.0f} % de la exposición."),
 ("Brecha restante", f"{PR.EMV_RESERVA-K.RESERVA_CRONO-comp:.2f}","—",
  "Se cierra recortando alcance secundario si llega a hacer falta."),
],widths=[5.6,2.4,2.4,5.6],fs=9.5)
P(doc,"Dos precisiones sobre cómo leer esta cifra. La primera: el valor esperado supone que los dieciocho "
  "riesgos son independientes y que sus impactos se suman, lo cual es una cota superior conservadora; en la "
  "práctica no todos se materializan. La segunda, en sentido contrario: el valor esperado es un promedio, "
  "no un tope. Si coincidieran los tres riesgos de mayor impacto, el retraso superaría con holgura "
  "cualquier reserva razonable.")
P(doc,"La conclusión práctica no es alarmante sino operativa: el proyecto cabe en el calendario en el "
  "escenario esperado, pero no tiene margen para una racha de mala suerte. Por eso los riesgos de mayor "
  "valor esperado, que son R17 sobre cambios de alcance, R16 sobre el choque con exámenes y R3 sobre la "
  "sobrecarga de QA, deben vigilarse semanalmente y no solo en los hitos.")
if os.path.exists(FIG+"Fig4_Matriz_riesgos.png"):
    doc.add_picture(FIG+"Fig4_Matriz_riesgos.png", width=Cm(13.6)); doc.paragraphs[-1].alignment=C
    caption(doc,"Matriz de probabilidad e impacto. Corresponde a los nueve riesgos originales; los nueve agregados se ubican en la tabla de la sección 21.")

doc.add_page_break()
H(doc,"23. Respuestas a los riesgos",2)
P(doc,"Cada riesgo lleva su disparador, redactado como un hecho observable, y el plan que se ejecuta cuando "
  "ese hecho ocurre.")
for rid, desc, prob, dias, alc, cat, est, resp, disp, plan in PR.RIESGOS:
    H(doc, f"{rid} — {desc}", 3)
    table(doc,["Campo","Contenido"],[
     ("Categoría",cat),
     ("Probabilidad e impacto",f"{prob:.0%} · {dias:.1f} días hábiles · valor esperado {prob*dias:.2f} días"),
     ("Impacto sobre el alcance",alc),
     ("Estrategia",est),
     ("Responsable",resp),
     ("Disparador",disp),
     ("Plan de respuesta",plan),
    ],widths=[4.0,12.0],fs=9)

doc.save('/tmp/_pcr_d.docx'); print("D OK")
