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
| 4 | El pad suena al golpearlo | Plano armado, cruce, predicción, `PlayScheduled` | **Escrito** |
| 5 | Número de latencia real, en ms | El hito Go/No-Go del acta | **Escrito** |
| 6 | Ajustes que bajan la latencia | Best Latency, 48 kHz, Vulkan, 72 vs 90 Hz, remedición | **Escrito** |
| 7 | Esbozo de la etapa B | Arquitectura de las seis piezas | **Escrito** |

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

El prefab del `XR Origin (VR)` trae ya la cámara y un objeto por cada mano con su
`TrackedPoseDriver` configurado. La jerarquía en XRI 3.x es:

```
XR Origin (XR Rig)          <- este es el que va al campo xrOrigin del StickTracker
└── Camera Offset
    ├── Main Camera
    ├── Left Controller
    └── Right Controller    <- este va al campo controller, y de él cuelga la baqueta
```

Aun así, **no te fíes del nombre, fíate del componente.** Lo que decide cuál objeto arrastrar en el
capítulo 4 es cuál tiene el `Tracked Pose Driver` de la mano derecha. Si tu versión los nombra
distinto, selecciónalos y míralo en el inspector: el nombre es decoración, el componente es el
contrato.

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
- `Debug.Log` **cada frame es caro**: son decenas de líneas por segundo cruzando a `logcat`. Se
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

---

# Capítulo 4 — El pad suena al golpearlo

Éste es el capítulo central de la guía. Al terminarlo existe el sistema de percusión completo de
la etapa A: un pad que suena al golpearlo, con vibración, y con el volumen ligado a la fuerza del
golpe. Todo lo anterior fue preparación y todo lo que sigue es medición y ajuste.

El código ya está escrito y vive en el repositorio, bajo
`proyecto-unity/Assets/Scripts/Drum/`. **Este capítulo no lo copia: lo explica.** Duplicar los
archivos aquí garantizaría que la guía y el código se desincronicen en la primera corrección. Se
pegan fragmentos cortos, y cada fragmento va acompañado de por qué está escrito así.

| Archivo | Responsabilidad |
|---|---|
| `DrumPad.cs` | Geometría del pad: plano armado, distancia con signo, prueba de radio |
| `DrumHit.cs` | El struct del golpe. Contrato entre la detección y sus consumidores |
| `DrumHitSink.cs` | Clase abstracta del receptor |
| `DrumHitFanout.cs` | Reparte un golpe a varios receptores |
| `CrossSolver.cs` | La matemática pura: fracción de cruce, instante de impacto, velocidad de punta |
| `StickTracker.cs` | Lee el hardware y orquesta. Una instancia por mano |
| `DrumVoice.cs` | Pool de `AudioSource` y `PlayScheduled` |
| `HapticSink.cs` | Vibración diferida hasta el instante del impacto |
| `LatencyProbe.cs` | Sonda interna: registra cada golpe y cuenta las agendas tardías |
| `PadCalibrator.cs` | Coloca el pad virtual sobre la superficie física de medición |

La división responde a una sola regla: **lo que se puede probar sin visor, vive aparte de lo que
necesita hardware.** Toda la matemática está en `CrossSolver` y en `DrumPad`, sin estado y sin
dependencias de XR, y por eso la sección 4.9 puede verificarla en el editor de la Mac antes de que
el Quest 3S esté siquiera encendido.

## 4.1 Por qué no colliders

La forma obvia de detectar un golpe en Unity es poner un colisionador en la punta de la baqueta,
otro en el pad, marcar uno como *trigger* y escuchar `OnTriggerEnter`. Es lo que hace cualquier
tutorial. **Para este proyecto está descartado por dos razones independientes, y cada una basta
por sí sola.**

**Razón 1: llega tarde, y llega tarde por diseño.** Los eventos de física no se emiten cuando
ocurre el cruce: se emiten en el siguiente paso de física, que corre a su propio ritmo fijo,
independiente del frame. Con el `Fixed Timestep` por defecto de Unity (0.02 s, 50 Hz) el paso dura
20 ms y un cruce cae en promedio a la mitad de un paso: **unos 10 ms de retraso medio, hasta 20 en
el peor caso**. Subiendo la física a 90 Hz el paso baja a 11 ms y el retraso medio a ~5.5 ms, a
cambio de multiplicar el coste de CPU de la simulación en un SoC móvil donde la CPU ya es el
cuello de botella. En el mejor de los casos son 5 ms; en la configuración por defecto son 10.
Sobre un presupuesto total de ~26 ms contra un umbral de 30, eso es entre la quinta parte y el
40% del margen, regalado a cambio de nada.

**Razón 2: el tunelado se traga golpes enteros.** Un colisionador detecta **superposición**: para
generar el evento, los dos volúmenes tienen que solaparse en algún instante muestreado. Un golpe
de batería con ganas mueve la punta a 10 m/s. A 90 Hz, eso son

```
10 m/s ÷ 90 frames/s = 0.111 m = 11.1 cm por frame
```

Si el pad tiene 2 cm de grosor, la punta puede estar delante en un muestreo y detrás en el
siguiente, **sin haberse solapado nunca**. El evento no se emite y el golpe simplemente no suena.
Y no falla al azar: falla **en los golpes fuertes**, que son los que el usuario más espera
escuchar. Un sistema que se come los golpes fuertes no es un instrumento.

**Lo que se hace en su lugar.** La prueba de plano no pregunta "¿se están tocando?" sino **"¿el
punto quedó de un lado del plano el frame pasado y del otro lado ahora?"**. Eso es detectar el
*cruce*, y un cruce no se puede saltar por rápido que se vaya: si la punta terminó del otro lado,
cruzó. El tunelado deja de existir, no se mitiga. Además el cálculo es un producto punto por pad y
por frame, sin motor de física de por medio, y devuelve **en qué fracción del intervalo** ocurrió
el cruce — información que el colisionador nunca da y que la sección 4.2 convierte en predicción.

## 4.2 El plano armado

El golpe **no** se detecta en la superficie del pad. Se detecta en un plano paralelo situado
6 centímetros **antes**, del lado del jugador. Ese es el plano armado.

```
                    baqueta bajando
                          │
                          ▼   v_normal = 4 m/s
   ─────────────────────── ● ────────────────────  plano ARMADO
                          ▲                        (a +6 cm sobre la superficie)
                          │                         aquí se DETECTA el cruce
             armDistance  │  0.06 m                 y se calcula todo
                          │
   ═══════════════════════╪════════════════════    superficie del PAD
                          ▼                         aquí se ESCUCHA el golpe
                                                    15 ms después

        │◄──── radius = 0.15 m ────►│
```

Al cruzar ese plano ya se conocen las dos cosas que hacen falta: **a qué distancia está la
superficie** (un valor fijo, `armDistance`) y **a qué velocidad se acerca la punta** (`v_normal`).
Con ambas, el instante del impacto se calcula en lugar de esperarse:

```
t_impacto = t_cruce + armDistance / v_normal
```

Ese cálculo es `CrossSolver.ImpactDsp`, de tres líneas:

```csharp
public static double ImpactDsp(double dspCross, float armDistance, float normalVelocity)
{
    if (normalVelocity <= 0f) return dspCross;
    return dspCross + armDistance / normalVelocity;
}
```

**Ejemplo numérico, el del proyecto.** A 4 m/s, que es un golpe normal:

```
0.06 m ÷ 4 m/s = 0.015 s = 15 ms en el FUTURO
```

Quince milisegundos de adelanto. Ese número es la prueba `TiempoDeImpacto_SumaElTramoQueFalta` de
`CrossSolverTests.cs`: cruce en `dsp = 100.0` y resultado esperado `100.015`.

La predicción se adapta sola a la fuerza del golpe, y hace falta que lo haga:

