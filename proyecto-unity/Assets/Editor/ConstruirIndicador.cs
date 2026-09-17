using System.Linq;
using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

/// Crea el panel que muestra pieza e intensidad del último golpe, y lo conecta al fanout.
///
/// Existe por el punto 2 de la demostración del 21-sep. Sin evidencia visible, que el sistema
/// identifique la pieza y la intensidad solo se puede afirmar de palabra.
public static class ConstruirIndicador
{
    [MenuItem("Batería/Construir indicador de golpes")]
    public static void Construir()
    {
        var fanout = Object.FindAnyObjectByType<DrumHitFanout>();
        if (fanout == null)
        {
            EditorUtility.DisplayDialog("Batería",
                "No encontré el DrumHitFanout en la escena.", "Vale");
            return;
        }

        Undo.SetCurrentGroupName("Construir indicador");
        int grupo = Undo.GetCurrentGroup();

        var existente = Object.FindAnyObjectByType<HitReadout>();
        GameObject go;
        if (existente != null)
        {
            go = existente.gameObject;
            Undo.RecordObject(go, "Reubicar indicador");
        }
        else
        {
            go = new GameObject("Indicador");
            Undo.RegisterCreatedObjectUndo(go, "Crear indicador");
        }

        // A la izquierda del kit y ligeramente girado hacia el jugador: no tapa las piezas y
        // se lee sin mover la cabeza del todo.
        go.transform.position = new Vector3(-0.75f, 1.35f, 0.55f);
        go.transform.rotation = Quaternion.Euler(0f, -25f, 0f);

        var texto = go.GetComponent<TextMeshPro>();
        if (texto == null) texto = Undo.AddComponent<TextMeshPro>(go);
        texto.text = "Golpea una pieza";
        texto.fontSize = 1.4f;                        // tamaño en METROS: es texto 3D, no UI
        texto.alignment = TextAlignmentOptions.TopLeft;
        texto.color = Color.white;
        texto.rectTransform.sizeDelta = new Vector2(1.1f, 0.7f);
        // Fuente monoespaciada no hay, pero el relleno a ancho fijo de HitRing alinea igual.

        var readout = go.GetComponent<HitReadout>();
        if (readout == null) readout = Undo.AddComponent<HitReadout>(go);
        var so = new SerializedObject(readout);
        so.FindProperty("texto").objectReferenceValue = texto;
        so.ApplyModifiedPropertiesWithoutUndo();
        EditorUtility.SetDirty(readout);

        // Añadirlo al fanout SIN pisar los destinos que ya tiene.
        var soF = new SerializedObject(fanout);
        var arr = soF.FindProperty("targets");
        bool ya = Enumerable.Range(0, arr.arraySize)
            .Any(i => arr.GetArrayElementAtIndex(i).objectReferenceValue == readout);
        if (!ya)
        {
            arr.arraySize++;
            arr.GetArrayElementAtIndex(arr.arraySize - 1).objectReferenceValue = readout;
            soF.ApplyModifiedPropertiesWithoutUndo();
            EditorUtility.SetDirty(fanout);
        }

        Undo.CollapseUndoOperations(grupo);
        EditorSceneManager.MarkSceneDirty(go.scene);

        string msg = $"Indicador {(existente != null ? "actualizado" : "creado")} en " +
                     $"{go.transform.position}.\n" +
                     $"Conectado al fanout ({arr.arraySize} destinos).\n\nGuarda la escena.";
        Debug.Log("[ConstruirIndicador] " + msg.Replace("\n", " · "), go);
        EditorUtility.DisplayDialog("Batería", msg, "Vale");
    }
}
