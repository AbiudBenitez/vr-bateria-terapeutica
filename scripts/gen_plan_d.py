# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import rc257 as R, costos as K
doc = Document('/tmp/_plan_c.docx')

# ================================================================ 15
H(doc,"15. Implementar la respuesta a los riesgos",2)
P(doc,"Planificar respuestas no reduce ningún riesgo: la reducción ocurre cuando alguien ejecuta la "
  "respuesta. Este proceso define cómo se pasa del plan a la acción, y es donde la mayoría de los registros "
  "de riesgos fracasa, porque quedan escritos y nadie los ejecuta.")

H(doc,"15.1 Regla de activación",3)
P(doc,"Cada riesgo del registro tiene un disparador redactado como un hecho observable, no como una "
  "apreciación. Cuando el responsable observa el disparador, ejecuta la respuesta sin esperar autorización "
  "ni a la reunión semanal. Solo se escala al director cuando la respuesta implica recortar alcance o "
  "consumir más de tres días de la reserva de cronograma.")
table(doc,["Situación","Quién decide","Plazo"],[
 ("El disparador se cumple y la respuesta está dentro del área del responsable.","El responsable del riesgo, por su cuenta.","De inmediato. Se informa en la siguiente reunión."),
 ("La respuesta requiere apoyo de otra área.","El gerente de proyecto.","En un plazo de 24 horas."),
 ("La respuesta implica recortar alcance o consumir más de tres días de reserva.","El director de proyecto.","En la siguiente reunión, o antes si es urgente."),
 ("Aparece un riesgo no registrado con impacto mayor a dos días.","El gerente lo registra y asigna responsable de inmediato.","El mismo día en que se detecta."),
],widths=[6.8,4.8,4.4],fs=9.5)

H(doc,"15.2 Responsables de riesgo",3)
P(doc,"Cada riesgo tiene un dueño nominal. Un riesgo sin dueño es un riesgo que nadie vigila.")
rows=[]
RESP_NOM={"R1":"Misael","R2":"Kimberly","R3":"Diana","R4":"Javier y Christian",
          "R5":"Benjamín","R6":"Sarai","R7":"Sarai","R8":"Diana","R9":"Benjamín"}
for rid, desc, prob, dias, alc, cat in K.RIESGOS:
    rows.append((rid, desc[:58], RESP_NOM[rid], f"{prob*dias:.2f} d"))
table(doc,["Id","Riesgo","Responsable de vigilarlo y ejecutarlo","Valor esperado"],rows,
      widths=[0.9,7.6,4.5,3.0],fs=9)

H(doc,"15.3 Registro de ejecución",3)
P(doc,"Cada vez que se ejecuta una respuesta se anota qué disparador se cumplió, qué se hizo, cuántos días "
  "de reserva se consumieron y cuál fue el resultado. Sin ese registro no se puede saber si la reserva "
  "sigue alcanzando, ni aprender nada para el siguiente proyecto.")
table(doc,["Campo","Contenido"],[
 ("Fecha","Cuándo se observó el disparador."),
 ("Riesgo","Identificador del registro."),
 ("Disparador observado","El hecho concreto, no la impresión."),
 ("Respuesta ejecutada","Qué se hizo, y quién."),
 ("Días de reserva consumidos","Cuánto se gastó de los "+f"{K.RESERVA_CRONO:.2f}"+" disponibles."),
 ("Reserva restante","Saldo después de la ejecución."),
 ("Resultado","Si la respuesta funcionó, y qué quedó pendiente."),
],widths=[4.4,11.6],fs=9.5)

# ================================================================ 16
H(doc,"16. Monitorear los riesgos",2)
P(doc,"Monitorear es comprobar que las respuestas funcionan, reevaluar los riesgos vigentes, identificar los "
  "nuevos y cerrar los que ya no pueden ocurrir. Es un proceso continuo, no una revisión al final.")

H(doc,"16.1 Actividades y periodicidad",3)
table(doc,["Actividad","Frecuencia","Responsable","Producto"],[
 ("Revisión del registro de riesgos","Semanal","Gerente de proyecto","Registro actualizado con probabilidades reevaluadas"),
 ("Verificación de disparadores","Semanal","Responsable de cada riesgo","Confirmación de que ningún disparador se cumplió, o activación de la respuesta"),
 ("Identificación de riesgos nuevos","Semanal","Todo el equipo","Altas en el registro, con responsable asignado el mismo día"),
 ("Control del saldo de la reserva de cronograma","Semanal","Gerente de proyecto","Días consumidos y días restantes"),
 ("Reevaluación completa del registro","En cada hito de control","Gerente y director","Registro revisado y reserva recalculada"),
 ("Cierre de riesgos superados","En cada hito","Gerente de proyecto","Riesgos marcados como cerrados, con la lección aprendida"),
 ("Auditoría de riesgos","A la mitad del proyecto","Gerente de proyecto","Informe sobre si las respuestas planificadas están siendo eficaces"),
],widths=[4.6,2.4,3.4,5.6],fs=9.5)

H(doc,"16.2 Cierre de riesgos",3)
P(doc,"Un riesgo se cierra cuando la ventana en que podía materializarse ya pasó. Cerrarlo libera la parte "
  "de reserva que tenía asociada, que vuelve a estar disponible para los riesgos vigentes.")
table(doc,["Riesgo","Se cierra cuando","Libera"],[
 ("R1  Latencia sobre el umbral","Se supera el hito de verificación de latencia con medición favorable.","1.50 días"),
 ("R4  Licencias ambiguas","Todos los recursos externos están incorporados y verificados.","0.70 días"),
 ("R5  Préstamo de visores","Existe confirmación escrita de la Facultad.","1.20 días"),
 ("R7  Mareo en usuarios","Concluyen las sesiones de prueba sin incidencias.","0.40 días"),
],widths=[4.4,8.0,3.6],fs=9.5)

H(doc,"16.3 Indicadores de seguimiento",3)
table(doc,["Indicador","Qué señala","Umbral de alarma"],[
 ("Días de reserva consumidos","Cuánto margen queda para absorber lo que falte.","Superar el 50 % antes de la mitad del proyecto."),
 ("Riesgos nuevos por semana","Si la identificación inicial fue suficiente.","Más de dos semanas consecutivas con altas."),
 ("Riesgos con disparador cumplido y sin respuesta ejecutada","Si el plan se está aplicando o solo está escrito.","Cualquier valor distinto de cero."),
 ("Valor esperado total del registro","Si la exposición del proyecto crece o baja.","Superar la reserva de cronograma disponible."),
],widths=[4.6,6.4,5.0],fs=9.5)
P(doc,"El tercero es el indicador decisivo. Un registro de riesgos con disparadores cumplidos y respuestas "
  "sin ejecutar no es una herramienta de gestión: es documentación.")

doc.save('/tmp/_plan_d.docx'); print("D OK")