| Velocidad normal | Adelanto disponible |
|---|---|
| 1 m/s (golpe suave) | 60 ms |
| 4 m/s (golpe normal) | 15 ms |
| 8 m/s (golpe fuerte) | 7.5 ms |

Un golpe suave da 60 ms de margen, de sobra para cualquier presupuesto. Un golpe muy fuerte deja
7.5 ms, que ya no cubre los ~26 ms del presupuesto completo: **en los golpes más fuertes el sistema
llega tarde de todos modos**, solo que menos. Esa es la razón de que `armDistance` sea un campo
editable en el inspector y no una constante: subirlo a 10 cm compra más adelanto, a cambio de que
un usuario que se detenga a mitad de camino escuche un golpe que nunca dio. Seis centímetros es el
punto de partida; el capítulo 6 lo ajusta con mediciones delante.

**Qué pasa con ese instante.** Se guarda en el campo `ImpactDsp` del `DrumHit` y viaja hasta los
tres receptores. `DrumVoice` agenda el audio con `PlayScheduled(hit.ImpactDsp)`, de modo que el
motor de audio coloca la primera muestra del sample **exactamente en ese instante del reloj DSP**,
con precisión de muestra, no de frame. `HapticSink` guarda el golpe en una lista y espera: el
háptico no se puede agendar, dispara de inmediato, así que vibrar al cruzar el plano armado haría
que el usuario **sintiera** el golpe 15 ms antes de **verse** tocar el pad. El propio archivo lo
explica en su cabecera:

> *"El háptico NO se puede agendar: SendHapticImpulse dispara de inmediato. Si se lanzara en el
> cruce del plano armado llegaría ~15 ms antes del impacto, y el usuario sentiría la vibración
> antes de "tocar" el pad."*

Y si la predicción no alcanzó —el frame se alargó, el golpe fue durísimo— `DrumVoice` no agenda en
el pasado, que sería silencio: dispara de inmediato y **lo anota**.

```csharp
if (hit.ImpactDsp <= AudioSettings.dspTime)
{
    LatencyProbe.CountLateSchedule();   // la predicción no alcanzó
    src.Play();                          // ya vamos tarde, disparar de inmediato
}
else
{
    src.PlayScheduled(hit.ImpactDsp);
}
```

El contador de agendas tardías es un dato de diagnóstico de primera: si sube, el margen se agotó y
hay que subir `armDistance` o bajar el tiempo de frame. Ese número aparece en el JSON que vuelca
`LatencyProbe` y se interpreta en el capítulo 5.

## 4.3 Por qué `dspTime` y nunca `Time.deltaTime`

Unity ofrece varios relojes y **solo uno sirve para ritmo**.

| Reloj | Qué mide | Uso aquí |
|---|---|---|
| `Time.deltaTime` | Duración del frame anterior | Solo animación visual. Nunca ritmo |
| `Time.time` | Suma acumulada de frames | Nunca |
| `AudioSettings.dspTime` | Tiempo del hilo de audio, en segundos | **El único reloj del sistema de percusión** |

`Time.deltaTime` no es una medida del tiempo: es cuánto tardó el frame anterior en dibujarse. Ese
valor sube y baja con la carga de render, con la recolección de basura, con el termal throttling
del visor y con cualquier hipo del sistema operativo. Acumularlo para llevar la cuenta del tiempo
es sumar una serie de errores del mismo signo, y el resultado **deriva**. En una sesión terapéutica
de doce minutos —que es la duración del protocolo de este proyecto— una deriva de milésimas por
frame se convierte en un desfase audible entre el metrónomo y la mano del usuario, justo el eje
sobre el que se mide la precisión rítmica. El instrumento de medición no puede correr sobre un
reloj que se atrasa.

`AudioSettings.dspTime` viene del hilo de audio, que avanza contando **muestras reproducidas** a
48 000 por segundo. No depende del frame rate, no se salta con una caída de frames y es el mismo
reloj en el que `PlayScheduled` interpreta su argumento. Agendar en un reloj y medir en otro sería
comparar peras con manzanas.

La regla operativa del proyecto es más específica que "usa `dspTime`": **se lee una sola vez por
frame, al inicio de `Update()`**, y ese valor se usa durante todo el frame.

```csharp
// Lectura ÚNICA del reloj DSP por frame. Regla del proyecto: nunca Time.time.
double  dspNow = AudioSettings.dspTime + poseToAudioOffset;
Vector3 tipNow = tip.position;
```

El motivo es que `dspTime` **avanza mientras el frame se ejecuta**: es un reloj real, no un valor
congelado. Leerlo dos veces dentro del mismo `Update()` da dos valores distintos, y si uno se usa
para el cruce y otro para el impacto, la resta entre ambos mezcla el tiempo del golpe con el tiempo
que tardó el código en llegar de una línea a la otra. Con dos pads y dos manos esos errores dejan
de ser reproducibles y el sistema se vuelve imposible de depurar. Una lectura, un instante, todo el
frame.

El `+ poseToAudioOffset` es la corrección constante entre el reloj de la pose y el del audio, de la
que habló la sección 3.2. Se queda en `0` hasta que el capítulo 6 la mida.

## 4.4 Velocidad de punta contra velocidad de control

`deviceVelocity` reporta la velocidad **del control**, es decir, del puño. La que importa es la de
la **punta de la baqueta**, y no son la misma cosa: entre ambas hay una palanca.

Un sólido rígido que gira mientras se traslada tiene, en cualquier punto distinto de su origen,
una velocidad igual a la de traslación más la aportada por el giro:

```
v_punta = v_dispositivo + ω × r
```

donde `ω` es la velocidad angular (`deviceAngularVelocity`, en rad/s) y `r` es el vector que va
del origen del control a la punta. Eso es exactamente `CrossSolver.TipVelocity`:

```csharp
public static Vector3 TipVelocity(Vector3 deviceVelocityWorld,
                                  Vector3 angularVelocityWorld,
                                  Vector3 controllerToTip)
    => deviceVelocityWorld + Vector3.Cross(angularVelocityWorld, controllerToTip);
```

**Ejemplo numérico**, el de la prueba `VelocidadDePunta_IncluyeElGiroDeMuneca` de
`CrossSolverTests.cs`: control **completamente quieto**, girando a 10 rad/s sobre el eje Z, con la
punta a 30 cm del origen sobre +X.

```
ω × r = (0, 0, 10) × (0.3, 0, 0) = (0, 3, 0)   →   3 m/s
```

**Tres metros por segundo de puro giro de muñeca, con `deviceVelocity` valiendo exactamente cero.**
Un sistema que usara solo `deviceVelocity` no detectaría ese golpe: `NormalSpeed` daría 0, no
superaría el `minVelocity` de 0.4 m/s y el golpe se descartaría en silencio.

Y ése es precisamente el golpe que da un baterista. La técnica de percusión real mueve poco el
brazo y mucho la muñeca; cuanto mejor es el ejecutante, mayor es la proporción del giro. Ignorar el
término `ω × r` produce un sistema que funciona con golpes de aficionado, torpes y de brazo
entero, y falla justo con quien sabe tocar. Para una herramienta cuyo objetivo medible es la
precisión motriz, eso lo descalifica.

El brazo `r` se calcula solo, gracias a la jerarquía que montó la sección 3.4:

```csharp
tip.position - controller.position
```

Alargar la baqueta alarga `r` y aumenta la contribución del giro. También amplifica cualquier error
angular del tracking: un error de medio grado en la orientación se convierte en más milímetros de
error de posición cuanto más larga sea la baqueta. Es el compromiso que se ajusta con los números
del paso 3 de la sección 3.4.

## 4.5 La trampa de los espacios de coordenadas

**Éste es el error que más caro sale de todo el proyecto**, y merece leerse dos veces. No revienta,
no da error de compilación, no aparece en ninguna prueba y **funciona perfectamente mientras se
mira al frente**. Se manifiesta el día de la demostración, cuando alguien se gira.

Los datos que se mezclan en el cálculo del golpe vienen de dos sistemas de coordenadas distintos:

