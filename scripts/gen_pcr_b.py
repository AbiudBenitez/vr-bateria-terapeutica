# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import rc257 as R, costos as K, pruebas as PR
def d(x): return f"${x:,.0f}"
doc = Document('/tmp/_pcr_a.docx')

# ======================================================= PARTE II
H(doc,"PARTE II. PLAN DE GESTIÓN DE LA CALIDAD",1)

H(doc,"5. Política de calidad",2)
P(doc,"El equipo se compromete a que cada entregable cumpla un criterio de aceptación definido antes de "
  "comenzar a producirlo, y a que ningún entregable se dé por terminado sin que otra persona distinta de "
  "quien lo produjo haya verificado ese criterio.")
P(doc,"La política se apoya en dos principios de la guía. El primero es que la calidad se planifica y no se "
  "inspecciona: cuesta menos prevenir un defecto que corregirlo. El segundo es que la calidad es "
  "responsabilidad de todo el equipo y no de una persona designada, razón por la cual la revisión por pares "
  "es rotativa.")

H(doc,"6. Objetivos de calidad",2)
table(doc,["#","Objetivo","Métrica asociada"],[
 ("OC1","El prototipo responde con inmediatez suficiente para que el golpe se perciba causal.","Latencia entre golpe y sonido"),
 ("OC2","El sistema identifica correctamente el componente golpeado.","Tasa de acierto en la detección"),
 ("OC3","La experiencia se ejecuta con fluidez en el visor objetivo.","Cuadros por segundo sostenidos"),
 ("OC4","El sistema distingue la fuerza del golpe.","Niveles de intensidad diferenciables"),
 ("OC5","El uso del simulador no produce molestia física.","Incidencia de mareo o fatiga"),
 ("OC6","Cada entregable cumple su criterio de aceptación.","Paquetes aceptados a la primera"),
 ("OC7","La documentación permite que un tercero instale y opere el sistema.","Prueba de instalación por persona ajena al equipo"),
],widths=[0.9,9.1,6.0],fs=9.5)

H(doc,"7. Métricas de calidad",2)
P(doc,"Cada métrica indica qué se mide, con qué umbral, cómo y cuándo. Una métrica sin umbral y sin método "
  "de medición no permite decidir si algo se acepta o se rechaza.")
table(doc,["Métrica","Umbral de aceptación","Método de medición","Frecuencia","Responsable"],[
 ("Latencia entre golpe y sonido","Menor a 30 ms en el percentil 95","Cien golpes cronometrados, caso CN-14","En cada versión integrada","Misael"),
 ("Tasa de acierto en la detección","Mayor o igual al 95 %","Doscientos golpes dirigidos a componentes conocidos","En cada versión integrada","Diana"),
 ("Cuadros por segundo","72 sostenidos, sin caídas bajo 60","Medición en el visor durante una sesión completa, caso CN-13","Semanal desde la integración","Misael"),
 ("Niveles de intensidad","Tres niveles diferenciables","Golpes controlados suave, medio y fuerte, casos CB-02 y CN-09","En cada versión integrada","Misael"),
 ("Incidencia de mareo o fatiga","Cero reportes en sesiones de quince minutos","Cuestionario posterior a cada sesión, caso CN-16","En cada sesión con usuarios","Sarai"),
 ("Paquetes aceptados a la primera","Mayor o igual al 80 %","Conteo de paquetes que pasan la revisión por pares sin correcciones","Semanal","Diana"),
 ("Defectos abiertos de severidad alta","Cero al cierre","Registro de errores","Semanal","Diana"),
 ("Cobertura de casos de prueba","Un caso por cada objetivo de calidad","Revisión del catálogo contra la lista de objetivos","Al cerrar el plan de pruebas","Diana"),
],widths=[3.2,3.2,5.4,2.0,2.2],fs=8.5)

H(doc,"8. Roles y responsabilidades",2)
table(doc,["Rol","Responsabilidad en materia de calidad"],[
 ("Director de proyecto","Aprueba el plan y resuelve las discrepancias sobre si un entregable cumple su criterio."),
 ("Gerente de proyecto","Mantiene el registro de aceptación y reporta las métricas semanalmente."),
 ("Responsable de cada área","Verifica que su entregable cumpla el criterio antes de someterlo a revisión."),
 ("Revisor por pares","Rol rotativo. Verifica el criterio de un entregable que no produjo."),
 ("Responsable de pruebas","Diseña y ejecuta los planes de prueba y mantiene el registro de errores."),
 ("Todo el equipo","Aplica los estándares técnicos acordados y reporta los defectos que detecta, sea cual sea el área."),
],widths=[3.6,12.4],fs=9.5)
P(doc,"La revisión por pares es rotativa y no recae en una persona fija. La razón es práctica: el área de "
  "aseguramiento de calidad ya concentra la cuarta parte del esfuerzo del proyecto, y distribuir la revisión "
  "evita acumular más trabajo ahí.")

