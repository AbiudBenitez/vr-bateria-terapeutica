# Guía de la batería VR — Etapa A · Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development
> (recomendado) o superpowers:executing-plans para ejecutar este plan tarea por tarea. Los pasos
> usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Goal:** Producir la guía de construcción del sistema de percusión VR —etapa A completa, etapa B
esbozada— junto con el código C# real y la herramienta de medición de latencia que la guía usa.

**Architecture:** Tres productos que se construyen en paralelo y se refuerzan entre sí:
(1) `scripts/latencia.py`, herramienta de análisis de WAV que convierte una grabación en un número
de latencia con mediana y p90 — es lo único verificable por completo sin hardware, y se construye
con TDD estricto; (2) los scripts C# como **archivos reales** bajo `proyecto-unity/`, con pruebas
EditMode de Unity para la parte matemática pura; (3) los ocho capítulos de la guía, que referencian
esos archivos en lugar de duplicar el código. El capítulo 1 se escribe primero para desbloquear la
instalación de Unity, que tarda horas.

**Tech Stack:** Unity 6 (6000.x LTS) · OpenXR 1.13+ · XR Interaction Toolkit 3.x · C# ·
Meta XR Simulator · Quest 3S · Python 3.11 (pyenv `redes`) con numpy + scipy + pytest · Audacity

**Spec:** `docs/superpowers/specs/2026-09-12-guia-bateria-vr-unity-design.md`

---

## Mapa de archivos

| Archivo | Responsabilidad |
|---|---|
| `scripts/latencia.py` | Detección de transitorios en WAV, clasificación clic/tambor, cálculo de Δ, estadística |
| `scripts/test_latencia.py` | Pruebas de `latencia.py` con WAV sintéticos de offset conocido |
| `proyecto-unity/Assets/Scripts/Drum/DrumPad.cs` | Geometría del pad: plano armado, distancia con signo, prueba de radio |
| `proyecto-unity/Assets/Scripts/Drum/DrumHit.cs` | Struct del golpe. Contrato entre detección y consumidores |
| `proyecto-unity/Assets/Scripts/Drum/DrumHitSink.cs` | Clase abstracta del receptor + `DrumHitFanout` |
| `proyecto-unity/Assets/Scripts/Drum/StickTracker.cs` | Lectura de pose, velocidad de punta, detección de cruce, predicción |
| `proyecto-unity/Assets/Scripts/Drum/DrumVoice.cs` | Pool de AudioSource, `PlayScheduled`, mapeo velocity→ganancia |
| `proyecto-unity/Assets/Scripts/Drum/HapticSink.cs` | Háptico diferido hasta `ImpactDsp` |
| `proyecto-unity/Assets/Scripts/Drum/LatencyProbe.cs` | Registro por golpe, conteo de agendas tardías, volcado a JSON |
| `proyecto-unity/Assets/Scripts/Drum/PadCalibrator.cs` | Fija el plano del pad sobre la superficie física con el botón A |
| `proyecto-unity/Assets/Scripts/Drum/Drum.asmdef` | Ensamblado propio, para que las pruebas EditMode puedan referenciarlo |
| `proyecto-unity/Assets/Tests/EditMode/*.cs` | Pruebas de la matemática pura, sin visor |
| `entregables/guia/Guia_Bateria_VR_A.md` | La guía, ocho capítulos |

**Por qué `Drum.asmdef`:** sin un ensamblado propio, las pruebas EditMode no pueden referenciar los
scripts y Unity recompila todo el proyecto en cada cambio. Con él, las pruebas corren en segundos.

---

## FASE 0 — Desbloqueo inmediato

### Task 1: Repositorio y estructura

**Files:**
- Create: `.gitignore`
- Create: `proyecto-unity/Assets/Scripts/Drum/.gitkeep`
- Create: `entregables/guia/.gitkeep`

- [ ] **Step 1: Inicializar el repositorio**

La carpeta no está bajo control de versiones. Sin esto no hay commits, y este plan los pide en cada
tarea.

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git init
git branch -M main
```

- [ ] **Step 2: Escribir el .gitignore**

Unity genera cientos de megas de artefactos regenerables. Sin `.gitignore` el repo queda inservible
desde el primer commit.

```gitignore
# macOS
.DS_Store

# Unity
proyecto-unity/[Ll]ibrary/
proyecto-unity/[Tt]emp/
proyecto-unity/[Oo]bj/
proyecto-unity/[Bb]uild/
proyecto-unity/[Bb]uilds/
proyecto-unity/[Ll]ogs/
proyecto-unity/[Uu]ser[Ss]ettings/
proyecto-unity/[Mm]emoryCaptures/
proyecto-unity/*.apk
proyecto-unity/*.aab
*.csproj
*.sln
*.unityproj
*.pidb
*.booproj

# Python
__pycache__/
*.pyc
.pytest_cache/

# Grabaciones de latencia: pesan y son datos crudos, no fuente
mediciones/*.wav
```

- [ ] **Step 3: Crear la estructura y commitear**

```bash
mkdir -p proyecto-unity/Assets/Scripts/Drum entregables/guia mediciones
touch proyecto-unity/Assets/Scripts/Drum/.gitkeep entregables/guia/.gitkeep mediciones/.gitkeep
git add -A
git commit -m "chore: inicializar repositorio con estructura del proyecto Unity"
```

- [ ] **Step 4: Verificar**

Run: `git log --oneline && git status --short`
Expected: un commit listado, y `git status` sin archivos sin seguimiento.

---

### Task 2: Capítulos 0 y 1 de la guía

Se escriben primero porque la descarga e instalación de Unity 6 con el módulo de Android tarda
horas. Misael arranca esa instalación mientras el resto del plan se construye.

**Files:**
- Create: `entregables/guia/Guia_Bateria_VR_A.md`

- [ ] **Step 1: Escribir el encabezado y el capítulo 0**

Contenido obligatorio del capítulo 0: la tabla de traducción completa de §4 del spec, con las once
filas. Cada fila explica en una línea **por qué** cambió, no solo qué reemplaza a qué — el objetivo
es que el tutorial viejo siga siendo utilizable como referencia conceptual.

Encabezado del documento:

```markdown
# Guía — Sistema de percusión VR, etapa A

**Autor:** Abiud Misael Benítez Franco · **Fecha:** 12 de septiembre de 2026
**Versiones fijadas:** Unity 6 (6000.x LTS) · OpenXR Plugin 1.13+ · XR Interaction Toolkit 3.x
**Hardware objetivo:** Meta Quest 3S · **Máquina de desarrollo:** MacBook Apple Silicon

Esta guía construye **un pad que suena al golpearlo, con háptico, corriendo en el visor, y con
la latencia medida en milisegundos**. Nada más. Las seis piezas, las capas de velocity y la
sesión terapéutica son etapas posteriores.

Cada capítulo termina con algo que corre en el Quest 3S. Si un capítulo no produjo su artefacto,
no se avanza al siguiente: los problemas de configuración se acumulan y se vuelven imposibles de
aislar.
```

- [ ] **Step 2: Escribir el capítulo 1**

Contenido obligatorio, en este orden:

1. Instalación de Unity Hub y Unity 6 con módulos Android Build Support, OpenJDK, Android SDK & NDK
2. Cuenta de desarrollador en developers.meta.com y creación de la organización
3. Activación del modo desarrollador desde la app Meta Horizon del celular
4. Creación del proyecto con plantilla **Universal 3D (URP)**
5. Instalación de los paquetes: `com.unity.xr.openxr`, `com.unity.xr.interaction.toolkit`,
   `com.meta.xr.simulator`
6. XR Plug-in Management: OpenXR en Android, grupo Meta Quest, perfil Oculus Touch Controller
7. **Lista de verificación de Player Settings**, reproducida completa desde §3.3 del spec
8. **Lista de verificación de Audio Settings**, con el aviso de que Best Latency es el ajuste de
   mayor impacto de todo el proyecto
9. Escena trivial: un cubo con un script de rotación
10. Build y despliegue con `adb`, incluyendo la ruta del `adb` que trae Unity y el modo inalámbrico

El script del cubo va completo en la guía:

```csharp
using UnityEngine;

public sealed class CuboQueGira : MonoBehaviour
{
    [SerializeField] float gradosPorSegundo = 45f;

    void Update() => transform.Rotate(Vector3.up, gradosPorSegundo * Time.deltaTime);
}
```

Comandos de despliegue, literales:

```bash
ADB=~/Library/Application\ Support/Unity/Hub/Editor/*/PlaybackEngines/AndroidPlayer/SDK/platform-tools/adb
$ADB devices                          # debe listar el visor como "device", no "unauthorized"
$ADB install -r Builds/bateria.apk
```

Para adb inalámbrico, con el visor conectado por cable la primera vez:

```bash
$ADB tcpip 5555
$ADB shell ip route | awk '{print $9}'   # imprime la IP del visor
$ADB connect <IP>:5555
```

**Criterio de término del capítulo 1:** un cubo gris girando dentro del Quest 3S, desplegado desde
la Mac. Sin esto no se avanza.

- [ ] **Step 3: Commit**

```bash
git add entregables/guia/Guia_Bateria_VR_A.md
git commit -m "docs(guia): capitulos 0 y 1 - deprecaciones y cadena completa hasta el visor"
```

- [ ] **Step 4: Entregar a Misael para ejecución en hardware**

Este capítulo no lo puede verificar ningún agente: requiere la Mac, la cuenta de Meta y el visor.
Se entrega y se continúa con el resto del plan mientras él lo ejecuta. Cualquier paso que falle en
su máquina se corrige en la guía antes de cerrar la tarea.

---

## FASE 1 — Herramienta de medición de latencia (TDD estricto)

Esta es la única pieza verificable de punta a punta sin hardware. Se construye con pruebas primero.

### Task 3: Entorno de pruebas

**Files:**
- Modify: entorno pyenv `redes`

- [ ] **Step 1: Instalar pytest en el entorno del proyecto**

El entorno `redes` (Python 3.11.9) ya tiene numpy 1.26.4 y scipy 1.15.2, que es lo que usa el resto
de los scripts del proyecto. Solo falta pytest.

```bash
~/.pyenv/versions/redes/bin/python -m pip install pytest
```

- [ ] **Step 2: Verificar**

Run: `~/.pyenv/versions/redes/bin/python -m pytest --version`
Expected: `pytest 8.x.x`

---

### Task 4: Detección de transitorios

**Files:**
- Create: `scripts/test_latencia.py`
- Create: `scripts/latencia.py`

- [ ] **Step 1: Escribir la prueba que falla**

Crear `scripts/test_latencia.py`:

```python
# -*- coding: utf-8 -*-
"""Pruebas de latencia.py con señales sintéticas de offset conocido."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import latencia

SR = 48000


def clic(sr=SR, dur_ms=2.0, semilla=0):
    """Clic de plástico: ráfaga corta de ruido blanco. Centroide espectral alto."""
    rng = np.random.default_rng(semilla)
    n = int(sr * dur_ms / 1000)
    env = np.exp(-np.linspace(0, 6, n))
    return rng.normal(0, 1, n) * env


def bombo(sr=SR, dur_ms=300.0, f0=150.0, f1=50.0):
    """Bombo: seno con barrido descendente y decaimiento. Centroide espectral bajo."""
    n = int(sr * dur_ms / 1000)
    t = np.arange(n) / sr
    f = np.linspace(f0, f1, n)
    fase = 2 * np.pi * np.cumsum(f) / sr
    return np.sin(fase) * np.exp(-t * 12)


def mezclar(eventos, dur_s=3.0, sr=SR):
    """Coloca (señal, t_segundos) sobre silencio. Devuelve la pista."""
    x = np.zeros(int(dur_s * sr))
    for sig, t in eventos:
        i = int(t * sr)
        x[i:i + len(sig)] += sig
    return x


def test_detecta_dos_transitorios():
    x = mezclar([(clic(), 1.0), (bombo(), 1.012)])
    ts = latencia.onset_times(x, SR)
    assert len(ts) == 2, f"esperaba 2 transitorios, hubo {len(ts)}"


def test_precision_sub_milisegundo():
    x = mezclar([(clic(), 1.0), (bombo(), 1.012)])
    ts = latencia.onset_times(x, SR)
    assert abs(ts[0] - 1.000) < 0.001
    assert abs(ts[1] - 1.012) < 0.001


def test_ignora_silencio():
    x = np.zeros(SR * 2)
    assert len(latencia.onset_times(x, SR)) == 0
```

- [ ] **Step 2: Correr para verificar que falla**

Run: `~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'latencia'`

- [ ] **Step 3: Implementación mínima**

Crear `scripts/latencia.py`:

```python
# -*- coding: utf-8 -*-
"""
Mide la latencia golpe -> sonido a partir de una grabación WAV.

