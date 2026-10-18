# Diseño — Métricas de sesión

**Fecha:** 18 de octubre de 2026 · **Estado:** aprobado, pendiente de plan
**Cubre:** `DM.1`, la única actividad que el recorte de alcance añadió
**Cierra:** medida de éxito 9 de la carta del patrocinador

---

## 1. Qué se resuelve

La medida 9 pide que el sistema exporte métricas por sesión. Hoy está en cero: el marcador
del juego de ritmo calcula el desfase de cada golpe y lo descarta en cuanto lo pinta en
pantalla.

Guardar esos desfases es barato y de ellos salen las dos métricas que la medida necesita. Es
la razón por la que el recorte añadió esta actividad mientras cortaba otras cien: una
actividad de trabajo convierte una medida fallida en cumplida.

## 2. Qué NO se mide, y por qué

La medida 9 nombraba tres cosas: precisión temporal, **amplitud de movimiento** y constancia
del pulso.

La amplitud de movimiento queda fuera. El equipo decidió antes del corte de medio curso
**retirar el marco de rehabilitación motriz** y quedarse con el emocional: la parte clínica no
tenía fundamento sostenible sin asesor externo ni validación, y afirmarla habría sido peor que
no afirmarla. La amplitud de movimiento es un dato de rehabilitación de miembro superior, y
sin ese marco mide algo que el proyecto ya no declara.

Las dos métricas restantes **no necesitan respaldo clínico**: medir si alguien toca a tiempo y
con regularidad es una observación de ejecución musical, verificable por sí misma.

## 3. Arquitectura

| Pieza | Responsabilidad | Probable sin hardware |
|---|---|---|
| `SessionStats` | Clase pura: lista de desfases → estadísticas | Sí |
| `Scoreboard` | Acumula los desfases y vuelca el JSON | En play |

El marcador ya calcula cada desfase. Solo hay que guardarlo en un arreglo **reservado en
`Awake`**: cero asignaciones en el camino del golpe, como el resto del proyecto. Si se
desborda, se deja de registrar en lugar de realocar — perder una muestra de diagnóstico es
preferible a un tirón del recolector de basura en mitad de la canción.

## 4. Dos constancias, no una

«Constancia del pulso» admite dos lecturas que responden preguntas distintas:

| Lectura | Qué mide |
|---|---|
| **Contra la rejilla** | Desviación típica de los desfases: qué tan parejo se pega el usuario al patrón |
| **Propia** | Desviación típica de los intervalos entre golpes consecutivos: qué tan estable es su pulso interno |

La segunda es la que un músico llamaría constancia. **Se puede ir treinta milisegundos atrasado
todo el tiempo y tener un pulso perfectamente estable**; la primera lectura lo castigaría y la
segunda no.

Se calculan las dos. Salen de los mismos datos y cuestan lo mismo, y juntas dicen algo que
ninguna dice sola: constancia propia baja con desviación contra la rejilla alta significa buen
pulso y mal anclaje al patrón, que es un diagnóstico útil y accionable.

## 5. El archivo

```json
{
  "sesion": "2026-10-18T14:32:10",
  "bpm": 120.0,
  "notas": { "total": 64, "perfect": 41, "good": 15, "miss": 8 },
  "aciertos": 56,
  "precisionPorcentaje": 87.5,
  "precisionTemporal": {
    "mediaMs": 3.2, "medianaMs": 2.8, "p90Ms": 18.4,
    "desviacionMs": 11.7, "minMs": -22.1, "maxMs": 24.9
  },
  "constanciaPulsoMs": 9.3,
  "desfases": [2.1, -4.8, 11.2]
}
```

**Se guardan los desfases crudos además del resumen.** Un informe que solo lleva promedios no
se puede reanalizar: con los datos en bruto se pueden hacer gráficas, recalcular si cambia el
criterio, o revisar una sesión que dio un número extraño.

El volcado sigue el patrón de `LatencyProbe`: `Application.persistentDataPath`, nombre con
marca de tiempo, y la misma guarda contra el volcado doble —`OnApplicationPause(true)` y
`OnApplicationQuit` se disparan ambos al cerrar y producían pares de archivos idénticos.

## 6. Casos borde

| Caso | Comportamiento |
|---|---|
| Sesión sin ningún golpe | Se vuelca con ceros y lista vacía. No revienta |
| Un solo golpe | Hay precisión temporal, no hay constancia de pulso: un intervalo necesita dos golpes |
| Se desborda la capacidad | Se deja de registrar. No se realoca en el camino del golpe |
| Desfases todos iguales | Desviación cero. Es el caso perfecto, no un error |

## 7. Pruebas

Sobre `SessionStats`, en EditMode sin audio ni escena:

1. Con desfases conocidos, media, mediana y p90 salen exactas.
2. La desviación típica de valores idénticos es cero.
3. Una lista vacía devuelve ceros sin lanzar excepción.
4. Un solo golpe no produce constancia de pulso.
5. **La constancia de pulso ignora el desfase constante**: una serie treinta milisegundos
   atrasada pero perfectamente regular da constancia alta y desviación contra rejilla alta.

La quinta es la que verifica que las dos métricas de la §4 miden de verdad cosas distintas. Sin
ella, nada impide que alguien las implemente iguales y nadie lo note.

## 8. Fuera de alcance

La amplitud de movimiento, por la razón de la §2.

La visualización de las métricas dentro del visor: la pantalla de resultados es `II.6`, del
área de interfaz. Este diseño produce el archivo; mostrarlo es otro trabajo.

El análisis de los archivos exportados. Forma parte del informe final (`QI.1`), del área de QA.
