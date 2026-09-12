# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
import pdm, edt

doc = nuevo()
portada(doc,
 "ACTA CONSTITUTIVA DEL PROYECTO",
 "Simulación de batería en realidad virtual\ncon enfoque de musicoterapia",
 [("Versión","3.0"),
  ("Fecha","3 de septiembre de 2026"),
  ("Sustituye a","Versión 2.0 del 31 de agosto de 2026"),
  ("Unidad de aprendizaje","Administración de Proyectos de Software"),
  ("Docente y patrocinadora","Dra. Leticia Amalia Neira Tovar"),
  ("Equipo","Equipo A"),
  ("Periodo del proyecto","1 de septiembre al 13 de noviembre de 2026"),
  ("Presupuesto total","$384,201 MXN")])

# ---------------------------------------------------------------- control
H(doc,"Control del documento",1)
table(doc,["Versión","Fecha","Autor","Descripción del cambio"],[
 ("1.0","27 ago 2026","Equipo A","Versión inicial presentada."),
 ("2.0","31 ago 2026","Equipo A","Incorporación del enfoque terapéutico, perfiles requeridos, desglose del presupuesto, diagrama de Gantt y trabajo simultáneo."),
 ("3.0","3 sep 2026","Equipo A","Estructura de desglose del trabajo con criterios de aceptación por paquete. Reasignación del paquete 3.3 y adelanto del 3.1. Corrección de la ruta crítica declarada. Actualización del riesgo del asesor terapéutico. Anexo de asignación por paquete."),
],widths=[1.8,2.4,2.6,9.2],fs=9.5)

H(doc,"Cambios respecto de la versión 2.0",2)
P(doc,"Los cambios de esta versión provienen de dos fuentes: las observaciones de la patrocinadora sobre la "
  "versión 2.0 y el cálculo formal de la ruta crítica, que reveló una inconsistencia en la programación.")
table(doc,["#","Cambio","Razón"],[
 ("1","La estructura de desglose del trabajo pasa de una lista de paquetes a un cuadro completo con criterio de aceptación, responsable, recursos y duración por paquete.",
  "La estructura de desglose es la base de toda la planificación. Sin criterio de aceptación por paquete no es posible determinar cuándo está terminado."),
 ("2","El paquete 3.3, modelado de baquetas y entorno, se reasigna del artista tridimensional al diseñador de interacción, y pasa a ejecutarse en paralelo con el 3.2.",
  "El cálculo de la ruta crítica mostró que la rama del modelo tridimensional era una cadena de 39 días hábiles con un solo responsable, y que constituía el cuello de botella del proyecto."),
 ("3","El paquete 3.1, diseño conceptual, se adelanta a la primera semana.",
  "No depende de ninguna otra actividad. Mantenerlo en la segunda semana retrasaba innecesariamente toda la rama."),
 ("4","Se corrige la ruta crítica declarada.",
  "La versión 2.0 la declaraba sin haberla calculado. Tras el rebalanceo, el cálculo confirma que la rama de interacción sí es crítica, pero también identifica una segunda ruta crítica por la rama de audio, que no estaba declarada."),
 ("5","Se actualiza el riesgo del asesor terapéutico y se acortan los paquetes 2.2 y 2.3.",
  "La gestión del asesor avanzó: existe contacto identificado a través del líder del equipo. El riesgo baja de alto a medio."),
 ("6","Se agrega el anexo de asignación nominal por paquete de trabajo.",
  "Permite verificar que todo paquete tiene responsable y detectar los que quedan sin cubrir."),
 ("7","Las relaciones de precedencia se expresan con su tipo y demora.",
  "El cronograma contiene traslapes que la versión 2.0 no documentaba. Declararlos como relaciones inicio → inicio los convierte en una decisión de programación explícita."),
],widths=[0.8,7.4,7.8],fs=9)

doc.add_page_break()
# ================================================================ 1
H(doc,"1. Resumen ejecutivo",1)
P(doc,"El proyecto desarrolla un simulador de batería en realidad virtual concebido como herramienta de "
  "apoyo a la rehabilitación motriz de miembro superior. El usuario toca una batería virtual siguiendo "
  "rutinas rítmicas graduadas, diseñadas sobre protocolos reconocidos de musicoterapia neurológica y "
  "validadas por un asesor terapéutico externo. El sistema registra su desempeño y lo entrega al terapeuta "
  "como información objetiva del avance.")
P(doc,"El fin principal es motriz: trabajar amplitud, coordinación y sincronización del movimiento del "
  "miembro superior. El beneficio emocional derivado de la ejecución musical se considera secundario y no se "
  "mide como objetivo del proyecto.")
