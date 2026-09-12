# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import pdm, edt

doc = Document('/tmp/_acta_a.docx')
doc.add_page_break()

# ================================================================ 3
H(doc,"3. Organización del proyecto",1)

H(doc,"3.1 Clientes y partes intervinientes",2)
table(doc,["Parte","Interés en el proyecto","Influencia"],[
 ("Patrocinadora — Dra. Leticia Amalia Neira Tovar","Verificar la aplicación de la metodología de administración de proyectos y la calidad del producto.","Alta. Aprueba el acta, los entregables y la calificación."),
 ("Equipo A","Desarrollar el proyecto y acreditar la unidad de aprendizaje.","Alta. Ejecuta la totalidad del trabajo."),
 ("Asesor terapéutico externo","Aportar criterio profesional y validar la pertinencia clínica.","Media. No ejecuta desarrollo, pero su dictamen condiciona el objetivo O5."),
 ("Usuarios de prueba","Participar en las sesiones de validación.","Media. Su retroalimentación determina las correcciones finales."),
 ("Facultad de Ingeniería Mecánica y Eléctrica","Disponer de un proyecto demostrable con aplicación real.","Baja durante la ejecución."),
],widths=[4.4,7.2,4.4],fs=9.5)

H(doc,"3.2 Roles y responsabilidades",2)
table(doc,["Rol","Responsabilidad principal","Integrante"],[
 ("Director de proyecto","Aprobar decisiones de alcance, presupuesto y hitos. Resolver bloqueos.","Abiud Misael Benítez Muñoz"),
 ("Gerente de proyecto","Mantener el plan, el cronograma y el registro de riesgos. Controlar el avance.","Ricardo Alejandro Rodríguez Ríos"),
 ("Coordinador","Coordinar al equipo, gestionar al asesor externo y las sesiones de prueba.","Jesús Eduardo Rodríguez Salinas"),
 ("Desarrollador de realidad virtual","Interacción, físicas, integración y build.","María Fernanda Montoya Valdez"),
 ("Diseñador de interacción y experiencia en realidad extendida","Ergonomía, interfaz, menús y, en esta versión, el modelado de baquetas y entorno.","Diana Laura Tello Salinas"),
 ("Artista y modelador tridimensional","Modelado de la batería, texturizado y optimización de geometría.","Christian Salvador Valadez Gallegos"),
 ("Diseñador de audio","Librería de muestras, capas de intensidad e integración con las físicas.","Javier Alejandro Hernández Caloca"),
 ("Analista de métricas","Investigación terapéutica, definición de métricas, protocolo de sesión e informe de resultados.","Kimberly González Sepúlveda"),
 ("Asesor terapéutico externo","Validar rutinas, métricas y protocolo. Emitir el dictamen de pertinencia.","Externo. Gestión en curso."),
],widths=[4.6,7.4,4.0],fs=9.5)

H(doc,"3.3 Perfiles requeridos",2)
P(doc,"Se detalla el perfil de cada rol: qué conocimientos exige y por qué el proyecto lo necesita.")
table(doc,["Rol","Perfil requerido","Por qué se necesita"],[
 ("Director de proyecto","Criterio para decidir sobre alcance y presupuesto. Conocimiento de la metodología del curso.","El proyecto tiene un hito de decisión, el Go / No-Go de latencia, que puede obligar a recortar alcance."),
 ("Gerente de proyecto","Manejo de estructura de desglose del trabajo, cronograma, ruta crítica y registro de riesgos. Uso de herramienta de programación.","Veinte de las 27 actividades no tienen holgura apreciable: el control del cronograma es la función más exigente del proyecto."),
 ("Coordinador","Capacidad de gestión con personas externas y organización de sesiones.","La incorporación del asesor y la organización de las pruebas con usuarios dependen de esta función."),
 ("Desarrollador de realidad virtual","Unity, kit de desarrollo de Meta, física de colisiones y programación de audio sincronizado con reloj de audio.","Es el rol con mayor carga y participa en las dos rutas críticas."),
 ("Diseñador de interacción y experiencia en realidad extendida","Diseño de interacción en realidad virtual, ergonomía, prevención de mareo por movimiento y modelado tridimensional básico.","Además de la interfaz, asume el modelado de baquetas y entorno para descargar la rama de arte."),
 ("Artista y modelador tridimensional","Modelado, texturizado y optimización de geometría para tiempo real.","La geometría debe ejecutarse en un visor autónomo, con presupuesto de polígonos restringido."),
 ("Diseñador de audio","Edición de muestras, capas de intensidad y variación por repetición.","La respuesta sonora por intensidad es una de las medidas de éxito declaradas."),
 ("Analista de métricas","Lectura de literatura científica, definición de indicadores y análisis de resultados.","Sostiene la fundamentación terapéutica y produce el informe final de resultados."),
 ("Asesor terapéutico externo","Fisioterapeuta, terapeuta ocupacional o musicoterapeuta con certificación vigente y experiencia en rehabilitación de miembro superior.","Sin validación profesional las rutinas no pueden presentarse como terapéuticas."),
],widths=[4.0,6.6,5.4],fs=9)

