# Beatmap y juicio del golpe — Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development
> (recomendado) o superpowers:executing-plans para ejecutar este plan tarea por tarea. Los pasos
> usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Goal:** Un juego de ritmo demostrable sobre el reloj musical: notas colocadas en beats que
aparecen, caen hacia su pieza, y se juzgan contra el golpe real del jugador.

**Architecture:** `Beatmap` es un ScriptableObject con la lista de notas. `HitJudge` y
`NoteMatcher` son clases puras probadas sin Unity. `NoteSpawner` y `Scoreboard` son
MonoBehaviours que las consumen. La comparación se hace en tiempo del reloj DSP, nunca en
beats, de modo que el juez no depende del tempo.

**Tech Stack:** Unity 6000.5.10f1 · C# · NUnit (EditMode) · `AudioSettings.dspTime`

**Spec:** `docs/superpowers/specs/2026-10-17-beatmap-y-juicio-design.md`

**Proyecto Unity:** `/Users/abiudbenitez/Documents/code/Unity/BateriaVR`

**Fecha límite:** demostración el miércoles 21 de octubre. Las tareas van en orden de valor
demostrable: si la ventana se acorta, lo que cae es lo de abajo.

---

## Mapa de archivos

| Archivo | Responsabilidad |
|---|---|
| `Assets/Scripts/Drum/Beatmap.cs` | ScriptableObject: notas y metadatos de la pista |
| `Assets/Scripts/Drum/HitJudge.cs` | Pura: desfase en ms → Perfect, Good o Miss |
| `Assets/Scripts/Drum/NoteMatcher.cs` | Pura: elige qué nota corresponde a un golpe |
| `Assets/Scripts/Drum/NoteSpawner.cs` | Saca las notas antes de su beat y las mueve |
| `Assets/Scripts/Drum/Scoreboard.cs` | Cuenta aciertos y precisión, y los muestra |
| `Assets/Editor/ConstruirBeatmapDemo.cs` | Genera el beatmap de demostración sobre el metrónomo |
| `Assets/Tests/EditMode/HitJudgeTests.cs` | 7 pruebas del juez |
| `Assets/Tests/EditMode/NoteMatcherTests.cs` | 6 pruebas del emparejado |

**Por qué juez y emparejado separados:** son preguntas distintas. «¿Qué tan bien cayó este
golpe?» es aritmética sobre un número. «¿A qué nota se refiere este golpe?» es una búsqueda
sobre una lista con estado. Separarlas permite probar cada una sin montar la otra.

**Convenciones del proyecto que hay que respetar:**
- Comentarios en español explicando el **porqué**, no el qué.
- `AudioSettings.dspTime` se lee **una sola vez por frame**.
- Cero asignaciones en el camino del golpe.
- Las clases puras no heredan de `MonoBehaviour`.
- Los consumidores de golpes heredan de `DrumHitSink` y se registran en `DrumHitFanout`.
- Los componentes validan sus referencias en `Awake` con `LogError`.

---

### Task 1: `Beatmap` — el ScriptableObject

**Files:**
- Create: `Assets/Scripts/Drum/Beatmap.cs`

- [ ] **Step 1: Implementar**

Crear `Assets/Scripts/Drum/Beatmap.cs`:

```csharp
using System;
using UnityEngine;

/// Las notas de una pista, colocadas en beats.
///
/// Es un ScriptableObject y no un formato de texto por una razón de equipo, no técnica: el área
/// de música no va a autorizar beatmaps por su cuenta en la ventana que queda, así que la
/// autonomía que compraría un parser no se usaría y su coste sí se pagaría. Queda anotado
/// como lo que habría que revisar si el proyecto continuara.
[CreateAssetMenu(fileName = "Beatmap", menuName = "Batería/Beatmap")]
public sealed class Beatmap : ScriptableObject
{
    [Serializable]
    public struct Nota
    {
        [Tooltip("Posición en beats desde el inicio de la canción. 0 es el primer pulso.")]
        public double beat;

        [Tooltip("Pieza que hay que golpear. Debe ser una de las del kit.")]
        public DrumKitPiece pieza;
    }

    [Header("Pista")]
    public AudioClip pista;

    [Tooltip("Tempo de la pista. Debe coincidir EXACTAMENTE con el real: un BPM aproximado " +
             "desincroniza a los pocos compases.")]
    public double bpm = 120.0;

    [Min(1), Tooltip("Pulsos por compás: 4 para 4/4, 3 para 3/4.")]
    public int pulsosPorCompas = 4;

    [Header("Notas")]
    [Tooltip("No hace falta que estén ordenadas: se ordenan al cargar.")]
    public Nota[] notas = Array.Empty<Nota>();

    /// Devuelve las notas ordenadas por beat, sin tocar el asset.
    ///
    /// Se ordena en lugar de exigirlo al autor: colocar notas en el inspector es ya bastante
    /// trabajo, y un beatmap que falla silenciosamente por estar desordenado sería un defecto
    /// imposible de ver.
    public Nota[] NotasOrdenadas()
    {
        var copia = (Nota[])notas.Clone();
        Array.Sort(copia, (a, b) => a.beat.CompareTo(b.beat));
        return copia;
    }
}
```

- [ ] **Step 2: Verificar que compila**

