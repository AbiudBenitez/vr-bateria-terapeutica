# Métricas de sesión — Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development
> (recomendado) o superpowers:executing-plans para ejecutar este plan tarea por tarea. Los pasos
> usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Goal:** Exportar por sesión la precisión temporal y las dos constancias del pulso, para
cerrar la medida de éxito 9 de la carta del patrocinador.

**Architecture:** `SessionStats` es una clase pura con dos funciones —estadísticas de los
desfases y constancia de los intervalos— probables sin Unity. `Scoreboard` acumula los desfases
y los instantes de golpe en arreglos reservados en `Awake`, y vuelca un JSON al cerrar la
aplicación siguiendo el patrón de `LatencyProbe`.

**Tech Stack:** Unity 6000.5.10f1 · C# · NUnit (EditMode) · `JsonUtility`

**Spec:** `docs/superpowers/specs/2026-10-18-metricas-de-sesion-design.md`

**Proyecto Unity:** `/Users/abiudbenitez/Documents/code/Unity/BateriaVR`

---

## Mapa de archivos

| Archivo | Responsabilidad |
|---|---|
| `Assets/Scripts/Drum/SessionStats.cs` | Clase pura: estadísticas de desfases y constancia de intervalos |
| `Assets/Scripts/Drum/Scoreboard.cs` | Acumula los datos y vuelca el JSON |
| `Assets/Tests/EditMode/SessionStatsTests.cs` | 8 pruebas de la clase pura |

**Por qué dos funciones puras y no una:** las estadísticas de los desfases y la constancia de
los intervalos consumen datos distintos —unos miden contra la rejilla, otros contra el golpe
anterior— y responden preguntas distintas. Juntarlas en una función obligaría a pasar dos
arreglos siempre, incluso cuando solo interesa uno.

**Convenciones del proyecto que hay que respetar:**
- Comentarios en español explicando el **porqué**, no el qué.
- **Cero asignaciones en el camino del golpe.** Los arreglos se reservan en `Awake`.
- `AudioSettings.dspTime` se lee una sola vez por frame.
- Las clases puras no heredan de `MonoBehaviour`.
- El volcado se protege contra el doble disparo de `OnApplicationPause` y `OnApplicationQuit`.

---

### Task 1: `SessionStats` — estadísticas de los desfases

**Files:**
- Create: `Assets/Scripts/Drum/SessionStats.cs`
- Create: `Assets/Tests/EditMode/SessionStatsTests.cs`

- [ ] **Step 1: Escribir las pruebas que fallan**

Crear `Assets/Tests/EditMode/SessionStatsTests.cs`:

