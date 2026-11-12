# -*- coding: utf-8 -*-
"""Rebasea los dos cronogramas: fechas reales en lo cerrado, replan del 12 al 20-nov en lo que falta.

QUE ESTABA MAL
--------------
Hasta el 11-nov-2026 los dos XML programaban todo lo antes posible desde el 7-sep y nunca se
les volvio a dar fecha. No habia ni un `ActualStart`, ni un `StatusDate`, y el `CurrentDate`
seguia congelado el 17-oct. Las actividades cerradas llevaban su fecha PLANEADA, de 3 a 6
semanas antes de cuando pasaron, asi que el proyecto entero se veia terminado el 6-oct en el
operativo y el 19-oct en el de ProjectLibre. Ninguna de las dos XML tenia una fecha en
noviembre, y por eso el Gantt decia que ya habiamos acabado.

QUE ESCRIBE
-----------
  cerradas    Finish = Stop = ActualFinish = su fecha de registro (scripts/cierres.py)
              Start = ese dia menos su duracion, en dias habiles
  pendientes  Start y Finish del replan traslapado (scripts/replan.py)
  todas       ConstraintType 4 (no antes de) con ConstraintDate en su inicio, y
              HonorConstraints 1 en la cabecera, para que al recalcular no se vayan
              de nuevo a septiembre
  calendario  los siete fines de semana que si se trabajaron quedan abiertos como
              excepcion, porque dos de ellos —sabado 17 y domingo 18 de octubre— son
              los dos dias de mayor cierre del proyecto
  cabecera    StatusDate y CurrentDate al 11-nov, FinishDate al 20-nov

NO TOCA las 101 recortadas del cronograma de ProjectLibre: siguen con su nota
[FUERA DE ALCANCE] y con las fechas de la linea base anterior, que es lo que son.

Es idempotente: correrlo dos veces deja el mismo archivo.
"""
import datetime as D
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cierres as CI
import rc257 as R
import replan as RP

AQUI = os.path.dirname(os.path.abspath(__file__))
OPERATIVO = os.path.join(AQUI, "..", "entregables", "Cronograma_Operativo.xml")
PROJECTLIBRE = os.path.join(AQUI, "..", "entregables", "Cronograma_ProjectLibre.xml")

CORTE = D.date(2026, 11, 11)      # fecha de estado
CIERRE = RP.CIERRE                # 2026-11-20, calculado por el replan
ABIERTOS = {D.date.fromisoformat(x) for x in CI.FINES_DE_SEMANA_TRABAJADOS}


def habil(d):
    return d.weekday() < 5 or d in ABIERTOS


def atras(d, n):
    """n dias habiles hacia atras desde d."""
    while n > 0:
        d -= D.timedelta(days=1)
        while not habil(d):
            d -= D.timedelta(days=1)
        n -= 1
    return d


def clave(nombre):
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre or "")
    return m.group(1) if m else None


def _campo(bloque, etiqueta, valor):
    """Fija un campo si existe; si no, lo inserta antes de </Task>."""
    if "<%s>" % etiqueta in bloque:
        return re.sub(r"<%s>.*?</%s>" % (etiqueta, etiqueta),
                      "<%s>%s</%s>" % (etiqueta, valor, etiqueta), bloque, flags=re.S)
    return bloque.replace("</Task>", "<%s>%s</%s></Task>" % (etiqueta, valor, etiqueta))


def _quitar(bloque, etiqueta):
    return re.sub(r"<%s>.*?</%s>" % (etiqueta, etiqueta), "", bloque, flags=re.S)


def ventana(k, cerrada):
    """(inicio, fin) como fechas, para la actividad k."""
    dur = R.T[k]["dur"] if k in R.T else 0.0
    if cerrada:
        fin = D.date.fromisoformat(CI.CIERRES[k][0])
        dias = max(1, int(dur + 0.999)) if dur > 0 else 1
        ini = atras(fin, dias - 1)
        return ini, fin
    return RP.CALENDARIO[k]