Con Unity cerrado:

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/bm.xml -logFile /tmp/bm.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/bm.log',errors='ignore').read()
print('errores:',len(re.findall(r'error CS\d+',L)))
r=ET.parse('/tmp/bm.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')}\")"
```

Expected: 0 errores, 66 de 66 pasadas.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/Beatmap.cs Assets/Scripts/Drum/Beatmap.cs.meta
git commit -m "feat(ritmo): beatmap como ScriptableObject

Las notas se ordenan al cargar en lugar de exigirselo al autor: colocar notas en el inspector
es ya bastante trabajo, y un beatmap que fallara en silencio por estar desordenado seria un
defecto imposible de ver.

Se eligio ScriptableObject sobre un formato de texto por una razon de equipo, no tecnica, y
queda anotada en el codigo.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: `HitJudge` — el juez

**Files:**
- Create: `Assets/Scripts/Drum/HitJudge.cs`
- Create: `Assets/Tests/EditMode/HitJudgeTests.cs`

- [ ] **Step 1: Escribir las pruebas que fallan**

Crear `Assets/Tests/EditMode/HitJudgeTests.cs`:

```csharp
using NUnit.Framework;

/// El juez convierte un desfase en un veredicto. Es aritmética pura sobre un número: no sabe
/// de tempo, ni de audio, ni de escena, y por eso se prueba sin nada de eso.
public class HitJudgeTests
{
    [Test]
    public void EnElInstanteExactoEsPerfect()
    {
        Assert.AreEqual(HitJudge.Veredicto.Perfect, HitJudge.Juzgar(0.0, 25.0, 60.0));
    }

    [Test]
    public void DentroDeLaVentanaEstrechaEsPerfect()
    {
        Assert.AreEqual(HitJudge.Veredicto.Perfect, HitJudge.Juzgar(24.0, 25.0, 60.0));
    }

    [Test]
    public void FueraDeLaEstrechaPeroDentroDeLaAnchaEsGood()
    {
        Assert.AreEqual(HitJudge.Veredicto.Good, HitJudge.Juzgar(26.0, 25.0, 60.0));
    }

    [Test]
    public void FueraDeLaAnchaEsMiss()
    {
        Assert.AreEqual(HitJudge.Veredicto.Miss, HitJudge.Juzgar(61.0, 25.0, 60.0));
    }

    [Test]
    public void AdelantarseValeLoMismoQueAtrasarse()
    {
        // La simetría importa: un golpe 24 ms antes del beat está tan bien ejecutado como uno
        // 24 ms después. Penalizar un lado sería arbitrario.
        Assert.AreEqual(HitJudge.Juzgar(24.0, 25.0, 60.0), HitJudge.Juzgar(-24.0, 25.0, 60.0));
        Assert.AreEqual(HitJudge.Juzgar(40.0, 25.0, 60.0), HitJudge.Juzgar(-40.0, 25.0, 60.0));
        Assert.AreEqual(HitJudge.Juzgar(70.0, 25.0, 60.0), HitJudge.Juzgar(-70.0, 25.0, 60.0));
    }

    [Test]
    public void LasFronterasExactasCaenDelLadoGeneroso()
    {
        // Justo en 25.0 cuenta como Perfect, y justo en 60.0 como Good. Un jugador que clava
        // la frontera no debe ser castigado por un redondeo.
        Assert.AreEqual(HitJudge.Veredicto.Perfect, HitJudge.Juzgar(25.0, 25.0, 60.0));
        Assert.AreEqual(HitJudge.Veredicto.Good,    HitJudge.Juzgar(60.0, 25.0, 60.0));
    }

    [Test]
    public void UmbralesCruzadosNoInviertenLaEscala()
    {
        // Mismo criterio que HitIntensity: un error en el inspector no debe invertir el
        // significado de los veredictos.
        Assert.AreEqual(HitJudge.Veredicto.Perfect, HitJudge.Juzgar(10.0, 60.0, 25.0));
        Assert.AreEqual(HitJudge.Veredicto.Miss,    HitJudge.Juzgar(90.0, 60.0, 25.0));
    }
}
```

- [ ] **Step 2: Correr para verificar que fallan**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/hj.xml -logFile /tmp/hj.log 2>&1
grep -c "error CS" /tmp/hj.log
```

Expected: error de compilación, `The name 'HitJudge' does not exist in the current context`.

- [ ] **Step 3: Implementar**

Crear `Assets/Scripts/Drum/HitJudge.cs`:

```csharp
using System;

/// Convierte el desfase de un golpe en un veredicto.
///
/// LAS VENTANAS VAN EN MILISEGUNDOS, NO EN FRACCIONES DE BEAT. Una ventana expresada como «un
/// dieciseisavo de pulso» se encoge al subir el tempo, y la precisión de una persona no escala
/// con el BPM: se acierta a ±30 ms a 60 BPM y a ±30 ms a 160. Atar la ventana al tempo
/// castigaría al jugador por una propiedad de la pista y no por su ejecución.
///
/// El ±25 por defecto no es arbitrario: es el criterio Go/No-Go del acta, y la medición del
/// hito dio un percentil 90 de +4.07 ms. La ventana es seis veces el error del sistema, de
/// modo que lo que se mide es al jugador y no al motor.
public static class HitJudge
{
    public enum Veredicto { Perfect, Good, Miss }

    public const double VentanaPerfectMs = 25.0;
    public const double VentanaGoodMs    = 60.0;

    /// `desfaseMs` es negativo si el golpe se adelantó al beat y positivo si se atrasó.
    public static Veredicto Juzgar(double desfaseMs, double perfectMs, double goodMs)
    {
        // Umbrales cruzados por error en el inspector no deben invertir la escala.
        if (goodMs < perfectMs) (perfectMs, goodMs) = (goodMs, perfectMs);

        // El valor absoluto hace la simetría: adelantarse y atrasarse valen lo mismo.
        double d = Math.Abs(desfaseMs);

        // <= y no <: quien clava la frontera no debe perder por un redondeo.
        if (d <= perfectMs) return Veredicto.Perfect;
        if (d <= goodMs)    return Veredicto.Good;
        return Veredicto.Miss;
    }

    public static Veredicto Juzgar(double desfaseMs) =>
        Juzgar(desfaseMs, VentanaPerfectMs, VentanaGoodMs);
}
```