| Dato | Origen | Espacio |
|---|---|---|
| `CommonUsages.deviceVelocity` | el runtime de XR | **espacio del XR Origin** |
| `CommonUsages.deviceAngularVelocity` | el runtime de XR | **espacio del XR Origin** |
| `tip.position`, `controller.position` | `Transform` de Unity | **mundo** |
| `pad.Normal`, `pad.Center` | `Transform` de Unity | **mundo** |

Mientras el `XR Origin` esté en el origen del mundo sin rotar, los dos espacios coinciden y todo
sale bien. En cuanto el Origin rota —porque se giró al jugador, porque se recolocó el rig, porque
se usó un sistema de recentrado— dejan de coincidir, y el producto punto de `NormalSpeed` empieza a
comparar un vector expresado en un espacio contra una normal expresada en otro.

El síntoma es característico y engañoso: **las magnitudes siguen siendo correctas.** La velocidad
vale 4 m/s, como debe. Lo que está mal es la dirección, así que el golpe deja de superar el umbral
cuando el jugador mira a 90 grados de la posición original, y vuelve a funcionar si se endereza.
Quien depura eso sin saber lo que busca cambia umbrales, revisa la geometría del pad y culpa al
tracking. La transformación es una sola línea, y va en `StickTracker.ReadTipVelocity`:

```csharp
return CrossSolver.TipVelocity(
    xrOrigin.TransformVector(v),
    xrOrigin.TransformVector(w),
    tip.position - controller.position);
```

`TransformVector` lleva un vector del espacio local del `Transform` al espacio de mundo aplicando
rotación y escala, **sin aplicar traslación**, que es lo correcto para una velocidad: una velocidad
es una dirección con magnitud, no una posición. Usar `TransformPoint` aquí —que sí traslada— sumaría
la posición del Origin a la velocidad y produciría números absurdos.

Hecha esa conversión, las tres entradas de `TipVelocity` están en mundo, igual que `pad.Normal`, y
el producto punto compara lo comparable. Por eso el propio archivo lleva la advertencia encima del
método:

> *"CUIDADO CON LOS ESPACIOS: deviceVelocity y deviceAngularVelocity vienen en el espacio del XR
> Origin, mientras que tip.position y pad.Normal están en mundo. Mezclarlos da magnitudes correctas
> con direcciones equivocadas en cuanto el jugador gira."*

**Consecuencia práctica para el ensamblado:** el campo `Xr Origin` del `StickTracker` no es
opcional ni decorativo. Si se deja vacío, el sistema lanza una excepción de referencia nula; si se
le arrastra el objeto equivocado, no lanza nada y se hereda el fallo silencioso completo.

## 4.6 Rearme por posición, no por tiempo

Un cruce de plano genera un golpe. El problema es el segundo frame: mientras la punta siga del otro
lado del plano, la condición "está pasado el plano" sigue siendo cierta, y sin una guarda el
sistema dispararía un golpe por frame, 72 veces por segundo, mientras la baqueta descanse sobre el
pad.

La solución obvia es un *cooldown*: ignorar golpes durante N milisegundos tras cada uno. **Está
descartada.** Un redoble de semicorcheas a 160 BPM —tempo normal para un ejercicio de coordinación,
y perfectamente al alcance del protocolo terapéutico de este proyecto— tiene los golpes separados
por

```
60 s/min ÷ 160 BPM ÷ 4 semicorcheas = 0.09375 s = 94 ms
```

Un cooldown de 100 ms, que suena conservador y razonable, **se comería uno de cada dos golpes del
redoble**. Y de nuevo fallaría en el caso que más importa: la ejecución rápida y precisa, que es
justo lo que la herramienta pretende medir. Cualquier cooldown fijo es una apuesta sobre el tempo
máximo que el usuario va a tocar, y esa apuesta se pierde.

El rearme correcto es **geométrico**: el pad queda muerto al golpearlo y **revive cuando la punta
vuelve a salir** del plano armado hacia el lado del jugador. Son tres líneas en
`StickTracker.Evaluate`:

```csharp
// Rearme POR POSICIÓN, no por tiempo: el pad revive cuando la baqueta vuelve a salir.
// Un cooldown temporal destruiría los redobles.
if (dNow > 0f && dPrev <= 0f) { armed[pad] = true; return; }

if (!armed[pad]) return;
if (!(dPrev > 0f && dNow <= 0f)) return;              // no cruzó hacia adentro
```

`dPrev` y `dNow` son la distancia con signo al plano armado en el frame anterior y en éste. La
primera línea detecta el cruce **hacia afuera** y rearma. Las dos siguientes exigen que el pad esté
armado y que el cruce sea **hacia adentro**. Lo que queda es un autómata de dos estados cuya
transición depende solo de dónde está la punta.

Esto no impone ningún límite de tempo: el usuario puede tocar tan rápido como sea capaz de sacar y
meter la baqueta, y cada ciclo completo produce exactamente un golpe. También resuelve gratis el
caso de la baqueta apoyada sobre el pad: mientras no salga, no vuelve a sonar.

El estado vive en un diccionario por pad, `readonly Dictionary<DrumPad, bool> armed`, inicializado
en `OnEnable`. Como cada mano tiene su propio `StickTracker`, cada mano lleva su propio armado: las
dos manos pueden golpear el mismo pad de forma independiente sin bloquearse entre sí.

## 4.7 Ensamblado de la escena

Cinco GameObjects. Se construye en este orden, y las referencias se arrastran desde la jerarquía al
campo correspondiente del inspector.

```
Escena Cap04_Pad
├── XR Origin (XR Rig)
│   └── Camera Offset
│       ├── Main Camera            ← trae el AudioListener
│       └── Right Controller       ← TrackedPoseDriver de la mano derecha
│           └── Baqueta (cilindro)
│               └── Tip            ← Transform vacío en la punta
├── Pad                            → DrumPad
├── Audio                          → DrumVoice
├── Haptico                        → HapticSink
├── Sonda                          → LatencyProbe
├── Fanout                         → DrumHitFanout
└── Tracker                        → StickTracker
```

### Paso 1 — `Pad`

`GameObject → Create Empty`, nombre `Pad`, y añadirle el componente `DrumPad`. Opcionalmente,
hacerle hijo un cilindro aplastado como representación visual, solo para verlo.

| Campo del inspector | Valor | Nota |
|---|---|---|
| Radius | `0.15` | Radio útil en metros |
| Arm Distance | `0.06` | Los 6 cm del plano armado |
| Min Velocity | `0.4` | Velocidad normal mínima para contar como golpe, en m/s |

**La orientación es lo que hay que cuidar.** `DrumPad.Normal` devuelve `transform.up`, así que con
rotación `(0,0,0)` la normal apunta hacia arriba y el pad se golpea **desde arriba**, como una
tarola horizontal. Rotar el objeto rota el plano y, con él, la dirección desde la que se golpea.
Colocarlo alrededor de `(0, 0.75, 0.45)` — altura de mesa, al frente — es un punto de partida
cómodo.

Con el objeto seleccionado, `DrumPad.OnDrawGizmos` dibuja en la vista de escena **dos círculos de
alambre**: uno amarillo en la superficie y uno cian en el plano armado, unidos por una línea. Es la
forma de comprobar de un vistazo que la orientación y el desplazamiento son los que se creen.

### Paso 2 — `Audio`

`GameObject → Create Empty`, nombre `Audio`, componente `DrumVoice`.

| Campo del inspector | Valor | Nota |
|---|---|---|
| Clip | el sample de bombo | Se obtiene en 4.8 |
| Voices | `8` | Voces simultáneas |
| Velocity To Gain | curva por defecto | Lineal de (0.4, 0.2) a (6, 1) |