def arreglar_tarea(bloque, k):
    cerrada = k in CI.CIERRES
    if not cerrada and k not in RP.CALENDARIO:
        return bloque, False          # recortada o fuera de los dos conjuntos: no se toca
    ini, fin = ventana(k, cerrada)
    hito = "<Milestone>1</Milestone>" in bloque
    s_ini = "%sT08:00:00" % ini
    s_fin = "%sT17:00:00" % fin
    if hito:
        s_ini = s_fin = "%sT08:00:00" % fin

    b = bloque
    b = _campo(b, "Start", s_ini)
    b = _campo(b, "Finish", s_fin)
    b = _campo(b, "ConstraintType", "4")
    b = _campo(b, "ConstraintDate", s_ini)

    if cerrada:
        b = _campo(b, "Stop", s_fin)
        b = _campo(b, "Resume", s_fin)
        b = _campo(b, "ActualStart", s_ini)
        b = _campo(b, "ActualFinish", s_fin)
        b = _campo(b, "PercentComplete", "100")
        b = _campo(b, "PercentWorkComplete", "100")
        b = _quitar(b, "RemainingDuration")
        dur = re.search(r"<Duration>(.*?)</Duration>", b)
        if dur:
            b = _campo(b, "ActualDuration", dur.group(1))
    else:
        b = _quitar(b, "Stop")
        b = _quitar(b, "Resume")
        b = _quitar(b, "ActualStart")
        b = _quitar(b, "ActualFinish")
        b = _quitar(b, "ActualDuration")
        b = _campo(b, "PercentComplete", "0")
        b = _campo(b, "PercentWorkComplete", "0")
        dur = re.search(r"<Duration>(.*?)</Duration>", b)
        if dur:
            b = _campo(b, "RemainingDuration", dur.group(1))
    return b, True


EXCEPCION = """
                <Exception>
                    <EnteredByOccurrences>0</EnteredByOccurrences>
                    <TimePeriod>
                        <FromDate>%sT00:00:00</FromDate>
                        <ToDate>%sT23:59:00</ToDate>
                    </TimePeriod>
                    <Occurrences>1</Occurrences>
                    <Type>1</Type>
                    <DayWorking>1</DayWorking>
                    <WorkingTimes>
                        <WorkingTime>
                            <FromTime>08:00:00</FromTime>
                            <ToTime>12:00:00</ToTime>
                        </WorkingTime>
                        <WorkingTime>
                            <FromTime>13:00:00</FromTime>
                            <ToTime>17:00:00</ToTime>
                        </WorkingTime>
                    </WorkingTimes>
                </Exception>"""
MARCA = "<!-- fines de semana trabajados, abiertos por rebaselinear.py -->"


def abrir_fines_de_semana(texto):
    """Abre en el calendario del proyecto los fines de semana que si se trabajaron."""
    if MARCA in texto:
        return texto, 0
    # El calendario del proyecto no tiene el mismo UID en los dos archivos: 34 en el
    # operativo y 19 en el de ProjectLibre. Se lee de la cabecera, no se supone.
    uid = re.search(r"<CalendarUID>(\d+)</CalendarUID>", texto)
    if not uid:
        return texto, 0
    cal = re.search(r"(<Calendar>\s*<UID>%s</UID>.*?</Calendar>)" % uid.group(1),
                    texto, re.S)
    if not cal or "<Exceptions>" not in cal.group(1):
        return texto, 0
    bloque = cal.group(1)
    nuevas = MARCA + "".join(EXCEPCION % (d, d)
                             for d in sorted(CI.FINES_DE_SEMANA_TRABAJADOS))
    nuevo = bloque.replace("</Exceptions>", nuevas + "\n            </Exceptions>")
    return texto.replace(bloque, nuevo), len(CI.FINES_DE_SEMANA_TRABAJADOS)


