# -*- coding: utf-8 -*-
"""Cronograma en formato MS Project XML (MSPDI), importable en MindView."""
import sys, os, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdm, edt
from xml.sax.saxutils import escape

NS = "http://schemas.microsoft.com/project"
D1 = pdm.dia(0)                       # 2026-09-01
DFIN = pdm.dia(pdm.TOTAL-1)

def ini(d):  return f"{d.isoformat()}T08:00:00"
def fin(d):  return f"{d.isoformat()}T17:00:00"
def dur(n):  return f"PT{n*8}H0M0S"
def lag(d):  return d*8*60*10          # decimas de minuto (jornada de 8 h)

RAMAS = [("1","Gestión del proyecto"),("2","Fundamentación terapéutica"),
         ("3","Modelo tridimensional y entorno"),("4","Sistema de interacción y físicas"),
         ("5","Sistema de audio y rutinas"),("6","Prototipo funcional integrado"),
         ("7","Pruebas y documentación")]

RECURSOS = [(1,"Director de proyecto",375),(2,"Gerente de proyecto",277),(3,"Coordinador",173),
            (4,"Desarrollador de realidad virtual",260),(5,"Diseñador de interacción / UX-XR",219),
            (6,"Artista y modelador 3D",185),(7,"Diseñador de audio",162),
            (8,"Analista de métricas",196),(9,"Asesor terapéutico externo",900)]
MAPR = {"Director":1,"Gerente":2,"Coordinador":3,"Dev RV":4,"Desarrollador VR":4,"UX-XR":5,
        "Artista 3D":6,"Audio":7,"Métricas":8,"Asesor":9,"QA":2}
def recursos_de(res):
    out=[]
    for parte in res.replace(" / ","/").split("/"):
        for k,v in MAPR.items():
            if k.lower() in parte.lower():
                if v not in out: out.append(v)
                break
    return out or [2]

# ---- UIDs
uid = {}; n = 1
for r,_ in RAMAS:
    uid["R"+r] = n; n += 1
    for c,_,_,_,_,_,_ in edt.PKG:
        if c.split(".")[0] == r: uid[c] = n; n += 1
HITOS = [("H1","Diseño conceptual aprobado","H"),("H2","Go / No-Go de latencia","N"),
         ("H3","Modelos integrados con físicas","R"),("H4","Rutinas y métricas integradas","V"),
         ("H5","Build candidata congelada","X"),("H6","Cierre del proyecto","Z")]
uid["RH"] = n; n += 1
for h,_,_ in HITOS: uid[h] = n; n += 1

PKGD = {c:(c,nm,cr,rs,rc,ac,dd) for c,nm,cr,rs,rc,ac,dd in edt.PKG}
POR_ACT = {}
for c,nm,cr,rs,rc,ac,dd in edt.PKG:
    POR_ACT.setdefault(ac, []).append(c)
POR_ACT["Z"] = ["7.3","7.4","7.5","7.6","1.6"]

# ---- dependencias a nivel de paquete
LINKS = {}                             # codigo -> [(uid_pred, tipo, demora_dias)]
def add(c, p, tipo, l):
    LINKS.setdefault(c, []).append((uid[p], tipo, l))

for act, cods in POR_ACT.items():
    if act == "*": continue
    for a, b in zip(cods, cods[1:]):           # encadenado interno
        ia, fa = edt.FECHAS[a]; ib, fb = edt.FECHAS[b]
        if ib >= fa: add(b, a, 1, ib-fa)       # 1 = fin a inicio
        else:        add(b, a, 3, ib-ia)       # 3 = inicio a inicio
for k in pdm.ORD:                               # dependencias entre actividades
    for p, t, l in pdm.PRE[k]:
        if t == "FS": add(POR_ACT[k][0], POR_ACT[p][-1], 1, l)
        else:         add(POR_ACT[k][0], POR_ACT[p][0],  3, l)

def tarea(u, id_, nombre, nivel, outline, wbs, a, b, d, hito, resumen, links=None):
    x  = f'    <Task>\n      <UID>{u}</UID>\n      <ID>{id_}</ID>\n'
    x += f'      <Name>{escape(nombre)}</Name>\n      <Type>1</Type>\n      <IsNull>0</IsNull>\n'
    x += f'      <WBS>{wbs}</WBS>\n      <OutlineNumber>{outline}</OutlineNumber>\n'
    x += f'      <OutlineLevel>{nivel}</OutlineLevel>\n      <Priority>500</Priority>\n'
    x += f'      <Start>{ini(a)}</Start>\n      <Finish>{fin(b)}</Finish>\n'
    x += f'      <Duration>{dur(d)}</Duration>\n      <DurationFormat>7</DurationFormat>\n'
    x += f'      <Milestone>{1 if hito else 0}</Milestone>\n      <Summary>{1 if resumen else 0}</Summary>\n'
    if not resumen:
        x += f'      <ConstraintType>4</ConstraintType>\n      <ConstraintDate>{ini(a)}</ConstraintDate>\n'
    for pu, tp, lg in (links or []):
        x += ('      <PredecessorLink>\n'
              f'        <PredecessorUID>{pu}</PredecessorUID>\n'
              f'        <Type>{tp}</Type>\n'
              f'        <LinkLag>{lag(lg)}</LinkLag>\n'
              f'        <LagFormat>7</LagFormat>\n'
              '      </PredecessorLink>\n')
    return x + '    </Task>\n'