No hay que añadir ningún `AudioSource` a mano: `DrumVoice.Awake` crea los ocho con
`gameObject.AddComponent<AudioSource>()` y los configura. Por eso `DrumVoice` va en un GameObject
propio y no compartido — al entrar en play mode aparecerán ocho `AudioSource` en su inspector, y
conviene que no estorben.

Cuatro decisiones de ese `Awake` que valen por sí solas:

- **`AddComponent` en `Awake`, nunca en runtime.** Crear componentes durante el juego asigna
  memoria, y asignar memoria alimenta al recolector de basura, y el recolector produce caídas de
  frame. Todo el pool se reserva antes de que empiece nada.
- **`spatialBlend = 0f`** — sonido 2D. La espacialización cuesta CPU y no aporta nada: hay un solo
  pad y la fuente está a medio metro de la cabeza. En la etapa B, con seis piezas, esto se
  reconsidera.
- **`bypassEffects`, `bypassListenerEffects`, `bypassReverbZones` en `true`** — cada efecto en la
  cadena es proceso entre la muestra y la bocina. Nada de eso se paga en la etapa A.
- **Asignación circular con corte.** `next = (next + 1) % pool.Length` recorre las voces; si se
  agotan, la más vieja se corta a media cola. Ocho voces cubren cualquier redoble razonable sobre un
  solo pad; el propio `Tooltip` del campo lo advierte: *"Dimensionar al peor redoble esperado:
  cuando se agotan, la voz más vieja se corta a media cola."*

**La curva `Velocity To Gain` es lo que hace que el golpe se sienta.** Va de 0.4 m/s (volumen 0.2) a
6 m/s (volumen 1.0), y es editable en el inspector sin recompilar: se pulsa sobre ella y se abre el
editor de curvas. Es el primer lugar donde tocar si el instrumento se siente plano o si todos los
golpes suenan igual de fuertes.

### Paso 3 — `Haptico`

`GameObject → Create Empty`, nombre `Haptico`, componente `HapticSink`.

| Campo del inspector | Valor | Nota |
|---|---|---|
| Velocity For Full Amplitude | `6` | Velocidad en m/s que corresponde a amplitud 1.0 |
| Duration Seconds | `0.04` | 40 ms. Un pulso seco, no un zumbido |

No tiene referencias que arrastrar: saca la mano del propio `DrumHit`, en el campo `Hand`, así que
una sola instancia sirve para las dos manos.

### Paso 4 — `Sonda`

`GameObject → Create Empty`, nombre `Sonda`, componente `LatencyProbe`.

| Campo del inspector | Valor | Nota |
|---|---|---|
| Capacidad Golpes | `2000` | Golpes que caben sin que la lista tenga que crecer |

Los 2000 no son un número al azar. `Awake` reserva toda la memoria de golpe y, si se desborda,
`Handle` **deja de registrar en lugar de realocar**. El `Tooltip` explica por qué: *"Una realocación
en mitad de la medición produce una caída de frame que contamina justo el dato que se está
midiendo."* Perder una muestra de diagnóstico es preferible a falsear la medición.

Al salir de la aplicación o al pausarla, `LatencyProbe` vuelca un JSON a
`Application.persistentDataPath`. Ese archivo es material del capítulo 5.

### Paso 5 — `Fanout`

`GameObject → Create Empty`, nombre `Fanout`, componente `DrumHitFanout`.

| Campo del inspector | Qué arrastrarle |
|---|---|
| Targets | Tamaño **3**. Elemento 0 → `Audio`, Elemento 1 → `Haptico`, Elemento 2 → `Sonda` |

Se pone el tamaño del arreglo en 3 y se arrastra cada GameObject a su ranura. Unity resuelve solo
qué componente tomar, porque `DrumVoice`, `HapticSink` y `LatencyProbe` derivan todos de
`DrumHitSink`, que es el tipo del campo. **Ésta es la razón concreta de que `DrumHitSink` sea una
clase abstracta y no una interfaz**, como explicó la sección 2.6: Unity no serializa campos de tipo
interfaz, y sin serialización no hay arrastre en el inspector.

El orden de los elementos es el orden en que se reparte el golpe, pero no importa: el audio está
agendado a un instante absoluto del reloj DSP, así que unos microsegundos de diferencia en el
reparto no mueven nada.

`DrumHitFanout` es a su vez un `DrumHitSink`, y esa es la pieza que permite que `StickTracker`
tenga un solo campo de salida en lugar de tres.

### Paso 6 — `Tracker`

`GameObject → Create Empty`, nombre `Tracker`, componente `StickTracker`. **Este es el que hay que
llenar con cuidado**: seis campos, y cinco son referencias arrastradas.

| Campo del inspector | Qué arrastrarle | Qué pasa si está mal |
|---|---|---|
| Hand | `RightHand` (desplegable) | Se lee el control equivocado y no hay golpes |
| Xr Origin | el GameObject raíz **`XR Origin (XR Rig)`** | Vacío: excepción de referencia nula. Equivocado: el fallo silencioso de 4.5 |
| Controller | el objeto del control derecho, **el que tiene el `Tracked Pose Driver`** | El brazo `r` sale mal y la velocidad de punta queda falseada |
| Tip | el `Transform` vacío `Tip` de la punta de la baqueta | Si se arrastra el cilindro, se detecta el golpe con el centro de la baqueta |
| Pads | Tamaño **1**, Elemento 0 → `Pad` | Vacío: no hay nada que evaluar, silencio total |
| Sink | `Fanout` | Vacío: excepción en el primer golpe |
| Pose To Audio Offset | `0` | Se mide en el capítulo 6. **No se adivina** |

Para dos manos se duplica este GameObject y se cambia `Hand` a `LeftHand`, `Controller` al control
izquierdo y `Tip` a la punta de la baqueta izquierda. Los demás campos apuntan a lo mismo: los
receptores se comparten.

### Paso 7 — Audio del proyecto

Confirmar la lista del capítulo 1, sección 1.8, antes de medir nada:

| Ajuste | Valor |
|---|---|
| DSP Buffer Size | **Best Latency** |
| System Sample Rate | 48000 |
| Default Speaker Mode | Stereo |

Es el ajuste de mayor impacto en latencia de todo el proyecto y no cuesta nada verificarlo otra vez.

## 4.8 El sample: por qué tiene que ser de bombo

Falta una sola cosa: el sonido. Y la elección **no es estética, es un requisito del instrumento de
medición**.

### La restricción

La herramienta de medición del capítulo 5 (`scripts/latencia.py`) funciona grabando con un
micrófono externo, en un mismo archivo de audio, dos golpes: **el clic físico** de la punta del
control contra la superficie real —que marca el instante verdadero del impacto— y **el tambor
virtual** que sale por las bocinas del visor. La diferencia entre ambos, en milisegundos, es la
latencia. Es la única medición que incluye la cadena completa: tracking, frame, render y audio.

Para eso, el programa tiene que distinguir cuál de los dos transitorios es cuál. Y **no los
distingue por orden**, precisamente porque el signo de la latencia es lo que se está midiendo y
puede ser negativo: la predicción del plano armado puede hacer que el sonido salga *antes* del
contacto físico. Los clasifica por **centroide espectral**: el clic del plástico es un golpe seco y
agudo con el centro de masa espectral alto; el bombo es grave y lo tiene bajo. El de arriba es el
clic.

El código exige que los dos centroides difieran por un factor mínimo:

```python
RAZON_CENTROIDE_MIN = 2.5
```

Y si no lo hacen, se niega a dar un número y dice exactamente por qué:

> *"No se puede saber cuál es el clic físico y cuál el tambor. Causa habitual: se midió con tarola
> en lugar de bombo. El protocolo exige un sample grave, porque el clic del plástico y la tarola
> tienen contenido espectral parecido."*

**Una tarola tiene centroide espectral parecido al del clic del plástico.** Ambos son ataques secos
con mucha energía de alta frecuencia; el bordonero de la tarola sube todavía más el centroide. Con
tarola, la clasificación se vuelve una moneda al aire y la medición deja de existir. Con bombo
—que barre de unos 150 Hz a unos 50 Hz— la separación es amplia y la clasificación es robusta.
**El sample de bombo es un requisito del hito Go/No-Go del acta**, no una preferencia.

