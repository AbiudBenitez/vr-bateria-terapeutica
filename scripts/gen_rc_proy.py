# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx.shared import Cm
import pdm

FIG="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/superados/figuras-cronograma-42-paquetes/"
TIPO={"FS":"Fin → inicio","SS":"Inicio → inicio","FF":"Fin → fin"}

# justificacion de cada dependencia
JUST={
("A",None):"Actividad inicial. No depende de nada.",
("C","D"):"El asesor no puede confirmarse antes de haber definido el perfil que se busca.",
("D","E"):"Las rutinas las diseña el asesor; no existen antes de su incorporación.",
("B","E"):"El diseño de rutinas parte de los protocolos identificados en la investigación de musicoterapia.",
("E","F"):"Las métricas miden el desempeño en las rutinas. Se pueden definir cuando las primeras rutinas ya están esbozadas, sin esperar a que se validen todas.",
("F","G"):"El protocolo de sesión indica qué se mide y cómo; requiere las métricas ya definidas.",
("H","I"):"No se modela sin referencias visuales aprobadas.",
("H","J"):"Misma razón. Se ejecuta en paralelo con el modelado de la batería por ser un responsable distinto.",
("I","K"):"El texturizado puede empezar sobre las piezas ya modeladas, sin esperar a que la batería completa esté terminada.",
("J","K"):"Igual que la anterior, respecto de baquetas y entorno.",
("K","L"):"La optimización de geometría puede comenzar sobre las piezas ya texturizadas.",
("M","N"):"No se puede medir la latencia sin el proyecto y el kit de desarrollo configurados.",
("N","O"):"Dependencia estricta. El resultado del hito Go / No-Go condiciona todo el desarrollo posterior; no se avanza hasta tenerlo.",
("O","P"):"La detección de colisiones puede programarse cuando el esquema de control ya está definido, sin esperar al ajuste fino del mapeo.",
("P","Q"):"La medición de velocidad se apoya en el evento de colisión, que ya existe a la mitad de esa actividad.",
("Q","R"):"La integración con modelos requiere el sistema de impacto completo.",
("L","R"):"La integración requiere la geometría ya optimizada para el visor.",
("R","S"):"La ergonomía se evalúa sobre la escena ya integrada.",
("N","T"):"La librería de muestras se selecciona una vez conocido el presupuesto de latencia disponible.",
("Q","U"):"El audio se dispara a partir del evento de impacto con su velocidad.",
("T","U"):"La integración requiere la librería de muestras terminada.",
("U","V"):"Las rutinas se implementan sobre el sistema de audio, que ya responde parcialmente.",
("E","V"):"Las rutinas implementadas son las validadas por el asesor.",
("R","W"):"La interfaz se construye sobre el esquema de interacción ya integrado.",
("S","W"):"Las decisiones de ergonomía condicionan la colocación de los menús; ambas actividades se trabajan juntas.",
("F","W"):"El módulo de registro implementa exactamente las métricas definidas.",
("V","X"):"La build integra las rutinas terminadas.",
("W","X"):"La build integra la interfaz terminada.",
("S","X"):"La build incorpora los ajustes de ergonomía.",
("W","Y-1"):"El plan de pruebas se redacta sobre la interfaz ya definida; no requiere esperar a que esté terminada.",
("F","Y-1"):"Los casos de prueba verifican las métricas definidas.",
("X","Y-2"):"Las pruebas de rendimiento se ejecutan sobre versiones intermedias durante la integración. La build candidata congela el resultado, no lo condiciona.",
("Y-1","Y-2"):"No se ejecutan pruebas sin casos definidos.",
("Y-2","Z"):"Las pruebas con usuarios se hacen sobre una versión que ya pasó las pruebas técnicas.",
("G","Z"):"Las pruebas con usuarios requieren el protocolo y el consentimiento informado aprobados.",
}
def just(p,k): return JUST.get((p,k),"—")

