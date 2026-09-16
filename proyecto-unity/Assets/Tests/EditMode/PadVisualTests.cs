using System.Linq;
using NUnit.Framework;
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

    [Test]
    public void NoQuedaElCilindroViejo()
    {
        var viejo = escena.GetRootGameObjects().FirstOrDefault(g => g.name == "DrumPadR");
        Assert.IsNull(viejo,
            "Sigue en la escena 'DrumPadR', el cilindro de 1 m que reemplazó el visual nuevo. " +
            "Dos pads visibles y solo uno responde.");
    }
}
