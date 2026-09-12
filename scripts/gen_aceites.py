# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx.shared import Cm
import aoa

D="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/tareas/2026-09-04-ejemplo-ruta-critica/"

doc = nuevo()
portada(doc,
 "MÉTODO DE LA RUTA CRÍTICA",
 "Ejemplo de aplicación — Obtención de aceites esenciales\nde hierbabuena y menta",
 [("Unidad de aprendizaje","Administración de Proyectos de Software"),
  ("Docente","Dra. Leticia Amalia Neira Tovar"),
  ("Equipo","Equipo A"),
  ("Actividad","Desarrollo completo del ejemplo, desde la lista de actividades hasta la determinación de la ruta crítica"),
  ("Fuente","«El Método de la Ruta Crítica» y presentación «Administración de Proyectos, Parte IV»"),
  ("Duración obtenida","220 días"),
  ("Fecha","4 de septiembre de 2026")],
 sub2="Desarrollo completo con justificación de cada etapa")

# ================================================================ 1
H(doc,"1. El método de la ruta crítica",1)
P(doc,"La ruta crítica es una técnica de planeación y control que representa un proyecto como una red de "
  "actividades enlazadas por relaciones de precedencia. Permite calcular la duración mínima del proyecto y "
  "determinar qué actividades no admiten retraso alguno sin desplazar la fecha de terminación.")

H(doc,"1.1 Origen",2)
P(doc,"El método proviene de dos desarrollos independientes y prácticamente simultáneos, ambos de 1957.")
table(doc,["Técnica","Origen","Propósito original","Consecuencia sobre el método"],[
 ("Técnica de evaluación y revisión de programas (PERT)",
  "Marina de Guerra de los Estados Unidos, con Lockheed y Booz-Allen & Hamilton, para el programa de misiles Polaris.",
  "Controlar un proyecto de investigación y desarrollo cuyas duraciones no se conocían con precisión.",
  "Trabaja con tres estimaciones de tiempo por actividad: optimista, media y pesimista, y calcula una duración esperada."),
 ("Método de la ruta crítica (CPM)",
  "E. I. du Pont de Nemours & Co. junto con Remington Rand.",
  "Programar el mantenimiento de plantas químicas, donde las duraciones se conocían por experiencia repetida.",
  "Trabaja con una sola estimación de tiempo por actividad."),
],widths=[3.4,4.6,4.0,4.0],fs=9)
P(doc,"Ambas técnicas comparten la misma matemática de red y hoy se emplean de forma combinada. En este "
  "ejercicio se aplica el enfoque del método de la ruta crítica, con una estimación única por actividad, "
  "porque es lo que proporciona el documento base: no se dan tiempos optimista ni pesimista, de modo que no "
  "hay elementos para aplicar el otro tratamiento.")

H(doc,"1.2 Elementos de la red",2)
P(doc,"El ejemplo se desarrolla en la notación de actividad en la flecha, que es la que emplea el documento "
  "base. Sus elementos son cuatro.")
table(doc,["Elemento","Representación","Significado"],[
 ("Actividad","Flecha continua","Trabajo real que consume tiempo y recursos. Se rotula con su clave y su duración."),
 ("Evento o nodo","Círculo numerado","Instante en el tiempo. No consume tiempo ni recursos. Representa el inicio o el fin de una o varias actividades."),
 ("Actividad ficticia","Flecha punteada","Liga lógica de duración cero. Expresa una precedencia que no se puede dibujar de otra forma, o evita que dos actividades distintas compartan el mismo par de eventos."),
 ("Ruta crítica","Trayectoria de mayor duración","Secuencia continua de actividades, del evento inicial al final, cuya suma de duraciones es máxima. Define la duración del proyecto y no tiene holgura."),
],widths=[3.0,3.4,9.6],fs=9.5)

