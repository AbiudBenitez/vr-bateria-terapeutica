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

    /// Ángulo respecto al frente, radio en metros, altura en metros, nombre del asset.
    ///
    /// LA ALTURA ES LO QUE HACE QUE QUEPAN. La primera versión puso las seis piezas a la misma
    /// altura en un arco de ±65°, y las cinco parejas adyacentes SE SOLAPABAN — Tarola y Bombo
    /// por 8 cm. Un golpe en la zona compartida disparaba los dos pads: dos piezas de un solo
    /// golpe, que rompe justo el criterio de "cada golpe se registra con su pieza".
    ///
    /// Los platillos arriba, como en una batería real, separan en la tercera dimensión lo que
    /// en planta está cerca. Con eso el arco se cierra a ±60°, el alcance baja a 0.40–0.62 m y
    /// los pads quedan MÁS grandes que antes. El radio de 0.15 nunca fue el problema.
    static readonly (string pieza, float grados, float radio, float altura)[] Disposicion =
    {
        ("TomAlto",  -60f, 0.62f, 0.75f),
        ("HiHat",    -38f, 0.62f, 1.00f),   // platillo: arriba
        ("Tarola",   -26f, 0.40f, 0.75f),   // la más tocada, la más cerca
        ("Bombo",     26f, 0.40f, 0.75f),
        ("Platillo",  38f, 0.62f, 1.00f),   // platillo: arriba
        ("TomBajo",   60f, 0.62f, 0.75f),
    };

    /// Holgura mínima exigida entre los BORDES de dos pads. Por debajo de esto un golpe puede
    /// caer dentro de dos a la vez.
    const float HolguraMinima = 0.02f;

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

        foreach (var (nombre, grados, radio, altura) in Disposicion)
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
            pad.transform.position = new Vector3(Mathf.Sin(rad) * radio, altura, Mathf.Cos(rad) * radio);
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

        // Comprobación que faltaba en la primera versión y que costó cinco pares solapados.
        string solapes = Solapes(pads);

        Undo.CollapseUndoOperations(grupo);
        EditorSceneManager.MarkSceneDirty(plantilla.gameObject.scene);

        var msg = new System.Text.StringBuilder();
        msg.AppendLine($"{pads.Count} piezas colocadas en arco:\n");
        foreach (var (nombre, grados, radio, altura) in Disposicion)
            if (!faltantes.Contains(nombre))
                msg.AppendLine($"  {nombre,-9} {grados,4:F0}°  r {radio:F2} m  altura {altura:F2} m");
        msg.AppendLine($"\n{trackers.Length} StickTracker cableados a los {pads.Count} pads.");
        if (!string.IsNullOrEmpty(solapes))
        {
            msg.AppendLine("\nPADS QUE SE SOLAPAN — un golpe dispararía los dos:");
            msg.Append(solapes);
            Debug.LogError("[ConstruirKit] Hay pads solapados:\n" + solapes);
        }
        if (faltantes.Count > 0)
            msg.AppendLine($"\nFALTAN en {CarpetaPiezas}: {string.Join(", ", faltantes)}\n" +
                           "Ejecuta 'Analizar kit' primero.");
        msg.Append("\nGuarda la escena (Cmd+S).");

        Debug.Log("[ConstruirKit]\n" + msg);
        EditorUtility.DisplayDialog("Batería", msg.ToString(), "Vale");
    }

    /// Devuelve los pares cuyos bordes quedan a menos de HolguraMinima, o cadena vacía.
    ///
    /// Se comprueba sobre las posiciones REALES de los pads, no sobre la tabla: si alguien
    /// mueve uno a mano, el siguiente que ejecute esto se entera.
    static string Solapes(System.Collections.Generic.List<DrumPad> pads)
    {
        var sb = new System.Text.StringBuilder();
        for (int i = 0; i < pads.Count; i++)
            for (int j = i + 1; j < pads.Count; j++)
            {
                float d = Vector3.Distance(pads[i].Center, pads[j].Center);
                float necesita = pads[i].Radius + pads[j].Radius + HolguraMinima;
                if (d < necesita)
                    sb.AppendLine($"  {pads[i].name} / {pads[j].name}: " +
                                  $"{d:F3} m, hacen falta {necesita:F3} m");
            }
        return sb.ToString();
    }
}
