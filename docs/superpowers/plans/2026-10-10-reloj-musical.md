# Reloj musical — Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development
> (recomendado) o superpowers:executing-plans para ejecutar este plan tarea por tarea. Los pasos
> usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Goal:** Dar al juego de ritmo una posición musical derivada del reloj de audio, no del tiempo
de frame, para que un golpe pueda compararse contra un beat sin deriva ni compensaciones.

**Architecture:** Dos clases puras —`TempoMap` convierte segundos ↔ beats, `MusicalTime`
descompone un beat en compás y subdivisión— más un MonoBehaviour `MusicalClock` que arranca la
canción con `PlayScheduled` y expone la posición. Las dos puras se prueban en EditMode sin audio
ni escena, igual que `CrossSolver` y `HitIntensity`.

**Tech Stack:** Unity 6000.5.10f1 · C# · NUnit (EditMode) · `AudioSettings.dspTime`

**Spec:** `docs/superpowers/specs/2026-10-07-reloj-musical-design.md`

**Proyecto Unity:** `/Users/abiudbenitez/Documents/code/Unity/BateriaVR`

---

## Mapa de archivos

| Archivo | Responsabilidad |
|---|---|
| `Assets/Scripts/Drum/TempoMap.cs` | Conversión segundos ↔ beats. La abstracción que deja abierta la puerta al tempo variable |
| `Assets/Scripts/Drum/MusicalTime.cs` | Descompone un beat en compás, pulso y subdivisión |
| `Assets/Scripts/Drum/MusicalClock.cs` | MonoBehaviour: arranca la canción y expone la posición |
| `Assets/Tests/EditMode/TempoMapTests.cs` | Pruebas de conversión, incluida la del tempo no constante |
| `Assets/Tests/EditMode/MusicalTimeTests.cs` | Pruebas de compases y subdivisiones |

**Por qué dos clases puras y no una:** convertir tiempo y descomponer compases son preguntas
distintas. La conversión cambiará cuando llegue el tempo variable; la descomposición no.
Separarlas evita que un cambio en una obligue a revisar las pruebas de la otra.

**Convenciones del proyecto que hay que respetar:**
- Comentarios en español explicando el **porqué**, no el qué. Identificadores en inglés o
  español según el dominio, como ya hace el resto del código.
- `AudioSettings.dspTime` se lee **una sola vez por frame**.
- Cero asignaciones en el camino caliente.
- Las clases puras no heredan de `MonoBehaviour`, para poder probarlas sin escena.

---

### Task 1: `TempoMap` — conversión segundos ↔ beats

**Files:**
- Create: `Assets/Scripts/Drum/TempoMap.cs`
- Create: `Assets/Tests/EditMode/TempoMapTests.cs`

- [ ] **Step 1: Escribir las pruebas que fallan**

Crear `Assets/Tests/EditMode/TempoMapTests.cs`:

```csharp
using NUnit.Framework;

/// La conversión entre tiempo y beats es la base del juego de ritmo: si deriva, la canción se
/// desincroniza. Se prueba sin audio porque TempoMap no depende de Unity.
public class TempoMapTests
{
    const double Tol = 1e-9;

    [Test]
    public void A120BpmUnBeatDuraMedioSegundo()
    {
        var t = new TempoConstante(120.0);
        Assert.AreEqual(0.5, t.BeatsASegundos(1.0), Tol);
        Assert.AreEqual(1.0, t.SegundosABeats(0.5), Tol);
    }

    [Test]
    public void A60BpmUnBeatDuraUnSegundo()
    {
        var t = new TempoConstante(60.0);
        Assert.AreEqual(1.0, t.BeatsASegundos(1.0), Tol);
    }

    [Test]
    public void LaIdaYVueltaDevuelveElOriginal()
    {
        var t = new TempoConstante(137.5);          // un BPM feo a propósito
        foreach (double beats in new[] { 0.0, 0.25, 1.0, 7.5, 128.0, 1000.0 })
            Assert.AreEqual(beats, t.SegundosABeats(t.BeatsASegundos(beats)), 1e-6,
                $"La ida y vuelta perdió precisión en {beats} beats.");
    }

    [Test]
    public void TiempoNegativoDaBeatsNegativos()
    {
        // Antes de que la canción empiece. Es la cuenta regresiva, no un error.
        var t = new TempoConstante(120.0);
        Assert.AreEqual(-2.0, t.SegundosABeats(-1.0), Tol);
        Assert.Less(t.BeatsASegundos(-4.0), 0.0);
    }

    [Test]
    public void UnBpmInvalidoSeRechazaAlConstruir()
    {
        Assert.Throws<System.ArgumentOutOfRangeException>(() => new TempoConstante(0.0));
        Assert.Throws<System.ArgumentOutOfRangeException>(() => new TempoConstante(-120.0));
    }

    [Test]
    public void ElBpmSeConsultaEnCualquierPunto()
    {
        var t = new TempoConstante(90.0);
        Assert.AreEqual(90.0, t.BpmEn(0.0), Tol);
        Assert.AreEqual(90.0, t.BpmEn(512.0), Tol);
    }
}
```