```csharp
using NUnit.Framework;

/// Las métricas de sesión son aritmética sobre dos listas de números. No saben de audio, de
/// escena ni de reloj, y por eso se prueban sin nada de eso.
public class SessionStatsTests
{
    const double Tol = 1e-6;

    [Test]
    public void CalculaMediaMedianaYExtremos()
    {
        // Cinco desfases conocidos: media 6, mediana 5, min -2, max 20.
        var d = new[] { 5.0, -2.0, 20.0, 3.0, 4.0 };
        var r = SessionStats.Calcular(d, d.Length);

        Assert.AreEqual(5, r.n);
        Assert.AreEqual(6.0, r.mediaMs, Tol);
        Assert.AreEqual(4.0, r.medianaMs, Tol);
        Assert.AreEqual(-2.0, r.minMs, Tol);
        Assert.AreEqual(20.0, r.maxMs, Tol);
    }

    [Test]
    public void LaMedianaDeUnNumeroParDeValoresPromedia()
    {
        var d = new[] { 10.0, 20.0, 30.0, 40.0 };
        Assert.AreEqual(25.0, SessionStats.Calcular(d, d.Length).medianaMs, Tol);
    }

    [Test]
    public void ValoresIdenticosDanDesviacionCero()
    {
        // Es el caso perfecto, no un error: tocar siempre con el mismo desfase.
        var d = new[] { 7.0, 7.0, 7.0, 7.0 };
        var r = SessionStats.Calcular(d, d.Length);

        Assert.AreEqual(0.0, r.desviacionMs, Tol);
        Assert.AreEqual(7.0, r.mediaMs, Tol);
    }

    [Test]
    public void UnaListaVaciaDevuelveCerosYNoRevienta()
    {
        // Una sesión sin golpes es un caso real: el usuario se pone el visor y se lo quita.
        var r = SessionStats.Calcular(new double[0], 0);

        Assert.AreEqual(0, r.n);
        Assert.AreEqual(0.0, r.mediaMs, Tol);
        Assert.AreEqual(0.0, r.desviacionMs, Tol);
    }

    [Test]
    public void SoloSeUsanLosPrimerosNElementos()
    {
        // El arreglo se reserva entero en Awake pero solo se llena en parte: el resto son
        // ceros que NO deben entrar en la estadística.
        var d = new double[100];
        d[0] = 10.0; d[1] = 20.0; d[2] = 30.0;

        var r = SessionStats.Calcular(d, 3);
        Assert.AreEqual(3, r.n);
        Assert.AreEqual(20.0, r.mediaMs, Tol);
    }

    [Test]
    public void ElPercentil90DejaElDiezPorCientoPeorFuera()
    {
        var d = new double[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 100 };
        var r = SessionStats.Calcular(d, d.Length);

        // El p90 por interpolación sobre diez valores cae entre el 9 y el 100.
        Assert.Greater(r.p90Ms, 9.0);
        Assert.Less(r.p90Ms, 100.0);
    }

    [Test]
    public void UnSoloGolpeNoProduceConstanciaDePulso()
    {
        // La constancia se mide sobre intervalos, y un intervalo necesita dos golpes.
        var t = new[] { 1.0 };
        Assert.AreEqual(0.0, SessionStats.ConstanciaPulsoMs(t, 1), Tol);
        Assert.AreEqual(0.0, SessionStats.ConstanciaPulsoMs(new double[0], 0), Tol);
    }

    [Test]
    public void LaConstanciaDePulsoIgnoraElDesfaseConstante()
    {
        // ESTA es la prueba que separa las dos métricas del diseño.
        //
        // Golpes cada 0.5 s exactos, pero todos 30 ms tarde respecto de la rejilla. Contra la
        // rejilla la desviación es alta; el pulso propio es perfecto. Si alguien implementara
        // las dos métricas igual, esta prueba lo detecta.
        var instantes = new[] { 10.03, 10.53, 11.03, 11.53, 12.03 };
        Assert.AreEqual(0.0, SessionStats.ConstanciaPulsoMs(instantes, instantes.Length), 1e-3,
            "Un pulso perfectamente regular debe dar constancia cero, por muy atrasado que vaya.");

        var desfases = new[] { 30.0, 30.0, 30.0, 30.0, 30.0 };
        Assert.AreEqual(30.0, SessionStats.Calcular(desfases, desfases.Length).mediaMs, Tol,
            "La media contra la rejilla sí debe recoger el atraso constante.");
    }

    [Test]
    public void UnPulsoIrregularDaConstanciaAlta()
    {
        // Intervalos de 0.4, 0.6, 0.4 y 0.6 segundos: media 0.5 con desviación de 100 ms.
        var instantes = new[] { 0.0, 0.4, 1.0, 1.4, 2.0 };
        double c = SessionStats.ConstanciaPulsoMs(instantes, instantes.Length);

        Assert.AreEqual(100.0, c, 1.0,
            "Intervalos alternando 400 y 600 ms deben dar unos 100 ms de desviación.");
    }
}
```

- [ ] **Step 2: Correr para verificar que fallan**

