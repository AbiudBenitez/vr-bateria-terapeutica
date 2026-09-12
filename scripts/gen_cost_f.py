# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import rc257 as R, costos as K, compresion as CP
M = R.V2
def d(x): return f"${x:,.0f}"
def d2(x): return f"${x:,.2f}"
f = R.fnum
doc = Document('/tmp/_cost_e.docx')

# ================================================================ 14
H(doc,"14. Conclusiones",1)
H(doc,"14.1 Resultado de la estimación",2)
table(doc,["Concepto","Valor"],[
 ("Actividades estimadas","257"),
 ("Esfuerzo total",f"{K.HORAS_TOT:,.0f} horas"),
 ("Tarifa media ponderada",d2(K.TARIFA_MED)+" por hora"),
 ("Mano de obra",d(K.MANO_OBRA)),
 ("Costos no laborales",d(K.NO_LAB_TOT)),
 ("Reserva de contingencia, por valor monetario esperado",d(K.CONTINGENCIA)),
 ("Línea base de costos",d(K.LINEA_BASE)),
 ("Reserva de gestión",d(K.GESTION)),
 ("Presupuesto total",d(K.PRESUPUESTO)),
 ("Valor de los recursos proporcionados por la Facultad, fuera del presupuesto",d(K.VALOR_PROPORCIONADO)),
],widths=[10.0,6.0],fs=10)

H(doc,"14.2 Hallazgos",2)
bullets(doc,[
 "El presupuesto se estimó de forma ascendente sobre las 257 actividades, que es la técnica más exacta de "
 "las que reconoce la guía y la única aplicable con el nivel de detalle disponible.",
 "Las tarifas provienen exclusivamente de fuentes oficiales mexicanas: el Observatorio Laboral de la "
 "Secretaría del Trabajo, Data México de la Secretaría de Economía, la CONASAMI y el IMSS. No se emplearon "
 "portales de empleo, que publican salarios ofrecidos y no ingresos percibidos.",
 "La tarifa media ponderada resultante, "+d2(K.TARIFA_MED)+" por hora, coincide con el equivalente de dos "
 "salarios mínimos generales, lo que verifica el orden de magnitud por una vía independiente.",
 "El área de QA, documentación y gestión concentra el "
 f"{100*K.POR_AREA['QA, documentación y gestión'][2]/K.MANO_OBRA:.0f} % del costo de mano de obra, porque "
 "absorbe la planificación y el seguimiento además de las pruebas y la documentación.",
 "El costo de la calidad asciende a "+d(sum(K.COQ_TOT.values()))+", con una proporción sana entre "
 "prevención y corrección de fallos.",
 "La reserva de contingencia se sustenta en el valor monetario esperado de nueve riesgos identificados, y "
 "no en un porcentaje fijo.",
 "El proyecto puede comprimirse hasta 4.10 días hábiles por "+d(CP.curva()[0][-1][1])+", aunque no lo "
 "necesita para cumplir el calendario.",
])

H(doc,"14.3 Sobre la magnitud del presupuesto",2)
P(doc,"Una versión preliminar de esta estimación arrojó un presupuesto considerablemente mayor porque "
  "empleaba tarifas de mercado tomadas de referencias no oficiales. Al sustituirlas por los datos del "
  "Observatorio Laboral, el costo de mano de obra se redujo un 45 % y el presupuesto total un 44 %.")
P(doc,"La diferencia no es un ajuste cosmético: las fuentes no oficiales publican el salario que las "
  "empresas ofrecen en sus vacantes, que sistemáticamente supera el ingreso que los profesionistas "
  "efectivamente perciben, porque las vacantes mejor pagadas son las que más se publican y porque el monto "
  "anunciado suele corresponder al tope del rango. La Encuesta Nacional de Ocupación y Empleo mide lo "
  "segundo, que es lo que corresponde usar para estimar un costo.")

