# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
import rc257 as R, costos as K
M = R.V2
def d(x): return f"${x:,.0f}"
c = K.corte(9.0)
TERM = set(c["terminadas"]); CURSO = set(c["en_curso"])

# entregable tangible por area
ENTREGA = {
 "D": ("Batería virtual funcional con detección de golpe",
   ["Proyecto Unity configurado con el kit de desarrollo de realidad virtual, seguimiento de cabeza y controles",
    "Baquetas sujetables con física ajustada",
    "Batería con sus componentes interactivos y detección de qué pieza fue golpeada",
    "Medición de velocidad de la baqueta convertida en tres niveles de intensidad",
    "Respuesta háptica proporcional a la fuerza del golpe",
    "Evento DrumHit que informa instrumento, intensidad y momento, y que consume el resto del sistema"],
   "Se toca la batería en el visor y cada golpe se registra con su pieza y su intensidad."),
 "J": ("Sistema de ritmo con puntuación",
   ["Reloj musical independiente de la tasa de cuadros",
    "Cálculo de tempo, compases y subdivisiones rítmicas",
    "Estructura de datos de canciones y mapas de notas",
    "Ventanas de precisión con detección de golpe anticipado, atrasado y nota no golpeada",
    "Puntuación, sistema de combo y cálculo de precisión porcentual",
    "Respuesta sonora inmediata de acierto y error"],
   "Se ejecuta una secuencia rítmica y el sistema califica cada golpe."),
 "E": ("Fundamentación terapéutica y guion de la experiencia",
   ["Objetivo y alcance terapéutico definidos y delimitados",
    "Matriz bibliográfica con los estudios que sustentan la propuesta",
    "Emociones, actividades y duración de sesión determinadas",
    "Guion del tutorial introductorio, de la actividad y del cierre",
    "Flujo completo de la experiencia, de inicio a fin",
    "Fundamentación teórica redactada"],
   "Documento de fundamentación y guion, listo para revisión."),
 "M": ("Marco musical del proyecto",
   ["Características musicales adecuadas a la experiencia, investigadas y documentadas",
    "Tempos y patrones rítmicos apropiados para principiantes, analizados",
    "Estilos musicales del proyecto definidos",
    "Decisión y verificación de licencias de las pistas"],
   "Documento de criterios musicales con las licencias resueltas."),
 "S": ("Biblioteca de sonidos lista para integrar",
   ["Fuentes de sonido identificadas y seleccionadas",
    "Muestras de cada componente en tres niveles de intensidad",
    "Muestras editadas, sin ruido, con inicio y final ajustados para evitar retrasos",
    "Volúmenes normalizados y exportados en el formato del motor",
    "Mezclador de audio creado en Unity con canales separados de batería, música, ambiente e interfaz"],
   "Se reproduce cada sonido desde el motor, con sus niveles de intensidad."),
 "I": ("Diseño del tutorial visual",
   ["Tutorial visual de cómo sujetar las baquetas",
    "Tutorial visual de cómo seguir el ritmo"],
   "Bocetos del tutorial. El resto de la interfaz arranca después por diseño de la red."),
 "A": ("Dirección artística del entorno",
   ["Investigación de entornos que favorecen la experiencia propuesta",
    "Comparación de ambientes candidatos",
    "Dirección artística general del escenario definida",
    "Teoría del color aplicada a la percepción emocional, investigada",
    "Límites de polígonos y criterios de rendimiento establecidos"],
   "Documento de dirección artística con referencias visuales."),
 "Q": ("Planeación completa del proyecto",
   ["Acta, alcance y estructura de desglose del trabajo",
    "Lista de 257 actividades con duración, dependencia y responsable",
    "Cronograma y diagrama de Gantt",
    "Red de precedencias y ruta crítica identificada",
    "Matriz de trazabilidad entre requisitos y funcionalidades",
    "Planes de prueba de batería, de ritmo, de interfaz y de audio",
    "Registro de riesgos y análisis de costos"],
   "Documentación de planeación completa, más el cronograma cargado en ProjectLibre."),
}

