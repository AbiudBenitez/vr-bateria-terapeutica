# Pistas de práctica y anillos — Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development
> (recomendado) o superpowers:executing-plans para ejecutar este plan tarea por tarea. Los pasos
> usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Goal:** Dar al juego un acompañamiento de percusión que marque el pulso y una guía visual que
permita acertar, para que el jugador deje de fallar por no saber cuándo golpear.

**Architecture:** Un generador en Python define cada patrón una sola vez y produce de ahí las
**dos** cosas —el WAV del acompañamiento y el JSON del beatmap—, de modo que no puedan
desincronizarse. Un script de editor importa ambos a Unity. En la escena, `ApproachRing` dibuja
sobre cada pad un anillo que se cierra hasta el radio exacto en el instante de la nota.

**Tech Stack:** Python 3 + numpy · Unity 6000.5.10f1 · C# · NUnit (EditMode)

**Spec:** `docs/superpowers/specs/2026-10-18-pistas-de-practica-design.md`

**Proyecto Unity:** `/Users/abiudbenitez/Documents/code/Unity/BateriaVR`

---

## Mapa de archivos

| Archivo | Responsabilidad |
|---|---|
| `scripts/patrones.py` | Los cuatro patrones como datos: qué pieza en qué beat |
| `scripts/gen_practica.py` | Sintetiza el WAV y escribe el JSON del beatmap |
| `scripts/test_patrones.py` | Pruebas del generador |
| `Assets/Editor/ImportarPractica.cs` | Crea los assets de Unity desde el JSON |
| `Assets/Scripts/Drum/RingMath.cs` | Pura: instante → radio del anillo |
| `Assets/Scripts/Drum/ApproachRing.cs` | MonoBehaviour que los dibuja |
| `Assets/Tests/EditMode/RingMathTests.cs` | Pruebas del radio |

**Por qué el generador vive en Python y no en Unity:** ya existe la cadena para esto —el
metrónomo se generó así y `latencia.py` lo verificó a 499.999 ms de intervalo—, y el audio
sintetizado se comprueba mejor fuera del motor.

**Por qué `RingMath` separado de `ApproachRing`:** el radio en función del tiempo es aritmética
pura y se prueba sin escena; dibujar es trabajo de MonoBehaviour.

**Convenciones del proyecto:**
- Comentarios en español explicando el **porqué**.
- Cero asignaciones en el camino del golpe; los conjuntos se reservan en `Awake`.
- Las clases puras no heredan de `MonoBehaviour`.
- Los componentes validan sus referencias en `Awake` con `LogError`.

---

### Task 1: Los patrones como datos

**Files:**
- Create: `scripts/patrones.py`

- [ ] **Step 1: Escribir el módulo**

Crear `scripts/patrones.py`:

```python
# -*- coding: utf-8 -*-
"""
Los patrones de práctica, como datos.

Cada patrón declara QUÉ pieza suena en QUÉ beat, y de aquí salen las dos cosas que tienen que
coincidir: el audio del acompañamiento y el beatmap de lo que el jugador toca.

Una sola fuente a propósito. El 18 de octubre el reloj corría a 80 BPM mientras el beatmap
declaraba 79.98, porque eran dos sitios donde escribir el mismo número; con una sola
definición esa clase de error deja de ser posible, no solo menos probable.

CONVENIO DE REPARTO
    acompanamiento  lo que SUENA en la pista: el hi-hat, que marca el pulso
    jugador         lo que el jugador debe GOLPEAR: bombo y caja

No se solapan. Si el acompañamiento tocara lo mismo que el jugador, este no distinguiría su
propio golpe del de la pista.
"""

# Posiciones dentro de un compás de 4/4, en beats desde su inicio.
CORCHEAS = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]

PATRONES = {
    "01_Pulso_80": dict(
        titulo="Pulso básico",
        bpm=80.0,
        pulsos_por_compas=4,
        compases=32,
        # Hi-hat solo en los pulsos: a 80 BPM son 1.33 golpes por segundo de referencia.
        acompanamiento={"HiHat": [0.0, 1.0, 2.0, 3.0]},
        # Lo mínimo que se puede tocar: una pieza cada dos pulsos, alternando manos.
        jugador={"Bombo": [0.0], "Tarola": [2.0]},
    ),
    "02_Rock_80": dict(
        titulo="Rock básico, lento",
        bpm=80.0,
        pulsos_por_compas=4,
        compases=32,
        acompanamiento={"HiHat": CORCHEAS},
        jugador={"Bombo": [0.0, 2.0, 2.5], "Tarola": [1.0, 3.0]},
    ),
    "03_Rock_100": dict(
        titulo="Rock básico, medio",
        bpm=100.0,
        pulsos_por_compas=4,
        compases=32,
        acompanamiento={"HiHat": CORCHEAS},
        jugador={"Bombo": [0.0, 2.0, 2.5], "Tarola": [1.0, 3.0]},
    ),
    "04_Rock_120": dict(
        titulo="Rock básico",
        bpm=120.0,
        pulsos_por_compas=4,
        compases=32,
        acompanamiento={"HiHat": CORCHEAS},
        jugador={"Bombo": [0.0, 2.0, 2.5], "Tarola": [1.0, 3.0]},
    ),
}


def eventos(patron, cual):
    """
    Todos los golpes de `cual` ("acompanamiento" o "jugador"), como (beat, pieza).

    El beat se calcula desde el NÚMERO DE COMPÁS, nunca sumando intervalos: acumular un
    intervalo cien veces introduce la deriva que esto viene a evitar.
    """
    fuera = []
    ppc = patron["pulsos_por_compas"]
    for c in range(patron["compases"]):
        base = c * ppc
        for pieza, posiciones in patron[cual].items():
            for p in posiciones:
                fuera.append((base + p, pieza))
    fuera.sort(key=lambda e: (e[0], e[1]))
    return fuera


def duracion_segundos(patron):
    return patron["compases"] * patron["pulsos_por_compas"] * 60.0 / patron["bpm"]


if __name__ == "__main__":
    for nombre, p in PATRONES.items():
        acc = eventos(p, "acompanamiento")
        jug = eventos(p, "jugador")
        dur = duracion_segundos(p)
        print(f"  {nombre:14s} {p['bpm']:5.1f} BPM · {dur:5.1f} s · "
              f"{len(acc):3d} de acompañamiento · {len(jug):3d} del jugador "
              f"({len(jug)/dur:.2f}/s)")
```