doc = nuevo()
portada(doc,
 "RUTA CRÍTICA DEL PROYECTO",
 "Simulación de batería en realidad virtual\ncon enfoque de musicoterapia",
 [("Unidad de aprendizaje","Administración de Proyectos de Software"),
  ("Docente","Dra. Leticia Amalia Neira Tovar"),
  ("Equipo","Equipo A"),
  ("Técnica aplicada","Método de diagramación por precedencias (PDM / AON)"),
  ("Duración de la red","50 días hábiles"),
  ("Periodo","1 de septiembre al 10 de noviembre de 2026"),
  ("Documento base del proyecto","Acta constitutiva v3.0"),
  ("Fecha","3 de septiembre de 2026")],
 sub2="Desarrollo completo con justificación de cada decisión")

# ================================================================ 1
H(doc,"1. Método empleado y justificación de su elección",1)
P(doc,"La ruta crítica es la trayectoria continua de actividades, desde el inicio hasta el fin del proyecto, "
  "cuya suma de duraciones es la mayor de todas las trayectorias posibles. Determina la duración mínima del "
  "proyecto: ninguna de las actividades que la componen admite retraso sin desplazar la fecha de terminación.")

H(doc,"1.1 Por qué diagramación por precedencias y no actividad en la flecha",2)
P(doc,"Existen dos notaciones para representar la red de un proyecto:")
table(doc,["Notación","Cómo representa","Tipos de dependencia","Elementos auxiliares"],[
 ("Actividad en la flecha (AOA)","La actividad es una flecha; los nodos son eventos, es decir instantes en el tiempo.","Solo fin → inicio.","Requiere actividades ficticias de duración cero para expresar precedencias que no se pueden dibujar de otro modo."),
 ("Actividad en el nodo (AON o PDM)","La actividad es un nodo; las flechas expresan únicamente la relación de precedencia.","Fin → inicio, fin → fin, inicio → inicio e inicio → fin. Esta última no se utiliza en la práctica.","No requiere actividades ficticias."),
],widths=[3.4,4.6,3.4,4.6],fs=9.5)

P(doc,"Se eligió la diagramación por precedencias por una razón concreta y verificable. El cronograma de este "
  "proyecto contiene actividades que arrancan antes de que termine la actividad de la que dependen. El "
  "texturizado, por ejemplo, comienza cuando el modelado de la batería lleva una semana de avance: no hace "
  "falta que el instrumento esté completo para empezar a texturizar las piezas ya modeladas.")
P(doc,"En la notación de actividad en la flecha ese traslape no se puede representar, porque solo admite la "
  "relación fin → inicio. Al modelar el proyecto en esa notación la red arroja 70 días hábiles, mientras que "
  "el cronograma comprometido son 53. La diferencia de 20 días no es un error del cronograma: es una "
  "limitación de la notación.")
P(doc,"La diagramación por precedencias representa esos traslapes de forma directa mediante relaciones "
  "inicio → inicio con demora, y produce una red de 50 días hábiles que sí corresponde al cronograma real. "
  "Por eso es la notación adecuada para este proyecto.")

H(doc,"1.2 Los cuatro tipos de dependencia",2)
table(doc,["Tipo","Significado","Uso en este proyecto"],[
 ("Fin → inicio (FS)","La actividad sucesora no puede iniciar hasta que la predecesora termine.","Es la relación predominante. Se usa en 24 de las 35 dependencias de la red."),
 ("Inicio → inicio (SS)","La sucesora puede iniciar cuando la predecesora lleva cierto avance, expresado como demora en días.","Se usa en 11 dependencias, siempre entre actividades que comparten responsable o cuyo producto es parcialmente utilizable antes de estar terminado."),
 ("Fin → fin (FF)","Las dos actividades deben terminar juntas o con una demora entre sus finales.","No se utiliza en esta red."),
 ("Inicio → fin (SF)","La sucesora no puede terminar hasta que la predecesora inicie.","No se utiliza. Es una relación que en la práctica profesional se considera fuente de errores."),
],widths=[3.4,6.6,6.0],fs=9.5)

H(doc,"1.3 Alcance de este documento",2)
P(doc,"El desarrollo cubre las etapas de planeación y programación del método: lista de actividades, matriz "
  "de secuencias, matriz de tiempos, matriz de información, red de precedencias, cálculo de tiempos próximos "
  "y remotos, red medida, matriz de elasticidad y determinación de la ruta crítica. Las etapas de costos y "
  "pendientes, compresión por costo y limitaciones de recursos quedan fuera: el presupuesto se administra en "
  "el acta constitutiva y el proyecto no tiene margen para adelantar la fecha de terminación pagando más.")

