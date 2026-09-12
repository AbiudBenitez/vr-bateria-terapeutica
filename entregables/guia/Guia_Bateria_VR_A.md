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
| 2 | Apéndice: C# para quien viene de Java | Diferencias que muerden, no fundamentos | **Escrito** |
| 3 | Manos que se mueven y vibran | `XR Origin`, pose, `deviceVelocity`, `SendHapticImpulse` | **Escrito** |
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
3. Tocar el **ícono del visor** en la barra de herramientas de la app. El visor emparejado aparece
   arriba, con su modelo y estado.
4. Tocar el visor → **Headset Settings / Ajustes del visor** → **Developer Mode / Modo desarrollador**
   → activar el interruptor.
5. **Reiniciar el visor.** El cambio no surte efecto hasta el reinicio.
6. Ya con el visor puesto: **Quick Settings → Settings → Developer** y activar **MTP Notification**.
   Sin esto el diálogo de depuración por USB puede no aparecer.
7. Conectar el visor a la Mac por cable USB-C. Ponérselo: aparece un diálogo **"Permitir depuración
   por USB"**. Aceptar, y marcar "permitir siempre desde esta computadora".

Ese diálogo es la causa número uno de que `adb devices` muestre `unauthorized` en el paso 1.10.
Hay que tener el visor puesto para verlo.

**Requisito previo:** hay que ser desarrollador registrado de Meta, con cuenta verificada y mayoría
de edad. Eso es lo que se resolvió en 1.2; sin ello el interruptor de modo desarrollador no aparece.

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

`Window → Package Manager`. Con el botón **+** de la barra superior, **Install package by name**,
instalar en este orden:

| Paquete | Nombre exacto | Versión |
|---|---|---|
| OpenXR Plugin | `com.unity.xr.openxr` | 1.13 o superior |
| XR Interaction Toolkit | `com.unity.xr.interaction.toolkit` | 3.x |

Son dos, no tres. **El Meta XR Simulator ya no se instala como paquete de Unity** — ver abajo.

Notas que ahorran tiempo:

- El XR Interaction Toolkit 3.x **arrastra el Input System** como dependencia. Unity pedirá
  reiniciar el editor para habilitarlo; aceptar. Ese reinicio es el que deja `Active Input Handling`
  en `Input System (New)`, el valor que la lista de 1.7 exige.

### Meta XR Simulator — aplicación aparte, no paquete

**El paquete `com.meta.xr.simulator` del Asset Store está deprecado.** Meta distribuye ahora el
simulador como **aplicación independiente** que se descarga de su portal:

- macOS Apple Silicon: `developers.meta.com/horizon/downloads/package/meta-xr-simulator-mac-arm/`
- Requisitos: **macOS ARM únicamente** (Mac Intel no está soportado) y **Unity OpenXR Plugin 1.13.0
  o posterior**, que es justo el que instalaste arriba.

Se instala una vez en el sistema; el editor lo detecta solo. No hay registro con alcance que
configurar ni paquete que añadir al `manifest.json`.

El simulador es lo que permite play mode con visor y controles simulados por mouse y teclado dentro
del editor en la Mac. Cubre lógica, UI y flujo de sesión. **No sustituye al visor** para velocidad
real de mano, latencia real ni háptico: esos tres solo se validan en el Quest 3S.

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
- **Single Pass Instanced** vive en `Edit → Project Settings → XR Plug-in Management → OpenXR`, en
  el desplegable **Render Mode**. **No** en Player Settings. El `Stereo Rendering Mode` de
  `Player Settings → XR Settings` es el camino heredado del VR integrado de Unity, exige marcar
  "Virtual Reality Supported" y no aplica a un proyecto con OpenXR: buscarlo ahí es perder la tarde.
  Cada proveedor de XR expone su propio control, y con OpenXR el control es Render Mode.
  Es lo que evita renderizar la escena dos veces, una por ojo, y por lo tanto es parte del
  presupuesto de latencia.
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
3. Crear el script: en el Project, `Assets/Scripts/`, clic derecho →
   `Create → Scripting → MonoBehaviour Script`, con el nombre `CuboQueGira`. En Unity 6 la creación
   de scripts se movió a un submenú **Scripting**; el `Create → C# Script` suelto que aparece en
   tutoriales viejos ya no está en la raíz del menú.

   **El nombre del archivo debe coincidir exactamente con el de la clase.** Unity no compila un
   `MonoBehaviour` cuyo archivo se llame distinto, y el error que da no lo dice claramente.
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