- [ ] **Step 2: Correr para verificar que fallan**

Con Unity cerrado:

```bash
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode \
  -projectPath /Users/abiudbenitez/Documents/code/Unity/BateriaVR \
  -testResults /tmp/t.xml -logFile /tmp/t.log
```

Expected: error de compilación, `The type or namespace name 'TempoConstante' could not be found`.

- [ ] **Step 3: Implementar**

Crear `Assets/Scripts/Drum/TempoMap.cs`:

```csharp
using System;

/// Convierte entre segundos y beats.
///
/// Es una interfaz y no una fórmula suelta porque el acta describe el iso-principio: la sesión
/// mide el tempo espontáneo del usuario, arranca ahí y desciende hasta 60 BPM. Cuando llegue
/// esa rampa, se implementa otro TempoMap y nada de lo que lo consume cambia — ni el beatmap,
/// ni el marcador, ni las ventanas de precisión.
///
/// El coste de dejar la puerta abierta hoy son dos métodos en lugar de multiplicar por
/// bpm/60 repartido por el código.
public interface ITempoMap
{
    /// Beats transcurridos desde el inicio de la canción. Negativo antes del arranque.
    double SegundosABeats(double segundos);

    /// Segundos desde el inicio hasta ese beat. Inversa exacta de SegundosABeats.
    double BeatsASegundos(double beats);

    /// Tempo instantáneo en ese punto. Con tempo constante no depende del argumento.
    double BpmEn(double beats);
}

/// Tempo fijo durante toda la pieza. Es lo que entregan las pistas con BPM determinado.
public sealed class TempoConstante : ITempoMap
{
    readonly double bpm;
    readonly double segundosPorBeat;

    public TempoConstante(double bpm)
    {
        if (bpm <= 0.0 || double.IsNaN(bpm) || double.IsInfinity(bpm))
            throw new ArgumentOutOfRangeException(
                nameof(bpm), bpm,
                "El tempo debe ser mayor que cero. Un BPM de cero o negativo haría que la " +
                "conversión dividiera entre cero y la canción nunca avanzaría.");

        this.bpm = bpm;
        // Se precalcula: la conversión se llama una vez por frame y por nota visible.
        segundosPorBeat = 60.0 / bpm;
    }

    public double Bpm => bpm;
    public double SegundosPorBeat => segundosPorBeat;

    public double SegundosABeats(double segundos) => segundos / segundosPorBeat;
    public double BeatsASegundos(double beats) => beats * segundosPorBeat;
    public double BpmEn(double beats) => bpm;
}
```

- [ ] **Step 4: Correr para verificar que pasan**

```bash
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode \
  -projectPath /Users/abiudbenitez/Documents/code/Unity/BateriaVR \
  -testResults /tmp/t.xml -logFile /tmp/t.log
~/.pyenv/versions/redes/bin/python -c "
import xml.etree.ElementTree as ET
r=ET.parse('/tmp/t.xml').getroot()
print(f\"{r.get('passed')}/{r.get('total')} pasadas, {r.get('failed')} fallidas\")"
```

Expected: 56 de 56 pasadas (50 previas + 6 nuevas), 0 fallidas.

- [ ] **Step 5: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/TempoMap.cs Assets/Tests/EditMode/TempoMapTests.cs
git commit -m "feat(ritmo): conversion entre segundos y beats

ITempoMap es interfaz y no formula suelta porque el acta describe el iso-principio: la sesion
desciende del tempo espontaneo del usuario hasta 60 BPM. Cuando llegue esa rampa se implementa
otro mapa y nada de lo que lo consume cambia.