doc.add_page_break()
# ================================================================ 2
H(doc,"2. De la estructura de desglose del trabajo a la lista de actividades",1)
P(doc,"La estructura de desglose del trabajo del acta constitutiva contiene 42 paquetes de trabajo "
  "organizados en siete ramas. La estructura de desglose describe qué se produce, pero no establece "
  "secuencia alguna entre sus componentes: esa es precisamente la diferencia entre la estructura de desglose "
  "y la red de actividades.")

H(doc,"2.1 Criterio de consolidación",2)
P(doc,"Una red de 42 nodos es ilegible en una hoja y no aporta precisión adicional, porque varios paquetes de "
  "una misma rama son estrictamente secuenciales, comparten responsable y no admiten traslape entre sí. Se "
  "consolidaron en 27 actividades aplicando dos condiciones que deben cumplirse simultáneamente:")
bullets(doc,[
 "Los paquetes agrupados tienen el mismo responsable.",
 "Los paquetes agrupados guardan entre sí una relación fin → inicio obligada, es decir, no pueden traslaparse "
 "ni reordenarse.",
],num=True)
P(doc,"Cuando alguna de las dos condiciones no se cumple, los paquetes se mantienen como actividades "
  "separadas. Por eso los paquetes 3.2 y 3.3, que antes se ejecutaban en secuencia, aparecen aquí como las "
  "actividades I y J: se reasignaron a responsables distintos y ahora corren en paralelo.")
P(doc,"Cada actividad conserva la referencia a los paquetes que la componen, de modo que la trazabilidad con "
  "la estructura de desglose se mantiene en ambos sentidos.")

H(doc,"2.2 Tratamiento de los hitos",2)
P(doc,"Los seis hitos del acta no son actividades: no consumen tiempo ni recursos. En la diagramación por "
  "precedencias no se representan como nodos de la red, sino como puntos de verificación asociados a la "
  "terminación de una actividad. Se listan en la sección 12.")

H(doc,"2.3 Lista de actividades",2)
rows=[(k, pdm.NOM[k], pdm.PAQ[k], pdm.RES[k]) for k in pdm.ORD]
table(doc,["Clave","Actividad","Paquetes de la EDT","Responsable"],rows,
      widths=[1.5,6.6,3.3,4.6],fs=9)
P(doc,"Las claves Y-1 y Y-2 corresponden a la rama de pruebas. Se mantienen separadas porque el plan de "
  "pruebas se redacta antes de que exista la versión a probar, mientras que la ejecución de las pruebas "
  "requiere esa versión: agruparlas ocultaría un traslape real de cinco días.")

doc.add_page_break()
# ================================================================ 3
H(doc,"3. Matriz de secuencias",1)
P(doc,"La matriz de secuencias establece, para cada actividad, de cuáles depende, con qué tipo de "
  "dependencia y con qué demora. Es el insumo del que se deriva toda la red. Cada renglón incluye la razón "
  "por la que la dependencia existe, porque una dependencia sin justificación no es verificable y suele "
  "esconder una restricción de recursos disfrazada de restricción lógica.")
rows=[]
for k in pdm.ORD:
    if not pdm.PRE[k]:
        rows.append((k,"—","—","—","Actividad inicial. Puede comenzar el primer día del proyecto."))
    else:
        for n,(p,t,l) in enumerate(pdm.PRE[k]):
            rows.append((k if n==0 else "", p, TIPO[t], str(l) if l else "0", just(p,k)))
table(doc,["Clave","Predecesora","Tipo","Demora","Justificación de la dependencia"],rows,
      widths=[1.3,1.7,2.3,1.3,9.4],fs=8.5)

H(doc,"3.1 Sobre las demoras",2)
P(doc,"Todas las demoras de las relaciones inicio → inicio valen cinco días hábiles, salvo dos que valen "
  "cero. El valor de cinco días corresponde a una semana laboral y responde a un criterio uniforme: se "
  "considera que una actividad de diez días entrega producto parcialmente utilizable a la mitad de su "
  "ejecución. No se emplearon demoras ajustadas actividad por actividad porque no existe base empírica para "
  "afinarlas y hacerlo daría una falsa apariencia de precisión.")
