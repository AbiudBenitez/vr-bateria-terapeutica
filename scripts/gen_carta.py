# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *

doc = nuevo()
portada(doc,
    "CARTA SPONSOR",
    "Simulación de batería en realidad virtual\ncon enfoque de musicoterapia",
    [("Título del proyecto","Simulación de batería en realidad virtual con enfoque de musicoterapia"),
     ("Fecha / Revisión","3 de septiembre de 2026  ·  Revisión 2"),
     ("Revisión que sustituye","Revisión 1 del 27 de agosto de 2026"),
     ("Unidad de aprendizaje","Administración de Proyectos de Software"),
     ("Docente","Dra. Leticia Amalia Neira Tovar"),
     ("Equipo","Equipo A"),
     ("Periodo del proyecto","1 de septiembre al 13 de noviembre de 2026")],
    sub2="Revisión 2  —  reorientación del proyecto a un fin terapéutico")

# ---------------------------------------------------------------- 1
H(doc,"1. Motivo de la revisión",1)
P(doc,"La revisión 1 de esta carta planteaba una simulación de batería en realidad virtual con un fin "
  "principalmente demostrativo: reproducir la experiencia de tocar el instrumento. La revisión 2 conserva "
  "íntegramente esa base técnica y le agrega un propósito terapéutico, que pasa a ser el fin principal del "
  "proyecto.")
P(doc,"El cambio responde a tres razones:")
bullets(doc,[
 "El proyecto necesitaba un problema real que resolver. Una simulación de batería sin destinatario definido "
 "es un ejercicio técnico; una simulación diseñada para rehabilitación motriz tiene usuario, criterio de "
 "éxito medible y valor demostrable.",
 "Existe evidencia clínica consolidada que respalda el uso de la percusión con fines terapéuticos. La "
 "estimulación auditiva rítmica y la ejecución instrumental terapéutica son técnicas reconocidas dentro de "
 "la musicoterapia neurológica, con protocolos publicados y resultados replicados.",
 "El enfoque terapéutico permite definir métricas objetivas de éxito (precisión temporal, amplitud de "
 "movimiento, constancia del pulso) que sustituyen a criterios subjetivos como «que se sienta realista».",
])
P(doc,"Los objetivos de esta revisión son los mismos entregables técnicos de la revisión 1, más el diseño y la "
  "validación de las rutinas terapéuticas que se ejecutan dentro del simulador.")

table(doc,["Concepto","Revisión 1","Revisión 2"],[
 ("Fin del proyecto","Experiencia musical interactiva","Herramienta de apoyo a la rehabilitación motriz, con beneficio emocional secundario"),
 ("Usuario objetivo","No definido","Persona en proceso de rehabilitación motriz de miembro superior, bajo supervisión de un terapeuta"),
 ("Validación","Pruebas funcionales del equipo","Pruebas funcionales más validación clínica de un asesor terapéutico externo"),
 ("Periodo","1 sep – 26 oct 2026 (4 meses declarados, inconsistente)","1 sep – 13 nov 2026 (11 semanas, verificado contra el cronograma)"),
 ("Presupuesto","$460,000 MXN","$384,201 MXN"),
 ("Equipo","5 roles","8 roles internos más un asesor terapéutico externo"),
],widths=[3.4,5.6,7.0],fs=9.5)

