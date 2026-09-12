using NUnit.Framework;
using UnityEngine;

public class DrumPadTests
{
    DrumPad pad;
    GameObject go;

    [SetUp]
    public void SetUp()
    {
        go = new GameObject("pad");
        go.transform.position = Vector3.zero;
        go.transform.rotation = Quaternion.identity;   // normal = Vector3.up
        pad = go.AddComponent<DrumPad>();
    }

    [TearDown]
    public void TearDown() => Object.DestroyImmediate(go);

    [Test]
    public void PlanoArmado_EstaPorDelanteDeLaSuperficie()
    {
        // Con armDistance = 0.06, un punto en y = 0.06 está exactamente sobre el plano armado.
        Assert.AreEqual(0f, pad.SignedDistanceToArmPlane(new Vector3(0f, 0.06f, 0f)), 1e-5f);
    }

    [Test]
    public void DistanciaPositiva_DelLadoDelJugador()
    {
        Assert.Greater(pad.SignedDistanceToArmPlane(new Vector3(0f, 0.20f, 0f)), 0f);
    }

    [Test]
    public void DistanciaNegativa_PasadoElPlanoArmado()
    {
        Assert.Less(pad.SignedDistanceToArmPlane(new Vector3(0f, 0.01f, 0f)), 0f);
    }

    [Test]
    public void DentroDelRadio_IgnoraLaAlturaSobreElPlano()
    {
        // Proyectado sobre el plano cae a 0.10 m del centro, dentro del radio de 0.15.
        Assert.IsTrue(pad.WithinRadius(new Vector3(0.10f, 0.50f, 0f)));
    }

    [Test]
    public void FueraDelRadio()
    {
        Assert.IsFalse(pad.WithinRadius(new Vector3(0.30f, 0f, 0f)));
    }

    [Test]
    public void PadRotado_LaNormalSigueAlTransform()
    {
        // Rotado 90° sobre Z, la normal local up apunta a -X en mundo.
        go.transform.rotation = Quaternion.Euler(0f, 0f, 90f);
        Assert.Less(Vector3.Dot(pad.Normal, Vector3.right), -0.99f);
        Assert.Greater(pad.SignedDistanceToArmPlane(new Vector3(-0.20f, 0f, 0f)), 0f);
    }
}
