# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
from collections import Counter
import rc257 as R, costos as K, pruebas as PR
doc = Document('/tmp/_pcr_b.docx')

# ======================================================= PARTE III
H(doc,"PARTE III. PRUEBAS DE CALIDAD",1)

H(doc,"13. Estrategia de pruebas",2)
P(doc,"Probar un simulador de realidad virtual plantea una dificultad particular: buena parte de lo que hay "
  "que verificar no es un valor de salida sino una sensación. Que un golpe «se sienta» causal no se "
  "comprueba leyendo un número. Por eso la estrategia combina dos enfoques complementarios: pruebas que "
  "examinan el código por dentro y pruebas que examinan el comportamiento desde fuera.")

H(doc,"13.1 Los dos enfoques",3)
table(doc,["Enfoque","Qué conoce quien prueba","Qué verifica","Quién la ejecuta"],[
 ("Caja blanca","La estructura interna del código: funciones, condiciones y caminos de ejecución.",
  "Que cada rama, condición y camino del código se ejecute y produzca el resultado correcto. Detecta errores de lógica, valores límite mal tratados y código inalcanzable.",
  "El desarrollador del módulo, porque es quien conoce su estructura interna."),
 ("Caja negra","Solo las entradas y las salidas. El código es opaco.",
  "Que el sistema haga lo que el requisito dice, con independencia de cómo esté construido. Detecta funciones faltantes, comportamientos incorrectos y errores de interfaz.",
  "Una persona distinta de quien lo programó, para evitar el sesgo de probar solo lo que se sabe que funciona."),
],widths=[2.4,4.4,5.8,3.4],fs=9)
P(doc,"Los dos enfoques no son alternativas entre las que haya que elegir: encuentran defectos distintos. "
  "Una función puede tener el cien por ciento de cobertura de código y aun así no cumplir el requisito, si "
  "lo que implementa está mal entendido. A la inversa, una prueba funcional puede pasar y dejar sin "
  "ejercitar una rama de error que fallará el día que se active.")
P(doc,"Se añade un tercer enfoque en dos casos concretos, el de rendimiento y el de usabilidad, en los que "
  "no se verifica una función sino una propiedad del sistema completo: cuántos cuadros por segundo sostiene "
  "y si su uso resulta cómodo.")

H(doc,"13.2 Niveles de prueba",3)
table(doc,["Nivel","Qué se prueba","Enfoque predominante","Tarea del cronograma"],[
 ("Unitario","Cada función o módulo por separado, aislado del resto.","Caja blanca","QT.6, QT.7"),
 ("Integración","La comunicación entre subsistemas: que el evento de golpe llegue al sistema de audio y al de ritmo.","Caja blanca y negra","QT.6, QT.7, QT.4"),
 ("Sistema","El producto completo en el visor, con todos sus subsistemas operando.","Caja negra","QV.1, QV.2"),
 ("Rendimiento","Cuadros por segundo, latencia y estabilidad bajo uso prolongado.","Medición instrumentada","QV.2, QV.3, QV.4"),
 ("Aceptación","Que el usuario final comprenda y pueda usar el sistema sin instrucción.","Caja negra con usuarios reales","QT.8, QV.5"),
],widths=[2.4,6.2,3.6,3.8],fs=9.5)

H(doc,"13.3 Criterios de entrada y de salida",3)
table(doc,["Criterio","Condición"],[
 ("Entrada a pruebas unitarias","El módulo compila, está integrado en su rama y tiene su criterio de aceptación redactado."),
 ("Salida de pruebas unitarias","Todos los casos de caja blanca del módulo se ejecutaron y no queda ningún defecto de severidad alta."),
 ("Entrada a pruebas de sistema","Los subsistemas pasaron sus pruebas unitarias y existe una versión integrada ejecutable en el visor."),
 ("Salida de pruebas de sistema","Los casos de caja negra se ejecutaron, las métricas de rendimiento están dentro de umbral y no hay cierres inesperados."),
 ("Entrada a pruebas con usuarios","Existe versión estable, el protocolo de sesión está aprobado y se cuenta con al menos cinco participantes."),
 ("Salida de pruebas con usuarios","Se completaron las sesiones previstas, los hallazgos están registrados y clasificados por gravedad."),
 ("Criterio de suspensión","Si aparece un defecto que impide continuar la sesión, se detiene la prueba, se registra y se reanuda tras la corrección."),
],widths=[4.6,11.4],fs=9.5)