- [ ] **Step 4: Correr para verificar que pasan**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/hj2.xml -logFile /tmp/hj2.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/hj2.log',errors='ignore').read()
print('errores:',len(re.findall(r'error CS\d+',L)))
r=ET.parse('/tmp/hj2.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')} fallidas {r.get('failed')}\")
for tc in r.iter('test-case'):
    if tc.get('result')!='Passed': print('FALLA',tc.get('name'))"
```

Expected: 0 errores, 73 de 73 pasadas, 0 fallidas.

- [ ] **Step 5: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/HitJudge.cs Assets/Scripts/Drum/HitJudge.cs.meta \
        Assets/Tests/EditMode/HitJudgeTests.cs Assets/Tests/EditMode/HitJudgeTests.cs.meta
git commit -m "feat(ritmo): juez del golpe con ventanas en milisegundos

Las ventanas NO van en fracciones de beat. Una ventana de un dieciseisavo de pulso se encoge al
subir el tempo, y la precision de una persona no escala con el BPM: se acierta a mas menos
30 ms a 60 BPM y a mas menos 30 ms a 160. Atar la ventana al tempo castigaria al jugador por
una propiedad de la pista y no por su ejecucion.

El mas menos 25 por defecto es el criterio Go/No-Go del acta. La medicion del hito dio un
percentil 90 de +4.07 ms, asi que la ventana es seis veces el error del sistema: lo que se mide
es al jugador, no al motor.

Las fronteras exactas caen del lado generoso y los umbrales cruzados no invierten la escala,
igual que en HitIntensity.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: `NoteMatcher` — a qué nota corresponde un golpe

**Files:**
- Create: `Assets/Scripts/Drum/NoteMatcher.cs`
- Create: `Assets/Tests/EditMode/NoteMatcherTests.cs`

- [ ] **Step 1: Escribir las pruebas que fallan**

Crear `Assets/Tests/EditMode/NoteMatcherTests.cs`:

```csharp
using NUnit.Framework;
using UnityEngine;

/// Elegir a qué nota se refiere un golpe es una búsqueda sobre una lista con estado, distinta
/// de juzgar qué tan bien cayó. Separarlas permite probar cada una sin montar la otra.
public class NoteMatcherTests
{
    DrumKitPiece tarola, bombo;
    NoteMatcher.Pendiente[] pendientes;

    /// Las piezas se crean en memoria: NoteMatcher solo las usa como identidad, nunca lee sus
    /// muestras, así que no hace falta cargar audio.
    [SetUp]
    public void Preparar()
    {
        tarola = ScriptableObject.CreateInstance<DrumKitPiece>();
        tarola.nombrePieza = "Tarola";
        bombo = ScriptableObject.CreateInstance<DrumKitPiece>();
        bombo.nombrePieza = "Bombo";

        // Cuatro notas: bombo en 0 y 2, tarola en 1 y 3. Tiempos en segundos.
        pendientes = new[]
        {
            new NoteMatcher.Pendiente { tiempo = 0.0, pieza = bombo,  juzgada = false },
            new NoteMatcher.Pendiente { tiempo = 0.5, pieza = tarola, juzgada = false },
            new NoteMatcher.Pendiente { tiempo = 1.0, pieza = bombo,  juzgada = false },
            new NoteMatcher.Pendiente { tiempo = 1.5, pieza = tarola, juzgada = false },
        };
    }

    [TearDown]
    public void Limpiar()
    {
        Object.DestroyImmediate(tarola);
        Object.DestroyImmediate(bombo);
    }

    [Test]
    public void EligeLaNotaDeLaPiezaGolpeada()
    {
        // Golpe de tarola cerca de 0.5 s: debe elegir el índice 1, no el 0 ni el 2.
        int i = NoteMatcher.Elegir(pendientes, 0.51, tarola, 0.060);
        Assert.AreEqual(1, i);
    }

    [Test]
    public void EligeLaMasCercanaDeEsaPieza()
    {
        // Golpe de bombo a 0.95: más cerca del índice 2 (1.0) que del 0 (0.0).
        int i = NoteMatcher.Elegir(pendientes, 0.95, bombo, 0.060);
        Assert.AreEqual(2, i);
    }

    [Test]
    public void SinCandidataEnVentanaDevuelveMenosUno()
    {
        // Golpe de tarola a 0.3: la tarola más cercana está a 0.5, o sea 200 ms. Fuera de los
        // 60 ms de ventana. No se penaliza: la batería tiene que seguir siendo tocable.
        Assert.AreEqual(-1, NoteMatcher.Elegir(pendientes, 0.3, tarola, 0.060));
    }

    [Test]
    public void NoEligeUnaNotaYaJuzgada()
    {
        pendientes[1].juzgada = true;
        Assert.AreEqual(-1, NoteMatcher.Elegir(pendientes, 0.51, tarola, 0.060));
    }

    [Test]
    public void NoCruzaPiezas()
    {
        // Hay un bombo exactamente en 1.0, pero el golpe es de tarola: no debe elegirlo.
        Assert.AreEqual(-1, NoteMatcher.Elegir(pendientes, 1.0, tarola, 0.060));
    }

    [Test]
    public void UnaListaVaciaNoRevienta()
    {
        Assert.AreEqual(-1, NoteMatcher.Elegir(new NoteMatcher.Pendiente[0], 1.0, tarola, 0.060));
    }
}
```

- [ ] **Step 2: Correr para verificar que fallan**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/nm.xml -logFile /tmp/nm.log 2>&1
grep -c "error CS" /tmp/nm.log
```

Expected: error de compilación, `The name 'NoteMatcher' does not exist in the current context`.

- [ ] **Step 3: Implementar**

Crear `Assets/Scripts/Drum/NoteMatcher.cs`:

```csharp
using System;

/// Decide a qué nota se refiere un golpe.
///
/// Separado de HitJudge a propósito: juzgar es aritmética sobre un número, emparejar es una
/// búsqueda sobre una lista con estado. Mezclarlas obligaría a montar la lista entera para
/// probar una ventana de 25 ms.
///
/// Los tiempos van en SEGUNDOS del reloj DSP, que es donde viven tanto DrumHit.ImpactDsp como
/// MusicalClock.DspDelBeat. Así la comparación no pasa por el tempo.
public static class NoteMatcher
{
    /// Una nota a la espera de ser golpeada.
    public struct Pendiente
    {
        public double tiempo;          // instante del reloj DSP en que toca golpearla
        public DrumKitPiece pieza;
        public bool juzgada;           // ya se resolvió, por golpe o por Miss
    }

    /// Índice de la nota que corresponde al golpe, o -1 si ninguna.
    ///
    /// Un golpe sin nota candidata se IGNORA en lugar de penalizar. En un prototipo, castigar
    /// al jugador por tocar fuera del patrón frustra sin enseñar nada, y la batería tiene que
    /// seguir siendo tocable fuera del juego.
    public static int Elegir(Pendiente[] pendientes, double tiempoGolpe,
                             DrumKitPiece pieza, double ventanaSegundos)
    {
        if (pendientes == null || pendientes.Length == 0 || pieza == null) return -1;

        int mejor = -1;
        double menorDistancia = double.MaxValue;

        for (int i = 0; i < pendientes.Length; i++)
        {
            ref readonly Pendiente p = ref pendientes[i];
            if (p.juzgada) continue;
            if (p.pieza != pieza) continue;      // no se cruzan piezas, nunca

            double d = Math.Abs(p.tiempo - tiempoGolpe);
            if (d > ventanaSegundos) continue;
            if (d >= menorDistancia) continue;

            menorDistancia = d;
            mejor = i;
        }
        return mejor;
    }
}
```

- [ ] **Step 4: Correr para verificar que pasan**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/nm2.xml -logFile /tmp/nm2.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/nm2.log',errors='ignore').read()
print('errores:',len(re.findall(r'error CS\d+',L)))
r=ET.parse('/tmp/nm2.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')} fallidas {r.get('failed')}\")
for tc in r.iter('test-case'):
    if tc.get('result')!='Passed': print('FALLA',tc.get('name'))"
```

Expected: 0 errores, 79 de 79 pasadas, 0 fallidas.

- [ ] **Step 5: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/NoteMatcher.cs Assets/Scripts/Drum/NoteMatcher.cs.meta \
        Assets/Tests/EditMode/NoteMatcherTests.cs Assets/Tests/EditMode/NoteMatcherTests.cs.meta
git commit -m "feat(ritmo): emparejar un golpe con su nota

Separado de HitJudge a proposito: juzgar es aritmetica sobre un numero, emparejar es una
busqueda sobre una lista con estado. Mezclarlas obligaria a montar la lista entera para probar
una ventana de 25 ms.

Un golpe sin nota candidata se ignora en lugar de penalizar. En un prototipo, castigar al
jugador por tocar fuera del patron frustra sin ensenar nada, y la bateria tiene que seguir
siendo tocable fuera del juego.

Los tiempos van en segundos del reloj DSP, que es donde viven tanto DrumHit.ImpactDsp como
MusicalClock.DspDelBeat: la comparacion no pasa por el tempo.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: `NoteSpawner` — las notas aparecen y caen

Es el MonoBehaviour que convierte el beatmap en algo visible. No lleva pruebas EditMode: la
lógica difícil está en las dos clases puras, y lo que queda es colocar objetos en el espacio.

**Files:**
- Create: `Assets/Scripts/Drum/NoteSpawner.cs`

- [ ] **Step 1: Implementar**

Crear `Assets/Scripts/Drum/NoteSpawner.cs`:

```csharp
using System.Collections.Generic;
using UnityEngine;

/// Saca las notas del beatmap antes de su momento y las mueve hacia la pieza que les toca.
///
/// LA ANTICIPACIÓN VA EN SEGUNDOS, NO EN BEATS. En beats, la velocidad visual cambiaría con el
/// tempo y el jugador tendría que recalibrar el ojo en cada pista. En segundos, una nota
/// siempre tarda lo mismo en recorrer su camino, que es lo que permite aprender a anticipar.
public sealed class NoteSpawner : MonoBehaviour
{
    [Header("Fuentes")]
    [SerializeField] MusicalClock reloj;
    [SerializeField] Beatmap beatmap;

    [SerializeField, Tooltip("Los pads del kit, uno por pieza. La nota viaja hacia el pad cuya " +
                             "Pieza coincide con la suya.")]
    DrumPad[] pads;

    [Header("Aspecto")]
    [SerializeField, Tooltip("Prefab de la nota. Si queda vacío se usa una esfera primitiva, " +
                             "que basta para demostrar el mecanismo.")]
    GameObject prefabNota;

    [SerializeField, Tooltip("Segundos que tarda una nota en llegar desde que aparece. " +
                             "Más tiempo da margen para anticipar; menos exige reflejos.")]
    float anticipacionSegundos = 1.5f;

    [SerializeField, Tooltip("Altura sobre el pad a la que nace la nota.")]
    float alturaDeSalida = 1.2f;

    [SerializeField, Min(8), Tooltip("Notas que pueden estar visibles a la vez. Se reservan en " +
                                     "Awake: instanciar en el camino del golpe produciría " +
                                     "caídas de frame, y una caída de frame es latencia.")]
    int capacidad = 64;

    /// Estado de una nota en vuelo.
    struct EnVuelo
    {
        public Transform cuerpo;
        public int indicePendiente;
        public bool activa;
    }