def rodar_resumenes(texto):
    """Recalcula Start y Finish de cada resumen a partir de sus hijas."""
    bloques = re.findall(r"<Task>.*?</Task>", texto, re.S)
    grupos, actual = {}, None
    for b in bloques:
        es_resumen = "<Summary>1</Summary>" in b
        nivel = re.search(r"<OutlineLevel>(\d+)</OutlineLevel>", b)
        if es_resumen and nivel and nivel.group(1) == "1":
            actual = b
            grupos[actual] = []
        elif actual is not None and not es_resumen:
            grupos[actual].append(b)
    hechos = 0
    for res, hijas in grupos.items():
        fechas = []
        for h in hijas:
            s = re.search(r"<Start>(.*?)</Start>", h)
            f = re.search(r"<Finish>(.*?)</Finish>", h)
            if s and f:
                fechas.append((s.group(1), f.group(1)))
        if not fechas:
            continue
        nuevo = _campo(res, "Start", min(x[0] for x in fechas))
        nuevo = _campo(nuevo, "Finish", max(x[1] for x in fechas))
        if nuevo != res:
            texto = texto.replace(res, nuevo, 1)
            hechos += 1
    return texto, hechos


def cabecera(texto):
    arranques = re.findall(r"<Start>(\d{4}-\d\d-\d\d)T", texto)
    inicio = min(arranques)
    texto = re.sub(r"<StartDate>.*?</StartDate>",
                   "<StartDate>%sT08:00:00</StartDate>" % inicio, texto)
    texto = re.sub(r"<FinishDate>.*?</FinishDate>",
                   "<FinishDate>%sT17:00:00</FinishDate>" % CIERRE, texto)
    texto = re.sub(r"<CurrentDate>.*?</CurrentDate>",
                   "<CurrentDate>%sT17:00:00</CurrentDate>" % CORTE, texto)
    texto = re.sub(r"<HonorConstraints>.*?</HonorConstraints>",
                   "<HonorConstraints>1</HonorConstraints>", texto)
    if "<StatusDate>" in texto:
        texto = re.sub(r"<StatusDate>.*?</StatusDate>",
                       "<StatusDate>%sT17:00:00</StatusDate>" % CORTE, texto)
    else:
        texto = texto.replace("<CurrentDate>",
                              "<StatusDate>%sT17:00:00</StatusDate><CurrentDate>" % CORTE, 1)
    return texto, inicio


def rebasear(ruta):
    texto = open(ruta, encoding="utf-8").read()
    bloques = re.findall(r"<Task>.*?</Task>", texto, re.S)
    tocadas, intactas = [], []
    for b in bloques:
        nm = re.search(r"<Name>(.*?)</Name>", b, re.S)
        if not nm or "<Summary>1</Summary>" in b:
            continue
        k = clave(nm.group(1))
        if not k:
            continue
        nuevo, cambio = arreglar_tarea(b, k)
        if cambio:
            texto = texto.replace(b, nuevo, 1)
            tocadas.append(k)
        else:
            intactas.append(k)
    texto, exc = abrir_fines_de_semana(texto)
    texto, res = rodar_resumenes(texto)
    texto, inicio = cabecera(texto)
    open(ruta, "w", encoding="utf-8").write(texto)
    return tocadas, intactas, exc, res, inicio


if __name__ == "__main__":
    for ruta in (OPERATIVO, PROJECTLIBRE):
        tocadas, intactas, exc, res, inicio = rebasear(ruta)
        cerradas = [k for k in tocadas if k in CI.CIERRES]
        print(os.path.basename(ruta))
        print("  refechadas    %d  (%d cerradas, %d pendientes)"
              % (len(tocadas), len(cerradas), len(tocadas) - len(cerradas)))
        print("  sin tocar     %d  (recortadas de la linea base anterior)" % len(intactas))
        print("  excepciones de calendario anadidas: %d" % exc)
        print("  resumenes recalculados: %d" % res)
        print("  arranque %s   cierre %s   fecha de estado %s" % (inicio, CIERRE, CORTE))
        print()
