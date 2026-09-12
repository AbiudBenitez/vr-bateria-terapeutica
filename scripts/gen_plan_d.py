# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import rc257 as R, costos as K
doc = Document('/tmp/_plan_c.docx')

doc.add_page_break()
# ======================================================= PARTE III
H(doc,"PARTE III. CERTIFICACIONES EN DIRECCIÓN DE PROYECTOS",1)
P(doc,"Revisión de las principales certificaciones profesionales del área, con sus requisitos, costo y "
  "perfil al que se dirigen. Los montos están en dólares estadounidenses, que es la moneda en que los "
  "organismos emisores publican sus tarifas, y corresponden a 2026.")

H(doc,"16. Panorama general",2)
P(doc,"Las certificaciones del área se agrupan en tres familias. Distinguirlas importa porque responden a "
  "filosofías distintas y no compiten entre sí de forma directa.")
table(doc,["Familia","Enfoque","Organismo","Certificaciones principales"],[
 ("Basadas en cuerpo de conocimiento","Certifican dominio de un conjunto de procesos, herramientas y técnicas. Es el enfoque de la guía PMBOK.","Project Management Institute (PMI), Estados Unidos","CAPM, PMP, PMI-ACP, PMI-RMP, PMI-SP"),
 ("Basadas en método","Certifican la aplicación de un método prescriptivo, con roles y productos definidos.","PeopleCert, Reino Unido","PRINCE2 Foundation y Practitioner"),
 ("Basadas en competencia","Certifican capacidad demostrada mediante evaluación de experiencia real, por niveles.","International Project Management Association (IPMA)","IPMA niveles D, C, B y A"),
 ("Marcos ágiles","Certifican el dominio de un marco de trabajo específico, no de la dirección de proyectos en general.","Scrum.org, Scrum Alliance, Scaled Agile","PSM, CSM, SAFe"),
],widths=[3.4,5.4,3.6,3.6],fs=9)

H(doc,"17. Certificaciones del Project Management Institute",2)
P(doc,"Son las de mayor reconocimiento en México y las que corresponden directamente a la guía PMBOK que "
  "se emplea en esta materia.")
table(doc,["Certificación","Dirigida a","Requisitos","Examen","Costo"],[
 ("CAPM — Certified Associate in Project Management",
  "Estudiantes y personas sin experiencia dirigiendo proyectos. Es la puerta de entrada.",
  "Bachillerato concluido más 23 horas de formación en dirección de proyectos. No exige experiencia dirigiendo proyectos.",
  "150 preguntas, 3 horas. Cubre fundamentos, metodologías predictiva y ágil, y análisis de negocio.",
  "USD $225 miembros · USD $300 no miembros"),
 ("PMP — Project Management Professional",
  "Profesionales con experiencia comprobable dirigiendo proyectos. Es la certificación de referencia del área.",
  "Con título universitario de cuatro años: 36 meses dirigiendo proyectos, equivalentes a 4,500 horas, más 35 horas de formación. Sin título: 60 meses y 7,500 horas.",
  "180 preguntas, 230 minutos. Cubre personas, procesos y entorno de negocio, con enfoques predictivo, ágil e híbrido.",
  "USD $405 miembros · USD $555 no miembros"),
 ("PMI-ACP — Agile Certified Practitioner",
  "Quienes trabajan en entornos ágiles y quieren acreditar dominio de varios marcos, no de uno solo.",
  "Experiencia en proyectos ágiles más formación específica en prácticas ágiles.",
  "Cubre Scrum, Kanban, Lean, programación extrema y otros marcos.",
  "USD $435 miembros · USD $495 no miembros aproximadamente"),
 ("PMI-RMP — Risk Management Professional",
  "Especialistas en gestión de riesgos dentro de proyectos grandes.",
  "Experiencia comprobable en gestión de riesgos más formación específica.",
  "Enfocado exclusivamente en el área de riesgos.",
  "USD $520 miembros · USD $670 no miembros aproximadamente"),
 ("PMI-SP — Scheduling Professional",
  "Especialistas en programación y control de cronogramas. Es la que más se acerca al trabajo de ruta crítica de esta materia.",
  "Experiencia comprobable en desarrollo y control de cronogramas más formación específica.",
  "Enfocado en planificación temporal, red de precedencias, ruta crítica y control del cronograma.",
  "USD $520 miembros · USD $670 no miembros aproximadamente"),
],widths=[3.2,3.6,4.4,3.0,2.0],fs=8)
P(doc,"La membresía del PMI cuesta USD $139 anuales más USD $10 de inscripción inicial. Conviene evaluarla "
  "antes de presentar examen: en el caso del PMP, el ahorro en la cuota del examen supera el costo de la "
  "membresía, de modo que afiliarse resulta más barato que no hacerlo. Además da acceso a la guía PMBOK en "
  "formato digital sin costo adicional.")

