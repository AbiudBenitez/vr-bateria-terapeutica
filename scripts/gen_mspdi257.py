# -*- coding: utf-8 -*-
"""Cronograma de las 257 tareas en MS Project XML (MSPDI), importable en ProjectLibre.

Incluye costos: cada recurso es una combinación de persona y perfil, con su tarifa
por hora derivada de la escala de múltiplos del salario mínimo de costos.py.
"""
import sys, os, json, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rc257 as R, costos as K
from xml.sax.saxutils import escape

NS   = "http://schemas.microsoft.com/project"
M    = R.V2
INI  = dt.date(2026, 9, 7)
FER  = {dt.date(2026, 9, 16), dt.date(2026, 11, 16)}
HDIA = 8

def habil(d): return d.weekday() < 5 and d not in FER
def momento(dias):
    h = round(dias*HDIA, 6); d = INI
    while not habil(d): d += dt.timedelta(days=1)
    while h >= HDIA:
        h -= HDIA; d += dt.timedelta(days=1)
        while not habil(d): d += dt.timedelta(days=1)
    t, extra = (dt.time(8,0), h) if h < 4 else (dt.time(13,0), h-4)
    return dt.datetime.combine(d, t) + dt.timedelta(hours=extra)
def fin_de(ini, dur):
    if dur <= 0: return momento(ini)
    f = momento(ini+dur)
    if f.time() == dt.time(8,0):
        d = f.date() - dt.timedelta(days=1)
        while not habil(d): d -= dt.timedelta(days=1)
        return dt.datetime.combine(d, dt.time(17,0))
    if f.time() == dt.time(13,0):
        return dt.datetime.combine(f.date(), dt.time(12,0))
    return f
def iso(x):   return x.strftime("%Y-%m-%dT%H:%M:%S")
def dur_h(n): return f"PT{int(round(n*HDIA))}H0M0S"
def wrk_h(h): return f"PT{h:g}H0M0S".replace(".0H","H")

# ---- avance real, de la hoja de control
_h = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hoja.json")))
ESTADO, REAL = {}, {}
for _f in _h:
    _k = _f[1].strip(); ESTADO[_k] = str(_f[5]).strip()
    if _f[10] and _f[10] != "None":
        try: REAL[_k] = dt.datetime.fromisoformat(_f[10])
        except Exception: pass
def avance(k):
    e = ESTADO.get(k, "")
    return 100 if e == "Completado" else (50 if e == "En curso" else 0)

# ---- recursos: una entrada por combinación de persona y perfil
COMB = {}                                   # (persona, perfil) -> [horas, costo, area]
for k in R.ORD:
    a = R.T[k]["area"]; key = (R.RESP[a], K.perfil(k))
    c = COMB.setdefault(key, [0.0, 0.0, a])
    c[0] += K.horas(k); c[1] += K.costo(k)
ORDEN_REC = sorted(COMB, key=lambda x: (-COMB[x][1], x[0]))
RUID = {key: i+1 for i, key in enumerate(ORDEN_REC)}
def recurso_de(k): return RUID[(R.RESP[R.T[k]["area"]], K.perfil(k))]

RAMAS = [("1","Gestión del proyecto")]      # no se usa; las ramas son las 8 áreas
uid = {}; n = 1
for a in R.AREAS:
    uid["#"+R.SIGLA[a]] = n; n += 1
    for k in R.ORD:
        if R.T[k]["area"] == a: uid[k] = n; n += 1

o  = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
o += f'<Project xmlns="{NS}">\n'
o += '  <Name>Cronograma_VR_Bateria.xml</Name>\n'
o += '  <Title>Simulación VR de batería con juego de ritmo — 257 tareas</Title>\n'
o += '  <Author>Equipo A</Author>\n  <Company>UANL FIME</Company>\n'
o += '  <ScheduleFromStart>1</ScheduleFromStart>\n'
o += f'  <StartDate>{iso(momento(0))}</StartDate>\n'
o += f'  <FinishDate>{iso(fin_de(0, M["TOTAL"]))}</FinishDate>\n'
o += '  <CurrencyDigits>0</CurrencyDigits>\n  <CurrencySymbol>$</CurrencySymbol>\n'
o += '  <CurrencySymbolPosition>0</CurrencySymbolPosition>\n  <CurrencyCode>MXN</CurrencyCode>\n'
o += '  <CalendarUID>1</CalendarUID>\n'
o += '  <DefaultStartTime>08:00:00</DefaultStartTime>\n  <DefaultFinishTime>17:00:00</DefaultFinishTime>\n'
o += '  <MinutesPerDay>480</MinutesPerDay>\n  <MinutesPerWeek>2400</MinutesPerWeek>\n'
o += '  <DaysPerMonth>20</DaysPerMonth>\n'
o += '  <DefaultStandardRate>0</DefaultStandardRate>\n  <DefaultOvertimeRate>0</DefaultOvertimeRate>\n'
o += '  <DefaultTaskType>0</DefaultTaskType>\n  <DefaultFixedCostAccrual>3</DefaultFixedCostAccrual>\n'
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

