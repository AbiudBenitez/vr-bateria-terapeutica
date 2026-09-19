# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import pmbok as PB
doc = Document('/tmp/_tarea_c.docx')

# procesos ejecutados en el proyecto del equipo
EJECUTADOS = {
 "4.1":"Acta constitutiva v3.0, con control de versiones y firmas de aprobación",
 "5.2":"Matriz de trazabilidad entre requisitos y funcionalidades, tarea QR.4",
 "5.4":"Estructura de desglose del trabajo: 42 paquetes en la primera versión, 257 actividades en la vigente",
 "6.2":"Lista de 257 actividades con clave, descripción, área y responsable",
 "6.3":"Red de precedencias con 417 dependencias de fin a inicio",
 "6.4":"Duración estimada de cada una de las 257 actividades",
 "6.5":"Cronograma de 38.25 días hábiles y ruta crítica de 28 actividades",
 "6.6":"Cronograma cargado en ProjectLibre con el avance real de las tareas cerradas",
 "7.1":"Plan de gestión de los costos: unidades, umbrales de control y regla de medición 0/100",
 "7.2":"Estimación ascendente sobre las 257 actividades, 1,978 horas",
 "7.3":"Presupuesto de $104,013 y reserva de cronograma de 10.75 días",
 "7.4":"Valor ganado al corte de medio curso: índice de desempeño del cronograma de 0.969",
 "8.1":"Plan de gestión de la calidad con métricas, umbrales y listas de verificación",
 "8.3":"Criterio de aceptación declarado para cada paquete de trabajo",
 "9.1":"Asignación de las ocho áreas a los ocho integrantes, con perfil y tarifa",
 "11.1":"Plan de gestión de los riesgos: escalas, matriz, umbrales y periodicidad",
 "11.2":"Registro de nueve riesgos identificados",
 "11.3":"Análisis cualitativo mediante matriz de probabilidad e impacto",
 "11.4":"Análisis cuantitativo: valor esperado de 9.15 días hábiles",
 "11.5":"Estrategia de respuesta, responsable y disparador para cada riesgo",
 "11.6":"Regla de activación y registro de ejecución de respuestas",
 "11.7":"Actividades de monitoreo, condiciones de cierre e indicadores de seguimiento",
 "13.1":"Identificación de partes interesadas en la sección 3 del acta constitutiva",
}
NOM = {n: nom for n,nom,a,g in PB.PROCESOS}
GR  = {n: g   for n,nom,a,g in PB.PROCESOS}

# ================================================================ 5
H(doc,"5. Resultados",1)
H(doc,"5.1 Hallazgos sobre la estructura del método",2)
P(doc,"El análisis de la estructura arrojó cinco hallazgos que no resultan evidentes al leer la lista de "
  "procesos.")
table(doc,["#","Hallazgo","Evidencia"],[
 ("1","El estándar concentra casi la mitad de su contenido en planificar.",
  "24 de 49 procesos pertenecen al grupo de planificación, frente a 10 de ejecución. La proporción expresa una postura: se considera más barato corregir un plan que rehacer un entregable."),
 ("2","Monitoreo y control no es una etapa, sino una actividad continua.",
  "Sus 12 procesos se ejecutan en paralelo a los demás grupos de principio a fin. Representarlo como una fase entre la ejecución y el cierre, que es el error habitual, deforma el modelo."),
 ("3","El encadenamiento entre procesos es el mecanismo que da coherencia al método.",
  "La salida de un proceso es casi siempre la entrada de otro. El acta de constitución, salida del primer proceso, aparece como entrada en la mayoría de los procesos de planificación."),
 ("4","El grupo de cierre tiene un solo proceso, y eso no lo hace menor.",
  "Cerrar el proyecto o fase concentra la aceptación formal, la transferencia del producto y el registro de lecciones aprendidas. Es concentrado, no marginal."),
 ("5","Las dos dimensiones del método son independientes entre sí.",
  "Un proceso pertenece a la vez a un grupo y a un área. Confundir ambas clasificaciones, por ejemplo tratar las áreas como etapas, impide leer correctamente la matriz."),
],widths=[0.8,5.2,10.0],fs=9.5)

H(doc,"5.2 Contraste con el proyecto de la unidad de aprendizaje",2)
P(doc,"Para verificar si la estructura teórica se corresponde con la práctica, se revisó la documentación "
  f"que el Equipo A ha producido y se ubicó cada entregable en el proceso del PMBOK que lo genera. Se "
  f"identificaron {len(EJECUTADOS)} de los 49 procesos.")
