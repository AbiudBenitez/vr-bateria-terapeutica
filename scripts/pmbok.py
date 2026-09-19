# -*- coding: utf-8 -*-
"""Estructura del PMBOK 6.ª edición: 5 grupos de procesos, 10 áreas, 49 procesos."""

GRUPOS = ["Inicio","Planificación","Ejecución","Monitoreo y Control","Cierre"]
GAB    = {"Inicio":"I","Planificación":"P","Ejecución":"E","Monitoreo y Control":"MC","Cierre":"C"}

AREAS = [
 ("4","Gestión de la Integración del Proyecto"),
 ("5","Gestión del Alcance del Proyecto"),
 ("6","Gestión del Cronograma del Proyecto"),
 ("7","Gestión de los Costos del Proyecto"),
 ("8","Gestión de la Calidad del Proyecto"),
 ("9","Gestión de los Recursos del Proyecto"),
 ("10","Gestión de las Comunicaciones del Proyecto"),
 ("11","Gestión de los Riesgos del Proyecto"),
 ("12","Gestión de las Adquisiciones del Proyecto"),
 ("13","Gestión de los Interesados del Proyecto"),
]

# (número, nombre, área, grupo)
PROCESOS = [
 ("4.1","Desarrollar el Acta de Constitución del Proyecto","4","Inicio"),
 ("4.2","Desarrollar el Plan para la Dirección del Proyecto","4","Planificación"),
 ("4.3","Dirigir y Gestionar el Trabajo del Proyecto","4","Ejecución"),
 ("4.4","Gestionar el Conocimiento del Proyecto","4","Ejecución"),
 ("4.5","Monitorear y Controlar el Trabajo del Proyecto","4","Monitoreo y Control"),
 ("4.6","Realizar el Control Integrado de Cambios","4","Monitoreo y Control"),
 ("4.7","Cerrar el Proyecto o Fase","4","Cierre"),
 ("5.1","Planificar la Gestión del Alcance","5","Planificación"),
 ("5.2","Recopilar Requisitos","5","Planificación"),
 ("5.3","Definir el Alcance","5","Planificación"),
 ("5.4","Crear la EDT/WBS","5","Planificación"),
 ("5.5","Validar el Alcance","5","Monitoreo y Control"),
 ("5.6","Controlar el Alcance","5","Monitoreo y Control"),
 ("6.1","Planificar la Gestión del Cronograma","6","Planificación"),
 ("6.2","Definir las Actividades","6","Planificación"),
 ("6.3","Secuenciar las Actividades","6","Planificación"),
 ("6.4","Estimar la Duración de las Actividades","6","Planificación"),
 ("6.5","Desarrollar el Cronograma","6","Planificación"),
 ("6.6","Controlar el Cronograma","6","Monitoreo y Control"),
 ("7.1","Planificar la Gestión de los Costos","7","Planificación"),
 ("7.2","Estimar los Costos","7","Planificación"),
 ("7.3","Determinar el Presupuesto","7","Planificación"),
 ("7.4","Controlar los Costos","7","Monitoreo y Control"),
 ("8.1","Planificar la Gestión de la Calidad","8","Planificación"),
 ("8.2","Gestionar la Calidad","8","Ejecución"),
 ("8.3","Controlar la Calidad","8","Monitoreo y Control"),
 ("9.1","Planificar la Gestión de Recursos","9","Planificación"),
 ("9.2","Estimar los Recursos de las Actividades","9","Planificación"),
 ("9.3","Adquirir Recursos","9","Ejecución"),
 ("9.4","Desarrollar el Equipo","9","Ejecución"),
 ("9.5","Dirigir al Equipo","9","Ejecución"),
 ("9.6","Controlar los Recursos","9","Monitoreo y Control"),
 ("10.1","Planificar la Gestión de las Comunicaciones","10","Planificación"),
 ("10.2","Gestionar las Comunicaciones","10","Ejecución"),
 ("10.3","Monitorear las Comunicaciones","10","Monitoreo y Control"),
 ("11.1","Planificar la Gestión de los Riesgos","11","Planificación"),
 ("11.2","Identificar los Riesgos","11","Planificación"),
 ("11.3","Realizar el Análisis Cualitativo de Riesgos","11","Planificación"),
 ("11.4","Realizar el Análisis Cuantitativo de Riesgos","11","Planificación"),
 ("11.5","Planificar la Respuesta a los Riesgos","11","Planificación"),
 ("11.6","Implementar la Respuesta a los Riesgos","11","Ejecución"),
 ("11.7","Monitorear los Riesgos","11","Monitoreo y Control"),
 ("12.1","Planificar la Gestión de las Adquisiciones","12","Planificación"),
 ("12.2","Efectuar las Adquisiciones","12","Ejecución"),
 ("12.3","Controlar las Adquisiciones","12","Monitoreo y Control"),
 ("13.1","Identificar a los Interesados","13","Inicio"),
 ("13.2","Planificar el Involucramiento de los Interesados","13","Planificación"),
 ("13.3","Gestionar el Involucramiento de los Interesados","13","Ejecución"),
 ("13.4","Monitorear el Involucramiento de los Interesados","13","Monitoreo y Control"),
]

