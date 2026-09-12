# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
import rc257 as R
M, O, C = R.V2, R.ORIG, R.CORR
f = R.fnum

doc = nuevo()
portada(doc,
 "RUTA CRÍTICA DEL PROYECTO",
 "Simulación VR de batería con juego de ritmo",
 [("Versión del análisis","3.0"),
  ("Sustituye a","Versión 2.0 del 9 de septiembre de 2026"),
  ("Unidad de aprendizaje","Administración de Proyectos de Software"),
  ("Docente","Dra. Leticia Amalia Neira Tovar"),
  ("Equipo","Equipo A"),
  ("Técnica aplicada","Método de diagramación por precedencias (PDM / AON)"),
  ("Actividades analizadas","257"),
  ("Duración de la ruta crítica","38.25 días hábiles"),
  ("Límite por carga de trabajo","63.9 días hábiles"),
  ("Fecha","11 de septiembre de 2026")],
 sub2="Criterio de duración alineado con la hoja de control de tareas del equipo")

# ---------------------------------------------------------------- control
H(doc,"Control del documento",1)
table(doc,["Versión","Fecha","Base de cálculo","Criterio de duración","Duración"],[
 ("1.0","7 sep 2026","Lista de 257 tareas con las dependencias originalmente declaradas.","Rangos al valor mayor","45.25 días"),
 ("2.0","9 sep 2026","La misma lista, con los 38 cambios de dependencias del documento «Cambios de dependencias».","Rangos al valor mayor","45.25 días"),
 ("3.0","11 sep 2026","Sin cambios en la red. Se alinea el criterio de duración con la hoja de control de tareas que el equipo mantiene.","Rangos al valor menor",f"{M['TOTAL']:.2f} días"),
],widths=[1.4,1.8,6.4,3.2,2.2],fs=9)
P(doc,"El cambio de la versión 3.0 no toca la red: las 257 actividades y las 417 dependencias son las "
  "mismas. Lo que cambia es cómo se interpreta una duración expresada como rango. Hasta la versión 2.0 se "
  "tomaba el extremo superior, criterio conservador; a partir de esta versión se toma el inferior, que es "
  "el que emplea la hoja de control de tareas con la que el equipo hace el seguimiento diario.")
P(doc,"Solo 18 de las 257 actividades tienen duración expresada como rango, pero tres de ellas están sobre "
  "la ruta crítica, de modo que el efecto sobre la duración total es de siete días hábiles. El esfuerzo "
  "total baja de 2,146 a 1,978 horas, un 7.8 % menos, y el presupuesto se ajusta en consecuencia.")
P(doc,"Se adoptó el criterio del equipo y no el contrario para que exista una sola verdad: mantener dos "
  "cifras distintas de duración entre el análisis y la hoja de seguimiento garantizaba que tarde o "
  "temprano se tomara una decisión con el número equivocado.")
P(doc,"La versión 1.0 identificó que la red de dependencias no cerraba: noventa actividades no conducían a "
  "ningún entregable. El equipo corrigió ese defecto en la versión 2.0. Esta versión conserva esa red y solo "
  "ajusta el criterio de duración. El contraste entre la red original y la corregida está en la sección 12.")

doc.add_page_break()
# ================================================================ 1
H(doc,"1. Método empleado y justificación de su elección",1)
P(doc,"La ruta crítica es la trayectoria continua de actividades, desde el inicio hasta el fin del proyecto, "
  "cuya suma de duraciones es la mayor de todas las trayectorias posibles. Determina la duración mínima del "
  "proyecto: ninguna de las actividades que la componen admite retraso sin desplazar la fecha de terminación.")

H(doc,"1.1 Notación elegida",2)
P(doc,"Se emplea la diagramación por precedencias, en la que cada actividad es un nodo y las flechas "
  "expresan únicamente la relación de precedencia. La alternativa, actividad en la flecha, representa las "
  "actividades como flechas entre eventos numerados.")
P(doc,"La elección responde a dos razones concretas:")
bullets(doc,[
 "Las 257 tareas declaran dependencias puras de fin a inicio, sin traslapes ni demoras. Es exactamente lo "
 "que la diagramación por precedencias representa de forma directa.",
 "La notación de actividad en la flecha exigiría numerar más de 250 eventos y agregar decenas de actividades "
 "ficticias para resolver los casos en que dos actividades comparten el mismo par de eventos. El resultado "
 "sería ilegible sin aportar información adicional.",
],num=True)

