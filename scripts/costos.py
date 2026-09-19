# -*- coding: utf-8 -*-
"""Costeo ascendente de las 257 tareas. PMBOK áreas 7 y 11.

Modelo vigente desde el 14-sep-2026:
  · El equipo son ocho estudiantes en prácticas profesionales bajo convenio escolar.
    No hay relación laboral, de modo que se paga por hora efectivamente trabajada.
  · Tarifa base: salario mínimo general nominal, $315.04 diarios entre las 8 horas de
    la jornada legal = $39.38 por hora, que se toma como 1 salario mínimo (SM).
  · Cada perfil se expresa como múltiplo del SM según su responsabilidad.
  · El proyecto no realiza compras: equipo prestado por la Facultad y recursos con
    licencia libre. Por tanto no hay costos no laborales ni reserva monetaria.
"""
import sys, os, datetime as dt
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rc257 as R

HDIA = 8
SM_DIARIO = 315.04                       # CONASAMI, vigente desde el 1-ene-2026
SM_HORA   = round(SM_DIARIO / HDIA, 4)   # $39.38

FUENTES = {
 "CONASAMI": (f"${SM_DIARIO:,.2f} diarios",
   "Comisión Nacional de los Salarios Mínimos. Salario mínimo general vigente desde el 1 de enero de 2026, zona resto del país, que incluye al área metropolitana de Monterrey."),
 "JCF": ("$9,582 mensuales",
   "Secretaría del Trabajo y Previsión Social. Programa Jóvenes Construyendo el Futuro: apoyo mensual a personas aprendices, equivalente al salario mínimo general."),
 "LFT": ("8 horas",
   "Ley Federal del Trabajo, artículo 61. Duración máxima de la jornada diurna."),
 "OL": ("$21,697 mensuales en TIC",
   "Observatorio Laboral (STPS) con datos de la ENOE del INEGI, 2.º trimestre de 2026. Se cita como contraste: es el ingreso de un profesionista titulado, no de un practicante."),
}

# perfil -> (múltiplo del salario mínimo, justificación de la responsabilidad)
PERFIL_BASE = {
 "Director de proyecto":             (2.2, "Decide sobre alcance y presupuesto, y responde por la aceptación de los hitos."),
 "Gerente de proyecto":              (1.8, "Mantiene plan, cronograma y riesgos, y responde por el control del avance."),
 "Desarrollador de realidad virtual":(1.5, "Requiere dominio de motor, física e integración; es el perfil técnico más especializado."),
 "Desarrollador de gameplay":        (1.5, "Mismo nivel de especialización técnica sobre el sistema de ritmo."),
 "Analista e investigador":          (1.3, "Requiere lectura de literatura científica y definición de indicadores."),
 "Artista y modelador 3D":           (1.3, "Requiere dominio de herramientas de modelado y criterios de optimización."),
 "Diseñador de interacción UX-XR":   (1.3, "Requiere criterio de diseño de interacción y de ergonomía en realidad virtual."),
 "Compositor y diseñador musical":   (1.2, "Requiere formación musical aplicada."),
 "Diseñador de audio":               (1.2, "Requiere manejo de herramientas de edición y mezcla."),
 "Analista de pruebas (QA)":         (1.1, "Trabajo sistemático de verificación, con menor exigencia de especialización."),
 "Redactor técnico":                 (1.0, "Perfil de entrada. Se toma como referencia de la escala."),
}
PERFIL = {p: (round(SM_HORA*m, 2), round(SM_HORA*m*173.33)) for p,(m,_) in PERFIL_BASE.items()}
def multiplo(p): return PERFIL_BASE[p][0]

# ---- grupo de clave -> perfil que ejecuta ese trabajo
GRUPO = {}
for g in "DP DX DO DB DT DG DH DR".split():                GRUPO[g] = "Desarrollador de realidad virtual"
for g in "JA JT JK JB JN JW JP JI JF JC JL JM JY".split(): GRUPO[g] = "Desarrollador de gameplay"
for g in "EO EB EE ER EG EF EI ET".split():                GRUPO[g] = "Analista e investigador"
for g in "MR ML MP MB MA MN".split():                      GRUPO[g] = "Compositor y diseñador musical"
for g in "SP SB SE SM SI SU SA SC".split():                GRUPO[g] = "Diseñador de audio"
for g in "IM IW IS IE IG IT II IR".split():                GRUPO[g] = "Diseñador de interacción UX-XR"
for g in "AE AC AA AB AP AL AD AS AO AR".split():          GRUPO[g] = "Artista y modelador 3D"
GRUPO.update({
 "QP":"Gerente de proyecto", "QG":"Gerente de proyecto", "QC":"Gerente de proyecto",
 "QR":"Analista e investigador", "QI":"Analista e investigador",
 "QT":"Analista de pruebas (QA)", "QE":"Analista de pruebas (QA)", "QV":"Analista de pruebas (QA)",
 "QD":"Redactor técnico", "QM":"Redactor técnico", "QF":"Redactor técnico",
 "QB":"Desarrollador de realidad virtual",
 "QX":"Director de proyecto",
})
def grupo(k):  return k.split(".")[0]
def perfil(k): return GRUPO[grupo(k)]
def tarifa(k): return PERFIL[perfil(k)][0]
def horas(k):  return round(R.T[k]["dur"]*HDIA, 4)
def costo(k):  return horas(k)*tarifa(k)
def costo_grupo(g): return sum(costo(k) for k in R.ORD if grupo(k)==g)
assert not [k for k in R.ORD if grupo(k) not in GRUPO]