H(doc,"18. Otras certificaciones relevantes",2)
table(doc,["Certificación","Organismo","Características","Costo aproximado"],[
 ("PRINCE2 Foundation","PeopleCert","Método prescriptivo de origen británico, muy extendido en Europa y en organismos públicos. Define siete principios, siete temas y siete procesos. No exige experiencia previa.","USD $300 a $500 según el país"),
 ("PRINCE2 Practitioner","PeopleCert","Segundo nivel. Evalúa la capacidad de adaptar el método a un escenario concreto. Requiere tener Foundation.","USD $500 a $700"),
 ("IPMA nivel D","International Project Management Association","Evalúa conocimiento de competencias en dirección de proyectos. Es el nivel de entrada y admite candidatos sin experiencia.","Varía por asociación nacional"),
 ("Professional Scrum Master I (PSM I)","Scrum.org","Certifica dominio del marco Scrum. No caduca ni requiere renovación. No exige curso previo.","USD $200"),
 ("Certified ScrumMaster (CSM)","Scrum Alliance","Equivalente en alcance, pero obliga a tomar un curso oficial de dos días y a renovar cada dos años.","USD $1,000 a $1,400, curso incluido"),
],widths=[3.4,3.2,7.0,2.4],fs=9)

H(doc,"19. Recomendación para el equipo",2)
P(doc,"La certificación pertinente para el perfil del equipo es la CAPM, por tres razones concretas.")
bullets(doc,[
 "No exige experiencia dirigiendo proyectos. El PMP pide 36 meses con título universitario, lo que lo "
 "vuelve inalcanzable para quien todavía está estudiando.",
 "Su requisito de 23 horas de formación en dirección de proyectos se cubre en buena medida con esta "
 "misma unidad de aprendizaje, siempre que se documente el contenido y la carga horaria.",
 "Su temario coincide con lo que este proyecto ya aplicó: estructura de desglose del trabajo, red de "
 "precedencias, ruta crítica, estimación ascendente de costos, gestión de la calidad y gestión de riesgos.",
],num=True)
table(doc,["Momento","Recomendación"],[
 ("Durante la carrera","CAPM. Es la única del PMI accesible sin experiencia, y convalida la formación de esta materia."),
 ("Primer empleo","PSM I si el entorno de trabajo es ágil. Cuesta USD $200, no caduca y no obliga a tomar curso."),
 ("A los tres años de ejercicio","PMP, una vez acumuladas las 4,500 horas dirigiendo proyectos que exige con título universitario."),
 ("Especialización posterior","PMI-SP para quien se incline por la planificación y el control de cronogramas, que es el terreno del trabajo de ruta crítica; PMI-RMP para quien se incline por la gestión de riesgos."),
],widths=[3.6,12.4],fs=9.5)
P(doc,"Una advertencia sobre el valor de las certificaciones: acreditan conocimiento del vocabulario y de "
  "los procesos, no capacidad de dirigir. El PMI lo reconoce al exigir experiencia comprobable para el PMP "
  "y no solo un examen. Para un egresado, la certificación abre la puerta a entrevistas; lo que sostiene la "
  "carrera es haber ejecutado proyectos reales.")

doc.add_page_break()
H(doc,"20. Fuentes",1)
table(doc,["Fuente","Contenido"],[
 ("Project Management Institute, pmi.org","Requisitos y cuotas vigentes de CAPM, PMP, PMI-ACP, PMI-RMP y PMI-SP, y de la membresía anual."),
 ("PeopleCert, peoplecert.org","Requisitos y cuotas de PRINCE2 Foundation y Practitioner."),
 ("Scrum.org y Scrum Alliance","Requisitos y cuotas de PSM I y CSM."),
 ("International Project Management Association, ipma.world","Esquema de certificación por niveles D a A."),
 ("Guía de los Fundamentos para la Dirección de Proyectos (Guía del PMBOK), Project Management Institute","Marco de referencia de las áreas 8 y 11, que sustentan las partes I y II de este documento."),
],widths=[5.6,10.4],fs=9.5)
P(doc,"Los costos de examen se consultaron en septiembre de 2026 y los organismos emisores los actualizan "
  "periódicamente. Conviene verificarlos en el sitio oficial antes de inscribirse.",italic=True)

out="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/Plan_Calidad_Plan_Riesgos.docx"
doc.save(out); print("OK", out)
print("párrafos:",len(doc.paragraphs)," tablas:",len(doc.tables)," imágenes:",len(doc.inline_shapes))
