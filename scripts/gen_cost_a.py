# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
import rc257 as R, costos as K
M = R.V2
def d(x): return f"${x:,.0f}"
def d2(x): return f"${x:,.2f}"

doc = nuevo()
portada(doc,
 "ANÁLISIS DE COSTOS, CALIDAD Y RIESGOS",
 "Simulación VR de batería con juego de ritmo",
 [("Unidad de aprendizaje","Administración de Proyectos de Software"),
  ("Docente","Dra. Leticia Amalia Neira Tovar"),
  ("Equipo","Equipo A"),
  ("Marco de referencia","Guía PMBOK: áreas 7 Costos, 8 Calidad y 11 Riesgos"),
  ("Técnica de estimación","Ascendente (bottom-up), sobre 257 actividades"),
  ("Criterio de duración","Rangos al valor menor, alineado con la hoja de control"),
  ("Esfuerzo estimado",f"{K.HORAS_TOT:,.0f} horas"),
  ("Presupuesto total",d(K.PRESUPUESTO)),
  ("Fecha","11 de septiembre de 2026")],
 sub2="Estimación con tarifas derivadas de fuentes oficiales mexicanas")

# ================================================================ 1
H(doc,"1. Alcance del documento",1)
P(doc,"Este documento desarrolla tres áreas de conocimiento de la guía PMBOK sobre el proyecto de "
  "simulación de batería en realidad virtual con juego de ritmo, tomando como base las 257 actividades "
  "definidas por el equipo y la red de precedencias del documento de ruta crítica.")
table(doc,["Área","Procesos que se desarrollan","Sección"],[
 ("7. Gestión de los Costos","7.1 Planificar la gestión de los costos · 7.2 Estimar los costos · 7.3 Determinar el presupuesto","2 a 7"),
 ("8. Gestión de la Calidad","Análisis del costo de la calidad, como insumo de 8.1 Planificar la gestión de la calidad","10"),
 ("11. Gestión de los Riesgos","11.2 Identificar los riesgos · 11.3 Análisis cualitativo · 11.4 Análisis cuantitativo, como sustento de la reserva de contingencia","11"),
],widths=[4.0,9.4,2.6],fs=9.5)
P(doc,"Los planes formales de gestión de la calidad y de los riesgos, con sus políticas, roles y respuestas, "
  "se desarrollan en el documento «Plan de Gestión de la Calidad y Plan de Gestión de los Riesgos». Aquí se "
  "presenta el análisis numérico que los sustenta.")

# ================================================================ 2
H(doc,"2. Planificar la gestión de los costos",1)
P(doc,"Este proceso establece las políticas y procedimientos con los que se estiman, presupuestan y "
  "controlan los costos del proyecto.")
table(doc,["Concepto","Definición adoptada"],[
 ("Unidad de medida del esfuerzo","Hora-persona. Las duraciones de las actividades se expresan en días laborables de ocho horas y se convierten a horas para costear."),
 ("Moneda","Peso mexicano (MXN), a precios de 2026. No se aplica inflación: el proyecto dura once semanas."),
 ("Nivel de precisión","Los montos se redondean al peso. Las tarifas por hora se expresan con dos decimales."),
 ("Nivel de exactitud","±10 % sobre la línea base, que corresponde a una estimación definitiva conforme a la clasificación de la guía."),
 ("Enlace con la estructura de desglose","Cada actividad pertenece a un grupo de claves y cada grupo a un área. Los tres niveles son cuentas de control."),
 ("Umbral de control","Una desviación acumulada superior al 10 % sobre la línea base en cualquier área obliga a informar al director del proyecto."),
 ("Regla de medición del desempeño","Valor ganado con la regla 0/100: una actividad aporta valor solo cuando cumple su criterio de aceptación. No se reconoce avance parcial."),
 ("Formato de los informes","Informe semanal de costo por área, con costo real contra valor planificado y valor ganado."),
],widths=[4.4,11.6],fs=9.5)

# ================================================================ 3
H(doc,"3. Estimar los costos: elección de la técnica",1)
P(doc,"La guía PMBOK reconoce varias técnicas para estimar costos. Se evaluaron tres y se eligió la "
  "estimación ascendente.")
table(doc,["Técnica","En qué consiste","Por qué se descartó o se eligió"],[
 ("Estimación análoga","Tomar el costo de un proyecto anterior parecido y ajustarlo.",
  "Descartada. El equipo no ha ejecutado ningún proyecto de realidad virtual previo, de modo que no existe un referente del cual partir."),
 ("Estimación paramétrica","Aplicar una relación estadística, por ejemplo un costo por punto de función o por línea de código.",
  "Descartada. No se dispone de datos históricos propios para calibrar el parámetro, y los valores publicados para otras industrias no son trasladables."),
 ("Estimación ascendente","Estimar el costo de cada actividad del nivel más bajo y sumar hacia arriba hasta obtener el total del proyecto.",
  "Elegida. El equipo ya descompuso el trabajo en 257 actividades con duración individual. Es la técnica más exacta y la única que el estado de la planificación permite aplicar."),
],widths=[3.4,5.6,7.0],fs=9.5)
P(doc,"La estimación ascendente exige que cada actividad tenga duración conocida y un recurso asignado. "
  "Ambas condiciones se cumplen: la duración proviene de la lista de actividades del equipo y el recurso se "
  "asigna por perfil, conforme a la sección 5.")

