# -*- coding: utf-8 -*-
"""Lee los volcados de sesion del visor. Datos reales, ninguno calculado a mano.

LAS SESIONES NO LLEVAN IDENTIFICADOR DE PARTICIPANTE. Llevan fecha, BPM, notas, precision,
constancia y los desfases crudos. Por eso este modulo habla de SESIONES y nunca de personas:
decir "14 participantes" a partir de estos archivos seria inventar la atribucion.

SE CUENTAN SOLO LAS PISTAS COMPLETAS -40 notas o mas-. Las de menos son arranques de prueba
y pruebas de cableado, y meterlas en la media la hunde sin que mida nada.
"""
import glob
import json
import os
import statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))

# El volcado vive en el repo Unity, que es donde `quest.sh pull` lo deja.
CARPETAS = [
    os.path.expanduser("~/Documents/code/Unity/BateriaVR/mediciones/files"),
    os.path.join(AQUI, "..", "entregables", "mediciones"),
]

MINIMO_NOTAS = 40


def _archivos(patron):
    for c in CARPETAS:
        hallados = sorted(glob.glob(os.path.join(c, patron)))
        if hallados:
            return hallados
    return []


def cargar():
    out = []
    for f in _archivos("sesion_*.json"):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("notas", {}).get("total", 0) < MINIMO_NOTAS:
            continue
        d["_archivo"] = os.path.basename(f)
        d["_fecha"] = os.path.basename(f)[7:15]
        out.append(d)
    return out


SESIONES = cargar()


def resumen():
    if not SESIONES:
        return None
    pr = [s["precisionPorcentaje"] for s in SESIONES]
    cg = [s["precisionTemporal"]["desviacionMs"] for s in SESIONES
          if "desviacionMs" in s.get("precisionTemporal", {})]
    cp = [s["constanciaPulsoMs"] for s in SESIONES if "constanciaPulsoMs" in s]
    notas = sum(s["notas"]["total"] for s in SESIONES)
    aciertos = sum(s["aciertos"] for s in SESIONES)
    return {
        "sesiones": len(SESIONES),
        "fechas": sorted({s["_fecha"] for s in SESIONES}),
        "notas": notas,
        "aciertos": aciertos,
        "precision_global": 100.0 * aciertos / notas if notas else 0.0,
        "precision_min": min(pr), "precision_mediana": st.median(pr),
        "precision_max": max(pr),
        "rejilla_mediana": st.median(cg) if cg else None,
        "pulso_mediana": st.median(cp) if cp else None,
        "bpm": sorted({s["bpm"] for s in SESIONES}),
        "mejor": max(SESIONES, key=lambda s: s["precisionPorcentaje"]),
    }


def tutoriales():
    out = []
    for f in _archivos("tutorial_*.json"):
        try:
            out.append(json.load(open(f, encoding="utf-8")))
        except Exception:
            pass
    return out


if __name__ == "__main__":
    r = resumen()
    if not r:
        raise SystemExit("No encontre volcados de sesion. Corre quest.sh pull en el repo Unity.")
    print("%d sesiones con pista completa (>=%d notas)" % (r["sesiones"], MINIMO_NOTAS))
    print("  fechas          %s" % ", ".join(r["fechas"]))
    print("  notas           %d, aciertos %d, global %.1f %%"
          % (r["notas"], r["aciertos"], r["precision_global"]))
    print("  precision       min %.1f  mediana %.1f  max %.1f"
          % (r["precision_min"], r["precision_mediana"], r["precision_max"]))
    print("  contra rejilla  mediana %s ms" % (
          "%.1f" % r["rejilla_mediana"] if r["rejilla_mediana"] is not None else "sin dato"))
    print("  pulso propio    mediana %s ms" % (
          "%.1f" % r["pulso_mediana"] if r["pulso_mediana"] is not None else "sin dato"))
    print("  tempos          %s" % ", ".join("%g" % b for b in r["bpm"]))
    print("  tutoriales      %d volcados" % len(tutoriales()))
