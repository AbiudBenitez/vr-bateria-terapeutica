using UnityEngine;

/// Mantiene el visual del pad fiel a su hitbox.
///
/// Existe por un defecto real: el cilindro que representaba el pad tenía 0.50 m de radio cuando
/// el radio de golpe era 0.15, y además su cara superior quedaba 15 cm por encima del plano de
/// golpe, porque un cilindro primitivo de Unity está centrado en su origen. Se apuntaba a una
/// superficie que no era la que disparaba el sonido.
///
/// [ExecuteAlways] a propósito: la sincronización ocurre en el editor, sin entrar en play. El
/// capítulo 6 obliga a barrer armDistance para calibrar, y el visual tiene que seguir ese barrido
/// o vuelve a mentir justo mientras se mide.
[ExecuteAlways]
[RequireComponent(typeof(DrumPad))]
public sealed class PadVisual : MonoBehaviour
{
    [Header("Hijos")]
    [SerializeField] Transform piel;
    [SerializeField] Transform aro;
    [SerializeField] Transform casco;
    [SerializeField] Transform planoArmado;

    [Header("Grosores, en metros")]
    [SerializeField, Tooltip("La piel se centra en el plano de golpe: el error entre lo que se " +
                             "ve y donde golpea es la mitad de este valor.")]
    float grosorPiel = 0.010f;

    [SerializeField, Tooltip("Más DELGADO que la piel a propósito. Si fuera más grueso, su cara " +
                             "superior taparía la piel y solo se vería el aro.")]
    float grosorAro = 0.008f;

    [SerializeField] float alturaCasco = 0.120f;
    [SerializeField] float grosorPlanoArmado = 0.004f;

    [Header("Cuánto sobresalen, en radio")]
    [SerializeField] float sobresaleAro = 0.010f;
    [SerializeField] float sobresalePlanoArmado = 0.0225f;
    [SerializeField, Tooltip("Cuánto se mete el casco respecto al borde de la piel.")]
    float mengualCasco = 0.005f;

    [Header("Visibilidad")]
    [SerializeField, Tooltip("El disco translúcido que marca dónde se dispara el audio. " +
                             "Encendido para medir, se puede apagar para tocar.")]
    bool mostrarPlanoArmado = true;

    DrumPad pad;

    void OnEnable()   => Sincronizar();
    void OnValidate() => Sincronizar();

    void Update()
    {
        // En play no hace falta: nada cambia el radio en runtime, y sincronizar cada frame
        // sería trabajo tirado en el camino caliente.
        if (!Application.isPlaying) Sincronizar();
    }

    /// Deriva la geometría de los hijos a partir del DrumPad. Idempotente y sin asignaciones.
    public void Sincronizar()
    {
        if (pad == null) pad = GetComponent<DrumPad>();
        if (pad == null) return;

        float r = pad.Radius;
        float d = 2f * r;

        // Un cilindro primitivo mide diámetro 1 y ALTO 2: para alto H la escala en Y es H/2.
        Colocar(piel, d, grosorPiel, 0f);
        Colocar(aro, d + 2f * sobresaleAro, grosorAro, 0f);
        Colocar(casco, d - 2f * mengualCasco, alturaCasco,
                -(grosorPiel * 0.5f + alturaCasco * 0.5f));
        Colocar(planoArmado, d + 2f * sobresalePlanoArmado, grosorPlanoArmado, pad.ArmDistance);

        if (planoArmado != null && planoArmado.gameObject.activeSelf != mostrarPlanoArmado)
            planoArmado.gameObject.SetActive(mostrarPlanoArmado);
    }

    static void Colocar(Transform t, float diametro, float alto, float centroY)
    {
        if (t == null) return;
        t.localPosition = new Vector3(0f, centroY, 0f);
        t.localRotation = Quaternion.identity;
        t.localScale    = new Vector3(diametro, alto * 0.5f, diametro);
    }

    /// Para el constructor de editor y para las pruebas.
    public void AsignarHijos(Transform piel, Transform aro, Transform casco, Transform planoArmado)
    {
        this.piel = piel;
        this.aro = aro;
        this.casco = casco;
        this.planoArmado = planoArmado;
    }

    public Transform Piel => piel;
    public Transform PlanoArmado => planoArmado;
}
