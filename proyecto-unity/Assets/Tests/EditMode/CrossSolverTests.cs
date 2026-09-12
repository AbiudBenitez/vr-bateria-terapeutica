using NUnit.Framework;
using UnityEngine;

public class CrossSolverTests
{
    [Test]
    public void Cruce_AMitadDelIntervalo_DaFraccionMedia()
    {
        // dPrev = +0.02, dNow = -0.02  ->  cruzó exactamente a la mitad
        Assert.AreEqual(0.5f, CrossSolver.Fraction(0.02f, -0.02f), 1e-5f);
    }

    [Test]
    public void Cruce_CercaDelFinal()
    {
        // dPrev = +0.01, dNow = -0.03  ->  t = 0.01 / 0.04 = 0.25
        Assert.AreEqual(0.25f, CrossSolver.Fraction(0.01f, -0.03f), 1e-5f);
    }

    [Test]
    public void TiempoDeImpacto_SumaElTramoQueFalta()
    {
        // Cruce en dsp=100.0, faltan 0.06 m a 4 m/s  ->  +15 ms
        double t = CrossSolver.ImpactDsp(dspCross: 100.0, armDistance: 0.06f, normalVelocity: 4f);
        Assert.AreEqual(100.015, t, 1e-6);
    }

    [Test]
    public void TiempoDeImpacto_GolpeLento_TardaMas()
    {
        double lento  = CrossSolver.ImpactDsp(100.0, 0.06f, 1f);    // +60 ms
        double rapido = CrossSolver.ImpactDsp(100.0, 0.06f, 8f);    // +7.5 ms
        Assert.Greater(lento, rapido);
        Assert.AreEqual(100.060, lento,  1e-6);
        Assert.AreEqual(100.0075, rapido, 1e-6);
    }

    [Test]
    public void VelocidadNormal_SoloCuentaLaComponenteHaciaElPad()
    {
        // Normal = up. Movimiento puramente lateral no es acercamiento.
        Assert.AreEqual(0f, CrossSolver.NormalSpeed(new Vector3(5f, 0f, 0f), Vector3.up), 1e-5f);
        // Bajando a 3 m/s contra un pad cuya normal apunta arriba: acercamiento +3.
        Assert.AreEqual(3f, CrossSolver.NormalSpeed(new Vector3(0f, -3f, 0f), Vector3.up), 1e-5f);
    }

    [Test]
    public void VelocidadNormal_Alejandose_EsNegativa()
    {
        Assert.Less(CrossSolver.NormalSpeed(new Vector3(0f, 2f, 0f), Vector3.up), 0f);
    }

    [Test]
    public void VelocidadDePunta_IncluyeElGiroDeMuneca()
    {
        // Control quieto, girando a 10 rad/s sobre Z, punta a 0.3 m en +X.
        // v = ω × r = (0,0,10) × (0.3,0,0) = (0, 3, 0)  ->  3 m/s por puro giro.
        Vector3 v = CrossSolver.TipVelocity(
            deviceVelocityWorld: Vector3.zero,
            angularVelocityWorld: new Vector3(0f, 0f, 10f),
            controllerToTip: new Vector3(0.3f, 0f, 0f));
        Assert.AreEqual(3f, v.y, 1e-4f);
        Assert.AreEqual(3f, v.magnitude, 1e-4f);
    }
}