doc.add_page_break()
H(doc,"14. Pruebas de caja blanca",2)
P(doc,"Estas pruebas examinan el código por dentro. Quien las diseña conoce la estructura de la función y "
  "construye los casos para recorrer sus caminos de ejecución.")
H(doc,"14.1 Técnicas aplicadas",3)
table(doc,["Técnica","En qué consiste","Cuándo se aplica en este proyecto"],[
 ("Cobertura de sentencias","Diseñar casos hasta que cada línea de código se haya ejecutado al menos una vez.","Es el mínimo exigible en todo módulo. Detecta código muerto."),
 ("Cobertura de decisiones","Que cada condición se evalúe al menos una vez como verdadera y una vez como falsa.","En la identificación de la pieza golpeada y en la clasificación de golpes del juego de ritmo."),
 ("Cobertura de condiciones","Cuando una decisión combina varias condiciones, ejercitar cada una por separado.","En la supresión de golpes duplicados y en el sistema de combo."),
 ("Cobertura de caminos","Recorrer todas las combinaciones de decisiones posibles dentro de una función.","En el evento de golpe, que combina instrumento, intensidad y mano."),
 ("Complejidad ciclomática","Medir cuántos caminos independientes tiene una función para saber cuántos casos hacen falta.","Sobre el módulo de detección completo. Si una función supera diez, se divide."),
 ("Análisis de valores límite sobre condiciones internas","Probar justo por debajo, en y justo por encima de cada umbral del código.","En los umbrales de intensidad y en las ventanas de precisión, que es donde más errores se concentran."),
],widths=[3.6,5.4,7.0],fs=9)

H(doc,"14.2 Catálogo de casos de caja blanca",3)
rows=[(i,t,m,e,r,q,tar) for i,t,m,e,r,q,tar in PR.CAJA_BLANCA]
table(doc,["Id","Técnica","Módulo o función","Entrada o condición","Resultado esperado","Ejecuta","Tarea"],rows,
      widths=[1.0,2.4,3.0,3.6,4.0,1.3,0.9],fs=7.5)

doc.add_page_break()
H(doc,"15. Pruebas de caja negra",2)
P(doc,"Estas pruebas verifican el comportamiento sin conocer el código. Se diseñan a partir de los "
  "requisitos y de los casos de uso, y las ejecuta alguien distinto de quien programó el módulo.")
H(doc,"15.1 Técnicas aplicadas",3)
table(doc,["Técnica","En qué consiste","Cuándo se aplica en este proyecto"],[
 ("Particiones de equivalencia","Dividir las entradas posibles en grupos que el sistema trata igual, y probar un representante de cada grupo.","En la selección de dificultad y en la reproducción de audio por componente e intensidad."),
 ("Análisis de valores límite","Probar en los extremos de cada partición, que es donde suelen concentrarse los errores.","En la duración de sesión y en la interfaz ante usuarios de estatura muy distinta."),
 ("Tabla de decisión","Enumerar las combinaciones de condiciones y el resultado que corresponde a cada una.","En el cálculo del resultado final, que combina aciertos, fallos y combo."),
 ("Transición de estados","Verificar que el sistema pase correctamente de un estado a otro y que ningún estado quede sin salida.","En el flujo completo de la sesión y en la pausa y reanudación."),
 ("Pruebas basadas en casos de uso","Recorrer el sistema como lo haría el usuario, siguiendo el flujo previsto.","En el tutorial y en el abandono de la actividad."),
 ("Adivinación de errores","Provocar deliberadamente situaciones que el diseño no contempló, apoyándose en la experiencia.","En golpes simultáneos y en golpear fuera de la batería."),
],widths=[3.6,5.4,7.0],fs=9)

H(doc,"15.2 Catálogo de casos de caja negra",3)
rows=[(i,t,m,e,r,q,tar) for i,t,m,e,r,q,tar in PR.CAJA_NEGRA]
table(doc,["Id","Técnica","Función o flujo","Entrada o condición","Resultado esperado","Ejecuta","Tarea"],rows,
      widths=[1.0,2.6,2.8,3.4,4.0,1.4,1.0],fs=7.5)

doc.add_page_break()
H(doc,"16. Asignación y calendario de las pruebas",2)
H(doc,"16.1 Quién ejecuta qué",3)
P(doc,"La asignación sigue dos reglas. Las pruebas de caja blanca las ejecuta el desarrollador del módulo, "
  "porque requieren conocer su estructura interna. Las de caja negra las ejecuta una persona distinta de "
  "quien lo programó, para evitar el sesgo de probar solo lo que se sabe que funciona.")