H(doc,"1.3 Regla de numeración de eventos",2)
P(doc,"Todo evento se numera de manera que, para cualquier actividad, el número del evento de inicio sea "
  "menor que el del evento de terminación. Esta regla no es una convención estética: garantiza que la red no "
  "contenga ciclos, es decir que ninguna actividad dependa indirectamente de sí misma, y permite recorrerla "
  "en un solo sentido durante los cálculos. La numeración empleada en este trabajo, del 0 al 20, cumple la "
  "regla en las 27 actividades y en las 3 ficticias, como puede verificarse en la matriz de información.")

H(doc,"1.4 Nota sobre la notación empleada",2)
P(doc,"La presentación del curso introduce también la diagramación por precedencias, en la que la actividad "
  "es un nodo y se admiten cuatro tipos de dependencia. Este ejercicio se desarrolla en actividad en la "
  "flecha porque es la notación del documento base y porque el ejemplo requiere actividades ficticias, que "
  "son un elemento propio de esa notación y no existen en la otra. La diagramación por precedencias se "
  "aplica en el documento de ruta crítica del proyecto de batería, donde sí resulta necesaria por la "
  "presencia de traslapes.")

doc.add_page_break()
# ================================================================ 2
H(doc,"2. Etapas del método",1)
P(doc,"El método se organiza en dos ciclos. El primero es de planeación y programación; el segundo, de "
  "ejecución y control. Este trabajo desarrolla el primer ciclo hasta la determinación de la ruta crítica.")
table(doc,["#","Etapa","Producto","Sección"],[
 ("1","Definición del proyecto","Objetivo, alcance y límites de lo que se va a programar.","1 y 3"),
 ("2","Lista de actividades","Relación de todas las actividades necesarias, cada una con su clave.","3"),
 ("3","Matriz de secuencias","Antecedentes y consecuentes de cada actividad.","4"),
 ("4","Matriz de tiempos","Duración estimada de cada actividad.","5"),
 ("5","Red de actividades o arreglo lógico","Dibujo de la red con eventos numerados y actividades ficticias.","7"),
 ("6","Costos y pendientes","Costo normal, costo límite y pendiente de cada actividad.","Fuera de alcance"),
 ("7","Compresión de la red","Reducción de la duración al mínimo costo incremental.","Fuera de alcance"),
 ("8","Limitaciones de tiempo, recursos y dinero","Ajuste de la programación a las restricciones reales.","Fuera de alcance"),
 ("9","Matriz de elasticidad","Holguras de cada actividad y determinación formal de la ruta crítica.","10 y 11"),
],widths=[0.9,4.6,7.5,3.0],fs=9.5)
P(doc,"Las etapas 6, 7 y 8 quedan fuera del alcance porque el documento base no proporciona datos de costo: "
  "desarrollarlas obligaría a inventar cifras y el resultado no sería verificable contra la fuente.")
P(doc,"La matriz de información no aparece como etapa numerada, pero es el cuadro que consolida las etapas "
  "2, 3 y 4 en un solo lugar y constituye el insumo directo para dibujar la red. Se incluye en la sección 6.")

H(doc,"2.1 Las tres preguntas para construir la red",2)
P(doc,"Al colocar cada actividad en el arreglo lógico se responden tres preguntas. Es el procedimiento que "
  "se siguió, renglón por renglón de la matriz de información, para construir la figura de la sección 7.")
bullets(doc,[
 "¿Qué actividades deben terminarse inmediatamente antes de que ésta pueda comenzar? Determina el evento de inicio.",
 "¿Qué actividades pueden comenzar inmediatamente después de que ésta termine? Determina el evento de terminación.",
 "¿Qué actividades pueden ejecutarse simultáneamente con ésta? Determina las ramas paralelas de la red.",
],num=True)

doc.add_page_break()
# ================================================================ 3
H(doc,"3. Lista de actividades",1)
P(doc,"El proyecto se descompone en 27 actividades. Las claves con sufijo 1 corresponden a la línea de "
  "hierbabuena y las de sufijo 2 a la línea de menta.")
