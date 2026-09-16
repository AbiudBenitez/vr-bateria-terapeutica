# Diseño — Visual del pad fiel a su hitbox

**Fecha:** 16 de septiembre de 2026 · **Estado:** aprobado, en implementación
**Proyecto Unity:** `/Users/abiudbenitez/Documents/code/Unity/BateriaVR`

---

## 1. Problema

El cilindro que representa el pad mentía de dos formas independientes, y las dos hacían difícil
apuntar — lo que a su vez complica la medición de latencia del capítulo 5.

| | Visual antes | Hitbox real |
|---|---|---|
| Radio | 0.50 m | **0.15 m** (3.3× más chico) |
| Plano de golpe | aparentaba estar en la cara superior | está en el **centro** del cilindro |

**La causa del segundo error.** Un cilindro primitivo de Unity mide 2 unidades de alto y está
centrado en su origen. Con `scale.y = 0.15` mide 0.30 m y sobresale ±0.15 m respecto al plano.
El usuario apunta a la cara que ve, que está **15 cm por encima** del plano donde de verdad se
dispara el golpe.

## 2. Objetivo

Que lo que se ve sea lo que golpea, con error por debajo del centímetro, y que **no pueda volver
a desincronizarse** cuando se cambien `radius` o `armDistance` — cosa que el capítulo 6 obliga a
hacer, porque la calibración barre `armDistance`.

Objetivo secundario: que parezca un tambor y no un disco gris, para que la escena sea legible.

## 3. Decisión de arquitectura

Se evaluaron tres caminos:

| | Camino | Veredicto |
|---|---|---|
| 1 | Escalas fijas puestas a mano | Descartado: vuelve a mentir al primer cambio de `radius`, y el cap 6 cambia `armDistance` |
| 2 | **Componente que deriva el visual del `DrumPad` en tiempo de edición** | **Elegido** |
| 3 | Generar la malla por código en `Awake` | Descartado: no se ve nada en el editor sin entrar en play, y asigna en el arranque |

`PadVisual` es `[ExecuteAlways]`: lee `radius` y `armDistance` del `DrumPad` del mismo GameObject
y escala y posiciona sus hijos. Cambiar el radio en el inspector reajusta el visual **sin darle
play**. La fidelidad deja de depender de que alguien se acuerde.

## 4. Estructura

Todo cuelga de `Pad`, de modo que visual y lógica no pueden separarse.

```
Pad  ·  DrumPad(radius, armDistance)  ·  PadVisual
│
├── PlanoArmado   disco translúcido    y = +armDistance   ← donde dispara el audio
├── Aro           cilindro metálico    y =  0            ← marca del plano
├── Piel          cilindro claro       y =  0            ← EL PLANO DE GOLPE
└── Casco         cilindro oscuro      y = −0.065        ← cuelga hacia abajo
```

Un cilindro primitivo mide diámetro 1 y alto 2, así que para diámetro `D` y alto `H` la escala es
`(D, H/2, D)`.

| Hijo | Diámetro | Alto | Centro en y |
|---|---|---|---|
| Piel | `2·radius` | 0.010 | 0 |
| Aro | `2·radius + 0.020` | 0.008 | 0 |
| Casco | `2·radius − 0.010` | 0.120 | −0.065 |
| PlanoArmado | `2·radius + 0.045` | 0.004 | `armDistance` |

### Las tres decisiones que importan

- **La piel mide 10 mm y está centrada en el plano.** Error máximo entre lo que se ve y donde
  golpea: **5 mm**, contra los 150 mm anteriores.
- **El casco cuelga hacia abajo.** Da lectura de tambor sin que ningún volumen quede por encima
  del plano confundiendo al apuntar.
- **El aro es más delgado que la piel** (8 mm contra 10 mm) aunque ambos estén centrados en `y=0`.
  Si fuera más grueso, su cara superior taparía la piel y solo se vería el aro. Al ser más
  delgado, la piel queda visible y el aro la rodea.

## 5. Materiales

Cuatro nuevos en `Assets/Materials/`. **Hay que crearlos, no editar el existente:** hoy Floor,
Baqueta y pad comparten el `Lit.mat` interno del paquete URP
(`Library/PackageCache/com.unity.render-pipelines.universal@.../Runtime/Materials/Lit.mat`), que
es de solo lectura. Por eso se ve todo del mismo gris.

Shader de este proyecto: `Universal Render Pipeline/Lit`, guid `8d2bb70cbf9db8d4da26e15b26e74248`.

| Material | Color | Notas |
|---|---|---|
| `Pad_Piel` | crema | `_Smoothness` 0.25, mate como un parche |
| `Pad_Casco` | rojo oscuro | `_Smoothness` 0.35 |
| `Pad_Aro` | gris metálico | `_Metallic` 0.9, `_Smoothness` 0.7 |
| `Pad_PlanoArmado` | cian, alpha 0.22 | `_Surface: 1`, `_SrcBlend: 5`, `_DstBlend: 10`, `_ZWrite: 0`, cola 3000 |

Se generan con `AssetDatabase.CreateAsset` desde un script de editor, no escribiendo YAML a mano:
así el shader y las keywords los resuelve Unity y no quedan a merced de un formato que cambia
entre versiones.

## 6. Construcción

`Assets/Editor/PadVisualBuilder.cs` añade el menú **`Batería → Reconstruir visual del pad`**, que
sobre la escena abierta:

1. Localiza el `DrumPad`.
2. Borra los hijos previos llamados `Piel`, `Casco`, `Aro`, `PlanoArmado` — es idempotente.
3. Crea los cuatro primitivos, **les quita el collider** que Unity añade por defecto.
4. Crea o reutiliza los cuatro materiales y los asigna.
5. Añade `PadVisual` al pad si falta, y lo sincroniza.
6. Borra el `DrumPadR` viejo, que es el cilindro de 1 m que mentía.
7. Deja `Tip` en escala `(1,1,1)`.
8. Marca la escena como modificada.

Se eligió un menú de editor en vez de editar el YAML de la escena a mano porque la API de Unity
produce objetos válidos por construcción, y un error en el YAML de una escena es caro de
diagnosticar.

### Por qué `Tip` se normaliza

Hoy tiene `scale (36.6, 10.1, 17.3)`. Es un `Transform` vacío y solo se lee su **posición**, así
que no afecta al cálculo del golpe. Pero es una trampa esperando: si alguien le cuelga geometría,
aparecerá deformada sin motivo aparente.

## 7. Cambio en código existente

`DrumPad` expone `ArmDistance`, `MinVelocity`, `Normal` y `Center`, pero **no** el radio.
`WithinRadius()` responde una pregunta distinta y no sirve. Se añade:

```csharp
public float Radius => radius;
```

## 8. Pruebas

Tres EditMode nuevas, sobre la escena real `Cap04_Pad.unity` — no sobre objetos construidos en
memoria, porque el invariante que importa es que **el artefacto que se va a medir** sea fiel:

1. El diámetro de la piel es exactamente `2 · radius`, con 1 mm de tolerancia.
2. La piel está centrada en el plano del pad, con 1 mm de tolerancia.
3. El plano armado está exactamente a `armDistance` sobre el pad, con 1 mm de tolerancia.

Corren sin visor. Fallan hasta que se ejecute el menú de reconstrucción, que es el orden correcto:
la prueba falla primero y pasa cuando el arreglo está puesto.

## 9. Fuera de alcance

Texturas, logotipos, sombras propias, más piezas de la batería, y cualquier cambio en la detección
del golpe. Esto es fidelidad visual y legibilidad; la física no se toca.
