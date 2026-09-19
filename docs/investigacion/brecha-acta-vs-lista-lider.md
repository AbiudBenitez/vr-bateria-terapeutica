# Brecha entre el acta v3.0 y la lista de 257 tareas

**Fecha:** 7-sep-2026
**Para:** discusión de equipo. No es un entregable.

El 3-sep entregamos carta sponsor v2.0, acta constitutiva v3.0, cronograma y ruta crítica
sobre un proyecto de **rehabilitación motriz con asesor terapéutico**. El 7-sep el líder
distribuyó una lista de 257 tareas que describe un proyecto distinto. Los dos no pueden
coexistir: hay que decidir cuál se defiende.

---

## 1. Las diferencias

| Dimensión | Acta v3.0 (3-sep) | Lista de 257 tareas (7-sep) |
|---|---|---|
| Producto | Simulador de batería como herramienta de apoyo a la rehabilitación motriz de miembro superior | Simulación VR de batería **con juego de ritmo**, tipo Guitar Hero, con envoltura de experiencia emocional |
| Fin declarado | Motriz primario, emocional secundario | Emocional. La palabra «rehabilitación» no aparece |
| Usuario | Persona en rehabilitación, bajo supervisión de terapeuta | Usuario general |
| Asesor terapéutico | Requisito. 4 sesiones, 24 h, $21,600. Riesgo R3 del acta | **No existe en la lista** |
| Validación clínica | Objetivo O5, dictamen escrito del asesor | No hay |
| Métricas | Precisión temporal, amplitud de movimiento, constancia del pulso, exportables al terapeuta | Puntuación, combo, precisión porcentual — métricas de videojuego |
| Descomposición | 42 paquetes de trabajo, 7 ramas | 257 tareas, 8 áreas |
| Duración | 50 días hábiles (red PDM con traslapes) | 39.9 días de ruta crítica, 70.9 por carga real |
| Presupuesto | $384,201 MXN, calculado por rol y esfuerzo | No hay |

### Alcance nuevo que no estaba en el acta

El **juego de ritmo** es un subsistema completo que el acta no contempla: 39 tareas, 36 días
de carga. Incluye reloj musical independiente de los FPS, cálculo de BPM y compases,
beatmaps, ventanas de precisión, clasificación de golpes, puntuación y combo, niveles de
dificultad y modo libre.

No es un añadido menor. Es la segunda área más grande del proyecto después de QA.

### Alcance del acta que desaparece

- Asesor terapéutico y su validación (paquetes 2.2, 2.3, 2.5, 2.7, 2.9 del acta)
- Protocolo de sesión y consentimiento informado (2.8)
- Métricas motrices y su exportación al terapeuta (2.6, 6.3)
- Toda la fundamentación de rehabilitación motriz

---

## 2. El equipo tampoco coincide

| Acta v3.0 | Lista del líder |
|---|---|
| Abiud Misael Benítez — Director de proyecto | Misael — Desarrollo VR y batería base |
| Ricardo Alejandro Rodríguez — Gerente de proyecto | **no aparece** |
| Jesús Eduardo Rodríguez — Coordinador | **no aparece** |
| María Fernanda Montoya — Desarrollador VR | María — Investigación y experiencia emocional |
| Diana Laura Tello — Diseñador UX-XR | Diana — QA, documentación y gestión |
| Christian Salvador Valadez — Artista 3D | Christian — Sonido y audio |
| Javier Alejandro Hernández — Diseñador de audio | Javier — Música y diseño rítmico |
| Kimberly González — Analista de métricas | Kimberly — Entorno 3D, assets y ambientación |
| — | **Benjamín** — Juego de ritmo y sistemas |
| — | **Sarai** — UX/UI y tutorial |

Seis personas coinciden pero **cambiaron de área**: María pasa de desarrollo VR a
investigación, Christian de arte 3D a audio, Kimberly de métricas a entorno 3D, Diana de UX
a QA. Aparecen dos integrantes nuevos y desaparecen dos.