POR_GRUPO = defaultdict(lambda:[0,0.0,0.0]); POR_AREA = defaultdict(lambda:[0,0.0,0.0])
POR_PERFIL= defaultdict(lambda:[0,0.0,0.0])
for k in R.ORD:
    for d,key in ((POR_GRUPO,(R.T[k]["sig"],grupo(k))),(POR_AREA,R.T[k]["area"]),(POR_PERFIL,perfil(k))):
        d[key][0]+=1; d[key][1]+=horas(k); d[key][2]+=costo(k)

MANO_OBRA  = sum(costo(k) for k in R.ORD)
HORAS_TOT  = sum(horas(k) for k in R.ORD)
TARIFA_MED = MANO_OBRA/HORAS_TOT

# ---- recursos proporcionados por la Facultad: no son costo del proyecto
PROPORCIONADOS = [
 ("Visor Meta Quest 3","Equipo principal de desarrollo y pruebas","Préstamo de la Facultad"),
 ("Visor Meta Quest 3S","Segundo equipo, para pruebas simultáneas","Préstamo de la Facultad"),
 ("Estaciones de trabajo","Equipos personales de los integrantes","Aportación del equipo"),
 ("Espacio para las sesiones de prueba","Aula o laboratorio","Instalaciones de la Facultad"),
]
# ---- partidas que en un proyecto comercial serían costo y aquí no lo son
SIN_COSTO = [
 ("Recursos gráficos y assets 3D","Bancos con licencia libre, del tipo CC0"),
 ("Librería de muestras de audio","Bancos de muestras con licencia libre"),
 ("Música para el juego de ritmo","Pistas con licencia libre o de composición propia"),
 ("Software de desarrollo","Unity en su licencia gratuita para estudiantes"),
 ("Software de gestión del proyecto","ProjectLibre, de código abierto"),
 ("Control de versiones y almacenamiento","Planes gratuitos"),
]
NO_LAB_TOT   = 0.0
DIRECTOS     = MANO_OBRA
CONTINGENCIA = 0.0            # ningún riesgo tiene impacto monetario
GESTION      = 0.0
LINEA_BASE   = DIRECTOS
PRESUPUESTO  = LINEA_BASE

# ---- registro de riesgos: el impacto se mide en días de cronograma, no en pesos
# id, descripción, prob., días de impacto, impacto en alcance, categoría
RIESGOS = [
 ("R1","La latencia entre golpe y sonido supera los 30 ms y obliga a rehacer el sistema de audio",0.30, 5.0,"Se degrada la respuesta sonora por intensidad","Técnico"),
 ("R2","La cadena del entorno tridimensional se retrasa y arrastra la fecha final",0.40, 4.0,"Ninguno si se absorbe con la reserva de cronograma","Cronograma"),
 ("R3","La carga de QA no cabe en su ventana y obliga a redistribuir trabajo",0.60, 3.0,"Se recorta documentación no exigida","Recursos"),
 ("R4","Los recursos con licencia libre resultan insuficientes o de licencia ambigua",0.35, 2.0,"Se sustituyen por recursos de menor calidad visual o sonora","Externo"),
 ("R5","La Facultad no concreta el préstamo de los visores",0.20, 6.0,"Las pruebas con usuarios se reducen a una sola sesión","Externo"),
 ("R6","Falla o indisponibilidad de un visor prestado durante el proyecto",0.15, 2.0,"Se pierde la posibilidad de sesiones simultáneas","Externo"),
 ("R7","Usuarios de prueba reportan mareo y hay que rehacer la ergonomía",0.20, 2.0,"Se simplifica el entorno visual","Técnico"),
 ("R8","Pérdida de trabajo por conflicto de versiones",0.20, 1.5,"Ninguno","Técnico"),
 ("R9","Un integrante reduce su disponibilidad por carga académica",0.45, 3.0,"Se redistribuye su trabajo y se recorta alcance secundario","Recursos"),
]
def emv_dias(r): return r[2]*r[3]
EMV_DIAS = sum(emv_dias(r) for r in RIESGOS)

