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

    [SerializeField, Tooltip("Golpes que caben sin que la lista tenga que crecer. Una realocación " +
                             "en mitad de la medición produce una caída de frame que contamina " +
                             "justo el dato que se está midiendo. 2000 cubre una sesión larga.")]
    int capacidadGolpes = 2000;

    static int lateSchedules;
    public static void CountLateSchedule() => lateSchedules++;

    readonly Volcado volcado = new();

    void Awake()
    {
        // Se reserva TODA la memoria aquí. A partir de este punto, Handle no asigna: List.Add
        // sobre una lista con capacidad suficiente solo escribe en el arreglo interno.
        volcado.registros.Capacity = capacidadGolpes;
        lateSchedules = 0;
    }

    public override void Handle(in DrumHit hit)
    {
        double now = AudioSettings.dspTime;

        // Si se desborda la capacidad reservada se deja de registrar en lugar de realocar:
        // perder una muestra de diagnóstico es preferible a falsear la medición con un
        // tirón del recolector de basura.
        if (volcado.registros.Count >= volcado.registros.Capacity) return;

        volcado.registros.Add(new Registro
        {
            dspImpacto   = hit.ImpactDsp,
            dspAhora     = now,
            velocidad    = hit.Velocity,
            agendaTardia = hit.ImpactDsp <= now,
        });
    }

    /// Cuántos registros se han escrito ya a disco.
    ///
    /// OnApplicationPause(true) y OnApplicationQuit se disparan los DOS al cerrar la app, con
    /// un segundo de diferencia, y cada uno producía un archivo. Quedaban pares de volcados
    /// idénticos con nombres distintos, y al revisarlos había que adivinar cuál era cuál.
    /// Se vuelca solo si hay golpes nuevos desde el último volcado.
    int registrosVolcados;

    void OnApplicationPause(bool paused) { if (paused) Dump(); }
    void OnApplicationQuit() => Dump();

    void Dump()
    {
        if (volcado.registros.Count <= registrosVolcados) return;

        volcado.totalGolpes    = volcado.registros.Count;
        volcado.agendasTardias = lateSchedules;

        string ruta = Path.Combine(Application.persistentDataPath,
            $"latencia_{System.DateTime.Now:yyyyMMdd_HHmmss}.json");
        File.WriteAllText(ruta, JsonUtility.ToJson(volcado, true));
        registrosVolcados = volcado.registros.Count;
        Debug.Log($"[LatencyProbe] {volcado.totalGolpes} golpes, " +
                  $"{volcado.agendasTardias} agendas tardías -> {ruta}");
    }
}
