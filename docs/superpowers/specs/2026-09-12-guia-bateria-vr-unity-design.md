# Diseño — Guía de construcción del sistema de batería VR

**Proyecto:** Simulación de Batería en Realidad Virtual con Enfoque Terapéutico
**Materia:** Administración de Proyectos de Software · UANL FIME · Equipo A
**Autor de la guía:** Abiud Misael Benítez Franco
**Fecha:** 12 de septiembre de 2026
**Estado:** Diseño aprobado, pendiente de plan de implementación

---

## 1. Propósito y alcance

Este documento diseña una **guía de aprendizaje y construcción** para levantar el sistema
funcional de percusión del prototipo VR. No es la guía; es la especificación de la guía.

**Alcance acordado: A completo + B esbozado.**

| Etapa | Contenido | Trato en la guía |
|---|---|---|
| **A** | Un pad. Suena al golpearlo. Con háptico. Corriendo en Quest 3S. Latencia medida en ms. | Completo, con código ejecutable |
| **B** | Seis piezas, capas de velocity, round-robin, pool de voces, anti-retrigger. | Arquitectura y decisiones, sin código completo |
| **C** | `SessionDirector`, `RhythmGuide`, `MetricsLogger`, STAI-6, entorno. | Fuera. Documento aparte, después de que A entregue un número de latencia aceptable |

**Por qué A primero y solo.** A es el hito Go/No-Go de latencia del acta. Si el golpe no baja
de 30 ms, las seis piezas, el round-robin y las métricas son trabajo construido sobre una base
rota. Además A obliga a atravesar la cadena completa —Unity, OpenXR, build ARM64, adb, visor—
con una escena trivial, donde depurar cuesta minutos en lugar de días.

### 1.1 Lo que esta guía NO cubre

Hand tracking (descartado en el acta), hi-hat con pedal abierto/cerrado, audio espacializado
con Meta XR Audio SDK, baqueta con Rigidbody físico, entorno 3D artístico, backend, multijugador.

---

## 2. Contexto del autor y del equipo

**Perfil de programación:** PHP y JS como lenguajes principales. POO sólida vía Java (clases,
herencia, eventos) y programas Java construidos. C y Python a nivel intermedio. **C# sin tocar.**

Consecuencia para la guía: C# no requiere enseñanza desde cero. Es Java con azúcar sintáctica.
Se resuelve con un apéndice corto de diferencias, no con un capítulo de fundamentos.

**Discrepancia de rol registrada.** El acta constitutiva v3.0 asigna a María Fernanda Montoya
Valdez como Desarrolladora VR y a Misael como Gerente de proyecto. En la práctica el desarrollo
de la batería lo ejecuta Misael. Esto es carga real fuera del rol formal y afecta el cálculo de
sobreasignación del cronograma. Queda anotado aquí para la conversación con el equipo; no se
modifica ningún documento de administración desde esta guía.

---

## 3. Entorno de desarrollo

### 3.1 Hardware — decisión de compra

**Comprar Meta Quest 3S de 128 GB ($6,600 MXN).** No el Quest 3 de 512 GB ($11,000 MXN).

| | Quest 3 | Quest 3S |
|---|---|---|
| SoC / RAM | Snapdragon XR2 Gen 2 · 8 GB | **idéntico** |
| Controles | Touch Plus | **idénticos** |
| Lentes | Pancake | Fresnel (god rays, bordes menos nítidos) |
| Resolución por ojo | 2064 × 2208 | 1832 × 1920 (−30%) |
| FOV horizontal | ~110° | ~96° |
| IPD | rueda continua 58–71 mm | 3 pasos fijos (58 / 63 / 68 mm) |
| Sensor de profundidad | LiDAR | solo iluminadores IR |
| Precio MX | $11,000 (512 GB) | $6,600 (128 GB) |

Razonamiento:

- **Mismo SoC y misma RAM.** El presupuesto de latencia (tracking + frame + buffer de audio) es
  idéntico entre ambos modelos. El riesgo dominante del proyecto no cambia ni un milisegundo.