P(doc,"Conviene detenerse en esa numeración porque explica la forma de toda la red. Ambas líneas son el "
  "mismo proceso aplicado a dos materias primas distintas: adquisición, caracterización, preparación, "
  "extracción, análisis, purificación, aprovechamiento de residuos, estabilidad y evaluación de calidad. "
  "Como no comparten equipo ni insumo, pueden ejecutarse en paralelo, y por eso la red se bifurca en dos "
  "ramas simétricas que solo vuelven a encontrarse al final, en las pruebas organolépticas y en el informe.")
table(doc,["Clave","Actividad","Días"],
      [(k, aoa.DESC[k], aoa.DUR[k]) for k in aoa.ORD],widths=[1.5,12.5,2.0],fs=9)

doc.add_page_break()
# ================================================================ 4
H(doc,"4. Matriz de secuencias",1)
P(doc,"La matriz de secuencias registra, para cada actividad, cuáles deben haber terminado antes de que ella "
  "pueda iniciar. Se presenta en sus dos formas equivalentes, por antecedentes y por consecuentes, porque "
  "juntas permiten verificarse mutuamente: si una actividad aparece como antecedente de otra, esa otra debe "
  "aparecer entre sus consecuentes.")
P(doc,"Esta matriz fue corregida respecto del documento base. Las siete diferencias y el procedimiento con "
  "que se determinó cuál versión es la correcta se justifican en el anexo A.")
table(doc,["Clave","Antecedentes","Consecuentes"],
      [(k, ", ".join(aoa.ANT[k]) or "—", ", ".join(aoa.CONS[k]) or "— (fin)") for k in aoa.ORD],
      widths=[1.8,7.1,7.1],fs=9)
H(doc,"4.1 Verificación de la matriz",2)
P(doc,"Se comprobaron tres condiciones sobre la matriz corregida:")
bullets(doc,[
 "Una sola actividad carece de antecedentes, la A, y es por tanto la actividad inicial del proyecto.",
 "Una sola actividad carece de consecuentes, la R, y es por tanto la actividad final.",
 "Toda actividad intermedia aparece al menos una vez en la columna de antecedentes de otra actividad, lo que "
 "confirma que la red es conexa y que ninguna actividad queda desconectada.",
],num=True)
P(doc,"Este último punto fue el que permitió detectar las erratas del documento base: en la versión original "
  "varias actividades de la rama de menta quedaban sin consecuente, es decir, la rama no cerraba en el "
  "evento final.")

doc.add_page_break()
# ================================================================ 5
H(doc,"5. Matriz de tiempos",1)
P(doc,"El documento base proporciona una estimación única de duración por actividad, expresada en días. Por "
  "esa razón el tratamiento corresponde al método de la ruta crítica y no a la técnica de evaluación y "
  "revisión de programas: no hay tiempo optimista ni pesimista, de modo que no puede calcularse duración "
  "esperada ni desviación estándar.")
mid=14; izq=aoa.ORD[:mid]; der=aoa.ORD[mid:]
rows=[]
for i in range(mid):
    a=izq[i]
    if i<len(der): b=der[i]; rows.append((a,aoa.DUR[a],b,aoa.DUR[b]))
    else: rows.append((a,aoa.DUR[a],"",""))
table(doc,["Clave","Duración (días)","Clave","Duración (días)"],rows,widths=[3.2,4.2,3.2,4.2],fs=10)
P(doc,f"Suma aritmética de todas las duraciones: {sum(aoa.DUR.values())} días. Este valor no es la duración "
  "del proyecto y conviene señalarlo porque es una confusión frecuente. Como muchas actividades corren en "
  "paralelo, la duración real es la de la trayectoria más larga de la red, que resulta ser de 220 días, "
  "menos de la mitad de la suma.")
P(doc,"Obsérvese además la dispersión de las duraciones: van de 5 días, en varias actividades de análisis, a "
  "90 días en las pruebas de estabilidad. Esa diferencia anticipa que las pruebas de estabilidad "
  "probablemente formen parte de la ruta crítica, cosa que el cálculo confirma.")

