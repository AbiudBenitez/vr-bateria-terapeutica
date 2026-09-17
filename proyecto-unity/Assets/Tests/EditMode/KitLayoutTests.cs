using System.Linq;
using NUnit.Framework;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

/// Invariantes de la disposición del kit.
///
/// Existen por un defecto real: las seis piezas se colocaron en un arco plano de ±65° y las
/// CINCO parejas adyacentes se solapaban — Tarola y Bombo por 8 cm. Un golpe en la zona
/// compartida disparaba los dos pads, o sea dos piezas de un solo golpe, que es exactamente lo
/// que el entregable del 21-sep se compromete a que no pase: "cada golpe se registra con su
/// pieza".
///
/// El error no estaba en el tamaño del pad sino en elegir ángulos sin comprobar la cuerda
/// contra el diámetro. Estas pruebas lo comprueban.
public class KitLayoutTests
{
    const string Ruta = "Assets/Scenes/Cap04_Pad.unity";
    const float HolguraMinima = 0.02f;

    Scene escena;
    DrumPad[] pads;

    [SetUp]
    public void Abrir()
    {
        if (!System.IO.File.Exists(Ruta)) Assert.Ignore($"No existe {Ruta}.");
        escena = EditorSceneManager.OpenScene(Ruta, OpenSceneMode.Additive);
        pads = escena.GetRootGameObjects()
                     .SelectMany(g => g.GetComponentsInChildren<DrumPad>(true))
                     .ToArray();
    }

    [TearDown]
    public void Cerrar()
    {
        if (escena.IsValid()) EditorSceneManager.CloseScene(escena, true);
    }

    [Test]
    public void NingunParDePadsSeSolapa()
    {
        if (pads.Length < 2) Assert.Ignore("Hace falta más de un pad para que haya solapes.");

        for (int i = 0; i < pads.Length; i++)
            for (int j = i + 1; j < pads.Length; j++)
            {
                float d = Vector3.Distance(pads[i].Center, pads[j].Center);
                float necesita = pads[i].Radius + pads[j].Radius + HolguraMinima;
                Assert.GreaterOrEqual(d, necesita,
                    $"'{pads[i].name}' y '{pads[j].name}' están a {d:F3} m y necesitan " +
                    $"{necesita:F3} m. Un golpe entre los dos dispararía AMBOS: sonarían dos " +
                    "piezas de un solo golpe.");
            }
    }

    [Test]
    public void CadaPadTieneSuPropiaPieza()
    {
        if (pads.Length < 2) Assert.Ignore("Escena de un solo pad.");

        var conPieza = pads.Where(p => p.Pieza != null).ToArray();
        Assert.AreEqual(pads.Length, conPieza.Length,
            "Hay pads sin DrumKitPiece asignada: sus golpes no sabrían qué instrumento son. " +
            $"Sin pieza: {string.Join(", ", pads.Where(p => p.Pieza == null).Select(p => p.name))}");

        var repetidas = conPieza.GroupBy(p => p.Pieza).Where(g => g.Count() > 1).ToArray();
        Assert.IsEmpty(repetidas,
            "Dos pads comparten la misma pieza: " +
            string.Join(" · ", repetidas.Select(g => $"{g.Key.name} en {string.Join(", ", g.Select(p => p.name))}")));
    }

    [Test]
    public void LosTrackersConocenTodosLosPads()
    {
        if (pads.Length < 2) Assert.Ignore("Escena de un solo pad.");

        var trackers = escena.GetRootGameObjects()
                             .SelectMany(g => g.GetComponentsInChildren<StickTracker>(true))
                             .ToArray();
        Assert.IsNotEmpty(trackers, "No hay ningún StickTracker en la escena.");

        foreach (var t in trackers)
        {
            var arr = new SerializedObject(t).FindProperty("pads");
            Assert.AreEqual(pads.Length, arr.arraySize,
                $"'{t.name}' conoce {arr.arraySize} pads de {pads.Length}. Los que le falten " +
                "no suenan con esa mano, y el síntoma parece un problema de audio.");
        }
    }
}