cnt = Counter()
for i,t,m,e,r,q,tar in PR.CAJA_BLANCA: cnt[(q,"Caja blanca")]+=1
for i,t,m,e,r,q,tar in PR.CAJA_NEGRA:  cnt[(q,"Caja negra")]+=1
personas = sorted({p for p,_ in cnt})
table(doc,["Responsable","Caja blanca","Caja negra","Total","Ámbito"],
 [(p, cnt.get((p,"Caja blanca"),0), cnt.get((p,"Caja negra"),0),
   cnt.get((p,"Caja blanca"),0)+cnt.get((p,"Caja negra"),0),
   {"Misael":"Detección de golpe, intensidad, evento de golpe y rendimiento",
    "Benjamín":"Reloj musical, ventanas de precisión, puntuación y combo",
    "Christian":"Audio espacial, selección de muestras y reproducción por intensidad",
    "Diana":"Flujo de sesión, menús, resultados, estabilidad y pruebas exploratorias",
    "Sarai":"Tutorial, legibilidad, ergonomía y comodidad",
    "Misael y Christian":"Latencia entre golpe y sonido, medición conjunta",
    "Sarai y Jesús":"Sesiones de prueba con usuarios"}.get(p,""))
  for p in personas] +
 [("Total", len(PR.CAJA_BLANCA), len(PR.CAJA_NEGRA), len(PR.CAJA_BLANCA)+len(PR.CAJA_NEGRA), "")],
 widths=[3.0,1.8,1.6,1.4,8.2],fs=9)

H(doc,"16.2 Cuándo se ejecutan",3)
table(doc,["Momento","Pruebas que se ejecutan","Tareas del cronograma"],[
 ("Al cerrar cada módulo","Casos de caja blanca del módulo correspondiente.","QT.6, QT.7"),
 ("Al integrar audio con físicas","CB-13, CB-14 y CN-09.","QT.4"),
 ("Sobre la primera versión integrada","Casos de caja negra de flujo, menús y resultados.","QT.3, QV.1"),
 ("Antes de congelar la versión candidata","Pruebas de rendimiento y estabilidad: CN-13, CN-14, CN-15.","QV.2, QV.3, QV.4"),
 ("Con usuarios, sobre la versión candidata","CN-10, CN-16 y observación libre.","QT.8, QV.5"),
 ("Después de corregir","Repetición de los casos que fallaron, más regresión de los módulos tocados.","QE.5"),
],widths=[3.8,7.2,5.0],fs=9.5)

H(doc,"17. Gestión de los defectos encontrados",2)
P(doc,"Encontrar un defecto no sirve de nada si no queda registrado con la información suficiente para "
  "reproducirlo y corregirlo. El formato de registro se define en la tarea QE.1.")
table(doc,["Campo","Contenido"],[
 ("Identificador","Consecutivo único."),
 ("Caso de prueba","Identificador del caso que lo detectó, o «exploratorio» si se halló fuera del catálogo."),
 ("Descripción","Qué ocurrió, redactado como hecho observable."),
 ("Pasos para reproducirlo","Secuencia exacta. Un defecto que no se reproduce no se puede corregir."),
 ("Resultado esperado y obtenido","Ambos, para que la diferencia sea evidente."),
 ("Severidad","Alta si impide continuar o compromete un objetivo de calidad; media si degrada la experiencia; baja si es cosmético."),
 ("Área responsable","A quién se le asigna, conforme a la tarea QE.4."),
 ("Estado","Abierto, en corrección, corregido o verificado."),
],widths=[4.2,11.8],fs=9.5)
table(doc,["Severidad","Definición","Plazo de atención"],[
 ("Alta","Impide continuar la sesión, produce cierre inesperado o incumple un objetivo de calidad.","Antes de congelar la versión candidata. Ninguno puede quedar abierto al cierre."),
 ("Media","Degrada la experiencia pero permite continuar.","Se corrige si el cronograma lo permite; en caso contrario se documenta."),
 ("Baja","Cosmético o de redacción.","Se registra y se corrige solo si sobra tiempo."),
],widths=[2.2,8.4,5.4],fs=9.5)
P(doc,"La verificación de la corrección es una actividad propia, la tarea QE.5, y la ejecuta una persona "
  "distinta de quien corrigió el defecto. Corregir y verificar con la misma persona anula el control.")

doc.add_page_break()
doc.save('/tmp/_pcr_c.docx'); print("C OK")