# ================================================================ 4
H(doc,"4. Determinación de las tarifas",1)
H(doc,"4.1 Criterio de selección de las fuentes",2)
P(doc,"Las tarifas no se tomaron de portales de empleo ni de agregadores de ofertas laborales, porque esas "
  "fuentes publican salarios ofrecidos y autorreportados, no ingresos efectivamente percibidos, y tienden a "
  "sobrestimar. Se emplearon exclusivamente fuentes oficiales del gobierno mexicano.")
table(doc,["Fuente","Institución","Dato utilizado","Periodo"],[
 ("Observatorio Laboral","Secretaría del Trabajo y Previsión Social, con datos de la Encuesta Nacional de Ocupación y Empleo del INEGI",
  "Ingreso promedio mensual de los profesionistas ocupados, por área de conocimiento","2.º trimestre de 2026"),
 ("Data México","Secretaría de Economía, con datos de la Encuesta Nacional de Ocupación y Empleo",
  "Ingreso promedio mensual por ocupación específica","1.er trimestre de 2026"),
 ("Salarios mínimos","Comisión Nacional de los Salarios Mínimos (CONASAMI)",
  "Salario mínimo general vigente, para el escenario de valoración a nivel de practicante","Vigente desde el 1 de enero de 2026"),
 ("Salario base de cotización","Instituto Mexicano del Seguro Social",
  "Salario base de cotización promedio nacional, empleado como contraste","Enero de 2026"),
],widths=[3.0,5.4,5.4,2.2],fs=9)

H(doc,"4.2 Valores de referencia",2)
table(doc,["Referencia","Ingreso mensual","Fuente"],
 [(k, d(v), s) for k,(v,s) in K.OFICIAL.items()],
 widths=[2.4,2.6,11.0],fs=8.5)

H(doc,"4.3 Conversión a tarifa horaria",2)
P(doc,"El ingreso mensual se divide entre 173.33 horas laborables al mes, que resultan de una jornada de "
  "cuarenta horas semanales multiplicada por 52 semanas y dividida entre 12 meses. Es el mismo divisor que "
  "emplea la práctica contable mexicana para obtener el costo horario a partir del sueldo.")
P(doc,"Algunos perfiles llevan un factor de ajuste sobre la referencia. Los factores superiores a uno "
  "corresponden a responsabilidad directiva o de planificación; los inferiores a uno, a perfiles de entrada.")
rows=[]
for p,(anc,fac,just) in K.PERFIL_BASE.items():
    tar,men = K.PERFIL[p]
    rows.append((p, anc, f"{fac:.2f}", d(men), d2(tar), just))
table(doc,["Perfil","Ref.","Factor","Mensual","Por hora","Justificación del factor"],rows,
      widths=[3.6,1.2,1.2,1.8,1.6,6.6],fs=8.5)
P(doc,f"Tarifa media ponderada del proyecto: {d2(K.TARIFA_MED)} por hora. Se obtiene dividiendo el costo "
  f"total de mano de obra entre las {K.HORAS_TOT:,.0f} horas estimadas.")

H(doc,"4.4 Contraste de las referencias entre sí",2)
P(doc,"Conviene verificar que las cifras adoptadas sean coherentes con las demás fuentes oficiales, porque "
  "cada una mide un universo distinto.")
table(doc,["Contraste","Valor","Lectura"],[
 ("Tarifa media del proyecto", d2(K.TARIFA_MED)+" por hora", "Equivale a "+d(K.TARIFA_MED*K.HMES)+" mensuales."),
 ("Salario base de cotización promedio del IMSS", d(K.OFICIAL['IMSS_SBC'][0])+" mensuales",
  "La tarifa media del proyecto queda por debajo, lo cual es consistente: el proyecto incluye perfiles de entrada."),
 ("Ocupación «Desarrolladores y Analistas de Software y Multimedia» en Data México", d(K.OFICIAL['OCUP_SW'][0])+" mensuales",
  "Muy por debajo de la referencia de profesionistas en TIC. La diferencia se explica porque esa medición incluye a trabajadores sin estudios superiores y un 14.2 % de informalidad."),
 ("Dos salarios mínimos generales", d(K.OFICIAL['SM'][0]*2)+" mensuales",
  "Coincide casi exactamente con la tarifa media adoptada. Es una verificación independiente de que el orden de magnitud es correcto."),
],widths=[5.0,3.4,7.6],fs=9)
P(doc,"La coincidencia entre la tarifa media adoptada y el equivalente de dos salarios mínimos generales "
  "respalda la estimación por una vía distinta de la que se empleó para construirla.")

doc.add_page_break()
doc.save('/tmp/_cost_a.docx'); print("A OK")