# ---- reserva de cronograma en lugar de reserva monetaria
FER = {dt.date(2026,9,16), dt.date(2026,11,16)}
def habiles(a,b):
    n=0; c=a
    while c<=b:
        if c.weekday()<5 and c not in FER: n+=1
        c+=dt.timedelta(days=1)
    return n
DIAS_DISPONIBLES = habiles(dt.date(2026,9,7), dt.date(2026,11,13))
DURACION_RED     = R.V2["TOTAL"]
RESERVA_CRONO    = DIAS_DISPONIBLES - DURACION_RED

# ---- costo de la calidad
COQ = {
 "Prevención":      ["QP","QG","QR","QC"],
 "Evaluación":      ["QT","QV"],
 "Fallos internos": ["QE","DR","IR","AR"],
}
COQ_TOT = {c: sum(costo_grupo(g) for g in gs) for c,gs in COQ.items()}

# ---- 7.4 Controlar los Costos: valor ganado
M = R.V2
def corte(dia_habil):
    """Estado del proyecto a un corte dado, en días hábiles desde el 7-sep."""
    term = [k for k in R.ORD if M["EF"][k] <= dia_habil+1e-9]
    curso= [k for k in R.ORD if M["ES"][k] < dia_habil < M["EF"][k]]
    PV = 0.0
    for k in R.ORD:                       # valor planificado: avance proporcional al plan
        if M["EF"][k] <= dia_habil+1e-9: PV += costo(k)
        elif M["ES"][k] < dia_habil:
            PV += costo(k) * (dia_habil-M["ES"][k])/(M["EF"][k]-M["ES"][k])
    EV = sum(costo(k) for k in term)      # valor ganado con regla 0/100
    return dict(dia=dia_habil, terminadas=term, en_curso=curso,
                horas=sum(horas(k) for k in term), PV=PV, EV=EV)

def fecha(n):
    c = dt.date(2026,9,7); k=0
    while True:
        if c.weekday()<5 and c not in FER:
            if k==n: return c
            k+=1
        c += dt.timedelta(days=1)

# ---- escenarios de sensibilidad
def escenario(tar_h): return HORAS_TOT*tar_h
ESCENARIOS = [
 ("A. Sin remuneración", 0.0,
  "El trabajo se cursa por créditos y no se remunera. Es el desembolso real del equipo."),
 ("B. Practicantes al salario mínimo, escala por responsabilidad", TARIFA_MED,
  "Línea base de este documento. Tarifa anclada al salario mínimo nominal, con múltiplos por responsabilidad."),
 ("C. Profesionistas titulados", 113.72,
  "Lo que costaría si el equipo fuera personal titulado, con tarifas del Observatorio Laboral."),
]

if __name__ == "__main__":
    print(f"1 SM por hora   ${SM_HORA:>10,.2f}")
    print(f"horas           {HORAS_TOT:>12,.0f} h")
    print(f"tarifa media    ${TARIFA_MED:>10,.2f}/h  ({TARIFA_MED/SM_HORA:.2f} SM)")
    print(f"MANO DE OBRA    ${MANO_OBRA:>10,.0f}")
    print(f"PRESUPUESTO     ${PRESUPUESTO:>10,.0f}   (sin costos no laborales ni reserva monetaria)")
    print()
    print(f"reserva de cronograma: {RESERVA_CRONO:.2f} d   EMV de riesgos: {EMV_DIAS:.2f} d   "
          f"{'SUFICIENTE' if RESERVA_CRONO>=EMV_DIAS else 'INSUFICIENTE'}")
    print()
    for p in sorted(POR_PERFIL, key=lambda x:-POR_PERFIL[x][2]):
        n,h,c = POR_PERFIL[p]
        print(f"  {p:<36}{multiplo(p):>4.1f} SM  ${PERFIL[p][0]:>6.2f}/h{h:>7.0f} h  ${c:>9,.0f}")
    print()
    for a in sorted(POR_AREA, key=lambda x:-POR_AREA[x][2]):
        n,h,c = POR_AREA[a]
        print(f"  {a[:30]:<32}{R.RESP[a]:<10}{n:>4}t{h:>7.0f} h  ${c:>9,.0f}  {100*c/MANO_OBRA:>5.1f}%")
    print()
    for c_,v in COQ_TOT.items(): print(f"  COQ {c_:<18}${v:>9,.0f}  {100*v/MANO_OBRA:>5.1f}%")
    c9 = corte(9.0)
    print()
    print(f"CORTE al {fecha(8)} (fin del día hábil 8):")
    print(f"  terminadas {len(c9['terminadas'])}/257  horas {c9['horas']:,.0f}  "
          f"PV ${c9['PV']:,.0f}  EV ${c9['EV']:,.0f}  SPI {c9['EV']/c9['PV']:.3f}")