P(doc,"Las dos demoras de valor cero, en las relaciones S → W y X → Y-2, indican actividades que arrancan el "
  "mismo día que su predecesora y avanzan en paralelo de principio a fin.")

doc.add_page_break()
# ================================================================ 4
H(doc,"4. Matriz de tiempos",1)
P(doc,"Las duraciones se expresan en días hábiles, sobre un calendario de lunes a viernes. El 16 de "
  "septiembre de 2026 es inhábil y está descontado. No se emplearon las tres estimaciones de la técnica de "
  "evaluación y revisión de programas, porque las duraciones provienen del cronograma ya acordado en el acta "
  "constitutiva y no de una estimación con incertidumbre: el tratamiento corresponde al método de la ruta "
  "crítica, con una estimación única por actividad.")
mid=(len(pdm.ORD)+1)//2
izq=pdm.ORD[:mid]; der=pdm.ORD[mid:]
rows=[]
for i in range(mid):
    a=izq[i]
    if i<len(der):
        b=der[i]; rows.append((a,pdm.DUR[a],b,pdm.DUR[b]))
    else:
        rows.append((a,pdm.DUR[a],"",""))
table(doc,["Clave","Días hábiles","Clave","Días hábiles"],rows,widths=[3.2,4.2,3.2,4.2],fs=10)
P(doc,f"Suma aritmética de las duraciones: {sum(pdm.DUR.values())} días hábiles. Este valor no es la duración "
  "del proyecto. La mayoría de las actividades se ejecutan en paralelo, de modo que la duración real es la de "
  "la trayectoria más larga de la red, que se obtiene en la sección 8.")

doc.add_page_break()
# ================================================================ 5
H(doc,"5. Matriz de información",1)
P(doc,"La matriz de información consolida en un solo cuadro la lista de actividades, sus secuencias y sus "
  "tiempos. Es el insumo directo para dibujar la red: cada renglón se convierte en un nodo, y las columnas de "
  "predecesoras y sucesoras indican qué flechas lo conectan.")
rows=[]
for k in pdm.ORD:
    pre=", ".join(f"{p} ({t}{'+'+str(l) if l else ''})" for p,t,l in pdm.PRE[k]) or "—"
    suc=", ".join(s for s,_,_ in pdm.SUC[k]) or "— (fin)"
    rows.append((k, pdm.PAQ[k], pdm.DUR[k], pre, suc))
table(doc,["Clave","Paquetes EDT","Días","Predecesoras (tipo y demora)","Sucesoras"],rows,
      widths=[1.3,2.6,1.2,6.5,4.4],fs=8.5)
P(doc,"Se verificó que la matriz sea consistente en ambos sentidos: toda actividad que aparece como "
  "predecesora de otra tiene a esa otra registrada entre sus sucesoras. Cinco actividades no tienen "
  "predecesora (A, B, C, H y M) y son los puntos de arranque del proyecto; una sola actividad no tiene "
  "sucesora (Z) y es el cierre.")

doc.add_page_break()
# ================================================================ 6 (horizontal)
landscape(doc)
H(doc,"6. Red de precedencias",1)
P(doc,"Cada nodo es una actividad; cada flecha es una relación de precedencia. Las flechas continuas "
  "representan relaciones fin → inicio y las punteadas relaciones inicio → inicio, con su demora indicada. "
  "Las actividades se disponen de izquierda a derecha en orden de tiempo próximo de iniciación, y por "
  "carriles horizontales según la rama de la estructura de desglose a la que pertenecen.",size=9.5)
if os.path.exists(FIG+"Fig1_Red_PDM.png"):
    doc.add_picture(FIG+"Fig1_Red_PDM.png", width=Cm(25.4)); doc.paragraphs[-1].alignment=C
caption(doc,"Fig. 1 — Red de precedencias del proyecto. 27 actividades, 35 dependencias.")
P(doc,"La red muestra con claridad la estructura del proyecto: cinco actividades arrancan simultáneamente el "
  "primer día, el trabajo se abre en cuatro ramas que avanzan en paralelo durante la mayor parte del "
  "periodo, y todas convergen en la actividad X, la build candidata, de la que dependen las pruebas y el "
  "cierre.",size=9.5)