    Beatmap.Nota[] notas;
    NoteMatcher.Pendiente[] pendientes;
    EnVuelo[] vuelo;
    Transform[] destino;          // pad de cada nota, resuelto una vez
    int siguienteNota;
    bool arrancado;

    public NoteMatcher.Pendiente[] Pendientes => pendientes;
    public float AnticipacionSegundos => anticipacionSegundos;

    void Awake()
    {
        if (reloj == null)
            Debug.LogError($"[NoteSpawner] '{name}' no tiene MusicalClock. Sin reloj no hay " +
                           "momento en el que colocar las notas.", this);
        if (beatmap == null)
            Debug.LogError($"[NoteSpawner] '{name}' no tiene Beatmap. No va a aparecer " +
                           "ninguna nota.", this);
        if (pads == null || pads.Length == 0)
            Debug.LogError($"[NoteSpawner] '{name}' no tiene pads asignados. Las notas no " +
                           "sabrían hacia dónde viajar.", this);

        // Todo el pool se reserva aquí. A partir de este punto no se instancia nada.
        vuelo = new EnVuelo[capacidad];
        for (int i = 0; i < capacidad; i++)
        {
            GameObject go = prefabNota != null
                ? Instantiate(prefabNota, transform)
                : GameObject.CreatePrimitive(PrimitiveType.Sphere);

            if (prefabNota == null)
            {
                go.transform.SetParent(transform, false);
                go.transform.localScale = Vector3.one * 0.08f;
                // Un collider en la nota cruzaría el camino del golpe sin aportar nada: la
                // detección es por plano armado, no por colisión.
                Destroy(go.GetComponent<Collider>());
            }
            go.name = $"Nota{i:00}";
            go.SetActive(false);
            vuelo[i].cuerpo = go.transform;
        }
    }

    /// Prepara el beatmap y arranca el reloj. Se llama una vez, al empezar la canción.
    public void Comenzar()
    {
        if (reloj == null || beatmap == null) return;

        notas = beatmap.NotasOrdenadas();
        if (notas.Length == 0)
            Debug.LogWarning($"[NoteSpawner] El beatmap '{beatmap.name}' no tiene notas. " +
                             "La canción va a sonar y no va a aparecer nada.", this);

        pendientes = new NoteMatcher.Pendiente[notas.Length];
        destino = new Transform[notas.Length];

        reloj.Comenzar();

        for (int i = 0; i < notas.Length; i++)
        {
            pendientes[i].tiempo  = reloj.DspDelBeat(notas[i].beat);
            pendientes[i].pieza   = notas[i].pieza;
            pendientes[i].juzgada = false;
            destino[i] = PadDe(notas[i].pieza);

            if (destino[i] == null)
                Debug.LogError($"[NoteSpawner] La nota {i} (beat {notas[i].beat}) pide una " +
                               "pieza que ningún pad declara. Esa nota no va a aparecer.", this);
        }

        siguienteNota = 0;
        arrancado = true;
    }

    Transform PadDe(DrumKitPiece pieza)
    {
        if (pieza == null || pads == null) return null;
        foreach (var p in pads)
            if (p != null && p.Pieza == pieza) return p.transform;
        return null;
    }

    void Update()
    {
        if (!arrancado || notas == null) return;

        // dspTime se lee UNA vez por frame, como en todo el proyecto.
        double ahora = AudioSettings.dspTime;

        // Sacar las notas que ya entran en la ventana de anticipación.
        while (siguienteNota < notas.Length &&
               pendientes[siguienteNota].tiempo - anticipacionSegundos <= ahora)
        {
            Lanzar(siguienteNota);
            siguienteNota++;
        }

        // Mover las que están en vuelo.
        for (int i = 0; i < vuelo.Length; i++)
        {
            if (!vuelo[i].activa) continue;
            int n = vuelo[i].indicePendiente;
            Transform pad = destino[n];
            if (pad == null) { Apagar(i); continue; }

            double restante = pendientes[n].tiempo - ahora;

            // Pasado su momento y ya resuelta: se retira. Se deja un margen para que una nota
            // juzgada no desaparezca en el mismo frame del golpe, que se vería como un parpadeo.
            if (restante < -0.25 || (pendientes[n].juzgada && restante < 0.0))
            {
                Apagar(i);
                continue;
            }

            float t = Mathf.Clamp01((float)(restante / anticipacionSegundos));
            vuelo[i].cuerpo.position = pad.position + pad.up * (alturaDeSalida * t);
        }
    }

    void Lanzar(int n)
    {
        if (destino[n] == null) return;

        for (int i = 0; i < vuelo.Length; i++)
        {
            if (vuelo[i].activa) continue;
            vuelo[i].activa = true;
            vuelo[i].indicePendiente = n;
            vuelo[i].cuerpo.gameObject.SetActive(true);
            return;
        }
        // Sin hueco libre no se instancia: perder una nota visible es preferible a una caída
        // de frame en mitad de la canción.
    }

    void Apagar(int i)
    {
        vuelo[i].activa = false;
        vuelo[i].cuerpo.gameObject.SetActive(false);
    }
}
```

- [ ] **Step 2: Verificar que compila**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/ns.xml -logFile /tmp/ns.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/ns.log',errors='ignore').read()
e=re.findall(r'error CS\d+[^\n]*',L)
print('errores:',len(e))
for l in e[:4]: print(' ',l[:120])
r=ET.parse('/tmp/ns.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')}\")"
```

Expected: 0 errores, 79 de 79 pasadas.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/NoteSpawner.cs Assets/Scripts/Drum/NoteSpawner.cs.meta
git commit -m "feat(ritmo): las notas aparecen y viajan hacia su pieza

La anticipacion va en SEGUNDOS y no en beats. En beats la velocidad visual cambiaria con el
tempo y el jugador tendria que recalibrar el ojo en cada pista; en segundos una nota siempre
tarda lo mismo en recorrer su camino, que es lo que permite aprender a anticipar.

