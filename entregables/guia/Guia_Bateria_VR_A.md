# Guía — Sistema de percusión VR, etapa A

**Autor:** Abiud Misael Benítez Franco · **Fecha:** 12 de septiembre de 2026
**Versiones fijadas:** Unity 6 (6000.x LTS) · OpenXR Plugin 1.13+ · XR Interaction Toolkit 3.x
**Hardware objetivo:** Meta Quest 3S · **Máquina de desarrollo:** MacBook Apple Silicon

Esta guía construye **un pad que suena al golpearlo, con háptico, corriendo en el visor, y con
la latencia medida en milisegundos**. Nada más. Las seis piezas, las capas de velocity y la
sesión terapéutica son etapas posteriores.

Cada capítulo termina con algo que corre en el Quest 3S. Si un capítulo no produjo su artefacto,
no se avanza al siguiente: los problemas de configuración se acumulan y se vuelven imposibles de
aislar.

---

## Contenido

| Cap | Título | Artefacto al terminar | Estado |
|---|---|---|---|
| 0 | Traducción de lo deprecado | Tabla de equivalencias del tutorial viejo | **Escrito** |
| 1 | Cadena completa hasta el visor | Cubo gris girando dentro del Quest 3S | **Escrito** |
| 2 | Apéndice: C# para quien viene de Java | Diferencias que muerden, no fundamentos | Pendiente |
| 3 | Manos que se mueven y vibran | `XR Origin`, pose, `deviceVelocity`, `SendHapticImpulse` | Pendiente |
| 4 | El pad suena al golpearlo | Plano armado, cruce, predicción, `PlayScheduled` | Pendiente |
| 5 | Número de latencia real, en ms | El hito Go/No-Go del acta | Pendiente |
| 6 | Ajustes que bajan la latencia | Best Latency, 48 kHz, Vulkan, 72 vs 90 Hz, remedición | Pendiente |
| 7 | Esbozo de la etapa B | Arquitectura de las seis piezas | Pendiente |

Los capítulos 4 y 5 concentran alrededor del 60% del documento final. Los demás existen para
llegar a ellos sin tropezar.

---

# Capítulo 0 — Traducción de lo deprecado

El tutorial de referencia tiene alrededor de siete años y apunta a Oculus Rift atado a una PC.
**Lo que sigue sirviendo son los conceptos.** Qué es un rig de VR y por qué la cámara no se mueve
sola sino colgada de un objeto padre que representa el suelo del jugador. Cómo se piensa la
interacción: la mano es una pose rastreada en el espacio, no un cursor, y todo lo que se agarra
o se golpea se razona en coordenadas de mundo. La idea de detectar un golpe a partir de posición
y velocidad, y de convertir esa velocidad en intensidad de sonido. El ciclo mental de trabajo:
escena, componente, inspector, play. Esa capa conceptual no ha envejecido y por eso el tutorial
todavía vale como lectura.

**Lo que ya no sirve es todo lo concreto.** Ningún paso, ningún nombre de clase, ninguna ruta de
menú, ninguna versión, ningún ajuste. Entre 2019 y 2026 cambió el SDK (Oculus Integration del
Asset Store desapareció en favor de paquetes UPM), cambió la capa de abstracción (`OVR*` cedió el
lugar a OpenXR, que es un estándar abierto y no una API de un fabricante), cambió el pipeline de
render (Built-in a URP), cambió el sistema de entrada (Input Manager a Input System) y cambió el
hardware objetivo (de un visor atado a PC a un Android ARM64 autónomo). Seguir los pasos del
tutorial en Unity 6 produce errores de compilación en el mejor caso y un proyecto que compila
pero no arranca en el visor en el peor. La tabla siguiente es el diccionario para leerlo sin
obedecerlo.

## 0.1 Tabla de equivalencias

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

## 0.2 Por qué cambió cada una

