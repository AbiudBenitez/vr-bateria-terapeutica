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
  ("Base de las tarifas","Salario mínimo general vigente, con escala por responsabilidad"),
  ("Esfuerzo estimado",f"{K.HORAS_TOT:,.0f} horas"),
  ("Presupuesto total",d(K.PRESUPUESTO)),
  ("Fecha","14 de septiembre de 2026")],
 sub2="Estimación ascendente sobre tarifas ancladas a fuentes oficiales")

# ================================================================ 1
H(doc,"1. Alcance del documento",1)
P(doc,"Este documento desarrolla tres áreas de conocimiento de la guía PMBOK sobre el proyecto de "
  "simulación de batería en realidad virtual con juego de ritmo, tomando como base las 257 actividades "
  "definidas por el equipo y la red de precedencias del documento de ruta crítica.")
table(doc,["Área","Procesos que se desarrollan","Sección"],[
 ("7. Gestión de los Costos","7.1 Planificar la gestión de los costos · 7.2 Estimar los costos · 7.3 Determinar el presupuesto · 7.4 Controlar los costos","2 a 8 y 13"),
 ("8. Gestión de la Calidad","Análisis del costo de la calidad, como insumo de 8.1 Planificar la gestión de la calidad","11"),
 ("11. Gestión de los Riesgos","11.2 Identificar los riesgos · 11.3 Análisis cualitativo · 11.4 Análisis cuantitativo","12"),
],widths=[4.0,9.4,2.6],fs=9.5)
P(doc,"Los planes formales de gestión de la calidad y de los riesgos, con sus políticas, roles, respuestas y "
  "procesos de implementación y monitoreo, se desarrollan en el documento «Plan de Gestión de la Calidad y "
  "Plan de Gestión de los Riesgos». Aquí se presenta el análisis numérico que los sustenta.")

# ================================================================ 2
H(doc,"2. Planificar la gestión de los costos",1)
P(doc,"Este proceso establece las políticas y procedimientos con los que se estiman, presupuestan y "
  "controlan los costos del proyecto.")
