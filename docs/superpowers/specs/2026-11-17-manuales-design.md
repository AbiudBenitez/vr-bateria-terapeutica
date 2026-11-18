# Manual técnico y manual de usuario — diseño

**Fecha:** 17 de noviembre de 2026
**Cierra:** `QM.2` (manual técnico de instalación y ejecución) y `QM.1` (manual básico de usuario)
**Estado:** aprobado

## Por qué

`QM.2` está cerrada desde el 21 de octubre con `BateriaVR/README.md` como evidencia. El README
es correcto y sirve a quien ya conoce el proyecto, pero no cubre **cómo modificar** ni **cómo
desinstalar**, y no es un entregable de la materia. `QM.1` sigue pendiente; el replan del 11 de
noviembre la tenía el 19–20 y se adelanta.

Al revisar el repo apareció un hueco: **`quest.sh` no tiene `uninstall`**. Documentar una
desinstalación que obliga a teclear `adb` a mano es documentar la ausencia de una herramienta.

## Qué se entrega

| Archivo | Cierra | Lector |
|---|---|---|
| `entregables/14_Manual_Tecnico.docx` | `QM.2` | Quien herede el proyecto |
| `entregables/15_Manual_Usuario.docx` | `QM.1` | El participante de `QT.8` |

Los dos en Word editable, formato neutral con `neutro.py`, como los trece anteriores.
`BateriaVR/README.md` queda como referencia rápida y remite al manual técnico.

## Arquitectura

Generados por script, no escritos a mano. Es la convención de los trece entregables
anteriores y aquí pesa más que en ninguno: el manual técnico es el documento con más cifras
que caducan —versión de Unity, identificadores de paquete, 29 comandos de menú, orden de los
constructores, número de pruebas, estados de la aplicación, rótulos de los pads.

```
scripts/manual_datos.py        extrae los hechos del repo Unity
scripts/datos_unity.json       caché commiteada de esos hechos
scripts/capturas.py            manifiesto de capturas e inserción tolerante
scripts/gen_manual_tecnico.py  → entregables/14_Manual_Tecnico.docx
scripts/gen_manual_usuario.py  → entregables/15_Manual_Usuario.docx
scripts/test_manuales.py       las pruebas
```

### Por qué una caché y no leer el repo Unity directo

Los dos repositorios son independientes y el espejo `proyecto-unity/` de esta carpeta quedó en
septiembre: no tiene `Flujo` ni `Tutorial`. Leer el repo real deja los generadores
inservibles para cualquier integrante que no lo tenga clonado en la misma ruta.

La caché resuelve las dos cosas. `manual_datos.py --refrescar` la reescribe desde el repo
Unity —ruta por `BATERIAVR_REPO`, con el valor por omisión documentado—; los generadores leen
solo la caché. Una prueba comprueba que, **cuando el repo está presente**, la caché coincide
con él; cuando no está, esa prueba se salta y las demás siguen valiendo.

Lo que se extrae: versión de Unity, nombre y versión del producto, identificador del paquete,
los `MenuItem` del editor, los diez estados de `EstadoApp`, los miembros de `EstadoApp.Evento`
en orden, la fila de cinco rótulos por estado de `OpcionesDeMenu`, los pasos del tutorial, los
patrones de práctica, el número de pruebas EditMode y los dos paquetes del Asset Store
ausentes.

### Las capturas

El lector del manual de usuario es el participante de `QT.8` y pidió capturas reales, no
diagramas. El visor no está conectado al escribir esto, así que el generador no puede
depender de ellas.

`capturas.py` declara un manifiesto: una entrada por pantalla, con su nombre de archivo y el
pie que lleva. `inserta()` pone la imagen si el archivo existe y, si no, **un recuadro visible
que nombra la pantalla que falta**. Un hueco silencioso en un manual de usuario es peor que un
hueco rotulado: el segundo se arregla, el primero se entrega.

`quest.sh capturas` baja `/sdcard/Oculus/Screenshots/` del visor a
`entregables/capturas/`. El ciclo es: tomar las capturas en el visor, correr `capturas`,
regenerar, y las imágenes aparecen sin tocar el generador.

