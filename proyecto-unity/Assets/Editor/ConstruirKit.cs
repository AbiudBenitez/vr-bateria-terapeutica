using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

/// Coloca las seis piezas en arco con alcance graduado.
///
/// La disposición no es estética. El acta mide coordinación óculo-manual y RANGO DE ALCANCE, y
/// un arco de distancia constante no ejercita el rango. Aquí las piezas más tocadas quedan
/// cerca y los acentos lejos, con tres radios distintos: el terapeuta gradúa la dificultad
/// acercando o alejando piezas, que es la ventaja sobre una batería real que declara el §2.5
/// del diseño técnico.
public static class ConstruirKit
{
    const string CarpetaPiezas = "Assets/Audio/Piezas";

    /// Ángulo en grados respecto al frente, radio en metros, nombre del asset de la pieza.
    /// Los radios crecen hacia los extremos: alcanzar de lado es natural, y de paso gradúa.
    static readonly (string pieza, float grados, float radio)[] Disposicion =
    {
        ("Platillo", -65f, 0.68f),   // acento, el más lejano
        ("HiHat",    -40f, 0.55f),
        ("Tarola",   -15f, 0.42f),   // la más tocada, la más cerca
        ("Bombo",     15f, 0.42f),
        ("TomAlto",   40f, 0.55f),
        ("TomBajo",   65f, 0.68f),
    };

    const float Altura = 0.75f;      // altura de tarola

    [MenuItem("Batería/Construir kit de 6 piezas")]
    public static void Construir()
    {
        var plantilla = Object.FindAnyObjectByType<DrumPad>();
        if (plantilla == null)
        {
            EditorUtility.DisplayDialog("Batería",
                "No encontré ningún DrumPad en la escena.\n\n" +
                "Abre Cap04_Pad.unity: el kit se construye a partir del pad que ya existe.",
                "Vale");
            return;
        }

        var fanout = Object.FindAnyObjectByType<DrumHitFanout>();
        var trackers = Object.FindObjectsByType<StickTracker>();

        Undo.SetCurrentGroupName("Construir kit de 6 piezas");
        int grupo = Undo.GetCurrentGroup();

        var pads = new System.Collections.Generic.List<DrumPad>();
        var faltantes = new System.Collections.Generic.List<string>();

        foreach (var (nombre, grados, radio) in Disposicion)
        {
            var pieza = AssetDatabase.LoadAssetAtPath<DrumKitPiece>($"{CarpetaPiezas}/{nombre}.asset");
            if (pieza == null) { faltantes.Add(nombre); continue; }

            // Reutiliza el pad existente para la primera pieza: conserva sus referencias y el
            // PadVisual ya montado.
            DrumPad pad;
            if (pads.Count == 0 && plantilla != null)
            {
                pad = plantilla;
                Undo.RecordObject(pad.gameObject, "Reubicar pad");
            }
            else
            {
                var go = Object.Instantiate(plantilla.gameObject);
                Undo.RegisterCreatedObjectUndo(go, $"Crear pad {nombre}");
                pad = go.GetComponent<DrumPad>();
            }

            pad.gameObject.name = $"Pad_{nombre}";
            float rad = grados * Mathf.Deg2Rad;
            pad.transform.position = new Vector3(Mathf.Sin(rad) * radio, Altura, Mathf.Cos(rad) * radio);
            pad.transform.rotation = Quaternion.identity;   // normal hacia arriba

            var so = new SerializedObject(pad);
            so.FindProperty("pieza").objectReferenceValue = pieza;
            so.ApplyModifiedPropertiesWithoutUndo();
            EditorUtility.SetDirty(pad);

            var visual = pad.GetComponent<PadVisual>();
            if (visual != null) visual.Sincronizar();

            pads.Add(pad);
        }

        // Cada tracker tiene que conocer los seis pads o solo sonará el primero.
        foreach (var t in trackers)
        {
            var so = new SerializedObject(t);
            var arr = so.FindProperty("pads");
            arr.arraySize = pads.Count;
            for (int i = 0; i < pads.Count; i++)
                arr.GetArrayElementAtIndex(i).objectReferenceValue = pads[i];
            so.ApplyModifiedPropertiesWithoutUndo();
            EditorUtility.SetDirty(t);
        }

        Undo.CollapseUndoOperations(grupo);
        EditorSceneManager.MarkSceneDirty(plantilla.gameObject.scene);

        var msg = new System.Text.StringBuilder();
        msg.AppendLine($"{pads.Count} piezas colocadas en arco:\n");
        foreach (var (nombre, grados, radio) in Disposicion)
            if (!faltantes.Contains(nombre))
                msg.AppendLine($"  {nombre,-9} {grados,4:F0}°  a {radio:F2} m");
        msg.AppendLine($"\n{trackers.Length} StickTracker cableados a los {pads.Count} pads.");
        if (faltantes.Count > 0)
            msg.AppendLine($"\nFALTAN en {CarpetaPiezas}: {string.Join(", ", faltantes)}\n" +
                           "Ejecuta 'Analizar kit' primero.");
        msg.Append("\nGuarda la escena (Cmd+S).");

        Debug.Log("[ConstruirKit]\n" + msg);
        EditorUtility.DisplayDialog("Batería", msg.ToString(), "Vale");
    }
}