H(doc,"1.2 Los cuatro tipos de dependencia",2)
table(doc,["Tipo","Significado","Uso en este proyecto"],[
 ("Fin → inicio (FS)","La sucesora no puede iniciar hasta que la predecesora termine.","Es el único tipo presente, tanto en las dependencias originales como en las 93 añadidas."),
 ("Inicio → inicio (SS)","La sucesora puede iniciar cuando la predecesora lleva cierto avance.","No se emplea. La lista de tareas no declara traslapes."),
 ("Fin → fin (FF)","Las dos actividades terminan juntas o con una demora entre sus finales.","No se emplea."),
 ("Inicio → fin (SF)","La sucesora no puede terminar hasta que la predecesora inicie.","No se emplea. En la práctica profesional se considera fuente de errores."),
],widths=[3.2,6.4,6.4],fs=9.5)
P(doc,"Que todas las dependencias sean de fin a inicio tiene una consecuencia que conviene anotar desde "
  "ahora: el cronograma resultante no admite ninguna compresión por traslape. Cada actividad espera a que su "
  "predecesora termine por completo. Es una de las razones por las que la duración crece al cerrar la red.")

H(doc,"1.3 Alcance de este documento",2)
P(doc,"El desarrollo cubre las etapas de planeación y programación del método: lista de actividades, matriz "
  "de tiempos, matriz de secuencias, matriz de información, red de precedencias, cálculo de tiempos próximos "
  "y remotos, red medida, matriz de elasticidad y determinación de la ruta crítica. Se incluye además la "
  "etapa de limitaciones de recursos, porque en este proyecto resulta ser la restricción determinante.")

doc.add_page_break()
# ================================================================ 2
H(doc,"2. Origen y preparación de los datos",1)
H(doc,"2.1 La lista de tareas",2)
P(doc,"El análisis se realiza sobre las 257 tareas definidas por el equipo en el documento de nomenclatura. "
  "Cada tarea trae clave, descripción, área, tiempo estimado y dependencia. No se agregó ni se eliminó "
  "ninguna tarea, ni se modificó ninguna duración.")

H(doc,"2.2 Sistema de claves",2)
P(doc,"Las claves se componen de dos letras y un número. La primera letra identifica el área y la segunda el "
  "grupo de actividades dentro de esa área. El número distingue las tareas del mismo grupo. Así, DG.3 es la "
  "tercera tarea del grupo de detección y procesamiento de golpes, dentro del área de desarrollo VR.")
table(doc,["Letra","Área","Responsable","Tareas","Carga"],
 [(R.SIGLA[a], a, R.RESP[a], R.NTAR[a], f"{R.CARGA[a]:.1f} d") for a in
  sorted(R.AREAS, key=lambda x: -R.CARGA[x])] +
 [("","Total","", sum(R.NTAR.values()), f"{sum(R.CARGA.values()):.1f} d")],
 widths=[1.4,5.6,3.0,2.2,2.4],fs=9.5)

H(doc,"2.3 Conversión de las estimaciones a días",2)
P(doc,"Las estimaciones vienen expresadas en horas o en días, y algunas como rango. Se aplicaron tres reglas, "
  "las mismas de la versión 1.0 del análisis y las mismas que empleó la estimación previa del equipo, de modo "
  "que todas las cifras sean comparables entre sí:")
table(doc,["Regla","Aplicación","Ejemplo"],[
 ("Ocho horas equivalen a un día hábil","Las tareas expresadas en horas se dividen entre ocho.","«5 horas» se convierte en 0.62 días"),
 ("Los rangos se toman en su valor mayor","Se adopta el extremo superior como estimación de trabajo.","«1 a 2 días» se convierte en 2 días"),
 ("Las tareas de seguimiento continuo se excluyen del cómputo","Una tarea sin duración acotada no puede formar parte de una trayectoria medible.","QC.1, «durante todo el proyecto», entra con duración cero"),
],widths=[4.6,7.0,4.4],fs=9.5)
P(doc,f"Suma aritmética de las 257 duraciones: {sum(R.T[k]['dur'] for k in R.ORD):.1f} días hábiles de "
  "trabajo. Este valor no cambió respecto de la versión 1.0, porque los cambios afectaron a las dependencias "
  "y no a las duraciones. Representa el esfuerzo total del proyecto, es decir la cantidad de trabajo que hay "
  "que repartir entre las ocho personas del equipo.")

