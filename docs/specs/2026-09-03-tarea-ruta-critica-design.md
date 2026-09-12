# Diseño — Tarea de ruta crítica y preparación del CPM del proyecto

**Fecha:** 3-sep-2026
**Entregas:** ejercicio de clase 4-sep-2026 · ruta crítica del proyecto 7-sep-2026

## Problema

Dos necesidades con plazos distintos derivadas del mismo documento base
(`El-Método-de-la-Ruta-Crítica.pdf`):

1. Resolver el ejemplo de la página 16 (aceites esenciales de hierbabuena y menta)
   **hasta el arreglo lógico**. Urgente: se entrega mañana.
2. Dejar preparados los insumos para construir la ruta crítica del proyecto de
   batería VR. Se entrega el lunes.

## Restricción encontrada

El documento base tiene inconsistencias internas: la matriz de secuencias, la matriz de
información y la matriz de elasticidad no describen la misma red. No se puede resolver el
ejercicio sin decidir cuál de los tres cuadros es el correcto.

## Decisiones

| Decisión | Alternativa descartada | Razón |
|---|---|---|
| Entregar el ejemplo **corregido** más un anexo de erratas | Reproducir el documento tal cual, con sus errores | La red del documento no cierra: hay actividades sin consecuente. Reproducirla sería entregar algo demostrablemente incorrecto. El anexo convierte el hallazgo en evidencia de análisis. |
| Determinar el cuadro correcto **recalculando el CPM completo** | Elegir por criterio editorial (el cuadro más limpio) | Verificable: la red corregida da 220 días y reproduce la matriz de elasticidad renglón por renglón. Ninguna otra combinación lo hace. |
| Diagrama generado con matplotlib, exportado a PNG | Dibujarlo a mano o describirlo en texto | Reproducible y corregible. Se necesitaron 4 iteraciones para eliminar traslapes de etiquetas en los arcos curvos. |
| Word para el ejercicio, Markdown para los insumos del proyecto | Todo en Word | El ejercicio se entrega impreso a la docente; los insumos son material de trabajo interno que se seguirá editando. |
| Consolidar los 42 paquetes de la EDT en 26 actividades A–Z | Una actividad por paquete | Una red AOA de 42 flechas es ilegible. Se agrupan solo paquetes con mismo responsable y secuencia obligada; se conserva la trazabilidad a la EDT. |
| Calcular la ruta crítica del proyecto con dependencias **lógicas**, no con las fechas del Gantt | Derivar las precedencias de las fechas del cronograma | Las fechas del Gantt incluyen traslape. Derivar precedencias de ellas produciría una red que solo describe el cronograma, no la lógica del proyecto. |

## Hallazgos

1. **Siete erratas en el documento base**, documentadas en el anexo A del Word:
   repetición de E como antecedente, corrimiento de un renglón desde L-2, la clave G-1
   transcrita como «1», corrimiento de dos renglones en la columna de duraciones,
   duración 0 en la actividad C, Q rotulada como O, y numeración de eventos ausente.

2. **La ruta crítica declarada en el acta v2.0 es incorrecta.** El acta señala la rama 4
   (interacción y físicas); el cálculo señala la rama 3 (modelo 3D). La rama 4 tiene
   10 días de holgura total. El cuello de botella real es el Artista 3D.

3. **Brecha de 26 días hábiles** entre la red lógica (79 d) y la ventana del Gantt (53 d),
   atribuible a traslape. Se recomienda reportarla como compresión de la red (etapa 7 del
   método) en lugar de tratarla como error.

## Entregables producidos

| Archivo | Contenido |
|---|---|
| `tareas/2026-09-04-ejemplo-ruta-critica/Ejemplo_Ruta_Critica_Aceites.docx` | 7 secciones + anexo de erratas, 10 tablas, red embebida en página horizontal |
| `tareas/2026-09-04-ejemplo-ruta-critica/Fig8_Arreglo_Logico.png` | Red AOA: 21 eventos, 27 actividades reales, 3 ficticias |
| `docs/investigacion/metodo-ruta-critica-apuntes.md` | El método destilado: 9 etapas, notación, fórmulas de las 4 holguras, criterios de criticidad |
| `docs/investigacion/ruta-critica-bateria-insumos.md` | 26 actividades, matriz de información, matriz de elasticidad calculada, ruta crítica y análisis de la brecha |

## Fuera de alcance

Etapas 6, 7 y 8 del método (costos y pendientes, compresión formal, limitaciones de
recursos) para el ejemplo de clase: la consigna pedía llegar hasta el arreglo lógico.
Para el proyecto, el arreglo lógico queda pendiente de dibujar antes del lunes.