portrait(doc)
# ================================================================ 7
H(doc,"7. Asignación de duraciones y cálculo de tiempos próximos",1)
P(doc,"El recorrido hacia adelante calcula, para cada actividad, lo más pronto que puede iniciar y "
  "terminar. Se parte del día cero y se avanza siguiendo el orden de la red.")
H(doc,"7.1 Reglas de cálculo",2)
P(doc,"El tiempo próximo de iniciación de una actividad es el mayor de los valores que le imponen sus "
  "predecesoras. Cada tipo de dependencia impone un valor distinto:")
table(doc,["Tipo de dependencia","Valor que impone al tiempo próximo de iniciación"],[
 ("Fin → inicio con demora d","Tiempo próximo de terminación de la predecesora, más d."),
 ("Inicio → inicio con demora d","Tiempo próximo de iniciación de la predecesora, más d."),
 ("Fin → fin con demora d","Tiempo próximo de terminación de la predecesora, más d, menos la duración de la sucesora."),
],widths=[5.6,10.4],fs=9.5)
P(doc,"El tiempo próximo de terminación es el tiempo próximo de iniciación más la duración. Las actividades "
  "sin predecesora inician en el día cero. La duración del proyecto es el mayor tiempo próximo de "
  "terminación de la red.")
H(doc,"7.2 Resultado",2)
rows=[(k,pdm.DUR[k],pdm.ES[k],pdm.EF[k],str(pdm.dia(pdm.ES[k])),str(pdm.dia(pdm.EF[k]-1))) for k in pdm.ORD]
table(doc,["Clave","Duración","Tiempo próximo de iniciación","Tiempo próximo de terminación","Fecha de inicio","Fecha de fin"],
      rows,widths=[1.6,2.0,3.2,3.4,3.0,3.0],fs=9)
P(doc,f"El mayor tiempo próximo de terminación es {pdm.TOTAL}, correspondiente a la actividad Z. "
  f"La duración del proyecto es de {pdm.TOTAL} días hábiles, del 1 de septiembre al 10 de noviembre de 2026.")

# ================================================================ 8
H(doc,"8. Cálculo de tiempos remotos",1)
P(doc,"El recorrido hacia atrás calcula, para cada actividad, lo más tarde que puede iniciar y terminar sin "
  "desplazar la fecha final del proyecto. Se parte del último día y se retrocede.")
table(doc,["Tipo de dependencia","Valor que impone al tiempo remoto de terminación"],[
 ("Fin → inicio con demora d","Tiempo remoto de iniciación de la sucesora, menos d."),
 ("Inicio → inicio con demora d","Tiempo remoto de iniciación de la sucesora, menos d, más la duración de la predecesora."),
 ("Fin → fin con demora d","Tiempo remoto de terminación de la sucesora, menos d."),
],widths=[5.6,10.4],fs=9.5)
P(doc,"El tiempo remoto de terminación de una actividad es el menor de los valores que le imponen sus "
  "sucesoras. El tiempo remoto de iniciación es el remoto de terminación menos la duración. Las actividades "
  "sin sucesora terminan en el día 50, la fecha final del proyecto.")
rows=[(k,pdm.DUR[k],pdm.LS[k],pdm.LF[k]) for k in pdm.ORD]
table(doc,["Clave","Duración","Tiempo remoto de iniciación","Tiempo remoto de terminación"],rows,
      widths=[2.4,2.6,5.5,5.5],fs=9)

doc.add_page_break()
# ================================================================ 9 (horizontal)
landscape(doc)
H(doc,"9. Red medida",1)
P(doc,"La red medida es la misma red de precedencias con los tiempos calculados incorporados a cada nodo. "
  "La banda superior de cada caja contiene, de izquierda a derecha, el tiempo próximo de iniciación, la "
  "duración y el tiempo próximo de terminación. La banda inferior contiene el tiempo remoto de iniciación, "
  "la holgura total y el tiempo remoto de terminación. Las cajas y flechas resaltadas forman la ruta "
  "crítica.",size=9.5)
if os.path.exists(FIG+"Fig2_Red_Medida_Ruta_Critica.png"):
    doc.add_picture(FIG+"Fig2_Red_Medida_Ruta_Critica.png", width=Cm(25.4)); doc.paragraphs[-1].alignment=C