H(doc,"3.4 Estructura organizacional",2)
P(doc,"La estructura es plana, con tres niveles. La dirección decide sobre alcance y presupuesto; la "
  "gerencia y la coordinación mantienen el plan y la operación; los cinco roles técnicos ejecutan. El asesor "
  "externo no depende jerárquicamente del equipo: participa por sesiones y emite dictamen.")
table(doc,["Nivel","Roles","Función"],[
 ("Dirección","Director de proyecto","Decide sobre alcance, presupuesto y aceptación de hitos."),
 ("Gestión","Gerente de proyecto, Coordinador","Mantienen plan, cronograma, riesgos y relación con externos."),
 ("Ejecución","Desarrollador de realidad virtual, Diseñador de interacción, Artista tridimensional, Diseñador de audio, Analista de métricas","Producen los entregables técnicos y de contenido."),
 ("Asesoría externa","Asesor terapéutico","Valida y dictamina. No ejecuta desarrollo."),
],widths=[2.6,7.4,6.0],fs=9.5)

doc.add_page_break()
# ================================================================ 4
H(doc,"4. Plan de implementación",1)

H(doc,"4.1 Enfoque",2)
P(doc,"El desarrollo es incremental y se organiza en cuatro frentes que avanzan en paralelo: fundamentación "
  "terapéutica, modelo tridimensional, interacción y físicas, y audio. Los cuatro convergen en una build "
  "candidata que se somete a pruebas técnicas y a pruebas con usuarios.")
P(doc,"La decisión de arranque es verificar la latencia antes de comprometer el resto del desarrollo. El "
  "paquete 4.2 es una prueba de concepto cuyo único fin es medir el retardo entre el golpe y el sonido en el "
  "hardware objetivo. Se programa en la segunda semana precisamente para que un resultado negativo deje "
  "margen de reacción.")
P(doc,"Sobre la relación entre este documento y la estructura de desglose: conforme a la metodología, la "
  "estructura de desglose del trabajo corresponde formalmente a los procesos de planificación y no a los de "
  "inicio. Se incluye en el acta porque es la base de toda la planificación posterior y porque el cronograma, "
  "el presupuesto y la ruta crítica se derivan de ella; sin la estructura de desglose, el resto del acta no "
  "sería verificable.")

H(doc,"4.2 Estructura de desglose del trabajo",2)
P(doc,"La estructura descompone el proyecto en siete ramas y 42 paquetes de trabajo. Se construyó por "
  "entregables, no por fases, y cumple la regla del 100 %: la suma de los paquetes de cada rama constituye la "
  "totalidad del trabajo de esa rama, y ningún paquete queda fuera de alguna rama. Ningún paquete excede las "
  "80 horas de esfuerzo.")
P(doc,"La estructura no establece secuencia alguna entre sus componentes. La secuencia se define en la "
  "sección 4.5 y se desarrolla en el documento de ruta crítica.")
table(doc,["Código","Rama","Entregable que produce"],[
 ("1","Gestión del proyecto","Documentación de administración: acta, plan, cronograma, riesgos y cierre."),
 ("2","Fundamentación terapéutica","Rutinas validadas, métricas motrices y protocolo de sesión."),
 ("3","Modelo tridimensional y entorno","Geometría optimizada de la batería, las baquetas y el escenario."),
 ("4","Sistema de interacción y físicas","Detección de golpe, medición de intensidad e integración con los modelos."),
 ("5","Sistema de audio y rutinas","Respuesta sonora por intensidad y rutinas ejecutables en el simulador."),
 ("6","Prototipo funcional integrado","Interfaz, registro de métricas y build candidata."),
 ("7","Pruebas y documentación","Informe de pruebas, manual y resultados."),
],widths=[1.5,4.5,10.0],fs=9.5)

H(doc,"4.3 Paquetes de trabajo",2)
P(doc,"Cada paquete incluye su criterio de aceptación, es decir la condición verificable que determina "
  "cuándo está terminado. Un paquete sin criterio de aceptación no se puede dar por cerrado sin discusión.")
rama_actual=None
for cod,nom,cri,res,rec,act,d in edt.PKG:
    r=cod.split(".")[0]
    if r!=rama_actual:
        rama_actual=r
        nombres={"1":"Gestión del proyecto","2":"Fundamentación terapéutica",
                 "3":"Modelo tridimensional y entorno","4":"Sistema de interacción y físicas",
                 "5":"Sistema de audio y rutinas","6":"Prototipo funcional integrado",
                 "7":"Pruebas y documentación"}
        H(doc,f"Rama {r} — {nombres[r]}",3)
        filas=[]
        for c2,n2,cr2,re2,rc2,a2,d2 in edt.PKG:
            if c2.split(".")[0]==r:
                ini,fin=edt.rango(c2)
                filas.append((c2,n2,cr2,re2,rc2,f"{d2} d",f"{edt.fmt(ini)} a {edt.fmt(fin)}"))
        table(doc,["Código","Paquete de trabajo","Criterio de aceptación","Responsable","Rec.","Dur.","Periodo"],
              filas,widths=[1.1,3.4,4.6,2.8,0.9,0.9,2.3],fs=8)

P(doc,"La columna de recursos indica el número de personas asignadas al paquete. La columna de duración se "
  "expresa en días hábiles.",italic=True)

doc.save('/tmp/_acta_b.docx'); print("parte B OK")
