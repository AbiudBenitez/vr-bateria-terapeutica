# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import rc257 as R, costos as K
M = R.V2
def d(x): return f"${x:,.0f}"
doc = Document('/tmp/_cost_d.docx')

c = K.corte(9.0)
PV, EV, BAC = c["PV"], c["EV"], K.PRESUPUESTO
SV, SPI = EV-PV, EV/PV

# ================================================================ 13
H(doc,"13. Controlar los costos",1)
P(doc,"Los procesos anteriores producen la línea base. Controlar los costos es el proceso de monitorear el "
  "avance real contra esa línea base, medir la desviación y pronosticar el resultado final. La guía PMBOK "
  "emplea para ello la gestión del valor ganado, que compara tres magnitudes expresadas todas en dinero.")

H(doc,"13.1 Las tres magnitudes",2)
table(doc,["Magnitud","Qué mide","Cómo se obtiene en este proyecto"],[
 ("Valor planificado (PV)","Cuánto valor debería haberse producido a la fecha de corte, según el plan.","Se acumula el costo de cada actividad en proporción al avance que el cronograma le asigna a esa fecha."),
 ("Valor ganado (EV)","Cuánto valor se ha producido realmente.","Suma del costo presupuestado de las actividades terminadas. Con la regla 0/100, una actividad aporta su costo completo al cumplir su criterio de aceptación, y cero antes."),
 ("Costo real (AC)","Cuánto se ha gastado realmente para producir ese valor.","Horas efectivamente trabajadas por la tarifa del perfil. Requiere que el equipo registre horas, cosa que hoy no hace."),
],widths=[3.2,5.2,7.6],fs=9.5)

H(doc,"13.2 Los índices de desempeño",2)
table(doc,["Indicador","Fórmula","Interpretación"],[
 ("Variación del cronograma (SV)","EV menos PV","Positiva, el proyecto va adelantado; negativa, atrasado. Se expresa en dinero aunque mida tiempo."),
 ("Índice de desempeño del cronograma (SPI)","EV entre PV","Mayor que 1, se produce más valor del planificado. Menor que 1, menos."),
 ("Variación del costo (CV)","EV menos AC","Positiva, se gastó menos de lo presupuestado para el valor producido."),
 ("Índice de desempeño del costo (CPI)","EV entre AC","Mayor que 1, eficiencia en costo. Menor que 1, sobrecosto."),
],widths=[4.4,2.8,8.8],fs=9.5)

H(doc,"13.3 Medición al corte de medio curso",2)
P(doc,f"Se toma como fecha de corte el cierre del {K.fecha(8):%d de %B de %Y}, que corresponde al día hábil "
  f"{int(c['dia'])} del proyecto y al último día laborable antes de la entrega de medio curso.")
table(doc,["Concepto","Valor"],[
 ("Actividades terminadas", f"{len(c['terminadas'])} de 257"),
 ("Actividades en curso", f"{len(c['en_curso'])}"),
 ("Horas de esfuerzo completadas", f"{c['horas']:,.0f} de {K.HORAS_TOT:,.0f}  ({100*c['horas']/K.HORAS_TOT:.0f} %)"),
 ("Valor planificado (PV)", d(PV)),
 ("Valor ganado (EV)", d(EV)),
 ("Variación del cronograma (SV)", d(SV)),
 ("Índice de desempeño del cronograma (SPI)", f"{SPI:.3f}"),
 ("Presupuesto hasta la conclusión (BAC)", d(BAC)),
],widths=[9.0,7.0],fs=10)
P(doc,f"El índice de desempeño del cronograma es {SPI:.3f}, es decir que el proyecto ha producido el "
  f"{100*SPI:.1f} % del valor que el plan preveía para esta fecha. La desviación es de {d(abs(SV))}, "
  f"equivalente a menos de medio día hábil de trabajo del equipo completo. El proyecto está esencialmente "
  "en plan.")
P(doc,"Conviene señalar qué no se puede medir todavía. El costo real exige registrar las horas que cada "
  "integrante dedica efectivamente a cada actividad, y la hoja de control del equipo registra la fecha real "
  "de término pero no las horas. Sin ese dato no pueden calcularse el índice de desempeño del costo ni la "
  "variación del costo, que son la mitad del método.")

H(doc,"13.4 Pronósticos",2)
P(doc,"A partir del desempeño observado se proyecta el resultado final. La guía PMBOK ofrece varias "
  "fórmulas según el supuesto que se adopte sobre el comportamiento futuro.")
eac1 = BAC
eac2 = BAC/SPI
table(doc,["Pronóstico","Fórmula","Supuesto","Resultado"],[
 ("Estimación a la conclusión (EAC)","BAC","Las desviaciones observadas son atípicas y no se repetirán.",d(eac1)),
 ("Estimación a la conclusión (EAC)","BAC entre SPI","El desempeño del cronograma observado se mantiene hasta el final.",d(eac2)),
 ("Estimación hasta la conclusión (ETC)","EAC menos EV","Trabajo que resta por producir, bajo el segundo supuesto.",d(eac2-EV)),
 ("Variación a la conclusión (VAC)","BAC menos EAC","Diferencia esperada contra el presupuesto, bajo el segundo supuesto.",d(BAC-eac2)),
],widths=[4.2,3.0,6.0,2.8],fs=9.5)
P(doc,f"Bajo el supuesto conservador, si el ritmo actual se mantiene, el proyecto concluiría con un valor de "
  f"{d(eac2)}, es decir {d(abs(BAC-eac2))} por encima del presupuesto. Como el costo es proporcional a las "
  "horas y estas no cambian, esa diferencia no significa gastar más dinero: significa que el equipo "
  "necesitaría más horas de las estimadas, y por tanto más días de calendario. Se absorbería con la reserva "
  "de cronograma.")

H(doc,"13.5 Qué debe empezar a registrarse",2)
P(doc,"Para que el control de costos funcione durante el resto del proyecto hacen falta dos datos que hoy no "
  "se capturan.")
table(doc,["Dato","Para qué sirve","Dónde registrarlo"],[
 ("Horas efectivamente dedicadas a cada actividad","Permite calcular el costo real y con él el índice de desempeño del costo.","Campo de trabajo real en ProjectLibre, o una columna adicional en el reporte semanal."),
 ("Porcentaje de avance de las actividades en curso","Permite refinar el valor ganado en los cortes intermedios.","Campo de porcentaje completado en ProjectLibre."),
],widths=[4.6,6.4,5.0],fs=9.5)
P(doc,"Con la regla 0/100 declarada en la sección 2, el porcentaje de avance no altera el valor ganado, pero "
  "sí sirve para anticipar si una actividad va a cerrar a tiempo. El registro de horas es el dato "
  "indispensable: sin él, la mitad del método de valor ganado queda inutilizable.")

doc.add_page_break()
doc.save('/tmp/_cost_e.docx'); print("E OK")