La implementacion de hoy es de tempo constante, que es lo que entregan las pistas con BPM
determinado.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Ybbgks8A3tRN6mPEhbwDMc"
```

---

### Task 2: La prueba que verifica que la puerta quedó abierta

Esta tarea no añade funcionalidad. Añade la prueba que detecta si alguien, más adelante,
implementa una conversión asumiendo tempo fijo. Sin ella, la abstracción de la Task 1 es una
promesa sin verificar.

**Files:**
- Modify: `Assets/Tests/EditMode/TempoMapTests.cs`

- [ ] **Step 1: Escribir la prueba que falla**

Añadir al final de `TempoMapTests.cs`, antes de la llave de cierre de la clase:

```csharp
    /// Tempo que cambia a mitad de pieza. No es una implementación de producción: existe solo
    /// para comprobar que quien consuma ITempoMap no pueda asumir un tempo fijo.
    sealed class TempoDeDosTramos : ITempoMap
    {
        readonly double bpmA, bpmB, beatDelCambio;

        public TempoDeDosTramos(double bpmA, double bpmB, double beatDelCambio)
        {
            this.bpmA = bpmA; this.bpmB = bpmB; this.beatDelCambio = beatDelCambio;
        }

        public double BeatsASegundos(double beats)
        {
            if (beats <= beatDelCambio) return beats * 60.0 / bpmA;
            double hastaElCambio = beatDelCambio * 60.0 / bpmA;
            return hastaElCambio + (beats - beatDelCambio) * 60.0 / bpmB;
        }

        public double SegundosABeats(double segundos)
        {
            double segundosDelCambio = beatDelCambio * 60.0 / bpmA;
            if (segundos <= segundosDelCambio) return segundos * bpmA / 60.0;
            return beatDelCambio + (segundos - segundosDelCambio) * bpmB / 60.0;
        }

        public double BpmEn(double beats) => beats <= beatDelCambio ? bpmA : bpmB;
    }

    [Test]
    public void LaIdaYVueltaSeMantieneConTempoVariable()
    {
        // 90 BPM los primeros 16 beats, 60 BPM después: el descenso del iso-principio.
        ITempoMap t = new TempoDeDosTramos(90.0, 60.0, 16.0);

        foreach (double beats in new[] { 0.0, 8.0, 16.0, 24.0, 64.0 })
            Assert.AreEqual(beats, t.SegundosABeats(t.BeatsASegundos(beats)), 1e-6,
                $"La ida y vuelta falló en {beats} beats con tempo variable.");
    }

    [Test]
    public void ElTempoVariableCambiaElBpmSegunElPunto()
    {
        ITempoMap t = new TempoDeDosTramos(90.0, 60.0, 16.0);
        Assert.AreEqual(90.0, t.BpmEn(4.0), Tol);
        Assert.AreEqual(60.0, t.BpmEn(32.0), Tol);
    }
```

- [ ] **Step 2: Correr para verificar que fallan**

```bash
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode \
  -projectPath /Users/abiudbenitez/Documents/code/Unity/BateriaVR \
  -testResults /tmp/t.xml -logFile /tmp/t.log
```

Expected: compila y **pasan**. Si `ITempoMap` quedó bien definida en la Task 1, estas pruebas
pasan sin tocar código de producción — que es exactamente lo que verifican. Si fallan, la
interfaz tiene una suposición de tempo fijo escondida y hay que corregirla.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Tests/EditMode/TempoMapTests.cs
git commit -m "test(ritmo): verificar que ITempoMap admite tempo variable

La abstraccion de ITempoMap promete que el tempo puede dejar de ser constante sin tocar a sus
consumidores. Esta prueba lo comprueba con un mapa de dos tramos: 90 BPM los primeros 16 beats
y 60 despues, que es el descenso del iso-principio del acta.

No es una implementacion de produccion. Existe para que, si alguien escribe mas adelante una
conversion asumiendo tempo fijo, la prueba falle en lugar de descubrirse cuando haga falta la
rampa.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Ybbgks8A3tRN6mPEhbwDMc"
```

---

### Task 3: `MusicalTime` — compases y subdivisiones

Cierra `JT.3`, la actividad que quedó fuera del reparto de R14 por un error de conteo.

**Files:**
- Create: `Assets/Scripts/Drum/MusicalTime.cs`
- Create: `Assets/Tests/EditMode/MusicalTimeTests.cs`

- [ ] **Step 1: Escribir las pruebas que fallan**

Crear `Assets/Tests/EditMode/MusicalTimeTests.cs`:

