# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
import pdm, edt, costos

doc = Document('/tmp/_acta_c.docx')

# ---------------------------------------------------------------- recursos
H(doc,"4.9 Plan de recursos",2)
table(doc,["Rol","Semanas activas","Esfuerzo","Horas","Paquetes principales"],[
 ("Director de proyecto","S1 – S11","25 %","110","1.4, 1.6, 2.3 y aprobación de los seis hitos"),
 ("Gerente de proyecto","S1 – S11","40 %","176","1.1 a 1.5, 7.6"),
 ("Coordinador","S1 – S11","40 %","176","1.5, 1.6, 2.2, 2.8, 7.3, 7.5"),
 ("Desarrollador de realidad virtual","S2 – S11","70 %","252","4.1 a 4.7, 5.3 a 5.5, 6.3, 6.4, 7.2, 7.4"),
 ("Diseñador de interacción / UX-XR","S2 – S11","50 %","160","3.1, 3.3, 4.3, 4.7, 5.5, 6.1, 6.2, 6.4, 7.3, 7.4"),
 ("Artista y modelador tridimensional","S1 – S8","50 %","140","3.1, 3.2, 3.4, 3.5, 4.6, 7.5"),
 ("Diseñador de audio","S3 – S8","40 %","96","4.2, 5.1 a 5.4"),
 ("Analista de métricas","S1 – S11","30 %","84","2.1, 2.4, 2.6, 2.8, 6.3, 7.1, 7.6"),
 ("Asesor terapéutico externo","S2, S5, S7, S8","24 horas","24","2.3, 2.5, 2.7, 2.9, 7.3"),
],widths=[4.6,2.6,1.8,1.6,5.4],fs=9.5)
P(doc,"Recursos materiales: dos visores autónomos, Meta Quest 3 y Quest 3S; estaciones de trabajo del "
  "equipo; recursos gráficos y librería de muestras con licencia; y espacio para las sesiones de prueba con "
  "usuarios.")

H(doc,"4.9.1 Nota sobre la reasignación del paquete 3.3",3)
P(doc,"En la versión 2.0 el artista tridimensional concentraba los paquetes 3.2 a 3.5 en secuencia, lo que "
  "producía una cadena de 39 días hábiles a cargo de una sola persona y constituía la ruta crítica del "
  "proyecto. El paquete 3.3, modelado de baquetas y entorno, se reasignó al diseñador de interacción porque "
  "es el elemento de menor complejidad técnica de la rama y porque ese rol tenía capacidad disponible en las "
  "semanas 2 a 4. Con el cambio, los paquetes 3.2 y 3.3 se ejecutan en paralelo y la rama deja de ser "
  "crítica.")

# ---------------------------------------------------------------- financiero
H(doc,"4.10 Plan financiero",2)
P(doc,"El equipo son practicantes bajo convenio escolar, no empleados de planta. Por eso la tarifa se "
  "ancla al salario mínimo general vigente —$%s diarios entre %d horas de jornada, es decir $%.2f por "
  "hora— y cada perfil es un múltiplo de ese salario según la responsabilidad que asume. La tarifa media "
  "del proyecto resulta de $%.2f por hora, equivalente a %.2f salarios mínimos."
  % (format(costos.SM_DIARIO, ",.2f"), costos.HDIA, costos.SM_HORA,
     costos.TARIFA_MED, costos.TARIFA_MED / costos.SM_HORA))
P(doc,"No se divide un sueldo mensual entre 173.33 horas. Ese cociente arroja el costo patronal de un "
  "trabajador de planta, que cobra los días de descanso; un practicante no los cobra, y usarlo infló el "
  "presupuesto de las dos versiones anteriores de esta acta.")

H(doc,"4.10.1 Tarifa por perfil",3)
table(doc,["Perfil","Múltiplo del salario mínimo","$ / hora","Por qué ese múltiplo"],
 [(rol, "%.1f" % mult, "$%.2f" % (mult * costos.SM_HORA), razon)
  for rol, (mult, razon) in sorted(costos.PERFIL_BASE.items(), key=lambda x: -x[1][0])],
 widths=[4.2,2.6,1.8,7.4],fs=8.5)