doc = nuevo()
portada(doc,
 "ENTREGABLE DE MEDIO CURSO",
 "Simulación VR de batería con juego de ritmo",
 [("Unidad de aprendizaje","Administración de Proyectos de Software"),
  ("Docente","Dra. Leticia Amalia Neira Tovar"),
  ("Equipo","Equipo A"),
  ("Fecha de entrega","Lunes 21 de septiembre de 2026"),
  ("Fecha de corte del avance",f"Viernes {K.fecha(8):%d de %B de %Y}"),
  ("Avance comprometido",f"{len(TERM)} de 257 actividades  ·  {100*c['horas']/K.HORAS_TOT:.0f} % del esfuerzo")],
 sub2="Compromiso de entrega derivado del cronograma del proyecto")

H(doc,"1. Alcance de esta entrega",1)
P(doc,"Este documento declara qué entrega el equipo el lunes 21 de septiembre. El compromiso no es una "
  "estimación optimista: se deriva del cronograma del proyecto, tomando como corte el cierre del viernes "
  f"{K.fecha(8):%d de %B}, que es el último día hábil previo a la entrega.")
P(doc,"El proyecto arrancó el 7 de septiembre y concluye el 30 de octubre, con una red de 38.25 días "
  "hábiles. Al corte de esta entrega se habrán recorrido 9 de esos días.")
table(doc,["Concepto","Valor"],[
 ("Actividades terminadas al corte",f"{len(TERM)} de 257"),
 ("Actividades en curso",f"{len(CURSO)}"),
 ("Esfuerzo completado",f"{c['horas']:,.0f} de {K.HORAS_TOT:,.0f} horas  ({100*c['horas']/K.HORAS_TOT:.0f} %)"),
 ("Valor planificado a la fecha",d(c["PV"])),
 ("Valor ganado a la fecha",d(c["EV"])),
 ("Índice de desempeño del cronograma",f"{c['EV']/c['PV']:.3f}"),
],widths=[8.0,8.0],fs=10)
P(doc,f"El índice de desempeño del cronograma es {c['EV']/c['PV']:.3f}, es decir que el proyecto habrá "
  f"producido el {100*c['EV']/c['PV']:.1f} % del valor que el plan preveía para esa fecha. La desviación "
  "equivale a menos de medio día hábil de trabajo del equipo completo.")

H(doc,"2. El entregable en una frase",1)
P(doc,"Un prototipo jugable de batería en realidad virtual, con detección de golpe e intensidad, sistema de "
  "ritmo con puntuación y biblioteca de sonidos integrada, acompañado de la documentación de planeación del "
  "proyecto completa.", bold=True)
P(doc,"Es decir: se puede tomar el visor, golpear la batería, escuchar el sonido correspondiente a la pieza "
  "y a la fuerza del golpe, y ver la calificación de precisión. Lo que todavía no existe es el entorno "
  "tridimensional definitivo, la interfaz de usuario y la integración de las rutinas terapéuticas.")

doc.add_page_break()
H(doc,"3. Entregables por área",1)
for s in "DJSEMAIQ":
    a = [x for x in R.AREAS if R.SIGLA[x]==s][0]
    tit, items, demo = ENTREGA[s]
    ks = sorted([k for k in TERM if R.T[k]["sig"]==s])
    H(doc, f"{s} · {a} — {R.RESP[a]}", 2)
    P(doc, tit, bold=True, after=4)
    bullets(doc, items)
    table(doc,["Concepto","Detalle"],[
     ("Actividades terminadas al corte", f"{len(ks)} de {R.NTAR[a]}"),
     ("Claves que lo respaldan", ", ".join(ks) if len(ks)<=40 else ", ".join(ks[:40])+" …"),
     ("Cómo se verifica", demo),
    ],widths=[4.0,12.0],fs=9)