1. **Oculus Integration → Meta XR SDK por UPM.** El Asset Store entregaba un `.unitypackage` que
   volcaba cientos de archivos dentro de `Assets/`, sin control de versión ni forma limpia de
   desinstalar. UPM instala fuera de `Assets/`, resuelve dependencias y deja la versión anotada en
   `manifest.json`, que es lo que hace reproducible un proyecto entre máquinas.
2. **`OVRCameraRig` → `XR Origin`.** El rig de Oculus solo funcionaba con hardware de Oculus. El
   `XR Origin` del XR Interaction Toolkit es agnóstico: define el mismo concepto (un origen de
   espacio de juego del que cuelgan cámara y manos) sobre cualquier runtime de OpenXR, y trae el
   manejo de espacios de seguimiento — suelo o dispositivo — que antes cada SDK resolvía a su modo.
3. **Oculus XR Plugin → OpenXR Plugin + grupo Meta Quest.** El plugin de Oculus era un camino
   propietario paralelo. OpenXR es el estándar del Khronos Group que Meta adoptó como vía oficial;
   el plugin de Oculus quedó en mantenimiento. El *grupo de características* Meta Quest es la capa
   que añade encima lo específico del fabricante sin abandonar el estándar.
4. **`GetLocalControllerVelocity()` → `TryGetFeatureValue(CommonUsages.deviceVelocity)`.** La API
   vieja era un método estático que asumía que el único hardware posible era Oculus. La nueva pide
   la *característica* a un dispositivo concreto y devuelve un `bool` que dice si ese dispositivo
   la ofrece. Es más verbosa a propósito: un runtime puede no exponer velocidad, y el código debe
   poder enterarse en lugar de recibir un cero silencioso. Para este proyecto es crítico, porque la
   velocidad del golpe es el dato del que sale el volumen.
5. **`SetControllerVibration()` → `SendHapticImpulse(0, amplitud, duración)`.** La API vieja fijaba
   un estado de vibración que seguía activo hasta apagarlo. La nueva envía un impulso con duración
   explícita, que es lo que un golpe de batería necesita, y el primer argumento es el canal háptico
   — hay hardware con más de uno. Consecuencia de diseño que pesa en el capítulo 4: **el impulso no
   se puede agendar a futuro**, dispara de inmediato.
6. **Built-in → URP.** No es cosmético. URP es lo que habilita *single-pass instanced* y *foveated
   rendering* en Quest, que son las dos optimizaciones que sostienen el frame rate en un SoC móvil.
   Built-in en Quest obliga a renderizar la escena dos veces completas, una por ojo.
7. **Rift atado a PC → Quest 3 / 3S standalone.** El visor ya no es una pantalla conectada a una
   GPU de escritorio: es una computadora Android ARM64 completa. Cambia el destino del build (APK
   en lugar de ejecutable de PC), el presupuesto de rendimiento (móvil, no escritorio) y el ciclo de
   trabajo (`adb install`, no pulsar play). **Para esta guía es el cambio que más pesa:** es
   justamente lo que permite trabajar desde una Mac sin Quest Link.
8. **Input Manager → Input System.** El Input Manager clásico se sondeaba por nombre de eje en un
   archivo global y no tenía noción de dispositivos que aparecen y desaparecen ni de perfiles de
   interacción. El Input System trabaja con acciones y enlaces, que es lo que OpenXR necesita para
   mapear el mismo botón lógico a controles de fabricantes distintos. Además es requisito del XR
   Interaction Toolkit 3.x.
9. **Multi-Pass → Single Pass Instanced.** Multi-Pass dibuja la escena una vez por ojo: dos
   recorridos completos de la lista de draw calls. Single Pass Instanced emite la geometría una sola
   vez con instanciación estéreo y la GPU produce ambos ojos. Recorta cerca de la mitad del costo de
   CPU por frame, y en un Quest la CPU es el cuello de botella antes que la GPU. Menos tiempo de
   frame es menos latencia, que es el riesgo dominante del proyecto.