### Dónde conseguirlo

| Fuente | Qué buscar | Cuidado |
|---|---|---|
| **Freesound.org** | `kick drum` o `bass drum`, filtrando por licencia **CC0** | Requiere cuenta gratuita. Verificar la licencia de cada archivo, no del sitio |
| **Archive.org** | Colecciones de bancos de sonido de dominio público | Calidad muy variable |
| **Packs gratuitos de bombo** distribuidos por revistas y fabricantes de audio | Suelen venir en WAV 44.1 o 48 kHz | Leer los términos: "gratis" no siempre es "libre de redistribuir" |

<!-- VERIFICAR: confirmar la licencia concreta del archivo descargado antes de incluirlo en el repositorio del proyecto -->

Para un trabajo académico basta con documentar la procedencia y la licencia del archivo usado. Si
nada convence, un bombo sintético sirve perfectamente para medir: un seno que barra de 150 a 50 Hz
en 120 ms con una envolvente exponencial descendente es exactamente lo que la herramienta espera.

### Cómo importarlo

Copiar el WAV a `Assets/Audio/` y, con el clip seleccionado, en su inspector de importación:

| Ajuste | Valor | Por qué |
|---|---|---|
| Force To Mono | activado | `spatialBlend = 0`: el estéreo no aporta nada y duplica memoria y proceso |
| Load Type | **Decompress On Load** | El clip queda descomprimido en RAM. Descomprimir al vuelo en el primer golpe produce un tirón justo cuando se está midiendo |
| Compression Format | **PCM** | Sin decodificación de por medio. El clip dura menos de un segundo: el ahorro de una compresión no compensa |
| Preload Audio Data | activado | Evita que el primer golpe de la sesión pague la carga |
| Sample Rate Setting | Preserve Sample Rate, con el archivo ya a **48 kHz** | Cualquier otra tasa fuerza remuestreo, que es trabajo y retardo por voz |

Recortar el silencio del principio del archivo es obligatorio. Un WAV con 20 ms de silencio delante
del ataque **añade 20 ms de latencia** que ninguna optimización de la guía puede recuperar, y que
la medición del capítulo 5 atribuirá al sistema. Se revisa en cualquier editor de audio: la primera
muestra distinta de cero debe ser el ataque.

## 4.9 Correr las pruebas EditMode

Antes de construir el APK, y de hecho antes de tener el visor encendido, **la matemática del golpe
se verifica en la Mac**. Las pruebas viven en `proyecto-unity/Assets/Tests/EditMode/`.

`Window → General → Test Runner`, pestaña **EditMode**, botón **Run All**. Deben pasar **15
pruebas**, todas en verde.

| Grupo | Pruebas | Qué cubre |
|---|---|---|
| `DrumPadTests` | 6 | Geometría del pad: que el plano armado esté a 6 cm por delante, que la distancia con signo sea positiva del lado del jugador y negativa una vez pasado, que el radio ignore la altura sobre el plano, que un punto lejano quede fuera, y que al rotar el pad la normal siga al `Transform` |
| `DrumHitFanoutTests` | 2 | Que un golpe llegue íntegro a todos los receptores —velocidad e instante de impacto incluidos— y que un fanout sin destinos no reviente |
| `CrossSolverTests` | 7 | La matemática completa: fracción del intervalo en que ocurrió el cruce, instante de impacto (incluida la asimetría entre golpe lento y rápido), velocidad normal —que el movimiento lateral no cuente y que alejarse dé negativo— y la velocidad de punta con el ejemplo del giro de muñeca |

**Estas pruebas corren sin visor.** No hay `XRNode`, no hay `InputDevice`, no hay audio: son
funciones puras y `GameObject` creados en memoria. Eso es lo que compra la separación entre
`CrossSolver` —estático, sin estado, sin hardware— y `StickTracker`, que es el único que toca el
runtime de XR. Se puede verificar que la predicción de impacto es correcta, que la velocidad de
punta incluye el giro de muñeca y que el pad rotado se comporta bien, **todo en la Mac, en
segundos, mientras el Quest 3S está en su caja**.

Que las 15 pasen no demuestra que el sistema suene. Demuestra algo distinto y muy útil: que si no
suena, **el problema no está en la matemática**. Reduce el espacio de búsqueda a la configuración
de la escena, a las referencias del inspector o al hardware, que es justo lo que la sección 4.10
recorre.

Si el Test Runner aparece vacío o no lista la pestaña EditMode, falta el paquete **Test Framework**
(`com.unity.test-framework`) en el Package Manager.

## 4.10 Problemas frecuentes

| Síntoma | Causa | Qué hacer |
|---|---|---|
| No suena nada, ni un golpe | Algún campo del `StickTracker` vacío, o `Clip` sin asignar en `DrumVoice` | Revisar los seis campos del paso 6 y el `Clip` del paso 2. Un `Debug.Log` temporal dentro de `Evaluate` dice si el cruce se detecta |
| Suena pero solo con golpes muy fuertes | `Min Velocity` demasiado alto, o la orientación del pad no corresponde a la dirección del golpe | Bajar `Min Velocity` a 0.2 para probar; mirar los gizmos del pad en la vista de escena |
| Suena varias veces por golpe | Hay dos `StickTracker` apuntando a la misma mano, o el pad está en la lista `Pads` dos veces | Revisar la jerarquía. El rearme por posición impide el retrigger de una sola instancia, no de dos |
| El volumen no cambia con la fuerza | La curva `Velocity To Gain` quedó plana | Abrir la curva en el inspector; debe subir de (0.4, 0.2) a (6, 1) |
| Funciona mirando al frente y falla al girarse | El fallo de espacios de coordenadas de 4.5 | Verificar que `Xr Origin` apunta al GameObject raíz del rig y no a otra cosa |
| El sonido llega claramente tarde | El sample tiene silencio al principio, o `DSP Buffer Size` no está en Best Latency | Recortar el WAV; revisar 1.8 |
| Se siente la vibración antes del sonido | Es el comportamiento esperado si la predicción es grande: ambos se agendan al mismo `ImpactDsp`, pero el háptico del hardware tiene su propio retardo | No tocar nada todavía. Se cuantifica en el capítulo 5 |
| Muchas agendas tardías en el JSON de `LatencyProbe` | La predicción no alcanza: frames largos o golpes muy fuertes | Subir `Arm Distance`; revisar el frame rate en el visor. Capítulo 6 |
| El primer golpe de la sesión suena tarde y los demás bien | El clip no estaba precargado | `Preload Audio Data` y `Decompress On Load` en el inspector del clip (4.8) |

---

**Criterio de término: el pad suena al golpearlo dentro del Quest 3S, con vibración, y el volumen
cambia según la fuerza del golpe.** En el visor físico, no en el simulador. A partir de aquí el
sistema existe; lo que falta es saber cuántos milisegundos tarda, y eso es el capítulo 5.

---

# Capítulo 5 — Número de latencia real, en ms

Éste es el capítulo que decide si el proyecto sigue. El acta fija la medición de latencia como
**hito Go/No-Go en la semana 4**, no como verificación final. La razón es económica: si el golpe no
se siente causal, las seis piezas, el round-robin, las métricas y la sesión terapéutica son trabajo
construido sobre una base rota. Más vale saberlo en la semana 4 que en la 10.

## 5.1 Por qué no contar frames de video

El método que todo el mundo intenta primero es grabar en cámara lenta y contar frames entre el
golpe y el sonido. Un celular a 240 fps da un frame cada **4.17 ms**. Con un umbral de 25 ms, eso
es una precisión del 17% del rango que se quiere medir: suficiente para saber si estás en 100 ms o
en 20, inútil para decidir entre 22 y 28.

