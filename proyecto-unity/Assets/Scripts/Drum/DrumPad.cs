using UnityEngine;

/// Pad de percusión definido por un plano.
/// El plano de golpe pasa por transform.position con normal transform.up.
/// El plano armado está desplazado armDistance metros a lo largo de la normal.
[DisallowMultipleComponent]
public sealed class DrumPad : MonoBehaviour
{
    [Header("Geometría")]
    [SerializeField, Tooltip("Radio útil del pad, en metros.")]
    float radius = 0.15f;

    [SerializeField, Tooltip("Distancia del plano armado por delante de la superficie, en metros.")]
    float armDistance = 0.06f;

    [Header("Umbral")]
    [SerializeField, Tooltip("Velocidad normal mínima para contar como golpe, en m/s.")]
    float minVelocity = 0.4f;

    /// El radio útil del pad. WithinRadius() responde otra pregunta y no sirve para
    /// dimensionar el visual, que necesita el valor en sí.
    public float   Radius      => radius;
    public float   ArmDistance => armDistance;
    public float   MinVelocity => minVelocity;
    public Vector3 Normal      => transform.up;
    public Vector3 Center      => transform.position;

    /// Distancia con signo al plano armado. Positiva = del lado del jugador.
    public float SignedDistanceToArmPlane(Vector3 worldPoint)
        => Vector3.Dot(worldPoint - (Center + Normal * armDistance), Normal);

    /// ¿El punto cae dentro del radio, una vez proyectado sobre el plano del pad?
    public bool WithinRadius(Vector3 worldPoint)
    {
        Vector3 flat = Vector3.ProjectOnPlane(worldPoint - Center, Normal);
        return flat.sqrMagnitude <= radius * radius;
    }

    void OnDrawGizmos()
    {
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(Center, radius);
        Gizmos.color = Color.cyan;                       // plano armado
        Gizmos.DrawWireSphere(Center + Normal * armDistance, radius);
        Gizmos.DrawLine(Center, Center + Normal * armDistance);
    }
}
