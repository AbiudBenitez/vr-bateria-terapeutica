using System.Linq;
using NUnit.Framework;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

/// El visual del pad tiene que decir la verdad sobre dónde golpea.
///
/// Existen por un defecto real: el cilindro medía 0.50 m de radio contra un radio de golpe de
/// 0.15, y su cara superior quedaba 15 cm por encima del plano, porque un cilindro primitivo de
/// Unity está centrado en su origen. Se apuntaba a una superficie que no disparaba nada.
///
/// Se comprueba sobre la escena REAL y no sobre objetos construidos en memoria: el invariante que
/// importa es que el artefacto que se va a medir en el capítulo 5 sea fiel.
public class PadVisualTests
{
    const string Ruta = "Assets/Scenes/Cap04_Pad.unity";
    const float Tolerancia = 0.001f;   // 1 mm

    static bool Existe => System.IO.File.Exists(Ruta);

    Scene escena;
    DrumPad pad;
    PadVisual visual;

    [SetUp]
    public void Abrir()
    {
        if (!Existe) Assert.Ignore($"No existe {Ruta}.");
        escena = EditorSceneManager.OpenScene(Ruta, OpenSceneMode.Additive);

        pad = escena.GetRootGameObjects()
                    .SelectMany(g => g.GetComponentsInChildren<DrumPad>(true))
                    .FirstOrDefault();
        Assert.IsNotNull(pad, "No encontré ningún DrumPad en la escena.");

        visual = pad.GetComponent<PadVisual>();
        Assert.IsNotNull(visual,
            "El DrumPad no tiene PadVisual. Ejecuta 'Batería → Reconstruir visual del pad'.");
    }

    [TearDown]
    public void Cerrar()
    {
        if (escena.IsValid()) EditorSceneManager.CloseScene(escena, true);
    }

    [Test]
    public void LaPielTieneElDiametroDelHitbox()
    {
        Assert.IsNotNull(visual.Piel, "PadVisual no tiene asignada la Piel.");

        // Un cilindro primitivo mide diámetro 1, así que localScale.x ES el diámetro.
        float esperado = 2f * pad.Radius;
        Assert.AreEqual(esperado, visual.Piel.localScale.x, Tolerancia,
            $"La piel mide {visual.Piel.localScale.x:F3} m de diámetro pero el radio de golpe es " +
            $"{pad.Radius:F3} m, o sea {esperado:F3} m de diámetro. El visual miente sobre dónde " +
            "golpea. Ejecuta 'Batería → Reconstruir visual del pad'.");
    }

    [Test]
    public void LaPielEstaCentradaEnElPlanoDeGolpe()
    {
        Assert.IsNotNull(visual.Piel, "PadVisual no tiene asignada la Piel.");

        Assert.Less(Mathf.Abs(visual.Piel.localPosition.y), Tolerancia,
            $"La piel está desplazada {visual.Piel.localPosition.y * 100f:F1} cm respecto al plano " +
            "de golpe. Un cilindro de Unity se centra en su origen: si se desplaza, la cara que " +
            "se ve deja de coincidir con la superficie que dispara el sonido.");
    }

    [Test]
    public void ElPlanoArmadoEstaALaDistanciaDeArmado()
    {
        Assert.IsNotNull(visual.PlanoArmado, "PadVisual no tiene asignado el PlanoArmado.");

        Assert.AreEqual(pad.ArmDistance, visual.PlanoArmado.localPosition.y, Tolerancia,
            $"El disco del plano armado está a {visual.PlanoArmado.localPosition.y:F3} m pero " +
            $"armDistance vale {pad.ArmDistance:F3} m. Es la marca de dónde se dispara el audio: " +
            "si no coincide, engaña en vez de ayudar.");
    }

    [Test]
    public void ElVisualCuelgaDelPad()
    {
        Assert.AreSame(pad.transform, visual.Piel.parent,
            "La piel no es hija del pad. Si son objetos separados pueden moverse por su cuenta y " +
            "el pad que suena deja de estar donde se ve.");
    }

    /// El capítulo 5 no se puede hacer sin calibrar, y el calibrador faltaba en la escena: se
    /// presionaba el botón y no pasaba nada porque el componente que escucha no existía.
    [Test]
    public void ExisteUnCalibradorCableado()
    {
        var cal = escena.GetRootGameObjects()
                        .SelectMany(g => g.GetComponentsInChildren<PadCalibrator>(true))
                        .FirstOrDefault();

        Assert.IsNotNull(cal,
            "No hay ningún PadCalibrator en la escena. Sin él, el botón A no hace nada y la " +
            "medición del capítulo 5 no se puede calibrar. Ejecuta " +
            "'Batería → Reconstruir visual del pad'.");

        var so = new SerializedObject(cal);
        Assert.IsNotNull(so.FindProperty("pad").objectReferenceValue,
            "El PadCalibrator no tiene asignado el DrumPad: el botón no movería nada.");
        Assert.IsNotNull(so.FindProperty("tip").objectReferenceValue,
            "El PadCalibrator no tiene asignado el Tip: no sabría a dónde mover el pad.");
    }

    [Test]
    public void ElCalibradorUsaLaMismaPuntaQueElTracker()
    {
        var cal = escena.GetRootGameObjects()
                        .SelectMany(g => g.GetComponentsInChildren<PadCalibrator>(true))
                        .FirstOrDefault();
        if (cal == null) Assert.Ignore("Sin calibrador; lo cubre ExisteUnCalibradorCableado.");

        var tipCal = new SerializedObject(cal).FindProperty("tip").objectReferenceValue;

        var tipsDeTrackers = escena.GetRootGameObjects()
            .SelectMany(g => g.GetComponentsInChildren<StickTracker>(true))
            .Select(t => new SerializedObject(t).FindProperty("tip").objectReferenceValue)
            .Where(o => o != null)
            .ToArray();

        CollectionAssert.Contains(tipsDeTrackers, tipCal,
            "El calibrador usa una punta distinta a la de cualquier StickTracker. Se calibraría " +
            "con una punta y se golpearía con otra, y el desfase se mediría como latencia.");
    }

    [Test]
    public void NoQuedaElCilindroViejo()
    {
        var viejo = escena.GetRootGameObjects().FirstOrDefault(g => g.name == "DrumPadR");
        Assert.IsNull(viejo,
            "Sigue en la escena 'DrumPadR', el cilindro de 1 m que reemplazó el visual nuevo. " +
            "Dos pads visibles y solo uno responde.");
    }
}
