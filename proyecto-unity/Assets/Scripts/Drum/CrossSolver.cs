using UnityEngine;

/// Matemática de la detección de golpe. Sin estado, sin MonoBehaviour, sin hardware:
/// todo lo que aquí vive se puede probar en EditMode sin visor.
public static class CrossSolver
{
    /// Fracción del intervalo entre frames en la que el punto cruzó el plano.
    /// dPrev debe ser positivo (antes del plano) y dNow negativo o cero (pasado el plano).
    public static float Fraction(float dPrev, float dNow)
    {
        float denom = dPrev - dNow;
        return Mathf.Approximately(denom, 0f) ? 0f : dPrev / denom;
    }

    /// Instante estimado del impacto: al cruce le falta recorrer armDistance a normalVelocity.
    /// Ésta es la predicción que compensa la latencia percibida.
    public static double ImpactDsp(double dspCross, float armDistance, float normalVelocity)
    {
        if (normalVelocity <= 0f) return dspCross;
        return dspCross + armDistance / normalVelocity;
    }

    /// Componente de la velocidad en dirección al pad, positiva si se acerca.
    public static float NormalSpeed(Vector3 velocityWorld, Vector3 padNormal)
        => -Vector3.Dot(velocityWorld, padNormal);

    /// Velocidad de la PUNTA, no del controlador: v_punta = v_dispositivo + ω × r.
    /// Con baqueta larga el giro de muñeca aporta la mayor parte de la velocidad del extremo.
    /// Todos los argumentos deben venir ya en espacio de MUNDO.
    public static Vector3 TipVelocity(Vector3 deviceVelocityWorld,
                                      Vector3 angularVelocityWorld,
                                      Vector3 controllerToTip)
        => deviceVelocityWorld + Vector3.Cross(angularVelocityWorld, controllerToTip);
}
