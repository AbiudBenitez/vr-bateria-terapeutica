using UnityEngine;
using UnityEngine.XR;

/// Contrato entre la detección de golpe y sus consumidores.
/// Struct de solo lectura: se pasa con 'in' para evitar copias en el camino caliente.
public readonly struct DrumHit
{
    public readonly DrumPad Pad;
    public readonly float   Velocity;    // m/s sobre la normal del pad, siempre positiva
    public readonly double  ImpactDsp;   // instante estimado del impacto, reloj DSP
    public readonly Vector3 Point;
    public readonly XRNode  Hand;

    public DrumHit(DrumPad pad, float velocity, double impactDsp, Vector3 point, XRNode hand)
    {
        Pad       = pad;
        Velocity  = velocity;
        ImpactDsp = impactDsp;
        Point     = point;
        Hand      = hand;
    }
}