# ---------------------------------------------------------------- 2
H(doc,"2. Beneficios para la institución",1)
table(doc,["Beneficio","Descripción"],[
 ("Aplicación con destinatario real",
  "El proyecto deja de ser una demostración tecnológica y se convierte en una herramienta de apoyo a la "
  "terapia de rehabilitación motriz de miembro superior, con un usuario y un contexto de uso definidos."),
 ("Respaldo en evidencia clínica",
  "El diseño se apoya en técnicas documentadas de musicoterapia neurológica: estimulación auditiva rítmica, "
  "ejecución instrumental terapéutica y realce sensorial por patrones. El proyecto no inventa un método: "
  "traslada a realidad virtual protocolos ya validados."),
 ("Accesibilidad y costo de la terapia",
  "Un equipo de percusión completo es costoso, ocupa espacio y es difícil de graduar en dificultad. El "
  "simulador reproduce el instrumento, permite ajustar la exigencia sesión por sesión y registra "
  "automáticamente el desempeño del paciente."),
 ("Medición objetiva del avance",
  "El sistema registra precisión temporal respecto al pulso, amplitud del movimiento y constancia entre "
  "sesiones. El terapeuta obtiene datos cuantitativos donde antes había apreciación cualitativa."),
 ("Innovación tecnológica aplicada",
  "Integra realidad virtual autónoma, física de colisiones, audio de baja latencia y registro de métricas "
  "en un mismo producto, sobre hardware de consumo accesible."),
 ("Base para trabajos posteriores",
  "La arquitectura de detección de golpe, medición de velocidad y disparo de audio es reutilizable para "
  "otros instrumentos de percusión y para otras rutinas terapéuticas."),
],widths=[4.2,11.8],fs=9.5)

# ---------------------------------------------------------------- 3
H(doc,"3. Documentos y productos esperados",1)
P(doc,"Se conservan los siete productos de la revisión 1 y se agregan cuatro derivados del enfoque terapéutico.")
H(doc,"3.1 Productos técnicos",2)
table(doc,["#","Producto","Descripción"],[
 ("1","Prototipo funcional","Simulación de realidad virtual ejecutable en visor autónomo, que permite visualizar e interactuar con una batería virtual."),
 ("2","Modelo virtual de la batería","Representación tridimensional optimizada de los componentes principales de una batería y de las baquetas."),
 ("3","Sistema de interacción","Detección de contacto entre baquetas virtuales y componentes de la batería, con medición de la velocidad de impacto."),
 ("4","Sistema de reproducción de audio","Disparo del sonido correspondiente a cada componente, con capas de intensidad según la fuerza del golpe."),
 ("5","Entorno virtual","Escenario tridimensional adecuado para la ejecución, diseñado para no producir fatiga ni mareo por movimiento."),
 ("6","Documentación técnica","Registro del desarrollo, la configuración y el funcionamiento de la simulación."),
 ("7","Informe de pruebas","Evidencia de las pruebas de interacción, detección de golpes y reproducción de sonido."),
],widths=[0.9,4.0,11.1],fs=9.5)
H(doc,"3.2 Productos del enfoque terapéutico",2)
table(doc,["#","Producto","Descripción"],[
 ("8","Rutinas rítmicas terapéuticas","Conjunto de ejercicios graduados por dificultad, diseñados sobre protocolos de musicoterapia neurológica y validados por el asesor terapéutico."),
 ("9","Protocolo de sesión","Documento que define duración, progresión, criterios de suspensión y consentimiento informado para las pruebas con usuarios."),
 ("10","Módulo de registro de métricas","Componente que registra precisión temporal, amplitud de movimiento y constancia del pulso por sesión, y los exporta para su análisis."),
 ("11","Informe de validación terapéutica","Dictamen del asesor externo sobre la pertinencia clínica de las rutinas y de las métricas implementadas."),
],widths=[0.9,4.0,11.1],fs=9.5)

# ---------------------------------------------------------------- 4
H(doc,"4. Medidas de éxito",1)
P(doc,"Cada medida se expresa con un criterio verificable. Las seis primeras provienen de la revisión 1; las "
  "cuatro últimas se agregan por el enfoque terapéutico.")