- **LiDAR no aplica.** Sirve para reconstruir la geometría de la sala en passthrough. La app es
  VR inmersiva con iluminación bakeada. Pérdida nula.
- **128 GB sobran.** El APK pesa del orden de 150–300 MB.
- Los $4,400 de diferencia no compran nada útil para este proyecto.

Dónde sí duele el 3S, y por qué se acepta: la lente Fresnel vuelve más borroso el texto en
canvas world-space (mitigación: tipografía grande, que era necesaria de todos modos), y el IPD
de tres pasos puede incomodar en sesiones de 12 minutos. **Ese hueco lo cubre el Quest 3 que
presta la Facultad:** Quest 3 para las pruebas con usuarios del piloto, Quest 3S para el
desarrollo diario.

No comprar Quest 2 de segunda mano: lentes Fresnel *y* XR2 Gen 1, ahí sí se pierde margen real
de rendimiento.

### 3.2 Máquina de desarrollo

Se evaluaron las cuatro opciones disponibles:

| Opción | Veredicto |
|---|---|
| MacBook ARM (Apple Silicon) | **Máquina principal** |
| Laptop Arch — AMD Picasso/Raven 2, Vega integrada | Descartada para Quest Link: GPU integrada, no compatible |
| Laptop familiar — sin GPU dedicada | Descartada por lo mismo |
| PC de FIME | Descartada como máquina principal: crea dependencia de horarios de facultad, justo lo que se quiere evitar para avanzar en fines de semana |

**Quest Link es exclusivo de Windows y exige GPU dedicada** (NVIDIA GTX 1060 6 GB / 1660 /
RTX 20–50, o AMD RX 400/500/5000/6000/Vega dedicada). Ninguna máquina disponible califica.
Instalar Windows en la laptop Arch no resolvería nada: el bloqueo es la GPU integrada, no el
sistema operativo.

**Flujo de trabajo resultante:**

```
Mac ARM (Unity 6)  ──play mode──>  Meta XR Simulator   [lógica, UI, flujo de sesión]
       │
       └──build APK + adb──────>   Quest 3S            [latencia, sensación de golpe, háptico]
```

**Meta XR Simulator sí corre en Mac Apple Silicon** (requiere Unity OpenXR Plugin 1.13.0+; Mac
Intel no está soportado). Se instala como aplicación del sistema, no como paquete de Unity. Da play mode en el editor con visor y controles
simulados por mouse y teclado. Cubre el grueso del trabajo diario: máquina de estados, UI,
flujo de sesión. **No sustituye al visor** para velocidad real de mano, latencia real ni háptico.

Iteración en el visor: build APK más `adb install -r`, del orden de 1–3 minutos por ciclo. Se
planifica alrededor de eso: lotes de cambios, no un cambio por build.

### 3.3 Configuración verificable

Estos valores son el estado objetivo. La guía los presenta como lista de verificación, y el
capítulo 1 no se da por terminado hasta que todos están puestos.

**Versiones confirmadas contra la instalación real del autor (12-sep-2026).** No se actualizan
sin volver a verificar: cambiar de versión de Unity o del plugin de OpenXR a media construcción
es una de las formas más caras de perder una semana.

**Unity y paquetes**

- Unity 6 (rama 6000.x LTS), build de Apple Silicon
- Módulos: Android Build Support, OpenJDK, Android SDK & NDK Tools
- Plantilla de proyecto: **Universal 3D (URP)**. No Built-in: URP es lo que habilita single-pass
  instanced y foveated rendering en Quest
- Paquetes UPM: `com.unity.xr.openxr` (1.13 o superior), `com.unity.xr.interaction.toolkit` (3.x)
- **Meta XR Simulator: aplicación independiente, NO paquete de Unity.** El paquete
  `com.meta.xr.simulator` del Asset Store está deprecado. Se descarga de
  `developers.meta.com/horizon/downloads/package/meta-xr-simulator-mac-arm/` y el editor lo
  detecta solo. Se activa con el ícono junto a Play, o
  `Window → Meta → Meta XR Simulator → Activate`