doc.add_page_break()
# ================================================================ 6
H(doc,"6. Matriz de información",1)
P(doc,"La matriz de información consolida en un solo cuadro la lista de actividades, sus secuencias y sus "
  "tiempos. Es el insumo directo para dibujar la red: cada renglón se convierte en una flecha, y las "
  "columnas de eventos indican entre qué nodos se traza.")
table(doc,["Clave","Antecedentes","Consecuentes","Días","Evento i","Evento j"],
      [(k, ", ".join(aoa.ANT[k]) or "—", ", ".join(aoa.CONS[k]) or "— (fin)",
        aoa.DUR[k], aoa.EV[k][0], aoa.EV[k][1]) for k in aoa.ORD],
      widths=[1.4,4.6,4.6,1.3,2.0,2.1],fs=8.5)
P(doc,"Las columnas de eventos se obtienen al trazar la red y se incorporan aquí como resultado del arreglo "
  "lógico. En las 27 actividades se cumple que el evento de inicio tiene número menor que el de terminación, "
  "conforme a la regla enunciada en la sección 1.3.")

# ================================================================ 7
landscape(doc)
H(doc,"7. Arreglo lógico",1)
P(doc,"La red se construyó aplicando las tres preguntas de la sección 2.1 a cada renglón de la matriz de "
  "información. Consta de 21 eventos, numerados del 0 al 20, veintisiete actividades reales y tres "
  "actividades ficticias.",size=9.5)
if os.path.exists(D+"Fig1_Arreglo_Logico.png"):
    doc.add_picture(D+"Fig1_Arreglo_Logico.png", width=Cm(25.4)); doc.paragraphs[-1].alignment=C
caption(doc,"Fig. 1 — Arreglo lógico. Obtención de aceites esenciales de hierbabuena y menta.")

H(doc,"7.1 Justificación de las actividades ficticias",2)
P(doc,"Las actividades ficticias no son un recurso de dibujo: cada una resuelve un problema lógico concreto "
  "que la notación no permite expresar de otra forma.",size=9.5)
table(doc,["Ficticia","Problema que resuelve"],[
 ("2 → 3","B y C parten ambas del evento 1, y las dos deben terminar antes de que inicien D, E, F y G-2. Si ambas se dibujaran entre los eventos 1 y 3 compartirían el mismo par de nodos, lo que la notación no permite porque entonces no habría forma de distinguirlas. Se hace terminar B en un evento propio, el 2, y una ficticia lleva esa terminación hasta el evento 3 sin consumir tiempo."),
 ("5 → 6","D, E y F deben terminar las tres antes de que inicie G-1, pero cada una termina en un evento distinto. E termina en el evento 5; la ficticia enlaza esa terminación con el evento 6, del que parte G-1."),
 ("4 → 6","Por la misma razón que la anterior, respecto de F, que termina en el evento 4."),
],widths=[2.6,22.5],fs=9.5)

H(doc,"7.2 Estructura de la red",2)
bullets(doc,[
 "Tramo común inicial, eventos 0 a 3: A, B y C. Todo el proyecto depende de que terminen el estudio de mercado y la formulación de los proyectos agrícolas.",
 "Tramo de preparación técnica, del evento 3 al 6: D, E y F corren en paralelo y convergen en el evento 6 por medio de las ficticias.",
 "Bifurcación: G-1, la línea de hierbabuena, arranca en el evento 6 y abre la rama superior; G-2, la de menta, arranca directamente en el evento 3 y abre la rama inferior. Ambas repiten el mismo proceso sobre materias primas distintas y se ejecutan simultáneamente.",
 "Primera convergencia, evento 17: M-1, M-2, O-1 y O-2 confluyen porque las pruebas organolépticas requieren las cuatro.",
 "Segunda convergencia, evento 19: N-1, N-2 y Q confluyen porque el informe final requiere las tres.",
 "Cierre: R conduce al evento 20, terminación del proyecto.",
])
P(doc,"Nótese una asimetría que resulta decisiva: G-2 arranca en el evento 3, mientras que G-1 debe esperar "
  "al evento 6. La rama de menta empieza 15 días antes que la de hierbabuena, y por eso, aunque ambas ramas "
  "tienen exactamente las mismas duraciones, solo una de ellas resulta crítica.",size=9.5)