7. Activar el simulador: **ícono del simulador junto al botón Play** en la barra de herramientas, o
   `Window → Meta → Meta XR Simulator → Activate`. La consola imprime
   `[Meta XR Simulator is activated]`. Para apagarlo, `Deactivate` en el mismo menú; `Status` dice
   en qué estado está.

8. Pulsar **Play**. Debe abrirse la ventana del simulador con el cubo girando, navegable con mouse
   y teclado.

Que funcione en el simulador **no cierra el capítulo**. Falta el visor.

## 1.10 Build y despliegue con adb

Abrir `File → Build Profiles` (en Unity 6 reemplazó a `File → Build Settings`, que es como lo
nombran los tutoriales viejos), seleccionar **Android** y pulsar **Switch Platform**. El primer cambio de plataforma reimporta todos los assets con compresión ASTC y tarda
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

---

# Capítulo 2 — Apéndice: C# para quien viene de Java

Esto no es un curso de C#. C# y Java comparten sintaxis, tipado estático, recolección de basura,
clases, interfaces, genéricos y herencia simple con interfaces múltiples. Quien escribió Java
escribe C# el primer día. Lo que muerde son diez diferencias concretas, y todas aparecen en el
código de este proyecto. Este capítulo es una tabla de consulta: se lee de corrido una vez y se
vuelve a él cuando algo no compila o se comporta raro.

Los ejemplos de C# están tomados de `proyecto-unity/Assets/Scripts/Drum/`.

## 2.1 `struct` frente a `class` — semántica de valor

En Java todo objeto es referencia. En C# un `struct` es un **tipo por valor**: se copia al
asignarlo y al pasarlo, vive en la pila cuando es local y **no genera basura**.

```java
// Java: DrumHit sería una clase; cada golpe es una asignación en el heap
final class DrumHit { final float velocity; /* ... */ }
```

```csharp
// C#: readonly struct. Se copia, no se asigna en el heap, no alimenta al recolector.
public readonly struct DrumHit { public readonly float Velocity; /* ... */ }
```

**Por qué `DrumHit` es struct.** Está en el camino caliente: se crea en cada golpe, dentro de
`Update()`. Como clase, cada golpe sería una asignación en el heap, y el recolector de basura
produce caídas de frame. Una caída de frame es latencia, que es el riesgo dominante del proyecto.

## 2.2 Properties y la forma de expresión `=>`

Java resuelve el encapsulamiento con métodos `getX()`. C# tiene *properties*: se usan como campos
y se implementan como métodos.

```java
private float armDistance;
public float getArmDistance() { return armDistance; }   // pad.getArmDistance()
```

```csharp
[SerializeField] float armDistance = 0.06f;
public float ArmDistance => armDistance;                 // pad.ArmDistance
```

El `=>` es la **forma de expresión**: cuerpo de una sola expresión, sin llaves ni `return`. Sirve
también para métodos: `public static float NormalSpeed(Vector3 v, Vector3 n) => -Vector3.Dot(v, n);`
Convención: las properties públicas van en `PascalCase`, los campos privados en `camelCase`.

## 2.3 `[SerializeField]` — privado pero visible en el inspector

Unity muestra en el inspector los campos **públicos** y los privados marcados con
`[SerializeField]`. La segunda vía es la correcta.

```java
public float radius = 0.15f;      // cualquiera lo escribe desde cualquier parte
```

```csharp
[SerializeField, Tooltip("Radio útil del pad, en metros.")]
float radius = 0.15f;             // editable en el inspector, invisible para el resto del código
```

Hacerlo público para verlo en el inspector rompe el encapsulamiento a cambio de nada: el valor se
ajusta igual, sin recompilar, y el código externo no puede tocarlo. `[Tooltip]`, `[Header]`,
`[Min(1)]` y `[Range]` documentan y validan el campo en la propia interfaz del editor.

## 2.4 El `null` de Unity que no es `null`

**Ésta es la diferencia que más tiempo cuesta.** `Object.Destroy` no borra el objeto administrado
de C#: lo deja marcado como destruido del lado nativo. Unity **sobrecarga el operador `==`** para
que ese objeto se compare igual a `null` aunque la referencia siga existiendo.

```java
if (obj != null) obj.doThing();          // Java: null es null, no hay ambigüedad
```