table(doc,["Concepto","Definición adoptada"],[
 ("Unidad de medida del esfuerzo","Hora-persona. Las duraciones de las actividades se expresan en días laborables de ocho horas y se convierten a horas para costear."),
 ("Moneda","Peso mexicano (MXN), a precios de 2026. No se aplica inflación: el proyecto dura ocho semanas."),
 ("Nivel de precisión","Los montos se redondean al peso. Las tarifas por hora se expresan con dos decimales."),
 ("Nivel de exactitud","±10 % sobre la línea base, que corresponde a una estimación definitiva conforme a la clasificación de la guía."),
 ("Enlace con la estructura de desglose","Cada actividad pertenece a un grupo de claves y cada grupo a un área. Los tres niveles son cuentas de control."),
 ("Umbral de control","Una desviación acumulada superior al 10 % sobre la línea base en cualquier área obliga a informar al director del proyecto."),
 ("Regla de medición del desempeño","Valor ganado con la regla 0/100: una actividad aporta valor solo cuando cumple su criterio de aceptación. No se reconoce avance parcial."),
 ("Formato de los informes","Informe semanal de costo por área, con valor planificado, valor ganado y los índices de desempeño."),
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
H(doc,"4.1 Naturaleza del equipo y consecuencia sobre la tarifa",2)
P(doc,"El proyecto lo ejecutan ocho estudiantes de licenciatura en el marco de sus prácticas profesionales, "
  "bajo convenio con la Facultad. Esa condición determina cómo debe calcularse la tarifa, y conviene "
  "explicarlo antes de presentar cifras.")
P(doc,"Las prácticas profesionales realizadas bajo convenio escolar no constituyen una relación laboral: no "
  "generan séptimo día pagado, ni aguinaldo, ni prima vacacional. La retribución corresponde a las horas "
  "efectivamente trabajadas. Por eso la tarifa por hora se obtiene dividiendo el salario mínimo general "
  "diario entre las ocho horas de la jornada legal, y no dividiendo el equivalente mensual entre las horas "
  "laborables del mes, que es el cálculo que corresponde a un trabajador de planta.")
table(doc,["Forma de conversión","Cálculo","Tarifa","A quién corresponde"],[
 ("Nominal, por hora trabajada", f"{d2(K.SM_DIARIO)} diarios entre 8 horas de jornada", d2(K.SM_HORA),
  "Practicante bajo convenio escolar. Es la que se aplica en este documento."),
 ("Costo patronal por hora productiva", "$9,577 mensuales entre 173.33 horas", "$55.25",
  "Trabajador con relación laboral formal, cuyo patrón paga también los días de descanso. No es el caso del equipo."),
],widths=[3.8,4.6,1.8,5.8],fs=9.5)
P(doc,"La diferencia entre ambas cifras no es de criterio contable sino de figura jurídica. Aplicar la "
  "segunda a un practicante sobrestimaría el costo, porque incluiría prestaciones que el convenio escolar no "
  "genera.")

H(doc,"4.2 Fuentes oficiales empleadas",2)
P(doc,"Las tarifas no se tomaron de portales de empleo ni de agregadores de ofertas laborales, porque esas "
  "fuentes publican salarios ofrecidos y autorreportados, no ingresos efectivamente percibidos, y tienden a "
  "sobrestimar. Se emplearon exclusivamente fuentes oficiales del gobierno mexicano.")
table(doc,["Referencia","Valor","Fuente y uso en este documento"],
 [(k, v, s) for k,(v,s) in K.FUENTES.items()],
 widths=[2.4,3.0,10.6],fs=9)
P(doc,"El programa Jóvenes Construyendo el Futuro merece mención aparte: es el único referente "
  "gubernamental de retribución a personas aprendices, y fija el apoyo mensual en el equivalente al salario "
  "mínimo general. Confirma que el salario mínimo es la referencia correcta para un perfil en formación, y "
  "que no existe base oficial para retribuir por debajo de él.")

H(doc,"4.3 Escala de tarifas por responsabilidad",2)
P(doc,"Los ocho integrantes son practicantes del mismo nivel académico, pero la responsabilidad de sus roles "
  "no es la misma: quien decide sobre el alcance del proyecto no asume la misma carga que quien redacta un "
  "manual. La tarifa se gradúa expresando cada perfil como múltiplo del salario mínimo por hora, que es la "
  "forma habitual de escalar retribuciones en México.")
rows=[]
for p,(m,just) in sorted(K.PERFIL_BASE.items(), key=lambda x:-x[1][0]):
    rows.append((p, f"{m:.1f} SM", d2(K.PERFIL[p][0]), just))
table(doc,["Perfil","Múltiplo","Por hora","Justificación del nivel"],rows,
      widths=[4.2,1.6,1.8,8.4],fs=8.5)
P(doc,f"Un salario mínimo por hora equivale a {d2(K.SM_HORA)}. La escala va de 1.0 a 2.2, es decir que el "
  f"perfil de mayor responsabilidad cuesta poco más del doble que el de entrada. La tarifa media ponderada "
  f"del proyecto es {d2(K.TARIFA_MED)} por hora, equivalente a {K.TARIFA_MED/K.SM_HORA:.2f} salarios mínimos.")

H(doc,"4.4 Contraste con el costo de personal titulado",2)
P(doc,"Conviene dimensionar lo que el proyecto ahorra por ejecutarse con practicantes. Si el mismo trabajo "
  "se contratara con profesionistas titulados, empleando las tarifas del Observatorio Laboral, el costo de "
  "mano de obra sería considerablemente mayor.")
table(doc,["Supuesto","Tarifa media","Mano de obra","Diferencia"],[
 ("Practicantes, escala del salario mínimo", d2(K.TARIFA_MED), d(K.MANO_OBRA), "—"),
 ("Profesionistas titulados, Observatorio Laboral", "$113.72", d(K.HORAS_TOT*113.72),
  d(K.HORAS_TOT*113.72-K.MANO_OBRA)+" más"),
],widths=[6.4,2.6,3.0,4.0],fs=9.5)
P(doc,"La diferencia no representa un ahorro que el proyecto capture, sino el valor del trabajo que los "
  "integrantes aportan mientras se forman. Se documenta porque es la magnitud que tendría el proyecto si se "
  "ejecutara comercialmente.")

doc.add_page_break()
# ================================================================ 5
H(doc,"5. Matriz de tiempos",1)
P(doc,"Las 257 duraciones, en horas, tras aplicar la conversión de ocho horas por día laborable. Se conserva "
  "la estimación original para poder verificar la conversión. Los rangos se toman en su valor menor, que es "
  "el criterio de la hoja de control de tareas del equipo.")
COLS = 3
mid = (len(R.ORD)+COLS-1)//COLS
part = [R.ORD[i*mid:(i+1)*mid] for i in range(COLS)]
rows = []
for i in range(mid):
    fila = []
    for c in range(COLS):
        if i < len(part[c]):
            k = part[c][i]; fila += [k, f"{K.horas(k):g}", R.T[k]["durtxt"]]
        else: fila += ["", "", ""]
    rows.append(fila)
table(doc,["Clave","Horas","Original"]*COLS, rows, widths=[1.5,1.0,2.8]*COLS, fs=7.5)
P(doc,f"Suma total: {K.HORAS_TOT:,.0f} horas. Representa el esfuerzo del proyecto, es decir la cantidad de "
  "trabajo que hay que repartir entre las ocho personas del equipo.")

doc.add_page_break()
doc.save('/tmp/_cost_a.docx'); print("A OK")