10. **ETC2 → ASTC.** ETC2 es el formato que exigía Android antiguo. ASTC ofrece mejor calidad por
    bit y tamaños de bloque variables, está soportado por hardware en el XR2, y es el formato que
    Meta recomienda para Quest. Con ETC2 se paga calidad de textura y peso de APK sin recibir nada
    a cambio.
11. **Unity 2018 / 2019 → Unity 6 (6000.x LTS).** Las versiones del tutorial no tienen build nativo
    de Apple Silicon, no soportan OpenXR con el grupo de Meta Quest, y su soporte de Android no
    llega al API level que el Quest 3S requiere. No es preferencia: es incompatibilidad dura.

---

# Capítulo 1 — Cadena completa hasta el visor

Este es el capítulo donde más gente se detiene, y por eso va primero y con la escena más trivial
posible. El objetivo no es aprender Unity: es demostrar que la cadena Mac → Unity → OpenXR →
build ARM64 → `adb` → Quest 3S funciona de extremo a extremo. Depurarla con un cubo cuesta
minutos; depurarla con el sistema de percusión encima cuesta días, porque cada falla admite tres
explicaciones a la vez.

Todo lo que sigue es macOS sobre Apple Silicon. **Quest Link no participa en ningún paso**: no
está disponible en esta máquina (es exclusivo de Windows y exige GPU dedicada). El ciclo de
trabajo es Meta XR Simulator en play mode dentro del editor, y build APK más `adb` al visor
físico.

## 1.1 Unity Hub y Unity 6 con los módulos de Android

1. Descargar **Unity Hub** desde `unity.com/download`. El instalador de Mac es un `.dmg`; arrastrar
   Unity Hub a Aplicaciones.
2. Iniciar sesión con la cuenta de Unity y activar la licencia **Personal**, que es gratuita y
   suficiente para este proyecto.
3. En Unity Hub, pestaña **Installs → Install Editor**, elegir una versión de **Unity 6, rama
   6000.x LTS**, en su **build de Apple Silicon** (Hub ofrece las variantes Intel y Apple Silicon;
   la correcta aquí es Apple Silicon).
4. En la pantalla de módulos marcar los tres, sin omitir ninguno:
   - **Android Build Support**
   - **OpenJDK** (hijo del anterior)
   - **Android SDK & NDK Tools** (hijo del anterior)
5. Aceptar los términos del SDK de Android y dejar correr la descarga.

**Esta descarga tarda horas.** Arrancarla antes de cualquier otra cosa y usar ese tiempo para los
pasos 1.2 y 1.3, que no dependen de Unity.

Los tres módulos son obligatorios y cada uno tiene una razón: sin Android Build Support no existe
la plataforma de destino, sin OpenJDK no se puede empaquetar el APK, y sin el NDK no hay
compilación nativa ARM64 — que es lo que exige IL2CPP, el backend de scripting que se configura
en 1.7. Instalar Unity sin los tres y descubrirlo en el paso de build es la pérdida de tiempo más
común de este capítulo.

**Verificación:** en Unity Hub → Installs, la versión instalada muestra el ícono de Android entre
sus plataformas.

## 1.2 Cuenta de desarrollador y organización en Meta

El modo desarrollador del visor no se activa con la cuenta personal: exige pertenecer a una
organización de desarrollador verificada. Es un trámite, no un paso técnico, pero bloquea todo lo
demás.

1. Entrar a **developers.meta.com** con la misma cuenta de Meta que tiene vinculado el Quest 3S.
2. Crear una **organización**. Basta el nombre; sirve el del equipo del proyecto.
3. Aceptar el acuerdo de desarrollador.
4. Completar la **verificación de la cuenta**. Meta pide confirmar identidad mediante tarjeta o
   activación de autenticación en dos pasos; la segunda vía es la rápida y no cuesta dinero.