H(doc,"4.10.2 Mano de obra por perfil",3)
P(doc,"El costeo es ascendente: se parte de las actividades de la lista de trabajo del equipo, se suman "
  "sus horas por perfil y se multiplican por la tarifa. Las %s horas de esfuerzo salen de ahí, no de "
  "estimar semanas por porcentaje de dedicación."
  % format(int(costos.HORAS_TOT), ",d"))
_fil = sorted(costos.POR_PERFIL.items(), key=lambda x: -x[1][2])
table(doc,["Perfil","Actividades","Horas","Costo (MXN)"],
 [(rol, n, "%.0f" % h, "$%s" % format(round(c), ",d")) for rol, (n, h, c) in _fil] +
 [("Total", sum(v[0] for _, v in _fil), "%.0f" % costos.HORAS_TOT,
   "$%s" % format(round(costos.MANO_OBRA), ",d"))],
 widths=[6.4,2.6,2.4,4.6],fs=9)

H(doc,"4.10.3 Recursos que no cuestan",3)
P(doc,"El proyecto no compra nada. Lo que en las versiones anteriores figuraba como equipo, licencias y "
  "operación —$48,748 de desembolso declarado— corresponde en realidad a recursos prestados o de uso "
  "libre.")
table(doc,["Recurso","Para qué","De dónde sale"], list(costos.PROPORCIONADOS),
 widths=[4.6,6.4,5.0],fs=9)
table(doc,["Recurso de uso libre","Condición"], list(costos.SIN_COSTO),
 widths=[6.0,10.0],fs=9)

H(doc,"4.10.4 Resumen del presupuesto",3)
table(doc,["Concepto","Monto (MXN)"],[
 ("Mano de obra", "$%s" % format(round(costos.MANO_OBRA), ",d")),
 ("Costos no laborales", "$%s" % format(round(costos.NO_LAB_TOT), ",d")),
 ("Subtotal de costos directos", "$%s" % format(round(costos.DIRECTOS), ",d")),
 ("Reserva de contingencia monetaria", "$0"),
 ("Presupuesto total", "$%s" % format(round(costos.PRESUPUESTO), ",d")),
],widths=[9.0,7.0],fs=10)

P(doc,"El presupuesto es costo imputado del trabajo del equipo: ningún integrante desembolsa esa cantidad, "
  "y sirve para dimensionar lo que el proyecto valdría si se contratara. La evolución de la cifra a lo "
  "largo del proyecto está documentada y cada corrección la acercó a lo que el proyecto realmente es:")
table(doc,["Versión del cálculo","Supuesto","Presupuesto"],
 [(e[0], e[2], "$%s" % format(round(costos.HORAS_TOT * e[1]), ",d")) for e in costos.ESCENARIOS],
 widths=[4.4,8.4,3.2],fs=9)

H(doc,"4.10.5 La reserva va en días, no en pesos",3)
P(doc,"Como el proyecto no compra ni contrata, ningún riesgo del registro tiene impacto monetario: todos "
  "golpean el calendario o degradan el alcance. Por eso no hay reserva de contingencia en dinero y sí la "
  "hay en cronograma. El valor monetario esperado de los riesgos se expresa en días hábiles y vale %.2f "
  "días, contra una reserva de %.2f: alcanza, con margen, salvo que tres riesgos se materialicen juntos."
  % (costos.EMV_DIAS, costos.RESERVA_CRONO))
P(doc,"Advertencia que conviene no perder de vista: si los riesgos R1, R2 y R5 ocurrieran a la vez serían "
  "quince días y la reserva no alcanzaría.")

P(doc,"Nota sobre las dos bases de cálculo. El esfuerzo de este plan financiero se cuenta sobre la lista "
  "de trabajo que el equipo ejecuta día a día, que es más detallada que los 42 paquetes de la sección 4.3. "
  "La reserva de cronograma que aquí se cita, de %.2f días, pertenece a esa misma base. La duración de 50 "
  "días hábiles y los 3 de margen que declara la sección 4.8 corresponden a la red de 27 actividades de "
  "esta acta. Son dos vistas del mismo proyecto a distinto grano, y conviene no mezclarlas al comparar "
  "cifras." % costos.RESERVA_CRONO)

