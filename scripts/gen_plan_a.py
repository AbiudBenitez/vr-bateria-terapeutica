# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
import rc257 as R, costos as K
def d(x): return f"${x:,.0f}"

doc = nuevo()
portada(doc,
 "PLAN DE GESTIÓN DE LA CALIDAD\nY PLAN DE GESTIÓN DE LOS RIESGOS",
 "Simulación VR de batería con juego de ritmo",
 [("Unidad de aprendizaje","Administración de Proyectos de Software"),
  ("Docente","Dra. Leticia Amalia Neira Tovar"),
  ("Equipo","Equipo A"),
  ("Marco de referencia","Guía PMBOK: áreas 8 Calidad y 11 Riesgos"),
  ("Documento complementario","Análisis de Costos, Calidad y Riesgos"),
  ("Fecha","11 de septiembre de 2026")],
 sub2="Con una revisión de las certificaciones en dirección de proyectos")

H(doc,"Nota sobre este documento",1)
P(doc,"Este documento contiene los dos planes de gestión: define políticas, roles, procesos y umbrales. El "
  "análisis numérico que los sustenta, es decir el costo de la calidad y el valor monetario esperado de los "
  "riesgos, está en el documento «Análisis de Costos, Calidad y Riesgos» y no se repite aquí.")
P(doc,"Se agrega al final una revisión de las certificaciones profesionales en dirección de proyectos, "
  "por solicitud de la docente.")

doc.add_page_break()
# ======================================================= PARTE I
H(doc,"PARTE I. PLAN DE GESTIÓN DE LA CALIDAD",1)

H(doc,"1. Política de calidad",2)
P(doc,"El equipo se compromete a que cada entregable cumpla un criterio de aceptación definido antes de "
  "comenzar a producirlo, y a que ningún entregable se dé por terminado sin que otra persona distinta de "
  "quien lo produjo haya verificado ese criterio.")
P(doc,"La política se apoya en dos principios de la guía PMBOK. El primero es que la calidad se planifica, "
  "no se inspecciona: es más barato prevenir un defecto que corregirlo, como confirma el análisis del costo "
  "de la calidad. El segundo es que la calidad es responsabilidad de todo el equipo, no de una persona "
  "designada.")

H(doc,"2. Objetivos de calidad del proyecto",2)
table(doc,["#","Objetivo","Métrica asociada"],[
 ("OC1","El prototipo responde con inmediatez suficiente para que el golpe se perciba causal.","Latencia entre golpe y sonido"),
 ("OC2","El sistema identifica correctamente el componente golpeado.","Tasa de acierto en la detección"),
 ("OC3","La experiencia se ejecuta con fluidez en el visor objetivo.","Cuadros por segundo sostenidos"),
 ("OC4","El uso del simulador no produce molestia física.","Incidencia de mareo o fatiga"),
 ("OC5","Cada entregable cumple su criterio de aceptación.","Porcentaje de paquetes aceptados a la primera"),
 ("OC6","La documentación permite que un tercero instale y opere el sistema.","Prueba de instalación por una persona ajena al equipo"),
],widths=[0.9,9.1,6.0],fs=9.5)

H(doc,"3. Métricas de calidad",2)
P(doc,"Cada métrica indica qué se mide, con qué umbral, cómo y cuándo. Una métrica sin umbral y sin método "
  "de medición no permite decidir si algo se acepta o se rechaza.")
table(doc,["Métrica","Umbral de aceptación","Método de medición","Frecuencia","Responsable"],[
 ("Latencia entre golpe y sonido","Menor a 30 ms","Registro de marcas de tiempo entre el evento de colisión y el disparo de audio, sobre 100 golpes","En cada versión integrada","Desarrollador VR"),
 ("Tasa de acierto en la detección","Mayor o igual al 95 %","Sesión de 200 golpes dirigidos a componentes conocidos","En cada versión integrada","Analista de pruebas"),
 ("Cuadros por segundo","72 sostenidos, sin caídas por debajo de 60","Medición en el visor durante una sesión completa","Semanal desde la integración","Desarrollador VR"),
 ("Niveles de intensidad distinguidos","Tres niveles diferenciables","Golpes controlados suave, medio y fuerte; verificación del valor de intensidad","En cada versión integrada","Desarrollador VR"),
 ("Incidencia de mareo o fatiga","Cero reportes en sesiones de 15 minutos","Cuestionario posterior a cada sesión de prueba","En cada sesión con usuarios","Coordinador"),
 ("Paquetes aceptados a la primera","Mayor o igual al 80 %","Conteo de paquetes que pasan la revisión por pares sin correcciones","Semanal","Gerente de proyecto"),
 ("Defectos abiertos de severidad alta","Cero al cierre","Registro de errores","Semanal","Analista de pruebas"),
 ("Cobertura de casos de prueba","Un caso por cada objetivo de calidad","Revisión del plan de pruebas contra la lista de objetivos","Al cerrar el plan de pruebas","Analista de pruebas"),
],widths=[3.4,3.2,5.2,2.0,2.2],fs=8.5)

H(doc,"4. Roles y responsabilidades en materia de calidad",2)
table(doc,["Rol","Responsabilidad"],[
 ("Director de proyecto","Aprueba el plan de calidad y resuelve las discrepancias sobre si un entregable cumple o no su criterio."),
 ("Gerente de proyecto","Mantiene el registro de aceptación de paquetes y reporta las métricas semanalmente."),
 ("Responsable de cada área","Verifica que su entregable cumpla el criterio antes de someterlo a revisión."),
 ("Revisor por pares","Rol rotativo. Verifica el criterio de aceptación de un entregable que no produjo."),
 ("Analista de pruebas","Diseña y ejecuta los planes de prueba, y mantiene el registro de errores."),
 ("Todo el equipo","Aplica los estándares técnicos acordados y señala los defectos que detecta, sea cual sea el área."),
],widths=[3.6,12.4],fs=9.5)
P(doc,"La revisión por pares es rotativa y no recae en una persona fija. La razón es práctica: el equipo "
  "tiene ocho integrantes y una sola área de aseguramiento de calidad, que ya está sobrecargada. Distribuir "
  "la revisión evita concentrar más trabajo ahí y aprovecha que cada integrante conoce a fondo su "
  "especialidad.")

H(doc,"5. Estándares aplicables",2)
table(doc,["Ámbito","Estándar o convención","Cómo se verifica"],[
 ("Código","Convenciones de nomenclatura de C# para Unity. Un script por responsabilidad.","Revisión por pares antes de integrar."),
 ("Control de versiones","Rama por funcionalidad. Ningún cambio se integra sin revisión.","Historial del repositorio."),
 ("Modelos tridimensionales","Presupuesto de polígonos definido por componente. Nomenclatura acordada de objetos y materiales.","Revisión del artista y medición en el visor."),
 ("Audio","Formato y frecuencia de muestreo uniformes. Niveles normalizados.","Revisión del diseñador de audio."),
 ("Documentación","Criterio de aceptación redactado en forma verificable, no en forma de intención.","Revisión del gerente de proyecto."),
 ("Ergonomía en realidad virtual","Lineamientos de comodidad de la plataforma objetivo: campo visual, distancia de interfaz, ausencia de movimiento impuesto.","Sesión de prueba de 15 minutos."),
 ("Licencias de recursos","Todo recurso externo debe tener licencia verificada y documentada antes de incorporarse.","Registro de licencias por recurso."),
],widths=[2.8,7.4,5.8],fs=9)

doc.save('/tmp/_plan_a.docx'); print("A OK")
