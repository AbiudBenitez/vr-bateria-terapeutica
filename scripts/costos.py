# -*- coding: utf-8 -*-
"""Costeo ascendente de las 257 tareas. PMBOK 7.2 Estimar los Costos.

Tarifas derivadas de fuentes oficiales mexicanas, no de portales de empleo:
  · Observatorio Laboral (STPS) con datos de la ENOE del INEGI, 2.º trimestre de 2026
  · Data México (Secretaría de Economía), ENOE, 1.er trimestre de 2026
  · CONASAMI, salarios mínimos vigentes desde el 1 de enero de 2026
  · IMSS, salario base de cotización promedio, enero de 2026
"""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rc257 as R

HDIA   = 8
HMES   = 173.33          # horas laborables al mes (40 h/semana × 52 / 12)

# ---- anclas oficiales, ingreso mensual
OFICIAL = {
 "TIC":        (21697, "Observatorio Laboral (STPS), ENOE-INEGI 2T-2026, área Tecnologías de la Información y la Comunicación"),
 "PROF":       (19494, "Observatorio Laboral (STPS), ENOE-INEGI 2T-2026, promedio nacional de profesionistas ocupados"),
 "ING":        (21165, "Observatorio Laboral (STPS), ENOE-INEGI 2T-2026, área Ingeniería, Manufactura y Construcción"),
 "SERV":       (16898, "Observatorio Laboral (STPS), ENOE-INEGI 2T-2026, área Servicios"),
 "OCUP_SW":    (11000, "Data México (Secretaría de Economía), ENOE 1T-2026, ocupación Desarrolladores y Analistas de Software y Multimedia"),
 "SM":         (9577,  "CONASAMI, salario mínimo general vigente desde el 1-ene-2026: $315.04 diarios, resto del país"),
 "IMSS_SBC":   (20149, "IMSS, salario base de cotización promedio nacional, enero de 2026: $662.80 diarios"),
}

# perfil -> (ancla, factor, justificación del factor)
PERFIL_BASE = {
 "Director de proyecto":             ("TIC", 1.40, "Prima por responsabilidad directiva sobre alcance y presupuesto"),
 "Gerente de proyecto":              ("TIC", 1.20, "Prima por responsabilidad de planificación y control"),
 "Desarrollador de realidad virtual": ("TIC", 1.00, "Corresponde directamente al área de referencia"),
 "Desarrollador de gameplay":        ("TIC", 1.00, "Corresponde directamente al área de referencia"),
 "Diseñador de interacción UX-XR":   ("PROF",1.00, "Perfil mixto de diseño e ingeniería; se toma el promedio de profesionistas"),
 "Analista e investigador":          ("PROF",1.00, "Perfil de investigación documental y análisis"),
 "Artista y modelador 3D":           ("PROF",1.00, "Perfil creativo con formación profesional"),
 "Compositor y diseñador musical":   ("SERV",1.00, "Área de servicios, que agrupa los perfiles creativos y culturales"),
 "Diseñador de audio":               ("SERV",1.00, "Área de servicios, que agrupa los perfiles creativos y culturales"),
 "Analista de pruebas (QA)":         ("TIC", 0.80, "Descuento por ser un perfil de entrada dentro del área de TIC"),
 "Redactor técnico":                 ("PROF",0.85, "Descuento por ser un perfil de entrada"),
}
PERFIL = {p: (round(OFICIAL[a][0]*f/HMES, 2), round(OFICIAL[a][0]*f))
          for p,(a,f,_) in PERFIL_BASE.items()}