H(doc,"14.4 Recomendaciones",2)
table(doc,["#","Recomendación","Efecto"],[
 ("1","Confirmar por escrito el préstamo de los visores con la Facultad antes del inicio de la fase de desarrollo.",
  "Elimina el riesgo R5, que es el de mayor impacto unitario del registro."),
 ("2","Redistribuir las tareas de documentación, evidencias y manuales del área de QA entre las ocho áreas.",
  "Atiende el riesgo R3 y corrige la restricción dominante del proyecto, que es de carga y no de costo."),
 ("3","Asignar de forma explícita los roles de dirección, gerencia y coordinación.",
  "Saca de QA el trabajo de planificación y seguimiento, que hoy está concentrado ahí por omisión."),
 ("4","Verificar la licencia de cada recurso gráfico y de audio antes de incorporarlo.",
  "Atiende el riesgo R4, cuya probabilidad subió al sustituir recursos de pago por recursos libres."),
 ("5","Reservar la compresión de la red como respuesta ante la materialización de un riesgo de cronograma.",
  "Convierte una capacidad ya cuantificada en un plan de contingencia concreto."),
 ("6","Presentar el escenario A junto con la línea base ante la patrocinadora.",
  "Distingue el costo valorizado del desembolso real, que son "+d(K.escenario(0.0)[3])+"."),
],widths=[0.8,8.4,6.8],fs=9.5)

# ================================================================ anexos
doc.add_page_break()
H(doc,"Anexo A. Costeo de las 257 actividades",1)
P(doc,"Cada actividad con su perfil asignado, tarifa, horas y costo. Es el nivel más bajo de la estimación "
  "ascendente; todas las cifras del documento se obtienen sumando esta tabla.")
rows=[(k, R.T[k]["desc"], R.T[k]["sig"], K.perfil(k)[:24], d2(K.tarifa(k)),
       f"{K.horas(k):g}", d(K.costo(k))) for k in R.ORD]
rows.append(("","Total","","","",f"{K.HORAS_TOT:,.0f}",d(K.MANO_OBRA)))
table(doc,["Clave","Actividad","Á.","Perfil","$/h","Horas","Costo"],rows,
      widths=[1.3,5.6,0.7,3.4,1.4,1.2,2.0],fs=7)

doc.add_page_break()
H(doc,"Anexo B. Pendientes de costo de las actividades críticas",1)
P(doc,"Las actividades de la ruta crítica, ordenadas de la más barata a la más cara de comprimir.")
rows=[(k, R.T[k]["desc"][:52], f(R.T[k]["dur"]), f"{CP.comprimible(k):.2f}", d(K.costo(k)),
       d(CP.sobrecosto(k)), d(CP.pendiente(k))) for k in CP.CANDIDATAS]
table(doc,["Clave","Actividad","Dur.","Recorte","Costo normal","Sobrecosto","$/día"],rows,
      widths=[1.3,6.2,1.1,1.4,2.2,2.0,1.8],fs=8)

doc.add_page_break()
H(doc,"Anexo C. Fuentes consultadas",1)
table(doc,["Fuente","Institución","Consulta"],[
 ("Observatorio Laboral Mexicano. Tendencias del empleo profesional, 2.º trimestre de 2026.",
  "Secretaría del Trabajo y Previsión Social, con datos de la Encuesta Nacional de Ocupación y Empleo del INEGI.",
  "observatoriolaboral.gob.mx"),
 ("Data México. Perfil de la ocupación «Desarrolladores y Analistas de Software y Multimedia», 1.er trimestre de 2026.",
  "Secretaría de Economía.","economia.gob.mx/datamexico"),
 ("Salarios mínimos generales y profesionales vigentes a partir del 1 de enero de 2026.",
  "Comisión Nacional de los Salarios Mínimos.","gob.mx/conasami"),
 ("Salario base de cotización promedio de los puestos de trabajo afiliados, enero de 2026.",
  "Instituto Mexicano del Seguro Social.","imss.gob.mx"),
 ("Guía de los Fundamentos para la Dirección de Proyectos (Guía del PMBOK).",
  "Project Management Institute.","Áreas de conocimiento 7, 8 y 11"),
 ("Ley Federal del Trabajo, artículos 66 a 68, sobre jornada extraordinaria.",
  "Cámara de Diputados del H. Congreso de la Unión.","Base del modelo de compresión"),
],widths=[7.0,6.0,3.0],fs=9)

out="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/Analisis_Costos_Calidad_Riesgos.docx"
doc.save(out); print("OK", out)
print("párrafos:",len(doc.paragraphs)," tablas:",len(doc.tables)," imágenes:",len(doc.inline_shapes))
