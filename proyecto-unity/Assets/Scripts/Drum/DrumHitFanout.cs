using UnityEngine;

/// Reparte cada golpe a varios receptores. Es el sink de producción:
/// StickTracker apunta aquí, y de aquí salen audio, háptico y sonda de latencia.
public sealed class DrumHitFanout : DrumHitSink
{
    [SerializeField] DrumHitSink[] targets;

    /// Un fanout sin destinos detecta los golpes y los tira a la basura: ni audio, ni háptico,
    /// ni métricas, y ni un solo mensaje en consola. El síntoma —"golpeo y no suena nada"— no
    /// se parece a la causa, así que la mala configuración tiene que gritar al arrancar.
    void Awake()
    {
        if (targets == null || targets.Length == 0)
        {
            Debug.LogError($"[DrumHitFanout] '{name}' no tiene destinos. Los golpes se van a " +
                           "detectar y descartar en silencio. Arrastra al array Targets el " +
                           "DrumVoice, el HapticSink y el LatencyProbe.", this);
            return;
        }

        for (int i = 0; i < targets.Length; i++)
        {
            if (targets[i] == null)
                Debug.LogError($"[DrumHitFanout] '{name}': el destino {i} está vacío.", this);
            else if (ReferenceEquals(targets[i], this))
                Debug.LogError($"[DrumHitFanout] '{name}' se apunta a sí mismo en el destino {i}. " +
                               "Eso es recursión infinita al primer golpe.", this);
        }
    }

    public override void Handle(in DrumHit hit)
    {
        if (targets == null) return;
        for (int i = 0; i < targets.Length; i++)
            if (targets[i] != null) targets[i].Handle(in hit);
    }

    /// Solo para pruebas EditMode: el inspector no existe fuera del editor.
    public void SetTargetsForTests(DrumHitSink[] t) => targets = t;
}
