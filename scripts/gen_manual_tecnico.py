# -*- coding: utf-8 -*-
"""Genera el manual tecnico. Cierra QM.2.

Los datos que caducan salen de manual_datos.DATOS, no de aqui: versiones, identificador del
paquete, comandos del menu, orden de los constructores, estados, pruebas y paquetes ausentes.
Aqui va la prosa, que es lo que no se puede extraer.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import manual_datos
import neutro

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")
DOC = os.path.join(SALIDA, "14_Manual_Tecnico.docx")
D = manual_datos.DATOS
FECHA = "18 de noviembre de 2026"


def doc():
    d = neutro.nuevo()

    neutro.portada(
        d, "Manual técnico",
        "Simulación de Batería en Realidad Virtual — %s %s" % (D["producto"], D["version"]),
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha", FECHA),
         ("Actividad", "QM.2 — Manual técnico de instalación y ejecución")])

    neutro.P(d,
        "Este manual es para quien tenga que instalar, compilar, modificar o desinstalar la "
        "aplicación sin haber participado en su desarrollo. Supone que sabe programar, y no "
        "supone nada sobre Unity ni sobre realidad virtual.")
    neutro.P(d,
        "El repositorio del prototipo lleva un archivo README.md con la misma información en "
        "forma de referencia rápida, para quien ya trabaja en él a diario. Si los dos se "
        "contradicen, manda el repositorio: ahí es donde se mide.")

    # ------------------------------------------------------------------ 1
    neutro.H(d, "1. Qué necesitas antes de empezar", 1)
    neutro.table(d, ["Qué", "Cuál", "Por qué esa"], [
        ["Visor", "Meta Quest 3 o Quest 3S, en modo de desarrollador",
         "La aplicación corre dentro del visor, sin PC. Quest Link no se usa: ninguna máquina "
         "del equipo tiene GPU compatible."],
        ["Unity", "%s, y no otra" % D["unity"],
         "El proyecto trae su carpeta ProjectSettings versionada. Abrirlo con otra versión la "
         "migra y cambia archivos que nadie revisó."],
        ["Módulo de Unity", "Android Build Support, con el SDK y el NDK",
         "Sin él no aparece Android como plataforma de compilación."],
        ["Herramientas de línea", "adb, que viene dentro del módulo de Android",
         "Instalar, desinstalar y recoger mediciones se hacen con adb. quest.sh ya lo busca "
         "dentro de la carpeta de Unity."],
        ["Cuenta de Unity", "Una con los dos paquetes del Asset Store de la sección 2",
         "Esos paquetes no están en el repositorio y su licencia no permite redistribuirlos."],
    ], widths=[2.8, 5.2, 7.0], fs=9, negritas_col0=True)

    neutro.P(d,
        "El modo de desarrollador del visor se activa desde la aplicación móvil de Meta, en los "
        "ajustes del dispositivo. Sin él, adb no ve el visor y no se puede instalar nada que no "
        "venga de la tienda.")

    # ------------------------------------------------------------------ 2
    neutro.H(d, "2. Instalar el proyecto desde cero", 1)
    neutro.P(d, "Clonar el repositorio del prototipo:")
    bloque(d, "git clone git@github.com:AbiudBenitez/BateriaVR.git\ncd BateriaVR")

    neutro.H(d, "2.1 Faltan dos paquetes, y es a propósito", 2)
    neutro.P(d,
        "Dos paquetes del Asset Store no están en el repositorio. Su licencia —Standard Unity "
        "Asset Store EULA— permite usarlos dentro de una aplicación pero no redistribuir los "
        "archivos originales, así que incluirlos sería incumplirla. Sin ellos el proyecto abre "
        "y funciona, pero la escena aparece con referencias perdidas en el entorno: el bosque "
        "no sale.")
    neutro.table(d, ["Paquete", "Id", "Qué hacer después de importarlo"], [
        [D["ausentes"][0]["nombre"], D["ausentes"][0]["id"],
         "Pasar el menú Batería → Entorno → Convertir bosque a URP"],
        [D["ausentes"][1]["nombre"], D["ausentes"][1]["id"],
         "Borrar la carpeta Demo que trae el paquete"],
    ], widths=[6.5, 1.5, 7.0], fs=9)
    neutro.P(d,
        "El código que los adapta sí está versionado —el shader de follaje, el convertidor a "
        "URP y el constructor del bosque— porque es obra propia y no parte del paquete.")
    neutro.P(d,
        "Todo lo demás viene completo: el kit de batería, la música, las pistas de práctica y "
        "el entorno propio, cada uno con su atribución. Ver la sección 12.")

    # ------------------------------------------------------------------ 3
    neutro.H(d, "3. Abrir el proyecto y reconstruir la escena", 1)
    neutro.P(d,
        "Los componentes de la escena se cablean por menú, no a mano en el inspector. No es "
        "comodidad: cablear veinte campos a mano es justo donde se cuelan los errores, y este "
        "proyecto ya gastó cinco sesiones de visor en defectos de cableado y no de diseño.")
    neutro.P(d,
        "Si algo aparece desconectado, hay que pasar los cuatro constructores y el orden "
        "importa:", bold=True)
    neutro.table(d, ["Orden", "Comando del menú", "Qué hace y por qué va aquí"],
                 [[str(i + 1), c[0].replace("Batería → ", ""), c[1]]
                  for i, c in enumerate(D["constructores"])],
                 widths=[1.3, 5.5, 8.2], fs=9)
    neutro.P(d,
        "El constructor del kit barre la escena entera y rellena cualquier campo de lista de "
        "pads que encuentre, así que no hay que acordarse de qué componentes los usan. Esa "
        "barrida existe porque una vez solo se recableó uno de ellos y el bombo se quedó sin "
        "destino: las notas del bombo no aparecían y nada lo avisaba.")

    neutro.H(d, "3.1 Todos los comandos del menú", 2)
    neutro.P(d,
        "El proyecto añade %d comandos al menú del editor, repartidos así."
        % sum(len(v) for v in D["menu"].values()))
    for grupo in sorted(D["menu"]):
        titulo = "Batería" if grupo == "(raíz)" else "Batería → %s" % grupo
        neutro.P(d, "%s — %d comandos" % (titulo, len(D["menu"][grupo])), bold=True, after=4)
        neutro.bullets(d, D["menu"][grupo])

    # ------------------------------------------------------------------ 4
    neutro.H(d, "4. Compilar la aplicación", 1)
    neutro.P(d, "Desde el editor: menú Batería → Compilar APK. Sin abrir el editor:")
    bloque(d, 'Unity -batchmode -quit -projectpath "$PWD" -executeMethod BuildAPK.DesdeLinea')
    neutro.table(d, ["Ajuste", "Valor"], [
        ["Plataforma", "Android"],
        ["Backend de scripting", "IL2CPP"],
        ["Arquitectura", "ARM64"],
        ["API de gráficos", "Vulkan"],
        ["Pipeline", "URP, con el perfil móvil"],
        ["Identificador del paquete", D["paquete"]],
        ["Versión", D["version"]],
        ["Dónde cae el APK", "Builds/bateria.apk"],
    ], widths=[5.0, 10.0], fs=9, negritas_col0=True)
    neutro.P(d,
        "El APK no está en el repositorio: son unos 60 MB de binario que cambian en cada "
        "compilación. Hay que compilarlo o pedírselo a quien lo tenga.")

    # ------------------------------------------------------------------ 5
    neutro.H(d, "5. Instalar en el visor", 1)
    neutro.P(d,
        "La primera vez hace falta el cable, solo para decirle al visor que acepte conexiones "
        "inalámbricas. Después se trabaja sin cable.")
    bloque(d, "./scripts/quest.sh wifi      # una vez, con el cable puesto\n"
              "./scripts/quest.sh install   # instala Builds/bateria.apk\n"
              "./scripts/quest.sh ip        # comprueba que sigue conectado")
    neutro.P(d,
        "El modo inalámbrico se pierde cuando el visor se reinicia; hay que repetir el paso "
        "del cable. La instalación conserva los datos de sesión que ya hubiera en el visor, y "
        "si las firmas no cuadran desinstala y reinstala, lo que sí los borra.")
    neutro.P(d,
        "quest.sh lee el identificador del paquete de ProjectSettings y no lo lleva escrito. "
        "Estuvo escrito a mano, con el valor de la plantilla de Unity, y la recogida de "
        "mediciones apuntaba a una carpeta que no existía.")

    # ------------------------------------------------------------------ 6
    neutro.H(d, "6. Desinstalar", 1)
    neutro.P(d,
        "Desinstalar borra los datos de sesión que la aplicación guardó en el visor, y esos "
        "datos son la evidencia de las pruebas con usuarios. Bájalos antes.", bold=True)
    bloque(d, "./scripts/quest.sh pull        # PRIMERO: baja mediciones y trazas\n"
              "./scripts/quest.sh uninstall   # pide confirmación antes de borrar")
    neutro.P(d,
        "El comando avisa cuántos archivos de datos hay en el visor y espera que se escriba SI "
        "en mayúsculas. Cualquier otra respuesta cancela sin borrar nada.")

    neutro.H(d, "6.1 Desde el visor, sin computadora", 2)
    neutro.P(d,
        "En el visor: Aplicaciones, filtro «Orígenes desconocidos», localizar %s, menú de tres "
        "puntos, Desinstalar. Es la vía para quien solo tiene el visor a mano."
        % D["producto"])

    neutro.H(d, "6.2 Qué queda atrás", 2)
    neutro.table(d, ["Qué", "Dónde", "Sobrevive a la desinstalación"], [
        ["Mediciones de sesión y trazas",
         "/sdcard/Android/data/%s/files" % D["paquete"], "No. Se borran."],
        ["Marca de tutorial visto",
         "El mismo directorio, tutorial_visto.txt", "No. Se borra."],
        ["Capturas de pantalla", "/sdcard/Oculus/Screenshots",
         "Sí. Son del sistema del visor, no de la aplicación."],
    ], widths=[4.6, 6.4, 4.0], fs=9, negritas_col0=True)
    neutro.P(d,
        "La marca de tutorial visto es un archivo y no una preferencia de Unity precisamente "
        "por esto: las preferencias de una compilación de Android no se pueden borrar sin "
        "acceso de raíz, así que al completar el tutorial una vez quedaba imposible repetirlo. "
        "Para volver a verlo sin desinstalar: ./scripts/quest.sh tutorial.")

    # ------------------------------------------------------------------ 7
    neutro.H(d, "7. Cómo modificar la aplicación", 1)
    neutro.P(d,
        "Las seis modificaciones que el proyecto previó. Cada una dice dónde se toca y qué "
        "hay que volver a pasar después.")

    neutro.H(d, "7.1 Cambiar el kit de batería", 2)
    neutro.P(d,
        "La disposición de las piezas —cuántas, dónde y de qué tamaño— está en un solo sitio, "
        "DisposicionKit, y el constructor la consume. Cambiar la tabla y pasar Batería → "
        "Construir kit de 7 piezas. El constructor recablea solo todo lo que use pads.")
    neutro.P(d,
        "Las muestras de sonido se eligen por pieza y por intensidad desde una sola lista "
        "ordenada. Si se añaden muestras, pasar Batería → Ajustar importación de los samples: "
        "una muestra importada con la configuración por omisión se descomprime en memoria y "
        "cuesta fotogramas.")

    neutro.H(d, "7.2 Añadir una pista de práctica", 2)
    neutro.P(d,
        "Los patrones son datos, no código: un archivo declara qué pieza suena en qué pulso, y "
        "de ahí salen a la vez el audio del acompañamiento y el mapa de notas que el jugador "
        "toca. Una sola definición a propósito: cuando eran dos sitios, el reloj corría a 80 "
        "pulsos por minuto y el mapa declaraba 79.98.")
    neutro.P(d,
        "Añadir el patrón, pasar Batería → Importar pistas de práctica, y aparece en el "
        "selector sin tocar nada más. Dos reglas que el archivo ya vigila con pruebas: el "
        "acompañamiento y lo que toca el jugador no comparten pieza —si no, el jugador no "
        "distingue su golpe del de la pista— y el acompañamiento marca cuatro golpes por "
        "compás, porque en corcheas suena 1.6 veces por cada golpe propio y compite en vez de "
        "guiar.")

    neutro.H(d, "7.3 Cambiar el entorno", 2)
    neutro.P(d,
        "Hay %d variantes de entorno en el submenú Batería → Entorno, cada una un comando que "
        "reconstruye la escena. Se eligen pasando el comando; no hay que tocar la iluminación "
        "a mano." % len(D["menu"].get("Entorno", [])))
    neutro.P(d,
        "Si se añade una variante, hay que medir los fotogramas por segundo otra vez: Batería → "
        "Montar sondas de medición, compilar, y ./scripts/quest.sh fps. El criterio es menos "
        "del 5 % de fotogramas fuera de sincronía vertical.")

    neutro.H(d, "7.4 Mover las ventanas de juicio", 2)
    neutro.P(d,
        "Las ventanas que deciden si un golpe es perfecto, bueno o fallado van en milisegundos "
        "y nunca en fracciones de pulso: una ventana en fracciones se encoge al subir el tempo, "
        "y la precisión de una persona no escala con el tempo.")
    neutro.P(d,
        "Están en un solo sitio y el tutorial usa las mismas: si el tutorial aprobara con una "
        "ventana más ancha, alguien pasaría ahí y fallaría en el juego. Cambiarlas obliga a "
        "revisar el criterio de aceptación del proyecto, porque la ventana estrecha es la "
        "medida que el acta compromete.")

    neutro.H(d, "7.5 Añadir una pantalla al flujo", 2)
    neutro.P(d,
        "Las transiciones son una tabla de datos, no condicionales repartidos por los "
        "componentes. Una tabla se prueba entera sin montar la escena, se lee de un vistazo, y "
        "un estado olvidado se ve como un hueco; repartida en condicionales, el mismo olvido "
        "solo aparece cuando alguien se queda encerrado en una pantalla durante una prueba con "
        "usuarios.")
    neutro.P(d, "Las %d pantallas de hoy:" % len(D["estados"]), after=4)
    neutro.bullets(d, D["estados"])
    neutro.P(d,
        "LOS MIEMBROS NUEVOS DE LA LISTA DE EVENTOS VAN AL FINAL, SIEMPRE.", bold=True)
    neutro.P(d,
        "Los eventos se guardan en la escena como el número de su posición, y la escena lleva "
        "doce pads con un número dentro. Insertar un evento en medio corre todos los de "
        "después, y entonces cada pad empieza a hacer lo del evento siguiente sin que nada "
        "cambie de aspecto.")
    neutro.P(d,
        "No es hipotético: al añadir un evento en medio, el pad que decía SALIR pasó a "
        "significar «pedir canción» y el que decía MENÚ pasó a «otra vez». Lo atrapó una prueba "
        "de escena, y hay otra que fija los números uno a uno para que se atrape antes.")
    neutro.P(d, "Los %d eventos, en su orden actual:" % len(D["eventos"]), after=4)
    neutro.bullets(d, D["eventos"], num=True)

    neutro.H(d, "7.6 Cambiar los rótulos de los pads", 2)
    neutro.P(d,
        "Qué dice y qué pide cada pad en cada pantalla es otra tabla, por la misma razón: así "
        "se comprueba sin montar la escena que ninguna opción miente. «Mentir» aquí tiene un "
        "caso concreto, ya ocurrido: los pads de la pantalla de resultados seguían diciendo "
        "TUTORIAL, TOCAR y SALIR mientras sus acciones eran OTRA VEZ y MENÚ. El reporte fue "
        "literal: «le di a salir y me salió el de tocar».")
    neutro.P(d,
        "La fila son %d plazas fijas de izquierda a derecha, y una pantalla que usa menos deja "
        "las demás apagadas. Las plazas no se recolocan: el pad que está a la izquierda sigue "
        "estando a la izquierda en todas las pantallas, y lo único que cambia es su rótulo y su "
        "acción. Son objetos en el espacio y el jugador los localiza con el cuerpo, no "
        "leyendo." % D["plazas"])
    filas = D["filas"]
    cuerpo = []
    for estado in D["estados"]:
        if estado not in filas:
            continue
        fila = filas[estado]
        celdas = [fila.get(i, ["—", ""])[0] for i in range(D["plazas"])]
        cuerpo.append([estado] + celdas)
    neutro.table(d, ["Pantalla"] + ["Plaza %d" % (i + 1) for i in range(D["plazas"])],
                 cuerpo, widths=[3.0] + [2.4] * D["plazas"], fs=8)
    neutro.P(d,
        "Las filas del selector no están aquí porque las arma el catálogo de pistas en "
        "ejecución: la primera pantalla ofrece los ritmos y la segunda las velocidades de ese "
        "ritmo, y en las dos la salida al menú va en la última plaza. Si hay más opciones que "
        "plazas sobran las últimas, pero el MENÚ no se pierde nunca: una opción de más que "
        "empujara la salida fuera de la fila abriría una pantalla sin retorno.")

    # ------------------------------------------------------------------ 8
    neutro.H(d, "8. Correr las pruebas", 1)
    neutro.P(d,
        "Hay %d métodos de prueba en %d archivos, más %d parametrizadas que generan un caso "
        "por escena, así que el corredor reporta más pruebas que métodos hay. Son la red que "
        "evita gastar sesiones de visor en defectos de cableado: córrelas antes de compilar."
        % (D["pruebas"], D["archivos"], D["parametrizadas"]))
    bloque(d, "# Unity NO puede estar abierto al mismo tiempo\n"
              "/Applications/Unity/Hub/Editor/%s/Unity.app/Contents/MacOS/Unity \\\n"
              "  -batchmode -runTests -testPlatform EditMode -projectpath \"$PWD\" \\\n"
              "  -testResults /tmp/res.xml -logFile /tmp/tests.log" % D["unity"])
    neutro.P(d,
        "Batchmode sin realidad virtual se lleva de ProjectSettings las referencias de los "
        "recursos precargados de OpenXR. El compilador del proyecto ya lo maneja: las anota "
        "antes, las repone después haya ido bien o mal, y se niega a compilar si al empezar ya "
        "faltaban, porque compilar sin ellas produce un APK que puede no entrar en realidad "
        "virtual y eso no se nota hasta ponerse el visor.", bold=True)
    neutro.P(d,
        "Una corrida de PRUEBAS en batchmode no pasa por el compilador, así que ahí el despojo "
        "sigue ocurriendo sin que nadie lo repare. Si tras correr las pruebas el archivo "
        "aparece modificado, deshazlo con git:")
    bloque(d, "git checkout -- ProjectSettings/ProjectSettings.asset")

    # ------------------------------------------------------------------ 9
    neutro.H(d, "9. Depurar dentro del visor", 1)
    neutro.P(d,
        "El registro normal de Unity no llega al visor. Está verificado contra 293 líneas de "
        "registro del sistema sin una sola entrada de Unity, ni en una compilación de "
        "diagnóstico, y las excepciones comparten ese mismo canal: un fallo en el visor no "
        "deja rastro por ahí.", bold=True)
    neutro.P(d,
        "El canal que sí funciona escribe a un archivo dentro del visor y se recoge con la "
        "misma herramienta que trae las mediciones:")
    bloque(d, "./scripts/quest.sh traza   # por dónde fue el flujo de la aplicación\n"
              "./scripts/quest.sh pull    # baja mediciones y trazas\n"
              "./scripts/quest.sh fps     # baja los volcados de fotogramas y da veredicto")

    # ------------------------------------------------------------------ 10
    neutro.H(d, "10. Tres reglas del código que no se negocian", 1)
    neutro.P(d,
        "Las tres existen por el riesgo dominante del proyecto, que es la latencia entre el "
        "golpe y el sonido. Por encima de 30 milisegundos el golpe deja de sentirse causal.")
    neutro.bullets(d, [
        "El reloj es el del sistema de audio, y se lee una vez por fotograma. Nunca el tiempo "
        "de fotograma: acumula deriva. Y la canción se agenda para un instante futuro del "
        "reloj de audio, nunca se manda reproducir sin más: reproducir y anotar el instante "
        "después deja un desfase constante que no se nota al principio y es evidente al "
        "minuto dos.",

        "Cero reservas de memoria en el camino del golpe. Todo lo que reserve memoria va en la "
        "inicialización. Un tirón del recolector de basura cuesta fotogramas, y un fotograma "
        "es latencia.",

        "El rearme de un pad es por posición, no por tiempo. Semicorcheas a 160 pulsos por "
        "minuto son 94 milisegundos: un rearme por tiempo se come el segundo golpe.",
    ])

    # ------------------------------------------------------------------ 11
    neutro.H(d, "11. Cómo está organizado el proyecto", 1)
    neutro.table(d, ["Carpeta", "Qué hay"], [
        ["Assets/Scripts/Drum", "La batería: pads, detección del golpe, voces y el juicio."],
        ["Assets/Scripts/Flujo", "Las pantallas: la tabla de transiciones, los rótulos de los "
                                 "pads, los paneles y la cortinilla."],
        ["Assets/Scripts/Tutorial", "El tutorial: sus pasos, el conductor, la baqueta que "
                                    "demuestra y el registro de lo que hizo el usuario."],
        ["Assets/Editor", "Los constructores de escena y los comandos del menú. No entran en "
                          "la compilación."],
        ["Assets/Tests", "Las pruebas en modo editor."],
        ["Assets/Audio", "Muestras del kit, música y pistas de práctica."],
        ["Assets/Entorno", "El escenario y su atribución."],
        ["scripts", "quest.sh y las herramientas de línea de comandos."],
        ["Builds", "Donde cae el APK. Ignorado por git."],
    ], widths=[5.0, 10.0], fs=9, negritas_col0=True)
    neutro.P(d,
        "Las carpetas de scripts llevan su propio ensamblado, así que un cambio en el tutorial "
        "no recompila la batería y las dependencias quedan declaradas en vez de ser implícitas.")

    # ------------------------------------------------------------------ 12
    neutro.H(d, "12. Licencias", 1)
    neutro.P(d,
        "Dos regímenes distintos y conviene no confundirlos.")
    neutro.table(d, ["Qué", "Licencia", "Qué permite"], [
        ["Kit de batería AVL Drumkits Red Zeppelin", "CC BY-SA 3.0",
         "Usar y redistribuir citando al autor y manteniendo la licencia. Está en el repositorio."],
        ["Muestras y música de origen libre", "CC0, CC BY 3.0, CC BY 4.0",
         "Usar y redistribuir, citando al autor donde la licencia lo pida. Están en el "
         "repositorio."],
        ["Los dos paquetes de la sección 2", "Standard Unity Asset Store EULA",
         "Usarlos dentro de la aplicación, NO redistribuir los archivos. Por eso no están."],
    ], widths=[5.4, 3.6, 6.0], fs=9, negritas_col0=True)
    neutro.P(d,
        "La atribución de cada recurso vive en el propio repositorio, junto a los archivos, y "
        "también en esta carpeta de entregables. Si se añade un recurso hay que anotarlo ahí: "
        "hay una actividad del proyecto dedicada a mantener ese registro.")

    # ------------------------------------------------------------------ 13
    neutro.H(d, "13. Problemas conocidos", 1)
    neutro.table(d, ["Síntoma", "Causa", "Qué hacer"], [
        ["El bosque no aparece y la escena tiene referencias perdidas",
         "Faltan los dos paquetes del Asset Store",
         "Sección 2. Importarlos y pasar el convertidor a URP."],
        ["Golpeo y no suena, o no se marca la nota",
         "Un consumidor de pads quedó sin cablear",
         "Pasar los cuatro constructores en el orden de la sección 3."],
        ["Un fallo en el visor no deja ningún rastro",
         "El registro normal de Unity no llega al visor",
         "Usar la traza a archivo. Sección 9."],
        ["Tras correr las pruebas, el visor ya no entra en realidad virtual",
         "batchmode sin realidad virtual borra las referencias de OpenXR",
         "Deshacer ProjectSettings/ProjectSettings.asset con git. Sección 8."],
        ["quest.sh dice que no hay conexión y el visor está encendido",
         "El visor se reinició y perdió el modo inalámbrico",
         "Enchufar el cable y repetir quest.sh wifi."],
        ["No puedo repetir el tutorial",
         "Quedó la marca de tutorial visto dentro del visor",
         "./scripts/quest.sh tutorial, o el comando del menú en el editor."],
        ["Un pad hace lo que dice el pad de al lado",
         "Se insertó un evento en medio de la lista",
         "Sección 7.5. Moverlo al final y volver a pasar los constructores."],
        ["La aplicación va a tirones en el visor",
         "Una variante de entorno demasiado cara, o una muestra mal importada",
         "Medir con quest.sh fps y pasar Batería → Ajustar importación de los samples."],
    ], widths=[4.6, 4.6, 5.8], fs=8)

    neutro.H(d, "Dónde está todo lo demás", 1)
    neutro.table(d, ["Qué", "Dónde"], [
        ["Repositorio del prototipo", "github.com/AbiudBenitez/BateriaVR"],
        ["Repositorio de la documentación", "github.com/AbiudBenitez/vr-bateria-terapeutica"],
        ["Referencia rápida para quien ya trabaja en el repo", "BateriaVR/README.md"],
        ["Manual de usuario", "15_Manual_Usuario.docx, en esta misma carpeta"],
        ["Estado del proyecto y decisiones", "12_Estado_del_Proyecto.docx"],
    ], widths=[7.0, 8.0], fs=9, negritas_col0=True)

    return d


def bloque(d, texto):
    """Un bloque de comandos, en monoespaciada y sin justificar."""
    from docx.shared import Pt
    p = d.add_paragraph()
    r = p.add_run(texto)
    r.font.name = "Courier New"
    r.font.size = Pt(9)
    p.alignment = None
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.left_indent = Pt(14)
    return p


if __name__ == "__main__":
    if D is None:
        raise SystemExit("No hay cache de datos. Corre: python3 manual_datos.py --refrescar")
    doc().save(DOC)
    print("OK", DOC)
