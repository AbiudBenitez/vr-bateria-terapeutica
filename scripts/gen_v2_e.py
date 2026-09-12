# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
from docx.shared import Cm
import rc257 as R
M, O = R.V2, R.ORIG
f = R.fnum
FIG = "/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/figuras257/"
doc = Document('/tmp/_v2_d.docx')

def alcanza(MM,i,fin):
    vis={i};p=[i]
    while p:
        k=p.pop()
        if k==fin: return True
        for s in MM["suc"].get(k,[]):
            if s not in vis: vis.add(s);p.append(s)
    return False

# ================================================================ 13
H(doc,"13. Observaciones sobre la red",1)
P(doc,"La red está bien formada y los cálculos son consistentes. Quedan tres observaciones que no alteran "
  "las cifras pero sí importan para el control del proyecto.")

H(doc,"13.1 Dos actividades no alimentan las pruebas con usuarios",2)
P(doc,"QT.8, «Realizar pruebas con usuarios del prototipo integrado», recibió catorce predecesoras nuevas. "
  "Dos actividades de cierre de rama quedaron fuera:")
table(doc,["Clave","Actividad","Área","Holgura total","¿Alcanza QT.8?"],[
 ("DR.2", R.T["DR.2"]["desc"], R.T["DR.2"]["area"], f"{M['HT']['DR.2']:.2f} d",
  "No. Llega al entregable final por otra vía."),
 ("MN.2", R.T["MN.2"]["desc"], R.T["MN.2"]["area"], f"{M['HT']['MN.2']:.2f} d",
  "No. Llega al entregable final por otra vía."),
],widths=[1.4,6.6,3.0,2.2,2.8],fs=9.5)
P(doc,"Significa que, tal como está declarada la red, se puede probar el prototipo integrado con usuarios "
  "sin que se hayan corregido los errores detectados en la primera prueba de la batería. Con las holguras "
  "actuales, de 15.4 y 13.0 días, la situación no se producirá salvo que esas ramas se retrasen mucho; "
  "agregar ambas dependencias no cambia la duración del proyecto en absoluto.")
P(doc,"Es una decisión del equipo, no un error de cálculo. Se documenta para que sea consciente: si se "
  "prefiere que las pruebas con usuarios esperen a la batería corregida, basta con agregar DR.2 a las "
  "predecesoras de QT.8 y la fecha final no se mueve.")

H(doc,"13.2 La cadena del entorno tridimensional creció",2)
P(doc,"Los cambios agregaron tres actividades a la cadena crítica del entorno: AA.4, revisar licencias de "
  "los assets; AD.1, añadir elementos ambientales secundarios; y AO.2, configurar niveles de detalle. La "
  "cadena pasa de catorce a diecisiete actividades seriales y de 20.25 a 19.25 días.")
P(doc,"Son dependencias correctas: no se puede componer el escenario con assets cuyas licencias no se han "
  "revisado, ni evaluar el rendimiento antes de configurar los niveles de detalle. Pero el efecto es que "
  "más de la mitad de la duración del proyecto está ahora en una sola cadena secuencial a cargo de una sola "
  "persona.")
P(doc,"Es el punto de mayor concentración de riesgo del cronograma. Un retraso de un día en cualquiera de "
  "esas diecisiete actividades desplaza la fecha final un día.")

H(doc,"13.3 Margen de calendario",2)
table(doc,["Concepto","Días hábiles"],[
 ("Del 7 de septiembre al 13 de noviembre de 2026, descontando el 16 de septiembre","49"),
 ("Duración de la ruta crítica, versión 2.0", f"{M['TOTAL']:.2f}"),
 ("Margen restante", f"{47-M['TOTAL']:.2f}"),
],widths=[11.0,5.0],fs=10)
P(doc,f"El margen es de {49-M['TOTAL']:.2f} días hábiles, alrededor de dos semanas. Conviene no leerlo como "
  "holgura cómoda: se reparte entre las 28 actividades de la cadena crítica, de modo que equivale a poco "
  "más de un tercio de día por actividad si los retrasos se distribuyeran de forma pareja.")
P(doc,"Conviene subrayar que este margen se calcula sobre la ruta crítica, que supone recursos ilimitados. "
  "La sección siguiente muestra que la restricción efectiva es otra y mucho más severa.")

doc.add_page_break()
# ================================================================ 14
H(doc,"14. Limitaciones de recursos",1)
P(doc,"El método de la ruta crítica calcula la duración suponiendo que hay tantos recursos como haga falta: "
  "si diez actividades pueden ejecutarse en paralelo, supone que hay diez personas para hacerlas. En este "
  "proyecto hay ocho personas y cada una tiene un área asignada, de modo que las actividades de una misma "
  "área no pueden ejecutarse en paralelo entre sí. Esta etapa del método ajusta el resultado a esa realidad.")
P(doc,"Los cambios de dependencias no modificaron ninguna duración, de modo que la carga de trabajo de cada "
  "persona es idéntica a la de la versión 1.0. Lo que cambió son las ventanas: al alargarse el proyecto, "
  "cada área dispone de algo más de tiempo.")

H(doc,"14.1 Carga de trabajo contra ventana disponible",2)
P(doc,"Para cada área se compara el trabajo que tiene asignado con el tiempo que el cronograma le concede, "
  "es decir el lapso entre el inicio más temprano de su primera actividad y el fin de su última.")
