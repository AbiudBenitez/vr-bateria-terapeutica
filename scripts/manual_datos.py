# -*- coding: utf-8 -*-
"""Los hechos del repo Unity que los manuales no deben teclear a mano.

POR QUE UNA CACHE Y NO LEER EL REPO DIRECTO
-------------------------------------------
Los dos repositorios son independientes. El espejo `proyecto-unity/` de esta carpeta quedo en
septiembre —no tiene ni `Flujo` ni `Tutorial`—, asi que no sirve. Y leer el repo Unity real
deja los generadores inservibles para cualquier integrante que no lo tenga clonado en la misma
ruta.

La cache resuelve las dos cosas:

    python3 manual_datos.py --refrescar    reescribe datos_unity.json desde el repo Unity
    DATOS                                  lo que leen los generadores, siempre de la cache

La ruta del repo sale de BATERIAVR_REPO, y si no esta, del valor por omision de abajo. Una
prueba comprueba que la cache coincide con el repo CUANDO el repo esta presente; cuando no
esta, esa prueba se salta y las demas siguen valiendo.

LO QUE SE EXTRAE es justo lo que caduca: versiones, identificador del paquete, los comandos
del menu del editor, los estados de la aplicacion, los rotulos de los pads por pantalla, los
pasos del tutorial, las pruebas y los paquetes del Asset Store ausentes. Nada de prosa: la
prosa va en los generadores, que es donde se puede escribir bien.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(AQUI, "datos_unity.json")

REPO_POR_OMISION = os.path.expanduser("~/Documents/code/Unity/BateriaVR")


def repo():
    """Ruta del repo Unity, o None si no esta."""
    r = os.environ.get("BATERIAVR_REPO") or REPO_POR_OMISION
    return r if os.path.isdir(os.path.join(r, "Assets")) else None


# ------------------------------------------------------------------ extraccion

def _texto(ruta):
    with open(ruta, encoding="utf-8", errors="replace") as f:
        return f.read()


def _cs(raiz):
    """Todos los .cs del proyecto, con su ruta relativa."""
    for base, _, archivos in os.walk(os.path.join(raiz, "Assets")):
        for a in archivos:
            if a.endswith(".cs"):
                p = os.path.join(base, a)
                yield os.path.relpath(p, raiz), p


def _ajustes(raiz):
    s = _texto(os.path.join(raiz, "ProjectSettings", "ProjectSettings.asset"))
    out = {}
    for campo, etiqueta in (("companyName", "empresa"), ("productName", "producto"),
                            ("bundleVersion", "version")):
        m = re.search(r"^\s*%s:\s*(.+)$" % campo, s, re.M)
        out[etiqueta] = m.group(1).strip() if m else ""
    m = re.search(r"applicationIdentifier:.*?Android:\s*(\S+)", s, re.S)
    out["paquete"] = m.group(1).strip() if m else ""
    ver = _texto(os.path.join(raiz, "ProjectSettings", "ProjectVersion.txt"))
    m = re.search(r"m_EditorVersion:\s*(\S+)", ver)
    out["unity"] = m.group(1) if m else ""
    return out


def _menu(raiz):
    """Los comandos del menu del editor, agrupados por submenu. Solo los del proyecto."""
    items = set()
    for rel, p in _cs(raiz):
        for m in re.finditer(r'MenuItem\("([^"]+)"', _texto(p)):
            ruta = m.group(1)
            if ruta.startswith("Batería/") or ruta.startswith("Bateria/"):
                items.add(ruta)
    salida = {}
    for ruta in sorted(items):
        partes = ruta.split("/")
        grupo = partes[1] if len(partes) > 2 else "(raíz)"
        salida.setdefault(grupo, []).append(partes[-1])
    for g in salida:
        salida[g].sort()
    return salida


def _enum(texto, nombre):
    """Los miembros de un enum, en orden de declaracion."""
    m = re.search(r"enum\s+%s\s*\{(.*?)\n\s*\}" % nombre, texto, re.S)
    if not m:
        return []
    cuerpo = re.sub(r"//[^\n]*", "", m.group(1))
    cuerpo = re.sub(r"/\*.*?\*/", "", cuerpo, flags=re.S)
    cuerpo = re.sub(r"///[^\n]*", "", cuerpo)
    out = []
    for trozo in cuerpo.split(","):
        t = trozo.strip()
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", t):
            out.append(t)
    return out


def _flujo(raiz):
    s = _texto(os.path.join(raiz, "Assets", "Scripts", "Flujo", "EstadoApp.cs"))
    return {"estados": _enum(s, "Estado"), "eventos": _enum(s, "Evento")}


def _filas(raiz):
    """La fila de rotulos por estado, leida de OpcionesDeMenu.

    Se lee el `switch` del metodo `De`, que es donde estan las filas fijas. Las del selector
    las arma el catalogo en ejecucion y no se pueden leer de aqui: se declaran aparte en el
    generador, nombradas como lo que son.
    """
    s = _texto(os.path.join(raiz, "Assets", "Scripts", "Flujo", "OpcionesDeMenu.cs"))
    cuerpo = s[s.index("public static Opcion[] De("):]
    cuerpo = cuerpo[:cuerpo.index("/// La primera pantalla")]
    filas, actual = {}, []
    for linea in cuerpo.split("\n"):
        mc = re.search(r"case\s+EstadoApp\.Estado\.(\w+)\s*:", linea)
        if mc:
            actual.append(mc.group(1))
            continue
        mf = re.search(r"fila\[(\d+)\]\s*=\s*Da\(EstadoApp\.Evento\.(\w+),\s*\"([^\"]+)\"", linea)
        if mf:
            plaza, evento, etiqueta = int(mf.group(1)), mf.group(2), mf.group(3)
            for e in actual:
                filas.setdefault(e, {})[plaza] = [etiqueta, evento]
        elif "break;" in linea:
            actual = []
    plazas = re.search(r"const int Plazas\s*=\s*(\d+)", s)
    return {"filas": filas, "plazas": int(plazas.group(1)) if plazas else 5}


def _tutorial(raiz):
    """Los pasos del tutorial, en el orden en que el conductor los encadena."""
    carpeta = os.path.join(raiz, "Assets", "Scripts", "Tutorial")
    pasos = sorted(a[:-3] for a in os.listdir(carpeta)
                   if a.startswith("Paso") and a.endswith(".cs") and a != "PasoTutorial.cs")
    runner = _texto(os.path.join(carpeta, "TutorialRunner.cs"))
    orden = []
    for p in re.findall(r"\bPaso[A-Z]\w+", runner):
        if p in pasos and p not in orden:
            orden.append(p)
    for p in pasos:
        if p not in orden:
            orden.append(p)
    m = re.search(r"\{\s*((?:\"[^\"]+\"\s*,?\s*){2,})\}", runner)
    recorrido = re.findall(r'"([^"]+)"', m.group(1)) if m else []
    return {"pasos": orden, "recorrido": recorrido}


def _pruebas(raiz):
    """Cuantas pruebas EditMode hay: se cuentan los atributos, no se teclea el numero.

    SE CUENTAN LOS METODOS, y aparte los parametrizados. `[TestCaseSource]` no lleva `[Test]`
    y genera un caso por elemento de la fuente, asi que el corredor reporta MAS pruebas que
    metodos hay. Dar un solo numero obligaria a elegir entre uno que no cuadra con el codigo y
    otro que no cuadra con la consola; se dan los dos y se dice cual es cual.

    El README decia 210 desde el 21 de octubre. El trabajo de noviembre -los estados nuevos
    del flujo, el selector, Fundido, Lectura y DisposicionKit- lo dejo corto por 160.
    """
    archivos = 0
    base = os.path.join(raiz, "Assets", "Tests")
    if not os.path.isdir(base):
        return {"pruebas": 0, "parametrizadas": 0, "archivos": 0}
    metodos = parametrizadas = 0
    for rel, p in _cs(raiz):
        if "Tests" not in rel.split(os.sep):
            continue
        archivos += 1
        s = _texto(p)
        metodos += len(re.findall(r"\[\s*Test\s*\]", s))
        parametrizadas += len(re.findall(r"\[\s*TestCaseSource\s*\(", s))
    return {"pruebas": metodos, "parametrizadas": parametrizadas, "archivos": archivos}


def _ausentes(raiz):
    """Los paquetes del Asset Store que NO estan en el repo, leidos del README."""
    s = _texto(os.path.join(raiz, "README.md"))
    out = []
    for m in re.finditer(r"\*\*(.+?)\*\*,\s*paquete\s*`(\d+)`", s):
        out.append({"nombre": m.group(1).strip(), "id": m.group(2)})
    return out


def _constructores(raiz):
    """El orden obligatorio de los constructores de escena, leido del bloque del README."""
    s = _texto(os.path.join(raiz, "README.md"))
    m = re.search(r"```\n(Batería → .*?)```", s, re.S)
    if not m:
        return []
    out = []
    for linea in m.group(1).strip().split("\n"):
        partes = re.split(r"\s{2,}", linea.strip(), maxsplit=1)
        out.append([partes[0].strip(), partes[1].strip() if len(partes) > 1 else ""])
    return out


def extraer(raiz):
    d = {"repo": os.path.basename(raiz)}
    d.update(_ajustes(raiz))
    d["menu"] = _menu(raiz)
    d.update(_flujo(raiz))
    d.update(_filas(raiz))
    d["tutorial"] = _tutorial(raiz)
    d.update(_pruebas(raiz))
    d["ausentes"] = _ausentes(raiz)
    d["constructores"] = _constructores(raiz)
    return d


# ------------------------------------------------------------------ cache

def cargar():
    with open(CACHE, encoding="utf-8") as f:
        d = json.load(f)
    # LAS PLAZAS VUELVEN A SER NUMEROS. JSON solo admite texto como clave, asi que la plaza 0
    # se guarda como "0" y `fila.get(0)` no encuentra nada: los dos manuales salieron con la
    # tabla de rotulos entera en guiones, sin un solo error. Se normaliza aqui y no en cada
    # consumidor, que es donde se olvidaria uno.
    d["filas"] = {estado: {int(k): v for k, v in fila.items()}
                  for estado, fila in d.get("filas", {}).items()}
    return d


def refrescar():
    r = repo()
    if not r:
        raise SystemExit(
            "No encuentro el repo Unity.\n"
            "  Probé: %s\n"
            "  Pásame la ruta así:  BATERIAVR_REPO=/ruta/al/repo python3 manual_datos.py "
            "--refrescar" % (os.environ.get("BATERIAVR_REPO") or REPO_POR_OMISION))
    d = extraer(r)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return d


DATOS = cargar() if os.path.exists(CACHE) else None


if __name__ == "__main__":
    if "--refrescar" in sys.argv:
        d = refrescar()
        print("Cache reescrita:", CACHE)
    else:
        d = DATOS
        if d is None:
            raise SystemExit("No hay cache. Corre: python3 manual_datos.py --refrescar")
        print("Cache:", CACHE)
    print("  Unity %s · %s %s · paquete %s"
          % (d["unity"], d["producto"], d["version"], d["paquete"]))
    print("  comandos de menu: %d en %d grupos"
          % (sum(len(v) for v in d["menu"].values()), len(d["menu"])))
    print("  estados %d · eventos %d · plazas %d"
          % (len(d["estados"]), len(d["eventos"]), d["plazas"]))
    print("  filas declaradas para: %s" % ", ".join(sorted(d["filas"])))
    print("  tutorial: %s" % " → ".join(d["tutorial"]["pasos"]))
    print("  recorrido del kit: %s" % ", ".join(d["tutorial"]["recorrido"]))
    print("  pruebas EditMode: %d metodos en %d archivos (+%d parametrizadas por escena)"
          % (d["pruebas"], d["archivos"], d["parametrizadas"]))
    print("  paquetes ausentes: %s"
          % ", ".join("%s (%s)" % (a["nombre"], a["id"]) for a in d["ausentes"]))
    print("  constructores: %d" % len(d["constructores"]))
