# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
import rc257 as R, costos as K, pruebas as PR
def d(x): return f"${x:,.0f}"
def d2(x): return f"${x:,.2f}"
c9 = K.corte(9.0)

doc = nuevo()
portada(doc,
 "PLANES DE COSTOS, CALIDAD Y RIESGOS",
 "Simulación VR de batería con juego de ritmo",
 [("Unidad de aprendizaje","Administración de Proyectos de Software"),
  ("Docente","Dra. Leticia Amalia Neira Tovar"),
  ("Equipo","Equipo A"),
  ("Marco de referencia","Guía PMBOK: áreas 7 Costos, 8 Calidad y 11 Riesgos"),
  ("Contenido","Plan de costos · Plan de calidad · Pruebas de calidad · Plan de riesgos"),
  ("Presupuesto",d(K.PRESUPUESTO)),
  ("Casos de prueba diseñados",f"{len(PR.CAJA_BLANCA)+len(PR.CAJA_NEGRA)}"),
  ("Riesgos identificados",f"{len(PR.RIESGOS)}"),
  ("Fecha","17 de septiembre de 2026")],
 sub2="Documento integrado de los tres planes de gestión")

H(doc,"Contenido del documento",1)
P(doc,"Este documento reúne en un solo lugar los tres planes de gestión que el proyecto requiere, más el "
  "diseño de las pruebas de calidad. Sustituye al documento «Plan de Gestión de la Calidad y Plan de "
  "Gestión de los Riesgos» entregado previamente, cuyo contenido se incorpora aquí actualizado y ampliado.")
table(doc,["Parte","Contenido","Área del PMBOK"],[
 ("I","Plan de gestión de los costos: estimación, presupuesto y control.","7. Gestión de los Costos"),
 ("II","Plan de gestión de la calidad: política, métricas, estándares y procesos.","8. Gestión de la Calidad"),
 ("III","Pruebas de calidad: estrategia, técnicas de caja blanca y caja negra, catálogo de casos y responsables de ejecución.","8. Gestión de la Calidad"),
 ("IV","Plan de gestión de los riesgos: metodología, registro de 18 riesgos, respuestas, implementación y monitoreo.","11. Gestión de los Riesgos"),
],widths=[1.2,10.4,4.4],fs=10)
P(doc,"El análisis numérico que sustenta las partes I y IV, con la estimación ascendente completa de las "
  "257 actividades, la curva S, la compresión de la red y la tabla de simultaneidad, se conserva en el "
  "documento «Análisis de Costos, Calidad y Riesgos», al que este remite cuando corresponde.")

doc.add_page_break()
# ======================================================= PARTE I
H(doc,"PARTE I. PLAN DE GESTIÓN DE LOS COSTOS",1)

H(doc,"1. Planificar la gestión de los costos",2)
P(doc,"Este proceso establece las políticas y procedimientos con los que se estiman, presupuestan y "
  "controlan los costos.")
table(doc,["Concepto","Definición adoptada"],[
 ("Unidad de medida","Hora-persona. Las duraciones se expresan en días laborables de ocho horas y se convierten a horas para costear."),
 ("Moneda","Peso mexicano, a precios de 2026. No se aplica inflación: el proyecto dura ocho semanas."),
 ("Nivel de precisión","Los montos se redondean al peso; las tarifas por hora llevan dos decimales."),
 ("Nivel de exactitud","±10 % sobre la línea base, que corresponde a una estimación definitiva."),
 ("Cuentas de control","Tres niveles: actividad, grupo de claves y área. Cada uno agrega el costo del nivel inferior."),
 ("Umbral de control","Una desviación acumulada mayor al 10 % sobre la línea base en cualquier área obliga a informar al director."),
 ("Regla de medición","Valor ganado con la regla 0/100. Una actividad aporta valor solo cuando cumple su criterio de aceptación."),
 ("Informes","Reporte semanal por área, con valor planificado, valor ganado e índices de desempeño."),
],widths=[4.2,11.8],fs=10)

H(doc,"2. Estimar los costos",2)
H(doc,"2.1 Técnica empleada",3)
P(doc,"Se emplea estimación ascendente: se estima el costo de cada una de las 257 actividades del nivel más "
  "bajo y se suma hacia arriba. Se descartaron la estimación análoga, porque el equipo no tiene proyectos "
  "de realidad virtual previos que sirvan de referente, y la paramétrica, porque no hay datos históricos "
  "propios para calibrar el parámetro.")

H(doc,"2.2 Base de las tarifas",3)
P(doc,"El proyecto lo ejecutan ocho estudiantes en el marco de sus prácticas profesionales, bajo convenio "
  "con la Facultad. Esa condición determina el cálculo: las prácticas bajo convenio escolar no constituyen "
  "relación laboral, de modo que no generan séptimo día pagado ni prestaciones. La tarifa se obtiene "
  "dividiendo el salario mínimo general diario entre las ocho horas de la jornada legal.")
