using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

/// Invariantes de las escenas de VR.
///
/// Existen por un bug real: el rig quedó inclinado 50° y, como el GravityProvider de los
/// Starter Assets aplica la gravedad en espacio LOCAL, el suelo horizontal pasó a tener una
/// pendiente aparente de 50° contra un SlopeLimit de 45. El personaje nunca volvió a estar
/// grounded y cayó indefinidamente, en el simulador y en el visor.
///
/// Cinco grados de diferencia. Estas pruebas evitan que vuelva a pasar sin avisar.
public class EscenaRigTests
{
    static readonly string[] Escenas =
    {
        "Assets/Scenes/Cap03_Manos.unity",
        "Assets/Scenes/Cap04_Pad.unity",
    };

    /// Tolerancia en grados. Una inclinación por debajo de esto no altera la física ni la
    /// geometría del golpe de forma apreciable.
    const float ToleranciaGrados = 0.5f;

    static IEnumerable<string> EscenasExistentes =>
        Escenas.Where(r => System.IO.File.Exists(r));

    [TestCaseSource(nameof(EscenasExistentes))]
    public void ElRigEstaDerecho(string ruta)
    {
        var escena = EditorSceneManager.OpenScene(ruta, OpenSceneMode.Additive);
        try
        {
            Transform rig = BuscarRig(escena);
            Assert.IsNotNull(rig, $"No encontré el XR Origin en {ruta}.");

            float inclinacion = Vector3.Angle(rig.up, Vector3.up);
            Assert.Less(inclinacion, ToleranciaGrados,
                $"El rig de {ruta} está inclinado {inclinacion:F1}° respecto a la vertical. " +
                "Con gravedad en espacio local, una inclinación mayor que el SlopeLimit del " +
                "CharacterController (45°) hace que el suelo deje de contar como piso y el " +
                "personaje caiga sin parar. Pon la rotación del XR Origin en (0, 0, 0).");
        }
        finally
        {
            EditorSceneManager.CloseScene(escena, true);
        }
    }

    [TestCaseSource(nameof(EscenasExistentes))]
    public void ElRigNoTieneLocomocion(string ruta)
    {
        var escena = EditorSceneManager.OpenScene(ruta, OpenSceneMode.Additive);
        try
        {
            Transform rig = BuscarRig(escena);
            Assert.IsNotNull(rig, $"No encontré el XR Origin en {ruta}.");

            var sobra = rig.GetComponentsInChildren<MonoBehaviour>(true)
                           .Where(m => m != null)
                           .Select(m => m.GetType().Name)
                           .Where(EsLocomocion)
                           .Distinct()
                           .OrderBy(n => n)
                           .ToArray();

            Assert.IsEmpty(sobra,
                $"El rig de {ruta} conserva locomoción: {string.Join(", ", sobra)}. " +
                "Este proyecto es de pie frente a una batería y no usa locomoción. " +
                "Cualquiera de esos componentes puede mover el rig respecto al pad y " +
                "invalidar en silencio la calibración de latencia. Borra el hijo 'Locomotion'.");
        }
        finally
        {
            EditorSceneManager.CloseScene(escena, true);
        }
    }

    [TestCaseSource(nameof(EscenasExistentes))]
    public void ElRigNoTieneCharacterController(string ruta)
    {
        var escena = EditorSceneManager.OpenScene(ruta, OpenSceneMode.Additive);
        try
        {
            Transform rig = BuscarRig(escena);
            Assert.IsNotNull(rig, $"No encontré el XR Origin en {ruta}.");

            var cc = rig.GetComponentInChildren<CharacterController>(true);
            Assert.IsNull(cc,
                $"El rig de {ruta} conserva un CharacterController en '{(cc != null ? cc.name : "")}'. " +
                "Sin proveedores de locomoción no lo mueve nadie, y su cápsula puede empujar " +
                "el rig al resolver penetraciones contra los colliders de las baquetas.");
        }
        finally
        {
            EditorSceneManager.CloseScene(escena, true);
        }
    }

    /// Se busca por componente, no por nombre: el nombre del GameObject cambia entre el
    /// prefab pelado ("XR Origin (VR)") y el de los Starter Assets ("XR Origin (XR Rig)").
    static Transform BuscarRig(Scene escena)
    {
        foreach (var raiz in escena.GetRootGameObjects())
        {
            foreach (var mb in raiz.GetComponentsInChildren<MonoBehaviour>(true))
            {
                if (mb != null && mb.GetType().Name == "XROrigin")
                    return mb.transform;
            }
        }
        return null;
    }

    static bool EsLocomocion(string nombreDeTipo) =>
        nombreDeTipo.EndsWith("MoveProvider")
        || nombreDeTipo.EndsWith("TurnProvider")
        || nombreDeTipo is "GravityProvider"
                        or "TeleportationProvider"
                        or "ClimbProvider"
                        or "JumpProvider"
                        or "LocomotionMediator";
}