Con Unity cerrado:

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/ss.xml -logFile /tmp/ss.log 2>&1
grep -c "error CS" /tmp/ss.log
```

Expected: error de compilación, `The name 'SessionStats' does not exist in the current context`.

- [ ] **Step 3: Implementar**

Crear `Assets/Scripts/Drum/SessionStats.cs`:

```csharp
using System;

/// Estadísticas de una sesión de juego.
///
/// Dos funciones separadas a propósito, porque miden cosas distintas:
///
///   Calcular()          trabaja sobre los DESFASES contra la rejilla del beatmap, y dice qué
///                       tan parejo se pega el usuario al patrón.
///   ConstanciaPulsoMs() trabaja sobre los INTERVALOS entre golpes consecutivos, y dice qué
///                       tan estable es su pulso propio.
///
/// No son lo mismo: se puede ir treinta milisegundos atrasado todo el tiempo y tener un pulso
/// perfectamente estable. La primera lo castigaría y la segunda no.
public static class SessionStats
{
    [Serializable]
    public struct Resumen
    {
        public int n;
        public double mediaMs;
        public double medianaMs;
        public double p90Ms;
        public double desviacionMs;
        public double minMs;
        public double maxMs;
    }

    /// Estadísticas de los primeros `n` elementos de `desfasesMs`.
    ///
    /// Se pasa `n` aparte porque el arreglo se reserva entero en Awake y solo se llena en
    /// parte: los ceros del final no son golpes y no deben entrar en la media.
    public static Resumen Calcular(double[] desfasesMs, int n)
    {
        var r = new Resumen();
        if (desfasesMs == null || n <= 0) return r;   // sesión sin golpes: ceros, no excepción
        if (n > desfasesMs.Length) n = desfasesMs.Length;

        r.n = n;

        var orden = new double[n];
        Array.Copy(desfasesMs, orden, n);
        Array.Sort(orden);

        r.minMs = orden[0];
        r.maxMs = orden[n - 1];

        double suma = 0.0;
        for (int i = 0; i < n; i++) suma += orden[i];
        r.mediaMs = suma / n;

        r.medianaMs = n % 2 == 1
            ? orden[n / 2]
            : 0.5 * (orden[n / 2 - 1] + orden[n / 2]);

        r.p90Ms = Percentil(orden, 90.0);

        double acum = 0.0;
        for (int i = 0; i < n; i++)
        {
            double d = orden[i] - r.mediaMs;
            acum += d * d;
        }
        // Desviación de la población, no muestral: se describe la sesión entera, no se infiere
        // de una muestra sobre algo mayor.
        r.desviacionMs = Math.Sqrt(acum / n);

        return r;
    }

    /// Desviación típica de los intervalos entre golpes consecutivos, en milisegundos.
    ///
    /// `instantesDsp` son los instantes de impacto en segundos del reloj DSP, en el orden en
    /// que ocurrieron. Devuelve 0 si no hay al menos dos golpes: un intervalo necesita dos.
    public static double ConstanciaPulsoMs(double[] instantesDsp, int n)
    {
        if (instantesDsp == null || n < 2) return 0.0;
        if (n > instantesDsp.Length) n = instantesDsp.Length;

        int cuantos = n - 1;
        double suma = 0.0;
        for (int i = 1; i < n; i++) suma += instantesDsp[i] - instantesDsp[i - 1];
        double media = suma / cuantos;

        double acum = 0.0;
        for (int i = 1; i < n; i++)
        {
            double d = (instantesDsp[i] - instantesDsp[i - 1]) - media;
            acum += d * d;
        }
        return Math.Sqrt(acum / cuantos) * 1000.0;
    }