caption(doc,"Fig. 2 — Red medida con la ruta crítica resaltada. Duración: 50 días hábiles.")

portrait(doc)
# ================================================================ 10
H(doc,"10. Matriz de elasticidad",1)
P(doc,"La matriz de elasticidad reúne los cuatro tipos de holgura de cada actividad. La holgura es el margen "
  "de retraso disponible, y cada tipo responde a una pregunta distinta.")
table(doc,["Holgura","Fórmula","Qué responde"],[
 ("Total","Tiempo remoto de iniciación menos tiempo próximo de iniciación.","Cuánto puede retrasarse la actividad sin mover la fecha final del proyecto."),
 ("Libre","Menor tiempo próximo de iniciación de las sucesoras, menos el tiempo próximo de terminación de la actividad.","Cuánto puede retrasarse sin afectar el inicio más temprano de ninguna actividad siguiente."),
 ("Interferente","Holgura total menos holgura libre.","Qué parte del margen, si se consume, reduce el margen de las actividades posteriores."),
 ("Independiente","Menor tiempo próximo de iniciación de las sucesoras, menos el mayor tiempo remoto de terminación de las predecesoras, menos la duración. Si resulta negativa se toma cero.","Cuánto puede retrasarse sin afectar ni a las predecesoras ni a las sucesoras, en el peor escenario."),
],widths=[2.4,6.8,6.8],fs=9)
rows=[]
for k in pdm.ORD:
    cr="Sí" if pdm.HT[k]==0 else ""
    rows.append((k,pdm.DUR[k],pdm.ES[k],pdm.EF[k],pdm.LS[k],pdm.LF[k],
                 pdm.HT[k],pdm.HL[k],pdm.HI[k],pdm.HIND[k],cr))
table(doc,["Clave","Dur.","TPI","TPT","TRI","TRT","H. total","H. libre","H. interf.","H. indep.","Crítica"],
      rows,widths=[1.4,1.1,1.1,1.1,1.1,1.1,1.5,1.5,1.5,1.5,1.5],fs=8.5)
P(doc,"Nota de lectura: TPI y TPT son los tiempos próximos de iniciación y terminación; TRI y TRT los "
  "remotos. Todos los valores están en días hábiles contados desde el día cero, que corresponde al 1 de "
  "septiembre de 2026.")

doc.add_page_break()
# ================================================================ 11
H(doc,"11. Ruta crítica",1)
H(doc,"11.1 Criterio de identificación",2)
P(doc,"Una actividad es crítica cuando cumple estas condiciones, que son equivalentes entre sí:")
bullets(doc,["Su tiempo próximo de iniciación es igual a su tiempo remoto de iniciación.",
             "Su tiempo próximo de terminación es igual a su tiempo remoto de terminación.",
             "Su holgura total es cero.",
             "Sus cuatro holguras son cero."],num=True)
P(doc,"Se verificaron las cuatro condiciones para cada actividad de la red. Las quince actividades marcadas "
  "en la matriz de elasticidad las cumplen todas.")

H(doc,"11.2 Resultado: dos rutas críticas",2)
P(doc,"La red tiene dos trayectorias críticas, no una. Ambas parten de la misma actividad, se separan tras "
  "el hito de latencia y vuelven a converger en la build candidata. Las dos miden 50 días hábiles.")
table(doc,["Ruta","Trayectoria","Rama de la EDT"],[
 ("Ruta crítica 1","M → N → O → P → Q → R → S → W → X → Y-2 → Z",
  "Configuración e interacción (rama 4), interfaz (rama 6) y pruebas (rama 7)."),
 ("Ruta crítica 2","M → N → T → U → V → X → Y-2 → Z",
  "Configuración (rama 4), audio y rutinas (rama 5) y pruebas (rama 7)."),
],widths=[3.0,7.6,5.4],fs=9.5)
P(doc,"Que existan dos rutas críticas duplica la exposición del proyecto: un retraso en cualquiera de las "
  "dos ramas desplaza la fecha final por igual. En términos de control, obliga a vigilar la rama de audio "
  "con la misma atención que la de interacción, aunque tenga menos actividades.")