**Verificación:** el panel de developers.meta.com muestra la organización creada y la cuenta como
verificada. Sin ese estado, el interruptor del paso 1.3 no aparece en el celular.

## 1.3 Modo desarrollador desde la app Meta Horizon

El interruptor vive en el celular, no en el visor ni en la Mac.

1. Instalar **Meta Horizon** en el celular (iOS o Android) e iniciar sesión con la misma cuenta.
2. Encender el Quest 3S y emparejarlo con la app si no lo está.
3. Abrir el visor en la app y entrar a sus ajustes de dispositivo.
4. Activar **Developer Mode / Modo desarrollador**. <!-- VERIFICAR --> La ruta exacta dentro de la app
   (Menú → Dispositivos → seleccionar el visor → Ajustes del visor → Modo desarrollador) cambia con
   las actualizaciones de Meta Horizon; verificar contra la app instalada.
5. **Reiniciar el visor.** El cambio no surte efecto hasta el reinicio.
6. Conectar el visor a la Mac por cable USB-C. Ponérselo: aparece un diálogo **"Permitir depuración
   por USB"**. Aceptar, y marcar "permitir siempre desde esta computadora".

Ese diálogo es la causa número uno de que `adb devices` muestre `unauthorized` en el paso 1.10.
Hay que tener el visor puesto para verlo.

## 1.4 Crear el proyecto — plantilla Universal 3D (URP)

En Unity Hub → **Projects → New project**, elegir la plantilla **Universal 3D (URP)** con la
versión de Unity 6 instalada, y darle un nombre sin espacios ni acentos (`BateriaVR`).

**Por qué URP y no Built-in.** URP es lo que habilita **single-pass instanced** y **foveated
rendering** en Quest. Con Built-in, la escena se renderiza dos veces completas, una por ojo, y se
pierde el foveated rendering; en un SoC móvil eso se traduce en frames más largos, y un frame más
largo es latencia añadida al golpe. El riesgo dominante del proyecto es la latencia golpe → sonido,
de modo que la elección de pipeline no es estética. Migrar de Built-in a URP más adelante obliga a
reconvertir todos los materiales: la decisión se toma aquí o se paga cara después.

No elegir la plantilla "VR" del Hub aunque exista y suene adecuada: trae paquetes y muestras
preconfiguradas que ocultan exactamente los ajustes que este capítulo pide poner a mano, y
entenderlos es el punto.

## 1.5 Paquetes

`Window → Package Manager`. Con el botón **+** de la barra superior, opción **Install package by
name**, instalar en este orden: <!-- VERIFICAR --> el rótulo exacto de esa opción en el Package
Manager de Unity 6 puede diferir ("Install package by name…" / "Add package by name"); es el mismo
flujo.

| Paquete | Nombre exacto | Versión |
|---|---|---|
| OpenXR Plugin | `com.unity.xr.openxr` | 1.13 o superior |
| XR Interaction Toolkit | `com.unity.xr.interaction.toolkit` | 3.x |
| Meta XR Simulator | `com.meta.xr.simulator` | la que corresponda al SDK v66 o superior |

Notas que ahorran tiempo:

- El XR Interaction Toolkit 3.x **arrastra el Input System** como dependencia. Unity pedirá
  reiniciar el editor para habilitarlo; aceptar. Ese reinicio es el que deja `Active Input Handling`
  en `Input System (New)`, el valor que la lista de 1.7 exige.
- El **Meta XR Simulator** es lo que permite play mode con visor y controles simulados por mouse y
  teclado dentro del editor en la Mac. Requiere **OpenXR Plugin 1.13+** y **Meta XR SDK v66+**;
  corre en Apple Silicon, no en Mac Intel. Cubre lógica, UI y flujo de sesión. **No sustituye al
  visor** para velocidad real de mano, latencia real ni háptico: esos tres solo se validan en el
  Quest 3S.