    /// Percentil por interpolación lineal sobre un arreglo YA ORDENADO.
    static double Percentil(double[] ordenado, double p)
    {
        int n = ordenado.Length;
        if (n == 0) return 0.0;
        if (n == 1) return ordenado[0];

        double pos = (p / 100.0) * (n - 1);
        int bajo = (int)Math.Floor(pos);
        int alto = (int)Math.Ceiling(pos);
        if (bajo == alto) return ordenado[bajo];

        double frac = pos - bajo;
        return ordenado[bajo] * (1.0 - frac) + ordenado[alto] * frac;
    }
}
```

- [ ] **Step 4: Correr para verificar que pasan**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/ss2.xml -logFile /tmp/ss2.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/ss2.log',errors='ignore').read()
print('errores:',len(re.findall(r'error CS\d+',L)),' avisos:',len({m for m in re.findall(r'warning CS\d+',L)}))
r=ET.parse('/tmp/ss2.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')} fallidas {r.get('failed')}\")
for tc in r.iter('test-case'):
    if tc.get('result')!='Passed':
        print('FALLA',tc.get('name'))
        m=tc.find('.//message')
        if m is not None and m.text: print('  ',m.text.strip().splitlines()[0][:130])"
```

Expected: 0 errores, **88 de 88** pasadas (79 previas + 9 nuevas), 0 fallidas.

- [ ] **Step 5: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/SessionStats.cs Assets/Scripts/Drum/SessionStats.cs.meta \
        Assets/Tests/EditMode/SessionStatsTests.cs Assets/Tests/EditMode/SessionStatsTests.cs.meta
git commit -m "feat(metricas): estadisticas de sesion

Dos funciones separadas porque miden cosas distintas. Calcular trabaja sobre los desfases
contra la rejilla del beatmap y dice que tan parejo se pega el usuario al patron;
ConstanciaPulsoMs trabaja sobre los intervalos entre golpes y dice que tan estable es su pulso
propio.

No son lo mismo: se puede ir treinta milisegundos atrasado todo el tiempo y tener un pulso
perfectamente estable. Hay una prueba que lo verifica, y es la que impide que alguien las
implemente iguales sin que nadie lo note.

Se pasa n aparte del arreglo porque este se reserva entero en Awake y solo se llena en parte:
los ceros del final no son golpes y no deben entrar en la media.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: El `Scoreboard` acumula y vuelca

**Files:**
- Modify: `Assets/Scripts/Drum/Scoreboard.cs`

- [ ] **Step 1: Añadir los campos de acumulación**

En `Assets/Scripts/Drum/Scoreboard.cs`, después del bloque de campos serializados y antes de
`int perfect, good, miss;`, insertar:

```csharp
    [Header("Métricas de sesión")]
    [SerializeField, Min(16), Tooltip("Golpes que caben sin que los arreglos tengan que " +
                                      "crecer. Una realocación en mitad de la canción produce " +
                                      "una caída de frame, y una caída de frame es latencia.")]
    int capacidadGolpes = 1024;

    [SerializeField, Tooltip("Si se desmarca, no se escribe el archivo de métricas. Útil para " +
                             "sesiones de prueba que no deben ensuciar los datos.")]
    bool exportarMetricas = true;

    // Se reservan en Awake y no vuelven a crecer.
    double[] desfases;
    double[] instantes;
    int golpes;
```

- [ ] **Step 2: Reservar los arreglos en `Awake`**

En el mismo archivo, dentro de `void Awake()`, justo después de `sb = new StringBuilder(160);`,
insertar:

```csharp
        // Toda la memoria de las métricas se reserva aquí. A partir de este punto, Handle no
        // asigna: escribir en un arreglo ya reservado no pasa por el recolector de basura.
        desfases  = new double[capacidadGolpes];
        instantes = new double[capacidadGolpes];
```

- [ ] **Step 3: Acumular en `Handle`**

En `public override void Handle(in DrumHit hit)`, sustituir estas tres líneas:

```csharp
        ultimoDesfaseMs = desfaseMs;
        huboGolpe = true;
        sucio = true;
```

por:

```csharp
        // Si se desborda la capacidad se deja de registrar en lugar de realocar: perder una
        // muestra de diagnóstico es preferible a falsear la medición con un tirón del
        // recolector de basura justo en el camino del golpe.
        if (golpes < desfases.Length)
        {
            desfases[golpes]  = desfaseMs;
            instantes[golpes] = hit.ImpactDsp;
            golpes++;
        }

        ultimoDesfaseMs = desfaseMs;
        huboGolpe = true;
        sucio = true;
```

- [ ] **Step 4: Añadir el volcado al final de la clase**

En el mismo archivo, justo antes de la llave de cierre de la clase, insertar:

```csharp
    // ---------------------------------------------------------------- métricas de sesión

    [Serializable]
    class Conteo
    {
        public int total;
        public int perfect;
        public int good;
        public int miss;
    }

    [Serializable]
    class Volcado
    {
        public string sesion;
        public double bpm;
        public Conteo notas = new();
        public int aciertos;
        public float precisionPorcentaje;
        public SessionStats.Resumen precisionTemporal;
        public double constanciaPulsoMs;
        public double[] desfases;
    }

    /// Cuántos golpes se han escrito ya a disco.
    ///
    /// OnApplicationPause(true) y OnApplicationQuit se disparan los DOS al cerrar la
    /// aplicación, con un segundo de diferencia, y cada uno producía un archivo. Quedaban
    /// pares de volcados idénticos con nombres distintos y al revisarlos había que adivinar
    /// cuál era cuál. Es la misma guarda que lleva LatencyProbe.
    int golpesVolcados;

    void OnApplicationPause(bool pausada) { if (pausada) Volcar(); }
    void OnApplicationQuit() => Volcar();

    void Volcar()
    {
        if (!exportarMetricas) return;
        if (golpes <= golpesVolcados && golpes > 0) return;

        var v = new Volcado
        {
            sesion = System.DateTime.Now.ToString("s"),
            bpm = reloj != null && reloj.Tempo != null ? reloj.Tempo.BpmEn(0.0) : 0.0,
            aciertos = perfect + good,
            precisionPorcentaje = Precision,
            precisionTemporal = SessionStats.Calcular(desfases, golpes),
            constanciaPulsoMs = SessionStats.ConstanciaPulsoMs(instantes, golpes),
        };
        v.notas.total   = perfect + good + miss;
        v.notas.perfect = perfect;
        v.notas.good    = good;
        v.notas.miss    = miss;

        // Los desfases crudos van además del resumen. Un informe que solo lleva promedios no
        // se puede reanalizar: con los datos en bruto se pueden hacer gráficas o recalcular
        // si cambia el criterio.
        v.desfases = new double[golpes];
        System.Array.Copy(desfases, v.desfases, golpes);

        string ruta = Path.Combine(Application.persistentDataPath,
            $"sesion_{System.DateTime.Now:yyyyMMdd_HHmmss}.json");
        File.WriteAllText(ruta, JsonUtility.ToJson(v, true));
        golpesVolcados = golpes;

        Debug.Log($"[Scoreboard] Sesión volcada: {golpes} golpes, " +
                  $"precisión {Precision:F0} %, " +
                  $"constancia {v.constanciaPulsoMs:F1} ms -> {ruta}", this);
    }
```

- [ ] **Step 5: Añadir los `using` que faltan**

En la cabecera del archivo, sustituir:

```csharp
using System.Text;
using TMPro;
using UnityEngine;
```

por:

```csharp
using System;
using System.IO;
using System.Text;
using TMPro;
using UnityEngine;
```

- [ ] **Step 6: Verificar que compila y las pruebas siguen verdes**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
/Applications/Unity/Hub/Editor/6000.5.10f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -runTests -testPlatform EditMode -projectPath "$PWD" \
  -testResults /tmp/sc.xml -logFile /tmp/sc.log 2>&1
