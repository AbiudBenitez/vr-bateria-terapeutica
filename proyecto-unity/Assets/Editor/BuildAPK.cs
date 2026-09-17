using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine;

/// Compila el APK con los ajustes fijados, desde el menú o desde la línea de comandos.
///
/// Existe para que el build sea reproducible. Compilar a mano desde Build Profiles funciona,
/// pero depende de que los interruptores estén como deben, y varios de ellos —ARM64, IL2CPP,
/// Vulkan— forman parte del presupuesto de latencia: si alguien los cambia y compila, la app
/// arranca igual y las mediciones dejan de describir el sistema que se cree estar midiendo.
/// Aquí se comprueban antes de compilar y el build falla si no cuadran.
public static class BuildAPK
{
    const string Salida = "Builds/bateria.apk";

    [MenuItem("Batería/Compilar APK")]
    public static void DesdeMenu()
    {
        var reporte = Compilar();
        if (reporte == null) return;

        bool ok = reporte.summary.result == BuildResult.Succeeded;
        EditorUtility.DisplayDialog("Batería",
            ok
                ? $"APK compilado.\n\n{Salida}\n" +
                  $"{reporte.summary.totalSize / (1024 * 1024)} MB en " +
                  $"{reporte.summary.totalTime.TotalMinutes:F1} min.\n\n" +
                  "Para instalarlo:\n  $ADB install -r " + Salida
                : $"El build falló: {reporte.summary.result}.\nRevisa la consola.",
            "Vale");
    }

    /// Punto de entrada para batchmode:
    ///   Unity -batchmode -quit -projectPath &lt;ruta&gt; -executeMethod BuildAPK.DesdeLinea -logFile -
    public static void DesdeLinea()
    {
        var reporte = Compilar();
        bool ok = reporte != null && reporte.summary.result == BuildResult.Succeeded;
        // El código de salida es lo único que ve un script que llame a esto.
        EditorApplication.Exit(ok ? 0 : 1);
    }

    static BuildReport Compilar()
    {
        string[] escenas = EditorBuildSettings.scenes
            .Where(s => s.enabled)
            .Select(s => s.path)
            .ToArray();

        if (escenas.Length == 0)
        {
            Debug.LogError("[BuildAPK] No hay escenas habilitadas en Build Profiles. " +
                           "El APK arrancaría en negro.");
            return null;
        }

        if (!Verificar()) return null;

        Directory.CreateDirectory(Path.GetDirectoryName(Salida) ?? "Builds");

        if (EditorUserBuildSettings.activeBuildTarget != BuildTarget.Android)
        {
            Debug.Log("[BuildAPK] Cambiando la plataforma activa a Android. " +
                      "La primera vez reimporta todos los assets y tarda varios minutos.");
            EditorUserBuildSettings.SwitchActiveBuildTarget(
                BuildTargetGroup.Android, BuildTarget.Android);
        }

        Debug.Log($"[BuildAPK] Compilando {escenas.Length} escena(s): " +
                  string.Join(", ", escenas));

        var reporte = BuildPipeline.BuildPlayer(new BuildPlayerOptions
        {
            scenes = escenas,
            locationPathName = Salida,
            target = BuildTarget.Android,
            targetGroup = BuildTargetGroup.Android,
            options = BuildOptions.None,
        });

        var r = reporte.summary;
        if (r.result == BuildResult.Succeeded)
            Debug.Log($"[BuildAPK] OK. {Salida} · {r.totalSize / (1024 * 1024)} MB · " +
                      $"{r.totalTime.TotalMinutes:F1} min");
        else
            Debug.LogError($"[BuildAPK] Falló: {r.result}. {r.totalErrors} error(es).");

        return reporte;
    }

    /// Los ajustes que forman parte del presupuesto de latencia. Si alguno se movió, el build
    /// se detiene: es preferible no compilar a compilar algo que mide otra cosa.
    static bool Verificar()
    {
        bool ok = true;

        void Exigir(bool condicion, string queja)
        {
            if (condicion) return;
            Debug.LogError($"[BuildAPK] {queja}");
            ok = false;
        }

        Exigir(PlayerSettings.GetScriptingBackend(NamedBuildTarget.Android)
                   == ScriptingImplementation.IL2CPP,
               "El Scripting Backend no es IL2CPP. Con Mono el APK no arranca en Quest.");

        Exigir(PlayerSettings.Android.targetArchitectures == AndroidArchitecture.ARM64,
               "Target Architectures debe ser solo ARM64.");

        var apis = PlayerSettings.GetGraphicsAPIs(BuildTarget.Android);
        Exigir(apis.Length > 0 && apis[0] == UnityEngine.Rendering.GraphicsDeviceType.Vulkan,
               "La primera Graphics API debe ser Vulkan.");
        Exigir(apis.All(a => a != UnityEngine.Rendering.GraphicsDeviceType.OpenGLES3),
               "OpenGLES3 sigue en la lista de Graphics APIs. Si Vulkan falla al arrancar, el " +
               "visor cae al camino lento en silencio y las mediciones dejan de valer.");

        // Estos dos van como AVISO y no bloquean: AudioSettings.GetConfiguration() devuelve la
        // configuración del editor, que puede no reflejar un override de la plataforma Android.
        // Un falso positivo aquí detendría un build correcto, y eso es peor que no avisar.
        var conf = AudioSettings.GetConfiguration();
        if (conf.sampleRate != 48000)
            Debug.LogWarning($"[BuildAPK] Sample rate {conf.sampleRate}, se esperaba 48000. " +
                             "Compruébalo en Project Settings → Audio.");
        if (conf.dspBufferSize > 256)
            Debug.LogWarning($"[BuildAPK] DSP Buffer Size {conf.dspBufferSize} samples. " +
                             "Con Best Latency (256) el presupuesto de latencia baja unos 6 ms. " +
                             "Compruébalo en Project Settings → Audio.");

        Exigir(!PlayerSettings.applicationIdentifier.Contains("UnityTechnologies")
               && !PlayerSettings.applicationIdentifier.Contains("template"),
               $"El package id sigue siendo el de la plantilla: " +
               $"'{PlayerSettings.applicationIdentifier}'.");

        if (!ok)
            Debug.LogError("[BuildAPK] Build detenido. Corrige lo de arriba y vuelve a intentarlo.");
        return ok;
    }
}
