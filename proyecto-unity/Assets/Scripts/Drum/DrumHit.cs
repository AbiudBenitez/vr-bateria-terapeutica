using UnityEngine;
using UnityEngine.XR;

/// Contrato entre la detección de golpe y sus consumidores.
///
/// Lleva el pad —que ES la identidad del instrumento—, la velocidad continua y el nivel
/// discreto 1-3. El entregable del 21-sep exige "instrumento, intensidad y momento": los tres
/// están aquí.
/// Struct de solo lectura: se pasa con 'in' para evitar copias en el camino caliente.
public readonly struct DrumHit
{
    public readonly DrumPad Pad;
    public readonly float   Velocity;    // m/s sobre la normal del pad, siempre positiva
    public readonly int     Intensidad;  // 1 suave, 2 medio, 3 fuerte
    public readonly double  ImpactDsp;   // instante estimado del impacto, reloj DSP
    public readonly Vector3 Point;
    public readonly XRNode  Hand;

    public DrumHit(DrumPad pad, float velocity, double impactDsp, Vector3 point, XRNode hand,
                   int intensidad = HitIntensity.Medio)
    {
        Pad        = pad;
        Intensidad = intensidad;
        Velocity  = velocity;
        ImpactDsp = impactDsp;
        Point     = point;
        Hand      = hand;
    }
}