```csharp
if (go != null) Object.DestroyImmediate(go);   // usa el == sobrecargado: correcto
go?.DoThing();                                 // ?. NO usa la sobrecarga: entra y revienta
```

Los operadores `?.`, `??` y `??=` están definidos por el lenguaje y **no llaman a la sobrecarga**:
sobre un `MonoBehaviour` destruido ven una referencia no nula y ejecutan la llamada, que falla con
`MissingReferenceException`. Regla del proyecto: sobre cualquier cosa derivada de
`UnityEngine.Object` se compara con `!= null` explícito, nunca con `?.`. Por eso `DrumHitFanout`
escribe `if (targets[i] != null)` y no `targets[i]?.Handle(in hit)`.

## 2.5 `var`

Inferencia de tipo en variables locales. Equivale al `var` de Java 10+, y en C# existe desde 2007,
así que su uso es idiomático, no exótico.

```java
InputDevice device = InputDevices.getDeviceAtXRNode(hand);
```

```csharp
var device = InputDevices.GetDeviceAtXRNode(hand);   // el tipo es evidente por el nombre
var src    = pool[next];                             // AudioSource, obvio por el contexto
```

Solo vale para locales, exige inicializador, y no cambia nada en tiempo de ejecución: el tipo
sigue siendo estático. Se usa cuando el tipo ya está escrito a la derecha; se escribe explícito
cuando no lo está (`float dPrev = ...`).

## 2.6 Eventos y `delegate` frente a las interfaces de callback de Java

Java simula los callbacks con interfaces de un método (`Runnable`, `ActionListener`). C# tiene
tipos función de primera clase: `delegate`, `Action<T>`, `Func<T>` y `event`.

```java
button.addListener(new Listener() { public void onHit(DrumHit h) { play(h); } });
```

```csharp
public event System.Action<DrumHit> OnHit;   // declaración
OnHit += h => Play(h);                       // suscripción
OnHit?.Invoke(hit);                          // disparo, seguro si nadie escucha
```

**Este proyecto no los usa, a propósito.** `DrumHitSink` es una clase abstracta que hereda de
`MonoBehaviour` porque Unity **no serializa** campos de tipo delegado ni de tipo interfaz: no se
podrían conectar los receptores arrastrándolos en el inspector, que es justamente el flujo de
trabajo del capítulo 4. El comentario del propio archivo lo dice: *"Clase abstracta y no interfaz,
para poder asignarla desde el inspector"*.

## 2.7 `out` y `ref`

Java solo pasa por valor y devuelve un valor. C# permite pasar por referencia: `ref` para
entrada-salida, `out` para salida pura (el método está obligado a asignarla).

```java
Vector3 v = device.getVelocity();        // o un objeto envoltorio si además hay que decir "falló"
```

```csharp
if (device.TryGetFeatureValue(CommonUsages.deviceVelocity, out Vector3 v)) { /* v es válida */ }
```

El patrón `TryGet...` es omnipresente en la API de XR: devuelve `bool` (¿el dispositivo ofrece esa
característica?) y entrega el dato por `out`. La variable se declara **dentro** de la llamada. Esto
es lo que evita recibir un cero silencioso cuando un runtime no expone la velocidad, y por eso el
capítulo 0 marcó esta API como más verbosa a propósito.

## 2.8 `readonly` frente a `final`

`readonly` es el `final` de campos: se asigna en la declaración o en el constructor, y después no.
La diferencia importante es que **también se aplica a un `struct` entero**.

```java
private final List<Pending> pending = new ArrayList<>();
```

```csharp
readonly List<Pending> pending = new(8);      // la referencia es fija; la lista sí se modifica
public readonly struct DrumHit { }            // el struct entero es inmutable
```

Igual que `final` en Java, `readonly` congela la **referencia**, no el contenido: a esa lista se
le siguen añadiendo elementos. La constante de compilación es `const`, no `readonly`. El `new(8)`
sin repetir el tipo es la *target-typed new expression*, azúcar de C# 9.

## 2.9 No hay excepciones verificadas

C# no tiene `throws` en la firma. Ninguna excepción es verificada: nada obliga a capturar ni a
declarar.

```java
void dump() throws IOException { Files.writeString(path, json); }   // obligatorio declararlo
```

```csharp
void Dump() { File.WriteAllText(ruta, JsonUtility.ToJson(volcado, true)); }   // sin throws
```

