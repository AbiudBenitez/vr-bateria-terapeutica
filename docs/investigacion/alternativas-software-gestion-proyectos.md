# Alternativas a MindView para la gestión del proyecto

**Fecha:** 11-sep-2026
**Problema:** la licencia de prueba de MindView es de 30 días y el semestre dura hasta el 13 de noviembre.
**Restricción adicional:** ProjectLibre no abre en una Mac con chip ARM.

---

## 1. Lo primero: ProjectLibre sí se puede arreglar

Antes de migrar a otra herramienta, conviene descartar el problema real, porque **ProjectLibre
cubre todo lo que necesitamos y es gratis**. No abre por una razón concreta y documentada, y
tiene solución.

### Qué está fallando

ProjectLibre es una aplicación Java. En Mac con Apple Silicon, el gestor de fuentes de Java no
encuentra una biblioteca del sistema y la aplicación muere en silencio: el icono aparece en
Aplicaciones, se hace doble clic y no pasa nada, sin mensaje de error.

El error real es:

```
Library not loaded: /opt/homebrew/opt/harfbuzz/lib/libharfbuzz.0.dylib
```

`harfbuzz` es una biblioteca de composición tipográfica. El tiempo de ejecución de Java que
ProjectLibre trae embebido la espera en la ruta de Homebrew, y si Homebrew no está instalado,
no existe.

### Diagnóstico: ver el error en vez de adivinar

Ejecutarlo desde la Terminal en lugar de dar doble clic. Así el error se imprime:

```bash
/Applications/ProjectLibre.app/Contents/MacOS/ProjectLibre
```

### Solución

```bash
# 1. Instalar Homebrew, si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar la biblioteca que falta
brew install harfbuzz

# 3. Reinstalar ProjectLibre desde Homebrew
brew install --cask projectlibre
```

Después, abrir con Spotlight normalmente.

### Si aún así no abre

| Síntoma | Causa | Qué hacer |
|---|---|---|
| «Bad CPU type in executable» | Binario para Intel en Mac ARM | Descargar la versión para Apple Silicon. La 1.9.8 de macOS **solo** existe para Apple Silicon; si bajaste un instalador viejo, es de Intel |
| Falla al arrancar mencionando `SecurityManager` | Java 24 o superior; ProjectLibre 1.9.8 se compiló contra Java 21 | Instalar Java 21: `brew install openjdk@21` |
| macOS lo bloquea por no venir de la App Store | Cuarentena de Gatekeeper | En Sonoma y posteriores el permiso desde Ajustes ya no basta. Instalarlo por Homebrew evita la cuarentena |
| Nada de lo anterior funciona | Incompatibilidad de la 1.9.8 | Bajar a la **1.9.3** desde SourceForge, que es más tolerante |

**Recomendación: intentar esto antes que cualquier migración.** Son diez minutos y si funciona
no hay que cambiar de herramienta ni volver a generar nada: ProjectLibre lee directamente el
`Cronograma_257_MindView.xml` que ya tenemos.

---

## 2. Qué necesitamos de la herramienta

Los criterios salen de lo que el proyecto ya tiene hecho, no de una lista genérica.

| # | Criterio | Por qué |
|---|---|---|
| 1 | **Gratis o gratis para estudiantes** durante todo el semestre | Es el problema que estamos resolviendo |
| 2 | **Funciona en Mac con Apple Silicon** | Es el equipo disponible |
| 3 | **Importa MS Project XML (MSPDI)** | Es el formato de `Cronograma_257_MindView.xml`, con 257 tareas y 417 vínculos. Si no lo importa, hay que recapturar todo a mano |
| 4 | **Calcula ruta crítica** | Es el corazón de lo que pide la materia |
| 5 | **Acepta duraciones en horas** | 100 de las 257 tareas duran menos de un día. Una herramienta que solo maneje días enteros infla el cronograma |
| 6 | **Maneja recursos y sobreasignación** | El hallazgo principal del análisis es que siete de ocho áreas están sobreasignadas |
| 7 | **Calcula costos** | La materia pide análisis de costos |

El criterio 5 es el que descarta al candidato que parecía obvio.

---

## 3. Comparativa

| Herramienta | Costo | Mac ARM | MSPDI | Ruta crítica | Horas | Recursos | Costos |
|---|---|---|---|---|---|---|---|
| **ProjectLibre** | Gratis, GPL | Sí, con el arreglo de arriba | Nativo | Sí | Sí | Sí | Sí |
| **GanttProject** | Gratis, GPL3 | Sí | Importa y exporta | Sí | **No** | Sí | Sí |
| **Merlin Project** | ~€19/mes | Nativo, excelente | Sí | Sí | Sí | Sí | Sí |
| **OpenProject Community** | Gratis, autoalojado | Vía navegador | Limitado | Sí | Sí | Sí | Parcial |
| **TaskJuggler** | Gratis, GPL | Sí | No | Sí | Sí | Sí | Sí |
| **MindView** | Prueba de 30 días | Sí | Sí | Sí | Sí | Sí | Sí |

### ProjectLibre — la recomendación

Es el sustituto directo de Microsoft Project: misma lógica, mismos conceptos, lee y escribe
MSPDI de forma nativa. Cubre los siete criterios. Su único defecto es el de arranque en Mac
ARM, que tiene solución documentada.

**Riesgo a considerar:** el proyecto avanza despacio. Hay reportes de incompatibilidad con
versiones recientes de Java, y la última versión estable lleva tiempo sin moverse. Para un
semestre no es problema; para uso profesional a largo plazo sí lo sería.