# ---------------------------------------------------------------- calidad
H(doc,"4.11 Plan de calidad",2)
table(doc,["Proceso","Cómo se aplica"],[
 ("Planificar la calidad","Cada paquete de trabajo tiene criterio de aceptación declarado en la sección 4.3."),
 ("Revisión por pares","Todo entregable técnico lo revisa un integrante distinto de quien lo produjo."),
 ("Control de versiones","El código y los recursos se mantienen en repositorio con historial."),
 ("Pruebas de aceptación","Existe un caso de prueba por cada medida de éxito declarada en la carta sponsor."),
 ("Pruebas de rendimiento","Se verifica el sostenimiento de 72 cuadros por segundo y el umbral de 30 ms de latencia."),
 ("Validación externa","El asesor terapéutico dictamina la pertinencia de rutinas, métricas y protocolo."),
 ("Pruebas con usuarios","Se ejecutan bajo protocolo aprobado y con consentimiento informado."),
 ("Registro de defectos","Cada defecto se clasifica por severidad. Ninguno de severidad alta queda abierto al cierre."),
 ("Auditoría de cierre","Se verifica que los 42 paquetes cumplan su criterio de aceptación antes de la presentación final."),
],widths=[4.6,11.4],fs=9.5)

# ---------------------------------------------------------------- terminacion
H(doc,"4.12 Criterios de terminación del proyecto",2)
P(doc,"El proyecto se considera terminado cuando se cumplen todas las condiciones siguientes:")
bullets(doc,[
 "Los 42 paquetes de trabajo cumplen su criterio de aceptación.",
 "Las diez medidas de éxito de la carta sponsor están verificadas y documentadas.",
 "No queda abierto ningún defecto de severidad alta.",
 "El asesor terapéutico emitió su dictamen de pertinencia.",
 "La documentación completa está entregada: manual técnico y de usuario, e informe de pruebas y resultados.",
 "La presentación final fue realizada ante la patrocinadora.",
],num=True)

doc.add_page_break()
# ================================================================ 5
H(doc,"5. Consideraciones",1)
H(doc,"5.1 Riesgos",2)
P(doc,"La probabilidad y el impacto se valoran en escala de tres niveles. La exposición combina ambos y "
  "determina el orden de atención.")
table(doc,["#","Riesgo","Prob.","Impacto","Exposición","Respuesta"],[
 ("R1","La latencia entre golpe y sonido supera los 30 ms en el visor autónomo.","Media","Alto","Alta",
  "Hito Go / No-Go en la segunda semana. El audio se sincroniza contra el reloj del sistema de audio y no contra el ciclo de cuadro. Si no se alcanza el umbral, se revisa el alcance del sistema de audio."),
 ("R2","La rama de interacción o la de audio se retrasan.","Media","Alto","Alta",
  "Son las dos rutas críticas y no tienen holgura. Revisión de avance semanal restringida a las actividades críticas. Reserva de 3 días hábiles más la semana del 16 al 20 de noviembre."),
 ("R3","No se concreta la participación del asesor terapéutico.","Baja","Alto","Media",
  "Existe contacto identificado a través del líder del equipo, con confirmación prevista para el 10 de septiembre. Si no se concreta, se adoptan protocolos publicados de musicoterapia neurológica y se documenta la ausencia de validación externa como limitación explícita."),
 ("R4","La geometría no alcanza el rendimiento requerido en el visor.","Media","Medio","Media",
  "El paquete 3.5 está dedicado a optimización. Se define presupuesto de polígonos desde el diseño conceptual."),
 ("R5","La rama del modelo tridimensional se retrasa.","Media","Medio","Media",
  "Tiene un solo día de holgura y se controla como crítica. El paquete 3.3 ya se reasignó para acortarla."),
 ("R6","Usuarios de prueba reportan mareo o fatiga.","Baja","Medio","Baja",
  "Paquete 4.7 dedicado a ergonomía. Sesiones limitadas en duración, con criterios de suspensión definidos en el protocolo."),
 ("R7","Falla o indisponibilidad del equipo de realidad virtual.","Baja","Alto","Media",
  "Se adquieren dos visores. El desarrollo se mantiene ejecutable también en simulador de escritorio."),
 ("R8","Sobrecarga del equipo por coincidencia con evaluaciones del semestre.","Alta","Medio","Alta",
  "El cronograma cierra el 13 de noviembre, diez días antes del inicio de exámenes. La semana del 16 al 20 de noviembre queda libre de trabajo programado."),
],widths=[0.8,4.4,1.4,1.4,1.6,6.4],fs=8.5)