- [ ] **Step 2: Correr y comprobar las densidades**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python scripts/patrones.py
```

Expected:
```
  01_Pulso_80     80.0 BPM ·  96.0 s · 128 de acompañamiento ·  64 del jugador (0.67/s)
  02_Rock_80      80.0 BPM ·  96.0 s · 256 de acompañamiento · 160 del jugador (1.67/s)
  03_Rock_100    100.0 BPM ·  76.8 s · 256 de acompañamiento · 160 del jugador (2.08/s)
  04_Rock_120    120.0 BPM ·  64.0 s · 256 de acompañamiento · 160 del jugador (2.50/s)
```

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add scripts/patrones.py
git commit -m "feat(practica): los patrones de practica como datos

Cada patron declara que pieza suena en que beat, y de aqui salen las dos cosas que tienen que
coincidir: el audio del acompanamiento y el beatmap de lo que el jugador toca.

Una sola fuente a proposito. El reloj corria a 80 BPM mientras el beatmap declaraba 79.98
porque eran dos sitios donde escribir el mismo numero.

El acompanamiento toca el hi-hat y el jugador bombo y caja: no se solapan, porque si la pista
tocara lo mismo el jugador no distinguiria su propio golpe.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: Pruebas del generador de patrones

**Files:**
- Create: `scripts/test_patrones.py`

- [ ] **Step 1: Escribir las pruebas**

Crear `scripts/test_patrones.py`:

```python
# -*- coding: utf-8 -*-
"""Pruebas de los patrones de práctica."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patrones


def test_el_acompanamiento_y_el_jugador_no_se_solapan():
    """
    Si la pista tocara lo mismo que el jugador, este no distinguiría su golpe del de la pista
    y el juego dejaría de enseñar nada.
    """
    for nombre, p in patrones.PATRONES.items():
        piezas_acc = set(p["acompanamiento"])
        piezas_jug = set(p["jugador"])
        assert not (piezas_acc & piezas_jug), \
            f"{nombre}: la pieza {piezas_acc & piezas_jug} suena y se toca a la vez"


def test_los_beats_se_calculan_desde_el_compas():
    """
    A 120 BPM el compás 10 empieza exactamente en el beat 40. Si se acumulara el intervalo,
    el error se arrastraría.
    """
    p = patrones.PATRONES["04_Rock_120"]
    ev = patrones.eventos(p, "jugador")
    beats = sorted({b for b, _ in ev})
    assert 40.0 in beats, "el compás 10 no empieza en el beat 40"
    assert 124.0 in beats, "el compás 31 no empieza en el beat 124"


def test_el_rock_basico_tiene_la_forma_de_la_partitura():
    """Bombo en 1, caja en 2, bombo en 3 y su corchea, caja en 4."""
    p = patrones.PATRONES["04_Rock_120"]
    primer_compas = sorted((b, n) for b, n in patrones.eventos(p, "jugador") if b < 4.0)
    assert primer_compas == [
        (0.0, "Bombo"), (1.0, "Tarola"), (2.0, "Bombo"), (2.5, "Bombo"), (3.0, "Tarola")
    ], f"el patrón no coincide con la partitura: {primer_compas}"


def test_el_hihat_va_en_corcheas_en_los_patrones_de_rock():
    for nombre in ("02_Rock_80", "03_Rock_100", "04_Rock_120"):
        p = patrones.PATRONES[nombre]
        assert p["acompanamiento"]["HiHat"] == patrones.CORCHEAS, \
            f"{nombre}: el hi-hat no marca las ocho corcheas"


def test_la_progresion_sube_de_densidad():
    """Cada pista debe pedir más golpes por segundo que la anterior."""
    orden = ["01_Pulso_80", "02_Rock_80", "03_Rock_100", "04_Rock_120"]
    densidades = []
    for n in orden:
        p = patrones.PATRONES[n]
        densidades.append(len(patrones.eventos(p, "jugador")) / patrones.duracion_segundos(p))
    assert densidades == sorted(densidades), \
        f"la progresión no es creciente: {[f'{d:.2f}' for d in densidades]}"


def test_la_primera_pista_es_de_verdad_facil():
    """Menos de un golpe por segundo: es la que existe para poder empezar."""
    p = patrones.PATRONES["01_Pulso_80"]
    d = len(patrones.eventos(p, "jugador")) / patrones.duracion_segundos(p)
    assert d < 1.0, f"la pista de entrada pide {d:.2f} golpes por segundo"
```

- [ ] **Step 2: Correr**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python -m pytest scripts/test_patrones.py -v 2>&1 | tail -12
```

Expected: 6 pruebas pasadas.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add scripts/test_patrones.py
git commit -m "test(practica): los patrones no se solapan y la progresion sube

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: Sintetizar el audio y escribir el beatmap

**Files:**
- Create: `scripts/gen_practica.py`

- [ ] **Step 1: Escribir el generador**

Crear `scripts/gen_practica.py`:

```python
# -*- coding: utf-8 -*-
"""
Sintetiza el acompañamiento de cada patrón y escribe su beatmap.

