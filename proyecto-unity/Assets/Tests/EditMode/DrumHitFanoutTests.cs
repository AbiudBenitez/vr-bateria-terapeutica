using NUnit.Framework;
using UnityEngine;
using UnityEngine.XR;

public class DrumHitFanoutTests
{
    class SinkEspia : DrumHitSink
    {
        public int Recibidos;
        public DrumHit Ultimo;
        public override void Handle(in DrumHit hit) { Recibidos++; Ultimo = hit; }
    }

    GameObject go;

    // El destruido va en TearDown y no al final de cada prueba: si un Assert falla, el resto
    // del cuerpo no se ejecuta y el GameObject sobreviviría hasta la siguiente prueba.
    [TearDown]
    public void TearDown()
    {
        if (go != null) Object.DestroyImmediate(go);
        go = null;
    }

    [Test]
    public void Fanout_RepartePorIgualATodosLosDestinos()
    {
        go = new GameObject("fanout");
        var a = go.AddComponent<SinkEspia>();
        var b = go.AddComponent<SinkEspia>();
        var fanout = go.AddComponent<DrumHitFanout>();
        fanout.SetTargetsForTests(new DrumHitSink[] { a, b });

        fanout.Handle(new DrumHit(null, 3.5f, 1234.5, Vector3.zero, XRNode.RightHand));

        Assert.AreEqual(1, a.Recibidos);
        Assert.AreEqual(1, b.Recibidos);
        Assert.AreEqual(3.5f, a.Ultimo.Velocity, 1e-5f);
        Assert.AreEqual(1234.5, b.Ultimo.ImpactDsp, 1e-9);
    }

    [Test]
    public void Fanout_SinDestinos_NoRevienta()
    {
        go = new GameObject("fanout");
        var fanout = go.AddComponent<DrumHitFanout>();
        fanout.SetTargetsForTests(new DrumHitSink[0]);
        Assert.DoesNotThrow(() =>
            fanout.Handle(new DrumHit(null, 1f, 0.0, Vector3.zero, XRNode.LeftHand)));
    }
}
