# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
import pmbok as PB

FALTA = "[COMPLETAR]"
doc = nuevo(fuente='Arial', tam=12)

# ---------------------------------------------------------------- portada
for _ in range(3): doc.add_paragraph()
P(doc,"UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN",bold=True,size=13,align=C,after=2)
P(doc,"FACULTAD DE INGENIERÍA MECÁNICA Y ELÉCTRICA",bold=True,size=12,align=C,after=34)
P(doc,"ELEMENTOS DE ESTUDIO DE LA GUÍA DEL PMBOK",bold=True,size=17,align=C,after=8)
P(doc,"Estructura del método, entradas y salidas por grupo de procesos",size=13,align=C,after=6)
P(doc,"Actividad individual",italic=True,size=12,align=C,after=40)
for etq, val in [
 ("Nombre","Abiud Misael Benítez Franco"),
 ("Matrícula",FALTA),
 ("Grupo",FALTA),
 ("Nombre del profesor","Dra. Leticia Amalia Neira Tovar"),
 ("Nombre del curso","Administración de Proyectos de Software"),
 ("Módulo",FALTA),
 ("Actividad",FALTA),
 ("Equipo","Equipo A"),
 ("Título del proyecto","Simulación de batería en realidad virtual con juego de ritmo"),
 ("Fecha","14 de septiembre de 2026"),
]:
    campo(doc, etq, val, after=6)
doc.add_page_break()

# ================================================================ 1
H(doc,"1. Objetivo",1)
P(doc,"Identificar y describir la estructura del método propuesto por la Guía de los Fundamentos para la "
  "Dirección de Proyectos, conocida como Guía del PMBOK, mediante una tabla que relacione sus elementos de "
  "estudio y detalle las entradas y las salidas características de cada uno de los cinco grupos de procesos.")
P(doc,"De manera específica, la actividad persigue tres propósitos:")
bullets(doc,[
 "Comprender cómo el estándar organiza la dirección de proyectos en dos dimensiones simultáneas: los grupos "
 "de procesos, que responden a cuándo se hace el trabajo, y las áreas de conocimiento, que responden a qué "
 "se gestiona.",
 "Describir, para cada grupo de procesos, qué información recibe y qué documentos produce, de modo que se "
 "haga visible el encadenamiento entre ellos.",
 "Contrastar esa estructura teórica con la documentación que el equipo ha producido en el proyecto de la "
 "unidad de aprendizaje, para verificar qué procesos se han ejecutado realmente y cuáles siguen pendientes.",
],num=True)

# ================================================================ 2
H(doc,"2. Introducción",1)
H(doc,"2.1 Qué es la Guía del PMBOK",2)
P(doc,"La Guía de los Fundamentos para la Dirección de Proyectos es el estándar que publica el Project "
  "Management Institute, organismo fundado en 1969 en Estados Unidos. No es un manual de instrucciones ni "
  "una metodología que deba seguirse al pie de la letra: es un cuerpo de conocimiento que recopila las "
  "prácticas que la profesión ha reconocido como generalmente aceptadas, y que cada organización adapta a "
  "sus propias condiciones.")
P(doc,"Esa distinción importa. Un estándar describe qué se considera buena práctica; una metodología "
  "prescribe cómo hacerlo. El PMBOK es lo primero. Por eso conviven con él métodos concretos como PRINCE2 o "
  "los marcos ágiles, que resuelven el cómo dentro del mismo marco conceptual.")

H(doc,"2.2 Antecedentes y evolución del estándar",2)
P(doc,"La primera versión del documento apareció en 1987 como un informe interno del instituto. Desde "
  "entonces ha pasado por varias ediciones, y cada una ha respondido a un cambio en la forma de trabajar de "
  "la profesión.")
table(doc,["Edición","Año","Aportación principal"],[
 ("Primera","1996","Formaliza el cuerpo de conocimiento y establece la idea de grupos de procesos."),
 ("Cuarta","2008","Consolida el modelo de entradas, herramientas y salidas para describir cada proceso."),
 ("Quinta","2013","Incorpora la gestión de los interesados como área de conocimiento independiente."),
 ("Sexta","2017","Renombra la gestión del tiempo como gestión del cronograma y la de recursos humanos como gestión de recursos. Queda con 49 procesos, 5 grupos y 10 áreas. Es la edición sobre la que se estructura este trabajo."),
 ("Séptima","2021","Cambia de raíz el enfoque: sustituye las diez áreas de conocimiento por ocho dominios de desempeño y doce principios. Deja de estar centrada en procesos y pasa a estarlo en la entrega de valor."),
 ("Octava","2026","Publicada el 13 de enero de 2026. Simplifica a seis principios y siete dominios de desempeño, y reincorpora procesos accionables, buscando un punto intermedio entre el enfoque de la sexta y el de la séptima edición."),
],widths=[2.0,1.4,12.6],fs=10)
P(doc,"Este trabajo se estructura sobre la sexta edición por una razón concreta: es la única que describe "
  "cada proceso mediante entradas, herramientas y salidas, que es precisamente lo que la actividad solicita. "
  "La séptima edición, al abandonar el enfoque de procesos, no ofrece ese nivel de detalle. La sección 3.7 "
  "documenta esa evolución para dejar constancia de cuál es el estado vigente del estándar.")

H(doc,"2.3 Contexto de la actividad",2)
P(doc,"Esta actividad se desarrolla de forma paralela al proyecto de la unidad de aprendizaje, en el que el "
  "Equipo A construye un simulador de batería en realidad virtual con un módulo de juego de ritmo. A lo "
  "largo del semestre el equipo ha producido acta constitutiva, estructura de desglose del trabajo, "
  "cronograma, red de precedencias, análisis de costos y registro de riesgos.")
P(doc,"Esa circunstancia permite que el trabajo no se limite a describir el estándar, sino que compruebe la "
  "correspondencia entre los procesos que el PMBOK enuncia y los documentos que efectivamente se han "
  "elaborado. Ese contraste se presenta en la sección 5.")

doc.add_page_break()
doc.save('/tmp/_tarea_a.docx'); print("A OK")
