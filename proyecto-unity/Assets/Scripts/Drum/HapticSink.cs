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