# ---- grupo de clave -> perfil que ejecuta ese trabajo
GRUPO = {}
for g in "DP DX DO DB DT DG DH DR".split():                GRUPO[g] = "Desarrollador de realidad virtual"
for g in "JA JT JK JB JN JW JP JI JF JC JL JM JY".split(): GRUPO[g] = "Desarrollador de gameplay"
for g in "EO EB EE ER EG EF EI ET".split():                GRUPO[g] = "Analista e investigador"
for g in "MR ML MP MB MA MN".split():                      GRUPO[g] = "Compositor y diseñador musical"
for g in "SP SB SE SM SI SU SA SC".split():                GRUPO[g] = "Diseñador de audio"
for g in "IM IW IS IE IG IT II IR".split():                GRUPO[g] = "Diseñador de interacción UX-XR"
for g in "AE AC AA AB AP AL AD AS AO AR".split():          GRUPO[g] = "Artista y modelador 3D"
GRUPO.update({                       # QA se desglosa: su trabajo no es de un solo perfil
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

MANO_OBRA = sum(costo(k) for k in R.ORD)
HORAS_TOT = sum(horas(k) for k in R.ORD)
TARIFA_MED= MANO_OBRA/HORAS_TOT

# ---- recursos proporcionados por la universidad: no son costo del proyecto
PROPORCIONADOS = [
 ("Visor Meta Quest 3","Equipo principal de desarrollo y pruebas",11999,"Préstamo de la Facultad"),
 ("Visor Meta Quest 3S","Segundo equipo, compatibilidad y sesiones simultáneas",6999,"Préstamo de la Facultad"),
 ("Espacio físico para pruebas","Aula o laboratorio para las sesiones con usuarios",0,"Instalaciones de la Facultad"),
]
VALOR_PROPORCIONADO = sum(x[2] for x in PROPORCIONADOS)

# ---- costos no laborales que sí desembolsa el proyecto
NO_LABORAL = [
 ("Equipo","Depreciación de equipo de cómputo","Parte proporcional del uso de las estaciones del equipo",8000),
 ("Equipo","Periféricos y accesorios","Cables, soportes, protectores faciales y baterías",2500),
 ("Licencias","Recursos gráficos y assets 3D","Se sustituyen por bancos con licencia libre (CC0 y equivalentes)",0),
 ("Licencias","Librería de muestras de audio","Se sustituye por bancos de muestras con licencia libre",0),
 ("Licencias","Licencias musicales","Pistas para el juego de ritmo. No se sustituyen: la oferta libre es insuficiente",3500),
 ("Licencias","Software de gestión de proyectos","Alternativa sin costo. Ver el análisis de herramientas",0),
 ("Operación","Traslados y logística","Sesiones de prueba con usuarios",4000),
 ("Operación","Consumibles e impresión","Documentación, consentimientos y material de pruebas",1500),
 ("Operación","Servicios digitales","Almacenamiento, control de versiones y colaboración",2250),
 ("Operación","Imprevistos menores de operación","Gastos operativos no clasificados",2000),
]
NO_LAB_TOT = sum(x[3] for x in NO_LABORAL)
DIRECTOS   = MANO_OBRA + NO_LAB_TOT

# ---- registro de riesgos con impacto monetario recalculado a las tarifas oficiales
# id, descripción, prob., impacto, categoría
RIESGOS = [
 ("R1","La latencia entre golpe y sonido supera los 30 ms y obliga a rehacer el sistema de audio",0.30,21000,"Técnico"),
 ("R2","La cadena del entorno tridimensional se retrasa y arrastra la fecha final",0.40,13500,"Cronograma"),
 ("R3","La carga de QA no cabe en su ventana y obliga a redistribuir trabajo",0.60,10000,"Recursos"),
 ("R4","Los recursos con licencia libre resultan insuficientes o de licencia ambigua",0.35,8000,"Externo"),
 ("R5","La Facultad no concreta el préstamo de los visores",0.20,18998,"Externo"),
 ("R6","Falla o indisponibilidad de un visor prestado durante el proyecto",0.15,9000,"Externo"),
 ("R7","Usuarios de prueba reportan mareo y hay que rehacer la ergonomía",0.20,7800,"Técnico"),
 ("R8","Pérdida de trabajo por conflicto de versiones",0.20,5000,"Técnico"),
 ("R9","Un integrante reduce su disponibilidad por carga académica",0.45,9000,"Recursos"),
]
def emv(r): return r[2]*r[3]
EMV          = sum(emv(r) for r in RIESGOS)
CONTINGENCIA = round(EMV/100)*100
LINEA_BASE   = DIRECTOS + CONTINGENCIA
GESTION      = round(LINEA_BASE*0.05/100)*100
PRESUPUESTO  = LINEA_BASE + GESTION

# ---- costo de la calidad
COQ = {
 "Prevención":      ["QP","QG","QR","QC"],
 "Evaluación":      ["QT","QV"],
 "Fallos internos": ["QE","DR","IR","AR"],
}
COQ_TOT = {c: sum(costo_grupo(g) for g in gs) for c,gs in COQ.items()}

# ---- escenarios de sensibilidad
def escenario(tar_h):
    mo = HORAS_TOT*tar_h; d = mo+NO_LAB_TOT
    lb = d+CONTINGENCIA; return mo, d, lb, lb+round(lb*0.05/100)*100
ESCENARIOS = [
 ("A. Costo de bolsillo",      0.0,          "El trabajo del equipo no se remunera: el proyecto es académico y se cursa por créditos."),
 ("B. Valorizado a practicante", OFICIAL["SM"][0]*1.5/HMES, "Un practicante de TIC percibe del orden de 1.5 salarios mínimos."),
 ("C. Valorizado a profesionista", TARIFA_MED, "Tarifas oficiales por perfil. Es la línea base."),
]

if __name__ == "__main__":
    print(f"horas           {HORAS_TOT:>12,.1f} h")
    print(f"mano de obra    ${MANO_OBRA:>12,.0f}   (tarifa media ${TARIFA_MED:.2f}/h)")
    print(f"no laboral      ${NO_LAB_TOT:>12,.0f}")
    print(f"directos        ${DIRECTOS:>12,.0f}")
    print(f"EMV riesgos     ${EMV:>12,.0f}  -> contingencia ${CONTINGENCIA:,.0f}")
    print(f"LÍNEA BASE      ${LINEA_BASE:>12,.0f}")
    print(f"reserva gestión ${GESTION:>12,.0f}")
    print(f"PRESUPUESTO     ${PRESUPUESTO:>12,.0f}")
    print(f"proporcionado por la Facultad (no es costo): ${VALOR_PROPORCIONADO:,.0f}")
    print()
    for nom,t,_ in ESCENARIOS:
        mo,d,lb,pt = escenario(t)
        print(f"  {nom:<32} mano de obra ${mo:>10,.0f}   presupuesto ${pt:>10,.0f}")
    print()
    for a in sorted(POR_AREA,key=lambda x:-POR_AREA[x][2]):
        n,h,c = POR_AREA[a]
        print(f"  {a[:30]:<32}{R.RESP[a]:<10}{n:>4}t{h:>7.0f} h  ${c:>9,.0f}  {100*c/MANO_OBRA:>5.1f}%")
    print()
    for c_,v in COQ_TOT.items(): print(f"  COQ {c_:<18}${v:>9,.0f}  {100*v/MANO_OBRA:>5.1f}%")
    print(f"  COQ {'TOTAL':<18}${sum(COQ_TOT.values()):>9,.0f}  {100*sum(COQ_TOT.values())/MANO_OBRA:>5.1f}%")