## Manual técnico — 13 secciones

1. **Qué necesitas.** Quest 3/3S en modo desarrollador, Unity 6000.5.10f1 exacta y por qué no
   otra, Android Build Support, el visor prestado.
2. **Instalar desde cero.** Clonar, los dos paquetes del Asset Store ausentes a propósito
   (`35361` Fantasy Forest, `265300` Low Poly Trees), su licencia, cómo reponerlos.
3. **Reconstruir la escena.** Los comandos del menú `Batería` en tabla, y el orden obligatorio
   de los cuatro constructores con la razón de cada paso.
4. **Compilar.** Desde el editor y en batchmode, dónde cae el APK, por qué no está en el repo.
5. **Instalar en el visor.** Cable la primera vez, modo inalámbrico, `quest.sh install`, y que
   el modo inalámbrico se pierde al reiniciar.
6. **Desinstalar.** `quest.sh uninstall`, la vía desde el visor, y qué queda atrás: las
   mediciones, las trazas y la marca de tutorial visto.
7. **Cómo modificar.** Cambiar el kit, añadir una pista de práctica, cambiar el entorno, mover
   las ventanas de juicio, añadir una pantalla al flujo, cambiar los rótulos de los pads. Lleva
   la trampa del `enum Evento`: los miembros nuevos van al final o los pads empiezan a hacer lo
   del evento siguiente sin cambiar de aspecto.
8. **Pruebas.** Las EditMode, cómo correrlas en batchmode, y el aviso de `ProjectSettings`.
9. **Depurar en el visor.** `Traza`, `quest.sh traza`, y por qué `Debug.Log` no llega.
10. **Las reglas que no se negocian.** `dspTime`, cero asignaciones en el camino del golpe,
    rearme por posición.
11. **Estructura de carpetas** y los ensamblados.
12. **Licencias y atribución** de cada asset, con los dos regímenes distintos.
13. **Problemas conocidos** y qué hacer con cada uno.

## Manual de usuario — 8 secciones

Para el participante de `QT.8`: una acción por paso, sin jerga, sin nombres de archivo.

1. Antes de empezar: ponerse el visor, los controles, el espacio, cuánto dura.
2. Lo primero que verás: la cortinilla y el tutorial, sus cuatro pasos.
3. La fila de cinco pads y qué dice en cada pantalla.
4. Tocar una pista: elegir ritmo, elegir velocidad, los aros, verde / amarillo / rojo.
5. Modo libre.
6. Tus resultados y qué significan los números.
7. Si algo va mal: no suena, no registra el golpe, me marea, no encuentro el pad.
8. Qué se guarda de ti y qué no.

## Cambios en el repo Unity

`scripts/quest.sh` gana dos comandos:

- `uninstall` — desinstala el paquete, **pidiendo confirmación antes de borrar**, y dice qué
  datos quedan en el visor.
- `capturas` — baja las capturas de pantalla del visor a `entregables/capturas/` del repo de
  gestión.

## Pruebas

`scripts/test_manuales.py`:

- Todo comando del menú `Batería` del repo aparece en la tabla del §3.
- El orden de los cuatro constructores coincide con el del `README`.
- Los rótulos de los pads del manual de usuario coinciden con `OpcionesDeMenu`.
- Las pantallas documentadas son exactamente los estados de `EstadoApp`.
- Toda captura del manifiesto existe o queda rotulada como faltante; ninguna se omite en
  silencio.
- Ninguna sección de ninguno de los dos manuales queda vacía.
- Los dos manuales declaran la misma versión de la aplicación.
- La caché coincide con el repo Unity cuando el repo está presente.
- `quest.sh` tiene `uninstall` y `capturas`, y `uninstall` pide confirmación.

## Lo que queda fuera

- **Diagramas generados.** Se eligieron capturas reales. Si no llegan antes del 20, los
  recuadros rotulados dicen cuál falta.
- **Traducción al inglés.** Ninguna medida de éxito la pide.
- **Regenerar el `README` del repo Unity** desde la misma fuente. Es tentador y es otro
  proyecto: el README es markdown para quien ya trabaja en el repo, el manual es Word para
  quien llega.