La grabación de audio no tiene ese problema. A 48 kHz cada muestra es **0.021 ms**. Y como resulta
que el golpe físico *produce sonido por sí mismo*, ese sonido puede servir de referencia.

## 5.2 El clic físico como verdad de referencia

Se coloca un objeto real —canto de mesa, libro grueso, pad de práctica de batería— exactamente
donde vive el pad virtual. Al golpear con el control se producen **dos** sonidos:

```
                    t0                 t1
                    │                  │
  ──────────────────┼──────────────────┼──────────────>  tiempo
                    │                  │
              clic del control    bombo virtual
              contra la mesa      por las bocinas
              (INSTANTE REAL      del visor
               DEL IMPACTO)

                    └────── Δ ─────────┘
```

Ambos entran por el mismo micrófono, al mismo archivo, en la misma línea de tiempo. **Δ = t1 − t0
es la latencia punta a punta**, con precisión de muestra y sin ninguna calibración de equipo.

No hace falta un micrófono bueno. El del celular sobra: lo único que importa es la posición
relativa de dos transitorios dentro de la misma grabación, y eso es inmune a la calidad del
micrófono, a su respuesta en frecuencia y a su ganancia.

## 5.3 Montaje

**1. La superficie física.** Algo rígido que produzca un clic seco. Un libro de tapa dura, el canto
de una mesa, un pad de práctica. Evita superficies blandas: una almohada no produce transitorio y
te quedas sin `t0`.

**2. Calibrar el pad virtual sobre ella.** Para esto existe `PadCalibrator`:

```csharp
if (pressed && !prevPressed)
{
    pad.transform.position = tip.position;
    pad.transform.rotation = Quaternion.identity;   // normal = Vector3.up
    Debug.Log($"[PadCalibrator] Pad recolocado en {tip.position}");
}
```

Apoyas la punta del control sobre la superficie física, presionas el botón primario (A o X), y el
pad virtual salta a ese punto exacto con la normal apuntando hacia arriba. La consola confirma con
`[PadCalibrator] Pad recolocado en (...)`.

**Sin este paso la medición no significa nada.** Si el pad virtual está 3 cm por encima de la mesa,
el sonido virtual se dispara 3 cm antes del contacto físico y estarías midiendo un error de montaje
disfrazado de latencia negativa.

**3. Audio por las bocinas del visor. Jamás por Bluetooth.** Los audífonos inalámbricos añaden
entre 100 y 200 ms de latencia propia. Medirías el códec Bluetooth, no tu aplicación. Las bocinas
integradas del Quest 3S sirven perfectamente y además las capta el micrófono del celular junto con
el clic, que es justo lo que se necesita.

**4. Celular a menos de 30 cm** de la mesa y del visor. El sonido recorre **34 cm por milisegundo**.
Si el micrófono está a 1 m de la mesa y a 30 cm del visor, la diferencia de trayecto mete ~2 ms de
sesgo en Δ. A menos de 30 cm de ambos, el error de geometría queda por debajo del ruido de la
medición.

**5. Sample de bombo, no de tarola.** No es preferencia estética: es un **requisito del
instrumento de medición**. La herramienta distingue el clic físico del tambor virtual por centroide
espectral, y una tarola tiene contenido espectral parecido al del clic del plástico. Si mides con
tarola, `latencia.py` se niega a adivinar y te lo dice:

```
ValueError: Par en t=1.043s: centroides demasiado parecidos (4210 Hz y 3890 Hz, razón 1.1).
No se puede saber cuál es el clic físico y cuál el tambor. Causa habitual: se midió con tarola
en lugar de bombo. El protocolo exige un sample grave, porque el clic del plástico y la tarola
tienen contenido espectral parecido.
```

El umbral está en `RAZON_CENTROIDE_MIN = 2.5` dentro de `scripts/latencia.py`. Con bombo la razón
sale del orden de 15 a 80; con tarola, cerca de 1.

**6. Grabar.** Cualquier grabadora de voz que produzca WAV. A 48 kHz si se puede elegir. Mono o
estéreo da igual: la herramienta promedia los canales.

## 5.4 Dos corridas, veinte golpes cada una

**Corrida A — con predicción.** Configuración normal, `armDistance = 0.06` en el `DrumPad`.

**Corrida B — sin predicción.** Pones `armDistance = 0` en el inspector del `DrumPad` y vuelves a
compilar. Con distancia de armado cero, el plano armado coincide con la superficie del pad y
`CrossSolver.ImpactDsp` devuelve el instante del cruce sin sumar nada: el sonido sale cuando el
frame lo detecta, sin adelanto.

**Veinte golpes por corrida.** No cinco. El número que decide es el percentil 90, y un p90 sobre
cinco muestras no es un percentil, es el máximo con otro nombre.

Ese par de números —A contra B— es la **evidencia documental** de que la mitigación del plano
armado funciona. Sin la corrida B no puedes afirmar en el informe que la predicción sirve de algo;
solo que el resultado final entró en rango, que es una afirmación mucho más débil.

## 5.5 Análisis

```bash
~/.pyenv/versions/redes/bin/python scripts/latencia.py mediciones/con_prediccion.wav \
    --etiqueta "con predicción" --detalle

~/.pyenv/versions/redes/bin/python scripts/latencia.py mediciones/sin_prediccion.wav \
    --etiqueta "sin predicción"
```

La salida tiene esta forma:

```
Corrida: con predicción
Archivo: mediciones/con_prediccion.wav  (48000 Hz, 9.0 s)
Transitorios detectados: 41   Golpes emparejados: 20
Mediana:  +11.29 ms
p90:      +13.06 ms   <- el que decide
Rango:     +8.23 ..  +14.56 ms
Criterio -10 .. +25 ms  ->  APRUEBA
```

**Cómo leer el diagnóstico.** La línea de `Transitorios detectados` contra `Golpes emparejados` es
lo primero que hay que mirar. Veinte golpes deberían producir alrededor de **40 transitorios** y
**20 emparejados**. Si ves 20 transitorios y 10 emparejados, el detector se está perdiendo la mitad
de los eventos. Si ves 80 transitorios, está inventando.

**`--margen-db` es la perilla para eso.** El detector decide qué es un transitorio comparándolo
contra una guarda que decae; el margen es cuántos decibelios tiene que superarla. El valor por
defecto es 6 dB y tiene una **meseta estrecha**: a 5 dB aparecen transitorios de más, a 8 dB se
pierde el segundo transitorio de los pares muy juntos. Sobre grabaciones reales, con ruido de sala
y un micrófono de celular, puede hacer falta moverlo:

```bash
~/.pyenv/versions/redes/bin/python scripts/latencia.py mediciones/con_prediccion.wav --margen-db 7
```

Súbelo si detecta de más, bájalo si se pierde golpes. Y vuelve a mirar la línea de diagnóstico.

## 5.6 Cómo leer un Δ negativo

**Δ negativo no es un error de medición.** Significa que el bombo virtual sonó *antes* de que el
control tocara la mesa. Con la predicción del plano armado bien calibrada, eso es exactamente lo
que debe pasar: estás disparando el audio con 6 cm de anticipación, extrapolando el instante de
contacto a partir de la velocidad.

Por eso el criterio de aceptación es **asimétrico**:

$$-10\text{ ms} \le \Delta(p_{90}) \le +25\text{ ms}$$

El oído perdona alrededor de 10 ms de adelanto —lo integra como simultáneo— y castiga con dureza
el retraso. Un sonido 20 ms tarde se percibe como un eco despegado del gesto; un sonido 8 ms
temprano no se percibe en absoluto. **El objetivo no es Δ = 0.**

**Y el p90 es el que decide, no la mediana.** El golpe que arruina la sensación no es el promedio:
es el que llegó tarde. Una mediana de +12 ms con un p90 de +40 ms describe un sistema que se
siente mal una de cada diez veces, y eso basta para romper la ilusión de causalidad.