Protocolo (ver §7 del spec de diseño): se golpea una superficie física situada exactamente
donde vive el pad virtual. La grabación contiene dos transitorios por golpe:

  - el clic físico del control contra la superficie -> instante REAL del impacto
  - el tambor virtual por las bocinas del visor     -> sonido generado por la app

Delta = t_virtual - t_fisico.
  Positivo -> el sonido llega tarde.
  Negativo -> el sonido se adelanta, porque la predicción del plano armado va por delante
              del contacto físico. Es un resultado esperado, no un error.
"""
import numpy as np

# La ventana RMS debe cubrir al menos un ciclo completo del tono más grave del bombo (50 Hz
# -> 20 ms) o la envolvente riza y genera transitorios falsos. 5 ms es el compromiso: cubre
# 200 Hz en adelante y el refinamiento posterior recupera la precisión que la ventana borra.
VENTANA_RMS_MS = 5.0
UMBRAL_DB = -40.0

# CUIDADO: el refractario NO puede acercarse a Δ. Δ va de -25 a +25 ms, así que un refractario
# de 40 ms se tragaría el segundo transitorio de cada par y dejaría un solo onset por golpe.
# 3 ms basta para no re-disparar sobre el mismo ataque; el emparejado agrupa el resto.
SEPARACION_MIN_MS = 3.0


def _envolvente_db(x, sr, ventana_ms=VENTANA_RMS_MS):
    """RMS móvil en dB, muestra a muestra, con ventana rectangular."""
    n = max(1, int(sr * ventana_ms / 1000))
    energia = np.convolve(x.astype(np.float64) ** 2, np.ones(n) / n, mode="same")
    return 10.0 * np.log10(energia + 1e-20)


def onset_times(x, sr, umbral_db=UMBRAL_DB, separacion_min_ms=SEPARACION_MIN_MS):
    """
    Devuelve los instantes de inicio de cada transitorio, en segundos.

    Dos etapas: detección gruesa por cruce ascendente del umbral de energía, con periodo
    refractario para no contar dos veces el mismo golpe; y refinamiento hacia atrás hasta la
    primera muestra que supera el 10% del pico local, lo que da precisión de muestra.
    """
    if np.max(np.abs(x)) < 1e-12:
        return np.array([])

    x = x / np.max(np.abs(x))
    env = _envolvente_db(x, sr)

    encima = env > umbral_db
    cruces = np.flatnonzero(encima[1:] & ~encima[:-1]) + 1

    refractario = int(sr * separacion_min_ms / 1000)
    n_ventana = int(sr * VENTANA_RMS_MS / 1000)
    ventana_pico = int(sr * 0.020)

    ts, ultimo = [], -refractario - 1
    for i in cruces:
        if i - ultimo < refractario:
            continue

        # La convolución centrada adelanta el cruce ~media ventana, así que la búsqueda del
        # inicio real arranca ANTES del cruce y avanza. Buscar solo hacia atrás daría onsets
        # adelantados y rompería la precisión sub-milisegundo.
        ini = max(0, i - n_ventana)
        fin = min(len(x), i + ventana_pico)
        region = np.abs(x[ini:fin])
        if region.size == 0:
            continue

        sobre = np.flatnonzero(region > 0.10 * region.max())
        if sobre.size == 0:
            continue
        j = ini + int(sobre[0])

        if ts and (j / sr - ts[-1]) * 1000 < separacion_min_ms:
            continue                      # el refinamiento colapsó dos cruces en el mismo onset
        ts.append(j / sr)
        ultimo = i

    return np.array(ts)
```

- [ ] **Step 4: Correr para verificar que pasa**

Run: `~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/latencia.py scripts/test_latencia.py
git commit -m "feat(latencia): deteccion de transitorios con refinamiento sub-muestra"
```

---

### Task 5: Clasificación clic contra tambor

El problema real: al detectar dos transitorios no se sabe cuál es cuál, y **no se puede resolver
por orden temporal** porque Δ puede ser negativo. Se resuelve por contenido espectral — el clic del
plástico es de banda ancha con centroide alto; el bombo tiene cuerpo grave y centroide bajo.

**Esto obliga a un requisito del protocolo: medir con un sample de BOMBO, no de tarola.** Una tarola
tiene centroide alto y se confunde con el clic. Va documentado en la guía.

**Files:**
- Modify: `scripts/test_latencia.py`
- Modify: `scripts/latencia.py`

- [ ] **Step 1: Escribir las pruebas que fallan**

Añadir a `scripts/test_latencia.py`:

```python
def test_centroide_separa_clic_de_bombo():
    sc_clic = latencia.spectral_centroid(clic(), SR)
    sc_bombo = latencia.spectral_centroid(bombo(), SR)
    assert sc_clic > 3000, f"centroide del clic demasiado bajo: {sc_clic:.0f} Hz"
    assert sc_bombo < 1000, f"centroide del bombo demasiado alto: {sc_bombo:.0f} Hz"


def test_delta_positivo_sonido_tarde():
    x = mezclar([(clic(), 1.0), (bombo(), 1.012)])
    ds = latencia.deltas_ms(x, SR)
    assert len(ds) == 1
    assert abs(ds[0] - 12.0) < 1.0


def test_delta_negativo_sonido_adelantado():
    # El bombo suena ANTES del contacto físico: predicción adelantada. Debe dar Δ negativo.
    x = mezclar([(bombo(), 0.995), (clic(), 1.000)])
    ds = latencia.deltas_ms(x, SR)
    assert len(ds) == 1
    assert abs(ds[0] - (-5.0)) < 1.0


def test_varios_golpes():
    eventos = []
    for k, off in enumerate([0.008, 0.012, 0.010]):
        t = 0.5 + k * 0.6
        eventos += [(clic(semilla=k), t), (bombo(), t + off)]
    ds = latencia.deltas_ms(mezclar(eventos, dur_s=3.0), SR)
    assert len(ds) == 3
    assert all(abs(d - e * 1000) < 1.0 for d, e in zip(ds, [0.008, 0.012, 0.010]))
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v`
Expected: FAIL con `AttributeError: module 'latencia' has no attribute 'spectral_centroid'`

- [ ] **Step 3: Implementar**

Añadir a `scripts/latencia.py`:

```python
VENTANA_CENTROIDE_MS = 10.0
CORTE_CENTROIDE_HZ = 1500.0
EMPAREJADO_MAX_MS = 80.0


def spectral_centroid(seg, sr):
    """Centroide espectral de un segmento, en Hz. Media de frecuencias pesada por magnitud."""
    if len(seg) < 16:
        return 0.0
    ventana = np.hanning(len(seg))
    mag = np.abs(np.fft.rfft(seg * ventana))
    freqs = np.fft.rfftfreq(len(seg), 1.0 / sr)
    total = np.sum(mag)
    return float(np.sum(freqs * mag) / total) if total > 1e-12 else 0.0


def _centroide_en(x, sr, t, limite_s=None, ventana_ms=VENTANA_CENTROIDE_MS):
    """
    Centroide en el instante t.

    limite_s acota la ventana para que NO alcance al otro transitorio del par: con Δ de 5 ms
    una ventana fija de 10 ms metería el clic dentro del segmento del bombo y la clasificación
    podría invertirse. Se deja medio milisegundo de guarda.
    """
    i = int(t * sr)
    n = int(sr * ventana_ms / 1000)
    if limite_s is not None:
        n = min(n, max(16, int(sr * (limite_s - 0.0005))))
    return spectral_centroid(x[i:i + n], sr)


def deltas_ms(x, sr, emparejado_max_ms=EMPAREJADO_MAX_MS, corte_hz=CORTE_CENTROIDE_HZ):
    """
    Devuelve un Δ en milisegundos por cada par clic/tambor encontrado.

    Empareja transitorios consecutivos separados por menos de emparejado_max_ms y los clasifica
    por centroide espectral: el de centroide más alto es el clic físico. NO se clasifica por
    orden temporal, porque Δ negativo es un resultado válido.
    """
    ts = onset_times(x, sr)
    salida = []
    i = 0
    while i < len(ts) - 1:
        t_a, t_b = ts[i], ts[i + 1]
        if (t_b - t_a) * 1000 > emparejado_max_ms:
            i += 1
            continue

        sep = t_b - t_a
        c_a = _centroide_en(x, sr, t_a, limite_s=sep)   # acotado: no debe tocar a t_b
        c_b = _centroide_en(x, sr, t_b)
        if c_a >= c_b:
            t_clic, t_virtual = t_a, t_b
        else:
            t_clic, t_virtual = t_b, t_a

        if max(c_a, c_b) < corte_hz:
            raise ValueError(
                f"Par en t={t_a:.3f}s: ningún transitorio supera {corte_hz:.0f} Hz de centroide. "
                "¿Se midió con tarola en lugar de bombo? El protocolo exige un sample grave."
            )

        salida.append((t_virtual - t_clic) * 1000.0)
        i += 2
    return salida
```

- [ ] **Step 4: Correr para verificar que pasan**

Run: `~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v`
Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/latencia.py scripts/test_latencia.py
git commit -m "feat(latencia): clasificar clic vs tambor por centroide espectral"
```

---

### Task 6: Estadística y criterio de aceptación

**Files:**
- Modify: `scripts/test_latencia.py`
- Modify: `scripts/latencia.py`

- [ ] **Step 1: Escribir las pruebas que fallan**

Añadir a `scripts/test_latencia.py`:

```python
def test_estadistica():
    st = latencia.stats([10.0, 12.0, 11.0, 40.0, 9.0])
    assert st["n"] == 5
    assert st["mediana"] == pytest.approx(11.0)
    assert st["p90"] == pytest.approx(28.8, abs=0.1)
    assert st["min"] == pytest.approx(9.0)
    assert st["max"] == pytest.approx(40.0)


def test_veredicto_aprueba_dentro_de_rango():
    # p90 dentro de [-10, 25] -> aprueba
    assert latencia.stats([18.0] * 20)["aprueba"] is True


def test_veredicto_rechaza_tarde():
    assert latencia.stats([30.0] * 20)["aprueba"] is False


def test_veredicto_rechaza_demasiado_adelantado():
    # Δ = -30 ms: el sonido va tan adelantado que se despega del gesto
    assert latencia.stats([-30.0] * 20)["aprueba"] is False


def test_estadistica_rechaza_lista_vacia():
    with pytest.raises(ValueError, match="sin golpes"):
        latencia.stats([])
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v`
Expected: FAIL con `AttributeError: module 'latencia' has no attribute 'stats'`

- [ ] **Step 3: Implementar**

Añadir a `scripts/latencia.py`:

```python
# Criterio de aceptación del hito Go/No-Go. Ver §7.3 del spec.
# Un adelanto moderado es preferible al retraso: el oído tolera ~10 ms de adelanto y castiga
# con dureza el retraso. Por eso el rango es asimétrico.
DELTA_MIN_MS = -10.0
DELTA_MAX_MS = 25.0


def stats(deltas):
    """Estadística de una corrida y veredicto contra el criterio de aceptación."""
    if not deltas:
        raise ValueError("Corrida sin golpes detectados.")
    a = np.asarray(deltas, dtype=np.float64)
    p90 = float(np.percentile(a, 90))
    return {
        "n": int(a.size),
        "mediana": float(np.median(a)),
        "p90": p90,
        "min": float(a.min()),
        "max": float(a.max()),
        "aprueba": bool(DELTA_MIN_MS <= p90 <= DELTA_MAX_MS),
    }
```

- [ ] **Step 4: Correr para verificar que pasan**

Run: `~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v`
Expected: 12 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/latencia.py scripts/test_latencia.py
git commit -m "feat(latencia): estadistica y veredicto contra criterio de -10 a +25 ms"
```

---

### Task 7: Interfaz de línea de comandos

**Files:**
- Modify: `scripts/test_latencia.py`
- Modify: `scripts/latencia.py`

- [ ] **Step 1: Escribir la prueba que falla**

Añadir a `scripts/test_latencia.py`:

```python
def test_carga_wav_de_disco(tmp_path):
    from scipy.io import wavfile
    x = mezclar([(clic(), 1.0), (bombo(), 1.012)])
    ruta = tmp_path / "corrida.wav"
    wavfile.write(str(ruta), SR, (x / np.max(np.abs(x)) * 32767).astype(np.int16))

    sr, y = latencia.load_wav(str(ruta))
    assert sr == SR
    ds = latencia.deltas_ms(y, sr)
    assert len(ds) == 1
    assert abs(ds[0] - 12.0) < 1.0


def test_load_wav_convierte_estereo_a_mono(tmp_path):
    from scipy.io import wavfile
    x = mezclar([(clic(), 1.0), (bombo(), 1.012)])
    x = (x / np.max(np.abs(x)) * 32767).astype(np.int16)
    ruta = tmp_path / "estereo.wav"
    wavfile.write(str(ruta), SR, np.column_stack([x, x]))

    sr, y = latencia.load_wav(str(ruta))
    assert y.ndim == 1
```

- [ ] **Step 2: Correr para verificar que fallan**

Run: `~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v`
Expected: FAIL con `AttributeError: module 'latencia' has no attribute 'load_wav'`

- [ ] **Step 3: Implementar**

Añadir a `scripts/latencia.py`:

```python
def load_wav(ruta):
    """Carga un WAV y devuelve (sample_rate, señal mono float64 en [-1, 1])."""
    from scipy.io import wavfile

    sr, data = wavfile.read(ruta)
    x = data.astype(np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    if np.issubdtype(data.dtype, np.integer):
        x /= float(np.iinfo(data.dtype).max)
    return sr, x


def _main():
    import argparse

    ap = argparse.ArgumentParser(
        description="Mide la latencia golpe->sonido desde una grabación WAV."
    )
    ap.add_argument("wav", help="Grabación de la corrida, 48 kHz recomendado.")
    ap.add_argument("--etiqueta", default="", help="Nombre de la corrida, p. ej. 'con predicción'.")
    ap.add_argument("--detalle", action="store_true", help="Imprime el Δ de cada golpe.")
    args = ap.parse_args()

    sr, x = load_wav(args.wav)
    ds = deltas_ms(x, sr)
    st = stats(ds)

    if args.etiqueta:
        print(f"Corrida: {args.etiqueta}")
    print(f"Archivo: {args.wav}  ({sr} Hz)")
    print(f"Golpes detectados: {st['n']}")
    if args.detalle:
        for k, d in enumerate(ds, 1):
            print(f"  golpe {k:2d}:  {d:+7.2f} ms")
    print(f"Mediana: {st['mediana']:+7.2f} ms")
    print(f"p90:     {st['p90']:+7.2f} ms   <- el que decide")
    print(f"Rango:   {st['min']:+7.2f} .. {st['max']:+7.2f} ms")
    print(f"Criterio {DELTA_MIN_MS:+.0f} .. {DELTA_MAX_MS:+.0f} ms  ->  "
          f"{'APRUEBA' if st['aprueba'] else 'NO APRUEBA'}")

    if st["n"] < 20:
        print(f"\nAviso: {st['n']} golpes. El protocolo pide 20 para que el p90 signifique algo.")


if __name__ == "__main__":
    _main()
```

- [ ] **Step 4: Correr para verificar que pasan**

Run: `~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v`
Expected: 14 passed

- [ ] **Step 5: Verificar la CLI de punta a punta**

```bash
~/.pyenv/versions/redes/bin/python - <<'EOF'
import sys, numpy as np; sys.path.insert(0,'scripts')
from scipy.io import wavfile
from test_latencia import clic, bombo, mezclar, SR
x = mezclar([(clic(semilla=k), 0.5+k*0.4) for k in range(20)] +
            [(bombo(), 0.512+k*0.4) for k in range(20)], dur_s=9.0)
wavfile.write('mediciones/demo.wav', SR, (x/np.max(np.abs(x))*32767).astype(np.int16))
EOF
~/.pyenv/versions/redes/bin/python scripts/latencia.py mediciones/demo.wav --etiqueta "demo sintética"
```

Expected: 20 golpes detectados, mediana y p90 alrededor de +12 ms, veredicto `APRUEBA`.

- [ ] **Step 6: Commit**

```bash
git add scripts/latencia.py scripts/test_latencia.py
git commit -m "feat(latencia): CLI con veredicto y aviso de muestra insuficiente"
```

---

## FASE 2 — Código C# y pruebas EditMode

### Task 8: DrumPad y su ensamblado

**Files:**
- Create: `proyecto-unity/Assets/Scripts/Drum/Drum.asmdef`
- Create: `proyecto-unity/Assets/Scripts/Drum/DrumPad.cs`
- Create: `proyecto-unity/Assets/Tests/EditMode/EditModeTests.asmdef`
- Create: `proyecto-unity/Assets/Tests/EditMode/DrumPadTests.cs`

- [ ] **Step 1: Crear los ensamblados**

`proyecto-unity/Assets/Scripts/Drum/Drum.asmdef`:

```json
{
    "name": "Drum",
    "rootNamespace": "",
    "references": ["Unity.XR.CoreUtils"],
    "includePlatforms": [],
    "excludePlatforms": [],
    "autoReferenced": true
}
```

`proyecto-unity/Assets/Tests/EditMode/EditModeTests.asmdef`:

```json
{
    "name": "EditModeTests",
    "rootNamespace": "",
    "references": ["Drum", "UnityEngine.TestRunner", "UnityEditor.TestRunner"],
    "includePlatforms": ["Editor"],
    "excludePlatforms": [],
    "overrideReferences": true,
    "precompiledReferences": ["nunit.framework.dll"],
    "defineConstraints": ["UNITY_INCLUDE_TESTS"],
    "autoReferenced": false
}
```

- [ ] **Step 2: Escribir las pruebas que fallan**

`proyecto-unity/Assets/Tests/EditMode/DrumPadTests.cs`:

```csharp
using NUnit.Framework;
using UnityEngine;

public class DrumPadTests
{
    DrumPad pad;
    GameObject go;

    [SetUp]
    public void SetUp()
    {
        go = new GameObject("pad");
        go.transform.position = Vector3.zero;
        go.transform.rotation = Quaternion.identity;   // normal = Vector3.up
        pad = go.AddComponent<DrumPad>();
    }

    [TearDown]
    public void TearDown() => Object.DestroyImmediate(go);

    [Test]
    public void PlanoArmado_EstaPorDelanteDeLaSuperficie()
    {
        // Con armDistance = 0.06, un punto en y = 0.06 está exactamente sobre el plano armado.
        Assert.AreEqual(0f, pad.SignedDistanceToArmPlane(new Vector3(0f, 0.06f, 0f)), 1e-5f);
    }

    [Test]
    public void DistanciaPositiva_DelLadoDelJugador()
    {
        Assert.Greater(pad.SignedDistanceToArmPlane(new Vector3(0f, 0.20f, 0f)), 0f);
    }

    [Test]
    public void DistanciaNegativa_PasadoElPlanoArmado()
    {
        Assert.Less(pad.SignedDistanceToArmPlane(new Vector3(0f, 0.01f, 0f)), 0f);
    }

    [Test]
    public void DentroDelRadio_IgnoraLaAlturaSobreElPlano()
    {
        // Proyectado sobre el plano cae a 0.10 m del centro, dentro del radio de 0.15.
        Assert.IsTrue(pad.WithinRadius(new Vector3(0.10f, 0.50f, 0f)));
    }

    [Test]
    public void FueraDelRadio()
    {
        Assert.IsFalse(pad.WithinRadius(new Vector3(0.30f, 0f, 0f)));
    }

    [Test]
    public void PadRotado_LaNormalSigueAlTransform()
    {
        // Rotado 90° sobre Z, la normal local up apunta a -X en mundo.
        go.transform.rotation = Quaternion.Euler(0f, 0f, 90f);
        Assert.Less(Vector3.Dot(pad.Normal, Vector3.right), -0.99f);
        Assert.Greater(pad.SignedDistanceToArmPlane(new Vector3(-0.20f, 0f, 0f)), 0f);
    }
}
```

- [ ] **Step 3: Correr para verificar que fallan**

En Unity: `Window > General > Test Runner > EditMode > Run All`.
Expected: error de compilación, `The type or namespace name 'DrumPad' could not be found`.

- [ ] **Step 4: Implementar DrumPad**

`proyecto-unity/Assets/Scripts/Drum/DrumPad.cs`, contenido íntegro de §6.4 del spec:

```csharp
using UnityEngine;

/// Pad de percusión definido por un plano.
/// El plano de golpe pasa por transform.position con normal transform.up.
/// El plano armado está desplazado armDistance metros a lo largo de la normal.
[DisallowMultipleComponent]
public sealed class DrumPad : MonoBehaviour
{
    [Header("Geometría")]
    [SerializeField, Tooltip("Radio útil del pad, en metros.")]
    float radius = 0.15f;

    [SerializeField, Tooltip("Distancia del plano armado por delante de la superficie, en metros.")]
    float armDistance = 0.06f;

    [Header("Umbral")]
    [SerializeField, Tooltip("Velocidad normal mínima para contar como golpe, en m/s.")]
    float minVelocity = 0.4f;

    public float   ArmDistance => armDistance;
    public float   MinVelocity => minVelocity;
    public Vector3 Normal      => transform.up;
    public Vector3 Center      => transform.position;

    /// Distancia con signo al plano armado. Positiva = del lado del jugador.
    public float SignedDistanceToArmPlane(Vector3 worldPoint)
        => Vector3.Dot(worldPoint - (Center + Normal * armDistance), Normal);

    /// ¿El punto cae dentro del radio, una vez proyectado sobre el plano del pad?
    public bool WithinRadius(Vector3 worldPoint)
    {
        Vector3 flat = Vector3.ProjectOnPlane(worldPoint - Center, Normal);
        return flat.sqrMagnitude <= radius * radius;
    }

    void OnDrawGizmos()
    {
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(Center, radius);
        Gizmos.color = Color.cyan;                       // plano armado
        Gizmos.DrawWireSphere(Center + Normal * armDistance, radius);
        Gizmos.DrawLine(Center, Center + Normal * armDistance);
    }
}
```

- [ ] **Step 5: Correr para verificar que pasan**

En Unity: `Test Runner > EditMode > Run All`.
Expected: 6 pruebas en verde.

- [ ] **Step 6: Commit**

```bash
git add proyecto-unity/Assets/Scripts/Drum proyecto-unity/Assets/Tests
git commit -m "feat(drum): DrumPad con plano armado y pruebas EditMode"
```

---

### Task 9: DrumHit y el receptor

**Files:**
- Create: `proyecto-unity/Assets/Scripts/Drum/DrumHit.cs`
- Create: `proyecto-unity/Assets/Scripts/Drum/DrumHitSink.cs`
- Create: `proyecto-unity/Assets/Scripts/Drum/DrumHitFanout.cs`
- Create: `proyecto-unity/Assets/Tests/EditMode/DrumHitFanoutTests.cs`

- [ ] **Step 1: Escribir la prueba que falla**

`proyecto-unity/Assets/Tests/EditMode/DrumHitFanoutTests.cs`:

```csharp
using NUnit.Framework;
using UnityEngine;
using UnityEngine.XR;

public class DrumHitFanoutTests
{
    class SinkEspia : DrumHitSink
    {
        public int Recibidos;
        public DrumHit Ultimo;
        public override void Handle(in DrumHit hit) { Recibidos++; Ultimo = hit; }
    }

    [Test]
    public void Fanout_RepartePorIgualATodosLosDestinos()
    {
        var go = new GameObject("fanout");
        var a = go.AddComponent<SinkEspia>();
        var b = go.AddComponent<SinkEspia>();
        var fanout = go.AddComponent<DrumHitFanout>();
        fanout.SetTargetsForTests(new DrumHitSink[] { a, b });

        fanout.Handle(new DrumHit(null, 3.5f, 1234.5, Vector3.zero, XRNode.RightHand));

        Assert.AreEqual(1, a.Recibidos);
        Assert.AreEqual(1, b.Recibidos);
        Assert.AreEqual(3.5f, a.Ultimo.Velocity, 1e-5f);
        Assert.AreEqual(1234.5, b.Ultimo.ImpactDsp, 1e-9);

        Object.DestroyImmediate(go);
    }

    [Test]
    public void Fanout_SinDestinos_NoRevienta()
    {
        var go = new GameObject("fanout");
        var fanout = go.AddComponent<DrumHitFanout>();
        fanout.SetTargetsForTests(new DrumHitSink[0]);
        Assert.DoesNotThrow(() =>
            fanout.Handle(new DrumHit(null, 1f, 0.0, Vector3.zero, XRNode.LeftHand)));
        Object.DestroyImmediate(go);
    }
}
```

- [ ] **Step 2: Correr para verificar que falla**

En Unity: `Test Runner > EditMode > Run All`.
Expected: error de compilación, `'DrumHitSink' could not be found`.

- [ ] **Step 3: Implementar**

`proyecto-unity/Assets/Scripts/Drum/DrumHit.cs`:

```csharp
using UnityEngine;
using UnityEngine.XR;

/// Contrato entre la detección de golpe y sus consumidores.
/// Struct de solo lectura: se pasa con 'in' para evitar copias en el camino caliente.
public readonly struct DrumHit
{
    public readonly DrumPad Pad;
    public readonly float   Velocity;    // m/s sobre la normal del pad, siempre positiva
    public readonly double  ImpactDsp;   // instante estimado del impacto, reloj DSP
    public readonly Vector3 Point;
    public readonly XRNode  Hand;

    public DrumHit(DrumPad pad, float velocity, double impactDsp, Vector3 point, XRNode hand)
    {
        Pad       = pad;
        Velocity  = velocity;
        ImpactDsp = impactDsp;
        Point     = point;
        Hand      = hand;
    }
}
```

`proyecto-unity/Assets/Scripts/Drum/DrumHitSink.cs`:

```csharp
using UnityEngine;

/// Receptor de golpes. Clase abstracta y no interfaz, para poder asignarla desde el inspector:
/// Unity no serializa referencias a interfaces en campos de MonoBehaviour.
public abstract class DrumHitSink : MonoBehaviour
{
    public abstract void Handle(in DrumHit hit);
}
```

`proyecto-unity/Assets/Scripts/Drum/DrumHitFanout.cs` — **archivo propio, no dentro de
`DrumHitSink.cs`**: Unity solo deja arrastrar al inspector el MonoBehaviour cuyo nombre coincide
con el del archivo. Metido en el archivo del sink, el fanout sería inasignable desde el editor.

```csharp
using UnityEngine;

/// Reparte cada golpe a varios receptores. Es el sink de producción:
/// StickTracker apunta aquí, y de aquí salen audio, háptico y sonda de latencia.
public sealed class DrumHitFanout : DrumHitSink
{
    [SerializeField] DrumHitSink[] targets;

    public override void Handle(in DrumHit hit)
    {
        if (targets == null) return;
        for (int i = 0; i < targets.Length; i++)
            if (targets[i] != null) targets[i].Handle(in hit);
    }

    /// Solo para pruebas EditMode: el inspector no existe fuera del editor.
    public void SetTargetsForTests(DrumHitSink[] t) => targets = t;
}
```

- [ ] **Step 4: Correr para verificar que pasan**

En Unity: `Test Runner > EditMode > Run All`.
Expected: 8 pruebas en verde.

- [ ] **Step 5: Commit**

```bash
git add proyecto-unity/Assets/Scripts/Drum proyecto-unity/Assets/Tests
git commit -m "feat(drum): DrumHit y reparto a multiples receptores"
```

---

### Task 10: Lógica de cruce, aislada y probable

La detección de cruce es matemática pura. Se extrae a una clase estática sin `MonoBehaviour` para
poder probarla sin visor, sin controles y sin reloj de audio. `StickTracker` queda como cascarón
que lee hardware y delega.

**Files:**
- Create: `proyecto-unity/Assets/Scripts/Drum/CrossSolver.cs`
- Create: `proyecto-unity/Assets/Tests/EditMode/CrossSolverTests.cs`

- [ ] **Step 1: Escribir las pruebas que fallan**

`proyecto-unity/Assets/Tests/EditMode/CrossSolverTests.cs`:

```csharp
using NUnit.Framework;
using UnityEngine;

public class CrossSolverTests
{
    [Test]
    public void Cruce_AMitadDelIntervalo_DaFraccionMedia()
    {
        // dPrev = +0.02, dNow = -0.02  ->  cruzó exactamente a la mitad
        Assert.AreEqual(0.5f, CrossSolver.Fraction(0.02f, -0.02f), 1e-5f);
    }

    [Test]
    public void Cruce_CercaDelFinal()
    {
        // dPrev = +0.01, dNow = -0.03  ->  t = 0.01 / 0.04 = 0.25
        Assert.AreEqual(0.25f, CrossSolver.Fraction(0.01f, -0.03f), 1e-5f);
    }

    [Test]
    public void TiempoDeImpacto_SumaElTramoQueFalta()
    {
        // Cruce en dsp=100.0, faltan 0.06 m a 4 m/s  ->  +15 ms
        double t = CrossSolver.ImpactDsp(dspCross: 100.0, armDistance: 0.06f, normalVelocity: 4f);
        Assert.AreEqual(100.015, t, 1e-6);
    }

    [Test]
    public void TiempoDeImpacto_GolpeLento_TardaMas()
    {
        double lento  = CrossSolver.ImpactDsp(100.0, 0.06f, 1f);    // +60 ms
        double rapido = CrossSolver.ImpactDsp(100.0, 0.06f, 8f);    // +7.5 ms
        Assert.Greater(lento, rapido);
        Assert.AreEqual(100.060, lento,  1e-6);
        Assert.AreEqual(100.0075, rapido, 1e-6);
    }

    [Test]
    public void VelocidadNormal_SoloCuentaLaComponenteHaciaElPad()
    {
        // Normal = up. Movimiento puramente lateral no es acercamiento.
        Assert.AreEqual(0f, CrossSolver.NormalSpeed(new Vector3(5f, 0f, 0f), Vector3.up), 1e-5f);
        // Bajando a 3 m/s contra un pad cuya normal apunta arriba: acercamiento +3.
        Assert.AreEqual(3f, CrossSolver.NormalSpeed(new Vector3(0f, -3f, 0f), Vector3.up), 1e-5f);
    }

    [Test]
    public void VelocidadNormal_Alejandose_EsNegativa()
    {
        Assert.Less(CrossSolver.NormalSpeed(new Vector3(0f, 2f, 0f), Vector3.up), 0f);
    }

    [Test]
    public void VelocidadDePunta_IncluyeElGiroDeMuneca()
    {
        // Control quieto, girando a 10 rad/s sobre Z, punta a 0.3 m en +X.
        // v = ω × r = (0,0,10) × (0.3,0,0) = (0, 3, 0)  ->  3 m/s por puro giro.
        Vector3 v = CrossSolver.TipVelocity(
            deviceVelocityWorld: Vector3.zero,
            angularVelocityWorld: new Vector3(0f, 0f, 10f),
            controllerToTip: new Vector3(0.3f, 0f, 0f));
        Assert.AreEqual(3f, v.y, 1e-4f);
        Assert.AreEqual(3f, v.magnitude, 1e-4f);
    }
}
```

- [ ] **Step 2: Correr para verificar que fallan**

En Unity: `Test Runner > EditMode > Run All`.
Expected: error de compilación, `'CrossSolver' could not be found`.

- [ ] **Step 3: Implementar**

`proyecto-unity/Assets/Scripts/Drum/CrossSolver.cs`:

```csharp
using UnityEngine;

/// Matemática de la detección de golpe. Sin estado, sin MonoBehaviour, sin hardware:
/// todo lo que aquí vive se puede probar en EditMode sin visor.
public static class CrossSolver
{
    /// Fracción del intervalo entre frames en la que el punto cruzó el plano.
    /// dPrev debe ser positivo (antes del plano) y dNow negativo o cero (pasado el plano).
    public static float Fraction(float dPrev, float dNow)
    {
        float denom = dPrev - dNow;
        return Mathf.Approximately(denom, 0f) ? 0f : dPrev / denom;
    }

    /// Instante estimado del impacto: al cruce le falta recorrer armDistance a normalVelocity.
    /// Ésta es la predicción que compensa la latencia percibida.
    public static double ImpactDsp(double dspCross, float armDistance, float normalVelocity)
    {
        if (normalVelocity <= 0f) return dspCross;
        return dspCross + armDistance / normalVelocity;
    }

    /// Componente de la velocidad en dirección al pad, positiva si se acerca.
    public static float NormalSpeed(Vector3 velocityWorld, Vector3 padNormal)
        => -Vector3.Dot(velocityWorld, padNormal);

    /// Velocidad de la PUNTA, no del controlador: v_punta = v_dispositivo + ω × r.
    /// Con baqueta larga el giro de muñeca aporta la mayor parte de la velocidad del extremo.
    /// Todos los argumentos deben venir ya en espacio de MUNDO.
    public static Vector3 TipVelocity(Vector3 deviceVelocityWorld,
                                      Vector3 angularVelocityWorld,
                                      Vector3 controllerToTip)
        => deviceVelocityWorld + Vector3.Cross(angularVelocityWorld, controllerToTip);
}
```

- [ ] **Step 4: Correr para verificar que pasan**

En Unity: `Test Runner > EditMode > Run All`.
Expected: 15 pruebas en verde.

- [ ] **Step 5: Commit**

```bash
git add proyecto-unity/Assets/Scripts/Drum proyecto-unity/Assets/Tests
git commit -m "feat(drum): CrossSolver con la matematica del cruce, probada sin visor"
```

---

### Task 11: StickTracker

**Files:**
- Create: `proyecto-unity/Assets/Scripts/Drum/StickTracker.cs`

No lleva pruebas EditMode: todo lo que tiene lógica ya está en `CrossSolver` y `DrumPad`, y lo
que queda es lectura de hardware. Se valida en el visor, en el capítulo 4.

- [ ] **Step 1: Implementar**

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;

/// Sigue la punta de una baqueta y emite DrumHit al cruzar el plano armado de un pad.
/// La matemática vive en CrossSolver; esto lee hardware y orquesta.
public sealed class StickTracker : MonoBehaviour
{
    [SerializeField] XRNode      hand = XRNode.RightHand;
    [SerializeField] Transform   xrOrigin;    // el XR Origin de la escena
    [SerializeField] Transform   controller;  // GameObject con el TrackedPoseDriver de esta mano
    [SerializeField] Transform   tip;         // punta de la baqueta, hija de controller
    [SerializeField] DrumPad[]   pads;
    [SerializeField] DrumHitSink sink;

    [SerializeField, Tooltip("Corrección constante entre el reloj de pose y el de audio, en segundos. " +
                             "Se determina midiendo, en el capítulo 6. No se adivina.")]
    float poseToAudioOffset = 0f;

    InputDevice device;
    Vector3     prevTip;
    double      prevDsp;
    bool        primed;

    readonly Dictionary<DrumPad, bool> armed = new();

    void OnEnable()
    {
        device = InputDevices.GetDeviceAtXRNode(hand);
        primed = false;
        armed.Clear();
        foreach (var p in pads) armed[p] = true;
    }

    void Update()
    {
        if (!device.isValid)
        {
            device = InputDevices.GetDeviceAtXRNode(hand);
            if (!device.isValid) return;
        }

        // Lectura ÚNICA del reloj DSP por frame. Regla del proyecto: nunca Time.time.
        double  dspNow = AudioSettings.dspTime + poseToAudioOffset;
        Vector3 tipNow = tip.position;

        if (!primed)
        {
            prevTip = tipNow;
            prevDsp = dspNow;
            primed  = true;
            return;
        }

        Vector3 vTip = ReadTipVelocity();

        for (int i = 0; i < pads.Length; i++)
            Evaluate(pads[i], tipNow, vTip, dspNow);

        prevTip = tipNow;
        prevDsp = dspNow;
    }

    /// CUIDADO CON LOS ESPACIOS: deviceVelocity y deviceAngularVelocity vienen en el espacio del
    /// XR Origin, mientras que tip.position y pad.Normal están en mundo. Mezclarlos da magnitudes
    /// correctas con direcciones equivocadas en cuanto el jugador gira.
    Vector3 ReadTipVelocity()
    {
        device.TryGetFeatureValue(CommonUsages.deviceVelocity,        out Vector3 v);
        device.TryGetFeatureValue(CommonUsages.deviceAngularVelocity, out Vector3 w);

        return CrossSolver.TipVelocity(
            xrOrigin.TransformVector(v),
            xrOrigin.TransformVector(w),
            tip.position - controller.position);
    }

    void Evaluate(DrumPad pad, Vector3 tipNow, Vector3 vTip, double dspNow)
    {
        float dPrev = pad.SignedDistanceToArmPlane(prevTip);
        float dNow  = pad.SignedDistanceToArmPlane(tipNow);

        // Rearme POR POSICIÓN, no por tiempo: el pad revive cuando la baqueta vuelve a salir.
        // Un cooldown temporal destruiría los redobles.
        if (dNow > 0f && dPrev <= 0f) { armed[pad] = true; return; }

        if (!armed[pad]) return;
        if (!(dPrev > 0f && dNow <= 0f)) return;              // no cruzó hacia adentro

        float vNormal = CrossSolver.NormalSpeed(vTip, pad.Normal);
        if (vNormal < pad.MinVelocity) return;

        float   t01        = CrossSolver.Fraction(dPrev, dNow);
        Vector3 crossPoint = Vector3.Lerp(prevTip, tipNow, t01);
        if (!pad.WithinRadius(crossPoint)) return;

        double dspCross  = prevDsp + (dspNow - prevDsp) * t01;
        double dspImpact = CrossSolver.ImpactDsp(dspCross, pad.ArmDistance, vNormal);

        armed[pad] = false;
        sink.Handle(new DrumHit(pad, vNormal, dspImpact, crossPoint, hand));
    }
}
```

- [ ] **Step 2: Verificar que compila**

En Unity, tras guardar: la consola no muestra errores y `Test Runner > EditMode > Run All` sigue en
15 verdes.

- [ ] **Step 3: Commit**

```bash
git add proyecto-unity/Assets/Scripts/Drum/StickTracker.cs
git commit -m "feat(drum): StickTracker con deteccion de cruce y rearme por posicion"
```

---

### Task 12: DrumVoice, háptico y sonda

**Files:**
- Create: `proyecto-unity/Assets/Scripts/Drum/DrumVoice.cs`
- Create: `proyecto-unity/Assets/Scripts/Drum/HapticSink.cs`
- Create: `proyecto-unity/Assets/Scripts/Drum/LatencyProbe.cs`

- [ ] **Step 1: Implementar DrumVoice**

```csharp
using UnityEngine;

/// Pool de AudioSource con agendado en el reloj DSP.
/// Cero asignaciones en el camino del golpe: el recolector de basura produce caídas de frame,
/// y una caída de frame es latencia.
public sealed class DrumVoice : DrumHitSink
{
    [SerializeField] AudioClip clip;
    [SerializeField] int voices = 8;
    [SerializeField] AnimationCurve velocityToGain =
        AnimationCurve.Linear(0.4f, 0.2f, 6f, 1f);

    AudioSource[] pool;
    int next;

    void Awake()
    {
        pool = new AudioSource[voices];
        for (int i = 0; i < voices; i++)
        {
            // AddComponent en Awake, nunca en runtime.
            var src = gameObject.AddComponent<AudioSource>();
            src.clip                  = clip;
            src.playOnAwake           = false;
            src.spatialBlend          = 0f;     // 2D: sin coste de espacialización
            src.bypassEffects         = true;
            src.bypassListenerEffects = true;
            src.bypassReverbZones     = true;
            pool[i] = src;
        }
    }

    public override void Handle(in DrumHit hit)
    {
        var src = pool[next];
        next = (next + 1) % pool.Length;

        if (src.isPlaying) src.Stop();
        src.volume = Mathf.Clamp01(velocityToGain.Evaluate(hit.Velocity));

        if (hit.ImpactDsp <= AudioSettings.dspTime)
        {
            LatencyProbe.CountLateSchedule();   // la predicción no alcanzó
            src.Play();                          // ya vamos tarde, disparar de inmediato
        }
        else
        {
            src.PlayScheduled(hit.ImpactDsp);
        }
    }
}
```

- [ ] **Step 2: Implementar HapticSink**

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;

/// El háptico NO se puede agendar: SendHapticImpulse dispara de inmediato.
/// Si se lanzara en el cruce del plano armado llegaría ~15 ms antes del impacto, y el usuario
/// sentiría la vibración antes de "tocar" el pad. Por eso el golpe queda pendiente hasta que
/// el reloj DSP alcanza ImpactDsp.
public sealed class HapticSink : DrumHitSink
{
    [SerializeField, Tooltip("Velocidad en m/s que corresponde a amplitud 1.0.")]
    float velocityForFullAmplitude = 6f;

    [SerializeField] float durationSeconds = 0.04f;

    struct Pending { public double Dsp; public float Amplitude; public XRNode Hand; }

    readonly List<Pending> pending = new(8);

    public override void Handle(in DrumHit hit)
    {
        pending.Add(new Pending
        {
            Dsp       = hit.ImpactDsp,
            Amplitude = Mathf.Clamp01(hit.Velocity / velocityForFullAmplitude),
            Hand      = hit.Hand,
        });
    }

    void Update()
    {
        double now = AudioSettings.dspTime;
        for (int i = pending.Count - 1; i >= 0; i--)
        {
            if (pending[i].Dsp > now) continue;
            Fire(pending[i]);
            pending.RemoveAt(i);
        }
    }

    void Fire(Pending p)
    {
        var device = InputDevices.GetDeviceAtXRNode(p.Hand);
        if (!device.isValid) return;
        if (device.TryGetHapticCapabilities(out var caps) && caps.supportsImpulse)
            device.SendHapticImpulse(0u, p.Amplitude, durationSeconds);
    }
}
```

- [ ] **Step 3: Implementar LatencyProbe**

```csharp
using System.Collections.Generic;
using System.IO;
using UnityEngine;

/// Sonda interna. Registra cada golpe y cuenta las agendas que cayeron en el pasado
/// (predicción fallida: el audio sale tarde necesariamente).
///
/// LIMITACIÓN DECLARADA: esto mide solo el tramo de audio. No incluye latencia de tracking ni
/// de presentación. La medición externa con clic físico (scripts/latencia.py) es la que vale
/// para el hito Go/No-Go.
public sealed class LatencyProbe : DrumHitSink
{
    [System.Serializable]
    struct Registro
    {
        public double dspImpacto;
        public double dspAhora;
        public float  velocidad;
        public bool   agendaTardia;
    }

    [System.Serializable]
    class Volcado
    {
        public int totalGolpes;
        public int agendasTardias;
        public List<Registro> registros = new();
    }

    static int lateSchedules;
    public static void CountLateSchedule() => lateSchedules++;

    readonly Volcado volcado = new();

    public override void Handle(in DrumHit hit)
    {
        double now = AudioSettings.dspTime;
        volcado.registros.Add(new Registro
        {
            dspImpacto   = hit.ImpactDsp,
            dspAhora     = now,
            velocidad    = hit.Velocity,
            agendaTardia = hit.ImpactDsp <= now,
        });
    }

    void OnApplicationPause(bool paused) { if (paused) Dump(); }
    void OnApplicationQuit() => Dump();

    void Dump()
    {
        if (volcado.registros.Count == 0) return;

        volcado.totalGolpes    = volcado.registros.Count;
        volcado.agendasTardias = lateSchedules;

        string ruta = Path.Combine(Application.persistentDataPath,
            $"latencia_{System.DateTime.Now:yyyyMMdd_HHmmss}.json");
        File.WriteAllText(ruta, JsonUtility.ToJson(volcado, true));
        Debug.Log($"[LatencyProbe] {volcado.totalGolpes} golpes, " +
                  $"{volcado.agendasTardias} agendas tardías -> {ruta}");
    }
}
```

- [ ] **Step 4: Verificar que compila y que las pruebas siguen verdes**

En Unity: consola sin errores, `Test Runner > EditMode > Run All` en 15 verdes.

- [ ] **Step 5: Commit**

```bash
git add proyecto-unity/Assets/Scripts/Drum
git commit -m "feat(drum): audio agendado, haptico diferido y sonda de latencia"
```

---

### Task 13: Calibrador del pad

Sin esto la medición de latencia no significa nada: el pad virtual tiene que coincidir con la
superficie física que produce el clic.

**Files:**
- Create: `proyecto-unity/Assets/Scripts/Drum/PadCalibrator.cs`

- [ ] **Step 1: Implementar**

```csharp
using UnityEngine;
using UnityEngine.XR;

/// Coloca el pad virtual exactamente donde está la superficie física de medición.
/// Se apoya la punta del control sobre la superficie y se presiona el botón primario:
/// el pad se mueve a ese punto, con la normal apuntando hacia arriba en el mundo.
public sealed class PadCalibrator : MonoBehaviour
{
    [SerializeField] DrumPad   pad;
    [SerializeField] Transform tip;
    [SerializeField] XRNode    hand = XRNode.RightHand;

    bool prevPressed;

    void Update()
    {
        var device = InputDevices.GetDeviceAtXRNode(hand);
        if (!device.isValid) return;

        if (!device.TryGetFeatureValue(CommonUsages.primaryButton, out bool pressed)) return;

        if (pressed && !prevPressed)
        {
            pad.transform.position = tip.position;
            pad.transform.rotation = Quaternion.identity;   // normal = Vector3.up
            Debug.Log($"[PadCalibrator] Pad recolocado en {tip.position}");
        }
        prevPressed = pressed;
    }
}
```

- [ ] **Step 2: Verificar que compila**

En Unity: consola sin errores.

- [ ] **Step 3: Commit**

```bash
git add proyecto-unity/Assets/Scripts/Drum/PadCalibrator.cs
git commit -m "feat(drum): calibrador que fija el pad sobre la superficie fisica"
```

---

## FASE 3 — Capítulos restantes de la guía

Cada tarea de esta fase escribe un capítulo. Los capítulos **referencian** los archivos de
`proyecto-unity/Assets/Scripts/Drum/` en vez de duplicar el código, salvo fragmentos cortos que se
explican línea por línea. Duplicar el código completo en la guía garantiza que se desincronicen.

### Task 14: Capítulo 2 — C# para quien viene de Java

**Files:**
- Modify: `entregables/guia/Guia_Bateria_VR_A.md`

- [ ] **Step 1: Escribir el apéndice**

Diez diferencias, en este orden, cada una con un fragmento de Java y su equivalente en C#:

1. `struct` frente a `class` — semántica de valor, y por qué `DrumHit` es struct
2. *Properties* con `get`/`set`, y la forma de expresión `=>`
3. `[SerializeField]` — por qué un campo privado aparece en el inspector, y por qué eso es mejor
   que hacerlo público
4. **El `null` de Unity que no es `null`** — `Destroy` deja el objeto en "fake null", `==` está
   sobrecargado, y por eso `?.` sobre un `MonoBehaviour` destruido no hace lo que parece
5. `var`
6. Eventos y `delegate` frente a las interfaces de callback de Java
7. `out` y `ref`
8. `readonly` frente a `final`
9. Ausencia de excepciones verificadas — no hay `throws` en la firma
10. `in` en parámetros, y por qué `Handle(in DrumHit hit)` lo usa

Cada punto en cinco líneas o menos. Esto es una tabla de consulta, no un curso.

- [ ] **Step 2: Commit**

```bash
git add entregables/guia/Guia_Bateria_VR_A.md
git commit -m "docs(guia): capitulo 2 - apendice de C# para quien viene de Java"
```

---

### Task 15: Capítulo 3 — Manos que se mueven y vibran

**Files:**
- Modify: `entregables/guia/Guia_Bateria_VR_A.md`

- [ ] **Step 1: Escribir el capítulo**

Contenido:

1. Añadir el XR Origin a la escena (`GameObject > XR > XR Origin (VR)`)
2. Qué es el `TrackedPoseDriver` y por qué la pose llega ya predicha al instante de presentación
3. Lectura de `CommonUsages.devicePosition`, `deviceVelocity`, `deviceAngularVelocity`
4. Un cilindro delgado como baqueta, hijo del controlador, con un `Transform` vacío en la punta
5. Háptico de prueba con el gatillo

Script de diagnóstico que va completo en la guía:

```csharp
using UnityEngine;
using UnityEngine.XR;

/// Imprime en pantalla lo que reporta el control. Sirve para confirmar que el tracking llega
/// antes de construir nada encima.
public sealed class DiagnosticoMano : MonoBehaviour
{
    [SerializeField] XRNode hand = XRNode.RightHand;

    void Update()
    {
        var device = InputDevices.GetDeviceAtXRNode(hand);
        if (!device.isValid) { Debug.Log("control no válido"); return; }

        device.TryGetFeatureValue(CommonUsages.deviceVelocity, out Vector3 v);
        device.TryGetFeatureValue(CommonUsages.triggerButton,  out bool gatillo);

        if (gatillo && device.TryGetHapticCapabilities(out var caps) && caps.supportsImpulse)
            device.SendHapticImpulse(0u, 0.5f, 0.05f);

        Debug.Log($"velocidad {v.magnitude:F2} m/s");
    }
}
```

**Criterio de término:** en el visor, la baqueta sigue la mano y el control vibra al apretar el
gatillo. En la consola de `adb logcat` se ve la velocidad subir al agitar el brazo.

Comando para leer la consola desde la Mac:

```bash
$ADB logcat -s Unity:V
```

- [ ] **Step 2: Commit**

```bash
git add entregables/guia/Guia_Bateria_VR_A.md
git commit -m "docs(guia): capitulo 3 - pose, velocidad y haptico"
```

---

### Task 16: Capítulo 4 — El pad suena al golpearlo

Es el capítulo central. Explica el porqué de cada decisión, no solo los pasos.

**Files:**
- Modify: `entregables/guia/Guia_Bateria_VR_A.md`

- [ ] **Step 1: Escribir el capítulo**

Secciones obligatorias:

1. **Por qué no colliders.** `OnTriggerEnter` llega en el paso de física, después del cruce real,
   sumando medio tick (~5–11 ms). Y a 10 m/s el controlador avanza 11 cm entre frames a 90 Hz: el
   tunelado se traga golpes enteros. La prueba de plano detecta el *cruce*, no la superposición.
2. **El plano armado.** Diagrama en texto de los dos planos, la distancia de 6 cm, y la fórmula
   `t_impacto = t_cruce + armDistance / v_normal`. Ejemplo numérico a 4 m/s: 15 ms de adelanto.
3. **Por qué `dspTime` y nunca `Time.deltaTime`.** El tiempo de frame es irregular y acumula
   deriva a lo largo de una sesión de doce minutos.
4. **Velocidad de punta contra velocidad de control.** La fórmula `v + ω × r` con el ejemplo
   numérico de la prueba: control quieto girando a 10 rad/s con punta a 30 cm da 3 m/s de puro giro.
5. **La trampa de los espacios de coordenadas.** `deviceVelocity` viene en espacio del XR Origin;
   `pad.Normal` está en mundo. Mezclarlos "funciona" mirando al frente y falla al voltearse. Éste
   es el error que más caro sale porque no se manifiesta hasta que el usuario gira.
6. **Rearme por posición, no por tiempo.** Semicorcheas a 160 BPM son 94 ms entre golpes; un
   cooldown temporal de 100 ms destruiría el redoble.
7. Ensamblado de la escena: qué componente va en qué GameObject y cómo se conectan las referencias
   en el inspector, incluido el `DrumHitFanout` apuntando a `DrumVoice`, `HapticSink` y
   `LatencyProbe`.
8. Obtención del sample de bombo. Fuentes libres y por qué el protocolo de medición exige bombo y
   no tarola: el centroide espectral del bombo se separa del clic del plástico, el de la tarola no.

Los scripts se referencian por ruta, no se copian:
`proyecto-unity/Assets/Scripts/Drum/{DrumPad,CrossSolver,StickTracker,DrumVoice,HapticSink}.cs`

**Criterio de término:** el pad suena al golpearlo dentro del Quest 3S, con vibración, y el volumen
cambia según la fuerza del golpe.

- [ ] **Step 2: Commit**

```bash
git add entregables/guia/Guia_Bateria_VR_A.md
git commit -m "docs(guia): capitulo 4 - plano armado, prediccion y audio agendado"
```

---

### Task 17: Capítulo 5 — Medición de latencia

**Files:**
- Modify: `entregables/guia/Guia_Bateria_VR_A.md`

- [ ] **Step 1: Escribir el capítulo**

Contenido, reproduciendo §7 del spec y añadiendo el uso de la herramienta:

1. **Por qué no contar frames de video.** 240 fps da 4.2 ms de precisión; el umbral es de 25 ms.
   La grabación de audio da precisión de muestra, bajo el milisegundo.
2. **El clic físico como verdad de referencia.** Los dos transitorios y qué es cada uno.
3. Montaje: superficie física, calibración con `PadCalibrator` y el botón A, **audio por bocinas
   del visor y jamás por Bluetooth** (los audífonos inalámbricos añaden 100–200 ms), celular a
   menos de 30 cm, sample de bombo.
4. Veinte golpes por corrida. Dos corridas: con predicción y sin predicción, cambiando
   `armDistance` a 0 para desactivarla.
5. Análisis:

```bash
~/.pyenv/versions/redes/bin/python scripts/latencia.py mediciones/con_prediccion.wav \
    --etiqueta "con predicción" --detalle
~/.pyenv/versions/redes/bin/python scripts/latencia.py mediciones/sin_prediccion.wav \
    --etiqueta "sin predicción"
```

6. **Cómo leer un Δ negativo.** No es error de medición: con la predicción calibrada el tambor
   suena antes del contacto físico. El oído tolera ~10 ms de adelanto y castiga el retraso, por eso
   el criterio es asimétrico: −10 ms ≤ Δ(p90) ≤ +25 ms.
7. **Qué hacer si no aprueba.** Orden de intervención, del más barato al más caro: verificar Best
   Latency y 48 kHz, subir `armDistance`, calibrar `poseToAudioOffset`, bajar a 72 Hz fijo.
8. Registro del resultado como evidencia del hito Go/No-Go, con las dos cifras y la fecha.

**Criterio de término:** dos números de latencia con mediana y p90, y un veredicto.

- [ ] **Step 2: Commit**

```bash
git add entregables/guia/Guia_Bateria_VR_A.md
git commit -m "docs(guia): capitulo 5 - protocolo de medicion con clic fisico"
```

---

### Task 18: Capítulo 6 — Ajustes que bajan la latencia

**Files:**
- Modify: `entregables/guia/Guia_Bateria_VR_A.md`

- [ ] **Step 1: Escribir el capítulo**

Cada ajuste se presenta con su costo en milisegundos y se **vuelve a medir** después de aplicarlo,
con el mismo protocolo del capítulo 5. El capítulo produce una tabla comparativa real, no teórica.

| Ajuste | Efecto esperado |
|---|---|
| DSP Buffer Size: Best Latency (256) frente a Good (512) | ~5 ms contra ~11 ms en el buffer |
| System Sample Rate 48000 | Elimina el remuestreo |
| Vulkan en lugar de OpenGLES3 | Menos latencia de presentación |
| 72 Hz fijo frente a 90 Hz con caídas | Un frame estable de 13.9 ms vence a uno inestable de 11 ms |
| `spatialBlend = 0` y bypass de efectos | Quita procesamiento del camino del audio |
| Calibración de `poseToAudioOffset` | Barrido de −10 a +10 ms en pasos de 2 ms, midiendo cada uno |

La calibración de `poseToAudioOffset` es el único parámetro que **no se puede deducir**: se barre y
se elige el valor que minimiza el p90 medido. Va explicado como procedimiento, con la tabla de
resultados en blanco para llenar.

- [ ] **Step 2: Commit**

```bash
git add entregables/guia/Guia_Bateria_VR_A.md
git commit -m "docs(guia): capitulo 6 - ajustes de latencia con medicion antes y despues"
```

---

### Task 19: Capítulo 7 — Esbozo de la etapa B

**Files:**
- Modify: `entregables/guia/Guia_Bateria_VR_A.md`

- [ ] **Step 1: Escribir el capítulo**

Arquitectura y decisiones, sin código completo. Contenido de §8 del spec:

1. **Seis piezas y el filtro de proximidad.** Por qué en A no está: con un pad, 1 prueba por frame
   por mano; con seis, 12. El collider amplio filtra y dentro va la prueba de plano.
2. **Capas de velocity.** 3 capas × 2–3 round-robin por pieza. Mapeo con `AnimationCurve` en el
   inspector, editable sin recompilar. Rango útil 0.5–8 m/s.
3. **Pool de voces dimensionado.** Cómo estimar el peor caso de redoble y por qué no se asigna nada
   en runtime.
4. **Anti-retrigger por posición.** Ya está implementado en `StickTracker`; aquí se explica por qué
   se eligió así desde A en vez de dejarlo para B.
5. Presupuesto de rendimiento heredado: <500 draw calls, <300 000 triángulos, ASTC, iluminación
   bakeada, single-pass instanced, foveated rendering, 72 Hz.
6. **Lo que queda fuera y por qué:** hi-hat con pedal, audio espacializado (suma latencia sin valor
   terapéutico), baqueta con Rigidbody, y toda la etapa C.

- [ ] **Step 2: Commit**

```bash
git add entregables/guia/Guia_Bateria_VR_A.md
git commit -m "docs(guia): capitulo 7 - esbozo de la etapa B"
```

---

### Task 20: Cierre

**Files:**
- Modify: `scripts/README.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Documentar latencia.py en el README de scripts**

Añadir a la tabla de módulos de `scripts/README.md`:

```markdown
| `latencia.py` | Mide la latencia golpe→sonido desde una grabación WAV. Detecta los dos transitorios (clic físico y tambor virtual), los clasifica por centroide espectral y reporta mediana, p90 y veredicto contra el criterio de −10 a +25 ms. Requiere el entorno pyenv `redes`. |
| `test_latencia.py` | Pruebas de `latencia.py` con WAV sintéticos de offset conocido. Correr con `~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v`. |
```

- [ ] **Step 2: Añadir la sección de desarrollo a CLAUDE.md**

Añadir al final de `CLAUDE.md`:

```markdown
## Desarrollo del prototipo — etapa A

| | |
|---|---|
| Guía | `entregables/guia/Guia_Bateria_VR_A.md` — 8 capítulos, cada uno produce algo que corre en el visor |
| Spec | `docs/superpowers/specs/2026-09-12-guia-bateria-vr-unity-design.md` |
| Plan | `docs/superpowers/plans/2026-09-12-bateria-vr-etapa-a.md` |
| Código | `proyecto-unity/Assets/Scripts/Drum/` con pruebas EditMode en `Assets/Tests/EditMode/` |
| Medición | `scripts/latencia.py`, entorno pyenv `redes` |

**Hardware:** Quest 3S comprado para desarrollo diario; Quest 3 de la Facultad reservado para las
pruebas con usuarios (lente pancake e IPD continuo importan para sesiones de 12 min).

**Máquina:** MacBook Apple Silicon. Quest Link no está disponible — ninguna máquina del usuario
tiene GPU dedicada compatible. Ciclo: Meta XR Simulator en play mode, y build APK + adb al visor.

**Criterio Go/No-Go de latencia:** −10 ms ≤ Δ(p90) ≤ +25 ms, medido con clic físico. Δ negativo es
resultado válido, no error: la predicción del plano armado adelanta el sonido.

**Regla que no se rompe:** el reloj rítmico sale de `AudioSettings.dspTime`, leído una sola vez por
frame. Nunca `Time.time` ni `Time.deltaTime`.

**Discrepancia de rol pendiente:** el acta v3.0 asigna el desarrollo VR a María Fernanda; en la
práctica lo ejecuta Misael. Afecta el cálculo de sobreasignación.
```

- [ ] **Step 3: Correr toda la batería de pruebas**

```bash
~/.pyenv/versions/redes/bin/python -m pytest scripts/test_latencia.py -v
```
Expected: 14 passed

En Unity: `Test Runner > EditMode > Run All`.
Expected: 15 pruebas en verde.

- [ ] **Step 4: Commit**

```bash
git add scripts/README.md CLAUDE.md
git commit -m "docs: registrar etapa A en CLAUDE.md y README de scripts"
```

---

## Resumen de verificación

| Qué | Cómo se verifica | Quién |
|---|---|---|
| `latencia.py` | 14 pruebas pytest con WAV sintéticos de offset conocido | Agente, sin hardware |
| `DrumPad`, `CrossSolver`, `DrumHitFanout` | 15 pruebas EditMode de Unity | Misael, sin visor |
| `StickTracker`, `DrumVoice`, `HapticSink` | Capítulo 4 en el visor | Misael, con visor |
| Cadena de build | Capítulo 1: cubo girando en el Quest 3S | Misael, con visor |
| Latencia | Capítulo 5: mediana y p90 de 20 golpes, dos corridas | Misael, con visor |
| Guía completa | Cada capítulo produjo su artefacto declarado | Misael |
