using System.Linq;
using UnityEditor;
using UnityEngine;

/// Aplica a los samples del kit los ajustes que importan para la latencia y la memoria.
///
/// Unity importa audio con valores por defecto pensados para música de fondo, no para golpes
/// de percusión: comprime en Vorbis y descomprime al vuelo. Eso mete trabajo de decodificación
/// entre la decisión de reproducir y la salida por la bocina, que es justo el camino que este
/// proyecto pasó semanas acortando.
///
/// Se hace por script y no a mano porque son 82 archivos y basta con que uno quede mal para
/// que un golpe de los seis suene distinto sin motivo aparente.
public static class ImportarSamples
{
    const string Carpeta = "Assets/Audio/Kit";

    [MenuItem("Batería/Ajustar importación de los samples")]
    public static void Ajustar()
    {
        string[] guids = AssetDatabase.FindAssets("t:AudioClip", new[] { Carpeta });
        if (guids.Length == 0)
        {
            EditorUtility.DisplayDialog("Batería",
                $"No encontré AudioClips en {Carpeta}.", "Vale");
            return;
        }

        int cambiados = 0, yaOk = 0;
        try
        {
            AssetDatabase.StartAssetEditing();
            foreach (string guid in guids)
            {
                string ruta = AssetDatabase.GUIDToAssetPath(guid);
                var imp = AssetImporter.GetAtPath(ruta) as AudioImporter;
                if (imp == null) continue;

                var muestra = imp.defaultSampleSettings;

                bool hayQueTocar =
                    !imp.forceToMono
                    || imp.preloadAudioData != true
                    || muestra.loadType != AudioClipLoadType.DecompressOnLoad
                    || muestra.compressionFormat != AudioCompressionFormat.PCM
                    || muestra.sampleRateSetting != AudioSampleRateSetting.PreserveSampleRate;

                if (!hayQueTocar) { yaOk++; continue; }

                // Mono: DrumVoice usa spatialBlend = 0, así que el canal derecho duplica la
                // memoria sin aportar nada audible.
                imp.forceToMono = true;
                imp.preloadAudioData = true;   // evita el tirón del primer golpe de cada pieza

                muestra.loadType = AudioClipLoadType.DecompressOnLoad;
                muestra.compressionFormat = AudioCompressionFormat.PCM;
                muestra.sampleRateSetting = AudioSampleRateSetting.PreserveSampleRate;
                imp.defaultSampleSettings = muestra;

                imp.SaveAndReimport();
                cambiados++;
            }
        }
        finally
        {
            AssetDatabase.StopAssetEditing();
            AssetDatabase.Refresh();
        }

        // Cuánto ocupa el kit ya en memoria, que es el número que importa en un visor.
        double megas = AssetDatabase.FindAssets("t:AudioClip", new[] { Carpeta })
            .Select(AssetDatabase.GUIDToAssetPath)
            .Select(AssetDatabase.LoadAssetAtPath<AudioClip>)
            .Where(c => c != null)
            .Sum(c => (double)c.samples * c.channels * 2) / (1024 * 1024);

        string msg = $"{guids.Length} samples.\n" +
                     $"Ajustados: {cambiados}\nYa estaban bien: {yaOk}\n\n" +
                     $"Memoria estimada del kit: {megas:F1} MB (PCM 16 bits, mono)";
        Debug.Log("[ImportarSamples] " + msg.Replace("\n", " · "));
        EditorUtility.DisplayDialog("Batería", msg, "Vale");
    }
}