table(doc,["#","Medida de éxito","Criterio de verificación"],[
 ("1","Identificación de componentes","El usuario distingue y alcanza los componentes de la batería sin indicación externa."),
 ("2","Detección de contacto","El sistema registra el golpe en el componente correcto en al menos el 95 % de los intentos."),
 ("3","Correspondencia del sonido","El sonido reproducido corresponde siempre al componente golpeado."),
 ("4","Latencia","El retardo entre el golpe y el sonido se mantiene por debajo de 30 milisegundos."),
 ("5","Estabilidad","La simulación sostiene 72 cuadros por segundo durante una sesión completa sin caídas ni cierres inesperados."),
 ("6","Interacción intuitiva","Un usuario sin experiencia previa comprende el uso sin instrucción escrita."),
 ("7","Sensibilidad a la intensidad","El sistema distingue golpe suave, medio y fuerte a partir de la velocidad de la baqueta y modifica la intensidad del sonido en consecuencia."),
 ("8","Pertinencia terapéutica","El asesor externo dictamina que las rutinas implementadas corresponden a protocolos reconocidos de musicoterapia."),
 ("9","Registro de métricas","El sistema exporta, por sesión, precisión temporal, amplitud de movimiento y constancia del pulso."),
 ("10","Seguridad de uso","Ningún participante de las pruebas reporta mareo, fatiga ni molestia articular atribuible al uso del simulador."),
],widths=[0.9,4.6,10.5],fs=9.5)

# ---------------------------------------------------------------- 5
H(doc,"5. Prioridad",1)
P(doc,"Alta. El proyecto aplica conocimientos de modelado tridimensional, programación de interacción, "
  "procesamiento de audio y simulación en un producto con destinatario real. El enfoque terapéutico eleva la "
  "prioridad respecto de la revisión 1: el resultado no es únicamente una demostración técnica, sino una "
  "herramienta de apoyo a un proceso de rehabilitación, con criterios de éxito medibles y validación externa.")

# ---------------------------------------------------------------- 6
H(doc,"6. Fechas clave",1)
P(doc,"El proyecto se desarrolla en 11 semanas, del 1 de septiembre al 13 de noviembre de 2026. Los exámenes "
  "del semestre inician el 23 de noviembre; la semana del 16 al 20 de noviembre se reserva como colchón de "
  "gestión y no contiene trabajo programado.")
P(doc,"Las etapas se traslapan entre sí. Esto es deliberado: el cronograma aplica compresión por traslape para "
  "caber en la ventana académica disponible, y el traslape solo se aplica entre actividades que pueden "
  "avanzar en paralelo sin dependencia estricta. El detalle de qué puede ejecutarse simultáneamente está en "
  "el acta constitutiva y en el documento de ruta crítica.")
table(doc,["Etapa","Periodo","Duración","Objetivo principal"],[
 ("1. Planeación y diseño conceptual","1 – 11 sep 2026","2 semanas",
  "Definir alcance, estructura de desglose del trabajo, cronograma y riesgos. Establecer referencias visuales del instrumento y confirmar al asesor terapéutico."),
 ("2. Modelado y entorno tridimensional","7 sep – 5 oct 2026","4 semanas",
  "Modelar batería, baquetas y escenario; texturizar y optimizar la geometría para su ejecución en visor autónomo."),
 ("3. Interacción, físicas y audio","8 sep – 20 oct 2026","6 semanas",
  "Configurar el entorno de desarrollo, verificar la latencia, programar colisiones, medición de velocidad de impacto y disparo de audio por intensidad."),
 ("4. Rutinas terapéuticas e integración","14 oct – 3 nov 2026","3 semanas",
  "Implementar las rutinas rítmicas validadas, la guía visual, los menús, la interfaz y el registro de métricas. Producir la build candidata."),
 ("5. Pruebas, corrección y cierre","21 oct – 13 nov 2026","4 semanas",
  "Ejecutar pruebas de rendimiento y latencia, pruebas con usuarios bajo el protocolo validado, corregir defectos y entregar documentación."),
 ("Reserva de gestión","16 – 20 nov 2026","1 semana",
  "Colchón previo al inicio de exámenes. Sin trabajo programado."),
],widths=[3.6,2.6,1.9,7.9],fs=9.5)

