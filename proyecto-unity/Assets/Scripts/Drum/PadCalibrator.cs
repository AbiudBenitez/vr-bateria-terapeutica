using UnityEngine;
using UnityEngine.XR;

/// Coloca el pad virtual exactamente donde está la superficie física de medición.
/// Se apoya la punta del control sobre la superficie y se presiona el botón primario
/// (A en el control derecho, X en el izquierdo): el pad salta a ese punto, con la normal
/// apuntando hacia arriba en el mundo.
///
/// Sin este paso la medición de latencia del capítulo 5 no significa nada: si el pad virtual
/// está unos centímetros por encima de la mesa, el sonido se dispara antes del contacto físico
/// y ese adelanto se mide como latencia negativa que en realidad es un error de montaje.
///
/// CONFIRMACIÓN HÁPTICA, no solo consola. Dentro del visor no se ve el Debug.Log, y si la punta
/// ya estaba cerca del pad el salto es imperceptible: se presiona el botón y parece que no pasó
/// nada. La vibración es la única señal que llega al usuario donde está.
public sealed class PadCalibrator : MonoBehaviour
{
    [SerializeField] DrumPad   pad;
    [SerializeField] Transform tip;
    [SerializeField] XRNode    hand = XRNode.RightHand;

    [Header("Confirmación")]
    [SerializeField, Tooltip("Vibración al calibrar. Es el único acuse de recibo que se percibe " +
                             "con el visor puesto.")]
    bool vibrarAlCalibrar = true;

    [SerializeField, Range(0f, 1f)] float amplitud = 0.8f;
    [SerializeField] float duracion = 0.12f;

    bool prevPressed;

    /// Cuántas veces se ha calibrado en esta sesión. Útil para confirmar desde la consola que
    /// el botón sí se está leyendo.
    public int Calibraciones { get; private set; }

    void Awake()
    {
        if (pad == null)
            Debug.LogError($"[PadCalibrator] '{name}': falta la referencia al DrumPad. " +
                           "El botón no va a hacer nada.", this);
        if (tip == null)
            Debug.LogError($"[PadCalibrator] '{name}': falta la referencia al Tip, la punta de " +
                           "la baqueta. El botón no va a hacer nada.", this);
    }

    void Update()
    {
        if (pad == null || tip == null) return;

        var device = InputDevices.GetDeviceAtXRNode(hand);
        if (!device.isValid) return;

        if (!device.TryGetFeatureValue(CommonUsages.primaryButton, out bool pressed)) return;

        if (pressed && !prevPressed) Calibrar(device);
        prevPressed = pressed;
    }

    void Calibrar(InputDevice device)
    {
        Vector3 destino = tip.position;
        pad.transform.position = destino;
        pad.transform.rotation = Quaternion.identity;   // normal = Vector3.up
        Calibraciones++;

        if (vibrarAlCalibrar
            && device.TryGetHapticCapabilities(out var caps)
            && caps.supportsImpulse)
        {
            device.SendHapticImpulse(0u, amplitud, duracion);
        }

        Debug.Log($"[PadCalibrator] Calibración #{Calibraciones}: pad recolocado en " +
                  $"({destino.x:F3}, {destino.y:F3}, {destino.z:F3}).", this);
    }
}
