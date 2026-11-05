# Un documento por área de conocimiento del PMBOK — diseño

**Fecha:** 4 de noviembre de 2026 · **Cierre del proyecto:** 13 de noviembre · 7 días hábiles

## Qué se construye

Nueve documentos en `entregables/pmbok/`, uno por área de conocimiento del PMBOK 6.ª
edición, salvo cronograma:

```
04_Integracion_Acta.docx   07_Costos.docx     09_Recursos.docx       11_Riesgos.docx
05_Alcance.docx            08_Calidad.docx    10_Comunicaciones.docx 12_Adquisiciones.docx
                                                                     13_Interesados.docx
```

**El área 6, cronograma, se omite** porque ya está cubierta por
`entregables/Cronograma_ProjectLibre.xml`, `Cronograma_Operativo.xml`,
`03_Ruta_Critica.docx` y `Ruta_Critica_257_Tareas_v3.docx`.

**No hay documento índice.** Se evaluó un `00_Indice_PMBOK.docx` con la matriz de los 49
procesos y el equipo decidió quedarse solo con los nueve.

## El punto de partida: tres niveles de trabajo muy distintos

| Área | Qué existía al 4-nov | Trabajo |
|---|---|---|
| 4 Integración | `02_Acta_Constitutiva` (8 611 palabras), `11_Cambio_de_Enfoque` es el 4.6 | reorganizar |
| 5 Alcance | disperso: §2.3, §2.4 y la EDT del acta, `10_Recorte`, `07_Carta_Validacion` | consolidar |
| 7 Costos | `05_Analisis` completo (7.1–7.4) y Parte I del `04` | reorganizar |
| 8 Calidad | Partes II y III del `04`, con catálogo de pruebas | reorganizar |
| 9 Recursos | disperso: §3.2, §3.3 y §4.9 del acta | consolidar |
| 10 Comunicaciones | nada | nuevo |
| 11 Riesgos | Parte IV del `04`: 18 riesgos con respuesta, `09_R14` | reorganizar |
| 12 Adquisiciones | solo la frase «el proyecto no realiza compras» | nuevo |
| 13 Interesados | §3.1 del acta, mínimo | consolidar |

## Decisión 1 — autocontenidos, generados por script

Cada documento de área **se sostiene solo**: quien abra únicamente esa carpeta tiene el área
completa. La alternativa —documentos cortos que remiten a los existentes, como hace el
documento 12— se descartó porque un lector que abra la carpeta vería nueve documentos casi
vacíos, y el entregable pedido es un documento por área, no un índice de nueve entradas.

**Autocontenido NO significa copiado a mano.** Las áreas con desarrollo profundo se generan
desde los mismos módulos de python que produjeron el 04 y el 05:

| Módulo de área | Importa | Para no divergir en |
|---|---|---|
| `a04.py` | `enfoque.py` | el cambio de encuadre terapéutico |
| `a05.py` | `recorte.py` | las 155 vigentes, las 102 recortadas, la medida 8 retirada |
| `a07.py` | `costos.py` | la tarifa de 1 SM, el presupuesto de $104 013 |
| `a08.py` | `pruebas.py` | el catálogo de casos de caja blanca y negra |
| `a11.py` | `r14.py` | el registro de riesgos y la respuesta ejecutada |

Esto no es elegancia: **es la lección de esta semana.** Los dos cronogramas declararon
avances distintos —59 % y 83 %— durante dos semanas porque cada uno se marcaba a mano. Una
cifra que vive en dos sitios acaba diciendo dos cosas.

## Decisión 2 — adquisiciones: no aplica, pero razonado y con evidencia

El proyecto no compra nada: visores prestados por la Facultad, Unity gratuito, assets de
licencia libre y dos paquetes del Asset Store ya poseídos.

El documento **no inventa un plan de contratación** ni **infla las licencias a categoría de
contrato**. Documenta:

- **12.1** El análisis de hacer-o-comprar que sí se hizo, con cada decisión y su razón:
  Unity contra Unreal, controles contra *hand tracking*, sin backend, integrar assets libres
  en vez de modelar, y el Audio Mixer descartado por no remedir la latencia.
- **12.2** No se efectuó ninguna adquisición. Los acuerdos que existen son de **licencia y
  préstamo**, enumerados con su régimen: CC0, CC BY 3.0, CC BY-SA 3.0, CC BY 4.0 y Standard
  Unity Asset Store EULA, más el préstamo de los visores.