El audio se construye con las muestras del PROPIO kit, de modo que no entra ninguna licencia
nueva y el timbre del acompañamiento es el mismo que suena al golpear.

Cada golpe se coloca desde su número de beat y nunca sumando intervalos: acumular un intervalo
cuatrocientas veces introduce la deriva que esto viene a evitar, y es el mismo criterio con el
que se generó el metrónomo, que midió 499.999 ms de intervalo medio.
"""
import json
import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patrones

SR = 48000          # tasa nativa del visor, la misma del kit
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITY = "/Users/abiudbenitez/Documents/code/Unity/BateriaVR"
KIT = os.path.join(UNITY, "Assets", "Audio", "Kit")
SALIDA = os.path.join(UNITY, "Assets", "Audio", "Practica")

# Una muestra fija por pieza, no sorteada: la pista debe sonar igual cada vez que se genere,
# para que una medición de hoy valga para el archivo de mañana.
MUESTRAS = {"HiHat": "Hat5-1.wav", "Bombo": "Kick8-1.wav", "Tarola": "Snare7-1.wav"}


def leer_muestra(pieza):
    ruta = os.path.join(KIT, pieza, MUESTRAS[pieza])
    with wave.open(ruta, "rb") as w:
        sr, n, ancho, canales = (w.getframerate(), w.getnframes(),
                                 w.getsampwidth(), w.getnchannels())
        crudo = w.readframes(n)
    x = np.frombuffer(crudo, dtype={1: np.int8, 2: "<i2", 4: "<i4"}[ancho]).astype(np.float64)
    if canales > 1:
        x = x.reshape(-1, canales).mean(axis=1)
    if sr != SR:
        raise SystemExit(f"{ruta} está a {sr} Hz y se esperaba {SR}")
    pico = np.max(np.abs(x))
    return x / pico if pico else x


def sintetizar(patron):
    """Mezcla el acompañamiento sobre silencio y devuelve la señal."""
    dur = patrones.duracion_segundos(patron)
    spb = 60.0 / patron["bpm"]
    cola = 1.0                                   # margen para que el último golpe no se corte
    senal = np.zeros(int((dur + cola) * SR))

    muestras = {p: leer_muestra(p) for p in patron["acompanamiento"]}
    for beat, pieza in patrones.eventos(patron, "acompanamiento"):
        # Desde el beat, NO acumulando.
        i = int(round(beat * spb * SR))
        m = muestras[pieza]
        fin = min(i + len(m), len(senal))
        senal[i:fin] += m[:fin - i] * 0.7        # deja sitio a lo que toca el jugador
    return senal


def escribir_wav(ruta, senal):
    pico = np.max(np.abs(senal))
    datos = (np.clip(senal / pico * 0.9, -1, 1) * 32767).astype("<i2") if pico else \
            np.zeros(len(senal), dtype="<i2")
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(datos.tobytes())


def beatmap_de(nombre, patron):
    return dict(
        nombre=nombre,
        titulo=patron["titulo"],
        bpm=patron["bpm"],
        pulsosPorCompas=patron["pulsos_por_compas"],
        pista=f"{nombre}.wav",
        notas=[dict(beat=b, pieza=p) for b, p in patrones.eventos(patron, "jugador")],
    )


def main():
    os.makedirs(SALIDA, exist_ok=True)
    indice = []
    for nombre, patron in patrones.PATRONES.items():
        senal = sintetizar(patron)
        escribir_wav(os.path.join(SALIDA, f"{nombre}.wav"), senal)

        bm = beatmap_de(nombre, patron)
        with open(os.path.join(SALIDA, f"{nombre}.json"), "w", encoding="utf-8") as fh:
            json.dump(bm, fh, indent=2, ensure_ascii=False)

        indice.append(nombre)
        print(f"  {nombre:14s} {patron['bpm']:5.1f} BPM · "
              f"{len(senal)/SR:5.1f} s · {len(bm['notas']):3d} notas")

    with open(os.path.join(SALIDA, "indice.json"), "w", encoding="utf-8") as fh:
        json.dump(indice, fh, indent=2)
    print(f"\n  -> {SALIDA}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Generar**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python scripts/gen_practica.py
```

Expected: cuatro líneas con sus BPM, duraciones y número de notas, y la ruta de salida.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add scripts/gen_practica.py
git commit -m "feat(practica): sintetizar el acompanamiento desde el kit

El audio se construye con las muestras del propio kit: ninguna licencia nueva y el mismo
timbre que suena al golpear.

Cada golpe se coloca desde su numero de beat, nunca sumando intervalos. Es el criterio con el
que se genero el metronomo, que midio 499.999 ms de intervalo medio.

La muestra por pieza es fija y no sorteada: la pista debe sonar igual cada vez que se genere,
para que una medicion de hoy valga para el archivo de manana.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: Verificar que el audio cae donde el beatmap dice

Es la prueba que cierra el círculo: comprueba sobre el archivo real que el acompañamiento y la
definición coinciden.

**Files:**
- Create: `scripts/verificar_practica.py`

- [ ] **Step 1: Escribir el verificador**

Crear `scripts/verificar_practica.py`:

```python
# -*- coding: utf-8 -*-
"""
Comprueba que los ataques del WAV caen donde el beatmap dice.

