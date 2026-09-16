using System.Collections.Generic;
using System.Reflection;
using System.Text;
using UnityEngine;

/// Sonda de diagnóstico: averigua QUÉ está moviendo el rig.
///
/// Se pone en cualquier GameObject de la escena. Cada 0.5 s imprime a la consola:
///   - cuánto se movió el XR Origin, descompuesto en horizontal y vertical
///   - el estado del CharacterController (si lo hay)
///   - qué proveedores de locomoción están activos en ese instante
///
/// Usa reflexión a propósito: así compila con cualquier versión del XR Interaction Toolkit
/// sin depender de nombres de namespace que cambian entre versiones.
public sealed class DiagnosticoMovimiento : MonoBehaviour
{
    [SerializeField, Tooltip("Raíz del rig. Si se deja vacío, se busca el XROrigin de la escena.")]
    Transform origen;

    [SerializeField] float intervalo = 0.5f;

    [SerializeField, Tooltip("Metros de movimiento por debajo de los cuales se considera quieto.")]
    float umbralQuieto = 0.001f;

    CharacterController cc;
    readonly List<MonoBehaviour> proveedores = new();
    Vector3 posPrevia;
    float siguiente;

    void Start()
    {
        if (origen == null)
        {
            foreach (var mb in FindObjectsByType<MonoBehaviour>(FindObjectsSortMode.None))
            {
                if (mb.GetType().Name == "XROrigin") { origen = mb.transform; break; }
            }
        }

        if (origen == null)
        {
            Debug.LogError("[DiagMov] No encontré ningún XROrigin en la escena. " +
                           "Asigna el campo 'origen' a mano.");
            enabled = false;
            return;
        }

        cc = origen.GetComponentInChildren<CharacterController>();

        foreach (var mb in origen.GetComponentsInChildren<MonoBehaviour>(true))
        {
            string n = mb.GetType().Name;
            if (n.EndsWith("Provider") || n.Contains("Locomotion") || n.Contains("Mediator"))
                proveedores.Add(mb);
        }

        posPrevia = origen.position;

        var sb = new StringBuilder();
        sb.AppendLine($"[DiagMov] Rig: '{origen.name}'  pos inicial {origen.position}");
        sb.AppendLine($"[DiagMov] CharacterController: {(cc != null ? cc.name : "NINGUNO")}");
        sb.AppendLine($"[DiagMov] {proveedores.Count} componentes de locomoción encontrados:");
        foreach (var p in proveedores)
            sb.AppendLine($"[DiagMov]    {p.GetType().Name}  (enabled={p.enabled}, go activo={p.gameObject.activeInHierarchy}) en '{p.gameObject.name}'");
        Debug.Log(sb.ToString());
    }

    void Update()
    {
        if (Time.time < siguiente) return;
        siguiente = Time.time + intervalo;

        Vector3 pos = origen.position;
        Vector3 d = pos - posPrevia;
        posPrevia = pos;

        float horiz = new Vector2(d.x, d.z).magnitude;
        float vert = d.y;

        if (horiz < umbralQuieto && Mathf.Abs(vert) < umbralQuieto)
        {
            Debug.Log($"[DiagMov] QUIETO  pos={Fmt(pos)}");
            return;
        }

        var sb = new StringBuilder();
        sb.Append($"[DiagMov] SE MUEVE  pos={Fmt(pos)}  ");
        sb.Append($"horiz={horiz / intervalo:F3} m/s  vert={vert / intervalo:+0.000;-0.000} m/s  ");
        sb.Append($"dir={Fmt(d.normalized)}");

        if (cc != null)
            sb.Append($"  | CC grounded={cc.isGrounded} vel={Fmt(cc.velocity)}");

        // Qué proveedor está activo. Se leen por reflexión las propiedades que las
        // distintas versiones del toolkit han usado para exponer ese estado.
        foreach (var p in proveedores)
        {
            if (!p.enabled || !p.gameObject.activeInHierarchy) continue;
            string estado = LeerEstado(p);
            if (estado != null) sb.Append($"  | {p.GetType().Name}={estado}");
        }

        Debug.Log(sb.ToString());
    }

    static string LeerEstado(MonoBehaviour p)
    {
        var t = p.GetType();
        foreach (string nombre in new[] { "locomotionState", "isLocomotionActive", "locomotionPhase" })
        {
            PropertyInfo pi = t.GetProperty(nombre,
                BindingFlags.Public | BindingFlags.Instance | BindingFlags.FlattenHierarchy);
            if (pi == null) continue;
            object v = pi.GetValue(p);
            if (v == null) continue;
            string s = v.ToString();
            // Solo interesa lo que NO está inactivo.
            if (s is "Idle" or "Ended" or "False" or "0") return null;
            return s;
        }
        return null;
    }

    static string Fmt(Vector3 v) => $"({v.x:F3}, {v.y:F3}, {v.z:F3})";
}