```csharp
using NUnit.Framework;

/// Descomposición de una posición en beats. Es lo que permite colocar notas en un beatmap
/// hablando de compases en lugar de números sueltos.
public class MusicalTimeTests
{
    const double Tol = 1e-9;

    [Test]
    public void ElPrimerBeatEsCompasCeroPulsoCero()
    {
        var p = MusicalTime.Descomponer(0.0, pulsosPorCompas: 4);
        Assert.AreEqual(0, p.Compas);
        Assert.AreEqual(0, p.Pulso);
        Assert.AreEqual(0.0, p.Subdivision, Tol);
    }

    [Test]
    public void ElBeatCuatroAbreElSegundoCompas()
    {
        var p = MusicalTime.Descomponer(4.0, pulsosPorCompas: 4);
        Assert.AreEqual(1, p.Compas);
        Assert.AreEqual(0, p.Pulso);
    }

    [Test]
    public void LaSubdivisionEsLaFraccionDelPulso()
    {
        // Beat 6.5 en 4/4: segundo compás, tercer pulso, a mitad de camino del siguiente.
        var p = MusicalTime.Descomponer(6.5, pulsosPorCompas: 4);
        Assert.AreEqual(1, p.Compas);
        Assert.AreEqual(2, p.Pulso);
        Assert.AreEqual(0.5, p.Subdivision, Tol);
    }

    [Test]
    public void FuncionaEnCompasDeTres()
    {
        var p = MusicalTime.Descomponer(7.0, pulsosPorCompas: 3);
        Assert.AreEqual(2, p.Compas);     // 7 = 2 compases de 3 + 1
        Assert.AreEqual(1, p.Pulso);
    }

    [Test]
    public void UnBeatNegativoDaCompasNegativo()
    {
        // Cuenta regresiva: un pulso antes de que la canción empiece.
        var p = MusicalTime.Descomponer(-1.0, pulsosPorCompas: 4);
        Assert.AreEqual(-1, p.Compas);
        Assert.AreEqual(3, p.Pulso);
        Assert.AreEqual(0.0, p.Subdivision, Tol);
    }

    [Test]
    public void ElPulsoNuncaSeSaleDelCompas()
    {
        for (double b = -8.0; b <= 8.0; b += 0.125)
        {
            var p = MusicalTime.Descomponer(b, pulsosPorCompas: 4);
            Assert.That(p.Pulso, Is.InRange(0, 3), $"Pulso fuera de rango en beat {b}.");
            Assert.That(p.Subdivision, Is.InRange(0.0, 1.0), $"Subdivisión fuera en beat {b}.");
        }
    }

    [Test]
    public void UnCompasInvalidoSeRechaza()
    {
        Assert.Throws<System.ArgumentOutOfRangeException>(
            () => MusicalTime.Descomponer(4.0, pulsosPorCompas: 0));
    }

    [Test]
    public void SeRecomponeElBeatDesdeLaDescomposicion()
    {
        foreach (double beat in new[] { 0.0, 3.25, 6.5, 15.75, -2.5 })
        {
            var p = MusicalTime.Descomponer(beat, pulsosPorCompas: 4);
            Assert.AreEqual(beat, p.ABeat(pulsosPorCompas: 4), 1e-9,
                $"La recomposición no devolvió el beat original en {beat}.");
        }
    }
}
```

- [ ] **Step 2: Correr para verificar que fallan**

```bash
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode \
  -projectPath /Users/abiudbenitez/Documents/code/Unity/BateriaVR \
  -testResults /tmp/t.xml -logFile /tmp/t.log
```

Expected: error de compilación, `The name 'MusicalTime' does not exist`.

- [ ] **Step 3: Implementar**

Crear `Assets/Scripts/Drum/MusicalTime.cs`:

```csharp
using System;

/// Descompone una posición en beats en compás, pulso y subdivisión.
///
/// Separado de TempoMap a propósito: convertir tiempo y contar compases son preguntas
/// distintas. La conversión cambiará cuando llegue el tempo variable; la descomposición no.
public static class MusicalTime
{
    /// Posición dentro de la pieza, en términos musicales.
    public readonly struct Posicion
    {
        /// Compás, empezando en cero. Negativo antes del arranque de la canción.
        public readonly int Compas;

        /// Pulso dentro del compás. Siempre en [0, pulsosPorCompas).
        public readonly int Pulso;

        /// Fracción del pulso actual, en [0, 1). Es donde viven corcheas y semicorcheas.
        public readonly double Subdivision;

        public Posicion(int compas, int pulso, double subdivision)
        {
            Compas = compas;
            Pulso = pulso;
            Subdivision = subdivision;
        }

        /// Vuelve al beat absoluto. Inversa exacta de Descomponer.
        public double ABeat(int pulsosPorCompas) =>
            Compas * (double)pulsosPorCompas + Pulso + Subdivision;

        public override string ToString() =>
            $"compás {Compas}, pulso {Pulso}, +{Subdivision:F3}";
    }

    public static Posicion Descomponer(double beat, int pulsosPorCompas)
    {
        if (pulsosPorCompas < 1)
            throw new ArgumentOutOfRangeException(
                nameof(pulsosPorCompas), pulsosPorCompas,
                "Un compás necesita al menos un pulso.");

        // Math.Floor y no truncamiento: con beats negativos —la cuenta regresiva— truncar
        // hacia cero daría pulsos negativos y compases salteados alrededor del origen.
        double pulsoAbsoluto = Math.Floor(beat);
        double subdivision = beat - pulsoAbsoluto;

        int compas = (int)Math.Floor(pulsoAbsoluto / pulsosPorCompas);
        int pulso = (int)(pulsoAbsoluto - (double)compas * pulsosPorCompas);

        return new Posicion(compas, pulso, subdivision);
    }
}
```

