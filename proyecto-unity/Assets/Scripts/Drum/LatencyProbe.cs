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
