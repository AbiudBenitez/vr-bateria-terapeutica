using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.XR;

/// Construye el visual del pad sobre la escena abierta.
///
/// Se hace desde un menú de editor y no editando el YAML de la escena a mano porque la API de
/// Unity produce objetos válidos por construcción. Un error en el YAML de una escena es caro de
/// diagnosticar y fácil de cometer.
///
/// Es idempotente: se puede ejecutar las veces que haga falta.
public static class PadVisualBuilder
{
    const string CarpetaMateriales = "Assets/Materials";
    static readonly string[] NombresHijos = { "Piel", "Aro", "Casco", "PlanoArmado" };

    [MenuItem("Batería/Reconstruir visual del pad")]
    public static void Reconstruir()
    {
        var pad = Object.FindFirstObjectByType<DrumPad>();
        if (pad == null)
        {
            EditorUtility.DisplayDialog("Batería",
                "No encontré ningún DrumPad en la escena abierta.\n\n" +
                "Abre Cap04_Pad.unity y vuelve a intentarlo.", "Vale");
            return;
        }

        Undo.SetCurrentGroupName("Reconstruir visual del pad");
        int grupo = Undo.GetCurrentGroup();

        BorrarHijosPrevios(pad.transform);

        var mats = CrearMateriales();

        Transform piel        = Crear(pad.transform, "Piel",        mats["Pad_Piel"]);
        Transform aro         = Crear(pad.transform, "Aro",         mats["Pad_Aro"]);
        Transform casco       = Crear(pad.transform, "Casco",       mats["Pad_Casco"]);
        Transform planoArmado = Crear(pad.transform, "PlanoArmado", mats["Pad_PlanoArmado"]);

        var visual = pad.GetComponent<PadVisual>();
        if (visual == null) visual = Undo.AddComponent<PadVisual>(pad.gameObject);
        Undo.RecordObject(visual, "Asignar hijos");
        visual.AsignarHijos(piel, aro, casco, planoArmado);
        visual.Sincronizar();
        EditorUtility.SetDirty(visual);

        BorrarCilindroViejo();
        NormalizarTip();
        AsegurarCalibrador(pad);

        Undo.CollapseUndoOperations(grupo);
        EditorSceneManager.MarkSceneDirty(pad.gameObject.scene);

        Debug.Log($"[PadVisualBuilder] Visual reconstruido sobre '{pad.name}'. " +
                  $"radius={pad.Radius:F3} m  armDistance={pad.ArmDistance:F3} m. " +
                  "Guarda la escena (Cmd+S).", pad);
    }

    /// El calibrador no estaba en la escena y el capítulo 5 lo daba por puesto: se presionaba
    /// el botón y no pasaba nada, porque el componente que escucha no existía.
    /// Se crea aquí para que no dependa de que alguien se acuerde de añadirlo a mano.
    static void AsegurarCalibrador(DrumPad pad)
    {
        var cal = Object.FindFirstObjectByType<PadCalibrator>();
        if (cal != null)
        {
            Debug.Log($"[PadVisualBuilder] Ya existe un PadCalibrator en '{cal.name}'.", cal);
            return;
        }

        // Se cuelga del tracker de la mano derecha para heredar su Tip sin ambigüedad.
        var tracker = Object.FindObjectsByType<StickTracker>(FindObjectsSortMode.None)
                            .FirstOrDefault(t => t.name.Contains("Tracker") && !t.name.EndsWith("L"))
                      ?? Object.FindFirstObjectByType<StickTracker>();

        var go = new GameObject("Calibrador");
        Undo.RegisterCreatedObjectUndo(go, "Crear Calibrador");
        cal = Undo.AddComponent<PadCalibrator>(go);

        Transform tip = tracker != null ? BuscarTip(tracker) : null;
        var so = new SerializedObject(cal);
        so.FindProperty("pad").objectReferenceValue = pad;
        so.FindProperty("tip").objectReferenceValue = tip;
        so.FindProperty("hand").intValue = (int)XRNode.RightHand;
        so.ApplyModifiedPropertiesWithoutUndo();
        EditorUtility.SetDirty(cal);

        if (tip == null)
            Debug.LogWarning("[PadVisualBuilder] Creé el Calibrador pero no encontré el Tip de la " +
                             "mano derecha. Asígnalo a mano en el inspector.", cal);
        else
            Debug.Log($"[PadVisualBuilder] Calibrador creado. Pad='{pad.name}', Tip='{tip.name}'. " +
                      "Apoya la punta en la mesa y presiona A: debe vibrar.", cal);
    }

    /// El Tip que usa el tracker es el mismo que debe usar el calibrador, o se calibraría con
    /// una punta y se golpearía con otra.
    static Transform BuscarTip(StickTracker tracker)
    {
        var so = new SerializedObject(tracker);
        var prop = so.FindProperty("tip");
        return prop != null ? prop.objectReferenceValue as Transform : null;
    }

    static void BorrarHijosPrevios(Transform padre)
    {
        var aBorrar = new List<GameObject>();
        foreach (Transform h in padre)
            foreach (string n in NombresHijos)
                if (h.name == n) { aBorrar.Add(h.gameObject); break; }

        foreach (var go in aBorrar) Undo.DestroyObjectImmediate(go);
    }