**XR Plug-in Management**

- Pestaña Android: OpenXR activado; grupo de características **Meta Quest**; perfil de
  interacción **Oculus Touch Controller Profile**
- Pestaña de escritorio (para play mode en Mac con el simulador): OpenXR activado

**Player Settings → Android**

| Ajuste | Valor |
|---|---|
| Scripting Backend | IL2CPP |
| Target Architectures | ARM64 **solamente** (ARMv7 desmarcado) |
| Graphics APIs | Vulkan únicamente (quitar OpenGLES3) |
| Minimum API Level | Android 12L (API 32) |
| Texture compression | ASTC |
| Color Space | Linear |
| Active Input Handling | Input System (New) |

**XR Plug-in Management → OpenXR**

| Ajuste | Valor | Nota |
|---|---|---|
| Render Mode | **Single Pass Instanced** | Con OpenXR el control vive aquí, **no** en Player Settings. El `Stereo Rendering Mode` de `Player Settings → XR Settings` es el camino heredado del VR integrado de Unity y no aplica a un proyecto OpenXR |

**Project Settings → Audio** — el ajuste de mayor impacto en latencia de todo el proyecto

| Ajuste | Valor | Nota |
|---|---|---|
| DSP Buffer Size | **Best Latency** | 256 samples. El valor por defecto en Android es 512 y sube el presupuesto de ~26 ms a ~32 ms |
| System Sample Rate | 48000 | Tasa nativa del Quest. Cualquier otra fuerza remuestreo |
| Default Speaker Mode | Stereo | |

**Visor y despliegue**

- Cuenta de desarrollador verificada en developers.meta.com, con organización creada
- Modo desarrollador activado desde la app Meta Horizon del celular
- `adb` viene con Unity, bajo `PlaybackEngines/AndroidPlayer/SDK/platform-tools/adb`
- adb inalámbrico para evitar el cable: `adb tcpip 5555` y luego `adb connect <ip>:5555`

---

## 4. Capítulo 0 — Traducción de lo deprecado

El tutorial de referencia del usuario tiene alrededor de siete años y apunta a Oculus Rift con
PC. Su valor conceptual sigue vigente; sus pasos concretos, no. Este capítulo existe para poder
seguir usándolo como referencia de *ideas* sin seguir sus *instrucciones*.

| Lo que dice el tutorial viejo | Lo vigente en 2026 |
|---|---|
| Oculus Integration desde el Asset Store | Meta XR SDK vía Package Manager (UPM) |
| `OVRCameraRig`, `OVRPlayerController` | `XR Origin` del XR Interaction Toolkit |
| Oculus XR Plugin | OpenXR Plugin + grupo de características Meta Quest |
| `OVRInput.GetLocalControllerVelocity()` | `InputDevice.TryGetFeatureValue(CommonUsages.deviceVelocity, out v)` |
| `OVRInput.SetControllerVibration()` | `InputDevice.SendHapticImpulse(0, amplitud, duración)` |
| Built-in Render Pipeline | URP |
| Oculus Rift / Rift S, atado a PC | Quest 3 / 3S standalone, se despliega APK |
| Input Manager clásico | Input System |
| Multi-Pass stereo | Single Pass Instanced |
| Compresión ETC2 | ASTC |
| Unity 2018 / 2019 | Unity 6 (6000.x LTS) |

---

## 5. Estructura de la guía

Ocho capítulos. **Cada uno termina con algo que corre en el Quest 3S.** Ningún capítulo es
teórico sin producir build.