## 5.7 Qué hacer si no aprueba

En este orden, del más barato al más caro:

| # | Intervención | Ganancia típica |
|---|---|---|
| 1 | Verificar **DSP Buffer Size = Best Latency** y **System Sample Rate = 48000** en `Project Settings → Audio` | ~6 ms |
| 2 | Subir `armDistance` de 0.06 a 0.08–0.10 m | Adelanta el disparo proporcionalmente |
| 3 | Calibrar `poseToAudioOffset` (capítulo 6) | Hasta 10 ms |
| 4 | Fijar 72 Hz en lugar de 90 Hz con caídas | Frame estable > frame corto e inestable |

El paso 1 es el que más veces resuelve el problema, y es el que más veces se olvida: el valor por
defecto de Unity en Android es 512 samples, que son ~11 ms en lugar de ~5.

## 5.8 La sonda interna, y por qué no sustituye a esto

`LatencyProbe` registra cada golpe dentro de la aplicación y vuelca un JSON al salir:

```json
{
    "totalGolpes": 20,
    "agendasTardias": 1,
    "registros": [
        { "dspImpacto": 1042.318, "dspAhora": 1042.303, "velocidad": 3.9, "agendaTardia": false }
    ]
}
```

El campo que importa es **`agendasTardias`**: cuenta cuántas veces la predicción llegó tarde y el
audio tuvo que dispararse de inmediato en lugar de agendarse. Es tu métrica interna de calidad. Un
porcentaje alto significa que `armDistance` es demasiado corto para la velocidad a la que golpea
ese usuario.

El archivo queda en `Application.persistentDataPath` del visor. Para sacarlo:

```bash
$ADB shell ls /sdcard/Android/data/<tu.bundle.id>/files/
$ADB pull /sdcard/Android/data/<tu.bundle.id>/files/latencia_20260925_143012.json mediciones/
```

**Limitación declarada, y es importante:** la sonda mide **solo el tramo de audio**. Conoce el
instante en que la aplicación decidió disparar y el instante en que lo agendó, pero no sabe nada de
la latencia del tracking ni de la presentación. Un sistema con 40 ms de latencia de tracking puede
mostrar cero agendas tardías y sentirse horrible.

**La medición externa de §5.2 es la que vale para el Go/No-Go.** La sonda es diagnóstico
complementario, no sustituto.

## 5.9 Registrar el resultado

El hito exige dejar constancia. Anota, con fecha:

| | Con predicción | Sin predicción |
|---|---|---|
| Golpes | 20 | 20 |
| Mediana | | |
| p90 | | |
| Rango | | |
| Veredicto | | |

Y la configuración con la que se midió: versión de Unity, DSP Buffer Size, sample rate, tasa de
refresco, `armDistance`, `poseToAudioOffset`. Sin eso el número no es reproducible y no sirve como
evidencia.

**Criterio de término del capítulo 5: dos números de latencia con mediana y p90, y un veredicto.**

---

# Capítulo 6 — Ajustes que bajan la latencia

Este capítulo no se lee, se ejecuta. Cada ajuste se aplica, **se vuelve a medir con el protocolo
del capítulo 5**, y se anota. Al final tienes una tabla con números tuyos, no con estimaciones de
una guía.

## 6.1 El presupuesto de latencia

De dónde salen los milisegundos:

| Fuente | Estimado |
|---|---|
| Tracking del controlador | ~10 ms |
| Un frame a 90 Hz | ~11 ms |
| Buffer de audio a 256 samples / 48 kHz (Best Latency) | ~5 ms |
| **Total** | **~26 ms** |

Con el valor por defecto de Unity en Android (512 samples) el total sube a **~32 ms**, que ya es
claramente perceptible.

Fíjate en algo: 26 ms ya está por encima del criterio de +25. **La predicción del plano armado es
lo que hace que el sistema pase.** No es una optimización opcional que se añade al final; es la
pieza que convierte un presupuesto de 26 ms en una latencia percibida cercana a cero, adelantando
el disparo del audio unos 15 ms a velocidad típica de golpe. Sin ella, el proyecto no cumple.

## 6.2 Los ajustes, en orden de impacto

### DSP Buffer Size

`Project Settings → Audio → DSP Buffer Size`. Tres opciones:

| Valor | Samples | Latencia del buffer |
|---|---|---|
| Best performance | 1024 | ~21 ms |
| Good latency | 512 (**defecto en Android**) | ~11 ms |
| **Best latency** | **256** | **~5 ms** |

Seis milisegundos entre el defecto y el correcto. Es el ajuste de mayor impacto de todo el
proyecto y está a dos clics. Si el buffer es demasiado pequeño para el dispositivo aparecen
crujidos y cortes; en el Quest 3S, 256 samples es estable.

### System Sample Rate

`Project Settings → Audio → System Sample Rate = 48000`. Es la tasa nativa del Quest. Cualquier
otro valor obliga al sistema a remuestrear en tiempo real, lo que añade latencia y consume CPU sin
darte nada. Asegúrate además de que tus samples de batería estén a 48 kHz: un WAV a 44.1 kHz se
remuestrea igual, aunque el proyecto esté configurado a 48.

### Vulkan en lugar de OpenGLES3

Ya está en la lista del capítulo 1, pero vale repetir por qué importa aquí: si OpenGLES3 queda en
la lista de Graphics APIs y Vulkan falla al arrancar, el visor cae silenciosamente al camino lento.
La aplicación funciona, nadie ve un error, y tus mediciones de latencia dejan de describir el
sistema que crees estar midiendo. Quita OpenGLES3 de la lista.

### 72 Hz fijo frente a 90 Hz con caídas

Contraintuitivo: **un frame estable de 13.9 ms (72 Hz) vence a uno inestable de 11.1 ms (90 Hz)**.

La razón es que la latencia que se siente es la del peor frame, no la del promedio. A 90 Hz con
caídas ocasionales a 45, los frames largos duran 22 ms y ésos son los que rompen la sensación de
causalidad. A 72 Hz sostenido no hay frames largos.

Empieza en 72 Hz fijo. Sube a 90 solo cuando el perfilado demuestre margen holgado, y vuelve a
medir la latencia después de subir: si aparecen caídas, 90 Hz te está costando latencia en lugar de
ahorrártela.

### `spatialBlend = 0` y bypass de efectos

Ya está en `DrumVoice`:

```csharp
src.spatialBlend          = 0f;     // 2D: sin coste de espacialización
src.bypassEffects         = true;
src.bypassListenerEffects = true;
src.bypassReverbZones     = true;
```

Cada procesador en el camino del audio añade trabajo entre la decisión de reproducir y la salida
por la bocina. La espacialización HRTF, en particular, no es gratis. Para la etapa A no aporta
nada terapéutico y sí cuesta milisegundos. En la etapa B, si se quiere espacializar, hay que
volver a medir.

## 6.3 Calibrar `poseToAudioOffset`

Éste es el único parámetro del sistema que **no se puede deducir**. Hay que medirlo.

El campo está en `StickTracker`, con este tooltip:

> Corrección constante entre el reloj de pose y el de audio, en segundos. Se determina midiendo,
> en el capítulo 6. No se adivina.

**Por qué existe.** La pose del controlador que Unity te entrega viene predicha al instante de
*presentación en pantalla*, no al instante del reloj de audio. Son dos relojes distintos con un
desfase que depende del runtime, de la tasa de refresco y del tamaño del buffer. Ese desfase es
constante para una configuración dada, pero no hay API que lo revele.

**Procedimiento.** Barrido de −10 a +10 ms en pasos de 2 ms. Para cada valor: compilas, mides 20
golpes con el protocolo del capítulo 5, anotas el p90. Te quedas con el valor que lo minimiza en
valor absoluto.

