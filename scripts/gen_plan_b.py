# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import rc257 as R, costos as K
def d(x): return f"${x:,.0f}"
doc = Document('/tmp/_plan_a.docx')

H(doc,"6. Gestionar la calidad",2)
P(doc,"Gestionar la calidad es el proceso de convertir el plan en actividades ejecutables. Se ocupa de los "
  "procesos, no de los entregables: busca que la forma de trabajar produzca buenos resultados de manera "
  "consistente.")
table(doc,["Actividad","Cuándo","Qué produce"],[
 ("Definir el criterio de aceptación antes de iniciar cada paquete","Al planificar cada semana","Criterio redactado y acordado, no supuesto"),
 ("Revisión por pares de todo entregable técnico","Antes de integrar","Registro de revisión con los hallazgos"),
 ("Auditoría de proceso a media ejecución","Semana 5","Informe de desviaciones respecto de los estándares acordados"),
 ("Revisión de licencias de recursos externos","Al incorporar cada recurso","Registro de licencias actualizado"),
 ("Retrospectiva quincenal","Cada dos semanas","Acuerdos de mejora del proceso, con responsable"),
 ("Verificación de la trazabilidad requisito-prueba","Al cerrar el plan de pruebas","Matriz de trazabilidad completa"),
],widths=[6.4,3.0,6.6],fs=9.5)

H(doc,"7. Controlar la calidad",2)
P(doc,"Controlar la calidad se ocupa de los entregables: verifica que cada uno cumpla lo especificado. La "
  "diferencia con el proceso anterior es la que hay entre revisar cómo se trabaja y revisar qué salió.")
table(doc,["Punto de control","Qué se verifica","Criterio de paso"],[
 ("Verificación de latencia","Medición de la latencia en el hardware objetivo","Menor a 30 ms. Si no se cumple, se convoca al director para revisar el alcance del sistema de audio"),
 ("Aceptación de paquete","Cumplimiento del criterio de aceptación declarado","El revisor por pares lo confirma por escrito"),
 ("Pruebas unitarias por área","Funcionamiento aislado de cada subsistema","Sin defectos de severidad alta"),
 ("Pruebas de integración","Funcionamiento conjunto de los subsistemas","El flujo completo se ejecuta sin error"),
 ("Pruebas de rendimiento","Cuadros por segundo y latencia sobre la versión integrada","72 cuadros por segundo sostenidos y latencia bajo umbral"),
 ("Pruebas con usuarios","Comprensión de uso, comodidad y ausencia de molestia","Sin reportes de mareo. El usuario comprende el uso sin instrucción escrita"),
 ("Aceptación de la versión final","Todos los objetivos de calidad verificados","Ningún defecto de severidad alta abierto"),
],widths=[3.4,6.0,6.6],fs=9)

H(doc,"8. Listas de verificación por entregable",2)
P(doc,"Las listas evitan que la aceptación dependa de la memoria de quien revisa.")
table(doc,["Entregable","Puntos a verificar"],[
 ("Modelo tridimensional","Nomenclatura conforme al estándar · Dentro del presupuesto de polígonos · Materiales asignados · Escala correcta respecto al usuario · Se visualiza sin defectos en el visor"),
 ("Componente de código","Revisado por un par · Sin advertencias del compilador · Nomenclatura conforme · Integrado en rama propia · Probado de forma aislada"),
 ("Recurso de audio","Formato y frecuencia uniformes · Nivel normalizado · Licencia verificada y registrada · Se dispara correctamente desde el motor"),
 ("Pantalla de interfaz","Alcanzable en tres pasos o menos · Legible a la distancia de uso · Coherente con el resto de las pantallas · Probada en el visor, no solo en pantalla plana"),
 ("Documento","Criterio de aceptación verificable · Sin apartados pendientes · Revisado por una persona distinta del autor · Cifras consistentes con las de los demás documentos"),
 ("Versión integrada","Compila e instala en el visor · Flujo completo sin error · Métricas de rendimiento dentro de umbral · Sin defectos de severidad alta"),
],widths=[3.4,12.6],fs=9)

H(doc,"9. Costo de la calidad",2)
P(doc,f"El esfuerzo dedicado a la calidad asciende a {d(sum(K.COQ_TOT.values()))}, equivalente al "
  f"{100*sum(K.COQ_TOT.values())/K.MANO_OBRA:.1f} % del costo de mano de obra. Se reparte en "
  f"{d(K.COQ_TOT['Prevención'])} de prevención, {d(K.COQ_TOT['Evaluación'])} de evaluación y "
  f"{d(K.COQ_TOT['Fallos internos'])} de corrección de fallos internos.")
P(doc,"Que la prevención supere a la corrección es el resultado buscado. El desglose completo está en la "
  "sección 12 del documento de análisis.")

doc.add_page_break()
# ======================================================= PARTE II
H(doc,"PARTE II. PLAN DE GESTIÓN DE LOS RIESGOS",1)