| Cap | Entregable del capítulo | Razón de existir |
|---|---|---|
| 0 | Tabla de deprecaciones | Que el tutorial viejo sirva sin desviar |
| 1 | Cubo gris girando dentro del visor | Atravesar la cadena completa con una escena trivial. Es el punto donde más gente se detiene |
| 2 | Apéndice: C# para quien viene de Java | Diferencias que muerden, no fundamentos |
| 3 | Manos que se mueven y vibran | XR Origin, lectura de pose, `deviceVelocity`, `SendHapticImpulse` |
| 4 | **El pad suena al golpearlo** | Plano, cruce, predicción, `PlayScheduled`. El corazón del documento |
| 5 | **Número de latencia real, en ms** | El hito Go/No-Go |
| 6 | Ajustes que bajan la latencia | Best Latency, 48 kHz, Vulkan, 72 vs 90 Hz. Se vuelve a medir y se compara |
| 7 | Esbozo de B | Arquitectura de las seis piezas |

Los capítulos 4 y 5 concentran alrededor del 60% del documento. Los demás existen para llegar
a ellos sin tropezar.

### 5.1 Apéndice de C# — contenido

Diez diferencias respecto de Java, elegidas por frecuencia con que causan errores reales:
`struct` frente a `class` (semántica de valor), *properties* con `get`/`set`, `[SerializeField]`
y por qué un campo privado aparece en el inspector, el `null` de Unity que no es `null` real
(`Destroy` deja el objeto en estado "fake null" y `== null` está sobrecargado), `var`, eventos
y `delegate` frente a interfaces de callback de Java, `out` y `ref`, `readonly` frente a `final`,
propiedades con cuerpo de expresión (`=>`), y ausencia de excepciones verificadas.

---

## 6. Arquitectura de A

Cinco piezas pequeñas, cada una comprobable por separado.

```
StickTracker (una por mano)            DrumPad
  lee pose y velocidad                   define plano: punto + normal + radio
  guarda la posición del frame previo    plano ARMADO desplazado +6 cm al frente
  consulta a cada pad                    distancia con signo y prueba de radio
         │                                        │
         └──────────────> DrumHit <───────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
     DrumVoice           Haptics           LatencyProbe
   PlayScheduled      SendHapticImpulse   registra dspTime y
   en dspImpact       en dspImpact        agendas tardías
```

### 6.1 Contrato entre componentes

```csharp
public readonly struct DrumHit
{
    public readonly DrumPad Pad;
    public readonly float   Velocity;    // m/s sobre la normal del pad, siempre positiva
    public readonly double  ImpactDsp;   // instante estimado del impacto, reloj DSP
    public readonly Vector3 Point;
    public readonly XRNode  Hand;

    public DrumHit(DrumPad pad, float velocity, double impactDsp, Vector3 point, XRNode hand)
    {
        Pad = pad; Velocity = velocity; ImpactDsp = impactDsp; Point = point; Hand = hand;
    }
}
```

El receptor es una clase abstracta, no una interfaz, para poder asignarla desde el inspector:

```csharp
public abstract class DrumHitSink : MonoBehaviour
{
    public abstract void Handle(in DrumHit hit);
}
```

`StickTracker` no conoce audio ni háptico: produce `DrumHit` y lo entrega a un `DrumHitSink`.
Audio, háptico y sonda de latencia son cada uno un sink, y consumen el mismo struct sin
conocerse entre sí. El sink de producción es un `DrumHitFanout` que reparte a los tres. Esto
permite probar la detección de golpe sin audio, y el audio sin visor.

### 6.2 El plano armado — la decisión central

El golpe **no** se detecta en la superficie del pad. Se detecta al cruzar un plano situado
6 cm antes. En ese punto ya se conocen velocidad y dirección, de modo que el impacto se predice:

```
t_impacto = t_cruce + (distancia_armado / velocidad_normal)
```

A 4 m/s eso son 15 ms **en el futuro**. El audio se agenda con `PlayScheduled(t_impacto)` y el
sonido sale cuando la baqueta toca el pad, no un frame después. Si el usuario frena o se retira
antes de llegar, la voz agendada se cancela.