- Si `com.meta.xr.simulator` no aparece por nombre, se instala desde el registro de Meta con el
  Meta XR SDK. <!-- VERIFICAR --> El registro con alcance (`scoped registry`) de Meta y su URL deben
  confirmarse contra la documentación vigente de Meta XR Simulator.

## 1.6 XR Plug-in Management

`Edit → Project Settings → XR Plug-in Management`. Si el panel ofrece instalar el paquete, ya está
instalado desde 1.5.

**Pestaña Android** (ícono del robot):

- Marcar **OpenXR**.
- Dentro de OpenXR, activar el grupo de características **Meta Quest**.
- En **Interaction Profiles**, añadir **Oculus Touch Controller Profile**.

**Pestaña de escritorio** (la de macOS / standalone):

- Marcar **OpenXR**. Este es el que hace funcionar el **Meta XR Simulator en play mode dentro de la
  Mac**. Es fácil de olvidar porque el destino final es Android, y su ausencia se manifiesta como un
  play mode que corre en 2D sin ningún error visible.

Si el panel de OpenXR muestra triángulos amarillos o rojos de validación, resolverlos ahora: casi
todos son ajustes de 1.7 que aún no se han puesto, y el botón **Fix** los aplica.

## 1.7 Lista de verificación — Player Settings → Android

`Edit → Project Settings → Player`, pestaña Android. Estos valores son el estado objetivo; el
capítulo no se da por terminado hasta que los ocho están puestos.

| Ajuste | Valor |
|---|---|
| Scripting Backend | IL2CPP |
| Target Architectures | ARM64 **solamente** (ARMv7 desmarcado) |
| Graphics APIs | Vulkan únicamente (quitar OpenGLES3) |
| Minimum API Level | Android 12L (API 32) |
| Texture compression | ASTC |
| Color Space | Linear |
| Stereo Rendering Mode | Single Pass Instanced |
| Active Input Handling | Input System (New) |

Apuntes de dónde vive cada uno y qué pasa si falta:

- **Scripting Backend, Target Architectures, Minimum API Level, Color Space, Active Input Handling**
  están en `Player Settings → Android → Other Settings`. IL2CPP con ARM64 es requisito de la Quest
  Store y del propio visor: Mono o ARMv7 producen un APK que el Quest 3S rechaza o que instala y no
  arranca.
- **Graphics APIs** también está en `Other Settings`: hay que desmarcar **Auto Graphics API** para
  poder editar la lista y quitar OpenGLES3. Dejar OpenGLES3 en la lista es peligroso porque, si
  Vulkan falla en tiempo de arranque, el visor cae silenciosamente al camino lento y las mediciones
  de latencia del capítulo 5 dejan de significar nada.
- **Texture compression = ASTC** en `Player Settings → Android`. Si el perfil de build también
  expone un selector de compresión de texturas, dejar ASTC en los dos: el que se aplica es el del
  build, y una discrepancia entre ambos se manifiesta como texturas ETC2 en el APK sin aviso alguno.
- **Stereo Rendering Mode = Single Pass Instanced** en `Player Settings → Android`. Si en esta
  instalación el control no aparece ahí, está como **Render Mode** dentro de
  `XR Plug-in Management → OpenXR` <!-- VERIFICAR -->; el valor exigido es el mismo y debe quedar en
  Single Pass Instanced esté donde esté el interruptor. Es lo que evita renderizar la escena dos
  veces, una por ojo, y por lo tanto es parte del presupuesto de latencia.
- **Color Space = Linear** es requisito de URP. En Gamma, la iluminación se ve mal y algunos efectos
  de URP directamente no funcionan.

## 1.8 Lista de verificación — Project Settings → Audio

`Edit → Project Settings → Audio`.

| Ajuste | Valor | Nota |
|---|---|---|
| DSP Buffer Size | **Best Latency** | 256 samples. El valor por defecto en Android es 512 y sube el presupuesto de ~26 ms a ~32 ms |
| System Sample Rate | 48000 | Tasa nativa del Quest. Cualquier otra fuerza remuestreo |
| Default Speaker Mode | Stereo | |

