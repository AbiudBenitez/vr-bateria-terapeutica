# Cómo trabajar con el repositorio

Guía para el Equipo A. No hace falta saber usar git: son cuatro pasos y se hacen desde una
aplicación con botones.

---

## Lo primero: qué se puede editar a la vez y qué no

Esta es la regla que evita que alguien pierda su trabajo.

| Archivo | ¿Varios a la vez? | Por qué |
|---|---|---|
| `Cronograma_ProjectLibre.xml` | **No** | ProjectLibre es una aplicación de escritorio de un solo usuario. Si dos lo abren y guardan, **el último borra el trabajo del primero sin avisar** |
| Documentos de Word | **No** | Mismo problema |
| Hoja de control de tareas | **Sí** | Está en Google Sheets, que sí permite edición simultánea |
| Código de Unity | **Sí**, en archivos distintos | Cada quien trabaja en sus propios archivos |

**El cronograma tiene una sola dueña: Diana.** Es la única que lo abre y lo guarda. El resto
lo abre solo para consultarlo, y **sin guardar cambios**.

Si necesitas que algo cambie en el cronograma, se lo dices a Diana. No lo edites tú aunque
puedas.

---

## Paso 1 — Instalar GitHub Desktop

Es la aplicación con botones. Nadie necesita escribir comandos.

1. Entra a **[desktop.github.com](https://desktop.github.com)** y descarga la versión de tu
   sistema, Windows o Mac.
2. Instálala y ábrela.
3. Inicia sesión con tu cuenta de GitHub. Si no tienes, créala en
   [github.com/signup](https://github.com/signup): es gratis y toma dos minutos.
4. Pásale tu usuario de GitHub a Abiud para que te dé acceso.

---

## Paso 2 — Descargar el proyecto

Solo se hace una vez.

1. En GitHub Desktop: **File → Clone repository**
2. Pestaña **URL**, y pega la dirección del repositorio.
3. Elige dónde guardarlo en tu computadora. El escritorio está bien.
4. Botón **Clone**.

Listo, ya tienes todo el proyecto.

---

## Paso 3 — Antes de trabajar, actualiza

**Esto es lo más importante de toda la guía.** Hazlo siempre, sin excepción.

Abre GitHub Desktop y presiona **Fetch origin** (arriba a la derecha). Si aparece
**Pull origin**, presiónalo también.

Eso trae los cambios que hicieron los demás. Si te saltas este paso y trabajas sobre una
versión vieja, después habrá que resolver conflictos a mano y es tedioso.

> Regla simple: **primero actualizas, luego trabajas.** Nunca al revés.

---

## Paso 4 — Trabaja en tu propia rama

No se escribe directamente en `main`. Cada cambio vive primero en una rama propia, y entra a
`main` solo después de que alguien lo revise.

Suena a trámite, pero resuelve un problema real: **`main` siempre tiene que funcionar**. Si
alguien sube algo a medias, todos lo heredan. En una rama, en cambio, puedes equivocarte sin
afectar a nadie.

1. En GitHub Desktop, arriba dice **Current branch**. Presiónalo y luego **New branch**.
2. Ponle un nombre que diga qué vas a hacer: `tutorial-intensidad`, `beatmap-cancion-1`.
3. **Create branch**.
4. Trabaja normal: abre tus archivos, haz tus cambios, guarda.
5. Vuelve a GitHub Desktop, escribe en **Summary** qué hiciste y presiona
   **Commit to [nombre-de-tu-rama]**. Fíjate que no diga `main`.
6. Presiona **Publish branch**.
7. Aparecerá un botón azul **Create Pull Request**. Presiónalo.

## Paso 5 — Que alguien lo revise

1. Avisa en el grupo que subiste un pull request.
2. Quien revise entra a la pestaña **Pull requests**, abre el tuyo y va a **Files changed**
   para ver exactamente qué cambiaste.
3. Si está bien: **Review changes → Approve → Submit review**.
4. Ya aprobado: **Merge pull request** y luego **Delete branch**.

**Nadie aprueba su propio trabajo.** Es la misma regla de revisión por pares que declaramos en
el plan de calidad.

> **¿Nunca has hecho esto?** El archivo [`FIRMAS.md`](FIRMAS.md) es un ejercicio para
> practicarlo sin riesgo: cada quien firma en su sección siguiendo el flujo completo.
> Empieza por ahí.

---

## Cinco reglas y ya

1. **Actualiza antes de trabajar.** *Fetch origin* siempre.
2. **Trabaja en tu rama, no en `main`.**
3. **Sube el mismo día.** No acumules una semana de trabajo sin subir: si tu computadora
   falla, se pierde todo, y además nadie sabe cómo vas.
4. **El cronograma lo toca Diana.** Los demás solo consultan.
5. **Si algo se ve raro, no lo arregles a la fuerza.** Avisa en el grupo. Un conflicto mal
   resuelto borra trabajo de otro.

---

## Preguntas que van a salir

**¿Y si trabajo en el mismo archivo que otro?**
Mientras sean archivos distintos, no hay problema: git los combina solo. El conflicto ocurre
cuando dos editan **el mismo archivo** antes de actualizar. Por eso la regla 1.

**¿Puedo editar el cronograma aunque Diana no esté?**
No. ProjectLibre no avisa ni bloquea el archivo: simplemente el último en guardar borra al
anterior y nadie se entera hasta que falta algo.

**Me sale «conflicto» y no sé qué hacer.**
No presiones nada. Toma captura y mándala al grupo. Se resuelve en un minuto entre dos, y es
mucho más rápido que deshacer un conflicto mal resuelto.

**¿Cómo abro el cronograma?**
Instala ProjectLibre desde [projectlibre.com](https://projectlibre.com). Luego
*Archivo → Abrir*, elige tipo **XML**, y abre `entregables/Cronograma_ProjectLibre.xml`.

> **En Mac con chip M1 o posterior:** si ProjectLibre no abre al dar doble clic, abre la
> Terminal y ejecuta estos dos comandos. Es un problema conocido de una librería que falta:
> ```bash
> brew install harfbuzz
> brew install --cask projectlibre
> ```
> El detalle está en `docs/investigacion/alternativas-software-gestion-proyectos.md`.

**¿Dónde reporto mi avance?**
En la hoja de control de tareas, en Google Sheets. Esa sí la editan todos a la vez.

**¿Por qué los documentos de Word no se editan a mano?**
Porque se generan con scripts. Las mismas cifras aparecen en varios documentos, y editar uno
a mano las desincroniza. Si detectas un error en un documento, avisa en el grupo en vez de
corregirlo directamente.

---

## Si prefieres no instalar nada

Puedes ver y descargar todo desde el navegador, entrando al repositorio en github.com. Sirve
para consultar, pero para subir tu trabajo necesitas GitHub Desktop.