Esto es lo que convierte los ~26 ms del presupuesto de latencia en latencia percibida cercana
a cero. Es la mitigación que el diseño técnico del proyecto ya exigía (§4.4 de
`2026-08-29-vr-percusion-terapeutica-design.md`), aquí concretada.

**Por qué no colliders.** `OnTriggerEnter` llega en el paso de física, después del cruce real,
sumando medio tick (~5–11 ms) al presupuesto. Y es vulnerable al tunelado: a 10 m/s el
controlador avanza 11 cm entre frames a 90 Hz y puede atravesar el collider sin generar evento.
La prueba de plano detecta el *cruce*, no la superposición, así que el tunelado no existe.

### 6.3 Regla de temporización

`AudioSettings.dspTime` se lee **una sola vez por frame**, al inicio de `Update()`, y ese valor
se usa durante todo el frame. Nunca `Time.time` ni `Time.deltaTime` para nada rítmico. El tiempo
de frame es irregular y acumula deriva a lo largo de una sesión de doce minutos.

### 6.4 DrumPad

```csharp
using UnityEngine;

/// Pad de percusión definido por un plano.
/// El plano de golpe pasa por transform.position con normal transform.up.
/// El plano armado está desplazado armDistance metros a lo largo de la normal.
[DisallowMultipleComponent]
public sealed class DrumPad : MonoBehaviour
{
    [Header("Geometría")]
    [SerializeField, Tooltip("Radio útil del pad, en metros.")]
    float radius = 0.15f;

    [SerializeField, Tooltip("Distancia del plano armado por delante de la superficie, en metros.")]
    float armDistance = 0.06f;

    [Header("Umbral")]
    [SerializeField, Tooltip("Velocidad normal mínima para contar como golpe, en m/s.")]
    float minVelocity = 0.4f;

    public float   ArmDistance => armDistance;
    public float   MinVelocity => minVelocity;
    public Vector3 Normal      => transform.up;
    public Vector3 Center      => transform.position;

    /// Distancia con signo al plano armado. Positiva = del lado del jugador.
    public float SignedDistanceToArmPlane(Vector3 worldPoint)
        => Vector3.Dot(worldPoint - (Center + Normal * armDistance), Normal);

    /// ¿El punto cae dentro del radio, una vez proyectado sobre el plano del pad?
    public bool WithinRadius(Vector3 worldPoint)
    {
        Vector3 flat = Vector3.ProjectOnPlane(worldPoint - Center, Normal);
        return flat.sqrMagnitude <= radius * radius;
    }
}
```

### 6.5 StickTracker

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;

public sealed class StickTracker : MonoBehaviour
{
    [SerializeField] XRNode      hand = XRNode.RightHand;
    [SerializeField] Transform   xrOrigin;    // el XR Origin de la escena
    [SerializeField] Transform   controller;  // GameObject con el TrackedPoseDriver de esta mano
    [SerializeField] Transform   tip;         // punta de la baqueta, hija de controller
    [SerializeField] DrumPad[]   pads;
    [SerializeField] DrumHitSink sink;

    InputDevice device;
    Vector3     prevTip;
    double      prevDsp;
    bool        primed;

    readonly Dictionary<DrumPad, bool> armed = new();

    void OnEnable()
    {
        device = InputDevices.GetDeviceAtXRNode(hand);
        primed = false;
        foreach (var p in pads) armed[p] = true;
    }

    void Update()
    {
        if (!device.isValid)
        {
            device = InputDevices.GetDeviceAtXRNode(hand);
            if (!device.isValid) return;
        }

        // Lectura única del reloj DSP por frame. Regla del proyecto.
        double  dspNow = AudioSettings.dspTime;
        Vector3 tipNow = tip.position;

        if (!primed)
        {
            prevTip = tipNow;
            prevDsp = dspNow;
            primed  = true;
            return;
        }

        Vector3 vTip = TipVelocity();

        foreach (var pad in pads)
            Evaluate(pad, tipNow, vTip, dspNow);

        prevTip = tipNow;
        prevDsp = dspNow;
    }