Además, la lista **no asigna a nadie los roles de dirección, gerencia y coordinación**. Las
tareas de gestión (QP, QG, QR, QC) quedaron dentro de QA, sumadas a la carga de Diana. Eso
explica en parte por qué QA acumula 70.9 días de trabajo.

---

## 3. Lo que dice el cálculo sobre la lista nueva

Detalle completo en `entregables/Ruta_Critica_257_Tareas.docx`. Resumen:

- La estimación de 36.9 días que circuló es **aritméticamente correcta**; se reprodujo de
  forma independiente hasta la centésima.
- Pero **90 de las 257 tareas no conducen a ningún entregable**. Nadie depende de ellas.
- Las pruebas del prototipo integrado no dependían de que el prototipo estuviera integrado.
  Corregido, la ruta pasa a 39.9 días.
- La ruta crítica **no toca el desarrollo VR ni el juego de ritmo**. Va por bibliografía →
  escenario 3D → QA.
- **Siete de ocho áreas están sobreasignadas.** QA al 178 %.
- Medido por carga, el proyecto necesita **70.9 días hábiles** y solo hay **49** hasta el
  13-nov.

---

## 4. Las opciones

### A. Defender el acta v3.0 y ajustar la lista

Se conserva el enfoque terapéutico ya presentado y aprobado. Habría que:
- reincorporar al asesor, el protocolo de sesión y las métricas motrices;
- decidir si el juego de ritmo entra como mecánica al servicio de la terapia — lo cual es
  defendible, porque la estimulación auditiva rítmica es exactamente eso — o si se recorta;
- volver a mapear las 257 tareas sobre las 7 ramas de la EDT.

**A favor:** no se tira el trabajo entregado ni la fundamentación. La inge ya vio ese enfoque.
**En contra:** obliga al líder a rehacer su reparto.

### B. Adoptar la lista del líder y rehacer la documentación

Carta sponsor v3.0 y acta v4.0 sobre el juego de ritmo con enfoque emocional.

**A favor:** el equipo ya está trabajando con esa nomenclatura y ese reparto.
**En contra:** se pierde el asesor terapéutico, que fue una corrección **exigida por la
docente** el 31-ago. Quitarlo sin explicación es un retroceso visible.

### C. Enfoque híbrido

El juego de ritmo entra como **mecánica de la terapia**, no como fin en sí mismo: las rutinas
rítmicas terapéuticas se implementan como beatmaps, y las ventanas de precisión son la
métrica de sincronización motriz. El asesor valida los beatmaps igual que habría validado las
rutinas.

**A favor:** conserva lo entregado, aprovecha las 257 tareas casi íntegras y le da al juego de
ritmo una justificación terapéutica real.
**En contra:** hay que reescribir la fundamentación para conectar ambas cosas.

---

## 5. Qué hay que decidir, y con qué urgencia

| Decisión | Quién | Urgencia |
|---|---|---|
| ¿Qué proyecto se defiende: el del acta, el de la lista, o el híbrido? | Equipo completo | Antes de tocar cualquier documento |
| ¿Entra o no el asesor terapéutico? | Equipo, con el líder | Alta. Fue una corrección exigida por la docente |
| ¿Quién asume dirección, gerencia y coordinación? | Equipo | Alta. Hoy nadie las tiene y su carga cayó en QA |
| Repartir las tareas de documentación de QA | Líder | Alta. Es lo que más brecha de calendario cierra |
| Declarar el destino de las 90 tareas terminales | Cada responsable de área | Alta. Sin eso no hay cálculo de duración fiable |

---

## Ver también

- `entregables/Ruta_Critica_257_Tareas.docx` — el análisis completo
- `entregables/02_Acta_Constitutiva.docx` — el proyecto entregado el 3-sep
- `docs/investigacion/metodo-ruta-critica-apuntes.md` — el método
- `referencia/Nomenclatura_Tareas_VR_Bateria_Colores.docx` — las 257 tareas
- `referencia/Organizacion_Simulacion_VR_Bateria.docx` — el reparto por áreas
