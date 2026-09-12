# -*- coding: utf-8 -*-
"""Cronograma de las 257 tareas en MS Project XML (MSPDI), importable en MindView."""
import sys, os, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rc257 as R
from xml.sax.saxutils import escape

NS   = "http://schemas.microsoft.com/project"
M    = R.V2
INI  = dt.date(2026, 9, 7)                       # lunes, arranque real segun la hoja de control
FER  = {dt.date(2026, 9, 16), dt.date(2026, 11, 16)}
HDIA = 8                                          # 08:00-12:00 y 13:00-17:00

def habil(d):
    return d.weekday() < 5 and d not in FER

def momento(dias):
    """Convierte un desplazamiento en días laborables de 8 h a fecha y hora reales."""
    h = round(dias * HDIA, 6)
    d = INI
    while not habil(d): d += dt.timedelta(days=1)
    while h >= HDIA:
        h -= HDIA; d += dt.timedelta(days=1)
        while not habil(d): d += dt.timedelta(days=1)
    if h < 4:  t = dt.time(8, 0) ; extra = h
    else:      t = dt.time(13, 0); extra = h - 4
    base = dt.datetime.combine(d, t) + dt.timedelta(hours=extra)
    return base

def fin_de(dias_ini, dur):
    """Instante en que se agota la duración. Si cae justo al abrir la jornada o al
    volver de comer, se reporta el cierre del tramo anterior."""
    if dur <= 0: return momento(dias_ini)
    f = momento(dias_ini + dur)
    if f.time() == dt.time(8, 0):                      # alba: cerrar el día hábil previo
        d = f.date() - dt.timedelta(days=1)
        while not habil(d): d -= dt.timedelta(days=1)
        return dt.datetime.combine(d, dt.time(17, 0))
    if f.time() == dt.time(13, 0):                     # vuelta de comer: cerrar la mañana
        return dt.datetime.combine(f.date(), dt.time(12, 0))
    return f

def iso(x): return x.strftime("%Y-%m-%dT%H:%M:%S")
def durxml(dias): return f"PT{int(round(dias*HDIA))}H0M0S"

# ---- avance real, tomado de la hoja de control de tareas
import json
_h = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hoja.json")))
ESTADO, REAL = {}, {}
for _f in _h:
    _k = _f[1].strip()
    ESTADO[_k] = str(_f[5]).strip()
    if _f[10] and _f[10] != "None":
        try: REAL[_k] = dt.datetime.fromisoformat(_f[10])
        except Exception: pass
def avance(k):
    e = ESTADO.get(k, "")
    return 100 if e == "Completado" else (50 if e == "En curso" else 0)

RECURSOS = [(i+1, R.RESP[a], a) for i, a in enumerate(R.AREAS)]
RUID = {a: i+1 for i, a in enumerate(R.AREAS)}

# ---- UIDs: 8 resúmenes de área + 257 tareas
uid = {}; n = 1
for a in R.AREAS:
    uid["#"+R.SIGLA[a]] = n; n += 1
    for k in R.ORD:
        if R.T[k]["area"] == a: uid[k] = n; n += 1

o  = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
o += f'<Project xmlns="{NS}">\n'
o += '  <Name>Cronograma_257_Tareas_VR_Bateria.xml</Name>\n'
o += '  <Title>Simulación VR de batería con juego de ritmo — 257 tareas</Title>\n'
o += '  <Author>Equipo A</Author>\n  <Company>UANL FIME</Company>\n'
o += '  <ScheduleFromStart>1</ScheduleFromStart>\n'
o += f'  <StartDate>{iso(momento(0))}</StartDate>\n'
o += f'  <FinishDate>{iso(fin_de(0, M["TOTAL"]))}</FinishDate>\n'
o += '  <CurrencyCode>MXN</CurrencyCode>\n  <CalendarUID>1</CalendarUID>\n'
o += '  <DefaultStartTime>08:00:00</DefaultStartTime>\n  <DefaultFinishTime>17:00:00</DefaultFinishTime>\n'
o += '  <MinutesPerDay>480</MinutesPerDay>\n  <MinutesPerWeek>2400</MinutesPerWeek>\n'
o += '  <DaysPerMonth>20</DaysPerMonth>\n'
o += '  <Calendars>\n    <Calendar>\n      <UID>1</UID>\n      <Name>Estándar</Name>\n'
o += '      <IsBaseCalendar>1</IsBaseCalendar>\n      <BaseCalendarUID>-1</BaseCalendarUID>\n      <WeekDays>\n'
for ds in range(1, 8):
    lab = 1 if 2 <= ds <= 6 else 0
    o += f'        <WeekDay>\n          <DayType>{ds}</DayType>\n          <DayWorking>{lab}</DayWorking>\n'
    if lab:
        o += ('          <WorkingTimes>\n'
              '            <WorkingTime><FromTime>08:00:00</FromTime><ToTime>12:00:00</ToTime></WorkingTime>\n'
              '            <WorkingTime><FromTime>13:00:00</FromTime><ToTime>17:00:00</ToTime></WorkingTime>\n'
              '          </WorkingTimes>\n')
    o += '        </WeekDay>\n'
for d in sorted(FER):
    o += ('        <WeekDay>\n          <DayType>0</DayType>\n          <DayWorking>0</DayWorking>\n'
          f'          <TimePeriod><FromDate>{d.isoformat()}T00:00:00</FromDate>'
          f'<ToDate>{d.isoformat()}T23:59:00</ToDate></TimePeriod>\n        </WeekDay>\n')
o += '      </WeekDays>\n    </Calendar>\n  </Calendars>\n'