# entradas y salidas características de cada grupo
GRUPO_IO = {
 "Inicio": dict(
   proposito="Definir un nuevo proyecto o una nueva fase, y obtener la autorización formal para comenzar.",
   entradas=["Caso de negocio y plan de gestión de beneficios",
             "Acuerdos, contratos o convenios con el patrocinador",
             "Factores ambientales de la empresa",
             "Activos de los procesos de la organización"],
   salidas=["Acta de constitución del proyecto",
            "Registro de supuestos",
            "Registro de interesados"],
   clave="El acta de constitución es la salida que autoriza el proyecto y designa al director. Sin ella, formalmente el proyecto no existe."),
 "Planificación": dict(
   proposito="Establecer el alcance total, refinar los objetivos y definir el curso de acción para alcanzarlos.",
   entradas=["Acta de constitución del proyecto",
             "Registro de interesados",
             "Salidas de otros procesos de planificación, que se retroalimentan entre sí",
             "Factores ambientales y activos de la organización"],
   salidas=["Plan para la dirección del proyecto, que integra los planes subsidiarios de las diez áreas",
            "Líneas base de alcance, cronograma y costos",
            "Documentos del proyecto: EDT, lista de actividades, cronograma, estimaciones, registro de riesgos, matriz de trazabilidad"],
   clave="Es el grupo con más procesos, 24 de 49, porque el esfuerzo de planificación condiciona todo lo demás. Sus salidas son las líneas base contra las que se mide el desempeño."),
 "Ejecución": dict(
   proposito="Completar el trabajo definido en el plan para satisfacer los requisitos del proyecto.",
   entradas=["Plan para la dirección del proyecto",
             "Documentos del proyecto",
             "Solicitudes de cambio aprobadas",
             "Factores ambientales y activos de la organización"],
   salidas=["Entregables",
            "Datos de desempeño del trabajo",
            "Registro de incidentes y de lecciones aprendidas",
            "Solicitudes de cambio",
            "Actualizaciones al plan y a los documentos del proyecto"],
   clave="Consume la mayor parte del presupuesto y de los recursos. Produce los entregables y, con ellos, los datos crudos de desempeño que alimentan el monitoreo."),
 "Monitoreo y Control": dict(
   proposito="Dar seguimiento, analizar y regular el avance y el desempeño; identificar cambios y aprobarlos.",
   entradas=["Plan para la dirección del proyecto y sus líneas base",
             "Documentos del proyecto",
             "Datos de desempeño del trabajo, provenientes de la ejecución",
             "Solicitudes de cambio"],
   salidas=["Información y luego informes de desempeño del trabajo",
            "Solicitudes de cambio",
            "Entregables verificados y aceptados",
            "Pronósticos de cronograma y de costos",
            "Actualizaciones al plan y a los documentos"],
   clave="Es el único grupo que se ejecuta en paralelo a todos los demás, de principio a fin. Transforma datos de desempeño en información y después en informes."),
 "Cierre": dict(
   proposito="Finalizar formalmente todas las actividades del proyecto o de una fase.",
   entradas=["Acta de constitución del proyecto",
             "Plan para la dirección del proyecto",
             "Documentos del proyecto",
             "Entregables aceptados",
             "Documentos de las adquisiciones"],
   salidas=["Transferencia del producto, servicio o resultado final",
            "Informe final del proyecto",
            "Actualización de los activos de los procesos de la organización, en particular el repositorio de lecciones aprendidas"],
   clave="Un solo proceso, pero indispensable: sin cierre formal no hay aceptación documentada ni lecciones aprendidas que capitalizar."),
}

def de_grupo(g):  return [p for p in PROCESOS if p[3]==g]
def de_area(a):   return [p for p in PROCESOS if p[2]==a]
def matriz():
    m = {}
    for num,nom,a,g in PROCESOS: m.setdefault((a,g),[]).append(num)
    return m

if __name__ == "__main__":
    assert len(PROCESOS)==49, len(PROCESOS)
    print(f"procesos: {len(PROCESOS)}   áreas: {len(AREAS)}   grupos: {len(GRUPOS)}")
    for g in GRUPOS: print(f"  {g:<22}{len(de_grupo(g)):>3} procesos")
    print()
    for a,nom in AREAS: print(f"  {a:>3}  {nom:<48}{len(de_area(a)):>3}")