rows=[]
for g in PB.GRUPOS:
    ns = sorted([n for n in EJECUTADOS if GR[n]==g], key=lambda x:(int(x.split('.')[0]),int(x.split('.')[1])))
    for i,n in enumerate(ns):
        rows.append((g if i==0 else "", n, NOM[n], EJECUTADOS[n]))
table(doc,["Grupo","N.º","Proceso del PMBOK","Entregable producido por el equipo"],rows,
      widths=[2.4,1.0,4.6,8.0],fs=9)

from collections import Counter
cnt = Counter(GR[n] for n in EJECUTADOS)
table(doc,["Grupo de procesos","Ejecutados","Del total","Cobertura"],
 [(g, cnt.get(g,0), len(PB.de_grupo(g)), f"{100*cnt.get(g,0)/len(PB.de_grupo(g)):.0f} %") for g in PB.GRUPOS] +
 [("Total", len(EJECUTADOS), 49, f"{100*len(EJECUTADOS)/49:.0f} %")],
 widths=[5.0,3.0,3.0,3.0],fs=10)
P(doc,"La lectura del cuadro deja tres conclusiones. La primera es que la cobertura de planificación es "
  "alta, lo que resulta coherente con el momento del semestre: el proyecto está en su fase de ejecución "
  "temprana. La segunda es que el grupo de ejecución aparece con cobertura baja porque sus procesos se están "
  "ejecutando ahora mismo, no porque se hayan omitido. La tercera, y la más útil, es que hay áreas completas "
  "sin atender: comunicaciones y adquisiciones no tienen ningún proceso ejecutado.")
P(doc,"Esa ausencia no es casual. La gestión de las adquisiciones carece de procesos ejecutados porque el "
  "proyecto no realiza compras: el equipo lo prestó la Facultad y los recursos gráficos y sonoros se "
  "obtienen con licencias libres. En cambio, la ausencia de la gestión de las comunicaciones sí constituye "
  "una omisión real: el equipo no ha elaborado un plan de comunicaciones, y con ocho integrantes en áreas "
  "distintas es una carencia que conviene subsanar.")

H(doc,"5.3 Análisis de las fuentes consultadas",2)
P(doc,"Se evaluó en qué medida cada fuente contribuyó a resolver la actividad.")
table(doc,["Fuente","Aportación","Limitación observada"],[
 ("Guía del PMBOK, sexta edición, del Project Management Institute",
  "Fuente primaria. De ella provienen la clasificación en grupos y áreas, los 49 procesos y la descripción de entradas, herramientas y salidas de cada uno.",
  "Su extensión dificulta obtener una visión de conjunto: describe cada proceso con detalle pero no ofrece una síntesis por grupo como la que esta actividad solicita, que hubo que construir."),
 ("Guía del PMBOK, séptima y octava ediciones",
  "Permitieron establecer el estado vigente del estándar y explicar por qué la actividad se estructura sobre la sexta edición.",
  "Al abandonar el enfoque de procesos, la séptima no aporta entradas ni salidas. Sirvió como contexto, no como contenido."),
 ("Material del curso: presentación «Administración de Proyectos, Parte IV»",
  "Aportó la distinción entre proyecto y trabajo operativo, y entre alcance del producto y alcance del proyecto. También la afirmación de que la estructura de desglose del trabajo es la base de toda la planificación, que se verificó en la matriz.",
  "Cubre solo algunos procesos, principalmente de alcance y cronograma. No abarca las diez áreas."),
 ("Documentación del proyecto del Equipo A",
  "Fue la fuente decisiva para la sección 5.2. Permitió pasar de describir el estándar a comprobar su aplicación, y detectar la ausencia del plan de comunicaciones.",
  "Es una sola experiencia y no permite generalizar. Lo observado vale para este proyecto."),
 ("Sitio oficial del Project Management Institute y publicaciones sobre la octava edición",
  "Confirmaron la fecha de publicación de la octava edición, el 13 de enero de 2026, y su estructura de seis principios y siete dominios.",
  "Buena parte del material disponible es de divulgación comercial de centros de capacitación, no del propio instituto. Se contrastaron varias fuentes antes de dar los datos por buenos."),
],widths=[4.0,6.4,5.6],fs=9)
P(doc,"La combinación que resultó más productiva fue la de la fuente primaria con la documentación propia "
  "del proyecto. La guía por sí sola permite describir; el contraste con el proyecto permite verificar, que "
  "es donde aparecieron los hallazgos que no estaban en ningún texto, como la ausencia del plan de "
  "comunicaciones.")

doc.add_page_break()
doc.save('/tmp/_tarea_d.docx'); print("D OK")
