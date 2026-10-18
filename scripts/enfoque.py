# -*- coding: utf-8 -*-
"""
Datos del cambio de enfoque terapéutico. Única fuente de verdad del documento 11.

POR QUE UN DOCUMENTO DE CAMBIO Y NO UNA CARTA SPONSOR REESCRITA

Un acta constitutiva aprobada no se edita en silencio. El PMBOK lo trata en 4.6, Realizar el
control integrado de cambios: lo que modifica una línea base aprobada entra por una solicitud
de cambio, se evalúa y se registra. Reescribir el documento original borra la evidencia de que
hubo una decisión, que es justo lo que el control de cambios existe para conservar.

El equipo ya sentó este precedente con el recorte de alcance: el acta no se tocó, se emitió un
documento que dice qué cambia y por qué. Este sigue la misma forma.

HONESTIDAD SOBRE LA FECHA

La decisión se tomó en conversación antes del corte de medio curso y NO SE REGISTRO ENTONCES.
Eso se declara tal cual en el documento. Fechar hoy una decisión de hace un mes sería más
cómodo y menos cierto; y la brecha entre decidir y registrar es, en sí misma, el hallazgo de
gestión más útil de este documento.
"""

FECHA_DECISION = "antes del 18 de septiembre de 2026, en reunión de equipo"
FECHA_REGISTRO = "18 de octubre de 2026"

# Por qué se cambió. Son las razones que dio el equipo, no una racionalización posterior.
MOTIVOS = [
    ("Sin asesor no hay fundamento clínico",
     "El marco de rehabilitación motriz exige que alguien con credencial clínica valide las "
     "rutinas. El asesor terapéutico tenía fecha límite el 10 de septiembre y no se concretó. "
     "Sostener un lenguaje clínico sin esa validación es afirmar algo que el proyecto no puede "
     "respaldar."),
    ("La medición motriz pedía instrumentos que el proyecto no tiene",
     "La amplitud de movimiento de miembro superior se mide con goniometría o con captura "
     "corporal. Un control de mano da la posición del control, no la del hombro ni la del codo: "
     "el mismo recorrido de la baqueta puede venir de un movimiento de muñeca o de uno de "
     "hombro, y el sistema no puede distinguirlos."),
    ("El beneficio emocional sí es observable con lo que hay",
     "La precisión temporal y la constancia del pulso se miden con el reloj de audio que el "
     "prototipo ya usa, y no necesitan respaldo clínico: comprobar si alguien toca a tiempo es "
     "una observación de ejecución musical, no un diagnóstico."),
]

# Qué dice hoy cada pasaje y qué pasa a decir. Texto literal, para que la sustitución sea
# verificable palabra por palabra y no una descripción vaga de la intención.
PASAJES = [
    ("Carta sponsor", "2. Justificación",
     "una simulación diseñada para rehabilitación motriz tiene usuario, criterio de éxito "
     "medible y valor demostrable",
     "una simulación diseñada para la regulación emocional por medio del ritmo tiene usuario, "
     "criterio de éxito medible y valor demostrable"),

    ("Carta sponsor", "2. Justificación",
     "Existe evidencia clínica consolidada que respalda el uso de la percusión con fines "
     "terapéuticos.",
     "Existe literatura revisada por pares sobre el uso de la percusión grupal e individual "
     "para la reducción del estrés percibido. El proyecto la cita como antecedente, no como "
     "aval clínico de sus resultados."),

    ("Carta sponsor", "3. Objetivo",
     "Herramienta de apoyo a la rehabilitación motriz, con beneficio emocional secundario",
     "Herramienta de regulación emocional por medio de la ejecución rítmica"),

    ("Carta sponsor", "3. Usuario",
     "Persona en proceso de rehabilitación motriz de miembro superior, bajo supervisión de un "
     "terapeuta",
     "Persona sin experiencia musical previa que busca una actividad rítmica de bajo estrés; "
     "no se requiere supervisión profesional"),

    ("Carta sponsor", "3. Validación",
     "Pruebas funcionales más validación clínica de un asesor terapéutico externo",
     "Pruebas funcionales con usuarios y registro objetivo de métricas de ejecución"),

    ("Carta sponsor", "4. Medida 9",
     "El sistema exporta, por sesión, precisión temporal, amplitud de movimiento y constancia "
     "del pulso.",
     "El sistema exporta, por sesión, precisión temporal y constancia del pulso, con los "
     "desfases individuales que permiten reanalizar los datos."),

    ("Acta constitutiva", "Perfil del asesor",
     "Fisioterapeuta, terapeuta ocupacional o musicoterapeuta con certificación vigente y "
     "experiencia en rehabilitación de miembro superior.",
     "Rol retirado. La medida de éxito 8 quedó formalmente retirada en el documento 10, "
     "Recorte de alcance."),
]