Todo el pool se reserva en Awake. Instanciar en mitad de la cancion produciria una caida de
frame, y una caida de frame es latencia -medida, no supuesta-. Si se agota el pool se pierde
una nota visible antes que provocar ese tiron.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 5: `Scoreboard` — juzgar los golpes y llevar la cuenta

Cierra el circuito: recibe los golpes, los empareja, los juzga y muestra el resultado.

**Files:**
- Create: `Assets/Scripts/Drum/Scoreboard.cs`

- [ ] **Step 1: Implementar**

Crear `Assets/Scripts/Drum/Scoreboard.cs`:

```csharp
using System.Text;
using TMPro;
using UnityEngine;

/// Juzga cada golpe contra la nota que le toca y lleva la cuenta.
///
/// Hereda de DrumHitSink y se registra en el DrumHitFanout, igual que DrumVoice, HapticSink y
/// HitReadout: el golpe llega a todos los interesados sin que ninguno conozca a los demás.
///
/// El golpe solo actualiza contadores; el texto se arma en Update a ritmo limitado. Formatear
/// cadenas por golpe asignaría memoria en el camino caliente.
public sealed class Scoreboard : DrumHitSink
{
    [SerializeField] NoteSpawner spawner;
    [SerializeField] MusicalClock reloj;
    [SerializeField] TMP_Text texto;

    [Header("Ventanas, en milisegundos")]
    [SerializeField, Tooltip("Dentro de esto cuenta como Perfect. El valor por defecto es el " +
                             "criterio Go/No-Go del acta, y es seis veces el error medido del " +
                             "sistema: lo que se mide es al jugador, no al motor.")]
    double ventanaPerfectMs = HitJudge.VentanaPerfectMs;

    [SerializeField, Tooltip("Dentro de esto cuenta como Good; más allá, Miss.")]
    double ventanaGoodMs = HitJudge.VentanaGoodMs;

    [SerializeField, Tooltip("Refrescos por segundo del texto. El ojo no lee más rápido y " +
                             "armar la cadena cuesta.")]
    float refrescosPorSegundo = 10f;

    int perfect, good, miss;
    double ultimoDesfaseMs;
    bool huboGolpe;

    StringBuilder sb;
    float siguienteRefresco;
    bool sucio;

    public int Perfect => perfect;
    public int Good    => good;
    public int Miss    => miss;

    /// Notas acertadas sobre notas resueltas. Es la precisión que pide el entregable.
    public float Precision
    {
        get
        {
            int total = perfect + good + miss;
            return total == 0 ? 0f : 100f * (perfect + good) / total;
        }
    }

    void Awake()
    {
        sb = new StringBuilder(160);
        if (spawner == null)
            Debug.LogError($"[Scoreboard] '{name}' no tiene NoteSpawner. No habría notas " +
                           "contra las que juzgar y todos los golpes se ignorarían.", this);
        if (reloj == null)
            Debug.LogError($"[Scoreboard] '{name}' no tiene MusicalClock.", this);
        if (texto == null)
            Debug.LogError($"[Scoreboard] '{name}' no tiene TMP_Text. Se juzgaría bien y no " +
                           "se vería nada.", this);
    }

    public override void Handle(in DrumHit hit)
    {
        if (spawner == null || hit.Pad == null) return;

        var pend = spawner.Pendientes;
        if (pend == null) return;

        // La ventana de búsqueda es la de Miss: fuera de ella el golpe no se refiere a
        // ninguna nota, y se ignora sin penalizar.
        double ventanaSeg = Mathf.Max((float)ventanaPerfectMs, (float)ventanaGoodMs) / 1000.0;
        int i = NoteMatcher.Elegir(pend, hit.ImpactDsp, hit.Pad.Pieza, ventanaSeg);
        if (i < 0) return;

        double desfaseMs = (hit.ImpactDsp - pend[i].tiempo) * 1000.0;
        var v = HitJudge.Juzgar(desfaseMs, ventanaPerfectMs, ventanaGoodMs);

        pend[i].juzgada = true;
        switch (v)
        {
            case HitJudge.Veredicto.Perfect: perfect++; break;
            case HitJudge.Veredicto.Good:    good++;    break;
            default:                         miss++;    break;
        }

        ultimoDesfaseMs = desfaseMs;
        huboGolpe = true;
        sucio = true;
    }

    void Update()
    {
        // Notas cuyo momento pasó sin que nadie las golpeara: Miss por omisión.
        var pend = spawner != null ? spawner.Pendientes : null;
        if (pend != null)
        {
            double ahora = AudioSettings.dspTime;
            double limite = Mathf.Max((float)ventanaPerfectMs, (float)ventanaGoodMs) / 1000.0;
            for (int i = 0; i < pend.Length; i++)
            {
                if (pend[i].juzgada) continue;
                if (ahora - pend[i].tiempo <= limite) continue;
                pend[i].juzgada = true;
                miss++;
                sucio = true;
            }
        }

        if (!sucio || texto == null || Time.unscaledTime < siguienteRefresco) return;
        siguienteRefresco = Time.unscaledTime + 1f / Mathf.Max(1f, refrescosPorSegundo);
        sucio = false;

        sb.Clear();
        sb.Append("Perfect ").Append(perfect)
          .Append("   Good ").Append(good)
          .Append("   Miss ").Append(miss).Append('\n');
        sb.Append("Precisión ").Append(Precision.ToString("F0")).Append(" %");
        if (huboGolpe)
            sb.Append("\nÚltimo ").Append(ultimoDesfaseMs.ToString("+0;-0")).Append(" ms");
        texto.SetText(sb);
    }
}
```