- [ ] **Step 4: Correr para verificar que pasan**

```bash
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode \
  -projectPath /Users/abiudbenitez/Documents/code/Unity/BateriaVR \
  -testResults /tmp/t.xml -logFile /tmp/t.log
~/.pyenv/versions/redes/bin/python -c "
import xml.etree.ElementTree as ET
r=ET.parse('/tmp/t.xml').getroot()
print(f\"{r.get('passed')}/{r.get('total')} pasadas, {r.get('failed')} fallidas\")"
```

Expected: 66 de 66 pasadas, 0 fallidas.

- [ ] **Step 5: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/MusicalTime.cs Assets/Tests/EditMode/MusicalTimeTests.cs
git commit -m "feat(ritmo): compases y subdivisiones

Cierra JT.3, la actividad que quedo fuera del reparto de R14 por un error de conteo.

Se usa Math.Floor y no truncamiento: con beats negativos -la cuenta regresiva antes de que
arranque la cancion- truncar hacia cero daria pulsos negativos y compases salteados alrededor
del origen.

Separado de TempoMap a proposito: convertir tiempo y contar compases son preguntas distintas,
y la primera cambiara cuando llegue el tempo variable.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Ybbgks8A3tRN6mPEhbwDMc"
```

---

### Task 4: `MusicalClock` — el MonoBehaviour

No lleva pruebas EditMode: toda la lógica difícil está en las dos clases puras, y lo que queda
es coordinación con el sistema de audio. Se valida en play y en el visor.

**Files:**
- Create: `Assets/Scripts/Drum/MusicalClock.cs`

- [ ] **Step 1: Implementar**

Crear `Assets/Scripts/Drum/MusicalClock.cs`:

```csharp
using UnityEngine;

/// Posición dentro de la canción, derivada del reloj de audio.
///
/// Nunca del tiempo de frame: el frame es irregular y acumula deriva, y a lo largo de una
/// canción de tres minutos la desincronización se vuelve audible. Es el mismo motivo por el
/// que la detección de golpe usa dspTime.
public sealed class MusicalClock : MonoBehaviour
{
    [Header("Música")]
    [SerializeField] AudioSource musica;

    [SerializeField, Tooltip("Tempo de la pista, en pulsos por minuto. Lo determina el área " +
                             "de música; un valor aproximado desincroniza a los pocos compases.")]
    double bpm = 120.0;

    [SerializeField, Min(1), Tooltip("Pulsos por compás: 4 para 4/4, 3 para 3/4.")]
    int pulsosPorCompas = 4;

    [Header("Arranque")]
    [SerializeField, Tooltip("Margen antes de que suene la música, en segundos. Da tiempo al " +
                             "sistema de audio a prepararse y abre espacio para la cuenta " +
                             "regresiva: los beats negativos son válidos.")]
    double margenArranque = 0.1;

    ITempoMap tempo;
    double dspDeArranque;
    bool sonando;
    bool yaAvise;

    public bool Sonando => sonando;
    public int PulsosPorCompas => pulsosPorCompas;
    public ITempoMap Tempo => tempo;

    void Awake()
    {
        tempo = new TempoConstante(bpm);
        if (musica == null)
            Debug.LogError($"[MusicalClock] '{name}' no tiene AudioSource. La canción no va " +
                           "a sonar y el reloj no tendrá nada que medir.", this);
    }

    /// Agenda la música y pone el reloj en marcha.
    ///
    /// Se agenda con PlayScheduled en lugar de llamar a Play() y anotar dspTime después:
    /// entre esas dos líneas transcurre un tiempo desconocido que queda como desfase constante
    /// durante toda la pieza. No se nota al principio y es evidente al minuto dos.
    public void Comenzar()
    {
        if (musica == null || musica.clip == null)
        {
            Debug.LogError($"[MusicalClock] '{name}' no tiene clip que reproducir.", this);
            return;
        }

        dspDeArranque = AudioSettings.dspTime + margenArranque;
        musica.PlayScheduled(dspDeArranque);
        sonando = true;

        Debug.Log($"[MusicalClock] Canción agendada para dsp={dspDeArranque:F3}, " +
                  $"{bpm} BPM, compás de {pulsosPorCompas}. " +
                  $"Cuenta regresiva: {margenArranque:F2} s.", this);
    }