o += '  <Tasks>\n'
idx = 1
for ia, a in enumerate(R.AREAS, start=1):
    ks = [k for k in R.ORD if R.T[k]["area"] == a]
    ini = min(M["ES"][k] for k in ks); fin = max(M["EF"][k] for k in ks)
    o += ('    <Task>\n'
          f'      <UID>{uid["#"+R.SIGLA[a]]}</UID>\n      <ID>{idx}</ID>\n'
          f'      <Name>{escape(R.SIGLA[a] + ". " + a)}</Name>\n'
          '      <Type>1</Type>\n      <IsNull>0</IsNull>\n'
          f'      <WBS>{ia}</WBS>\n      <OutlineNumber>{ia}</OutlineNumber>\n'
          '      <OutlineLevel>1</OutlineLevel>\n      <Priority>500</Priority>\n'
          f'      <Start>{iso(momento(ini))}</Start>\n'
          f'      <Finish>{iso(fin_de(0, fin))}</Finish>\n'
          f'      <Duration>{durxml(fin-ini)}</Duration>\n      <DurationFormat>7</DurationFormat>\n'
          '      <Milestone>0</Milestone>\n      <Summary>1</Summary>\n'
          '    </Task>\n'); idx += 1
    for j, k in enumerate(ks, start=1):
        t = R.T[k]
        crit = 1 if abs(M["HT"][k]) < 1e-6 else 0
        o += ('    <Task>\n'
              f'      <UID>{uid[k]}</UID>\n      <ID>{idx}</ID>\n'
              f'      <Name>{escape(k + " — " + t["desc"])}</Name>\n'
              '      <Type>1</Type>\n      <IsNull>0</IsNull>\n'
              f'      <WBS>{ia}.{j}</WBS>\n      <OutlineNumber>{ia}.{j}</OutlineNumber>\n'
              '      <OutlineLevel>2</OutlineLevel>\n      <Priority>500</Priority>\n'
              f'      <Start>{iso(momento(M["ES"][k]))}</Start>\n'
              f'      <Finish>{iso(fin_de(M["ES"][k], t["dur"]))}</Finish>\n'
              f'      <Duration>{durxml(t["dur"])}</Duration>\n      <DurationFormat>7</DurationFormat>\n'
              f'      <Milestone>{1 if t["dur"]==0 else 0}</Milestone>\n      <Summary>0</Summary>\n'
              f'      <Critical>{crit}</Critical>\n'
              f'      <PercentComplete>{avance(k)}</PercentComplete>\n'
              f'      <PercentWorkComplete>{avance(k)}</PercentWorkComplete>\n')
        if avance(k) > 0:
            o += f'      <ActualStart>{iso(momento(M["ES"][k]))}</ActualStart>\n'
            if avance(k) == 100:
                _r = REAL.get(k)
                _f = _r.replace(hour=17, minute=0) if _r else fin_de(M["ES"][k], t["dur"])
                o += f'      <ActualFinish>{iso(_f)}</ActualFinish>\n'
        o += ('      <ConstraintType>0</ConstraintType>\n')
        for p in M["pre"][k]:
            o += ('      <PredecessorLink>\n'
                  f'        <PredecessorUID>{uid[p]}</PredecessorUID>\n'
                  '        <Type>1</Type>\n        <LinkLag>0</LinkLag>\n'
                  '        <LagFormat>7</LagFormat>\n      </PredecessorLink>\n')
        o += '    </Task>\n'; idx += 1
o += '  </Tasks>\n'

o += '  <Resources>\n'
for u, nom, area in RECURSOS:
    o += (f'    <Resource>\n      <UID>{u}</UID>\n      <ID>{u}</ID>\n'
          f'      <Name>{escape(nom)}</Name>\n'
          f'      <Initials>{escape(R.SIGLA[area])}</Initials>\n'
          f'      <Group>{escape(area)}</Group>\n'
          '      <Type>1</Type>\n      <IsNull>0</IsNull>\n      <MaxUnits>1</MaxUnits>\n'
          '      <CalendarUID>1</CalendarUID>\n    </Resource>\n')
o += '  </Resources>\n'

o += '  <Assignments>\n'
au = 1
for k in R.ORD:
    t = R.T[k]
    o += (f'    <Assignment>\n      <UID>{au}</UID>\n      <TaskUID>{uid[k]}</TaskUID>\n'
          f'      <ResourceUID>{RUID[t["area"]]}</ResourceUID>\n      <Units>1</Units>\n'
          f'      <Start>{iso(momento(M["ES"][k]))}</Start>\n'
          f'      <Finish>{iso(fin_de(M["ES"][k], t["dur"]))}</Finish>\n'
          f'      <Work>{durxml(t["dur"])}</Work>\n    </Assignment>\n'); au += 1
o += '  </Assignments>\n</Project>\n'

out = "/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/Cronograma_257_ProjectLibre.xml"
open(out, "w", encoding="utf-8").write(o)
print("OK", out)

import xml.etree.ElementTree as ET
r = ET.parse(out).getroot()
T_ = r.findall(f'{{{NS}}}Tasks/{{{NS}}}Task')
print("tareas:", len(T_),
      " resumen:", sum(1 for x in T_ if x.findtext(f'{{{NS}}}Summary')=='1'),
      " recursos:", len(r.findall(f'{{{NS}}}Resources/{{{NS}}}Resource')),
      " asignaciones:", len(r.findall(f'{{{NS}}}Assignments/{{{NS}}}Assignment')),
      " vinculos:", sum(len(x.findall(f'{{{NS}}}PredecessorLink')) for x in T_))
print("inicio:", iso(momento(0)), " fin:", iso(fin_de(0, M["TOTAL"])))
print("criticas marcadas:", sum(1 for x in T_ if x.findtext(f'{{{NS}}}Critical')=='1'))