| `poseToAudioOffset` | p90 medido |
|---|---|
| −0.010 | |
| −0.008 | |
| −0.006 | |
| −0.004 | |
| −0.002 | |
| 0.000 | |
| +0.002 | |
| +0.004 | |
| +0.006 | |
| +0.008 | |
| +0.010 | |

Once compilaciones a 1–3 minutos cada una, más 20 golpes por corrida. Es una tarde de trabajo
tediosa y es la más rentable del capítulo: recupera hasta 10 ms sin tocar una línea de código.

**Atajo si vas con prisa:** mide primero en 0.000, −0.006 y +0.006. La curva es monótona a cada
lado del mínimo, así que esos tres puntos te dicen hacia dónde ir y puedes refinar solo esa mitad.

## 6.4 La tabla que produce este capítulo

| Ajuste | Antes | Después | Ganancia |
|---|---|---|---|
| DSP Buffer 512 → 256 | | | |
| Sample rate → 48000 | | | |
| OpenGLES3 fuera | | | |
| 90 Hz → 72 Hz fijo | | | |
| `poseToAudioOffset` calibrado | | | |
| **Total** | | | |

Cada celda es un p90 sobre 20 golpes. Esta tabla es el anexo técnico del informe del hito.

---

# Capítulo 7 — Esbozo de la etapa B

La etapa A entrega **un** pad. La B entrega el instrumento: seis piezas tocables con las dos manos,
con dinámica y sin sonido robótico. Este capítulo no trae código; trae las decisiones de
arquitectura y sus razones, para que cuando lo construyas no tengas que redescubrirlas.

**No empieces la etapa B hasta que el capítulo 5 haya dado un veredicto de APRUEBA.**

## 7.1 Seis piezas y el filtro de proximidad

En la etapa A, `StickTracker` prueba un plano por mano y por frame. Con seis piezas y dos manos son
**12 pruebas por frame**, y cada una implica dos productos punto y una proyección.

La solución es el esquema híbrido: un **collider amplio** alrededor de cada pieza actúa como filtro
de proximidad, y solo dentro de él se ejecuta la prueba de plano. El collider no detecta el golpe
—eso seguiría teniendo el problema de tunelado y del paso de física del capítulo 4— sino que
responde a una pregunta mucho más barata: *¿está esta baqueta cerca de esta pieza?*

**Por qué en A no está.** Con un solo pad, el filtro no ahorra nada: cuesta lo mismo preguntar
"¿estás cerca?" que hacer la prueba directamente. Meterlo en A habría sido complejidad sin
beneficio, y además habría contaminado la medición de latencia con una capa más entre el
movimiento y el sonido.

## 7.2 Capas de velocity y round-robin

Un solo sample reproducido a distinto volumen **no suena a batería**. Un bombo golpeado suave y uno
golpeado fuerte no se diferencian en volumen: se diferencian en contenido espectral, en el ataque,
en cuánto excita el parche. Subir el volumen de un golpe suave da un golpe suave más fuerte, no un
golpe fuerte.

De ahí las dos técnicas:

- **Capas de velocity.** Tres grabaciones por pieza —suave, media, fuerte— y se elige según la
  velocidad del golpe.
- **Round-robin.** Dos o tres variantes por capa, alternadas. Sin esto, dos golpes seguidos
  reproducen exactamente la misma onda y el oído lo detecta al instante como artificial. Es el
  efecto "ametralladora" y es lo que más delata a una batería programada.

Son 6 piezas × 3 capas × 2–3 variantes = **36 a 54 samples**. Conseguirlos o grabarlos es trabajo
real y hay que planificarlo.

La estructura para el mapeo ya está puesta en `DrumVoice`:

```csharp
[SerializeField] AnimationCurve velocityToGain =
    AnimationCurve.Linear(0.4f, 0.2f, 6f, 1f);
```

Una `AnimationCurve` en el inspector se edita arrastrando puntos, **sin recompilar**. En la etapa B
hay que extenderla a una curva que devuelva capa *y* ganancia, pero la decisión de exponer el mapeo
como curva editable en lugar de constantes en código ya está tomada. El rango útil de velocidad es
**0.5 a 8 m/s**.

## 7.3 Dimensionar el pool de voces

`DrumVoice` preinstancia N `AudioSource` en `Awake` y los reparte en círculo. Cuando se agotan, la
voz más vieja se corta a media cola.

Para dimensionarlo, el peor caso: un redoble de semicorcheas a 160 BPM son **10.6 golpes por
segundo por mano**. Con la cola de un crash durando 3 segundos, un golpe de crash puede solaparse
con 30 golpes posteriores. En la práctica, 8 voces por pieza bastan para tambores y 16 para
platillos.

**Lo que no se negocia es que se reserven en `Awake`.** Ni `Instantiate`, ni `AddComponent`, ni
`new` en el camino del golpe. El recolector de basura produce caídas de frame, y en este proyecto
una caída de frame es latencia medible.

## 7.4 Anti-retrigger por posición

Ya está implementado en `StickTracker` desde la etapa A:

```csharp
// Rearme POR POSICIÓN, no por tiempo: el pad revive cuando la baqueta vuelve a salir.
// Un cooldown temporal destruiría los redobles.
if (dNow > 0f && dPrev <= 0f) { armed[pad] = true; return; }
```

**Por qué se eligió así desde A** y no se dejó para B: el enfoque obvio —un cooldown de, digamos,
100 ms tras cada golpe— parece funcionar en pruebas manuales y **destruye los redobles**.
Semicorcheas a 160 BPM son 94 ms entre golpes. Un cooldown de 100 ms se comería uno de cada dos.

El bug aparecería en la etapa B, al probar con alguien que sepa tocar, y sería difícil de
diagnosticar porque en pruebas lentas todo funciona. Poner la histéresis correcta desde A cuesta
tres líneas y evita ese descubrimiento tardío.

## 7.5 Presupuesto de rendimiento

Heredado del diseño técnico del proyecto, se aplica a la etapa B:

- Menos de **500 draw calls**
- Menos de **300 000 triángulos**
- Texturas comprimidas en **ASTC**
- Iluminación **completamente bakeada**, sin GI en tiempo real
- **Single-pass instanced**
- **Foveated rendering** activado
- Objetivo **72 Hz fijo**; 90 Hz solo si el margen lo permite y se vuelve a medir la latencia

## 7.6 Lo que queda fuera, y por qué

| Fuera de alcance | Razón |
|---|---|
| Hi-hat con pedal abierto/cerrado | Requiere entrada continua y cross-fade entre estados. Complejidad alta, valor terapéutico bajo en esta etapa |
| Audio espacializado (Meta XR Audio SDK) | Suma latencia al camino del audio. No aporta valor terapéutico medible: el usuario está frente a la batería, no rodeado de ella |
| Baqueta con Rigidbody físico | La simulación física introduce el paso de física en el camino del golpe, que es exactamente lo que el capítulo 4 evitó |
| Hand tracking | Descartado en el acta: no da háptico ni lectura confiable de velocidad, y ambos son esenciales |
| `SessionDirector`, `RhythmGuide`, `MetricsLogger` completo, STAI-6 | Etapa C. Son la sesión terapéutica, no el instrumento |
| Entorno 3D artístico | Etapa C |

## 7.7 Qué sigue

En este orden, sin saltarse pasos:

1. **Correr las 15 pruebas EditMode.** `Window → General → Test Runner → EditMode → Run All`. No
   necesitan visor. Si alguna falla, se arregla antes de tocar hardware.
2. **Cumplir el capítulo 1** hasta ver el cubo girando dentro del Quest 3S.
3. **Capítulos 3 y 4** hasta que el pad suene al golpearlo con háptico.
4. **Capítulo 5**, hasta tener dos números y un veredicto.
5. **Capítulo 6** si el veredicto fue NO APRUEBA, o para afinar si fue APRUEBA por poco margen.
6. **Solo entonces**, la etapa B.

El paso 4 es el hito. Todo lo anterior existe para llegar a él, y todo lo posterior depende de que
haya salido bien.
