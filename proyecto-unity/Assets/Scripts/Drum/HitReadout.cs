using System.Text;
using TMPro;
using UnityEngine;

/// Muestra en el visor la pieza y la intensidad de los últimos golpes.
///
/// Existe por el punto 2 de la demostración del 21-sep: "se señala cómo el sistema identifica
/// la pieza y distingue tres niveles de intensidad". Sin esto, eso solo se puede AFIRMAR — se
/// oye un sonido y nada demuestra que el sistema sepa qué pieza fue ni con qué fuerza.
///
/// El golpe solo escribe datos en un buffer ya reservado; el texto se arma en Update a ritmo
/// limitado. Formatear cadenas por golpe asignaría memoria en el camino caliente.
public sealed class HitReadout : DrumHitSink
{
    [SerializeField] TMP_Text texto;

    [SerializeField, Tooltip("Cuántos golpes se muestran. Con un redoble rápido, uno solo no da " +
                             "tiempo a leerse.")]
    int historial = 5;

    [SerializeField, Tooltip("Refrescos por segundo del texto. No hace falta más: el ojo no lee " +
                             "más rápido y armar la cadena cuesta.")]
    float refrescosPorSegundo = 15f;

    HitRing anillo;
    StringBuilder sb;
    float siguienteRefresco;
    bool sucio;

    void Awake()
    {
        anillo = new HitRing(Mathf.Max(1, historial));
        sb = new StringBuilder(256);
        if (texto == null)
            Debug.LogError($"[HitReadout] '{name}' no tiene TMP_Text asignado: no se verá nada.", this);
    }

    public override void Handle(in DrumHit hit)
    {
        // Sin asignaciones. NombrePieza ya es una cadena existente, no se construye aquí.
        anillo.Agregar(hit.Pad != null ? hit.Pad.NombrePieza : "?", hit.Intensidad, hit.Velocity);
        sucio = true;
    }

    void Update()
    {
        if (!sucio || texto == null || Time.unscaledTime < siguienteRefresco) return;
        siguienteRefresco = Time.unscaledTime + 1f / Mathf.Max(1f, refrescosPorSegundo);
        sucio = false;

        anillo.Describir(sb);
        texto.SetText(sb);   // SetText(StringBuilder) no asigna, a diferencia de .text = string
    }
}