    public void Detener()
    {
        if (musica != null) musica.Stop();
        sonando = false;
    }

    /// Beat correspondiente a un instante del reloj DSP.
    ///
    /// Es el método que usa el juego de ritmo para puntuar: DrumHit.ImpactDsp ya viene en este
    /// mismo reloj, de modo que puntuar un golpe no necesita compensación de latencia alguna.
    public double BeatEn(double dsp)
    {
        if (!sonando)
        {
            if (!yaAvise)
            {
                Debug.LogWarning($"[MusicalClock] '{name}' consultado antes de Comenzar(). " +
                                 "Devuelve cero hasta que la canción arranque.", this);
                yaAvise = true;
            }
            return 0.0;
        }
        return tempo.SegundosABeats(dsp - dspDeArranque);
    }

    /// Beat actual. Negativo durante la cuenta regresiva.
    public double BeatActual() => BeatEn(AudioSettings.dspTime);

    public MusicalTime.Posicion PosicionActual() =>
        MusicalTime.Descomponer(BeatActual(), pulsosPorCompas);

    /// Instante del reloj DSP en que cae un beat. Lo usa el beatmap para agendar notas.
    public double DspDelBeat(double beat) => dspDeArranque + tempo.BeatsASegundos(beat);
}
```

- [ ] **Step 2: Verificar que compila**

```bash
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode \
  -projectPath /Users/abiudbenitez/Documents/code/Unity/BateriaVR \
  -testResults /tmp/t.xml -logFile /tmp/t.log