portrait(doc)
# ================================================================ 8
H(doc,"8. Asignación de duraciones y cálculo de tiempos próximos",1)
P(doc,"El recorrido hacia adelante calcula el tiempo próximo de cada evento, es decir lo más pronto que "
  "puede ocurrir. Se parte del evento 0 en el día cero y se avanza siguiendo la red.")
H(doc,"8.1 Regla de cálculo",2)
P(doc,"El tiempo próximo de un evento es el mayor de los valores que le llegan por cada actividad que "
  "termina en él, entendiendo cada valor como el tiempo próximo del evento de origen más la duración de la "
  "actividad. Se toma el mayor porque el evento no puede ocurrir mientras no hayan terminado todas las "
  "actividades que llegan a él.")
P(doc,"Las actividades ficticias participan en el cálculo con duración cero: transmiten el tiempo del evento "
  "de origen al de destino sin agregarle nada.")
H(doc,"8.2 Cálculo de los tiempos remotos",2)
P(doc,"El recorrido hacia atrás calcula el tiempo remoto de cada evento, es decir lo más tarde que puede "
  "ocurrir sin retrasar el proyecto. Se parte del evento final, cuyo tiempo remoto es igual a su tiempo "
  "próximo, y se retrocede. El tiempo remoto de un evento es el menor de los valores que le llegan desde los "
  "eventos siguientes, entendiendo cada valor como el tiempo remoto del evento de destino menos la duración "
  "de la actividad. Se toma el menor porque el evento debe ocurrir a tiempo para la más exigente de las "
  "actividades que parten de él.")
H(doc,"8.3 Resultado por evento",2)
rows=[]
for e in range(0, aoa.NEV, 2):
    a=(e, aoa.TPI[e], aoa.TRT[e], aoa.TRT[e]-aoa.TPI[e], "Sí" if aoa.TPI[e]==aoa.TRT[e] else "")
    if e+1 < aoa.NEV:
        b=(e+1, aoa.TPI[e+1], aoa.TRT[e+1], aoa.TRT[e+1]-aoa.TPI[e+1], "Sí" if aoa.TPI[e+1]==aoa.TRT[e+1] else "")
        rows.append(a+b)
    else:
        rows.append(a+("","","",""))
table(doc,["Evento","T. próximo","T. remoto","Holgura","Crítico","Evento","T. próximo","T. remoto","Holgura","Crítico"],
      rows,widths=[1.6,1.7,1.7,1.4,1.6,1.6,1.7,1.7,1.4,1.6],fs=9)
P(doc,"El tiempo próximo del evento 20 es de 220 días: ésa es la duración del proyecto. Doce de los "
  "veintiún eventos tienen tiempo próximo igual al remoto y son por tanto eventos críticos. Los nueve "
  "restantes tienen holgura, y todos ellos pertenecen a la rama de menta o a las actividades de "
  "aprovechamiento de residuos y evaluación de calidad.")

# ================================================================ 9
landscape(doc)
H(doc,"9. Red medida",1)
P(doc,"La red medida es el mismo arreglo lógico con los tiempos incorporados. Sobre cada nodo se anota el "
  "tiempo próximo del evento y debajo su tiempo remoto. Sobre cada flecha se anota la clave de la actividad "
  "y su duración. Los eventos en que ambos tiempos coinciden son críticos.",size=9.5)
if os.path.exists(D+"Fig2_Red_Medida.png"):
    doc.add_picture(D+"Fig2_Red_Medida.png", width=Cm(25.4)); doc.paragraphs[-1].alignment=C
caption(doc,"Fig. 2 — Red medida. Tiempos próximos y remotos de los eventos. Duración total: 220 días.")