    /// Velocidad de la PUNTA, no del controlador.
    /// v_punta = v_dispositivo + ω × r, donde r va del origen del control a la punta.
    /// Con la baqueta corta de A la diferencia es menor; con baqueta larga en B es decisiva,
    /// porque el giro de muñeca aporta la mayor parte de la velocidad del extremo.
    ///
    /// CUIDADO CON LOS ESPACIOS: deviceVelocity y deviceAngularVelocity vienen en el espacio
    /// del XR Origin, mientras que tip.position y pad.Normal están en espacio de mundo.
    /// Mezclarlos da magnitudes correctas pero direcciones equivocadas en cuanto el jugador
    /// gira o el Origin no está en el origen del mundo.
    Vector3 TipVelocity()
    {
        device.TryGetFeatureValue(CommonUsages.deviceVelocity,        out Vector3 v);
        device.TryGetFeatureValue(CommonUsages.deviceAngularVelocity, out Vector3 w);

        Vector3 vWorld = xrOrigin.TransformVector(v);
        Vector3 wWorld = xrOrigin.TransformVector(w);

        Vector3 r = tip.position - controller.position;   // del control a la punta, en mundo
        return vWorld + Vector3.Cross(wWorld, r);
    }

    void Evaluate(DrumPad pad, Vector3 tipNow, Vector3 vTip, double dspNow)
    {
        float dPrev = pad.SignedDistanceToArmPlane(prevTip);
        float dNow  = pad.SignedDistanceToArmPlane(tipNow);

        // Rearme por posición: la baqueta salió del plano armado, el pad vuelve a estar vivo.
        if (dNow > 0f && dPrev <= 0f) { armed[pad] = true; return; }

        if (!armed[pad]) return;
        if (!(dPrev > 0f && dNow <= 0f)) return;          // no cruzó hacia adentro

        float vNormal = -Vector3.Dot(vTip, pad.Normal);   // acercamiento, positivo
        if (vNormal < pad.MinVelocity) return;

        // Fracción del intervalo entre frames en la que ocurrió el cruce.
        float   t01        = dPrev / (dPrev - dNow);
        Vector3 crossPoint = Vector3.Lerp(prevTip, tipNow, t01);
        if (!pad.WithinRadius(crossPoint)) return;

        double dspCross  = prevDsp + (dspNow - prevDsp) * t01;
        double dspImpact = dspCross + pad.ArmDistance / vNormal;

        armed[pad] = false;
        sink.Handle(new DrumHit(pad, vNormal, dspImpact, crossPoint, hand));
    }
}
```

**Desfase pose/audio.** La pose del controlador viene predicha al instante de presentación en
pantalla, no al instante del reloj de audio. Eso introduce un desfase constante entre `dspCross`
y el tiempo real del cruce. Se resuelve con una constante de calibración `poseToAudioOffset`
expuesta en el inspector, cuyo valor se determina empíricamente en el capítulo 6 midiendo con
distintos valores y quedándose con el que minimiza la latencia medida. No se adivina: se mide.

### 6.6 DrumVoice

```csharp
using UnityEngine;

public sealed class DrumVoice : MonoBehaviour
{
    [SerializeField] AudioClip clip;
    [SerializeField] int voices = 8;
    [SerializeField] AnimationCurve velocityToGain =
        AnimationCurve.Linear(0.4f, 0.2f, 6f, 1f);

    AudioSource[] pool;
    int next;

    void Awake()
    {
        pool = new AudioSource[voices];
        for (int i = 0; i < voices; i++)
        {
            // AddComponent en Awake, nunca en runtime.
            var src = gameObject.AddComponent<AudioSource>();
            src.clip                  = clip;
            src.playOnAwake           = false;
            src.spatialBlend          = 0f;     // 2D: sin coste de espacialización
            src.bypassEffects         = true;
            src.bypassListenerEffects = true;
            src.bypassReverbZones     = true;
            pool[i] = src;
        }
    }

