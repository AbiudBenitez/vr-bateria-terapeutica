using UnityEngine;

/// Una pieza del kit: sus muestras ORDENADAS POR BRILLO, no por nombre de archivo.
///
/// El orden por nombre engaña. La primera revisión de este pack concluyó que las series eran
/// capas de velocity porque el pico correlacionaba 0.97 con el índice — pero sobre un rango de
/// 3.2 dB, y con el brillo yendo en sentido CONTRARIO. Lo genera `Batería → Analizar kit`
/// midiendo cada archivo; no se escribe a mano.
[CreateAssetMenu(fileName = "Pieza", menuName = "Batería/Pieza del kit")]
public sealed class DrumKitPiece : ScriptableObject
{
    /// Por debajo de esta razón entre el brillo máximo y el mínimo, la pieza no tiene eje
    /// timbral aprovechable y se reproduce en round-robin puro. El Platillo del kit actual
    /// tiene 1.05 (0.4 dB): doce variantes prácticamente idénticas.
    public const float UmbralBrillo = 1.3f;

    [System.Serializable]
    public struct Muestra
    {
        public AudioClip clip;

        [Tooltip("Centroide espectral de los primeros 50 ms, en Hz. Es el eje de ordenación.")]
        public float centroideHz;

        [Tooltip("Ganancia de normalización, siempre <= 1. AudioSource.volume no puede " +
                 "amplificar, así que se atenúa hacia la muestra más floja del kit.")]
        public float ganancia;
    }

    public string nombrePieza;

    [Tooltip("Ordenadas de más opaca a más brillante.")]
    public Muestra[] muestras;

    [Tooltip("Brillo máximo dividido entre el mínimo.")]
    public float rangoDeBrillo;

    /// ¿Tiene suficiente recorrido timbral para que la velocidad seleccione muestra?
    public bool TieneEjeTimbral => rangoDeBrillo >= UmbralBrillo;

    public int Cuenta => muestras != null ? muestras.Length : 0;
}
