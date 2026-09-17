using UnityEngine;

/// Elige qué muestra suena. Función pura, sin MonoBehaviour y sin estado: se puede probar en
/// EditMode sin audio, sin escena y sin visor, igual que CrossSolver.
public static class SampleSelector
{
    /// Devuelve el índice de la muestra a reproducir, o -1 si no hay ninguna.
    ///
    /// El número aleatorio entra como PARÁMETRO en lugar de llamar a Random por dentro. Así la
    /// función es determinista y las pruebas no dependen de una semilla global — que es la
    /// diferencia entre una prueba que falla una vez cada veinte ejecuciones y una que no.
    ///
    /// <param name="t01">Posición en el eje de brillo: 0 la más opaca, 1 la más brillante.</param>
    /// <param name="ultimo">Índice reproducido la vez anterior, o -1 si no hay.</param>
    /// <param name="ventana">Cuántas muestras a cada lado del centro entran en el sorteo.</param>
    /// <param name="ejeTimbral">false = round-robin sobre toda la lista.</param>
    /// <param name="aleatorio">En [0, 1).</param>
    public static int Elegir(int n, float t01, int ultimo, int ventana, bool ejeTimbral,
                             float aleatorio)
    {
        if (n <= 0) return -1;
        if (n == 1) return 0;

        int lo, hi;
        if (ejeTimbral)
        {
            int centro = Mathf.RoundToInt(Mathf.Clamp01(t01) * (n - 1));
            int v = Mathf.Max(0, ventana);
            lo = Mathf.Max(0, centro - v);
            hi = Mathf.Min(n - 1, centro + v);
        }
        else
        {
            lo = 0;
            hi = n - 1;
        }

        // Cuántos candidatos hay una vez excluida la última reproducida.
        bool excluye = ultimo >= lo && ultimo <= hi;
        int disponibles = (hi - lo + 1) - (excluye ? 1 : 0);

        // Solo ocurre si la ventana contenía únicamente a la última. Repetir es inevitable.
        if (disponibles <= 0) return Mathf.Clamp(ultimo, 0, n - 1);

        int k = Mathf.Clamp(Mathf.FloorToInt(Mathf.Clamp01(aleatorio) * disponibles),
                            0, disponibles - 1);

        int elegido = lo + k;
        if (excluye && elegido >= ultimo) elegido++;   // salta el hueco de la excluida
        return Mathf.Clamp(elegido, 0, n - 1);
    }
}
