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
