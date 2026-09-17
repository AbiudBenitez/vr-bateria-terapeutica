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
    [SerializeField, Tooltip("Pad de REFERENCIA: el que quedará bajo la punta al calibrar.")]
    DrumPad pad;

    [SerializeField, Tooltip("Qué se mueve. Con un solo pad, su propio Transform. Con un kit " +
                             "de seis piezas, la raíz del kit: así todo se desplaza junto y la " +
                             "disposición se conserva. Vacío = se mueve el pad de referencia.")]
    Transform objetivo;

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
        // Se aplica un DESPLAZAMIENTO, no una posición absoluta. Con un kit de seis piezas,
        // teletransportar la raíz a la punta lo mandaría todo a otro sitio; lo que se quiere es
        // que el pad de referencia acabe bajo la punta y el resto lo acompañe.
        Transform mueve = objetivo != null ? objetivo : pad.transform;
        Vector3 delta = tip.position - pad.Center;
        mueve.position += delta;

        Calibraciones++;

        if (vibrarAlCalibrar
            && device.TryGetHapticCapabilities(out var caps)
            && caps.supportsImpulse)
        {
            device.SendHapticImpulse(0u, amplitud, duracion);
        }

        Debug.Log($"[PadCalibrator] Calibración #{Calibraciones}: '{mueve.name}' desplazado " +
                  $"({delta.x:+F3}, {delta.y:+F3}, {delta.z:+F3}) m para poner " +
                  $"'{pad.name}' bajo la punta.", this);
    }
}