- [ ] **Step 2: Verificar que compila**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/sb.xml -logFile /tmp/sb.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/sb.log',errors='ignore').read()
e=re.findall(r'error CS\d+[^\n]*',L)
print('errores:',len(e))
for l in e[:4]: print(' ',l[:120])
r=ET.parse('/tmp/sb.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')}\")"
```

Expected: 0 errores, 79 de 79 pasadas.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/Scoreboard.cs Assets/Scripts/Drum/Scoreboard.cs.meta
git commit -m "feat(ritmo): juicio del golpe y marcador

Cierra el circuito: recibe el golpe por DrumHitSink, lo empareja con su nota, lo juzga contra
las ventanas y lleva la cuenta. Las notas cuyo momento pasa sin golpe se marcan Miss solas.

El golpe solo actualiza contadores; el texto se arma en Update a ritmo limitado. Formatear
cadenas por golpe asignaria memoria en el camino caliente, igual que en HitReadout.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 6: Beatmap de demostración y escena

Genera un beatmap sobre el metrónomo de 120 BPM que ya está en el repositorio, y monta la
escena. Por menú, como el resto de constructores del proyecto.

**Files:**
- Create: `Assets/Editor/ConstruirBeatmapDemo.cs`

- [ ] **Step 1: Implementar**

Crear `Assets/Editor/ConstruirBeatmapDemo.cs`:

```csharp
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

/// Genera el beatmap de demostración sobre el metrónomo de 120 BPM exactos.
///
/// Se genera y no se coloca a mano por el mismo motivo que el metrónomo: el BPM es exacto por
/// construcción, así que un desajuste que apareciera en la demostración solo podría venir del
/// código, nunca del dato.
///
/// El patrón es el rock básico de ocho tiempos, que es lo primero que aprende cualquiera en
/// una batería: bombo en 1 y 3, tarola en 2 y 4, hi-hat en cada pulso.
public static class ConstruirBeatmapDemo
{
    const string RutaBeatmap = "Assets/Audio/Pruebas/Beatmap_Demo.asset";
    const string RutaPista   = "Assets/Audio/Pruebas/Metronomo_120BPM.wav";
    const int Compases = 16;                 // 32 segundos a 120 BPM

    [MenuItem("Batería/Construir beatmap de demostración")]
    public static void Construir()
    {
        var piezas = AssetDatabase.FindAssets("t:DrumKitPiece")
            .Select(AssetDatabase.GUIDToAssetPath)
            .Select(AssetDatabase.LoadAssetAtPath<DrumKitPiece>)
            .Where(p => p != null)
            .ToDictionary(p => p.nombrePieza, p => p);

        DrumKitPiece Buscar(params string[] nombres)
        {
            foreach (string n in nombres)
                if (piezas.TryGetValue(n, out var p)) return p;
            return piezas.Values.FirstOrDefault();
        }

        var bombo  = Buscar("Bombo");
        var tarola = Buscar("Tarola");
        var hihat  = Buscar("HiHat", "Hi-Hat");

        if (bombo == null || tarola == null || hihat == null)
        {
            EditorUtility.DisplayDialog("Batería",
                "No encontré las piezas Bombo, Tarola y HiHat. Ejecuta primero " +
                "'Batería → Construir kit de 6 piezas'.", "Vale");
            return;
        }

        var notas = new List<Beatmap.Nota>();
        for (int c = 0; c < Compases; c++)
        {
            double b = c * 4.0;
            notas.Add(new Beatmap.Nota { beat = b + 0.0, pieza = bombo  });
            notas.Add(new Beatmap.Nota { beat = b + 1.0, pieza = tarola });
            notas.Add(new Beatmap.Nota { beat = b + 2.0, pieza = bombo  });
            notas.Add(new Beatmap.Nota { beat = b + 3.0, pieza = tarola });
            for (int p = 0; p < 4; p++)
                notas.Add(new Beatmap.Nota { beat = b + p, pieza = hihat });
        }

        var bm = AssetDatabase.LoadAssetAtPath<Beatmap>(RutaBeatmap);
        bool nuevo = bm == null;
        if (nuevo) bm = ScriptableObject.CreateInstance<Beatmap>();

        bm.pista           = AssetDatabase.LoadAssetAtPath<AudioClip>(RutaPista);
        bm.bpm             = 120.0;
        bm.pulsosPorCompas = 4;
        bm.notas           = notas.ToArray();

        Directory.CreateDirectory(Path.GetDirectoryName(RutaBeatmap));
        if (nuevo) AssetDatabase.CreateAsset(bm, RutaBeatmap);
        EditorUtility.SetDirty(bm);
        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();

        string msg = $"Beatmap creado: {RutaBeatmap}\n\n" +
                     $"{notas.Count} notas · {Compases} compases · 120 BPM · " +
                     $"{Compases * 2} segundos\n\n" +
                     "Rock básico de ocho tiempos: bombo en 1 y 3, tarola en 2 y 4, " +
                     "hi-hat en cada pulso.\n\n" +
                     (bm.pista == null
                        ? "NO ENCONTRÉ LA PISTA. Asigna el metrónomo a mano."
                        : $"Pista: {bm.pista.name}");
        Debug.Log("[ConstruirBeatmapDemo] " + msg.Replace("\n", " "), bm);
        EditorUtility.DisplayDialog("Batería", msg, "Vale");
        Selection.activeObject = bm;
    }
}
```

- [ ] **Step 2: Verificar que compila**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/bd.xml -logFile /tmp/bd.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/bd.log',errors='ignore').read()
e=re.findall(r'error CS\d+[^\n]*',L)
print('errores:',len(e))
for l in e[:4]: print(' ',l[:120])
r=ET.parse('/tmp/bd.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')}\")"
```

Expected: 0 errores, 79 de 79 pasadas.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Editor/ConstruirBeatmapDemo.cs Assets/Editor/ConstruirBeatmapDemo.cs.meta
git commit -m "feat(ritmo): beatmap de demostracion sobre el metronomo

