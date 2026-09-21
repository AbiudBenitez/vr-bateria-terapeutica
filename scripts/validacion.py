# -*- coding: utf-8 -*-
"""
Datos para la carta de validación y la lista de verificación.

Las cifras se LEEN del cronograma y de la hoja de control, no se escriben a mano. Es la
convención del proyecto: una cifra aparece en varios documentos y tiene que poder regenerarse
cuando cambie. Escribirla a mano es cómo se llega a tener tres números distintos para la misma
cosa, que es exactamente lo que esta carta viene a resolver.
"""
import pathlib
import re
import xml.etree.ElementTree as ET

NS = "{http://schemas.microsoft.com/project}"
RAIZ = pathlib.Path(__file__).resolve().parent.parent
CRONO = RAIZ / "entregables" / "Cronograma_ProjectLibre.xml"
HOJA = pathlib.Path.home() / "Downloads" / "Hoja de control de tareas.xlsx"

AREAS = {
    "D": "Desarrollo VR y batería",
    "J": "Juego de ritmo",
    "Q": "QA, documentación y gestión",
    "E": "Experiencia emocional",
    "S": "Sonido",
    "M": "Música",
    "I": "Interfaz / UX-UI",
    "A": "Entorno 3D",
}


def clave(nombre):
    """La clave de una tarea a partir de su nombre: 'DG.1 — Crear...' -> 'DG.1'."""
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre)
    return m.group(1) if m else None


def cronograma():
    """Lee el cronograma. Devuelve {clave: porcentaje} solo de tareas reales."""
    raiz = ET.parse(CRONO).getroot()
    tareas = {}
    for t in raiz.iter(NS + "Task"):
        nm = t.find(NS + "Name")
        sm = t.find(NS + "Summary")
        if nm is None or not nm.text:
            continue
        if sm is not None and sm.text == "1":       # los resúmenes no son trabajo
            continue
        k = clave(nm.text)
        if not k:
            continue
        pc = t.find(NS + "PercentComplete")
        tareas[k] = dict(
            nombre=nm.text.split("—", 1)[-1].strip(),
            pct=int(pc.text) if pc is not None and pc.text else 0,
        )
    return tareas


def hoja_control():
    """Lee la hoja de control del equipo. Devuelve {clave: {responsable, estado, ...}}."""
    if not HOJA.exists():
        return {}
    import openpyxl
    ws = openpyxl.load_workbook(HOJA, data_only=True).active
    filas = {}
    for f in ws.iter_rows(min_row=3, values_only=True):
        if not f[1]:
            continue
        filas[str(f[1]).strip()] = dict(
            area=str(f[2]).strip() if f[2] else "",
            tarea=str(f[3]).strip() if f[3] else "",
            responsable=str(f[4]).strip() if f[4] else "",
            estado=str(f[5]).strip() if f[5] else "",
            compromiso=f[9],
        )
    return filas


def fusion():
    """
    Combina ambas fuentes. El cronograma manda en el porcentaje, la hoja en el responsable.

    El cronograma manda porque ya lleva la unión de las dos fuentes: la hoja registra el
    trabajo documental del equipo y el cronograma añade el área D, que la hoja nunca
    actualizó. Tomar solo la hoja perdería 21 tareas construidas y verificables.
    """
    cr, hj = cronograma(), hoja_control()
    out = {}
    for k in set(cr) | set(hj):
        c = cr.get(k, {})
        h = hj.get(k, {})
        out[k] = dict(
            clave=k,
            tarea=h.get("tarea") or c.get("nombre", ""),
            responsable=h.get("responsable", "—"),
            area=h.get("area", ""),
            compromiso=h.get("compromiso"),
            pct=c.get("pct", 0),
            estado_hoja=h.get("estado", "—"),
            hecha=c.get("pct", 0) == 100,
        )
    return out


def resumen():
    """Cifras agregadas, listas para meter en un documento."""
    f = fusion()
    hechas = [t for t in f.values() if t["hecha"]]
    por_resp = {}
    for t in f.values():
        r = t["responsable"]
        d = por_resp.setdefault(r, dict(total=0, hechas=0))
        d["total"] += 1
        d["hechas"] += 1 if t["hecha"] else 0
    por_area = {}
    for t in hechas:
        a = AREAS.get(t["clave"][0], t["clave"][0])
        por_area[a] = por_area.get(a, 0) + 1
    return dict(
        total=len(f),
        hechas=len(hechas),
        pct=100.0 * len(hechas) / max(len(f), 1),
        por_responsable=dict(sorted(por_resp.items(), key=lambda kv: -kv[1]["hechas"])),
        por_area=dict(sorted(por_area.items(), key=lambda kv: -kv[1])),
        # Las que la hoja del equipo no refleja: el desfase que la carta declara.
        desfase=sorted(t["clave"] for t in f.values()
                       if t["hecha"] and t["estado_hoja"] != "Completado"),
    )


if __name__ == "__main__":
    r = resumen()
    print(f"  {r['hechas']} de {r['total']} terminadas ({r['pct']:.0f}%)")
    print("\n  por responsable:")
    for k, v in r["por_responsable"].items():
        print(f"    {k:12s} {v['hechas']:3d} de {v['total']:3d}")
    print("\n  por área:")
    for k, v in r["por_area"].items():
        print(f"    {k:30s} {v}")
    print(f"\n  terminadas que la hoja no refleja: {len(r['desfase'])}")
    print(f"    {', '.join(r['desfase'])}")