Consecuencia práctica: el compilador no avisa de nada, así que los puntos de falla se identifican
leyendo la documentación, no la firma. `LatencyProbe.Dump()` escribe a disco sin `try`: si falla,
se pierde un archivo de diagnóstico, no una sesión. La decisión es explícita, no un olvido.

## 2.10 `in` en parámetros

`in` pasa un argumento **por referencia y de solo lectura**. Es la contraparte de `out`: entrada
pura, sin copia.

```java
void handle(DrumHit hit) { }      // en Java siempre se copia la referencia, nunca el objeto
```

```csharp
public abstract void Handle(in DrumHit hit);        // por referencia, inmodificable
targets[i].Handle(in hit);                          // en la llamada también se escribe 'in'
```

**Por qué `DrumHitSink.Handle` lo usa.** `DrumHit` es un struct de cinco campos; pasarlo por valor
lo copiaría una vez por receptor, y `DrumHitFanout` lo reparte a tres. `in` evita esas copias sin
renunciar a la semántica de valor. Solo compila sobre un `readonly struct` sin efectos raros: si el
struct fuera mutable, el compilador insertaría copias defensivas y el `in` no ahorraría nada.

## 2.11 Lo que se traduce sin pensar

| Java | C# |
|---|---|
| `package` | `namespace` |
| `import` | `using` |
| `final class` | `sealed class` |
| `@Override` | `override` (obligatorio, no opcional) |
| `String.format("%.2f", x)` | `$"{x:F2}"` (cadena interpolada) |
| `toString()` | `ToString()` |
| `instanceof` | `is` |
| `List<T>` / `ArrayList<T>` | `List<T>` |
| `Map<K,V>` / `HashMap<K,V>` | `Dictionary<K,V>` |
| `for (Pad p : pads)` | `foreach (var p in pads)` |
| métodos en `camelCase` | métodos y properties en `PascalCase` |

Dos trampas de esa tabla: `override` es **obligatorio** en C# —omitirlo no sobrescribe, oculta el
método del padre y el compilador solo emite una advertencia—, y el método base debe estar marcado
`virtual` o `abstract` para poder sobrescribirse. En Java todo método es sobrescribible por
defecto; en C# no.

---

**Criterio de término: ninguno. Este capítulo no produce artefacto.** Es material de consulta para
los capítulos 3 y 4, que sí lo producen.

---

# Capítulo 3 — Manos que se mueven y vibran

El capítulo 1 demostró que la cadena llega al visor. Éste demuestra que **el visor devuelve
datos**: posición, velocidad y velocidad angular de cada control, y vibración de vuelta. Son las
tres entradas y la única salida táctil que el capítulo 4 necesita. Antes de escribir una línea de
detección de golpes hay que ver esos números moverse.

El orden importa: si la velocidad no llega, un golpe que no suena tiene dos explicaciones posibles
(la detección está mal, o el dato nunca llegó) y hay que descartar una a ciegas. Aquí se descarta.

## 3.1 El XR Origin en la escena

1. `File → New Scene`, plantilla básica de URP, guardar como `Assets/Scenes/Cap03_Manos.unity`.
2. `GameObject → XR → XR Origin (VR)`.
3. Borrar la `Main Camera` que trae la escena por defecto. El `XR Origin` aporta la suya; dos
   cámaras compiten y el resultado es impredecible.
4. Añadir un plano o un cubo de referencia visual en el suelo. Sin nada fijo alrededor no se
   percibe si la cabeza se mueve.

**Qué es el XR Origin.** Es el objeto que representa **el suelo del jugador dentro del mundo**.
De él cuelgan la cámara y los controles. Cuando el usuario camina, la cámara se mueve *dentro* del
Origin; cuando el juego teletransporta al usuario, lo que se mueve es el Origin. Esa distinción es
la raíz de la trampa de espacios de coordenadas del capítulo 4: todo lo que el hardware reporta
está expresado **respecto al Origin**, no respecto al mundo.

El prefab del `XR Origin (VR)` trae ya, colgando de un `Camera Offset`, la cámara y un objeto por
cada mano con su `TrackedPoseDriver` configurado. Los nombres exactos de esos hijos cambian entre
versiones del XR Interaction Toolkit — en 3.x suelen ser `Left Controller` y `Right Controller`
bajo `XR Origin (XR Rig) → Camera Offset`. <!-- VERIFICAR: nombres exactos de los hijos del prefab XR Origin (VR) en la versión de XRI 3.x instalada -->
Lo que importa no es el nombre sino **cuál de esos objetos tiene el componente `Tracked Pose Driver`
de la mano derecha**: ése es el que en el capítulo 4 se arrastra al campo `Controller` del
`StickTracker`.