H(doc,"5.2 Problemas abiertos",2)
table(doc,["#","Problema","Fecha límite","Responsable"],[
 ("P1","Confirmación formal del asesor terapéutico.","10 sep 2026","Director de proyecto"),
 ("P2","Definición del perfil de los usuarios de prueba y su reclutamiento.","19 oct 2026","Coordinador"),
 ("P3","Selección de la librería de muestras de audio con licencia compatible.","25 sep 2026","Diseñador de audio"),
 ("P4","Definición del presupuesto de polígonos para la escena completa.","4 sep 2026","Artista 3D / Dev RV"),
],widths=[0.9,8.4,3.2,3.5],fs=9.5)

H(doc,"5.3 Supuestos",2)
bullets(doc,[
 "El equipo dispone de los dos visores durante todo el periodo del proyecto.",
 "Los ocho integrantes mantienen la dedicación declarada en el plan de recursos.",
 "El asesor terapéutico se incorpora dentro de la primera quincena de septiembre.",
 "El hardware objetivo permite alcanzar el umbral de latencia de 30 ms.",
 "Se dispone de espacio físico adecuado para las sesiones de prueba con usuarios.",
 "Los usuarios de prueba participan de forma voluntaria y bajo consentimiento informado.",
])

H(doc,"5.4 Restricciones",2)
bullets(doc,[
 "El proyecto debe terminar el 13 de noviembre de 2026. Los exámenes inician el 23 de noviembre.",
 "El presupuesto total no excede $%s MXN, y es costo imputado: el proyecto no compra ni contrata." % format(round(costos.PRESUPUESTO), ",d"),
 "La aplicación se ejecuta en visor autónomo, sin equipo de cómputo conectado.",
 "La interacción se realiza mediante los controles del visor, no mediante seguimiento de manos.",
 "El proyecto no contempla componente de servidor: las métricas se exportan a archivo local.",
 "El sistema no se presenta ni certifica como dispositivo médico.",
])

doc.add_page_break()
# ================================================================ 6
H(doc,"6. Apéndice",1)

H(doc,"6.1 Anexo A. Asignación nominal por paquete de trabajo",2)
P(doc,"Este anexo verifica que cada uno de los 42 paquetes tenga responsable nominal asignado. Se incluye "
  "porque un paquete sin responsable identificado es un paquete que nadie ejecuta.")
NOMB={"Gerente de proyecto":"Ricardo Alejandro Rodríguez Ríos","Director de proyecto":"Abiud Misael Benítez Muñoz",
 "Coordinador":"Jesús Eduardo Rodríguez Salinas","Desarrollador VR":"María Fernanda Montoya Valdez",
 "Diseñador UX-XR":"Diana Laura Tello Salinas","Artista 3D":"Christian Salvador Valadez Gallegos",
 "Diseñador de audio":"Javier Alejandro Hernández Caloca","Analista de métricas":"Kimberly González Sepúlveda",
 "Asesor terapéutico":"Externo, por confirmar"}