portrait(doc)
# ================================================================ 10
H(doc,"10. Matriz de elasticidad",1)
P(doc,"La matriz de elasticidad reúne los tiempos y las holguras de cada actividad. La holgura es el margen "
  "de retraso disponible, y se distingue en cuatro tipos porque cada uno responde a una pregunta distinta.")
table(doc,["Holgura","Fórmula","Qué responde"],[
 ("Total","Tiempo remoto de terminación menos tiempo próximo de iniciación menos duración.","Cuánto puede retrasarse la actividad sin mover la fecha final del proyecto."),
 ("Libre","Tiempo próximo del evento de terminación menos el tiempo próximo de terminación de la actividad.","Cuánto puede retrasarse sin afectar el inicio más temprano de ninguna actividad siguiente."),
 ("Interferente","Holgura total menos holgura libre.","Qué parte del margen, si se consume, reduce el margen de las actividades posteriores."),
 ("Independiente","Tiempo próximo del evento de terminación menos el tiempo remoto del evento de inicio menos la duración. Si resulta negativa se toma cero.","Cuánto puede retrasarse sin afectar ni a las antecedentes ni a las consecuentes, en el peor escenario."),
],widths=[2.4,6.8,6.8],fs=9)
rows=[(k,aoa.DUR[k],aoa.A_TPI[k],aoa.A_TPT[k],aoa.A_TRI[k],aoa.A_TRT[k],
       aoa.HT[k],aoa.HL[k],aoa.HI[k],aoa.HIND[k],"Sí" if aoa.HT[k]==0 else "") for k in aoa.ORD]
table(doc,["Clave","Dur.","TPI","TPT","TRI","TRT","H. total","H. libre","H. interf.","H. indep.","Crítica"],
      rows,widths=[1.4,1.1,1.1,1.1,1.1,1.1,1.5,1.5,1.5,1.5,1.5],fs=8.5)
P(doc,"TPI y TPT son los tiempos próximos de iniciación y terminación; TRI y TRT los remotos. Todos los "
  "valores están en días contados desde el inicio del proyecto.",italic=True)

# ================================================================ 11
H(doc,"11. Ruta crítica",1)
H(doc,"11.1 Criterio de identificación",2)
P(doc,"Una actividad es crítica cuando cumple estas condiciones, que son equivalentes entre sí:")
bullets(doc,["Su tiempo próximo de iniciación es igual a su tiempo remoto de iniciación.",
             "Su tiempo próximo de terminación es igual a su tiempo remoto de terminación.",
             "La diferencia entre su tiempo próximo de terminación y su tiempo remoto de iniciación es igual a su duración.",
             "Sus cuatro holguras valen cero."],num=True)
P(doc,"Se verificaron las cuatro condiciones en las 27 actividades. Diez las cumplen.")
H(doc,"11.2 Resultado",2)
P(doc,"Ruta crítica: A → C → D → G-1 → I-1 → J-1 → K-1 → L-1 → N-1 → R.")
table(doc,["Clave","Actividad","Días","Acumulado"],
      [(k, aoa.DESC[k][:70], aoa.DUR[k], sum(aoa.DUR[x] for x in aoa.CRIT[:i+1]))
       for i,k in enumerate(aoa.CRIT)]+[("","Total","","220 días")],
      widths=[1.4,10.0,1.8,2.8],fs=9)
P(doc,"La suma de las duraciones a lo largo de la ruta crítica es de 220 días, exactamente igual a la "
  "duración obtenida en el recorrido hacia adelante. Esta coincidencia es la comprobación aritmética de que "
  "los cálculos son correctos: si no coincidiera, habría un error en la red o en alguno de los recorridos.")

H(doc,"11.3 Lectura del resultado",2)
P(doc,"La ruta crítica recorre íntegramente la rama de hierbabuena y no toca la de menta, pese a que ambas "
  "ramas tienen exactamente las mismas duraciones. La razón está en el arreglo lógico: G-2 arranca en el "
  "evento 3, mientras que G-1 debe esperar a que terminen D, E y F, es decir al evento 6. Esos 15 días de "
  "diferencia se conservan a lo largo de toda la rama y se convierten en la holgura de 15 días que muestran "
  "todas las actividades de la línea de menta.")