H(doc,"9. Estándares aplicables",2)
table(doc,["Ámbito","Estándar o convención","Cómo se verifica"],[
 ("Código","Convenciones de nomenclatura de C# para el motor. Un script por responsabilidad.","Revisión por pares antes de integrar."),
 ("Control de versiones","Rama por funcionalidad. Ningún cambio se integra sin revisión.","Historial del repositorio."),
 ("Modelos tridimensionales","Presupuesto de polígonos por componente. Nomenclatura acordada de objetos y materiales.","Revisión del artista y medición en el visor."),
 ("Audio","Formato y frecuencia de muestreo uniformes. Niveles normalizados.","Revisión del responsable de sonido."),
 ("Documentación","Criterio de aceptación redactado en forma verificable, no como intención.","Revisión del gerente de proyecto."),
 ("Ergonomía en realidad virtual","Campo visual, distancia de interfaz y ausencia de movimiento impuesto.","Sesión de prueba de quince minutos, caso CN-16."),
 ("Licencias de recursos","Todo recurso externo debe tener licencia verificada y documentada antes de incorporarse.","Registro de licencias por recurso."),
],widths=[2.8,7.4,5.8],fs=9)

H(doc,"10. Gestionar la calidad",2)
P(doc,"Gestionar la calidad se ocupa de los procesos, no de los entregables: busca que la forma de trabajar "
  "produzca buenos resultados de manera consistente.")
table(doc,["Actividad","Cuándo","Qué produce"],[
 ("Definir el criterio de aceptación antes de iniciar cada paquete","Al planificar cada semana","Criterio redactado y acordado, no supuesto"),
 ("Revisión por pares de todo entregable técnico","Antes de integrar","Registro de revisión con los hallazgos"),
 ("Auditoría de proceso a media ejecución","Semana 5","Informe de desviaciones respecto de los estándares"),
 ("Revisión de licencias de recursos externos","Al incorporar cada recurso","Registro de licencias actualizado"),
 ("Retrospectiva quincenal","Cada dos semanas","Acuerdos de mejora con responsable asignado"),
 ("Verificación de la trazabilidad requisito-prueba","Al cerrar el plan de pruebas","Matriz de trazabilidad completa, tarea QR.4"),
],widths=[6.4,3.0,6.6],fs=9.5)

H(doc,"11. Controlar la calidad",2)
P(doc,"Controlar la calidad se ocupa de los entregables: verifica que cada uno cumpla lo especificado. La "
  "diferencia con el proceso anterior es la que hay entre revisar cómo se trabaja y revisar qué salió. Su "
  "instrumento principal es el catálogo de pruebas de la parte III.")
table(doc,["Punto de control","Qué se verifica","Criterio de paso"],[
 ("Verificación de latencia","Medición en el hardware objetivo","Menor a 30 ms. Si no se cumple se convoca al director para revisar el alcance del sistema de audio"),
 ("Aceptación de paquete","Cumplimiento del criterio declarado","El revisor por pares lo confirma por escrito"),
 ("Pruebas unitarias por área","Funcionamiento aislado de cada subsistema","Sin defectos de severidad alta"),
 ("Pruebas de integración","Funcionamiento conjunto de los subsistemas","El flujo completo se ejecuta sin error"),
 ("Pruebas de rendimiento","Cuadros por segundo y latencia sobre la versión integrada","Umbrales de la sección 7"),
 ("Pruebas con usuarios","Comprensión de uso, comodidad y ausencia de molestia","Sin reportes de mareo. El usuario comprende el uso sin instrucción escrita"),
 ("Aceptación de la versión final","Todos los objetivos de calidad verificados","Ningún defecto de severidad alta abierto"),
],widths=[3.4,6.0,6.6],fs=9)

H(doc,"12. Costo de la calidad",2)
P(doc,f"El esfuerzo dedicado a la calidad asciende a {d(sum(K.COQ_TOT.values()))}, el "
  f"{100*sum(K.COQ_TOT.values())/K.MANO_OBRA:.1f} % del costo de mano de obra.")
table(doc,["Categoría","Tipo","Monto","% de la mano de obra"],
 [("Prevención","Conformidad",d(K.COQ_TOT["Prevención"]),f"{100*K.COQ_TOT['Prevención']/K.MANO_OBRA:.1f} %"),
  ("Evaluación","Conformidad",d(K.COQ_TOT["Evaluación"]),f"{100*K.COQ_TOT['Evaluación']/K.MANO_OBRA:.1f} %"),
  ("Fallos internos","No conformidad",d(K.COQ_TOT["Fallos internos"]),f"{100*K.COQ_TOT['Fallos internos']/K.MANO_OBRA:.1f} %"),
  ("Fallos externos","No conformidad","No aplica","—"),
  ("Total","",d(sum(K.COQ_TOT.values())),f"{100*sum(K.COQ_TOT.values())/K.MANO_OBRA:.1f} %")],
 widths=[4.0,3.4,4.2,4.4],fs=10)
P(doc,"Que la prevención supere a la corrección de fallos es el resultado buscado: cuesta menos evitar un "
  "defecto que repararlo. No hay costos por fallos externos porque el prototipo no llega a usuarios finales "
  "fuera del entorno controlado de prueba.")

doc.add_page_break()
doc.save('/tmp/_pcr_b.docx'); print("B OK")