python3 -c "
import re,xml.etree.ElementTree as ET
L=open('/tmp/sc.log',errors='ignore').read()
e=re.findall(r'error CS\d+[^\n]*',L)
print('errores:',len(e),' avisos:',len({m for m in re.findall(r'warning CS\d+',L)}))
for l in e[:5]: print('  ',l[:130])
r=ET.parse('/tmp/sc.xml').getroot()
print(f\"pruebas: {r.get('passed')}/{r.get('total')}\")"
```

Expected: 0 errores, 0 avisos, 88 de 88 pasadas.

- [ ] **Step 7: Commit**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
git add Assets/Scripts/Drum/Scoreboard.cs
git commit -m "feat(metricas): exportar las metricas de sesion a JSON

Cierra DM.1 y con ella la medida de exito 9, que estaba en cero.

El marcador ya calculaba el desfase de cada golpe y lo descartaba en cuanto lo pintaba en
pantalla. Ahora lo guarda, junto con el instante del impacto, en arreglos reservados en Awake:
escribir en un arreglo ya reservado no pasa por el recolector de basura, y una caida de frame
en el camino del golpe es latencia.

Si se desborda la capacidad se deja de registrar en lugar de realocar. Perder una muestra de
diagnostico es preferible a falsear la medicion con un tiron del recolector.

El archivo lleva los desfases CRUDOS ademas del resumen: un informe que solo lleva promedios no
se puede reanalizar.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: Verificar en el visor

Esta tarea la ejecuta Misael. No puede automatizarse: el archivo se escribe al cerrar la
aplicación.

- [ ] **Step 1: Probar en el editor**

Abrir `Assets/Scenes/Cap04_Pad.unity`, entrar en play, tocar unos veinte golpes, y salir de
play.

La consola debe mostrar:

```
[Scoreboard] Sesión volcada: 20 golpes, precisión 85 %, constancia 24.3 ms -> /Users/.../sesion_20261018_143210.json
```

Abrir ese archivo y comprobar que lleva las tres cosas: el conteo de notas, el bloque
`precisionTemporal` y el arreglo `desfases` con tantos elementos como golpes.

- [ ] **Step 2: Compilar e instalar en el visor**

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
# Con Unity abierto: Batería → Compilar APK
./scripts/quest.sh install
```

- [ ] **Step 3: Jugar una sesión completa y bajar el archivo**

Jugar los 32 segundos del beatmap de demostración, **cerrar la aplicación desde el menú del
visor** —el archivo se escribe al cerrar, no al terminar la canción— y después:

```bash
cd /Users/abiudbenitez/Documents/code/Unity/BateriaVR
./scripts/quest.sh pull
ls -lt mediciones/files/sesion_*.json | head -3
python3 -m json.tool "$(ls -t mediciones/files/sesion_*.json | head -1)"
```

**Criterios de aceptación:**

1. El archivo existe y es JSON válido.
2. `notas.total` coincide con las notas que tuvo la canción.
3. `desfases` tiene tantos elementos como golpes acertados.
4. `precisionTemporal.mediaMs` está en el orden de unas pocas decenas de milisegundos.
5. `constanciaPulsoMs` es mayor que cero si se tocó de forma irregular.

- [ ] **Step 4: Commit de la evidencia**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
mkdir -p entregables/mediciones
cp /Users/abiudbenitez/Documents/code/Unity/BateriaVR/mediciones/files/sesion_*.json \
   entregables/mediciones/
git add entregables/mediciones/
git commit -m "docs: evidencia de la medida 9, metricas de sesion exportadas

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: Registrar el avance

**Files:**
- Modify: `scripts/recorte.py`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Marcar `DM.1` como hecha**

En `scripts/recorte.py`, sustituir el bloque `NUEVAS` por:

```python
# Actividad que NO existía en el plan original y se añadió con el recorte.
#
# Es el único sitio donde aquel recorte sumó alcance, y la razón era la desproporción: el
# marcador del juego de ritmo ya calculaba precisión temporal y constancia, así que volcarlas
# a un archivo cerraba la medida 9, que estaba en cero.
#
# TERMINADA el 18-oct-2026. La amplitud de movimiento que la medida nombraba queda fuera: el
# equipo retiró el marco de rehabilitación motriz antes del corte de medio curso, y sin ese
# marco la amplitud mide algo que el proyecto ya no declara.
NUEVAS = {
    "DM.1": (9, "Exportar las métricas de sesión a JSON: precisión temporal y constancia"),
}

NUEVAS_HECHAS = {"DM.1"}
```

- [ ] **Step 2: Verificar que las pruebas del recorte siguen pasando**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python -m pytest scripts/test_recorte.py -q 2>&1 | tail -3
```

Expected: 8 pruebas pasadas. `NUEVAS_HECHAS` es un conjunto nuevo que ninguna prueba examina,
así que no debe romper nada.

- [ ] **Step 3: Añadir la sección a `CLAUDE.md`**

Añadir antes de `## Tareas de clase entregadas`:

```markdown
## Métricas de sesión — 18-oct-2026

`DM.1` terminada. Cierra la **medida de éxito 9**, que estaba en cero.

| | |
|---|---|
| Spec | `docs/superpowers/specs/2026-10-18-metricas-de-sesion-design.md` |
| Plan | `docs/superpowers/plans/2026-10-18-metricas-de-sesion.md` |
| Código | `SessionStats.cs` · volcado en `Scoreboard.cs` |
| Evidencia | `entregables/mediciones/sesion_*.json` |

### Dos constancias, no una

- **Contra la rejilla** — desviación típica de los desfases. Qué tan parejo se pega al patrón.
- **Propia** — desviación típica de los intervalos entre golpes. Qué tan estable es su pulso.

**Se puede ir 30 ms atrasado todo el tiempo y tener un pulso perfectamente estable.** Hay una
prueba que lo verifica, y es la que impide que alguien las implemente iguales sin que nadie
lo note.

### La amplitud de movimiento queda fuera

La medida 9 la nombraba, pero es un dato de rehabilitación de miembro superior. El equipo
retiró ese marco antes del corte de medio curso, y sin él la amplitud mide algo que el
proyecto ya no declara. Las dos métricas rítmicas **no necesitan respaldo clínico**: medir si
alguien toca a tiempo es una observación de ejecución musical.

### El archivo lleva los datos crudos

Además del resumen va el arreglo completo de desfases. Un informe que solo lleva promedios no
se puede reanalizar, y el informe final (`QI.1`) va a necesitar gráficas.
```

- [ ] **Step 4: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add scripts/recorte.py CLAUDE.md
git commit -m "docs: DM.1 terminada, medida 9 cerrada

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Resumen de verificación

| Qué | Cómo | Quién |
|---|---|---|
| `SessionStats`, 9 pruebas | EditMode, sin audio | Agente, en batchmode |
| Las dos constancias miden distinto | `LaConstanciaDePulsoIgnoraElDesfaseConstante` | Agente |
| Compilación limpia | 88 de 88, cero errores y cero avisos | Agente |
| El archivo se escribe y es válido | Play en el editor, revisar el JSON | Misael |
| Los números son plausibles | Sesión completa en el visor | Misael, con el Quest |

## Qué NO cubre este plan

**La amplitud de movimiento.** Fuera de alcance por el retiro del marco clínico.

**Mostrar las métricas dentro del visor.** La pantalla de resultados es `II.6`, del área de
interfaz. Este plan produce el archivo.

**El análisis de los archivos.** Forma parte del informe final (`QI.1`), del área de QA.

**La deuda documental del cambio de enfoque.** Ocho documentos afirman el marco motriz y la
decisión de retirarlo es anterior al corte de medio curso. Necesita su propio documento, y no
es este.