- **12.3** La verificación de cada licencia en su origen y la restricción que impone cada
  una — incluido que dos paquetes **no pueden ir al repositorio** porque su EULA permite
  usarlos pero no redistribuirlos.

Un «no aplica» con evidencia vale más que un plan de contratación que nunca existió.

## Decisión 3 — comunicaciones: solo lo verificable, y el hueco declarado

Es la única área sin ningún dato en el repositorio. Se documentan los **seis canales que
dejan rastro** —git, el cronograma como plan único, la hoja de control del equipo, los doce
documentos como canal formal con la patrocinadora, la Traza para los fallos en el visor, y la
revisión semanal en clase— con qué deja cada uno y quién lo mantiene.

Y se **declara explícitamente** que la comunicación interna fue informal y sin cadencia fija.
La evidencia de que eso costó algo es medible: la hoja de control del equipo quedó
desincronizada del cronograma en **74 actividades**. No es un defecto de herramienta, es uno
de comunicación, y es lo que el riesgo R15 describía.

**No se escribe un plan normativo** con cadencia de reuniones y matriz de escalamiento: a
siete días del cierre describiría prácticas que el equipo no tuvo y que ya no puede empezar
a cumplir.

## Arquitectura

```
scripts/pmbok_areas/__init__.py
scripts/pmbok_areas/a04.py … a13.py    datos de cada área (nueve módulos)
scripts/gen_pmbok.py                   el único renderizador
scripts/test_pmbok_areas.py            pruebas
```

**Un solo renderizador** para que la carpeta se lea como un conjunto y no como nueve
documentos sueltos. Cada `aNN.py` exporta la misma forma:

| Campo | Contenido |
|---|---|
| `AREA` | `("7", "Gestión de los Costos del Proyecto")`, **leído de `pmbok.py`**, no reteclado |
| `RESUMEN` | un párrafo: qué decidió el proyecto en esta área |
| `PROCESOS` | por cada proceso del área: `(numero, que_hizo, evidencia)` |
| `TABLAS` | `(titulo, encabezados, filas)`, construidas desde los módulos existentes |
| `LECCIONES` | qué salió mal y qué enseñó |
| `REMITE_A` | qué documento lleva el detalle de nivel anexo |

El número, el nombre y el grupo de proceso salen de `scripts/pmbok.py`, que ya tiene las 10
áreas y los 49 procesos de la 6.ª edición con `de_area()` y `matriz()`. Ningún módulo de área
vuelve a escribir el nombre de un proceso.

## Datos nuevos, y de dónde salen

| Área | Fuente verificable |
|---|---|
| 9 Recursos | los 14 recursos del `Cronograma_Operativo.xml` con su tarifa. **Diana figura como seis recursos distintos** —directora, gerente, QA, analista, redactora y desarrolladora VR—: es la concentración que R3 y R14 produjeron, visible en el propio archivo |
| 10 Comunicaciones | los seis canales con rastro, y el desfase de 74 actividades |
| 12 Adquisiciones | `ATRIBUCION_entorno.txt`, `ATRIBUCION_musica.txt` y el `.gitignore` del repo Unity, que documenta qué EULA impide redistribuir |
| 13 Interesados | §3.1 del acta, más el asesor terapéutico que nunca se concretó y la medida 8 que se retiró por eso |

## Pruebas

Convención del proyecto: todo script lleva las suyas.

1. **Cobertura exacta.** Cada área cubre exactamente los procesos que `pmbok.py` lista para
   ella: ninguno de menos, ninguno inventado.
2. **Nada sin evidencia.** Cada proceso dice qué hizo el proyecto y con qué se demuestra.
3. **Las cifras coinciden con su fuente viva.** Presupuesto contra `costos.py`, avance contra
   el cronograma, medida retirada contra `recorte.py`.
4. **Cada `REMITE_A` nombra un archivo que existe.**
5. **Las nueve áreas son las diez menos cronograma**, y la ausencia del 06 queda declarada
   dentro del documento de integración.

## Lo que este trabajo NO hace

- No inventa cadencia de reuniones ni prácticas que el equipo no tuvo.
- No toca los doce documentos existentes: siguen siendo los vigentes.
- No regenera el `07` ni el `08`, que están fechados el 21 de septiembre y llevan firma.
- No añade el área 6 ni un documento índice.

## Orden de ejecución

Primero las cinco que no existen —comunicaciones, adquisiciones, interesados, recursos,
alcance—, después las cuatro que reutilizan material ya escrito. Si el tiempo aprieta, el
hueco cerrado es mayor.
