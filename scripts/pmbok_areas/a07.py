# -*- coding: utf-8 -*-
"""
Área 7 — Costos. Todas las cifras se importan de costos.py.

EL PRESUPUESTO SE CALCULÓ TRES VECES Y CADA CORRECCIÓN LO BAJÓ. De $559,891 a $294,981 y de
ahí a los $104,013 vigentes. No fue un recorte: fue reconocer qué es el proyecto realmente —un
equipo de practicantes bajo convenio escolar, sin compras— y anclar la tarifa a una fuente
oficial en vez de estimarla.
"""
import costos

AREA = "7"

# Corte de medio curso, 18-sep-2026. Las tres magnitudes del valor ganado.
PV, EV, SPI = 47562, 46097, 0.969

RESUMEN = [
    f"El presupuesto del proyecto es de ${costos.MANO_OBRA:,.0f}, y es mano de obra en su "
    f"totalidad: {costos.HORAS_TOT:,.0f} horas a una tarifa media de "
    f"${costos.TARIFA_MED:.2f} por hora. No hay una sola línea de compra, porque no hay nada "
    "que comprar: los visores son un préstamo de la Facultad, Unity es gratuito y los assets "
    "tienen licencia libre.",

    f"La tarifa no se estimó: se ancló al salario mínimo nominal publicado por la CONASAMI, "
    f"${costos.SM_DIARIO:,.2f} diarios entre {costos.HDIA} horas = ${costos.SM_HORA} por hora, "
    "que se toma como una unidad —1 SM—. Cada perfil es un múltiplo de esa unidad según su "
    "responsabilidad, de 1.0 para el redactor técnico a 2.2 para la dirección, y cada múltiplo "
    "lleva escrita su justificación.",

    "No hay reserva monetaria, y es deliberado: ningún riesgo del proyecto tiene impacto en "
    "dinero, porque el proyecto no compra ni contrata. La reserva es de cronograma y se mide "
    "en días hábiles. Un presupuesto con una reserva de contingencia en pesos habría sido una "
    "cifra sin nada que la justificara.",
]

PROCESOS = {
    "7.1": (
        "Se planificó la gestión de costos con una decisión de fondo: el proyecto se costea "
        "por mano de obra, en horas, con tarifa anclada a fuente oficial; y no lleva reserva "
        "monetaria porque no tiene desembolsos que un riesgo pueda encarecer.",
        "04_Planes, Parte I §1; 05_Analisis §2.",
    ),
    "7.2": (
        "La estimación es ascendente, actividad por actividad: horas por actividad, perfil por "
        "grupo de actividades, y tarifa por perfil. Se eligió esa técnica y no la analogía "
        "porque el proyecto no tiene un proyecto anterior comparable.",
        f"05_Analisis §3 a §7, con la matriz de tiempos y la agregación; anexo A con el costeo "
        f"de las 257 actividades. scripts/costos.py: {costos.HORAS_TOT:,.0f} horas.",
    ),
    "7.3": (
        f"El presupuesto se determinó en ${costos.MANO_OBRA:,.0f}, agregando el costo por área "
        "de trabajo y por perfil, con la curva S de desembolso. Se documentó explícitamente "
        "que no hay compras y que la reserva va en días.",
        "05_Analisis §8, incluidas §8.1 el proyecto no realiza compras, §8.2 reservas y §8.4 "
        "la curva S; acta constitutiva §4.10 plan financiero.",
    ),
    "7.4": (
        f"El control se hizo con valor ganado al corte de medio curso: PV de ${PV:,}, EV de "
        f"${EV:,} y un SPI de {SPI}. El propio documento declara la limitación: sin registro "
        "de horas reales no hay costo real ni índice de desempeño del costo, así que la mitad "
        "del método queda inutilizable.",
        f"05_Analisis §13, con las tres magnitudes, los índices, la medición al corte y los "
        "pronósticos; §13.5 qué debe empezar a registrarse.",
    ),
}