H(doc,"2.4 Cambios de dependencias aplicados",2)
P(doc,"El 9 de septiembre el equipo emitió el documento «Cambios de dependencias — Simulación VR de "
  "batería», que corrige la red. Conviene precisar su naturaleza, porque no es una lista completa de "
  "actividades: contiene únicamente aquellas cuya dependencia debe modificarse, y las claves que indica se "
  "agregan a las dependencias ya declaradas en la lista original, sin sustituirlas.")
P(doc,f"El documento modifica {len(R.CAMBIOS)} actividades y agrega "
  f"{sum(len(v) for v in R.CAMBIOS.values())} dependencias nuevas.")

H(doc,"2.4.1 Validación de los cambios",3)
P(doc,"Antes de aplicarlos se verificó que fueran consistentes con la lista original:")
table(doc,["Comprobación","Resultado"],[
 ("Las 38 actividades destino existen en la lista de 257.","Se cumple. Ninguna clave desconocida."),
 ("Las 93 claves referenciadas como nuevas predecesoras existen en la lista de 257.","Se cumple. Ninguna referencia a clave inexistente."),
 ("Ninguna de las dependencias añadidas estaba ya declarada.","Se cumple. No hay duplicados."),
 ("La red resultante no contiene ciclos.","Se cumple. El ordenamiento topológico recorre las 257 actividades sin bloqueo."),
],widths=[10.4,5.6],fs=9.5)
P(doc,"El documento de cambios señala además que la referencia inexistente T3.24, que aparecía asociada a "
  "QI.4, ya no figura en la nomenclatura vigente. Se confirma: en la lista analizada QI.4 no contiene esa "
  "referencia.")

H(doc,"2.4.2 Los cambios, por área",3)
rows=[]
for a in R.AREAS:
    ks=[k for k in R.ORD if k in R.CAMBIOS and R.T[k]["area"]==a]
    for n,k in enumerate(ks):
        rows.append((R.SIGLA[a] if n==0 else "", k, R.T[k]["desc"][:60],
                     ", ".join(R.CAMBIOS[k]), len(R.CAMBIOS[k])))
table(doc,["Á.","Clave","Actividad","Dependencias agregadas","N.º"],rows,
      widths=[0.8,1.5,6.0,6.5,1.2],fs=8)
P(doc,"Los tres cambios de mayor efecto son los de QT.8, QI.4 y JI.5. QT.8, «Realizar pruebas con usuarios "
  "del prototipo integrado», pasa de tres a diecisiete predecesoras: ahora sí espera a que existan el juego "
  "de ritmo, el audio mezclado, la interfaz, el entorno optimizado y los cinco planes de prueba. Es el cambio "
  "que cierra la red.")

doc.add_page_break()
# ================================================================ 3
H(doc,"3. Matriz de tiempos",1)
P(doc,"Las 257 duraciones, en días hábiles, tras aplicar las reglas de conversión de la sección 2.3. Se "
  "conserva entre paréntesis la estimación original para poder verificar la conversión. Estas cifras son "
  "idénticas a las de la versión 1.0 del análisis.")
COLS = 3
mid = (len(R.ORD)+COLS-1)//COLS
part = [R.ORD[i*mid:(i+1)*mid] for i in range(COLS)]
rows = []
for i in range(mid):
    fila = []
    for c in range(COLS):
        if i < len(part[c]):
            k = part[c][i]; fila += [k, f(R.T[k]["dur"]), R.T[k]["durtxt"]]
        else: fila += ["", "", ""]
    rows.append(fila)
table(doc,["Clave","Días","Original"]*COLS, rows, widths=[1.5,1.0,2.8]*COLS, fs=7.5)

doc.add_page_break()
doc.save('/tmp/_v2_a.docx'); print("A OK")