P(doc,"El tramo M → N es común a ambas rutas. Son la configuración del entorno de desarrollo y el spike de "
  "latencia: diez días hábiles de los que depende absolutamente todo el trabajo técnico posterior. Es el "
  "tramo más sensible del proyecto.")

H(doc,"11.3 Verificación aritmética",2)
P(doc,"La suma de las duraciones a lo largo de la ruta crítica 1, descontando los traslapes de las "
  "relaciones inicio → inicio, debe dar exactamente la duración de la red:")
table(doc,["Actividad","Duración","Traslape aplicado","Aporte a la ruta"],[
 ("M  Configuración de Unity y SDK","5","—","5"),
 ("N  Spike de latencia","5","—","5"),
 ("O  Mapeo de controles","10","—","10"),
 ("P  Detección de colisiones","10","Inicia 5 días tras el inicio de O","5"),
 ("Q  Medición de velocidad de impacto","5","Inicia 5 días tras el inicio de P","5"),
 ("R  Integración de modelos con físicas","5","—","5"),
 ("S  Ergonomía","5","—","5"),
 ("W  Menús, interfaz y registro de métricas","10","Inicia junto con S","10"),
 ("X  Build candidata","5","—","5"),
 ("Y-2  Pruebas de rendimiento y latencia","5","Inicia junto con X","0"),
 ("Z  Pruebas con usuarios y cierre","5","—","5"),
 ("Total","","","50 días hábiles"),
],widths=[6.4,2.0,4.4,3.2],fs=9)
P(doc,"El resultado coincide con la duración obtenida en el recorrido hacia adelante, lo que confirma que "
  "los cálculos son consistentes.")

H(doc,"11.4 Actividades cuasi-críticas",2)
P(doc,"La rama del modelo tridimensional (actividades H, I, J, K y L) tiene holgura total de un solo día. "
  "Formalmente no es crítica, pero un día de margen sobre una cadena de 24 días hábiles es despreciable: "
  "cualquier contratiempo la convierte en crítica. Debe controlarse con el mismo rigor que las dos rutas "
  "críticas.")
P(doc,"Conviene señalar de dónde viene esa holgura de un día. En la versión anterior del cronograma esta "
  "rama era la ruta crítica del proyecto, con holgura cero, porque el modelado de la batería y el de "
  "baquetas y entorno se ejecutaban en secuencia bajo un mismo responsable. Al reasignar el paquete 3.3 al "
  "diseñador de interacción y adelantar el diseño conceptual a la primera semana, la cadena se acortó y la "
  "criticidad se desplazó a la rama de interacción.")

doc.add_page_break()
# ================================================================ 12
H(doc,"12. Análisis de la programación",1)

H(doc,"12.1 Trabajo simultáneo",2)
P(doc,"La red identifica con precisión qué actividades pueden ejecutarse al mismo tiempo. El cuadro "
  "siguiente recorre el proyecto por tramos y señala los frentes activos en cada uno.")
table(doc,["Tramo","Frentes simultáneos","Por qué son independientes"],[
 ("Días 0 – 4","A, B, C, H, M","Cinco actividades sin predecesora: gestión, investigación de musicoterapia, gestión del asesor, diseño conceptual y configuración del entorno de desarrollo. No comparten insumo ni responsable."),
 ("Días 4 – 10","I y J (modelado), D (asesor), N (latencia)","El modelado avanza en dos frentes con responsables distintos mientras se confirma al asesor y se verifica la latencia."),
 ("Días 10 – 25","K, L (arte), O, P, Q (interacción), T (audio), E, F (terapia)","Punto de máximo paralelismo: cuatro ramas activas a la vez, con siete actividades en curso."),
 ("Días 25 – 35","R, S (integración), U (audio), G (protocolo)","La integración de modelos con físicas corre junto a la integración de audio y a la preparación del protocolo de sesión."),
 ("Días 30 – 40","V (rutinas), W (interfaz), Y-1 (plan de pruebas)","Tres frentes que convergen en la build candidata."),
 ("Días 40 – 45","X (build) y Y-2 (pruebas de rendimiento)","Las pruebas técnicas se ejecutan sobre versiones intermedias mientras se cierra la integración."),
 ("Días 45 – 50","Z","Cierre. Sin paralelismo."),
],widths=[2.4,4.8,8.8],fs=9)