## 3.2 El `TrackedPoseDriver` y la pose predicha

El `TrackedPoseDriver` es un componente que **escribe la pose del dispositivo en el `Transform` de
su GameObject**, cada frame. No hay que llamarlo: se limita a copiar posición y rotación del
control al objeto. Por eso basta con colgar la baqueta de ese objeto para que la baqueta siga la
mano; no se escribe código de seguimiento.

El dato que hay que retener para el capítulo 4 es **cuándo** vale esa pose. El runtime de OpenXR
no entrega la posición que el control tenía cuando se preguntó: entrega la que el modelo de
movimiento predice que tendrá **en el instante en que ese frame aparezca ante los ojos**. Esa
predicción cubre el tiempo de render y de escaneo de la pantalla, y es la razón de que en un visor
moderno la mano virtual no se sienta arrastrada.

Tres consecuencias directas:

- **La pose ya viene adelantada.** El capítulo 4 no debe volver a adelantarla por su cuenta: lo que
  predice es el instante del *impacto*, que es otra cosa.
- **El reloj de la pose y el reloj del audio no son el mismo.** La pose vive en el tiempo de
  presentación del frame; `AudioSettings.dspTime` vive en el tiempo del hilo de audio. La diferencia
  entre ambos es un desfase pequeño y **constante**, y por eso `StickTracker` expone un campo
  `poseToAudioOffset`, con este comentario en el archivo:

  > *"Corrección constante entre el reloj de pose y el de audio, en segundos. Se determina midiendo,
  > en el capítulo 6. No se adivina."*

  Se deja en `0` hasta tener una medición real delante.
- **La velocidad reportada corresponde a esa misma pose predicha**, no a la posición cruda del
  sensor. Es el dato coherente con la mano que el usuario ve.

## 3.3 Leer el dispositivo: `devicePosition`, `deviceVelocity`, `deviceAngularVelocity`

El acceso al hardware es siempre el mismo patrón de dos pasos: se obtiene el dispositivo por nodo
(`XRNode.RightHand`, `XRNode.LeftHand`, `XRNode.Head`) y se le piden *características* con
`TryGetFeatureValue`.

```csharp
var device = InputDevices.GetDeviceAtXRNode(XRNode.RightHand);
device.TryGetFeatureValue(CommonUsages.devicePosition,        out Vector3 p);   // metros
device.TryGetFeatureValue(CommonUsages.deviceVelocity,        out Vector3 v);   // m/s
device.TryGetFeatureValue(CommonUsages.deviceAngularVelocity, out Vector3 w);   // rad/s
```

| Característica | Tipo | Unidad | Para qué sirve en este proyecto |
|---|---|---|---|
| `devicePosition` | `Vector3` | metros | Diagnóstico. La posición real se toma del `Transform`, que el `TrackedPoseDriver` ya actualiza |
| `deviceVelocity` | `Vector3` | m/s | Fuerza del golpe → volumen del sample |
| `deviceAngularVelocity` | `Vector3` | rad/s | El giro de muñeca, que en la punta de la baqueta se convierte en velocidad lineal |
| `triggerButton` | `bool` | — | Prueba de háptico de este capítulo |
| `primaryButton` | `bool` | — | Botón A. Lo usa `PadCalibrator` en el capítulo 5 |

Tres cosas que hay que interiorizar aquí, porque reaparecen:

1. **`TryGetFeatureValue` devuelve `bool`.** Es `false` si el runtime no ofrece esa característica.
   Ignorar el retorno y usar el `out` deja un `Vector3.zero` silencioso, que en este proyecto se
   traduce en golpes que nunca superan el umbral de velocidad y un sistema que "no funciona" sin
   error alguno.
2. **`device.isValid` cambia durante la sesión.** Si el control se apaga por inactividad o pierde
   tracking, el `InputDevice` guardado deja de ser válido. Por eso `StickTracker` lo vuelve a pedir
   cada frame cuando deja de serlo, en lugar de obtenerlo una sola vez en `Awake`.