H(doc,"10. Metodología",2)
P(doc,"El plan sigue los procesos de la guía PMBOK para el área de riesgos, adaptados a la escala del "
  "proyecto: once semanas, ocho personas y un entregable académico.")
table(doc,["Proceso","Cómo se aplica en este proyecto"],[
 ("Planificar la gestión de los riesgos","Este documento. Define escalas, roles, periodicidad y umbrales."),
 ("Identificar los riesgos","Sesión inicial de identificación con todo el equipo, más revisión en cada reunión semanal. Técnicas: tormenta de ideas, análisis de supuestos y revisión de la red de precedencias en busca de puntos de convergencia."),
 ("Análisis cualitativo","Valoración de probabilidad e impacto en escalas de cinco niveles y ubicación en la matriz."),
 ("Análisis cuantitativo","Cálculo del valor esperado de cada riesgo en días hábiles, cuyo total determina la reserva de cronograma."),
 ("Planificar la respuesta","Estrategia, responsable, disparador y plan de contingencia por cada riesgo, en la sección 13."),
 ("Implementar la respuesta","El responsable ejecuta la estrategia acordada cuando se cumple el disparador."),
 ("Monitorear los riesgos","Revisión semanal del registro. Se reevalúan probabilidades, se cierran los superados y se identifican nuevos."),
],widths=[4.4,11.6],fs=9.5)

H(doc,"11. Roles y periodicidad",2)
table(doc,["Rol","Responsabilidad en materia de riesgos"],[
 ("Director de proyecto","Autoriza el uso de la reserva de cronograma y decide ante riesgos que comprometan el alcance."),
 ("Gerente de proyecto","Es el dueño del registro de riesgos. Lo actualiza, lo presenta semanalmente y vigila los disparadores."),
 ("Responsable de área","Identifica y reporta los riesgos de su ámbito, y ejecuta las respuestas que le corresponden."),
 ("Todo el equipo","Reporta cualquier riesgo que detecte, sin esperar a la reunión semanal si es urgente."),
],widths=[3.6,12.4],fs=9.5)
P(doc,"Periodicidad: revisión del registro en la reunión semanal de seguimiento. Reevaluación completa en "
  "los hitos de control del proyecto.")

H(doc,"12. Escalas, matriz y umbrales",2)
P(doc,"Las escalas se definen antes de valorar los riesgos, para que la valoración sea reproducible y no "
  "dependa de la impresión de quien la hace.")
table(doc,["Nivel","Probabilidad","Impacto en cronograma","Impacto en alcance"],[
 ("Muy bajo","10 %","Alrededor de 1 día hábil","Ningún entregable afectado"),
 ("Bajo","30 %","Alrededor de 2 días hábiles","Un entregable secundario se degrada"),
 ("Medio","50 %","Alrededor de 3 días hábiles","Un entregable principal se degrada"),
 ("Alto","70 %","Alrededor de 5 días hábiles","Se pierde un entregable secundario"),
 ("Muy alto","90 %","8 días o más, o compromete la entrega","Se pierde un entregable principal"),
],widths=[2.0,2.2,4.8,7.0],fs=9)
P(doc,"El impacto no se valora en dinero. El proyecto no realiza compras ni contrata personal, de modo que "
  "ningún riesgo puede materializarse como un desembolso: lo que puede perder es tiempo y alcance. La "
  "justificación completa está en la sección 12.1 del documento de análisis.")

H(doc,"12.1 Umbrales de acción",3)
table(doc,["Severidad","Definición","Acción obligatoria"],[
 ("Baja","Producto de nivel de probabilidad por nivel de impacto menor o igual a 4","Se registra y se vigila. No requiere respuesta activa."),
 ("Moderada","Producto entre 5 y 9","Requiere estrategia de respuesta y responsable asignado."),
 ("Alta","Producto entre 10 y 15","Requiere respuesta activa, plan de contingencia y revisión semanal explícita."),
 ("Muy alta","Producto mayor a 15","Se escala al director del proyecto. Requiere plan de contingencia aprobado antes de continuar."),
],widths=[2.2,5.4,8.4],fs=9.5)
P(doc,"Tolerancia al riesgo del proyecto: la fecha de entrega es la restricción rígida, porque los exámenes "
  "del semestre inician el 23 de noviembre y no es negociable. El alcance es la variable con la que se "
  "absorben los imprevistos, y el costo tiene margen a través de las reservas. En caso de conflicto, se "
  "sacrifica alcance antes que fecha.")

H(doc,"13. Estructura de desglose de riesgos",2)
table(doc,["Categoría","Qué agrupa","Riesgos del registro"],[
 ("Técnico","Rendimiento, latencia, integración y herramientas.","R1, R7, R8"),
 ("Cronograma","Encadenamiento de actividades y puntos de convergencia.","R2"),
 ("Recursos","Disponibilidad y carga de trabajo del equipo.","R3, R9"),
 ("Externo","Dependencias fuera del control del equipo.","R4, R5, R6"),
],widths=[2.6,8.4,5.0],fs=9.5)

doc.save('/tmp/_plan_b.docx'); print("B OK")