    /// El cilindro de 1 m de diámetro que mentía. Su plano de golpe aparente quedaba 15 cm por
    /// encima del real, porque un cilindro primitivo se centra en su origen.
    static void BorrarCilindroViejo()
    {
        var viejo = GameObject.Find("DrumPadR");
        if (viejo == null) return;
        Debug.Log("[PadVisualBuilder] Borrado 'DrumPadR', el cilindro viejo de 1 m.", viejo);
        Undo.DestroyObjectImmediate(viejo);
    }

    /// Los Tip tenían escalas como (36.6, 10.1, 17.3). Son Transform vacíos y solo se lee su
    /// posición, así que no afectaban al cálculo del golpe, pero es una trampa esperando a que
    /// alguien les cuelgue geometría.
    static void NormalizarTip()
    {
        foreach (var tracker in Object.FindObjectsByType<StickTracker>(FindObjectsSortMode.None))
        {
            foreach (Transform t in tracker.GetComponentsInChildren<Transform>(true))
            {
                if (t.name != "Tip" || t.localScale == Vector3.one) continue;
                Undo.RecordObject(t, "Normalizar Tip");
                t.localScale = Vector3.one;
                EditorUtility.SetDirty(t);
                Debug.Log($"[PadVisualBuilder] Escala de '{t.name}' normalizada a (1,1,1).", t);
            }
        }
    }

    static Transform Crear(Transform padre, string nombre, Material mat)
    {
        var go = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        go.name = nombre;

        // Los primitivos vienen con collider. Aquí estorba: la detección del golpe es por
        // plano, no por colisión, y un collider suelto puede empujar cosas.
        var col = go.GetComponent<Collider>();
        if (col != null) Object.DestroyImmediate(col);

        go.GetComponent<MeshRenderer>().sharedMaterial = mat;
        Undo.RegisterCreatedObjectUndo(go, $"Crear {nombre}");
        go.transform.SetParent(padre, false);
        return go.transform;
    }

    static Dictionary<string, Material> CrearMateriales()
    {
        if (!Directory.Exists(CarpetaMateriales))
        {
            Directory.CreateDirectory(CarpetaMateriales);
            AssetDatabase.Refresh();
        }

        var shader = Shader.Find("Universal Render Pipeline/Lit");
        if (shader == null)
        {
            Debug.LogError("[PadVisualBuilder] No encontré el shader de URP. " +
                           "¿El proyecto se creó con la plantilla Universal 3D?");
            shader = Shader.Find("Standard");
        }

        var salida = new Dictionary<string, Material>
        {
            ["Pad_Piel"]  = Material("Pad_Piel", shader, new Color(0.93f, 0.89f, 0.78f),
                                     metallic: 0f, smoothness: 0.25f),
            ["Pad_Casco"] = Material("Pad_Casco", shader, new Color(0.45f, 0.10f, 0.10f),
                                     metallic: 0f, smoothness: 0.35f),
            ["Pad_Aro"]   = Material("Pad_Aro", shader, new Color(0.72f, 0.73f, 0.76f),
                                     metallic: 0.9f, smoothness: 0.70f),
            ["Pad_PlanoArmado"] = Transparente("Pad_PlanoArmado", shader,
                                               new Color(0.25f, 0.85f, 0.95f, 0.22f)),
        };
        AssetDatabase.SaveAssets();
        return salida;
    }

    static Material Material(string nombre, Shader shader, Color color,
                             float metallic, float smoothness)
    {
        string ruta = $"{CarpetaMateriales}/{nombre}.mat";
        var mat = AssetDatabase.LoadAssetAtPath<Material>(ruta);
        if (mat == null)
        {
            mat = new Material(shader);
            AssetDatabase.CreateAsset(mat, ruta);
        }
        mat.shader = shader;
        mat.SetColor("_BaseColor", color);
        if (mat.HasProperty("_Color")) mat.SetColor("_Color", color);
        mat.SetFloat("_Metallic", metallic);
        mat.SetFloat("_Smoothness", smoothness);
        EditorUtility.SetDirty(mat);
        return mat;
    }

    /// URP no expone la transparencia con un solo interruptor: hay que poner el modo de
    /// superficie, los factores de mezcla, desactivar la escritura de profundidad, mover el
    /// material a la cola de transparentes y activar la keyword. Si falta cualquiera de los
    /// cinco, el material sale opaco sin avisar.
    static Material Transparente(string nombre, Shader shader, Color color)
    {
        var mat = Material(nombre, shader, color, metallic: 0f, smoothness: 0.5f);
        mat.SetFloat("_Surface", 1f);                                  // 0 opaco, 1 transparente
        mat.SetFloat("_Blend", 0f);                                    // alpha
        mat.SetFloat("_SrcBlend", (float)UnityEngine.Rendering.BlendMode.SrcAlpha);
        mat.SetFloat("_DstBlend", (float)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
        mat.SetFloat("_ZWrite", 0f);
        mat.SetFloat("_AlphaClip", 0f);
        mat.EnableKeyword("_SURFACE_TYPE_TRANSPARENT");
        mat.DisableKeyword("_ALPHATEST_ON");
        mat.renderQueue = (int)UnityEngine.Rendering.RenderQueue.Transparent;
        EditorUtility.SetDirty(mat);
        return mat;
    }
}