**Advertencia: `DSP Buffer Size` en "Best Latency" es el ajuste de mayor impacto en latencia de
todo el proyecto.** Un solo desplegable decide alrededor de 6 ms del presupuesto, y el presupuesto
completo es de ~26 ms contra un umbral de 30 ms. Dejarlo en el valor por defecto consume de golpe
la quinta parte del margen disponible, antes de escribir una línea de código de percusión.

`System Sample Rate` en 48000 elimina el remuestreo: el Quest reproduce a 48 kHz de forma nativa y
cualquier otra tasa obliga al runtime a convertir, lo que añade trabajo y retardo por cada voz.
`Default Speaker Mode` en Stereo es el que corresponde a las bocinas del visor, y es también el
modo bajo el que se hará la medición externa de latencia del capítulo 5.

Estos tres valores se vuelven a tocar en el capítulo 6, ya con un número de latencia medido
delante, para comparar el efecto real de cada uno. Aquí se ponen y se dejan.

## 1.9 Escena trivial

1. `File → New Scene`, plantilla básica de URP, y guardarla como `Assets/Scenes/Cap01_Cubo.unity`.
2. `GameObject → 3D Object → Cube`. Dejarlo en `(0, 1, -2)` para que quede a la altura de la vista y
   por delante del origen, que es donde nace el `XR Origin`.
3. Crear el script: en el Project, `Assets/Scripts/`, clic derecho → `Create → MonoBehaviour Script`
   con el nombre `CuboQueGira`. <!-- VERIFICAR --> En Unity 6 el rótulo del menú de creación de
   scripts cambió respecto de `Create → C# Script`; el nombre del archivo debe coincidir exactamente
   con el de la clase, se llame como se llame la opción.
4. Pegar exactamente esto:

```csharp
using UnityEngine;

public sealed class CuboQueGira : MonoBehaviour
{
    [SerializeField] float gradosPorSegundo = 45f;

    void Update() => transform.Rotate(Vector3.up, gradosPorSegundo * Time.deltaTime);
}
```

5. Arrastrar el script al cubo. En el inspector debe aparecer el campo **Grados Por Segundo** con
   valor 45.
6. Añadir el rig de VR: `GameObject → XR → XR Origin (VR)`. Borrar la `Main Camera` que trae la
   escena por defecto, porque el `XR Origin` aporta la suya y dos cámaras compiten.

Dos cosas que se ven aquí y conviene registrar ahora, porque reaparecen en todo el proyecto:
`[SerializeField]` sobre un campo privado es lo que lo hace visible y editable en el inspector sin
volverlo público — se ajusta el valor sin recompilar; y `Time.deltaTime` es legítimo **solo** para
cosas visuales como este giro. **Nunca para nada rítmico**: a partir del capítulo 4 el reloj es
`AudioSettings.dspTime`, leído una sola vez por frame, porque el tiempo de frame es irregular y
acumula deriva a lo largo de una sesión de doce minutos.

7. Pulsar **Play**. Con el Meta XR Simulator activo debe aparecer la ventana del simulador con el
   cubo girando, navegable con mouse y teclado. <!-- VERIFICAR --> El punto de activación del
   simulador (un menú propio del paquete de Meta dentro del editor) debe confirmarse contra la
   documentación de Meta XR Simulator para la versión instalada.

Que funcione en el simulador **no cierra el capítulo**. Falta el visor.

## 1.10 Build y despliegue con adb

Abrir el perfil de build de Android <!-- VERIFICAR --> (`File → Build Profiles` en Unity 6; en
versiones anteriores era `File → Build Settings`), seleccionar **Android** y pulsar **Switch
Platform**. El primer cambio de plataforma reimporta todos los assets con compresión ASTC y tarda
varios minutos.