# ---- documento
o  = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
o += f'<Project xmlns="{NS}">\n'
o += '  <Name>Cronograma_Bateria_VR_Musicoterapia.xml</Name>\n'
o += '  <Title>Simulación de batería en realidad virtual con enfoque de musicoterapia</Title>\n'
o += '  <Author>Equipo A</Author>\n  <Company>UANL FIME</Company>\n'
o += '  <ScheduleFromStart>1</ScheduleFromStart>\n'
o += f'  <StartDate>{ini(D1)}</StartDate>\n  <FinishDate>{fin(DFIN)}</FinishDate>\n'
o += '  <CurrencyCode>MXN</CurrencyCode>\n  <CalendarUID>1</CalendarUID>\n'
o += '  <DefaultStartTime>08:00:00</DefaultStartTime>\n  <DefaultFinishTime>17:00:00</DefaultFinishTime>\n'
o += '  <MinutesPerDay>480</MinutesPerDay>\n  <MinutesPerWeek>2400</MinutesPerWeek>\n'
o += '  <DaysPerMonth>20</DaysPerMonth>\n'
o += '  <Calendars>\n    <Calendar>\n      <UID>1</UID>\n      <Name>Estándar</Name>\n'
o += '      <IsBaseCalendar>1</IsBaseCalendar>\n      <BaseCalendarUID>-1</BaseCalendarUID>\n      <WeekDays>\n'
for dia_sem in range(1, 8):
    lab = 1 if 2 <= dia_sem <= 6 else 0
    o += f'        <WeekDay>\n          <DayType>{dia_sem}</DayType>\n          <DayWorking>{lab}</DayWorking>\n'
    if lab:
        o += ('          <WorkingTimes>\n'
              '            <WorkingTime><FromTime>08:00:00</FromTime><ToTime>12:00:00</ToTime></WorkingTime>\n'
              '            <WorkingTime><FromTime>13:00:00</FromTime><ToTime>17:00:00</ToTime></WorkingTime>\n'
              '          </WorkingTimes>\n')
    o += '        </WeekDay>\n'
for f_ in ("2026-09-16", "2026-11-16"):
    o += ('        <WeekDay>\n          <DayType>0</DayType>\n          <DayWorking>0</DayWorking>\n'
          f'          <TimePeriod><FromDate>{f_}T00:00:00</FromDate><ToDate>{f_}T23:59:00</ToDate></TimePeriod>\n'
          '        </WeekDay>\n')
o += '      </WeekDays>\n    </Calendar>\n  </Calendars>\n'

o += '  <Tasks>\n'
idx = 1
for r, nom in RAMAS:
    cods = [c for c,_,_,_,_,_,_ in edt.PKG if c.split(".")[0] == r]
    a = min(edt.rango(c)[0] for c in cods); b = max(edt.rango(c)[1] for c in cods)
    nd = sum(1 for _ in range(0))  # placeholder
    o += tarea(uid["R"+r], idx, f"{r}. {nom}", 1, r, r, a, b,
               pdm.habiles(a, b), False, True); idx += 1
    for c in cods:
        _, nm, cr, rs, rc, ac, dd = PKGD[c]
        ca, cb = edt.rango(c)
        o += tarea(uid[c], idx, nm, 2, c, c, ca, cb, dd, False, False, LINKS.get(c)); idx += 1
a = min(pdm.dia(pdm.EF[x]-1) for _,_,x in HITOS); b = max(pdm.dia(pdm.EF[x]-1) for _,_,x in HITOS)
o += tarea(uid["RH"], idx, "8. Hitos de control", 1, "8", "8", a, b, pdm.habiles(a,b), False, True); idx += 1
for h, nom, act in HITOS:
    d_ = pdm.dia(pdm.EF[act]-1)
    o += tarea(uid[h], idx, f"{h} — {nom}", 2, f"8.{h[1]}", f"8.{h[1]}", d_, d_, 0, True, False); idx += 1
o += '  </Tasks>\n'

o += '  <Resources>\n'
for u, nom, tar in RECURSOS:
    o += (f'    <Resource>\n      <UID>{u}</UID>\n      <ID>{u}</ID>\n      <Name>{escape(nom)}</Name>\n'
          f'      <Type>1</Type>\n      <IsNull>0</IsNull>\n      <MaxUnits>1</MaxUnits>\n'
          f'      <StandardRate>{tar}</StandardRate>\n      <StandardRateFormat>2</StandardRateFormat>\n'
          f'      <CalendarUID>1</CalendarUID>\n    </Resource>\n')
o += '  </Resources>\n'

o += '  <Assignments>\n'
au = 1
for c, nm, cr, rs, rc, ac, dd in edt.PKG:
    for r_ in recursos_de(rs):
        ca, cb = edt.rango(c)
        o += (f'    <Assignment>\n      <UID>{au}</UID>\n      <TaskUID>{uid[c]}</TaskUID>\n'
              f'      <ResourceUID>{r_}</ResourceUID>\n      <Units>1</Units>\n'
              f'      <Start>{ini(ca)}</Start>\n      <Finish>{fin(cb)}</Finish>\n    </Assignment>\n')
        au += 1
o += '  </Assignments>\n</Project>\n'

out = "/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/superados/Cronograma_MindView_42_paquetes.xml"
open(out, "w", encoding="utf-8").write(o)
print("OK", out)
import xml.etree.ElementTree as ET
t = ET.parse(out); root = t.getroot()
print("tareas:", len(root.findall(f'{{{NS}}}Tasks/{{{NS}}}Task')),
      " recursos:", len(root.findall(f'{{{NS}}}Resources/{{{NS}}}Resource')),
      " asignaciones:", len(root.findall(f'{{{NS}}}Assignments/{{{NS}}}Assignment')),
      " vinculos:", sum(len(x.findall(f'{{{NS}}}PredecessorLink')) for x in root.iter(f'{{{NS}}}Task')))
