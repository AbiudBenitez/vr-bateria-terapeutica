using System.Text;
using NUnit.Framework;

/// El historial de golpes que alimenta el indicador de la demostración.
public class HitRingTests
{
    [Test]
    public void ElMasRecienteEsElPrimero()
    {
        var r = new HitRing(5);
        r.Agregar("Tarola", 1, 1.0f);
        r.Agregar("Bombo", 3, 4.2f);

        Assert.AreEqual("Bombo", r.Reciente(0).Pieza);
        Assert.AreEqual("Tarola", r.Reciente(1).Pieza);
    }

    [Test]
    public void DescartaLosViejosAlLlenarse()
    {
        var r = new HitRing(3);
        foreach (var n in new[] { "a", "b", "c", "d", "e" }) r.Agregar(n, 2, 1f);

        Assert.AreEqual(3, r.Cuantos, "No debe crecer: el buffer es fijo para no asignar.");
        Assert.AreEqual("e", r.Reciente(0).Pieza);
        Assert.AreEqual("c", r.Reciente(2).Pieza);
    }

    [Test]
    public void PedirMasAlaDeLoGuardadoNoRevienta()
    {
        var r = new HitRing(3);
        r.Agregar("x", 1, 1f);
        Assert.DoesNotThrow(() => r.Reciente(50));
        Assert.IsNull(r.Reciente(50).Pieza);
    }

    [Test]
    public void LaIntensidadSeVeComoCirculosLlenos()
    {
        var r = new HitRing(3);
        r.Agregar("Tarola", 2, 2.5f);

        var sb = new StringBuilder();
        r.Describir(sb);
        string s = sb.ToString();

        StringAssert.Contains("Tarola", s);
        StringAssert.Contains("2.5 m/s", s);
        StringAssert.Contains("●●○", s);   // dos llenos, uno vacío
    }

    [Test]
    public void DescribirNoAcumulaEntreLlamadas()
    {
        // Se reutiliza el mismo StringBuilder en cada refresco: si no se limpiara, el texto
        // crecería sin parar hasta llenar la pantalla.
        var r = new HitRing(3);
        r.Agregar("Bombo", 3, 4f);
        var sb = new StringBuilder();
        r.Describir(sb);
        int largo = sb.Length;
        r.Describir(sb);
        Assert.AreEqual(largo, sb.Length);
    }

    [Test]
    public void CapacidadCeroNoRevienta()
    {
        var r = new HitRing(0);
        Assert.DoesNotThrow(() => r.Agregar("x", 1, 1f));
        Assert.GreaterOrEqual(r.Capacidad, 1);
    }
}
