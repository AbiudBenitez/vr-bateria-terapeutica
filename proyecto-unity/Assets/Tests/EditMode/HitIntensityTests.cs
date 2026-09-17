using NUnit.Framework;

/// El entregable del 21-sep exige tres niveles de intensidad. Se prueban aquí, sin escena.
public class HitIntensityTests
{
    const float Medio = 1.5f, Fuerte = 3.5f;

    [Test]
    public void GolpeFlojoEsSuave()
    {
        Assert.AreEqual(HitIntensity.Suave, HitIntensity.From(0.5f, Medio, Fuerte));
        Assert.AreEqual(HitIntensity.Suave, HitIntensity.From(1.49f, Medio, Fuerte));
    }

    [Test]
    public void GolpeIntermedioEsMedio()
    {
        Assert.AreEqual(HitIntensity.Medio, HitIntensity.From(1.5f, Medio, Fuerte));
        Assert.AreEqual(HitIntensity.Medio, HitIntensity.From(3.49f, Medio, Fuerte));
    }

    [Test]
    public void GolpeFuerteEsFuerte()
    {
        Assert.AreEqual(HitIntensity.Fuerte, HitIntensity.From(3.5f, Medio, Fuerte));
        Assert.AreEqual(HitIntensity.Fuerte, HitIntensity.From(12f, Medio, Fuerte));
    }

    [Test]
    public void LosUmbralesInvertidosNoInviertenLaEscala()
    {
        // Alguien cruza los dos campos en el inspector. Un golpe fuerte debe seguir siendo
        // fuerte, no convertirse en suave sin que nada avise.
        Assert.AreEqual(HitIntensity.Fuerte, HitIntensity.From(10f, Fuerte, Medio));
        Assert.AreEqual(HitIntensity.Suave, HitIntensity.From(0.1f, Fuerte, Medio));
    }

    [Test]
    public void LaEscalaEsMonotona()
    {
        int anterior = HitIntensity.Suave;
        for (float v = 0f; v <= 10f; v += 0.05f)
        {
            int i = HitIntensity.From(v, Medio, Fuerte);
            Assert.GreaterOrEqual(i, anterior, $"La intensidad bajó al subir la velocidad en v={v}.");
            anterior = i;
        }
    }
}