### GanttProject — descartada por el criterio 5

Parecía la opción obvia: gratis, mantenida desde 2003, multiplataforma, importa MSPDI, calcula
ruta crítica, maneja recursos y costos.

**Pero su duración mínima es un día y no acepta horas ni fracciones.** Es una limitación
conocida, con solicitudes de cambio abiertas desde 2003 que siguen sin implementarse.

En nuestro proyecto eso es grave: hay tareas de 3 y de 5 horas. Si cada una se redondea a un
día completo, las 2,146 horas se convierten en 257 días de calendario y todo el análisis de
ruta crítica se invalida.

**Sirve solo si antes se consolidan las 257 tareas en unas 60 de un día o más**, lo cual es
rehacer el trabajo.

Segunda limitación: solo admite dependencias de fin a inicio. En nuestro caso no estorba,
porque las 417 dependencias son todas de ese tipo.

### Merlin Project — la mejor, pero de paga

Nativa de Mac, rápida, con diagramas de Gantt, kanban y mapas mentales, y buen manejo de
recursos y costos. Cubre todo.

Cuesta alrededor de €19 al mes. Tiene prueba de 30 días, que es exactamente el problema que
queremos evitar. Solo vale la pena si alguien del equipo ya la tiene o si se reparte el costo
de dos meses entre ocho personas, que serían unos $80 por cabeza.

### OpenProject Community — para trabajo en equipo, no para ruta crítica

Es gratis y de código abierto, pero es una plataforma web pensada para colaboración continua,
no una herramienta de programación con red de precedencias. Su importación de MSPDI es
limitada y el análisis de ruta crítica es menos completo. Requiere además montar un servidor,
lo que agrega trabajo de infraestructura que no aporta a la materia.

### TaskJuggler — potente pero sin interfaz

Es un programador de proyectos de línea de comandos: se describe el proyecto en un archivo de
texto y genera los reportes. Maneja horas nativamente, hace ruta crítica y resuelve
asignación de recursos mejor que cualquiera de las anteriores.

No importa MSPDI, pero eso no es un obstáculo real: los scripts del proyecto ya generan el
cronograma desde `rc257.py`, y generar un archivo `.tjp` en vez de un XML es un cambio menor.

**Su problema es de entrega, no técnico:** la docente espera ver un diagrama de Gantt
producido por una herramienta de gestión. TaskJuggler los genera, pero el flujo de trabajo
–editar texto, compilar, revisar– no se parece a lo que la materia enseña.

---

## 4. Recomendación

**Plan A — ProjectLibre.** Aplicar el arreglo de la sección 1. Diez minutos. Si funciona, no
hay que migrar nada ni volver a capturar el cronograma.

**Plan B — Merlin Project repartida.** Si ProjectLibre no levanta y el equipo puede poner unos
$80 por persona, es la mejor herramienta del comparativo y es nativa de Mac.

**Plan C — GanttProject con el cronograma consolidado.** Si no hay presupuesto, consolidar las
257 tareas en unas 60 de duración mínima de un día y trabajar con esa versión. Se pierde
detalle, pero la herramienta es gratis y estable.

**Lo que no recomiendo:** seguir renovando pruebas de 30 días con distintas cuentas. Además de
irregular, en algún momento del semestre se quedan sin acceso al archivo en el peor momento.

---

## 5. Nota sobre el formato del cronograma

Conviene conservar `entregables/Cronograma_257_MindView.xml` como fuente. MS Project XML es el
formato de intercambio más soportado: lo leen ProjectLibre, GanttProject, Merlin Project,
MindView y Microsoft Project.

Si hay que cambiar de herramienta a mitad del semestre, se vuelve a importar ese archivo y no
se pierde nada. Y si cambia algún dato del proyecto, se regenera con
`python3 scripts/gen_mspdi257.py` en lugar de editarlo a mano.

Un apunte de contexto: **Microsoft Project Online se retira el 30 de septiembre de 2026**, de
modo que tampoco es una alternativa a futuro aunque la universidad tuviera licencia.

---

## Fuentes

- [ProjectLibre — hilo del foro sobre Apple Silicon](https://projectlibre.com/topic/cant-open-projectlibre-on-m1-mac/)
- [ProjectLibre — ticket 206, «Bad CPU type in executable» en macOS 15](https://sourceforge.net/p/projectlibre/tickets/206/)
- [ProjectLibre — ticket 191, incompatibilidad con Java 24](https://sourceforge.net/p/projectlibre/tickets/191/)
- [GanttProject — solicitud de granularidad en horas](https://sourceforge.net/p/ganttproject/feature-requests/34/)
- [GanttProject — soporte: cómo fijar duración en horas](https://help.ganttproject.biz/t/how-to-set-duration-in-hours/9320)
- [GanttProject frente a Microsoft Project, 2026](https://ganttfather.com/article/ganttproject-vs-microsoft-project-2026/)
- [Merlin Project — ProjectWizards](https://www.projectwizards.net/en/merlin-project)
- [Alternativas gratuitas a Microsoft Project, 2026](https://onplana.com/blog/free-microsoft-project-alternatives-2026)

## Ver también

- `entregables/Cronograma_257_MindView.xml` — el cronograma en MS Project XML
- `scripts/gen_mspdi257.py` — el generador
- `entregables/Ruta_Critica_257_Tareas_v2.docx` — el análisis que sustenta los criterios