P(doc,"El proyecto se desarrolla en 11 semanas, del 1 de septiembre al 13 de noviembre de 2026, con un "
  "presupuesto total de $384,201 MXN. La red de precedencias arroja una duración de 50 días hábiles frente a "
  "los 53 disponibles, más una semana de reserva de gestión antes del inicio de exámenes.")
table(doc,["Concepto","Valor"],[
 ("Duración de la red de actividades","50 días hábiles"),
 ("Ventana disponible","53 días hábiles"),
 ("Reserva de cronograma","3 días hábiles, más la semana del 16 al 20 de noviembre"),
 ("Paquetes de trabajo","42, agrupados en 7 ramas"),
 ("Actividades de la red","27"),
 ("Rutas críticas","2, que convergen en la build candidata"),
 ("Equipo","8 roles internos y 1 asesor externo"),
 ("Presupuesto total","$384,201 MXN"),
],widths=[7.0,9.0],fs=10)

# ================================================================ 2
H(doc,"2. Definición del proyecto",1)
H(doc,"2.1 Visión",2)
P(doc,"Que una persona en proceso de rehabilitación motriz de miembro superior realice sus ejercicios "
  "tocando una batería en realidad virtual, y que su terapeuta disponga de un registro objetivo de cómo "
  "evoluciona sesión tras sesión.")

H(doc,"2.2 Objetivos",2)
table(doc,["#","Objetivo","Criterio de verificación"],[
 ("O1","Construir un simulador de batería en realidad virtual ejecutable en visor autónomo.","La aplicación se instala y ejecuta en el visor objetivo sin equipo de cómputo conectado."),
 ("O2","Lograr una respuesta suficientemente inmediata para que la ejecución se perciba natural.","El retardo entre el golpe y el sonido se mantiene por debajo de 30 milisegundos."),
 ("O3","Implementar rutinas rítmicas con fundamento terapéutico.","Al menos tres rutinas graduadas, con su fundamento documentado y validadas por el asesor."),
 ("O4","Registrar métricas objetivas del desempeño motriz.","El sistema exporta precisión temporal, amplitud de movimiento y constancia del pulso por sesión."),
 ("O5","Validar la pertinencia clínica de la solución.","Dictamen escrito del asesor terapéutico sobre rutinas y métricas."),
 ("O6","Entregar la documentación completa conforme a la metodología del curso.","Carta sponsor, acta constitutiva, estructura de desglose, cronograma, ruta crítica, manual e informe de pruebas."),
],widths=[0.9,6.1,9.0],fs=9.5)

H(doc,"2.3 Alcance",2)
P(doc,"Queda dentro del alcance:")
bullets(doc,[
 "Modelado tridimensional de la batería, las baquetas y el entorno de ejecución.",
 "Sistema de interacción con detección de colisión y medición de velocidad de impacto.",
 "Sistema de audio con capas de intensidad y variación por repetición.",
 "Rutinas rítmicas terapéuticas con guía visual y referencia de pulso.",
 "Interfaz adaptable a la altura y el alcance del usuario.",
 "Registro y exportación de métricas por sesión.",
 "Pruebas técnicas y pruebas con usuarios bajo protocolo validado.",
])
P(doc,"Queda fuera del alcance:")
bullets(doc,[
 "Diagnóstico clínico. El sistema entrega datos; la interpretación corresponde al terapeuta.",
 "Almacenamiento en servidor o expediente clínico. Las métricas se exportan a archivo local. El proyecto no contempla componente de servidor.",
 "Multijugador o sesiones remotas.",
 "Instrumentos distintos de la batería.",
 "Seguimiento de manos sin controles. La interacción se realiza mediante los controles del visor.",
 "Certificación como dispositivo médico.",
])

H(doc,"2.4 Entregables",2)
table(doc,["#","Entregable","Fecha"],[
 ("E1","Carta sponsor, revisión 2","3 sep 2026"),
 ("E2","Acta constitutiva, versión 3.0, con estructura de desglose del trabajo","3 sep 2026"),
 ("E3","Cronograma en formato importable y diagrama de Gantt","3 sep 2026"),
 ("E4","Documento de ruta crítica","7 sep 2026"),
 ("E5","Modelo tridimensional optimizado de la batería y el entorno","5 oct 2026"),
 ("E6","Sistema de interacción, físicas y audio integrado","20 oct 2026"),
 ("E7","Rutinas terapéuticas validadas y protocolo de sesión","27 oct 2026"),
 ("E8","Build candidata","3 nov 2026"),
 ("E9","Informe de pruebas y resultados","10 nov 2026"),
 ("E10","Manual técnico y de usuario","10 nov 2026"),
 ("E11","Presentación final","13 nov 2026"),
],widths=[1.0,10.0,5.0],fs=9.5)

doc.save('/tmp/_acta_a.docx'); print("parte A OK")