3. **Estos vectores vienen en el espacio del XR Origin, no en el del mundo.** Aquí no se nota
   porque solo se imprime su magnitud. En el capítulo 4 sí se nota, y es la sección 4.5 completa.

## 3.4 La baqueta: un cilindro y un `Transform` vacío en la punta

La baqueta de la etapa A es geometría de mentira. No tiene física, no tiene colisionador y no
interactúa con nada: solo hay que **verla** y saber **dónde está su punta**.

1. Seleccionar el objeto del control derecho dentro del `XR Origin` (el que tiene el
   `Tracked Pose Driver`).
2. `GameObject → 3D Object → Cylinder`, y arrastrarlo en la jerarquía para que quede **hijo** de
   ese objeto.
3. En el `Transform` del cilindro: escala `(0.012, 0.16, 0.012)` — un cilindro de Unity mide 2
   unidades de alto, de modo que `Y = 0.16` da una baqueta de 32 cm; posición `(0, 0, 0.16)` y
   rotación `(90, 0, 0)` para que salga hacia adelante desde el puño.
4. **Quitarle el `Capsule Collider`** que el cilindro trae por defecto. No se usa física en ningún
   punto de este sistema, y un colisionador suelto solo puede generar eventos que nadie espera.
5. `GameObject → Create Empty`, hijo del **cilindro**, con nombre `Tip`, en posición `(0, 1, 0)`
   local — el extremo del cilindro, ya que mide 2 unidades y su origen está al centro.

**Por qué `tip` tiene que ser hijo del controlador.** Ésta es la pieza que hace que todo lo demás
sea simple. `Transform.position` de un hijo se calcula componiendo la jerarquía completa hasta la
raíz: si `Tip` cuelga del cilindro y el cilindro cuelga del objeto que el `TrackedPoseDriver`
actualiza, entonces `tip.position` es **la posición en mundo de la punta de la baqueta, ya
resuelta, actualizada cada frame, sin una línea de código**. Es exactamente lo que consume
`StickTracker`:

```csharp
Vector3 tipNow = tip.position;
```

Si `Tip` estuviera suelto en la escena en lugar de colgado del control, esa línea devolvería un
punto fijo y la detección de golpes no vería moverse nada. Y `StickTracker` necesita **las dos**
referencias, `controller` y `tip`, porque el vector entre ambas es el brazo `r` de la fórmula
`v + ω × r` de la sección 4.4.

Con ajustar los números del paso 3 se cambia el largo de la baqueta. Vale la pena hacerlo pronto:
una baqueta larga es más fácil de golpear pero amplifica el error angular del tracking.

## 3.5 Script de diagnóstico

Crear `Assets/Scripts/DiagnosticoMano.cs` — recordar que el nombre del archivo debe coincidir con
el de la clase — y pegarlo completo:

```csharp
using UnityEngine;
using UnityEngine.XR;

/// Imprime en pantalla lo que reporta el control. Sirve para confirmar que el tracking llega
/// antes de construir nada encima.
public sealed class DiagnosticoMano : MonoBehaviour
{
    [SerializeField] XRNode hand = XRNode.RightHand;

    void Update()
    {
        var device = InputDevices.GetDeviceAtXRNode(hand);
        if (!device.isValid) { Debug.Log("control no válido"); return; }

        device.TryGetFeatureValue(CommonUsages.deviceVelocity, out Vector3 v);
        device.TryGetFeatureValue(CommonUsages.triggerButton,  out bool gatillo);

        if (gatillo && device.TryGetHapticCapabilities(out var caps) && caps.supportsImpulse)
            device.SendHapticImpulse(0u, 0.5f, 0.05f);

        Debug.Log($"velocidad {v.magnitude:F2} m/s");
    }
}
```

Arrastrarlo a cualquier GameObject de la escena — no necesita estar en el control, porque pide el
dispositivo por nodo, no por jerarquía.

Lectura línea por línea de lo que no es obvio:

- `InputDevices.GetDeviceAtXRNode(hand)` se llama **cada frame**, no se cachea. Es deliberado: en
  un script de diagnóstico interesa ver aparecer y desaparecer el control.
- `SendHapticImpulse(0u, 0.5f, 0.05f)` son canal, amplitud (0 a 1) y duración en segundos. El
  canal `0` es el único que tiene el Touch Plus. Es un **impulso con duración explícita**, no un
  estado que haya que apagar: ésa fue la diferencia número 5 del capítulo 0.