H(doc,"6.1 Hitos de control",2)
table(doc,["Hito","Fecha","Qué se verifica"],[
 ("H1  Diseño conceptual aprobado","11 sep 2026","Alcance, estructura de desglose del trabajo y referencias visuales aprobadas."),
 ("H2  Go / No-Go de latencia","14 sep 2026","Se comprueba que el retardo entre golpe y sonido se mantiene por debajo de 30 ms en el hardware objetivo. Si no se cumple, se revisa el alcance antes de continuar."),
 ("H3  Modelos integrados con físicas","13 oct 2026","La batería modelada responde a las colisiones y a la medición de velocidad."),
 ("H4  Rutinas y métricas integradas","27 oct 2026","Las rutinas validadas y el registro de métricas operan dentro del simulador."),
 ("H5  Build candidata congelada","3 nov 2026","Versión estable sobre la que se ejecutan las pruebas con usuarios."),
 ("H6  Cierre","13 nov 2026","Pruebas cerradas, defectos corregidos y documentación entregada."),
],widths=[4.4,2.4,9.2],fs=9.5)

# ---------------------------------------------------------------- 7
H(doc,"7. Equipo de proyecto y presupuesto",1)
P(doc,"El presupuesto de la revisión 1 estimaba $460,000 MXN sobre cuatro meses de trabajo y cinco roles a "
  "dedicación completa. Esa estimación tenía dos defectos: el periodo de cuatro meses no coincidía con el "
  "cronograma, que terminaba el 26 de octubre, y suponía dedicación de tiempo completo para un equipo que "
  "trabaja por asignación parcial.")
P(doc,"La revisión 2 recalcula el presupuesto sobre el periodo real de 11 semanas, con el porcentaje de "
  "esfuerzo que cada rol dedica efectivamente al proyecto y con tarifas por hora derivadas del salario "
  "mensual de mercado en el área metropolitana de Monterrey para 2026, dividido entre 173.33 horas laborables "
  "al mes. El resultado es menor que la estimación anterior pese a incorporar tres roles adicionales y un "
  "asesor externo.")

H(doc,"7.1 Costo de personal",2)
table(doc,["Rol","Costo por hora","Esfuerzo","Semanas","Horas","Costo (MXN)"],[
 ("Director de proyecto","$375","25 %","11","110","$41,250"),
 ("Gerente de proyecto","$277","40 %","11","176","$48,752"),
 ("Coordinador","$173","40 %","11","176","$30,448"),
 ("Desarrollador de realidad virtual","$260","70 %","9","252","$65,520"),
 ("Diseñador de interacción / UX-XR","$219","50 %","8","160","$35,040"),
 ("Artista y modelador 3D","$185","50 %","7","140","$25,900"),
 ("Diseñador de audio","$162","40 %","6","96","$15,552"),
 ("Analista de métricas","$196","30 %","7","84","$16,464"),
 ("Subtotal equipo interno","","","","1,194 h","$278,926"),
 ("Asesor terapéutico externo","$900","por sesión","—","24 h","$21,600"),
 ("Total de personal","","","","1,218 h","$300,526"),
],widths=[5.4,2.3,1.8,1.8,1.8,2.9],fs=9.5,negritas_col0=False)

H(doc,"7.2 Costos no laborales",2)
table(doc,["Concepto","Detalle","Costo (MXN)"],[
 ("Visor Meta Quest 3","Equipo principal de desarrollo y pruebas","$11,999"),
 ("Visor Meta Quest 3S","Segundo equipo, para pruebas de compatibilidad y sesiones simultáneas","$6,999"),
 ("Depreciación de equipo de cómputo","Parte proporcional del uso de las estaciones de trabajo durante el periodo","$8,000"),
 ("Periféricos y accesorios","Cables, soportes, protectores faciales y baterías","$2,500"),
 ("Recursos gráficos con licencia","Modelos, texturas y materiales adquiridos","$4,500"),
 ("Librería de muestras de audio","Grabaciones de percusión con licencia de uso","$3,000"),
 ("Traslados y logística","Sesiones con el asesor terapéutico y pruebas con usuarios","$6,000"),
 ("Consumibles e impresión","Documentación, formatos de consentimiento y material de pruebas","$1,500"),
 ("Servicios digitales","Almacenamiento, control de versiones y herramientas de colaboración","$2,250"),
 ("Imprevistos menores de operación","Gastos operativos no clasificados","$2,000"),
 ("Total de costos no laborales","","$48,748"),
],widths=[5.2,8.0,2.8],fs=9.5)