El generador y el beatmap salen de la misma definición, así que en teoría no pueden
discrepar. Esto lo comprueba sobre el ARCHIVO, que es lo que de verdad va al visor: un error
de redondeo al escribir las muestras, o una muestra que empiece con silencio, aparecerían
aquí y no en las pruebas del generador.
"""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import latencia
import patrones

UNITY = "/Users/abiudbenitez/Documents/code/Unity/BateriaVR"
SALIDA = os.path.join(UNITY, "Assets", "Audio", "Practica")
TOLERANCIA_MS = 5.0


def verificar(nombre):
    with open(os.path.join(SALIDA, f"{nombre}.json"), encoding="utf-8") as fh:
        bm = json.load(fh)
    sr, x = latencia.load_wav(os.path.join(SALIDA, f"{nombre}.wav"))
    detectados = latencia.onset_times(x, sr)

    patron = patrones.PATRONES[nombre]
    spb = 60.0 / bm["bpm"]
    esperados = np.array([b * spb for b, _ in patrones.eventos(patron, "acompanamiento")])
    esperados = np.unique(np.round(esperados, 6))

    # Para cada golpe esperado, el ataque detectado más cercano
    errores = []
    for e in esperados:
        if len(detectados) == 0:
            break
        errores.append((detectados[np.argmin(np.abs(detectados - e))] - e) * 1000.0)
    errores = np.array(errores)

    return dict(
        nombre=nombre,
        esperados=len(esperados),
        detectados=len(detectados),
        error_max=float(np.max(np.abs(errores))) if len(errores) else float("inf"),
        error_medio=float(np.mean(np.abs(errores))) if len(errores) else float("inf"),
    )


def main():
    nombres = sorted(os.path.basename(p)[:-5]
                     for p in glob.glob(os.path.join(SALIDA, "*.json"))
                     if not p.endswith("indice.json"))
    if not nombres:
        raise SystemExit("No hay pistas generadas. Corre antes gen_practica.py")

    print(f"  {'pista':16s}{'esperados':>11s}{'detectados':>12s}"
          f"{'error medio':>13s}{'error máx':>11s}")
    fallos = 0
    for n in nombres:
        r = verificar(n)
        ok = r["error_max"] <= TOLERANCIA_MS
        fallos += 0 if ok else 1
        print(f"  {n:16s}{r['esperados']:>11d}{r['detectados']:>12d}"
              f"{r['error_medio']:>12.2f} ms{r['error_max']:>9.2f} ms"
              f"  {'OK' if ok else 'FALLA'}")

    if fallos:
        raise SystemExit(f"\n  {fallos} pistas fuera de la tolerancia de {TOLERANCIA_MS} ms")
    print(f"\n  Las {len(nombres)} pistas dentro de {TOLERANCIA_MS} ms")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verificar**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python scripts/verificar_practica.py
```

Expected: las cuatro pistas con error máximo por debajo de 5 ms.

**Si alguna falla:** el número de ataques detectados dirá por dónde. Menos detectados que
esperados significa que dos golpes muy juntos se fundieron —a 120 BPM las corcheas están a
250 ms, de sobra para el detector—; más detectados, que la cola de una muestra se está
contando como ataque.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add scripts/verificar_practica.py
git commit -m "test(practica): verificar que el audio cae donde el beatmap dice

El generador y el beatmap salen de la misma definicion, asi que en teoria no pueden discrepar.
Esto lo comprueba sobre el ARCHIVO, que es lo que va al visor: un error de redondeo al escribir
las muestras, o una muestra que empiece con silencio, apareceria aqui y no en las pruebas del
generador.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 5: Importar las pistas a Unity

**Files:**
- Create: `Assets/Editor/ImportarPractica.cs`

- [ ] **Step 1: Escribir el importador**

Crear `Assets/Editor/ImportarPractica.cs`:

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

/// Crea los assets de Beatmap desde los JSON que escribe gen_practica.py.
///
/// El JSON y el WAV salen de la misma definición en Python, así que no pueden discrepar. Este
/// importador solo traduce: no decide nada sobre tempos ni posiciones.
public static class ImportarPractica
{
    const string Carpeta = "Assets/Audio/Practica";

    [Serializable] class NotaJson { public double beat; public string pieza; }

    [Serializable]
    class BeatmapJson
    {
        public string nombre;
        public string titulo;
        public double bpm;
        public int pulsosPorCompas;
        public string pista;
        public NotaJson[] notas;
    }

    [MenuItem("Batería/Importar pistas de práctica")]
    public static void Importar()
    {
        if (!Directory.Exists(Carpeta))
        {
            EditorUtility.DisplayDialog("Batería",
                $"No existe {Carpeta}.\n\nCorre antes:\n" +
                "  python scripts/gen_practica.py", "Vale");
            return;
        }

        var piezas = AssetDatabase.FindAssets("t:DrumKitPiece")
            .Select(AssetDatabase.GUIDToAssetPath)
            .Select(AssetDatabase.LoadAssetAtPath<DrumKitPiece>)
            .Where(p => p != null)
            .GroupBy(p => p.nombrePieza)
            .ToDictionary(g => g.Key, g => g.First());

        var hechas = new List<string>();
        var avisos = new List<string>();

        foreach (string json in Directory.GetFiles(Carpeta, "*.json"))
        {
            if (Path.GetFileName(json) == "indice.json") continue;

            var d = JsonUtility.FromJson<BeatmapJson>(File.ReadAllText(json));
            if (d == null || d.notas == null) { avisos.Add($"{json}: ilegible"); continue; }

            string rutaPista = $"{Carpeta}/{d.pista}";
            var clip = AssetDatabase.LoadAssetAtPath<AudioClip>(rutaPista);
            if (clip == null) { avisos.Add($"{d.nombre}: falta {d.pista}"); continue; }

            var notas = new List<Beatmap.Nota>();
            bool faltaPieza = false;
            foreach (var n in d.notas)
            {
                if (!piezas.TryGetValue(n.pieza, out var p))
                {
                    if (!faltaPieza) avisos.Add($"{d.nombre}: no existe la pieza '{n.pieza}'");
                    faltaPieza = true;
                    continue;
                }
                notas.Add(new Beatmap.Nota { beat = n.beat, pieza = p });
            }

            string rutaAsset = $"{Carpeta}/{d.nombre}.asset";
            var bm = AssetDatabase.LoadAssetAtPath<Beatmap>(rutaAsset);
            bool nuevo = bm == null;
            if (nuevo) bm = ScriptableObject.CreateInstance<Beatmap>();

            bm.pista = clip;
            bm.bpm = d.bpm;
            bm.pulsosPorCompas = d.pulsosPorCompas;
            bm.notas = notas.ToArray();

            if (nuevo) AssetDatabase.CreateAsset(bm, rutaAsset);
            EditorUtility.SetDirty(bm);
            hechas.Add($"{d.nombre}  {d.bpm} BPM  {notas.Count} notas");
        }

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();

        string msg = hechas.Count > 0
            ? "Beatmaps importados:\n\n  " + string.Join("\n  ", hechas)
            : "No se importó ninguno.";
        if (avisos.Count > 0) msg += "\n\nAvisos:\n  " + string.Join("\n  ", avisos);

        Debug.Log("[ImportarPractica] " + msg.Replace("\n", " "));
        EditorUtility.DisplayDialog("Batería", msg, "Vale");
    }
}
```

- [ ] **Step 2: Verificar que compila**

Con Unity cerrado:

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/pr1.xml -logFile /tmp/pr1.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/pr1.log',errors='ignore').read()
e=re.findall(r'error CS\d+[^\n]*',L)
print('errores:',len(e),' avisos:',len({m for m in re.findall(r'warning CS\d+',L)}))
for l in e[:4]: print('  ',l[:130])
r=ET.parse('/tmp/pr1.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')}\")"
```

Expected: 0 errores, 96 de 96 pasadas.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Editor/ImportarPractica.cs Assets/Editor/ImportarPractica.cs.meta
git commit -m "feat(practica): importador de las pistas generadas

El JSON y el WAV salen de la misma definicion en Python, asi que no pueden discrepar. Este
importador solo traduce: no decide nada sobre tempos ni posiciones.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 6: `RingMath` — el radio del anillo

**Files:**
- Create: `Assets/Scripts/Drum/RingMath.cs`
- Create: `Assets/Tests/EditMode/RingMathTests.cs`

- [ ] **Step 1: Escribir las pruebas que fallan**

Crear `Assets/Tests/EditMode/RingMathTests.cs`:

```csharp
using NUnit.Framework;

/// El radio del anillo en función del tiempo. Aritmética pura: no sabe de escena ni de audio.
public class RingMathTests
{
    const float Tol = 1e-5f;

    [Test]
    public void AlAparecerElAnilloEstaEnElRadioInicial()
    {
        // Falta una anticipación completa: el anillo acaba de nacer.
        float r = RingMath.Radio(restanteSeg: 1.5f, anticipacionSeg: 1.5f,
                                 radioPad: 0.15f, factorInicial: 3f);
        Assert.AreEqual(0.45f, r, Tol);
    }

    [Test]
    public void EnElInstanteDeLaNotaElRadioEsElDelPad()
    {
        // ES el criterio del diseño: los bordes coinciden justo al golpear.
        float r = RingMath.Radio(0f, 1.5f, 0.15f, 3f);
        Assert.AreEqual(0.15f, r, Tol);
    }

    [Test]
    public void AMitadDeCaminoElRadioEstaAMitad()
    {
        // Lineal en el tiempo: el ojo lee la velocidad de cierre mejor que la posición.
        float r = RingMath.Radio(0.75f, 1.5f, 0.15f, 3f);
        Assert.AreEqual(0.30f, r, Tol);
    }

    [Test]
    public void PasadaLaNotaElRadioNoSigueBajando()
    {
        // Sin esto el anillo se cerraría hasta desaparecer y parecería otra cosa.
        Assert.AreEqual(0.15f, RingMath.Radio(-0.2f, 1.5f, 0.15f, 3f), Tol);
        Assert.AreEqual(0.15f, RingMath.Radio(-5f, 1.5f, 0.15f, 3f), Tol);
    }

    [Test]
    public void AntesDeAparecerNoPasaDelRadioInicial()
    {
        Assert.AreEqual(0.45f, RingMath.Radio(9f, 1.5f, 0.15f, 3f), Tol);
    }

    [Test]
    public void UnaAnticipacionInvalidaNoDivideEntreCero()
    {
        float r = RingMath.Radio(1f, 0f, 0.15f, 3f);
        Assert.AreEqual(0.15f, r, Tol, "con anticipación cero el anillo ya debería estar cerrado");
    }

    [Test]
    public void VisibleSoloDentroDeLaVentana()
    {
        Assert.IsTrue(RingMath.Visible(1.0f, 1.5f, margenSalidaSeg: 0.2f));
        Assert.IsTrue(RingMath.Visible(0f, 1.5f, 0.2f));
        Assert.IsTrue(RingMath.Visible(-0.1f, 1.5f, 0.2f));
        Assert.IsFalse(RingMath.Visible(-0.3f, 1.5f, 0.2f), "pasado el margen debe apagarse");
        Assert.IsFalse(RingMath.Visible(2.0f, 1.5f, 0.2f), "aún no le toca aparecer");
    }
}
```

- [ ] **Step 2: Correr para verificar que fallan**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/pr2.xml -logFile /tmp/pr2.log 2>&1
grep -c "error CS" /tmp/pr2.log
```

Expected: error de compilación, `The name 'RingMath' does not exist in the current context`.

- [ ] **Step 3: Implementar**

Crear `Assets/Scripts/Drum/RingMath.cs`:

```csharp
using UnityEngine;

/// Radio de un anillo de aproximación en función de lo que falta para su nota.
///
/// El anillo empieza grande y se cierra hasta el radio EXACTO del pad en el instante del
/// golpe. La coincidencia de dos bordes es un instante inequívoco; juzgar cuándo un objeto que
/// cae llega a un plano exige percepción de profundidad, que en realidad virtual es justo lo
/// peor calibrado.
///
/// El radio es LINEAL en el tiempo, como en osu!: el ojo lee la velocidad de cierre mucho
/// mejor que la posición absoluta.
public static class RingMath
{
    /// `restanteSeg` es lo que falta para la nota; negativo si ya pasó.
    public static float Radio(float restanteSeg, float anticipacionSeg,
                              float radioPad, float factorInicial)
    {
        // Anticipación nula o negativa: no hay recorrido que interpolar, el anillo está
        // cerrado. Sin esta guarda la división de abajo reventaría.
        if (anticipacionSeg <= 0f) return radioPad;

        float t = Mathf.Clamp01(restanteSeg / anticipacionSeg);
        float radioInicial = radioPad * Mathf.Max(1f, factorInicial);
        return Mathf.Lerp(radioPad, radioInicial, t);
    }

    /// Si el anillo debe dibujarse. Se apaga un poco DESPUÉS de la nota para que el jugador
    /// alcance a ver dónde estaba cuando llega tarde.
    public static bool Visible(float restanteSeg, float anticipacionSeg, float margenSalidaSeg)
    {
        return restanteSeg <= anticipacionSeg && restanteSeg >= -margenSalidaSeg;
    }
}
```

- [ ] **Step 4: Correr para verificar que pasan**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/pr3.xml -logFile /tmp/pr3.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/pr3.log',errors='ignore').read()
print('errores:',len(re.findall(r'error CS\d+',L)))
r=ET.parse('/tmp/pr3.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')} fallidas {r.get('failed')}\")
for tc in r.iter('test-case'):
    if tc.get('result')!='Passed': print('FALLA',tc.get('name'))"
```

Expected: 0 errores, **103 de 103** pasadas (96 previas + 7 nuevas).

- [ ] **Step 5: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/RingMath.cs Assets/Scripts/Drum/RingMath.cs.meta \
        Assets/Tests/EditMode/RingMathTests.cs Assets/Tests/EditMode/RingMathTests.cs.meta
git commit -m "feat(ritmo): radio del anillo de aproximacion

El anillo empieza grande y se cierra hasta el radio EXACTO del pad en el instante del golpe. La
coincidencia de dos bordes es un instante inequivoco; juzgar cuando un objeto que cae llega a
un plano exige percepcion de profundidad, que en VR es justo lo peor calibrado.

El radio es lineal en el tiempo, como en osu!: el ojo lee la velocidad de cierre mejor que la
posicion absoluta.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 7: `ApproachRing` — dibujarlos

**Files:**
- Create: `Assets/Scripts/Drum/ApproachRing.cs`
- Modify: `Assets/Scripts/Drum/NoteSpawner.cs`

- [ ] **Step 1: Exponer el pad de cada nota**

En `Assets/Scripts/Drum/NoteSpawner.cs`, justo después del método `PosicionDe`, añadir:

```csharp
    /// El pad de la nota pendiente `i`, o null si su pieza no está en la escena.
    ///
    /// Lo necesitan los anillos: además de dónde está el pad, hace falta su RADIO, que es
    /// donde el anillo tiene que cerrar.
    public DrumPad PadDe(int i)
    {
        if (destino == null || i < 0 || i >= destino.Length || destino[i] == null) return null;
        return destino[i].GetComponent<DrumPad>();
    }
```

- [ ] **Step 2: Implementar el componente**

Crear `Assets/Scripts/Drum/ApproachRing.cs`:

```csharp
using UnityEngine;

/// Dibuja sobre cada pad un anillo que se cierra hasta su radio en el instante de la nota.
///
/// Sustituye a la esfera que cae como guía principal. En realidad virtual, juzgar cuándo un
/// objeto que cae alcanza un plano exige percepción de profundidad —lo peor calibrado de la
/// percepción en VR—; un anillo que se cierra sobre el pad es información bidimensional sobre
/// una superficie que el jugador ya está mirando.
public sealed class ApproachRing : MonoBehaviour
{
    [SerializeField] NoteSpawner spawner;

    [SerializeField, Tooltip("Cuántas veces el radio del pad mide el anillo al aparecer.")]
    float factorInicial = 3f;

    [SerializeField, Tooltip("Segundos que el anillo sigue visible tras pasar su nota, para " +
                             "que el jugador vea dónde estaba cuando llega tarde.")]
    float margenSalida = 0.2f;

    [SerializeField, Tooltip("Grosor del trazo, en metros.")]
    float grosor = 0.008f;

    [SerializeField, Tooltip("Altura sobre la superficie del pad. Lo justo para no pelearse " +
                             "con la piel por el mismo plano.")]
    float alturaSobrePad = 0.003f;

    [SerializeField, Min(4), Tooltip("Anillos visibles a la vez. Se reservan en Awake: " +
                                     "instanciar en el camino del golpe cuesta frames.")]
    int capacidad = 24;

    [SerializeField, Min(8), Tooltip("Segmentos de cada anillo. 48 ya se ve redondo.")]
    int segmentos = 48;

    [SerializeField] Color color = new Color(0.65f, 0.85f, 1f, 0.9f);

    LineRenderer[] anillos;
    Vector3[] buffer;

    void Awake()
    {
        if (spawner == null)
            Debug.LogError($"[ApproachRing] '{name}' no tiene NoteSpawner: no hay notas de " +
                           "las que dibujar anillos.", this);

        buffer = new Vector3[segmentos + 1];
        anillos = new LineRenderer[capacidad];

        var mat = new Material(Shader.Find("Sprites/Default"));
        for (int i = 0; i < capacidad; i++)
        {
            var go = new GameObject($"Anillo{i:00}");
            go.transform.SetParent(transform, false);
            var lr = go.AddComponent<LineRenderer>();
            lr.useWorldSpace = true;
            lr.loop = true;
            lr.positionCount = segmentos;
            lr.widthMultiplier = grosor;
            lr.material = mat;
            lr.startColor = lr.endColor = color;
            lr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
            lr.receiveShadows = false;
            go.SetActive(false);
            anillos[i] = lr;
        }
    }

    void Update()
    {
        if (spawner == null) return;
        var pend = spawner.Pendientes;
        if (pend == null) return;

        // dspTime se lee UNA vez por frame, como en todo el proyecto.
        double ahora = AudioSettings.dspTime;
        float anticipacion = spawner.AnticipacionSegundos;

        int usados = 0;
        for (int i = 0; i < pend.Length && usados < anillos.Length; i++)
        {
            if (pend[i].juzgada) continue;

            float restante = (float)(pend[i].tiempo - ahora);
            if (!RingMath.Visible(restante, anticipacion, margenSalida)) continue;

            var pad = spawner.PadDe(i);
            if (pad == null) continue;

            float r = RingMath.Radio(restante, anticipacion, pad.Radius, factorInicial);
            Dibujar(anillos[usados], pad, r);
            usados++;
        }

        // Apagar los que sobran. No se destruyen: se reutilizan al frame siguiente.
        for (int i = usados; i < anillos.Length; i++)
            if (anillos[i].gameObject.activeSelf) anillos[i].gameObject.SetActive(false);
    }

    void Dibujar(LineRenderer lr, DrumPad pad, float radio)
    {
        Vector3 centro = pad.Center + pad.Normal * alturaSobrePad;
        Vector3 u = Vector3.Cross(pad.Normal, Vector3.forward);
        if (u.sqrMagnitude < 1e-6f) u = Vector3.Cross(pad.Normal, Vector3.right);
        u.Normalize();
        Vector3 v = Vector3.Cross(pad.Normal, u);

        for (int s = 0; s < segmentos; s++)
        {
            float a = s * 2f * Mathf.PI / segmentos;
            buffer[s] = centro + (u * Mathf.Cos(a) + v * Mathf.Sin(a)) * radio;
        }
        lr.SetPositions(buffer);     // el buffer sobra en 1; SetPositions usa positionCount

        if (!lr.gameObject.activeSelf) lr.gameObject.SetActive(true);
    }
}
```

- [ ] **Step 3: Verificar que compila**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/pr4.xml -logFile /tmp/pr4.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/pr4.log',errors='ignore').read()
e=re.findall(r'error CS\d+[^\n]*',L)
print('errores:',len(e),' avisos:',len({m for m in re.findall(r'warning CS\d+',L)}))
for l in e[:4]: print('  ',l[:130])
r=ET.parse('/tmp/pr4.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')}\")"
```

Expected: 0 errores, 0 avisos, 103 de 103 pasadas.

- [ ] **Step 4: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/ApproachRing.cs Assets/Scripts/Drum/ApproachRing.cs.meta \
        Assets/Scripts/Drum/NoteSpawner.cs
git commit -m "feat(ritmo): anillos de aproximacion sobre los pads

Sustituyen a la esfera que cae como guia principal. En VR, juzgar cuando un objeto que cae
alcanza un plano exige percepcion de profundidad -lo peor calibrado de la percepcion en VR-;
un anillo que se cierra sobre el pad es informacion bidimensional sobre una superficie que el
jugador ya esta mirando.

Los LineRenderer se reservan en Awake y se reutilizan apagandolos, nunca destruyendolos.

NoteSpawner expone PadDe para que el anillo conozca el RADIO del pad, que es donde tiene que
cerrar.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 8: Apagar las notas que caen y cablear

**Files:**
- Modify: `Assets/Scripts/Drum/NoteSpawner.cs`
- Modify: `Assets/Editor/CablearJuegoDeRitmo.cs`

- [ ] **Step 1: Añadir la casilla de las esferas**

En `Assets/Scripts/Drum/NoteSpawner.cs`, dentro del bloque `[Header("Aspecto")]`, antes del
campo `prefabNota`, añadir:

```csharp
    [SerializeField, Tooltip("Dibujar las notas que caen además de los anillos. Apagadas por " +
                             "defecto: el anillo ya aparece con la misma anticipación y ya " +
                             "dice de qué pieza se trata, así que la esfera añade ruido " +
                             "visual sin añadir información.")]
    bool mostrarNotasQueCaen = false;
```

Y en `Update`, sustituir el bucle que mueve las notas. Buscar:

```csharp
        // Mover las que están en vuelo.
        for (int i = 0; i < vuelo.Length; i++)
        {
```

y sustituir por:

```csharp
        // Mover las que están en vuelo.
        for (int i = 0; i < vuelo.Length; i++)
        {
            if (!mostrarNotasQueCaen && vuelo[i].activa) { Apagar(i); continue; }
```

- [ ] **Step 2: Cablear el anillo**

En `Assets/Editor/CablearJuegoDeRitmo.cs`, justo después del bloque que cablea el `JudgePopup`
—la línea `soMarc.FindProperty("globos").objectReferenceValue = popup;`— añadir antes de
`soMarc.ApplyModifiedPropertiesWithoutUndo();`:

```csharp
        // El anillo de aproximación: la guía principal para acertar el instante.
        var anillo = Buscar<ApproachRing>();
        if (anillo == null)
        {
            anillo = spawner.gameObject.AddComponent<ApproachRing>();
            hechos.Add("ApproachRing añadido al spawner");
        }
        var soAnillo = new SerializedObject(anillo);
        soAnillo.FindProperty("spawner").objectReferenceValue = spawner;
        soAnillo.ApplyModifiedPropertiesWithoutUndo();
        hechos.Add("anillos: spawner");
```

- [ ] **Step 3: Verificar que compila**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/pr5.xml -logFile /tmp/pr5.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/pr5.log',errors='ignore').read()
e=re.findall(r'error CS\d+[^\n]*',L)
print('errores:',len(e))
for l in e[:4]: print('  ',l[:130])
r=ET.parse('/tmp/pr5.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')}\")"
```

Expected: 0 errores, 103 de 103 pasadas.

- [ ] **Step 4: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/NoteSpawner.cs Assets/Editor/CablearJuegoDeRitmo.cs
git commit -m "feat(ritmo): las notas que caen pasan a secundarias

El anillo aparece con la misma anticipacion y ya dice de que pieza se trata, asi que la esfera
cayendo anade ruido visual sin anadir informacion. Queda con casilla por si en el visor resulta
util para anticipar desde lejos: esa decision se toma mirando, no antes.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 9: Probar en el visor

Esta tarea la ejecuta Misael.

- [ ] **Step 1: Generar e importar**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python scripts/gen_practica.py
~/.pyenv/versions/redes/bin/python scripts/verificar_practica.py
```

Luego en Unity: `Batería → Importar pistas de práctica`.

- [ ] **Step 2: Montar y jugar**

1. Abrir `Assets/Scenes/Cap04_Pad.unity`.
2. En el `NoteSpawner`, poner **Beatmap: `02_Rock_80`**.
3. `Batería → Cablear juego de ritmo` — toma el tempo y la pista del beatmap, y añade el anillo.
4. Play.

**Criterios de aceptación:**

1. Se oye el hi-hat marcando cada corchea.
2. Sobre cada pad aparece un anillo que se cierra.
3. El anillo coincide con el borde del pad **justo cuando hay que golpear**.
4. Golpear en ese instante da `PERFECT`.
5. La precisión sube respecto de lo que daba con *Maccary Bay*.

- [ ] **Step 3: Probar en el visor**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
# Batería → Compilar APK, y luego:
./scripts/quest.sh install
# jugar y CERRAR la app desde el menú del visor
./scripts/quest.sh pull
python3 -m json.tool "$(ls -t mediciones/files/sesion_*.json | head -1)" | head -25
```

**Lo que debería cambiar frente a las sesiones de Maccary Bay:** la precisión sube y el
desfase medio se acerca a cero, porque ahora hay un pulso audible contra el que sincronizarse.

- [ ] **Step 4: Decidir sobre las esferas**

Con los anillos funcionando, decidir si las notas que caen aportan. Si sí, marcar
`mostrarNotasQueCaen` en el `NoteSpawner`. Si no, se quedan apagadas.

- [ ] **Step 5: Commit de la escena y la evidencia**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scenes/Cap04_Pad.unity Assets/Audio/Practica/
git commit -m "feat(practica): escena con las pistas de practica y los anillos

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"

cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
cp /Users/abiudbenitez/Documents/code/Unity/BateriaVR/mediciones/files/sesion_*.json \
   entregables/mediciones/
git add entregables/mediciones/
git commit -m "docs: sesiones sobre las pistas de practica

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Resumen de verificación

| Qué | Cómo | Quién |
|---|---|---|
| Los patrones no se solapan y la progresión sube | 6 pruebas en Python | Agente |
| El audio cae donde el beatmap dice | `verificar_practica.py`, tolerancia 5 ms | Agente |
| El radio del anillo, 7 pruebas | EditMode sin escena | Agente |
| Compilación limpia | 103 de 103, cero errores y cero avisos | Agente |
| El anillo cierra donde debe | Play en el editor | Misael |
| La precisión mejora | Sesión en el visor, comparando JSON | Misael |

## Qué NO cubre este plan

**Menú de selección de pista.** La interfaz se recortó al flujo mínimo; la pista se elige en el
inspector.

**Patrones con platillos, toms o redobles.** Cuatro pistas con bombo, caja y hi-hat bastan para
demostrar el mecanismo y son lo que el patrón de referencia pide.

**Retirar *Maccary Bay*.** Queda como la pista medida que cierra `MP.1` a `MP.3`, documentada
con su licencia y su tempo verificado.
