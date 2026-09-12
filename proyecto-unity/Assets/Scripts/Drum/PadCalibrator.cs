using UnityEngine;
using UnityEngine.XR;

/// Coloca el pad virtual exactamente donde está la superficie física de medición.
/// Se apoya la punta del control sobre la superficie y se presiona el botón primario:
/// el pad se mueve a ese punto, con la normal apuntando hacia arriba en el mundo.
public sealed class PadCalibrator : MonoBehaviour
{
    [SerializeField] DrumPad   pad;
    [SerializeField] Transform tip;
    [SerializeField] XRNode    hand = XRNode.RightHand;

    bool prevPressed;

    void Update()
    {
        var device = InputDevices.GetDeviceAtXRNode(hand);
        if (!device.isValid) return;

        if (!device.TryGetFeatureValue(CommonUsages.primaryButton, out bool pressed)) return;

        if (pressed && !prevPressed)
        {
            pad.transform.position = tip.position;
            pad.transform.rotation = Quaternion.identity;   // normal = Vector3.up
            Debug.Log($"[PadCalibrator] Pad recolocado en {tip.position}");
        }
        prevPressed = pressed;
    }
}
