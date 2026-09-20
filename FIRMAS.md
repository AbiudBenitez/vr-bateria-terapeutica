# Firmas del Equipo A

Este archivo tiene dos propósitos. El primero es dejar constancia de quién participó en el
proyecto. El segundo, y el más importante, es que cada quien practique el flujo de trabajo
real con el que se colabora en software: **rama → cambio → pull request → revisión → merge**.

Es un ejercicio de bajo riesgo. Lo peor que puede pasar es que haya que borrar una rama.

---

## Qué tienes que hacer

Buscar tu sección más abajo y reemplazar las tres líneas que dicen `pendiente` por tus datos.
Nada más. **No toques la sección de nadie más**, y así git combina todo sin conflictos.

---

## El flujo, paso a paso

Hay dos formas de hacerlo. Elige la que te acomode: el resultado es idéntico.

### Opción A — Desde la página de GitHub, sin instalar nada

Es la más rápida para este ejercicio.

1. Entra al repositorio y abre el archivo `FIRMAS.md`.
2. Presiona el **lápiz** (Edit this file), arriba a la derecha.
3. Busca tu sección y llena tus datos.
4. Baja hasta el final. Verás dos opciones: elige **«Create a new branch for this commit
   and start a pull request»**.
5. En el nombre de la rama escribe `firma/tu-nombre`. Por ejemplo: `firma/kimberly`.
6. Presiona **Propose changes**.
7. En la pantalla siguiente presiona **Create pull request**.

Listo. Ya hiciste una rama y un pull request.

### Opción B — Desde GitHub Desktop

Si ya lo instalaste y quieres ver cómo se siente el flujo completo.

1. **Fetch origin**, para partir de la versión más reciente.
2. Arriba, donde dice **Current branch**, presiona y luego **New branch**.
3. Nómbrala `firma/tu-nombre` y presiona **Create branch**.
4. Abre `FIRMAS.md` en cualquier editor de texto, llena tu sección y guarda.
5. Vuelve a GitHub Desktop. Escribe en **Summary**: `Firma de [tu nombre]`.
6. **Commit to firma/tu-nombre** ← fíjate que dice el nombre de tu rama, no `main`.
7. **Publish branch**.
8. Aparecerá un botón azul: **Create Pull Request**. Presiónalo.

---

## Qué pasa después

1. **Alguien revisa tu pull request.** Entra a la pestaña *Pull requests* del repositorio, abre
   el tuyo, va a *Files changed* y ve exactamente qué cambiaste.
2. Si está bien, presiona **Review changes → Approve → Submit review**.
3. Ya aprobado, se presiona **Merge pull request**. Tu cambio pasa a `main`.
4. **Delete branch**, que aparece después del merge. La rama ya cumplió su función.

**Revísense entre ustedes, no se aprueben a sí mismos.** Esa es la idea del ejercicio: que
otra persona vea el cambio antes de que entre. Sugerencia de parejas para que nadie se quede
esperando:

| Quien firma | Quien revisa |
|---|---|
| Misael | Benjamín |
| Benjamín | Misael |
| María | Javier |
| Javier | María |
| Christian | Sarai |
| Sarai | Christian |
| Kimberly | Diana |
| Diana | Kimberly |

---

## Por qué se trabaja así

Podrían escribir directamente en `main` y sería más rápido. Se usa este flujo por tres razones
concretas:

- **`main` siempre funciona.** Lo que está ahí es la versión buena. Los experimentos viven en
  ramas, y si algo sale mal se borra la rama sin afectar a nadie.
- **Alguien más ve el cambio antes de que entre.** Es el mismo principio de la revisión por
  pares que ya declaramos en el plan de calidad: nadie acepta su propio trabajo.
- **Queda registro de quién cambió qué y por qué.** Dentro de dos meses, cuando haya que
  explicar una decisión, el historial lo dice.

---

# Firmas

> Cada quien llena **solo su sección**. Reemplaza lo que dice `pendiente`.

---

### Abiud Misael Benítez Franco

- **Área:** Desarrollo VR y batería base
- **Usuario de GitHub:** pendiente
- **Fecha:** pendiente
- **Con qué contribuyo al proyecto:** pendiente

---

### Benjamín Ignacio Villalón Bobadilla

- **Área:** Juego de ritmo y sistemas
- **Usuario de GitHub:** pendiente
- **Fecha:** pendiente
- **Con qué contribuyo al proyecto:** pendiente

---

### Christian Salvador Valadez Gallegos

- **Área:** Sonido y audio
- **Usuario de GitHub:** pendiente
- **Fecha:** pendiente
- **Con qué contribuyo al proyecto:** pendiente

---

### Diana Laura Tello Salinas

- **Área:** Aseguramiento de calidad, documentación y gestión
- **Usuario de GitHub:** pendiente
- **Fecha:** pendiente
- **Con qué contribuyo al proyecto:** DOCUMENTACION

---

### Javier Alejandro Hernández Caloca

- **Área:** Música y diseño rítmico
- **Usuario de GitHub:** pendiente
- **Fecha:** pendiente
- **Con qué contribuyo al proyecto:** pendiente

---

### Kimberly González Sepúlveda

- **Área:** Entorno 3D, assets y ambientación
- **Usuario de GitHub:** pendiente
- **Fecha:** pendiente
- **Con qué contribuyo al proyecto:** pendiente

---

### María Fernanda Montoya Valdez

- **Área:** Investigación y experiencia emocional
- **Usuario de GitHub:** pendiente
- **Fecha:** pendiente
- **Con qué contribuyo al proyecto:** firma/Fernanda

---

### Sarai Galindo García

- **Área:** Interfaz, UX/UI y tutorial
- **Usuario de GitHub:** saragdot
- **Fecha:** pendiente
- **Con qué contribuyo al proyecto:** pendiente

---

## Si algo sale mal

**«Dice que hay un conflicto».** Pasa cuando dos personas tocaron las mismas líneas. Como cada
quien tiene su propia sección, no debería ocurrir. Si ocurre, no presiones nada: manda captura
al grupo.

**«Me equivoqué en el nombre de la rama».** No importa. Borra la rama y empieza de nuevo, o
déjala: el nombre no afecta nada.

**«Hice commit en `main` sin querer».** Avisa antes de subirlo. Se corrige en un minuto.

**«Ya hice el pull request pero quiero cambiar algo».** Haz otro commit en la misma rama. El
pull request se actualiza solo.