rows=[]
for a in sorted(R.AREAS, key=lambda x: -R.CARGA[x]):
    c, v, v1 = R.CARGA[a], R.VENTANA[a], R.VENTANA_V1[a]
    rows.append((a, R.RESP[a], R.NTAR[a], f"{c:.1f} d", f"{v1:.1f} d", f"{v:.1f} d",
                 f"{100*c/v:.0f} %", "Sobreasignado" if c > v else "Viable"))
table(doc,["Área","Responsable","Tareas","Carga","Ventana v1.0","Ventana v2.0","Ocupación","Situación"],rows,
      widths=[4.0,2.2,1.3,1.5,2.0,2.0,1.6,2.4],fs=8.5)
if os.path.exists(FIG+"Fig4_Carga_por_persona.png"):
    doc.add_picture(FIG+"Fig4_Carga_por_persona.png", width=Cm(16.2)); doc.paragraphs[-1].alignment=C
caption(doc,"Fig. 4 — Carga de trabajo por persona contra la ventana que le concede el cronograma.")
sob=[a for a in R.AREAS if R.CARGA[a]>R.VENTANA[a]]
P(doc,f"{len(sob)} de las ocho áreas están sobreasignadas. El caso extremo es QA, documentación y gestión, "
  f"con una ocupación del {100*R.CARGA['QA, documentación y gestión']/R.VENTANA['QA, documentación y gestión']:.0f} %.")
P(doc,"El caso de QA, documentación y gestión sigue siendo el más severo: 60 tareas que suman 63.9 días "
  "hábiles de trabajo dentro de una ventana de 45.2 días. Conviene señalar una causa concreta: la lista de "
  "áreas no asigna a nadie los roles de dirección, gerencia y coordinación, de modo que las tareas de "
  "planificación, gestión de riesgos, requisitos y seguimiento quedaron dentro de QA, sumadas a las de "
  "pruebas y documentación.")

H(doc,"14.2 Duración con recursos limitados",2)
P(doc,"Si cada persona ejecuta sus actividades una tras otra, la duración del proyecto no puede ser menor "
  "que la carga de la persona más ocupada. Ese es el límite inferior real.")
table(doc,["Criterio","Duración","Supuesto"],[
 ("Ruta crítica, versión 1.0", f"{O['TOTAL']:.2f} días","Recursos ilimitados, y 90 actividades que no llegaban al entregable."),
 ("Ruta crítica, versión 2.0", f"{M['TOTAL']:.2f} días","Recursos ilimitados, con la red cerrada."),
 ("Carga media por persona", f"{sum(R.CARGA.values())/8:.1f} días","Ocho personas, trabajo repartido de forma perfectamente equilibrada. No es alcanzable, porque cada área tiene su especialidad."),
 ("Carga de la persona más ocupada", f"{max(R.CARGA.values()):.1f} días","Ocho personas, una por área, cada una al 100 % de su jornada. Es el límite realista."),
],widths=[5.4,2.6,8.0],fs=9.5)
P(doc,f"La diferencia entre {M['TOTAL']:.2f} y {max(R.CARGA.values()):.1f} días no es un margen de error: son dos magnitudes que miden cosas "
  "distintas. La primera dice cuánto tarda la cadena de dependencias más larga. La segunda dice cuánto tarda "
  "la persona más cargada en hacer su trabajo. El proyecto no puede terminar antes de la mayor de las dos.")

H(doc,"14.3 Contraste con el calendario disponible",2)
table(doc,["Concepto","Días hábiles","¿Cabe?"],[
 ("Del 7 de septiembre al 13 de noviembre de 2026","49","—"),
 ("Ruta crítica, versión 2.0", f"{M['TOTAL']:.2f}", "Sí, con 10.75 días de margen"),
 ("Carga de QA, documentación y gestión", f"{max(R.CARGA.values()):.1f}", "No. Excede en 23.9 días"),
],widths=[8.0,3.4,4.6],fs=10)
P(doc,"El proyecto cabe en el calendario si se mide por la ruta crítica, y por muy poco. No cabe si se mide "
  "por la carga de trabajo. Como la segunda es la restricción efectiva, el proyecto tal como está repartido "
  "no termina antes del inicio de exámenes.")

H(doc,"14.4 Caminos para cerrar la brecha",2)
P(doc,"El desequilibrio se resuelve por alguno de estos caminos, o por una combinación. Se enuncian sin "
  "cuantificar, porque el reparto concreto es una decisión del equipo.")
table(doc,["Camino","Efecto sobre la brecha"],[
 ("Repartir entre las áreas las tareas de QA que no requieren especialidad, en particular documentación, evidencias y manuales, dejando en QA las pruebas y la gestión de errores.",
  "Es el de mayor efecto. QA concentra 63.9 de los 268.2 días de carga total del proyecto."),
 ("Asignar de forma explícita los roles de dirección, gerencia y coordinación, hoy no atribuidos a nadie.",
  "Saca de QA las tareas de planificación, riesgos, requisitos y seguimiento."),
 ("Acortar la cadena del entorno tridimensional permitiendo que algunas de sus diecisiete actividades se traslapen.",
  "Reduce la ruta crítica, no la carga total."),
 ("Apoyar al juego de ritmo, que está al 112 % de su ventana y sostiene la mecánica principal del producto.",
  "Reduce la carga de un área, sin efecto sobre la ruta crítica."),
 ("Reducir el alcance.",
  "Baja la carga total. Candidatos naturales: el modo libre, las pistas musicales adicionales y parte de la documentación no exigida por la asignatura."),
 ("Ampliar el plazo.",
  "No es viable. Los exámenes inician el 23 de noviembre."),
],widths=[9.4,6.6],fs=9)

doc.save('/tmp/_v2_e.docx'); print("E OK")