- La comprobación `TryGetHapticCapabilities(...) && caps.supportsImpulse` no es paranoia: llamar a
  `SendHapticImpulse` sobre un dispositivo que no lo soporta no hace nada y tampoco avisa. Es la
  misma guarda que usa `HapticSink` en el sistema definitivo.
- **El háptico dispara de inmediato y no se puede agendar.** Aquí da igual; en el capítulo 4 es el
  motivo de que `HapticSink` guarde el golpe en una lista y espere a que el reloj DSP alcance el
  instante del impacto en lugar de vibrar al cruzar el plano.
- `Debug.Log` **cada frame es caro**: a 72 Hz son 72 líneas por segundo cruzando a `logcat`. Se
  tolera porque este script se borra al terminar el capítulo. Nada de esto sobrevive al capítulo 4.

## 3.6 Leer la consola del visor desde la Mac

`Debug.Log` dentro del Quest no tiene ventana de consola. Sale por el log de Android, y se lee por
`adb` con la variable `ADB` que se definió en el capítulo 1:

```bash
$ADB logcat -s Unity:V
```

`-s` filtra por etiqueta —solo `Unity`, no los miles de líneas del sistema— y `V` es el nivel más
detallado (*verbose*). Para limpiar el búfer antes de una prueba y no leer lo de la sesión
anterior:

```bash
$ADB logcat -c
```

Funciona igual por cable o por la conexión inalámbrica de 1.10. Ésta es la herramienta de
depuración del resto de la guía: en el visor no hay otra forma de ver qué está pasando.

## 3.7 Prueba en el orden correcto

1. **Play mode en la Mac, con el Meta XR Simulator activo.** Confirma que el script compila, que
   encuentra el dispositivo y que imprime. La velocidad será la del mouse: sirve para ver que el
   número existe, no para creerle.
2. **Build e instalación en el Quest 3S**, `$ADB install -r Builds/bateria.apk`, y `logcat`
   abierto en otra terminal.

Cuatro cosas que verificar puestas el visor, en este orden:

- La baqueta está donde la mano, y se mueve con ella sin arrastre perceptible.
- `logcat` imprime `velocidad 0.0x m/s` con el brazo quieto — un valor pequeño y no exactamente
  cero es lo normal: es el ruido del tracking.
- Al agitar el brazo el número sube. Un golpe de batería normal ronda **2 a 6 m/s**; con ganas se
  pasa de 8. Esas cifras son las que justifican el `minVelocity` de 0.4 m/s y la curva
  `velocityToGain` que va de 0.4 a 6 m/s en `DrumVoice`.
- Al apretar el gatillo, el control vibra.

## 3.8 Problemas frecuentes

| Síntoma | Causa | Qué hacer |
|---|---|---|
| `logcat` imprime `control no válido` sin parar | El control está dormido, o el `XRNode` del script no corresponde a la mano que se está moviendo | Apretar un botón del control para despertarlo; revisar el campo **Hand** en el inspector |
| La velocidad siempre sale `0.00` pero la baqueta sí se mueve | El runtime no expone `deviceVelocity`, o se está mirando el play mode del simulador | Probar en el visor físico; si en el visor también sale cero, comprobar que **Oculus Touch Controller Profile** está en Interaction Profiles (1.6) |
| La baqueta no se mueve | El cilindro no quedó hijo del objeto con el `Tracked Pose Driver`, sino hermano o hijo del `Camera Offset` | Revisar la jerarquía y reparentar |
| La baqueta se mueve pero apunta hacia atrás o al suelo | Rotación local del cilindro | Ajustar la rotación del paso 3 de 3.4 hasta que salga del puño hacia adelante |
| No vibra nada | El dispositivo no reporta `supportsImpulse`, o el gatillo mapeado no es `triggerButton` | Imprimir `caps.supportsImpulse` en `logcat`; probar con `primaryButton` para aislar si el problema es el botón o el háptico |
| `logcat` no imprime nada | Se está leyendo el visor equivocado, o la app no está corriendo | `$ADB devices`, `$ADB logcat -c` y relanzar la app desde **Fuentes desconocidas** |

---

**Criterio de término: la baqueta sigue la mano dentro del Quest 3S, el control vibra al apretar el
gatillo, y `logcat` muestra la velocidad subir al agitar el brazo.** Los tres, en el visor físico.
El simulador no valida ninguno de ellos.