Se genera y no se coloca a mano por el mismo motivo que el metronomo: el BPM es exacto por
construccion, asi que un desajuste que apareciera en la demostracion solo podria venir del
codigo, nunca del dato.

El patron es el rock basico de ocho tiempos -bombo en 1 y 3, tarola en 2 y 4, hi-hat en cada
pulso-, que es lo primero que aprende cualquiera en una bateria.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 7: Montar y verificar en el visor

Esta tarea la ejecuta Misael. No puede automatizarse.

- [ ] **Step 1: Generar el beatmap**

En Unity: `Batería → Construir beatmap de demostración`. Debe reportar **192 notas, 16
compases, 32 segundos**.

- [ ] **Step 2: Montar sobre la escena del kit**

Abrir `Assets/Scenes/Cap04_Pad.unity`, que ya tiene las seis piezas y el `DrumHitFanout`.

1. Crear un GameObject vacío `JuegoDeRitmo`.
2. Añadirle un `AudioSource`: **Play On Awake desmarcado**, clip = `Metronomo_120BPM`.
3. Añadirle `MusicalClock` → Música: ese AudioSource · BPM: **120** · Pulsos por compás: 4.
4. Añadirle `NoteSpawner` → Reloj: el `MusicalClock` · Beatmap: `Beatmap_Demo` ·
   **Pads: arrastrar los seis pads del kit**.
5. Añadirle `Scoreboard` → Spawner · Reloj · Texto: el `TMP_Text` del indicador que ya existe,
   o uno nuevo.
6. **Registrar el `Scoreboard` en el array `Targets` del `DrumHitFanout`.** Sin esto los golpes
   se detectan y se descartan en silencio — es exactamente el bug del 16 de septiembre.
7. Añadirle `ArranqueDePrueba` → Reloj: el `MusicalClock`.

⚠️ `ArranqueDePrueba` llama a `MusicalClock.Comenzar()`, pero el que debe arrancar es
`NoteSpawner.Comenzar()`, que a su vez arranca el reloj. **Cambiar la referencia del
`ArranqueDePrueba`** o añadir un disparador que llame al spawner.

- [ ] **Step 2b: Ajustar `ArranqueDePrueba` para que arranque el spawner**

Reemplazar `Assets/Scripts/Drum/ArranqueDePrueba.cs` por:

```csharp
using UnityEngine;

/// Temporal: arranca el juego al entrar en play para poder probarlo sin menús.
///
/// Se retira cuando el flujo de la aplicación llame a Comenzar() desde la pantalla previa.
public sealed class ArranqueDePrueba : MonoBehaviour
{
    [SerializeField, Tooltip("Si hay spawner, se arranca él: el spawner arranca el reloj por " +
                             "dentro después de preparar las notas. Arrancar el reloj por " +
                             "separado dejaría las notas colocadas contra un origen distinto.")]
    NoteSpawner spawner;

    [SerializeField, Tooltip("Respaldo para escenas sin juego, como Cap08_Reloj.")]
    MusicalClock reloj;

    void Start()
    {
        if (spawner != null) { spawner.Comenzar(); return; }
        if (reloj != null)   { reloj.Comenzar();   return; }
        Debug.LogError($"[ArranqueDePrueba] '{name}' no tiene ni spawner ni reloj.", this);
    }
}
```

Verificar que compila y commitear:

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/ap.xml -logFile /tmp/ap.log 2>&1
grep -c "error CS" /tmp/ap.log
git add Assets/Scripts/Drum/ArranqueDePrueba.cs
git commit -m "fix(ritmo): el arranque de prueba lanza el spawner, no el reloj

El spawner arranca el reloj por dentro, despues de preparar las notas. Arrancar el reloj por
separado dejaria las notas colocadas contra un origen distinto del que mide la cancion.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

- [ ] **Step 3: Verificar en el editor**

Entrar en play. **Criterios de aceptación:**

1. Las notas aparecen sobre los pads y bajan hacia ellos.
2. Golpear un pad cuando su nota llega suma a **Perfect** o **Good**.
3. No golpear una nota suma a **Miss**.
4. Golpear un pad sin nota cerca **no cambia ningún contador**.
5. La precisión se muestra como porcentaje.
6. El campo «Último» muestra un desfase de pocas decenas de milisegundos.

- [ ] **Step 4: Verificar en el visor**

Compilar con `Batería → Compilar APK`, instalar, y jugar. El visor importa porque es donde el
golpe tiene velocidad real de mano.

- [ ] **Step 5: Commit de la escena**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scenes/Cap04_Pad.unity Assets/Audio/Pruebas/Beatmap_Demo.asset \
        Assets/Audio/Pruebas/Beatmap_Demo.asset.meta
git commit -m "feat(ritmo): juego de ritmo montado sobre la escena del kit

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Resumen de verificación

| Qué | Cómo | Quién |
|---|---|---|
| `HitJudge`, 7 pruebas | EditMode, sin audio | Agente, en batchmode |
| `NoteMatcher`, 6 pruebas | EditMode, sin audio | Agente |
| Compilación limpia | 79 de 79, cero errores y cero avisos | Agente |
| Notas que caen | Play en el editor | Misael |
| Golpe juzgado y contado | Play en el editor | Misael |
| Con velocidad real de mano | Build APK y jugar | Misael, con el Quest |

## Qué NO cubre este plan

Niveles de dificultad, combo, pausa y reanudación, pantalla de resultados y modo libre: los
recortó la respuesta al riesgo R14.

Tampoco la rampa de tempo del iso-principio: la interfaz del reloj la admite, y no hace falta
para la demostración.

El beatmap sobre música real espera a que el área de música entregue pista, BPM exacto y
estructura. El metrónomo basta para demostrar el mecanismo completo.