H(doc,"7.3 Resumen del presupuesto",2)
table(doc,["Concepto","Monto (MXN)"],[
 ("Personal (equipo interno y asesor externo)","$300,526"),
 ("Costos no laborales","$48,748"),
 ("Subtotal de costos directos","$349,274"),
 ("Reserva de contingencia (10 % de los costos directos)","$34,927"),
 ("Presupuesto total del proyecto","$384,201"),
],widths=[10.0,6.0,],fs=10)
P(doc,"Diferencia respecto de la revisión 1: $75,799 menos, equivalente a una reducción del 16.5 %. La "
  "reducción proviene de calcular el esfuerzo real por rol en lugar de suponer dedicación completa, y de "
  "ajustar el periodo a las 11 semanas verificadas contra el cronograma.")
P(doc,"La reserva de contingencia cubre desviaciones dentro del alcance aprobado. El riesgo con mayor "
  "impacto sobre el presupuesto es no alcanzar el umbral de latencia de 30 ms en el hito H2, lo que obligaría "
  "a revisar el alcance del sistema de audio; por eso ese hito se coloca en la segunda semana, cuando aún es "
  "posible reaccionar.")

# ---------------------------------------------------------------- 8
H(doc,"8. Recurso externo requerido",1)
P(doc,"El proyecto requiere un asesor terapéutico externo. Es un requisito y no una mejora opcional: sin "
  "validación profesional, las rutinas implementadas no pueden presentarse como terapéuticas y el proyecto "
  "regresaría al alcance de la revisión 1.")
table(doc,["Aspecto","Definición"],[
 ("Perfil requerido","Fisioterapeuta, terapeuta ocupacional o musicoterapeuta con certificación vigente y experiencia en rehabilitación de miembro superior."),
 ("Participación","Cuatro sesiones de trabajo distribuidas a lo largo del proyecto, con un total estimado de 24 horas."),
 ("Responsabilidades","Validar las rutinas rítmicas, revisar las métricas motrices propuestas, aprobar el protocolo de sesión y el consentimiento informado, y emitir el dictamen de pertinencia terapéutica."),
 ("Situación actual","Gestión en curso a través del líder del equipo, con contacto identificado. Confirmación prevista para el 10 de septiembre de 2026."),
 ("Plan alternativo","Si la confirmación no se obtiene en la fecha prevista, el proyecto adopta protocolos publicados de musicoterapia neurológica, documenta la ausencia de validación externa como limitación explícita y ajusta las medidas de éxito 8 y 10."),
],widths=[3.6,12.4],fs=9.5)

# ---------------------------------------------------------------- 9
H(doc,"9. Aprobación",1)
P(doc,"Con la firma de este documento, el patrocinador autoriza el inicio del proyecto conforme al alcance, "
  "las fechas y el presupuesto aquí establecidos, y designa al equipo responsable de su ejecución.")
doc.add_paragraph()
table(doc,["Nombre","Rol","Firma","Fecha"],[
 ("Dra. Leticia Amalia Neira Tovar","Patrocinadora del proyecto","",""),
 ("","Director de proyecto","",""),
 ("","Gerente de proyecto","",""),
],widths=[5.4,4.4,3.6,2.6],fs=10)

out="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/01_Carta_Sponsor.docx"
doc.save(out); print("OK",out)
