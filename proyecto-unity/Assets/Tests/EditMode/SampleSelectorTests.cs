using NUnit.Framework;

/// La selección de muestra decide si un golpe suave suena distinto de uno fuerte, o solo más
/// bajo. Se prueba sin audio, sin escena y sin visor porque SampleSelector es una función pura.
public class SampleSelectorTests
{
    const int Ventana = 1;

    [Test]
    public void ConUnaSolaMuestraSiempreDevuelveCero()
    {
        for (float t = 0f; t <= 1f; t += 0.25f)
            Assert.AreEqual(0, SampleSelector.Elegir(1, t, -1, Ventana, true, 0.5f),
                "Con una sola muestra no hay nada que elegir.");
    }

    [Test]
    public void SinMuestrasDevuelveMenosUno()
    {
        Assert.AreEqual(-1, SampleSelector.Elegir(0, 0.5f, -1, Ventana, true, 0.5f));
    }

    [Test]
    public void GolpeSuaveCaeEnLaZonaOpaca()
    {
        // t = 0 es la muestra más opaca; con ventana 1 el sorteo es entre los índices 0 y 1.
        for (float r = 0f; r < 1f; r += 0.1f)
        {
            int i = SampleSelector.Elegir(14, 0f, -1, Ventana, true, r);
            Assert.LessOrEqual(i, Ventana,
                $"Con t=0 el índice debería quedar en la zona opaca, salió {i}.");
        }
    }

    [Test]
    public void GolpeFuerteCaeEnLaZonaBrillante()
    {
        const int n = 14;
        for (float r = 0f; r < 1f; r += 0.1f)
        {
            int i = SampleSelector.Elegir(n, 1f, -1, Ventana, true, r);
            Assert.GreaterOrEqual(i, n - 1 - Ventana,
                $"Con t=1 el índice debería quedar en la zona brillante, salió {i}.");
        }
    }

    [Test]
    public void ElIndiceNuncaSeSaleDelRango()
    {
        foreach (int n in new[] { 1, 2, 3, 7, 14, 20 })
            for (float t = -0.5f; t <= 1.5f; t += 0.1f)      // t fuera de rango a propósito
                for (float r = 0f; r < 1f; r += 0.2f)
                    foreach (int ult in new[] { -1, 0, n / 2, n - 1 })
                    {
                        int i = SampleSelector.Elegir(n, t, ult, Ventana, true, r);
                        Assert.That(i, Is.InRange(0, n - 1),
                            $"n={n} t={t} ultimo={ult} aleatorio={r} devolvió {i}.");
                    }
    }

    [Test]
    public void NuncaRepiteLaMuestraAnterior()
    {
        // Con n >= 3 y ventana 1 siempre hay al menos otra candidata, así que repetir sería
        // un fallo: dos golpes seguidos idénticos son lo que delata a una batería programada.
        foreach (int n in new[] { 3, 7, 14, 20 })
            for (float t = 0f; t <= 1f; t += 0.1f)
                for (float r = 0f; r < 1f; r += 0.2f)
                {
                    int primero = SampleSelector.Elegir(n, t, -1, Ventana, true, r);
                    int segundo = SampleSelector.Elegir(n, t, primero, Ventana, true, r);
                    Assert.AreNotEqual(primero, segundo,
                        $"n={n} t={t}: repitió el índice {primero}.");
                }
    }

    [Test]
    public void SinEjeTimbralPuedeElegirCualquiera()
    {
        // El Platillo tiene 0.4 dB de rango: doce variantes casi idénticas. Ahí la velocidad no
        // debe restringir la elección, o se desperdician diez de las doce.
        const int n = 12;
        var vistos = new System.Collections.Generic.HashSet<int>();
        for (float r = 0f; r < 1f; r += 0.02f)
            vistos.Add(SampleSelector.Elegir(n, 0f, -1, Ventana, false, r));

        Assert.Greater(vistos.Count, Ventana * 2 + 1,
            "Sin eje timbral debería recorrer toda la lista, no solo la ventana de t=0.");
    }

    [Test]
    public void ConEjeTimbralLaVelocidadSiRestringe()
    {
        const int n = 12;
        var vistos = new System.Collections.Generic.HashSet<int>();
        for (float r = 0f; r < 1f; r += 0.02f)
            vistos.Add(SampleSelector.Elegir(n, 0f, -1, Ventana, true, r));

        Assert.LessOrEqual(vistos.Count, Ventana * 2 + 1,
            "Con eje timbral, t=0 solo debería alcanzar la ventana de la zona opaca.");
    }
}