Agregar la escena a la lista de escenas del build, y construir a `Builds/bateria.apk`. El primer
build con IL2CPP tarda; los siguientes son de 1 a 3 minutos. Se planifica alrededor de eso: **lotes
de cambios, no un cambio por build.**

`adb` viene con Unity, no hay que instalar Android Studio:

```bash
ADB=~/Library/Application\ Support/Unity/Hub/Editor/*/PlaybackEngines/AndroidPlayer/SDK/platform-tools/adb
$ADB devices                          # debe listar el visor como "device", no "unauthorized"
$ADB install -r Builds/bateria.apk
```

`-r` reinstala sobre la versión existente conservando los datos de la app, que es lo que se quiere
en cada iteración.

Para quitar el cable, con el visor conectado por USB la primera vez:

```bash
$ADB tcpip 5555
$ADB shell ip route | awk '{print $9}'   # imprime la IP del visor
$ADB connect <IP>:5555
```

A partir de ahí se desconecta el cable y `$ADB install -r` funciona por la red local. La conexión
inalámbrica se pierde al reiniciar el visor o al cambiar de red: se repite la secuencia con cable.

Para lanzar la app en el visor: menú de aplicaciones → filtro **Fuentes desconocidas** (las apps
instaladas por `adb` no aparecen en la biblioteca normal).

## 1.11 Problemas frecuentes

| Síntoma | Causa | Qué hacer |
|---|---|---|
| `$ADB devices` lista el visor como `unauthorized` | No se aceptó el diálogo de depuración USB **dentro del visor** | Ponerse el visor con el cable conectado, aceptar "Permitir depuración por USB" y marcar "permitir siempre". Si el diálogo no aparece: `$ADB kill-server`, desconectar y reconectar el cable |
| `$ADB devices` no lista nada | Cable de solo carga, o modo desarrollador no activado / visor sin reiniciar tras activarlo | Usar un cable USB-C de datos, verificar el interruptor en Meta Horizon y reiniciar el visor |
| El build falla con error de NDK ausente o ruta de NDK inválida | Se instaló Unity sin el módulo **Android SDK & NDK Tools**; IL2CPP no puede compilar a nativo ARM64 sin él | Unity Hub → Installs → engranaje de la versión → **Add modules** → marcar Android SDK & NDK Tools, y reiniciar el editor |
| La app arranca **en 2D**, como pantalla plana flotante, en lugar de VR | Falta el `XR Origin` en la escena, o **OpenXR no está activado en la pestaña Android** de XR Plug-in Management | Añadir `GameObject → XR → XR Origin (VR)` y borrar la `Main Camera` duplicada; revisar 1.6. Si falla solo en play mode en la Mac, lo que falta es OpenXR en la **pestaña de escritorio** |
| El APK instala pero no aparece en el visor | Las apps instaladas por `adb` no van a la biblioteca normal | Buscarla en el menú de aplicaciones bajo el filtro **Fuentes desconocidas** |
| `$ADB install` falla con `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | Ya hay una versión instalada firmada con otra clave | `$ADB uninstall <package name>` y volver a instalar |
| El build sale con `Target Architectures` en ARMv7 o el visor rechaza el APK | ARMv7 marcado o Scripting Backend en Mono | Revisar la lista de 1.7: IL2CPP + ARM64 solamente |
| El audio suena arenoso o con retardo perceptible desde el primer día | `DSP Buffer Size` quedó en el valor por defecto (512 samples) o el sample rate no es 48000 | Revisar 1.8. Es el ajuste de mayor impacto en latencia del proyecto |
| Play mode en la Mac corre pero sin visor ni controles simulados | Falta OpenXR en la pestaña de escritorio, o el Meta XR Simulator no está activo | Revisar 1.6 y el activador del simulador en 1.9 |

---

**Criterio de término: un cubo gris girando dentro del Quest 3S, desplegado desde la Mac. Sin esto
no se avanza.**