    public void Play(double dspImpact, float velocity)
    {
        var src = pool[next];
        next = (next + 1) % pool.Length;

        if (src.isPlaying) src.Stop();
        src.volume = Mathf.Clamp01(velocityToGain.Evaluate(velocity));

        if (dspImpact <= AudioSettings.dspTime)
        {
            LatencyProbe.CountLateSchedule();   // la predicción no alcanzó
            src.Play();                          // ya vamos tarde, disparar de inmediato
        }
        else
        {
            src.PlayScheduled(dspImpact);
        }
    }
}
```

**Cero asignaciones en tiempo de ejecución.** Ni `Instantiate`, ni `AddComponent`, ni `new` en
el camino del golpe. El recolector de basura produce caídas de frame, y una caída de frame es
latencia.

### 6.7 Háptico

El háptico **no se puede agendar**: `SendHapticImpulse` dispara de inmediato. Si se lanza en el
cruce del plano armado, llega ~15 ms antes del impacto. Se guarda el golpe pendiente y se
dispara cuando `AudioSettings.dspTime` alcanza `ImpactDsp`, verificado en `Update()`.

```csharp
if (device.TryGetHapticCapabilities(out var caps) && caps.supportsImpulse)
    device.SendHapticImpulse(0u, Mathf.Clamp01(velocity / 6f), 0.04f);
