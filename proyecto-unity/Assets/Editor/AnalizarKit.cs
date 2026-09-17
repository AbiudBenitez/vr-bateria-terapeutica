using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

/// Mide cada muestra del kit y genera un DrumKitPiece por carpeta, ORDENADO POR BRILLO.
///
/// Existe porque el orden por nombre de archivo engaña: en este pack el índice correlaciona
/// 0.97 con el pico pero −0.92 con el brillo, o sea al revés de como se comporta un tambor
/// real. Lo único fiable es medir.
public static class AnalizarKit
{
    const string Carpeta = "Assets/Audio/Kit";
    const string Destino = "Assets/Audio/Piezas";

    [MenuItem("Batería/Analizar kit")]
    public static void Analizar()
    {
        if (!Directory.Exists(Carpeta))
        {
            EditorUtility.DisplayDialog("Batería", $"No existe {Carpeta}.", "Vale");
            return;
        }
        Directory.CreateDirectory(Destino);

        var piezas = new List<(string nombre, List<(AudioClip clip, float cen, float rms, float pico)> m)>();

        foreach (string dir in Directory.GetDirectories(Carpeta))
        {
            string nombre = Path.GetFileName(dir);
            var medidas = new List<(AudioClip, float, float, float)>();

            foreach (string guid in AssetDatabase.FindAssets("t:AudioClip", new[] { dir }))
            {
                string ruta = AssetDatabase.GUIDToAssetPath(guid);
                var c = AssetDatabase.LoadAssetAtPath<AudioClip>(ruta);
                if (c == null) continue;

                var datos = new float[c.samples * c.channels];
                if (!c.GetData(datos, 0))
                {
                    Debug.LogWarning($"[AnalizarKit] No pude leer '{c.name}'. " +
                                     "¿Está en Decompress On Load? Ejecuta primero " +
                                     "'Ajustar importación de los samples'.");
                    continue;
                }

                float pico = 0f, suma = 0f;
                for (int i = 0; i < datos.Length; i++)
                {
                    float a = Mathf.Abs(datos[i]);
                    if (a > pico) pico = a;
                    suma += datos[i] * datos[i];
                }
                float rms = Mathf.Sqrt(suma / Mathf.Max(datos.Length, 1));
                medidas.Add((c, Centroide(datos, c.frequency, c.channels), rms, pico));
            }

            if (medidas.Count > 0)
            {
                medidas.Sort((a, b) => a.Item2.CompareTo(b.Item2));   // por brillo ascendente
                piezas.Add((nombre, medidas.Select(x => (x.Item1, x.Item2, x.Item3, x.Item4)).ToList()));
            }
        }

        if (piezas.Count == 0)
        {
            EditorUtility.DisplayDialog("Batería", $"No encontré AudioClips bajo {Carpeta}.", "Vale");
            return;
        }

        // Referencia de nivel: el RMS más bajo de TODO el kit.
        //
        // AudioSource.volume no puede pasar de 1, así que no se puede amplificar lo flojo: hay
        // que atenuar hacia ello. Cuesta headroom —unos 19 dB con este kit— y se compensa con
        // el volumen del visor. Es un compromiso forzado por la API, no una preferencia.
        float rmsObjetivo = piezas.SelectMany(p => p.m).Min(x => x.rms);

        var informe = new System.Text.StringBuilder();
        foreach (var (nombre, medidas) in piezas)
        {
            float cenMin = medidas.Min(x => x.cen), cenMax = medidas.Max(x => x.cen);
            float rango = cenMin > 1f ? cenMax / cenMin : 1f;

            string ruta = $"{Destino}/{nombre}.asset";
            var activo = AssetDatabase.LoadAssetAtPath<DrumKitPiece>(ruta);
            bool nuevo = activo == null;
            if (nuevo) activo = ScriptableObject.CreateInstance<DrumKitPiece>();

            activo.nombrePieza = nombre;
            activo.rangoDeBrillo = rango;
            activo.muestras = medidas.Select(x => new DrumKitPiece.Muestra
            {
                clip = x.clip,
                centroideHz = x.cen,
                // Dos topes: el primero evita recorte digital, el segundo respeta el límite
                // de AudioSource.volume.
                ganancia = Mathf.Min(rmsObjetivo / Mathf.Max(x.rms, 1e-6f),
                                     0.98f / Mathf.Max(x.pico, 1e-6f), 1f),
            }).ToArray();

            if (nuevo) AssetDatabase.CreateAsset(activo, ruta);
            EditorUtility.SetDirty(activo);

            informe.AppendLine(
                $"{nombre,-10} {medidas.Count,3} muestras · brillo {cenMin,6:F0}–{cenMax,-6:F0} Hz " +
                $"(×{rango:F2}) · {(activo.TieneEjeTimbral ? "eje timbral" : "ROUND-ROBIN, sin eje")}");
        }

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();

        string msg = informe.ToString();
        Debug.Log("[AnalizarKit]\n" + msg);
        EditorUtility.DisplayDialog("Batería",
            msg + $"\nAssets en {Destino}/\nArrastra el que toque al campo 'Pieza' del DrumVoice.",
            "Vale");
    }

    /// Centroide espectral del ataque: dónde está el centro de gravedad de la energía.
    ///
    /// CUIDADO CON EL LÍMITE SUPERIOR. La primera versión recorría 256 bandas de 1024, o sea
    /// solo hasta 5977 Hz a 48 kHz. Un platillo vive entero por encima de eso: medía 4116 Hz
    /// cuando su centroide real es 11509. Hay que barrer hasta Nyquist o los instrumentos
    /// brillantes salen todos iguales y se ordenan por ruido.
    static float Centroide(float[] datos, int frecuencia, int canales)
    {
        int n = Mathf.Min(1024, datos.Length / Mathf.Max(canales, 1));
        if (n < 64) return 0f;

        // Mono y ventana de Hann en un solo paso.
        var x = new float[n];
        for (int i = 0; i < n; i++)
        {
            float s = 0f;
            for (int c = 0; c < canales; c++) s += datos[i * canales + c];
            x[i] = s / canales * (0.5f - 0.5f * Mathf.Cos(2f * Mathf.PI * i / (n - 1)));
        }

        // DFT directa hasta Nyquist. n es pequeño y esto corre una vez, en el editor.
        float num = 0f, den = 0f;
        for (int k = 1; k <= n / 2; k++)
        {
            float re = 0f, im = 0f;
            float w = 2f * Mathf.PI * k / n;
            for (int i = 0; i < n; i++)
            {
                re += x[i] * Mathf.Cos(w * i);
                im -= x[i] * Mathf.Sin(w * i);
            }
            float mag = Mathf.Sqrt(re * re + im * im);
            num += mag * (k * (float)frecuencia / n);
            den += mag;
        }
        return den > 1e-9f ? num / den : 0f;
    }
}