TABLAS = [
    ("Escala de tarifas: cada perfil como múltiplo del salario mínimo",
     ["Perfil", "Múltiplo", "Por hora", "Justificación del múltiplo"],
     [[p, f"{m:.1f} SM", f"${costos.PERFIL[p][0]:,.2f}", razon]
      for p, (m, razon) in costos.PERFIL_BASE.items()]),

    ("Integración del presupuesto",
     ["Concepto", "Monto", "Nota"],
     [["Mano de obra", f"${costos.MANO_OBRA:,.0f}",
       f"{costos.HORAS_TOT:,.0f} horas a ${costos.TARIFA_MED:.2f} de media "
       f"({costos.TARIFA_MED/costos.SM_HORA:.2f} SM)."],
      ["Costos no laborales", "$0",
       "Visores prestados, licencias libres, Unity gratuito, sin backend."],
      ["Reserva de contingencia monetaria", "$0",
       "Ningún riesgo tiene impacto en dinero. La reserva va en días hábiles."],
      ["Presupuesto total", f"${costos.MANO_OBRA:,.0f}", "Aprobado en el acta constitutiva."]]),

    ("Evolución del presupuesto: tres cálculos, y qué enseñó cada corrección",
     ["Versión", "Supuesto", "Presupuesto", "Por qué estaba mal"],
     [["1.ª", "Tarifas de mercado sin fuente, más compras de equipo", "$559,891",
       "Las tarifas no tenían origen verificable y el proyecto no iba a comprar los visores."],
      ["2.ª", "Observatorio Laboral, tarifas de profesionistas titulados", "$294,981",
       "La fuente era oficial, pero describía a profesionistas con título ejerciendo. El "
       "equipo son practicantes bajo convenio escolar."],
      ["3.ª vigente", "Salario mínimo escalado por responsabilidad, sin compras",
       f"${costos.MANO_OBRA:,.0f}",
       "Es la que corresponde a lo que el proyecto es. Regla que quedó: no estimar tarifas "
       "sin fuente oficial."]]),

    ("Control por valor ganado al corte de medio curso",
     ["Magnitud", "Valor", "Qué dice"],
     [["Valor planificado (PV)", f"${PV:,}", "Lo que debía haberse ejecutado al 18 de "
       "septiembre según el cronograma."],
      ["Valor ganado (EV)", f"${EV:,}", "Lo que realmente se completó, valorado al "
       "presupuesto."],
      ["Índice de desempeño del cronograma (SPI)", str(SPI),
       "Ligeramente por debajo de 1: el proyecto iba un 3 % detrás del plan."],
      ["Costo real (AC)", "no disponible",
       "No se registraron horas reales por actividad. Sin ese dato no hay AC ni CPI."],
      ["Índice de desempeño del costo (CPI)", "no calculable",
       "Es la limitación declarada del área: la mitad del método del valor ganado no se pudo "
       "aplicar."]]),
]

LECCIONES = [
    ("El error que inflaba el presupuesto un 40 % y no se veía en la hoja de cálculo",
     f"Dividir el salario mensual entre 173.33 horas da ${costos.SM_HORA * 1.4030:.2f} por "
     f"hora en vez de ${costos.SM_HORA}, y parece más riguroso porque usa el estándar de horas "
     "laborables del mes. No lo es: ese número es el costo patronal de un trabajador de planta "
     "que cobra los días de descanso. Un practicante bajo convenio escolar no los cobra, así "
     f"que la división correcta es el salario diario entre {costos.HDIA} horas efectivamente "
     "trabajadas. Nada en la fórmula parecía mal; lo que estaba mal era el supuesto sobre quién "
     "cobra."),

    ("Un presupuesto sin reserva monetaria es defendible si se dice por qué",
     "La plantilla pide una reserva de contingencia, y la tentación es poner un porcentaje. "
     "Aquí se dejó en cero y se explicó: ningún riesgo del registro tiene impacto en dinero, "
     "porque el proyecto no compra ni contrata. Lo que sí se reservó —y se calculó— son días "
     "hábiles de cronograma, que es la moneda en que este proyecto puede perder. Poner un 10 % "
     "de reserva en pesos habría sido una cifra que nadie podría haber justificado si la "
     "docente preguntara contra qué riesgo se reservó."),

    ("Medir el avance sin registrar horas deja el método a la mitad",
     "El valor ganado calculó PV, EV y SPI, pero no AC ni CPI, porque nadie registró horas "
     "reales por actividad. El documento lo declara como limitación en vez de inventar el dato, "
     "y lo deja como la recomendación principal del área. La lección es de secuencia: el "
     "registro de horas hay que montarlo antes de necesitarlo, porque a mitad del proyecto ya "
     "no se puede reconstruir hacia atrás."),
]

REMITE_A = [
    ("entregables/05_Analisis_Costos_Calidad_Riesgos.docx",
     "El análisis completo del área 7: la determinación de las tarifas con sus fuentes "
     "oficiales, la matriz de tiempos, la agregación ascendente, la curva S, los escenarios de "
     "sensibilidad, el valor ganado y el anexo A con el costeo de las 257 actividades."),
    ("entregables/04_Planes_Costos_Calidad_Riesgos.docx",
     "La Parte I: el plan de gestión de los costos."),
    ("entregables/02_Acta_Constitutiva.docx",
     "§4.10 plan financiero, con la tarifa por perfil y el resumen del presupuesto aprobado."),
    ("entregables/Cronograma_ProjectLibre.xml",
     "Los trece recursos con su tarifa y su costo cargado, actividad por actividad."),
    ("scripts/costos.py",
     "La fuente única: el salario mínimo vigente, la escala de perfiles con su justificación y "
     "el cálculo del esfuerzo y de la mano de obra."),
]
