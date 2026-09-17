using UnityEngine;

/// Pool de AudioSource con agendado en el reloj DSP, dinámica timbral y round-robin.
///
/// Cero asignaciones en el camino del golpe: el recolector de basura produce caídas de frame,
/// y una caída de frame es latencia — medida, no supuesta: sin la predicción del plano armado
/// el jitter se triplica por cuantización de frame.
public sealed class DrumVoice : DrumHitSink
{
    [Header("Fuente de sonido")]
    [SerializeField, Tooltip("Pieza del kit con sus muestras ordenadas por brillo. " +
                             "Si se deja vacía se usa el clip suelto de abajo.")]
    DrumKitPiece pieza;

    [SerializeField, Tooltip("Respaldo de una sola muestra. Es lo que usa Cap04_Pad, la escena " +
                             "con la que se midió el hito de latencia: no tocar sin motivo.")]
    AudioClip clip;

    [Header("Voces")]
    [SerializeField, Min(1), Tooltip("Voces simultáneas. Dimensionar al peor redoble esperado: " +
                                     "cuando se agotan, la voz más vieja se corta a media cola.")]
    int voices = 8;

    [Header("Respuesta a la velocidad")]
    [SerializeField, Tooltip("Velocidad del golpe en m/s -> ganancia.")]
    AnimationCurve velocityToGain = AnimationCurve.Linear(0.4f, 0.2f, 6f, 1f);

    [SerializeField, Tooltip("Velocidad del golpe en m/s -> posición en el eje de brillo. " +
                             "0 es la muestra más opaca, 1 la más brillante. Un golpe suave " +
                             "debe sonar opaco, no solo bajo.")]
    AnimationCurve velocityToBrillo = AnimationCurve.Linear(0.4f, 0f, 6f, 1f);

    [SerializeField, Tooltip("Cuántas muestras a cada lado del centro entran en el sorteo. " +
                             "Sube si suena repetitivo, baja si la dinámica se difumina.")]
    int ventanaRoundRobin = 1;

    AudioSource[] pool;
    int next;
    int ultimoIndice = -1;

    void Awake()
    {
        bool hayPieza = pieza != null && pieza.Cuenta > 0;
        if (!hayPieza && clip == null)
            Debug.LogError($"[DrumVoice] '{name}' no tiene ni pieza ni AudioClip. Los golpes se " +
                           "van a detectar y no va a sonar nada.", this);

        pool = new AudioSource[voices];
        for (int i = 0; i < voices; i++)
        {
            // AddComponent en Awake, nunca en runtime.
            var src = gameObject.AddComponent<AudioSource>();
            src.clip                  = hayPieza ? null : clip;
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

        float ganancia = Mathf.Clamp01(velocityToGain.Evaluate(hit.Velocity));

        if (pieza != null && pieza.Cuenta > 0)
        {
            int i = SampleSelector.Elegir(
                pieza.Cuenta,
                velocityToBrillo.Evaluate(hit.Velocity),
                ultimoIndice,
                ventanaRoundRobin,
                pieza.TieneEjeTimbral,
                Random.value);

            if (i < 0) return;
            ultimoIndice = i;

            var m = pieza.muestras[i];
            src.clip   = m.clip;
            src.volume = Mathf.Clamp01(ganancia * m.ganancia);
        }
        else
        {
            src.clip   = clip;
            src.volume = ganancia;
        }

        if (src.clip == null) return;

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