P(doc,"Dos observaciones adicionales sobre el resultado:")
bullets(doc,[
 "Las pruebas de estabilidad de la hierbabuena, con 90 días, representan por sí solas el 41 % de la duración "
 "del proyecto. Cualquier esfuerzo de reducción del plazo debería concentrarse ahí antes que en cualquier "
 "otra actividad.",
 "El estudio de mercado, con 30 días, tiene 30 días de holgura total: puede duplicar su duración sin afectar "
 "la fecha final. En cambio la formulación de los proyectos agrícolas, con 60 días, es crítica. Ambas parten "
 "del mismo evento, pero solo una condiciona el plazo.",
])

# ================================================================ 12
landscape(doc)
H(doc,"12. Ruta crítica sobre la red",1)
if os.path.exists(D+"Fig3_Ruta_Critica.png"):
    doc.add_picture(D+"Fig3_Ruta_Critica.png", width=Cm(25.4)); doc.paragraphs[-1].alignment=C
caption(doc,"Fig. 3 — Ruta crítica resaltada: A → C → D → G-1 → I-1 → J-1 → K-1 → L-1 → N-1 → R. Duración: 220 días.")

portrait(doc)
# ================================================================ 13
H(doc,"13. Análisis de la programación",1)
H(doc,"13.1 Trabajo simultáneo",2)
table(doc,["Tramo","Actividades simultáneas","Observación"],[
 ("Días 0 – 5","A","Sin paralelismo. Todo el proyecto depende de esta actividad."),
 ("Días 5 – 65","B y C","El estudio de mercado corre junto a la formulación de los proyectos agrícolas. B termina en el día 35 y C en el 65."),
 ("Días 65 – 80","D, E, F y G-2","Cuatro frentes simultáneos. Aquí arranca la rama de menta, 15 días antes que la de hierbabuena."),
 ("Días 80 – 115","Ambas ramas completas","Punto de máximo paralelismo: caracterización, preparación, extracción, análisis y purificación de las dos materias primas a la vez."),
 ("Días 115 – 205","N-1, N-2, M-1, M-2, O-1, O-2, P y Q","Las pruebas de estabilidad, de 90 días, dominan el tramo. Todo lo demás cabe holgadamente dentro de ellas."),
 ("Días 205 – 220","R","Cierre. Sin paralelismo."),
],widths=[2.6,5.4,8.0],fs=9.5)
H(doc,"13.2 Distribución de las holguras",2)
table(doc,["Grupo de actividades","Holgura total","Interpretación"],[
 ("Ruta crítica: A, C, D, G-1, I-1, J-1, K-1, L-1, N-1, R","0 días","No admiten retraso alguno."),
 ("Rama de menta: G-2, H-2, I-2, J-2, K-2, L-2, N-2","15 a 30 días","Heredan el adelanto de 15 días con que arranca la rama."),
 ("Preparación técnica: E, F","5 días","Margen pequeño: convergen con D en el evento 6."),
 ("Estudio de mercado: B","30 días","Puede duplicar su duración sin afectar el plazo."),
 ("Residuos y calidad: M-1, M-2, O-1, O-2, P, Q","65 a 90 días","Alimentan las pruebas organolépticas y el análisis económico, que caben dentro de los 90 días de las pruebas de estabilidad."),
],widths=[6.4,2.6,7.0],fs=9.5)
P(doc,"Diez de las 27 actividades son críticas y las diecisiete restantes tienen holgura, en varios casos "
  "muy amplia. Es una red con margen: el control puede concentrarse en la rama de hierbabuena sin descuidar "
  "el proyecto.")

doc.add_page_break()
# ================================================================ anexo
H(doc,"Anexo A. Erratas detectadas en el documento base",1)
P(doc,"Durante la elaboración del ejercicio se encontraron inconsistencias internas en el documento fuente. "
  "Se documentan aquí porque afectan el trazado de la red y porque su corrección debe quedar justificada: "
  "todas las tablas de este trabajo incorporan ya las correcciones.")
