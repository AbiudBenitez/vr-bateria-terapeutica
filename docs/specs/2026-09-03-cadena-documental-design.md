# Diseño — Cadena documental completa hasta la ruta crítica

**Fecha:** 3-sep-2026
**Alcance:** carta sponsor, acta constitutiva con EDT, cronograma importable y ruta crítica del proyecto, más el desarrollo completo del ejemplo de clase.

## Problema

Los documentos del proyecto se habían producido en desorden respecto de la metodología. La
carta sponsor describía un proyecto sin enfoque terapéutico, el acta declaraba una ruta
crítica que nadie había calculado, y el cronograma contenía traslapes no documentados. Al
calcular formalmente la ruta crítica aparecieron dos inconsistencias reales.

## Cadena correcta y su fundamento

De `PMI 4.pdf`:

- Diapositiva 5, punto 5: la estructura de desglose del trabajo es la base de toda planificación.
- Diapositiva 7: omitir la descomposición a nivel de actividades no favorece un proyecto exitoso.
- Diapositiva 9: la EDT no tiene ninguna relación de secuencia entre sus componentes.
- Diapositivas 12–14: la secuenciación se hace con diagramación por precedencias (PDM/AON),
  con cuatro tipos de dependencia; la de inicio a fin no se usa.

Orden aplicado: **carta sponsor → acta constitutiva (contiene la EDT) → secuenciación → ruta crítica**.

Matiz metodológico documentado en el acta §4.1: en PMBOK la EDT corresponde formalmente a
los procesos de planificación (5.4 Crear la EDT), no a los de inicio. Se incluye en el acta
porque la plantilla de la docente lo pide y porque sin ella el resto del acta no sería
verificable.

## Decisiones

| Decisión | Alternativa descartada | Razón |
|---|---|---|
| PDM/AON para la ruta crítica del proyecto | AOA, como el ejemplo de aceites | El cronograma tiene traslapes. En AOA solo existe fin→inicio, y modelado así el proyecto da 70 días contra los 53 disponibles. PDM representa los traslapes como inicio→inicio con demora y da 50 días, que sí corresponde al cronograma real. Decisión del usuario tras ver la comparación. |
| AOA para el ejemplo de aceites | PDM | Es la notación de la fuente y el ejemplo requiere actividades ficticias, que no existen en PDM. |
| Rebalancear antes de declarar la ruta crítica | Solo corregir la declaración del acta | El cálculo mostró que la rama 3D era una cadena de 39 días con un solo responsable. Corregir la declaración sin tocar el cronograma habría dejado documentado un cuello de botella evitable. |
| Reasignar 3.3 a UX-XR y adelantar 3.1 a la semana 1 | Contratar apoyo externo de modelado | Sin costo adicional. 3.3 es el paquete de menor complejidad técnica de la rama y UX-XR tenía capacidad libre en las semanas 2 a 4. |
| Formato neutral en los Word | Estilos con encabezados de color | Petición explícita del usuario. |
| Generar todo desde scripts | Editar los Word a mano | Las mismas cifras aparecen en cuatro documentos. Un cambio de duración se propaga solo si los documentos se derivan de un modelo común. |
| Archivar las versiones anteriores en `superados/` | Borrarlas | Reversible, y evita que se entregue la versión equivocada teniendo dos actas en la misma carpeta. |
| La división de tareas del líder no entra en los documentos | Reescribir los roles según sus seis frentes | Petición del usuario. En su lugar, el anexo A del acta lista la asignación nominal por paquete, que permite ver la cobertura sin señalar a nadie. |

## Hallazgos

1. **La ruta crítica declarada en el acta v2.0 no estaba calculada.** Antes del rebalanceo el
   cálculo daba la rama 3 (modelo 3D); después del rebalanceo da la rama 4, que es lo que el
   acta decía. La declaración era correcta por accidente, no por método.

2. **Hay dos rutas críticas, no una.** Convergen en la build candidata:
   `M→N→O→P→Q→R→S→W→X→Y-2→Z` (interacción, UI, pruebas) y `M→N→T→U→V→X→Y-2→Z` (audio, rutinas,
   pruebas). La segunda no estaba declarada en ninguna versión anterior.

3. **La red comprimida son 50 días hábiles contra 70 sin comprimir.** Los 20 días de diferencia
   son traslape deliberado. Sin él el proyecto terminaría 17 días hábiles después del cierre del
   periodo, ya iniciados los exámenes.

4. **15 de 27 actividades quedan sin holgura**, y otras 5 tienen un solo día. Es el costo de la
   compresión y se declara como riesgo R2 del acta, no se presenta como una programación holgada.

5. **La carta sponsor tenía dos defectos aritméticos**: declaraba cuatro meses con un cronograma
   que terminaba el 26 de octubre, y suponía dedicación completa para un equipo de asignación
   parcial. El presupuesto recalculado baja de $460,000 a $384,201 pese a incorporar tres roles
   más y un asesor externo.

6. **La división de tareas del líder deja tres ramas sin responsable**: la 1 (gestión), la 6
   (menús, interfaz, registro de métricas) y la 7 (pruebas y documentación). Las ramas 6 y 7
   están sobre la ruta crítica. No entra en los documentos por decisión del usuario; queda
   registrado en `CLAUDE.md` y en el anexo A del acta.

## Verificaciones realizadas

- La suma de duraciones a lo largo de cada ruta crítica, descontando traslapes, coincide con la
  duración obtenida en el recorrido hacia adelante. Se incluye como sección 11.3 del documento
  de ruta crítica.
- El ejemplo de aceites da 220 días y la suma de su ruta crítica da 220. Reproduce además la
  matriz de elasticidad publicada renglón por renglón, lo que resolvió cuál de los tres cuadros
  contradictorios de la fuente es el correcto.
- El XML del cronograma se valida como XML bien formado: 56 tareas, 9 recursos, 65 asignaciones
  y 48 vínculos.
- Las cifras clave se verificaron por conteo automático en los cuatro documentos.

## Entregables

| Archivo | Contenido |
|---|---|
| `entregables/01_Carta_Sponsor.docx` | Revisión 2 con enfoque terapéutico y presupuesto recalculado. |
| `entregables/02_Acta_Constitutiva.docx` | 42 paquetes con criterio de aceptación, Gantt, simultaneidad, ruta crítica y anexo de asignación nominal. |
| `entregables/superados/Cronograma_MindView_42_paquetes.xml` | MS Project XML con dependencias tipadas. |
| `entregables/superados/Ruta_Critica_42_paquetes_superada.docx` | Desarrollo PDM completo con justificación por sección. |
| `entregables/figuras/` | Red de precedencias y red medida. |
| `tareas-individuales/2026-09-04-ejemplo-ruta-critica/` | Ejemplo de aceites completo con tres figuras y anexo de erratas. |
| `scripts/` | Todo lo anterior es reproducible desde aquí. |

## Fuera de alcance

- Etapas 6, 7 y 8 del método (costos y pendientes, compresión por costo, limitaciones de
  recursos) para el ejemplo de aceites: la fuente no da datos de costo.
- Segundo ciclo del método (ejecución y control) para el proyecto: corresponde al seguimiento
  semanal, no a la documentación de planeación.