table(doc,["Referencia","Valor","Fuente"],
 [(k, v, s) for k,(v,s) in K.FUENTES.items()], widths=[2.2,2.8,11.0],fs=9)
P(doc,f"Un salario mínimo por hora equivale a {d2(K.SM_HORA)}. Cada perfil se expresa como múltiplo de esa "
  "base, según la responsabilidad del rol.")
table(doc,["Perfil","Múltiplo","Por hora","Justificación"],
 [(p, f"{m:.1f} SM", d2(K.PERFIL[p][0]), just)
  for p,(m,just) in sorted(K.PERFIL_BASE.items(), key=lambda x:-x[1][0])],
 widths=[4.2,1.6,1.8,8.4],fs=9)
P(doc,f"Tarifa media ponderada del proyecto: {d2(K.TARIFA_MED)} por hora, equivalente a "
  f"{K.TARIFA_MED/K.SM_HORA:.2f} salarios mínimos.")

H(doc,"3. Determinar el presupuesto",2)
H(doc,"3.1 El proyecto no realiza compras",3)
P(doc,"El presupuesto se compone únicamente de mano de obra. Los visores y el espacio de pruebas los "
  "aporta la Facultad; conforme a la guía PMBOK, los recursos que proporciona la organización ejecutante no "
  "se cargan al presupuesto, pero sí se registran porque su disponibilidad es un supuesto del que el "
  "proyecto depende. Los recursos gráficos, sonoros y de software se resuelven con licencias libres o "
  "gratuitas para estudiantes.")

H(doc,"3.2 Reservas",3)
P(doc,"La reserva de contingencia monetaria es cero, y la razón es estructural. Esa reserva existe para "
  "financiar el impacto económico de los riesgos; como el proyecto no compra nada, no contrata a nadie y no "
  "paga penalizaciones, ninguno de los riesgos identificados tiene impacto monetario. Todos impactan el "
  "cronograma o el alcance. En su lugar se constituye una reserva de cronograma, que es la respuesta "
  "adecuada a riesgos cuyo efecto se mide en días. Su dimensionamiento y su suficiencia se analizan en la "
  "sección 22.")

H(doc,"3.3 Integración del presupuesto",3)
table(doc,["Concepto","Monto"],[
 ("Mano de obra", d(K.MANO_OBRA)),
 ("Costos no laborales","Ninguno"),
 ("Costos directos", d(K.DIRECTOS)),
 ("Reserva de contingencia monetaria","Ninguna. Se sustituye por reserva de cronograma"),
 ("Línea base de costos", d(K.LINEA_BASE)),
 ("Reserva de gestión","Ninguna"),
 ("Presupuesto hasta la conclusión", d(K.PRESUPUESTO)),
],widths=[8.4,7.6],fs=10)
table(doc,["Área","Responsable","Horas","Costo","%"],
 [(a, R.RESP[a], f"{K.POR_AREA[a][1]:,.0f}", d(K.POR_AREA[a][2]),
   f"{100*K.POR_AREA[a][2]/K.MANO_OBRA:.1f} %")
  for a in sorted(R.AREAS, key=lambda x:-K.POR_AREA[x][2])] +
 [("Total","",f"{K.HORAS_TOT:,.0f}",d(K.MANO_OBRA),"100.0 %")],
 widths=[5.4,2.8,2.0,2.8,2.0],fs=9.5)

H(doc,"4. Controlar los costos",2)
P(doc,"El control se realiza mediante gestión del valor ganado, comparando tres magnitudes: el valor "
  "planificado, que es el valor que el plan preveía a la fecha; el valor ganado, que es el valor "
  "efectivamente producido; y el costo real, que es lo gastado para producirlo.")
table(doc,["Indicador","Fórmula","Interpretación"],[
 ("Variación del cronograma","Valor ganado menos valor planificado","Negativa indica atraso, expresado en dinero."),
 ("Índice de desempeño del cronograma","Valor ganado entre valor planificado","Menor que uno indica que se produce menos valor del previsto."),
 ("Variación del costo","Valor ganado menos costo real","Positiva indica que se gastó menos de lo presupuestado para el valor producido."),
 ("Índice de desempeño del costo","Valor ganado entre costo real","Menor que uno indica sobrecosto."),
],widths=[4.4,3.4,8.2],fs=9.5)
P(doc,f"Medición al último corte, cierre del {K.fecha(8):%d de %B}: valor planificado {d(c9['PV'])}, valor "
  f"ganado {d(c9['EV'])}, índice de desempeño del cronograma {c9['EV']/c9['PV']:.3f}. El proyecto está "
  "esencialmente en plan.")
P(doc,"Los índices de costo no pueden calcularse todavía, porque exigen registrar las horas efectivamente "
  "dedicadas a cada actividad y el equipo no lo hace. Es la principal carencia de control del proyecto y se "
  "recoge como riesgo R15.")

doc.add_page_break()
doc.save('/tmp/_pcr_a.docx'); print("A OK")