H(doc,"A.1 Procedimiento de verificación",2)
P(doc,"El documento base contiene tres cuadros que describen la misma red: la matriz de secuencias, la "
  "matriz de información y la matriz de elasticidad. Los tres son mutuamente contradictorios, de modo que "
  "hubo que determinar cuál es el correcto antes de poder resolver el ejercicio.")
P(doc,"El procedimiento fue el siguiente. Se reconstruyó la red completa y se recalcularon los tiempos "
  "próximos y remotos de los veintiún eventos. La red corregida arroja una duración total de 220 días y una "
  "matriz de holguras que coincide renglón por renglón con la matriz de elasticidad publicada en el "
  "documento. La red sin corregir no reproduce esos valores y, de hecho, ni siquiera cierra: la rama de "
  "menta queda sin conexión con el evento final.")
P(doc,"Se concluye que la matriz de elasticidad es el cuadro correcto y que los errores están en la matriz "
  "de secuencias y en la matriz de información. La coincidencia de la suma de la ruta crítica con la "
  "duración total, ambas de 220 días, confirma el resultado por una vía independiente.")
H(doc,"A.2 Erratas",2)
table(doc,["#","Ubicación","Dice","Debe decir","Cómo se detectó"],[
 ("1","Matriz de secuencias, renglón B","B → E, E, F, G-2","B → D, E, F, G-2","La actividad E aparece repetida y D queda sin antecedente. Una D sin antecedente no podría iniciar nunca, porque no es la actividad inicial."),
 ("2","Matriz de secuencias, de L-2 en adelante","Corrimiento de un renglón en los consecuentes de L-2, M-2, N-2, O-2, P y Q","L-2 → N-2 y O-2; M-2 → P; N-2 → R; O-2 → P; P → Q; Q → R","La rama de menta no cerraba en el evento final: N-2 quedaba sin consecuente, lo que viola la condición de que solo la actividad final carezca de consecuentes."),
 ("3","Matriz de secuencias, clave G-1","Aparece como «1»","G-1","La clave «1» no existe en la lista de actividades. Por su posición y por sus consecuentes, H-1 e I-1, corresponde a G-1."),
 ("4","Matriz de información, columna de duración","Corrimiento de dos renglones a partir de la mitad del cuadro","Las duraciones de la sección 5 de este documento","Las duraciones no coincidían con las de la lista de actividades ni reproducían los 220 días de la matriz de elasticidad."),
 ("5","Lista de actividades, clave C","Duración de 0 días","60 días","Una actividad de duración cero es por definición ficticia. C es la formulación de dos proyectos agrícolas, es decir trabajo real. Con 60 días la red reproduce exactamente la matriz de elasticidad; con cualquier otro valor no lo hace."),
 ("6","Matriz de elasticidad","Una actividad aparece rotulada como «O»","Q","La actividad O tiene dos variantes, O-1 y O-2, y ninguna corresponde a los antecedentes indicados. Por sus antecedentes, P, y su consecuente, R, se trata de Q, el análisis económico."),
 ("7","Numeración de eventos","Ausente o incompleta en el diagrama del documento","Numeración de 0 a 20 propuesta en la sección 6","Sin numeración explícita no es posible construir la matriz de información ni verificar la regla de que el evento de inicio tenga número menor que el de terminación."),
],widths=[0.8,3.3,3.3,3.4,5.2],fs=8.5)
P(doc,"Las correcciones 1 a 5 modifican la red y por tanto el resultado. Las correcciones 6 y 7 son de "
  "rotulación y no alteran los cálculos.")

out=D+"Ejemplo_Ruta_Critica_Aceites_Completo.docx"
doc.save(out); print("OK",out)
print("parrafos:",len(doc.paragraphs)," tablas:",len(doc.tables)," imagenes:",len(doc.inline_shapes))