def nominal(res):
    partes=[p.strip() for p in res.replace(" / ","/").split("/")]
    mapa={"Gerente":"Ricardo A. Rodríguez","Director":"Abiud M. Benítez","Coordinador":"Jesús E. Rodríguez",
     "Dev RV":"M. Fernanda Montoya","UX-XR":"Diana L. Tello","Artista 3D":"Christian S. Valadez",
     "Audio":"Javier A. Hernández","Métricas":"Kimberly González","Asesor":"Externo","QA":"rotativo entre el equipo"}
    out=[]
    for p in partes:
        for k,v in mapa.items():
            if k.lower() in p.lower(): out.append(v); break
        else: out.append(NOMB.get(p,p))
    vistos=[]
    for o in out:
        if o not in vistos: vistos.append(o)
    return ", ".join(vistos)
rows=[(c,n,r,nominal(r)) for c,n,cr,r,rc,a,d in edt.PKG]
table(doc,["Código","Paquete de trabajo","Rol responsable","Integrante"],rows,
      widths=[1.2,5.6,4.0,5.2],fs=8.5)
P(doc,"La función de aseguramiento de calidad se ejerce de forma rotativa: cada entregable lo revisa un "
  "integrante distinto de quien lo produjo. No es un rol de dedicación exclusiva.")

H(doc,"6.2 Anexo B. Glosario",2)
table(doc,["Término","Definición"],[
 ("Estructura de desglose del trabajo","Descomposición jerárquica del alcance total en componentes menores y en paquetes de trabajo. No establece secuencia entre sus componentes."),
 ("Paquete de trabajo","Componente del nivel más bajo de la estructura de desglose, con responsable, duración y criterio de aceptación propios."),
 ("Diagramación por precedencias","Técnica de secuenciación en la que cada actividad es un nodo y las flechas expresan la relación de precedencia. Admite cuatro tipos de dependencia."),
 ("Dependencia fin → inicio","La actividad sucesora no puede iniciar hasta que la predecesora termine."),
 ("Dependencia inicio → inicio","La sucesora puede iniciar cuando la predecesora lleva cierto avance, expresado como demora."),
 ("Demora","Tiempo que debe transcurrir entre el punto de referencia de la predecesora y el inicio de la sucesora."),
 ("Ruta crítica","Trayectoria continua de mayor duración entre el inicio y el fin del proyecto. Sus actividades tienen holgura cero."),
 ("Holgura total","Margen de retraso de una actividad sin desplazar la fecha final del proyecto."),
 ("Latencia","Retardo entre el golpe de la baqueta virtual y la reproducción del sonido correspondiente."),
 ("Musicoterapia neurológica","Aplicación clínica de la música para tratar alteraciones del sistema nervioso, con protocolos estandarizados."),
 ("Estimulación auditiva rítmica","Técnica que emplea un pulso auditivo constante para regular el movimiento del paciente."),
 ("Reserva de gestión","Periodo sin trabajo programado, destinado a absorber desviaciones del cronograma."),
],widths=[4.4,11.6],fs=9)

H(doc,"6.3 Anexo C. Documentos relacionados",2)
table(doc,["Documento","Contenido"],[
 ("Carta sponsor, revisión 2","Autorización del proyecto, beneficios, medidas de éxito y presupuesto."),
 ("Ruta crítica del proyecto","Desarrollo completo del método: matrices de secuencias, tiempos, información y elasticidad; red de precedencias, red medida y determinación de la ruta crítica."),
 ("Cronograma en formato importable","Archivo del cronograma con fechas, dependencias y recursos, para su importación en la herramienta de programación."),
],widths=[4.8,11.2],fs=9.5)

H(doc,"6.4 Aprobación",2)
doc.add_paragraph()
table(doc,["Nombre","Rol","Firma","Fecha"],[
 ("Dra. Leticia Amalia Neira Tovar","Patrocinadora",""," "),
 ("Abiud Misael Benítez Muñoz","Director de proyecto","",""),
 ("Ricardo Alejandro Rodríguez Ríos","Gerente de proyecto","",""),
],widths=[5.4,4.2,3.8,2.6],fs=10)

out="/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/02_Acta_Constitutiva.docx"
doc.save(out); print("OK",out)
print("parrafos:",len(doc.paragraphs)," tablas:",len(doc.tables)," secciones:",len(doc.sections))
