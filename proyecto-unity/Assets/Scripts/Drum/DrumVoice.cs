using UnityEngine;

/// Pool de AudioSource con agendado en el reloj DSP.
/// Cero asignaciones en el camino del golpe: el recolector de basura produce caídas de frame,
/// y una caída de frame es latencia.
public sealed class DrumVoice : DrumHitSink
{
    [SerializeField] AudioClip clip;

    [SerializeField, Min(1), Tooltip("Voces simultáneas. Dimensionar al peor redoble esperado: " +
                                     "cuando se agotan, la voz más vieja se corta a media cola.")]
    int voices = 8;

    [SerializeField] AnimationCurve velocityToGain =
        AnimationCurve.Linear(0.4f, 0.2f, 6f, 1f);

    AudioSource[] pool;
    int next;

    void Awake()
    {
        if (clip == null)
            Debug.LogError($"[DrumVoice] '{name}' no tiene AudioClip. Los golpes se van a " +
                           "detectar y no va a sonar nada.", this);

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