```

---

## 7. Protocolo de medición de latencia

El método común —contar frames de video a 240 fps— tiene precisión de 4.2 ms, pobre frente a un
umbral de 30 ms. Este protocolo usa el **clic físico como verdad de referencia** y alcanza
precisión de muestra, por debajo del milisegundo.

### 7.1 Fundamento

Se coloca un objeto real —canto de mesa, libro grueso, pad de práctica— exactamente donde vive
el pad virtual. Al golpear con el control se producen **dos** sonidos:

1. El clic físico del control contra la superficie: el instante real del impacto, `t0`
2. El tambor virtual saliendo por las bocinas del visor: `t1`

Ambos se graban con el micrófono del celular en un solo archivo WAV a 48 kHz. Se abre en
Audacity y se mide la separación entre los dos transitorios.

**Δ = t1 − t0 es la latencia punta a punta**, con precisión de muestra.

### 7.2 Procedimiento

1. **Calibración.** Se apoya la punta del control en la superficie física y se presiona A: eso
   fija el plano del pad virtual sobre la superficie real. Sin este paso la medición no
   significa nada.
2. **Audio por bocinas del visor.** Nunca Bluetooth: los audífonos inalámbricos añaden 100–200 ms
   y destruyen la medición.
3. Celular a menos de 30 cm de la mesa y del visor. El sonido recorre 34 cm por milisegundo;
   más distancia y la geometría contamina el resultado.
4. **20 golpes por corrida.**
5. Se reporta **mediana y percentil 90**, nunca el mejor valor. El p90 es el que decide el
   Go/No-Go: el golpe que se siente mal es el que llega tarde, no el promedio.
6. **Dos corridas: con predicción y sin predicción.** Ese par de números es la evidencia
   documental de que la mitigación funciona, o de que no.

### 7.3 Criterio de aceptación

**−10 ms ≤ Δ(p90) ≤ +25 ms**

Δ negativo es un resultado esperado y no un error de medición: con la predicción bien calibrada
el tambor suena **antes** de que el control toque la superficie. Perceptualmente un adelanto
moderado es preferible al retraso — el oído tolera alrededor de 10 ms de adelanto y castiga con
dureza el retraso. El objetivo no es Δ = 0.

### 7.4 Sonda interna, secundaria

`LatencyProbe` registra por golpe el `dspTime` del cruce, el instante agendado, la velocidad
normal y si la agenda cayó **en el pasado** (predicción fallida: el audio sale tarde
necesariamente). El porcentaje de agendas tardías es la métrica interna de calidad.

Se serializa a JSON en almacenamiento local del visor. Es además el primer ladrillo del
`MetricsLogger` (M5) del diseño técnico.

**Limitación declarada:** la sonda interna mide solo el tramo de audio. No incluye latencia de
tracking ni de presentación. La medición externa del 7.1 es la que vale para el Go/No-Go.

---

## 8. Esbozo de B

Cuatro adiciones, ninguna trivial.

| Adición | Decisión de diseño |
|---|---|
| **Seis piezas** | Migración al esquema híbrido: collider amplio como filtro de proximidad y, dentro de él, la prueba de plano. Sin filtro serían 6 pads × 2 manos = 12 pruebas por frame. Con un solo pad el filtro no compra nada, por eso en A no está |
| **Capas de velocity** | 3 capas × 2–3 variantes round-robin por pieza. Mapeo de v (m/s) a capa y ganancia mediante `AnimationCurve` en el inspector, editable sin recompilar. Rango útil 0.5–8 m/s |
| **Pool de voces** | N `AudioSource` preinstanciados con asignación circular, dimensionado para el peor caso de redoble. Cero asignaciones en runtime |
| **Anti-retrigger** | Histéresis **por posición, no por tiempo**. El pad queda muerto hasta que la baqueta vuelve a salir del plano armado. Un cooldown temporal destruye los redobles: semicorcheas a 120 BPM son 125 ms entre golpes, y a 160 BPM son 94 ms |

Presupuesto de rendimiento heredado del diseño técnico: menos de 500 draw calls, menos de
300 000 triángulos, ASTC, iluminación bakeada sin GI en tiempo real, single-pass instanced,
foveated rendering activo, 72 Hz fijo como objetivo.

---

## 9. Riesgos de la guía

| Riesgo | Mitigación |
|---|---|
| El capítulo 1 (cadena completa hasta el visor) es donde más gente se atasca | Va primero, con escena trivial, y con la lista de verificación de §3.3 como criterio de término |
| `poseToAudioOffset` no tiene valor conocido de antemano | Se determina empíricamente en el capítulo 6, con el protocolo de §7. No se adivina |
| La velocidad de la punta con baqueta larga no es la del controlador | `TipVelocity()` incluye ω × r desde A, aunque en A el efecto sea pequeño. Así B no requiere reescribir la detección |
| Ciclo de iteración de 1–3 min en Mac desalienta el trabajo fino | El simulador cubre lógica y UI en play mode; el visor se reserva para lotes de cambios y para lo que solo él puede validar |
| La guía envejece como el tutorial de 7 años que la motivó | Cada versión fija la versión exacta de Unity y de los paquetes usados, en §3.3 |

---

## 10. Referencias

- Diseño técnico del prototipo: `docs/specs/2026-08-29-vr-percusion-terapeutica-design.md`
  (arquitectura de módulos, presupuesto de latencia, regla de `dspTime`, presupuesto de rendimiento)
- Acta constitutiva v3.0 y EDT de 42 paquetes: `entregables/Acta_Constitutiva_v3.0.docx`
- [Meta Quest 3 y 3S en México](https://about.fb.com/ltam/news/2025/05/meta-quest-3-y-quest-3s-llegan-a-mexico-el-20-de-mayo/)
- [Comparativa de especificaciones Quest 3S / 3 / 2 — Road to VR](https://roadtovr.com/quest-3s-quest-3-quest-2-specs-compared/)
- [Especificaciones del Quest 3S — UploadVR](https://www.uploadvr.com/quest-3s-specs/)
- [Meta XR Simulator, primeros pasos](https://developers.meta.com/horizon/documentation/unity/xrsim-getting-started/)
- [Soporte de Mac para Unity con Meta Quest](https://developers.meta.com/horizon/blog/mac-support-unity-meta-quest-horizon-developer/)
- [Requisitos de PC para Meta Horizon Link](https://www.meta.com/help/quest/140991407990979/)