doc.add_page_break()
H(doc,"4. Demostración en vivo",1)
P(doc,"Se propone demostrar en el siguiente orden, que sigue el flujo del propio sistema.")
table(doc,["#","Qué se muestra","Quién","Duración"],[
 ("1","Puesta del visor y calibración de altura. Se toman las baquetas.","Misael","1 min"),
 ("2","Golpes sobre cada componente de la batería. Se señala cómo el sistema identifica la pieza y distingue tres niveles de intensidad, con respuesta háptica.","Misael","3 min"),
 ("3","Respuesta sonora: se escucha cómo el sonido corresponde a la pieza y cambia con la fuerza del golpe.","Christian","2 min"),
 ("4","Ejecución de una secuencia rítmica. Se muestran las ventanas de precisión, la puntuación y el combo.","Benjamín","3 min"),
 ("5","Recorrido por la documentación de planeación: estructura de desglose, red de precedencias, ruta crítica y cronograma en ProjectLibre.","Diana","4 min"),
 ("6","Fundamentación terapéutica y guion de la experiencia. Criterios musicales y dirección artística del entorno.","María, Javier y Kimberly","4 min"),
],widths=[0.8,8.6,3.6,2.0],fs=9.5)
P(doc,"Duración total estimada: 17 minutos. Conviene tener el visor conectado y con la aplicación instalada "
  "antes de comenzar, y una segunda pantalla que replique lo que ve quien lo usa.")

H(doc,"5. Lo que no se entrega y por qué",1)
P(doc,"Declarar lo que falta evita que se interprete como retraso lo que es secuencia planificada.")
table(doc,["Componente","Estado al corte","Cuándo llega","Por qué no antes"],[
 ("Entorno tridimensional definitivo","Solo dirección artística y criterios de rendimiento","Semanas 4 a 6",
  "Su cadena tiene 17 actividades estrictamente seriales y es la ruta crítica del proyecto. No admite adelanto sin comprometer la calidad del resultado."),
 ("Interfaz de usuario y menús","Solo los bocetos del tutorial","Semanas 5 a 7",
  "La interfaz se construye sobre el esquema de interacción ya integrado. Diseñarla antes obligaría a rehacerla."),
 ("Rutinas terapéuticas dentro del simulador","Guion y flujo definidos, sin implementar","Semanas 5 a 6",
  "Requieren que el sistema de audio esté integrado con la física, cosa que ocurre después de este corte."),
 ("Pruebas con usuarios","Planes de prueba redactados","Semana 7",
  "Necesitan el prototipo integrado completo."),
],widths=[3.4,4.2,2.4,6.0],fs=9)
P(doc,"Conviene anticipar una observación: el área de interfaz aparece con solo dos actividades terminadas, "
  "frente a veintisiete de desarrollo o veintidós de ritmo. No es retraso. La red de precedencias hace que "
  "la interfaz arranque después, porque se diseña sobre una interacción que ya funciona. Adelantarla "
  "produciría trabajo que habría que rehacer.")

H(doc,"6. Estado del proyecto al corte",1)
table(doc,["Área","Responsable","Terminadas","Del total","% del área"],
 [(a, R.RESP[a], sum(1 for k in TERM if R.T[k]["area"]==a), R.NTAR[a],
   f"{100*sum(1 for k in TERM if R.T[k]['area']==a)/R.NTAR[a]:.0f} %")
  for a in sorted(R.AREAS, key=lambda x: -sum(1 for k in TERM if R.T[k]["area"]==x))],
 widths=[5.4,3.0,2.4,2.2,3.0],fs=9.5)
P(doc,"El proyecto continúa después de esta entrega con la construcción del entorno tridimensional, la "
  "interfaz de usuario, la integración de las rutinas terapéuticas y las pruebas con usuarios, para concluir "
  "el 30 de octubre.")

out="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/Entregable_Medio_Curso_21sep.docx"
doc.save(out); print("OK", out)
print("párrafos:",len(doc.paragraphs)," tablas:",len(doc.tables))