# ---------------------------------------------------------------- tareas
o += '  <Tasks>\n'
idx = 1
for ia, a in enumerate(R.AREAS, start=1):
    ks  = [k for k in R.ORD if R.T[k]["area"] == a]
    ini = min(M["ES"][k] for k in ks); fin = max(M["EF"][k] for k in ks)
    hs  = sum(K.horas(k) for k in ks); cs = sum(K.costo(k) for k in ks)
    o += ('    <Task>\n'
          f'      <UID>{uid["#"+R.SIGLA[a]]}</UID>\n      <ID>{idx}</ID>\n'
          f'      <Name>{escape(R.SIGLA[a] + ". " + a)}</Name>\n'
          '      <Type>1</Type>\n      <IsNull>0</IsNull>\n'
          f'      <WBS>{ia}</WBS>\n      <OutlineNumber>{ia}</OutlineNumber>\n'
          '      <OutlineLevel>1</OutlineLevel>\n      <Priority>500</Priority>\n'
          f'      <Start>{iso(momento(ini))}</Start>\n      <Finish>{iso(fin_de(0, fin))}</Finish>\n'
          f'      <Duration>{dur_h(fin-ini)}</Duration>\n      <DurationFormat>7</DurationFormat>\n'
          f'      <Work>{wrk_h(hs)}</Work>\n'
          '      <Milestone>0</Milestone>\n      <Summary>1</Summary>\n'
          f'      <FixedCost>0</FixedCost>\n      <FixedCostAccrual>3</FixedCostAccrual>\n'
          f'      <Cost>{cs:.2f}</Cost>\n'
          '    </Task>\n'); idx += 1
    for j, k in enumerate(ks, start=1):
        t = R.T[k]; crit = 1 if abs(M["HT"][k]) < 1e-9 else 0
        av = avance(k)
        o += ('    <Task>\n'
              f'      <UID>{uid[k]}</UID>\n      <ID>{idx}</ID>\n'
              f'      <Name>{escape(k + " — " + t["desc"])}</Name>\n'
              '      <Type>1</Type>\n      <IsNull>0</IsNull>\n'
              f'      <WBS>{ia}.{j}</WBS>\n      <OutlineNumber>{ia}.{j}</OutlineNumber>\n'
              '      <OutlineLevel>2</OutlineLevel>\n      <Priority>500</Priority>\n'
              f'      <Start>{iso(momento(M["ES"][k]))}</Start>\n'
              f'      <Finish>{iso(fin_de(M["ES"][k], t["dur"]))}</Finish>\n'
              f'      <Duration>{dur_h(t["dur"])}</Duration>\n      <DurationFormat>7</DurationFormat>\n'
              f'      <Work>{wrk_h(K.horas(k))}</Work>\n'
              f'      <Milestone>{1 if t["dur"]==0 else 0}</Milestone>\n      <Summary>0</Summary>\n'
              f'      <Critical>{crit}</Critical>\n'
              '      <FixedCost>0</FixedCost>\n      <FixedCostAccrual>3</FixedCostAccrual>\n'
              f'      <PercentComplete>{av}</PercentComplete>\n'
              f'      <PercentWorkComplete>{av}</PercentWorkComplete>\n'
              f'      <Cost>{K.costo(k):.2f}</Cost>\n')
        if av > 0:                                  # el orden del esquema es
            o += f'      <ActualStart>{iso(momento(M["ES"][k]))}</ActualStart>\n'   # ActualStart,
            if av == 100:                                                            # ActualFinish,
                _r = REAL.get(k)
                _f = _r.replace(hour=17, minute=0) if _r else fin_de(M["ES"][k], t["dur"])
                o += f'      <ActualFinish>{iso(_f)}</ActualFinish>\n'
            o += f'      <ActualCost>{K.costo(k)*av/100:.2f}</ActualCost>\n'         # ActualCost,
            o += f'      <ActualWork>{wrk_h(round(K.horas(k)*av/100,4))}</ActualWork>\n'  # ActualWork
        o += '      <ConstraintType>0</ConstraintType>\n' 
        for p in M["pre"][k]:
            o += ('      <PredecessorLink>\n'
                  f'        <PredecessorUID>{uid[p]}</PredecessorUID>\n'
                  '        <Type>1</Type>\n        <LinkLag>0</LinkLag>\n'
                  '        <LagFormat>7</LagFormat>\n      </PredecessorLink>\n')
        o += '    </Task>\n'; idx += 1