~/.pyenv/versions/redes/bin/python -c "
import re,pathlib,xml.etree.ElementTree as ET
L=pathlib.Path('/tmp/t.log').read_text(errors='ignore')
print('errores CS:', len(re.findall(r'error CS\d+', L)))
r=ET.parse('/tmp/t.xml').getroot()
print(f\"{r.get('passed')}/{r.get('total')} pasadas\")"
```

Expected: 0 errores, 66 de 66 pasadas.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/MusicalClock.cs
git commit -m "feat(ritmo): reloj musical derivado del reloj de audio

Cierra JT.1 y JT.2. La posicion dentro de la cancion se deriva de AudioSettings.dspTime y
nunca del tiempo de frame, que es irregular y acumula deriva.

La cancion se agenda con PlayScheduled en lugar de llamar a Play() y anotar dspTime despues:
entre esas dos lineas transcurre un tiempo desconocido que queda como desfase constante
durante toda la pieza. No se nota al principio y es evidente al minuto dos.

BeatEn(hit.ImpactDsp) es todo lo que necesita el juego para puntuar un golpe, sin compensacion
de latencia: ImpactDsp ya viene en el mismo reloj. Es lo que cobra el trabajo del hito
Go/No-Go, y es la razon por la que JY -calibrar la latencia entre golpe y musica- quedo sin
objeto.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Ybbgks8A3tRN6mPEhbwDMc"
```

---

### Task 5: Sonda de verificación en el visor

Las clases puras están probadas, pero que el reloj **no derive a lo largo de una canción real**
solo se comprueba con audio sonando. Esta sonda es el equivalente rítmico de `LatencyProbe`.

**Files:**
- Create: `Assets/Scripts/Drum/ClockProbe.cs`

- [ ] **Step 1: Implementar**

Crear `Assets/Scripts/Drum/ClockProbe.cs`:

```csharp
using UnityEngine;

/// Comprueba que el reloj musical no deriva respecto del audio que realmente suena.
///
/// Las pruebas EditMode verifican la aritmética; no pueden verificar que el reloj siga
/// pegado a la canción durante tres minutos en el visor. Eso solo se ve con audio sonando.
///
/// Compara dos relojes que deberían coincidir: la posición que el reloj musical calcula a
/// partir de dspTime, y la posición real de reproducción del AudioSource. Si divergen, hay
/// deriva.
public sealed class ClockProbe : MonoBehaviour
{
    [SerializeField] MusicalClock reloj;
    [SerializeField] AudioSource musica;

    [SerializeField, Tooltip("Cada cuántos segundos se compara. No hace falta más: la deriva " +
                             "que importa se acumula a lo largo de minutos.")]
    float intervalo = 5f;

    float siguiente;
    double desvioMaximo;

    void Update()
    {
        if (reloj == null || musica == null || !reloj.Sonando) return;
        if (!musica.isPlaying) return;
        if (Time.unscaledTime < siguiente) return;
        siguiente = Time.unscaledTime + intervalo;

        // Posición según el reloj musical, en segundos de canción.
        double segunReloj = reloj.Tempo.BeatsASegundos(reloj.BeatActual());

        // Posición real de reproducción, leída del propio AudioSource.
        double segunAudio = (double)musica.timeSamples / musica.clip.frequency;

        double desvio = segunReloj - segunAudio;
        if (Mathf.Abs((float)desvio) > Mathf.Abs((float)desvioMaximo)) desvioMaximo = desvio;

        Debug.Log($"[ClockProbe] reloj={segunReloj:F3}s  audio={segunAudio:F3}s  " +
                  $"desvío={desvio * 1000.0:+0.0;-0.0} ms  " +
                  $"máximo={desvioMaximo * 1000.0:+0.0;-0.0} ms");
    }
}
```

- [ ] **Step 2: Verificar que compila**

```bash
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode \
  -projectPath /Users/abiudbenitez/Documents/code/Unity/BateriaVR \
  -testResults /tmp/t.xml -logFile /tmp/t.log
```

Expected: 0 errores CS, 66 de 66 pasadas.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/ClockProbe.cs
git commit -m "feat(ritmo): sonda que detecta deriva del reloj musical

Las pruebas EditMode verifican la aritmetica de la conversion; no pueden verificar que el
reloj siga pegado a la cancion durante tres minutos en el visor.

La sonda compara dos relojes que deberian coincidir: la posicion que el reloj calcula desde
dspTime, y la posicion real de reproduccion leida del AudioSource. Si divergen, hay deriva.

Es el equivalente ritmico de LatencyProbe.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Ybbgks8A3tRN6mPEhbwDMc"
```

---

### Task 6: Escena de prueba y verificación en el visor

Esta tarea la ejecuta Misael en su Mac. No puede automatizarse.

**Files:**
- Create: `Assets/Scenes/Cap08_Reloj.unity` (desde el editor)

- [ ] **Step 1: Montar la escena**

1. `File → New Scene`, plantilla básica de URP. Guardar como `Assets/Scenes/Cap08_Reloj.unity`.
2. `GameObject → XR → XR Origin (VR)`. Borrar la `Main Camera` que trae la escena.
3. Crear un GameObject vacío llamado `Reloj`.
4. Añadirle un `AudioSource`: desmarcar **Play On Awake**, asignar una pista de música.
5. Añadirle `MusicalClock`. Arrastrarle el `AudioSource` propio al campo **Música**.
6. Poner el **BPM** exacto de la pista. Si Javier aún no lo entregó, usar un metrónomo de BPM
   conocido para esta prueba.
7. Añadirle `ClockProbe`. Arrastrarle el `MusicalClock` y el `AudioSource`.

- [ ] **Step 2: Disparar el arranque**

`MusicalClock.Comenzar()` es público y no se llama solo. Para la prueba, añadir un script
temporal en el mismo GameObject:

```csharp
using UnityEngine;

/// Temporal: arranca el reloj al entrar en play para poder probarlo sin menús.
public sealed class ArranqueDePrueba : MonoBehaviour
{
    [SerializeField] MusicalClock reloj;
    void Start() { if (reloj != null) reloj.Comenzar(); }
}
```

- [ ] **Step 3: Verificar en el editor**

Entrar en play y leer la consola. Expected:

```
[MusicalClock] Canción agendada para dsp=..., 120 BPM, compás de 4. Cuenta regresiva: 0.10 s.
[ClockProbe] reloj=5.012s  audio=5.011s  desvío=+1.0 ms  máximo=+1.0 ms
```

**Criterio de aceptación:** tras tres minutos de reproducción, el desvío máximo se mantiene
**por debajo de 20 ms** y no crece de forma sostenida. Un desvío que crece linealmente es
deriva y significa que el BPM configurado no coincide con el real de la pista.

- [ ] **Step 4: Verificar en el visor**

Compilar con `Batería → Compilar APK`, instalar, y leer con:

```bash
ADB=$(ls /Applications/Unity/Hub/Editor/*/PlaybackEngines/AndroidPlayer/SDK/platform-tools/adb \
        ~/Library/Application\ Support/Unity/Hub/Editor/*/PlaybackEngines/AndroidPlayer/SDK/platform-tools/adb \
        2>/dev/null | head -1)
$ADB logcat -c && $ADB logcat -s Unity:V | grep ClockProbe
```

El visor importa porque su reloj de audio es distinto al de la Mac.

- [ ] **Step 5: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scenes/Cap08_Reloj.unity Assets/Scenes/Cap08_Reloj.unity.meta
git add Assets/Scripts/Drum/ArranqueDePrueba.cs
git commit -m "feat(ritmo): escena de verificacion del reloj musical

Criterio de aceptacion: tras tres minutos de reproduccion el desvio maximo entre el reloj y el
audio real se mantiene por debajo de 20 ms y no crece de forma sostenida. Un desvio que crece
linealmente es deriva y significa que el BPM configurado no coincide con el real de la pista.

Se verifica tambien en el visor: su reloj de audio no es el de la Mac.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Ybbgks8A3tRN6mPEhbwDMc"
```

---

### Task 7: Registrar el avance

**Files:**
- Modify: `entregables/Cronograma_ProjectLibre.xml`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Marcar JT.1, JT.2 y JT.3 en el cronograma**

Desde ProjectLibre, que es lo más seguro: doble clic en cada una, `% Complete: 100`, Aceptar,
guardar.

**No editar el XML a mano.** ProjectLibre no usa los campos `Actual*` del esquema MSPDI sino un
`<Stop>` propio, y al recalcular mueve fechas que dejan los `Stop` desfasados. Ya costó tres
intentos averiguarlo.

- [ ] **Step 2: Verificar el nuevo total**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python scripts/validacion.py | head -3
```

Expected: 80 de 257 terminadas (77 previas + 3).

- [ ] **Step 3: Añadir la sección a CLAUDE.md**

Añadir antes de `## Tareas de clase entregadas`:

```markdown
## Juego de ritmo — reloj musical, desde el 10-oct-2026

El área de juego de ritmo pasó a desarrollo VR por la respuesta al riesgo R14. Primera pieza
construida: el reloj musical.

| | |
|---|---|
| Spec | `docs/superpowers/specs/2026-10-07-reloj-musical-design.md` |
| Plan | `docs/superpowers/plans/2026-10-10-reloj-musical.md` |
| Código | `TempoMap.cs` · `MusicalTime.cs` · `MusicalClock.cs` · `ClockProbe.cs` |
| Cierra | `JT.1` reloj sin deriva · `JT.2` BPM y duración de beat · `JT.3` compases |

**Puerta abierta al iso-principio.** `ITempoMap` es una interfaz con dos métodos de conversión.
La implementación de hoy es de tempo constante; cuando llegue la rampa que el acta describe
—del tempo espontáneo del usuario hasta 60 BPM— se implementa otro mapa y nada de lo que lo
consume cambia. Hay una prueba que lo verifica con un mapa de dos tramos.

**La canción se agenda, no se reproduce.** `PlayScheduled(dspTime + margen)` y el reloj arranca
en ese mismo instante. Llamar a `Play()` y anotar `dspTime` después deja un desfase constante
que se hace evidente al minuto dos.

**Puntuar un golpe no necesita compensar latencia.** `reloj.BeatEn(hit.ImpactDsp)` y ya:
`ImpactDsp` viene en el mismo reloj DSP que mide la canción. Es lo que cobra el hito Go/No-Go,
y por lo que `JY` —calibrar latencia entre golpe y música— quedó sin objeto.

**Criterio de verificación:** `ClockProbe` compara el reloj contra la posición real del
`AudioSource`. Tras tres minutos el desvío debe mantenerse por debajo de 20 ms sin crecer.
```

- [ ] **Step 4: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add CLAUDE.md entregables/Cronograma_ProjectLibre.xml
git commit -m "docs: registrar el reloj musical y su avance en el cronograma

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Ybbgks8A3tRN6mPEhbwDMc"
```

---

## Resumen de verificación

| Qué | Cómo | Quién |
|---|---|---|
| `TempoMap`, 8 pruebas | EditMode, sin audio | Agente, en batchmode |
| Puerta al tempo variable | La prueba de dos tramos pasa sin tocar producción | Agente |
| `MusicalTime`, 8 pruebas | EditMode, sin audio | Agente |
| Compilación limpia | 66 de 66, cero errores y cero avisos | Agente |
| Deriva en tres minutos | `ClockProbe`, desvío < 20 ms sin crecer | Misael, en el editor |
| Deriva en el visor | Lo mismo, con `adb logcat` | Misael, con el Quest |

## Qué NO cubre este plan

El beatmap y su formato (`JA.2`, `JA.3`, `JB.1`–`JB.3`), las notas visuales (`JN.1`, `JN.2`),
las ventanas de precisión (`JW.1`, `JW.2`, `JW.5`) y la puntuación (`JP.1`, `JP.3`). Todas
consumen este reloj y van en el siguiente plan.

Tampoco la rampa de tempo del iso-principio: la interfaz la admite, la implementación espera a
tener un requisito concreto.