# Lo que NO cambia. Vale tanto como lo que cambia: acota el alcance del cambio y evita que
# alguien suponga que se movió algo que sigue igual.
NO_CAMBIA = [
    ("Medidas de éxito 1 a 7 y 10",
     "Están redactadas en términos de comportamiento del sistema, sin supuesto clínico. "
     "Identificación de componentes, detección de contacto, correspondencia del sonido, "
     "latencia, estabilidad, interacción intuitiva, sensibilidad a la intensidad y seguridad "
     "de uso se verifican igual bajo cualquiera de los dos enfoques."),
    ("Presupuesto",
     "$104,013 MXN. El asesor externo nunca llegó a contratarse, así que su retiro no libera "
     "dinero: el presupuesto vigente ya estaba calculado sin él."),
    ("Cronograma y ruta crítica",
     "Ninguna actividad de la ruta crítica dependía del marco motriz. El recorte de alcance "
     "del documento 10 ya reflejó las que sí."),
    ("Riesgo dominante",
     "La latencia por debajo de 30 ms sigue siendo el criterio que decide si el golpe se "
     "siente causal. Un golpe que no se siente propio no regula nada, igual que no "
     "rehabilitaba nada."),
    ("Arquitectura del prototipo",
     "El reloj musical, el juicio de golpes y el registro de métricas no suponen ningún "
     "marco terapéutico: miden ejecución rítmica. La interfaz ITempoMap deja además abierta "
     "la rampa de tempo del iso-principio, que pertenece a los dos enfoques."),
]

# Lo que el proyecto pierde al cambiar. Un documento de cambio que solo enumera ventajas no
# es un análisis, es una justificación.
RENUNCIAS = [
    ("Se pierde el destinatario clínico",
     "La revisión 1 ganó valor al pasar de «simulación sin destinatario» a «herramienta con "
     "usuario definido». El usuario sigue existiendo, pero ya no es un paciente en "
     "rehabilitación: es alguien que busca una actividad rítmica. El valor social declarado "
     "baja."),
    ("Se pierde la validación externa",
     "Ningún profesional avala el resultado. Queda como limitación explícita del informe "
     "final, no como omisión."),
    ("Se pierde una métrica",
     "La amplitud de movimiento desaparece del registro. Las dos que quedan son suficientes "
     "para la medida 9, pero el conjunto de datos es menor."),
]

# Qué hay que hacer con esto, con responsable.
ACCIONES = [
    ("Anexar este documento a la carta sponsor y al acta constitutiva",
     "Gerente de proyecto", "Al firmarse"),
    ("Recoger la firma de la patrocinadora",
     "Director de proyecto", "Próxima sesión de clase"),
    ("Redactar la limitación en el informe final (QI.3)",
     "QA y gestión", "Antes del cierre del informe"),
    ("Verificar que el prototipo no exporte amplitud de movimiento",
     "Desarrollo VR", "Hecho: SessionStats no la calcula"),
]