o += '  </Tasks>\n'

# ---------------------------------------------------------------- recursos
o += '  <Resources>\n'
for key in ORDEN_REC:
    persona, perf = key
    u = RUID[key]; h, c, area = COMB[key]
    tar = K.PERFIL[perf][0]
    o += (f'    <Resource>\n      <UID>{u}</UID>\n      <ID>{u}</ID>\n'
          f'      <Name>{escape(persona + " — " + perf)}</Name>\n'
          '      <Type>1</Type>\n      <IsNull>0</IsNull>\n'
          f'      <Initials>{escape(persona[:3])}</Initials>\n'
          f'      <Group>{escape(area)}</Group>\n'
          '      <MaxUnits>1</MaxUnits>\n'
          '      <AccrueAt>3</AccrueAt>\n'
          f'      <Work>{wrk_h(h)}</Work>\n'
          f'      <StandardRate>{tar:.2f}</StandardRate>\n'
          '      <StandardRateFormat>2</StandardRateFormat>\n'
          f'      <Cost>{c:.2f}</Cost>\n'
          f'      <OvertimeRate>{tar*1.5:.2f}</OvertimeRate>\n'
          '      <OvertimeRateFormat>2</OvertimeRateFormat>\n'
          '      <CostPerUse>0</CostPerUse>\n'
          '      <CalendarUID>1</CalendarUID>\n'
          f'      <Notes>{escape(f"{K.multiplo(perf):.1f} salarios mínimos por hora. Tarifa base: ${K.SM_HORA:.2f}/h.")}</Notes>\n'
          '    </Resource>\n')
o += '  </Resources>\n'

# ---------------------------------------------------------------- asignaciones
o += '  <Assignments>\n'
au = 1
for k in R.ORD:
    t = R.T[k]; av = avance(k); ru = recurso_de(k)
    ini_, fin_ = momento(M["ES"][k]), fin_de(M["ES"][k], t["dur"])
    o += (f'    <Assignment>\n      <UID>{au}</UID>\n'
          f'      <TaskUID>{uid[k]}</TaskUID>\n      <ResourceUID>{ru}</ResourceUID>\n'
          f'      <PercentWorkComplete>{av}</PercentWorkComplete>\n'
          f'      <ActualCost>{K.costo(k)*av/100:.2f}</ActualCost>\n'
          f'      <ActualWork>{wrk_h(round(K.horas(k)*av/100,4))}</ActualWork>\n'
          f'      <Cost>{K.costo(k):.2f}</Cost>\n'
          f'      <Finish>{iso(fin_)}</Finish>\n'
          f'      <Start>{iso(ini_)}</Start>\n'
          '      <Units>1</Units>\n'
          f'      <Work>{wrk_h(K.horas(k))}</Work>\n    </Assignment>\n'); au += 1
o += '  </Assignments>\n</Project>\n'

out = "/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/Cronograma_ProjectLibre.xml"
open(out, "w", encoding="utf-8").write(o)
print("OK", out)

import xml.etree.ElementTree as ET
r = ET.parse(out).getroot()
T_ = r.findall(f'{{{NS}}}Tasks/{{{NS}}}Task')
hojas = [x for x in T_ if x.findtext(f'{{{NS}}}Summary') == '0']
print("tareas:", len(T_), " hojas:", len(hojas),
      " recursos:", len(r.findall(f'{{{NS}}}Resources/{{{NS}}}Resource')),
      " asignaciones:", len(r.findall(f'{{{NS}}}Assignments/{{{NS}}}Assignment')),
      " vínculos:", sum(len(x.findall(f'{{{NS}}}PredecessorLink')) for x in T_))
suma = sum(float(x.findtext(f'{{{NS}}}Cost')) for x in hojas)
print(f"costo sumado en el XML: ${suma:,.2f}   modelo: ${K.MANO_OBRA:,.2f}   dif ${abs(suma-K.MANO_OBRA):.4f}")
print(f"inicio {iso(momento(0))}  fin {iso(fin_de(0, M['TOTAL']))}")
