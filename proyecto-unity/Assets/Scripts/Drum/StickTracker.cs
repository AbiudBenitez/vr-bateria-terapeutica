using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;

/// Sigue la punta de una baqueta y emite DrumHit al cruzar el plano armado de un pad.
/// La matemática vive en CrossSolver; esto lee hardware y orquesta.
public sealed class StickTracker : MonoBehaviour
{
    [SerializeField] XRNode      hand = XRNode.RightHand;
    [SerializeField] Transform   xrOrigin;    // el XR Origin de la escena
    [SerializeField] Transform   controller;  // GameObject con el TrackedPoseDriver de esta mano
    [SerializeField] Transform   tip;         // punta de la baqueta, hija de controller
    [SerializeField] DrumPad[]   pads;
    [SerializeField] DrumHitSink sink;

    [SerializeField, Tooltip("Margen del pre-filtro de proximidad, en metros. Solo se evalúa " +
                             "el plano de los pads que la punta tenga cerca.")]
    float margenProximidad = 0.15f;

    [SerializeField, Tooltip("Corrección constante entre el reloj de pose y el de audio, en segundos. " +
                             "Se determina midiendo, en el capítulo 6. No se adivina.")]
    float poseToAudioOffset = 0f;

    InputDevice device;
    Vector3     prevTip;
    double      prevDsp;
    bool        primed;

    readonly Dictionary<DrumPad, bool> armed = new();

    void Awake()
    {
        // Sin estas referencias el tracker no detecta nada y no dice por qué.
        if (xrOrigin == null)
            Debug.LogError($"[StickTracker] '{name}': falta xrOrigin. Sin él, la velocidad del " +
                           "control no se puede pasar a espacio de mundo.", this);
        if (controller == null)
            Debug.LogError($"[StickTracker] '{name}': falta controller.", this);
        if (tip == null)
            Debug.LogError($"[StickTracker] '{name}': falta tip, la punta de la baqueta.", this);
        if (sink == null)
            Debug.LogError($"[StickTracker] '{name}': falta sink. Los golpes no van a ninguna parte.", this);
        if (pads == null || pads.Length == 0)
            Debug.LogError($"[StickTracker] '{name}': el array Pads está vacío. No hay nada que golpear.", this);
        else
            for (int i = 0; i < pads.Length; i++)
                if (pads[i] == null)
                    Debug.LogError($"[StickTracker] '{name}': el pad {i} está vacío.", this);
    }

    void OnEnable()
    {
        device = InputDevices.GetDeviceAtXRNode(hand);
        primed = false;
        armed.Clear();
        foreach (var p in pads) armed[p] = true;
    }

    void Update()
    {
        if (!device.isValid)
        {
            device = InputDevices.GetDeviceAtXRNode(hand);
            if (!device.isValid) return;
        }

        // Lectura ÚNICA del reloj DSP por frame. Regla del proyecto: nunca Time.time.
        double  dspNow = AudioSettings.dspTime + poseToAudioOffset;
        Vector3 tipNow = tip.position;

        if (!primed)
        {
            prevTip = tipNow;
            prevDsp = dspNow;
            primed  = true;
            return;
        }

        Vector3 vTip = ReadTipVelocity();

        for (int i = 0; i < pads.Length; i++)
            Evaluate(pads[i], tipNow, vTip, dspNow);

        prevTip = tipNow;
        prevDsp = dspNow;
    }

    /// CUIDADO CON LOS ESPACIOS: deviceVelocity y deviceAngularVelocity vienen en el espacio del
    /// XR Origin, mientras que tip.position y pad.Normal están en mundo. Mezclarlos da magnitudes
    /// correctas con direcciones equivocadas en cuanto el jugador gira.
    Vector3 ReadTipVelocity()
    {
        device.TryGetFeatureValue(CommonUsages.deviceVelocity,        out Vector3 v);
        device.TryGetFeatureValue(CommonUsages.deviceAngularVelocity, out Vector3 w);

        return CrossSolver.TipVelocity(
            xrOrigin.TransformVector(v),
            xrOrigin.TransformVector(w),
            tip.position - controller.position);
    }

    void Evaluate(DrumPad pad, Vector3 tipNow, Vector3 vTip, double dspNow)
    {
        // Pre-filtro barato: con seis piezas y dos manos serían 12 pruebas de plano por frame.
        // Se descarta por DISTANCIA, no con un collider: un collider devolvería la física al
        // camino del golpe, que es exactamente lo que el capítulo 4 sacó de ahí.
        //
        // Se exige que AMBOS extremos del segmento estén lejos. Con solo comprobar la posición
        // actual, una baqueta rápida podría atravesar el pad entre frames y el filtro se lo
        // tragaría — el mismo tunelado que motivó no usar colliders.
        float alcance = pad.Radius + pad.ArmDistance + margenProximidad;
        float a2 = alcance * alcance;
        if ((tipNow - pad.Center).sqrMagnitude > a2 &&
            (prevTip - pad.Center).sqrMagnitude > a2)
        {
            armed[pad] = true;   // lejos del pad: queda rearmado para el próximo acercamiento
            return;
        }

        float dPrev = pad.SignedDistanceToArmPlane(prevTip);
        float dNow  = pad.SignedDistanceToArmPlane(tipNow);

        // Rearme POR POSICIÓN, no por tiempo: el pad revive cuando la baqueta vuelve a salir.
        // Un cooldown temporal destruiría los redobles.
        if (dNow > 0f && dPrev <= 0f) { armed[pad] = true; return; }

        if (!armed[pad]) return;
        if (!(dPrev > 0f && dNow <= 0f)) return;              // no cruzó hacia adentro

        float vNormal = CrossSolver.NormalSpeed(vTip, pad.Normal);
        if (vNormal < pad.MinVelocity) return;

        float   t01        = CrossSolver.Fraction(dPrev, dNow);
        Vector3 crossPoint = Vector3.Lerp(prevTip, tipNow, t01);
        if (!pad.WithinRadius(crossPoint)) return;

        double dspCross  = prevDsp + (dspNow - prevDsp) * t01;
        double dspImpact = CrossSolver.ImpactDsp(dspCross, pad.ArmDistance, vNormal);

        armed[pad] = false;
        sink.Handle(new DrumHit(pad, vNormal, dspImpact, crossPoint, hand,
                                pad.Intensidad(vNormal)));
    }
}
