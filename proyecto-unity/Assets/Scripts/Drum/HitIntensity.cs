using UnityEngine;

/// Convierte la velocidad continua del golpe en los tres niveles que pide el entregable.
///
/// Se mantiene como función pura y aparte para poder probarla sin escena, y porque la
/// velocidad continua NO se descarta: DrumHit lleva las dos cosas. El documento pide tres
/// niveles, la dinámica timbral necesita el valor continuo, y ninguna de las dos tiene por qué
/// ceder ante la otra.
public static class HitIntensity
{
    public const int Suave = 1;
    public const int Medio = 2;
    public const int Fuerte = 3;

    public static int From(float velocidad, float umbralMedio, float umbralFuerte)
    {
        // Umbrales cruzados por error en el inspector no deben invertir la escala.
        if (umbralFuerte < umbralMedio)
            (umbralMedio, umbralFuerte) = (umbralFuerte, umbralMedio);

        if (velocidad >= umbralFuerte) return Fuerte;
        if (velocidad >= umbralMedio)  return Medio;
        return Suave;
    }
}
