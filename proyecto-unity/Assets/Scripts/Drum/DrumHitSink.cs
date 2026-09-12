using UnityEngine;

/// Receptor de golpes. Clase abstracta y no interfaz, para poder asignarla desde el inspector:
/// Unity no serializa referencias a interfaces en campos de MonoBehaviour.
public abstract class DrumHitSink : MonoBehaviour
{
    public abstract void Handle(in DrumHit hit);
}