H(doc,"12.2 Compresión de la red",2)
P(doc,"El proyecto está comprimido por traslape. La magnitud de la compresión se obtiene comparando la red "
  "con y sin las relaciones inicio → inicio:")
table(doc,["Escenario","Duración","Diferencia"],[
 ("Red con todas las dependencias como fin → inicio","70 días hábiles","—"),
 ("Red con los traslapes aplicados","50 días hábiles","20 días hábiles menos"),
 ("Ventana disponible: 1 de septiembre al 13 de noviembre","53 días hábiles","3 días hábiles de margen"),
],widths=[8.6,3.6,3.8],fs=9.5)
P(doc,"Sin la compresión el proyecto terminaría 17 días hábiles después del cierre del periodo, ya iniciados "
  "los exámenes. La compresión no es opcional: es la condición para que el proyecto quepa en el semestre.")
P(doc,"El traslape se aplicó únicamente donde es defendible, es decir, entre actividades cuyo producto es "
  "parcialmente utilizable antes de estar terminado, o que comparten responsable y pueden alternarse. No se "
  "traslapó ninguna dependencia que atraviese un hito de decisión: en particular, el spike de latencia "
  "mantiene relación fin → inicio estricta con todo lo que sigue, porque su resultado puede obligar a "
  "revisar el alcance.")

H(doc,"12.3 Riesgo derivado de la compresión",2)
P(doc,"Quince de las 27 actividades quedan sin holgura, y otras cinco tienen un solo día. Es decir, 20 de "
  "27 actividades no admiten retraso apreciable. Es el costo directo de comprimir 20 días para caber en la "
  "ventana académica, y debe declararse como riesgo del proyecto, no presentarse como una programación "
  "holgada.")
table(doc,["Consecuencia","Medida de control"],[
 ("Cualquier retraso en la rama de interacción o en la de audio desplaza la fecha final.",
  "Revisión de avance semanal sobre las actividades críticas exclusivamente, no sobre el proyecto completo."),
 ("El tramo M → N concentra la dependencia de todo el trabajo técnico.",
  "El hito de latencia se coloca el día 10, cuando aún quedan 40 días para reaccionar si el resultado es negativo."),
 ("La rama del modelo tridimensional tiene un solo día de margen.",
  "Se controla como si fuera crítica. El paquete 3.3 ya se reasignó para acortarla."),
 ("La reserva de contingencia del cronograma es de solo 3 días hábiles.",
  "Se suma la semana del 16 al 20 de noviembre como reserva de gestión, disponible antes del inicio de exámenes."),
],widths=[7.6,8.4],fs=9.5)

H(doc,"12.4 Hitos de control",2)
table(doc,["Hito","Actividad que lo produce","Día","Fecha"],[
 ("H1  Diseño conceptual aprobado","H","4","11 de septiembre de 2026"),
 ("H2  Go / No-Go de latencia","N","10","14 de septiembre de 2026"),
 ("H3  Modelos integrados con físicas","R","30","13 de octubre de 2026"),
 ("H4  Rutinas y métricas integradas","V y W","40","27 de octubre de 2026"),
 ("H5  Build candidata congelada","X","45","3 de noviembre de 2026"),
 ("H6  Cierre del proyecto","Z","50","10 de noviembre de 2026"),
],widths=[5.4,4.4,1.8,4.4],fs=9.5)
P(doc,"Cinco de los seis hitos se producen al término de una actividad crítica. El único que no lo es, H1, "
  "corresponde a la rama cuasi-crítica del modelo tridimensional.")

H(doc,"12.5 Conclusión",2)
P(doc,"El proyecto es realizable dentro del periodo disponible, con una duración de red de 50 días hábiles "
  "frente a 53 disponibles, más una semana de reserva de gestión. La programación depende de dos condiciones "
  "que deben sostenerse: que el spike de latencia resulte favorable en el día 10, y que las ramas de "
  "interacción y de audio avancen sin retrasos, ya que ninguna de las dos tiene margen.")

out="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/superados/Ruta_Critica_42_paquetes_superada.docx"
doc.save(out); print("OK",out)
