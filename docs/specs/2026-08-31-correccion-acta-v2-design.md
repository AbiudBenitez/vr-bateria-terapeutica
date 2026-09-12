# Diseño — Corrección del Acta Constitutiva v2.0 y entregables asociados

**Proyecto:** Simulación de Batería en Realidad Virtual con Enfoque Terapéutico
**Equipo:** A · **Docente:** Dra. Leticia Amalia Neira Tovar · **UANL FIME**
**Fecha:** 31 de agosto de 2026
**Estado:** Aprobado, en generación de entregables

---

## 1. Origen

El 30 de agosto de 2026 se presentó el acta constitutiva v1.0. La docente solicitó cinco correcciones:

1. Agregar al diagrama de Gantt todo el trabajo real, incluida la investigación sobre terapia.
2. Conseguir un terapeuta que asesore al equipo.
3. Agregar los perfiles requeridos (diseñador, backend, etcétera), incluido el asesor terapéutico.
4. Desglosar exactamente en qué se aplica el presupuesto.
5. Indicar en el desglose de trabajo qué actividades pueden ejecutarse en paralelo.

Al revisar el acta v1.0 contra la plantilla oficial se detectaron además defectos no señalados por la docente, que también se corrigen.

## 2. Decisiones tomadas

| Decisión | Valor elegido | Alternativas descartadas |
|---|---|---|
| Enfoque terapéutico | **Motriz primario, emocional secundario** | Respetar el alcance amplio sin jerarquía; acotar solo a salud mental |
| Presupuesto | **Recalcular desde cero con tarifas de mercado** | Respetar los $460,000 y desglosarlos hacia atrás; presentar comparativo |
| Formato del cronograma | **MS Project XML** | Excel, OPML, generación directa de `.mvdx` |
| Periodo | **1-sep-2026 → 13-nov-2026**, reserva 16–20 nov | Mantener el 26/10 del plan de recursos v1.0 |

Razón del enfoque jerarquizado: conserva el texto ya presentado y aprobado, evitando contradecir a la docente, y a la vez aterriza las métricas en variables observables (precisión rítmica, velocidad de impacto, simetría) sin depender de instrumentos psicométricos que exigirían un asesor en psicología además del terapeuta.

Razón del formato MS Project XML: MindView 9 lo importa sin requerir Microsoft Project instalado, y es el único formato de intercambio que transporta fechas, duraciones, dependencias y asignación de recursos. Un import de Excel u OPML reconstruiría el árbol de la EDT pero dejaría el Gantt sin fechas ni vínculos. Generar `.mvdx` directamente se descartó por ser un formato propietario no documentado.

## 3. Defectos detectados en el acta v1.0

| # | Defecto | Corrección |
|---|---|---|
| D1 | El título del documento dice "Sistemas de simulación de phishing" | Se sustituye por el nombre real del proyecto |
| D2 | El resumen ejecutivo declara un ciclo de 4 meses, pero el plan de recursos termina el 26/10 (8 semanas) | Se unifica en 11 semanas, 1-sep a 13-nov |
| D3 | Faltan por completo las secciones 5 (Consideraciones del proyecto: riesgos, problemas, supuestos, restricciones) y 6 (Apéndice), pese a estar en la tabla de contenido | Se agregan completas |
| D4 | Falta la tabla de Dependencias que exige la plantilla | Se agrega |
| D5 | El plan de calidad enumera criterios técnicos, pero la plantilla pide los nueve procesos de gestión | Se agregan los nueve |
| D6 | Las tablas de Control del documento y Aprobaciones están vacías | Se llenan |
| D7 | Los encabezados "Estructura del desglose del trabajo" y "Diagrama de Gantt" están vacíos | Se llenan con la EDT y el cronograma |
| D8 | El presupuesto declara $460,000 MXN sin ningún desglose | Se recalcula y desglosa |

## 4. Presupuesto recalculado

Tarifa horaria = sueldo mensual de mercado en Monterrey 2026 dividido entre 173.33 horas.

### 4.1 Personal

| Rol | $/h | % esfuerzo | Semanas | Horas | Costo |
|---|---:|---:|---:|---:|---:|
| Director de proyecto | 375 | 25% | 11 | 110 | 41,250 |
| Coordinador | 173 | 40% | 11 | 176 | 30,448 |
| Gerente de proyecto | 277 | 40% | 11 | 176 | 48,752 |
| Desarrollador VR (Unity) | 260 | 70% | 9 | 252 | 65,520 |
| Diseñador de interacción / UX-XR | 219 | 50% | 8 | 160 | 35,040 |
| Artista 3D | 185 | 50% | 7 | 140 | 25,900 |
| Diseñador de audio | 162 | 40% | 6 | 96 | 15,552 |
| Analista de métricas | 196 | 30% | 7 | 84 | 16,464 |
| **Subtotal equipo interno** | | | | **1,194** | **278,926** |
| Asesor terapéutico externo | 900 | — | — | 24 | 21,600 |
| **Total personal** | | | | | **300,526** |

### 4.2 Hardware, software y operación

| Categoría | Rubro | Monto |
|---|---|---:|
| Hardware | Meta Quest 3 128 GB | 11,999 |
| Hardware | Meta Quest 3S 128 GB | 6,999 |
| Hardware | Depreciación de PC de desarrollo | 8,000 |
| Hardware | Periféricos y almacenamiento | 2,500 |
| Software | Assets 3D y entorno | 4,500 |
| Software | Librería de samples de batería | 3,000 |
| Operación | Conectividad, energía y espacio | 6,000 |
| Operación | Papelería, consentimientos y encuestas | 1,500 |
| Operación | Incentivos a participantes (15 × 150) | 2,250 |
| Operación | Traslados a sesiones con el asesor | 2,000 |
| | **Subtotal** | **48,748** |

### 4.3 Total

| Concepto | Monto |
|---|---:|
| Costos directos | 349,274 |
| Reserva de contingencia (10%) | 34,927 |
| **TOTAL** | **384,201 MXN** |

**Variación contra la v1.0:** −$75,799, es decir −16.5%. La cifra original asumía un ciclo de cuatro meses; el cronograma real es de once semanas. Unity Personal, Blender y las librerías de audio libres tienen costo cero, lo que reduce el rubro de software respecto de una estimación gruesa.

## 5. Perfiles requeridos

| Rol | Perfil profesional | Competencias clave | Asignado |
|---|---|---|---|
| Director de proyecto | Gestión de proyectos de TI | PMBOK, control de alcance, toma de decisiones | Benjamín Villalón |
| Coordinador | Coordinación de equipos | Seguimiento, comunicación, gestión de reuniones | Sarai Galindo |
| Gerente de proyecto | Administración de proyectos | Cronograma, recursos, control de avance y riesgos | Abiud Benítez |
| Desarrollador VR | Ingeniería de software con especialidad XR | Unity, C#, XR Interaction Toolkit, SDK de Meta, optimización móvil | Ma. Fernanda Montoya |
| Diseñador de interacción / UX-XR | Diseño de experiencia de usuario | Ergonomía en VR, interfaz espacial, accesibilidad, prevención de motion sickness | Diana Laura Tello |
| Artista 3D | Modelado y arte digital | Blender, modelado low-poly, mapeo UV, texturizado, optimización de geometría | Christian Valadez |
| Diseñador de audio | Producción y diseño sonoro | Edición de samples, capas de velocity, audio espacial, control de latencia | Javier Hernández |
| Analista de métricas | Análisis de datos | Diseño de indicadores, JSON, análisis descriptivo, reportes | Kimberly González |
| Asesor terapéutico | Fisioterapeuta, terapeuta ocupacional o musicoterapeuta certificado | Rehabilitación motriz de extremidad superior, diseño de rutinas, criterios de seguridad, validación clínica | Externo, por conseguir |
| QA y pruebas | Rotativo dentro del equipo | Casos de prueba, medición de latencia y FPS, registro de defectos | Rol compartido |

**Perfil de backend: no requerido.** La aplicación es standalone en el visor y las métricas se escriben en JSON local. Se declara explícitamente en el acta para justificar su ausencia en la plantilla de personal.

### 5.1 Plan de adquisición del asesor terapéutico

| Actividad | Semana | Fecha límite |
|---|---|---|
| Definir el perfil requerido y redactar la carta de solicitud | S1 | 4-sep |
| Contactar Facultad de Psicología UANL, Facultad de Música UANL y clínicas de rehabilitación física | S1–S2 | 11-sep |
| Confirmar asesor y acordar alcance de participación | S3 | 18-sep |
| Sesión 1: validación de rutinas rítmicas y criterios de seguridad | S5 | 2-oct |
| Sesión 2: revisión de métricas motrices | S7 | 16-oct |
| Sesión 3: validación previa a pruebas con usuarios | S9 | 30-oct |

Presupuestado a 24 horas de honorarios. **Contingencia:** si no se confirma asesor al cierre de la semana 3, se adoptan protocolos publicados de Neurologic Music Therapy y se documenta la ausencia de validación profesional como limitación explícita del proyecto.

## 6. Cronograma

**Inicio 1-sep-2026 (martes). Fin 13-nov-2026 (viernes). Reserva de gestión 16–20 nov. Exámenes desde el 23-nov.**

| Semana | Fechas | Observación |
|---|---|---|
| S1 | 1 – 4 sep | Arranca en martes |
| S2 | 7 – 11 sep | |
| S3 | 14 – 18 sep | 16 de septiembre inhábil |
| S4 | 21 – 25 sep | |
| S5 | 28 sep – 2 oct | |
| S6 | 5 – 9 oct | |
| S7 | 12 – 16 oct | |
| S8 | 19 – 23 oct | |
| S9 | 26 – 30 oct | |
| S10 | 2 – 6 nov | |
| S11 | 9 – 13 nov | Entrega final |
| Reserva | 16 – 20 nov | 16 de noviembre inhábil |

### 6.1 Hitos

| Hito | Cierre de | Fecha | Contenido |
|---|---|---|---|
| H1 | S2 | 11-sep | Diseño conceptual aprobado y fundamentación terapéutica base |
| H2 | S4 | 25-sep | Spike de latencia: decisión Go / No-Go |
| H3 | S7 | 16-oct | Modelos 3D integrados con físicas funcionales |
| H4 | S9 | 30-oct | Audio, rutinas terapéuticas y métricas integradas |
| H5 | S10 | 6-nov | Build estable congelada |
| H6 | S11 | 13-nov | Pruebas cerradas y documentación entregada |

## 7. EDT con carriles paralelos

Siete ramas de primer nivel, descompuestas por entregables. Seis carriles se ejecutan de forma simultánea.

| Carril | Rama | Semanas activas |
|---|---|---|
| A | 1. Gestión del proyecto | S1 – S11 |
| B | 2. Fundamentación terapéutica | S1 – S9 |
| C | 3. Modelo 3D y entorno | S2 – S7 |
| D | 4. Sistema de interacción y físicas | S3 – S8 |
| E | 5. Sistema de audio y rutinas | S5 – S9 |
| F | 6. Prototipo funcional integrado | S8 – S10 |
| F | 7. Pruebas y documentación | S9 – S11 |

### 7.1 Paralelismos declarados

1. **La rama 2 es independiente de las ramas 3, 4 y 5 hasta la semana 8.** La investigación terapéutica, la búsqueda del asesor y el diseño de rutinas no bloquean el desarrollo. Responde directamente a la observación de la docente sobre la investigación de terapia.
2. **Las ramas 3 y 4 corren en paralelo de S3 a S7.** Las físicas se desarrollan sobre primitivas geométricas (cilindros y discos) y los modelos definitivos se sustituyen en el paquete 4.6. El desarrollo no espera al arte.
3. **La rama 5 arranca en S5 sobre la rama 4 en curso**, no después de terminarla. Dentro de la rama 7, los manuales (7.5) se redactan en paralelo con la ejecución de pruebas (7.2 a 7.4).

### 7.2 Ruta crítica

4.1 → 4.2 → 4.4 → 4.5 → 4.6 → 5.3 → 6.4 → 7.2 → 7.3 → 7.6

El resto de los paquetes dispone de holgura. El congelamiento de funcionalidad en la semana 10 no es negociable: sin build estable no hay pruebas con usuarios, y sin pruebas no hay informe de resultados.

## 8. Entregables de esta corrección

| # | Archivo | Formato | Propósito |
|---|---|---|---|
| E1 | `entregables/Acta_Constitutiva_v2.0.docx` | Word | Acta corregida, completa contra la plantilla |
| E2 | `entregables/Cronograma_MindView.xml` | MS Project XML | Importable en MindView: genera el diagrama de Gantt y la vista de esquema/EDT |
| E3 | `CLAUDE.md` | Markdown | Contexto persistente para sesiones futuras |
| E4 | `docs/specs/` | Markdown | Diseño técnico del prototipo y de esta corrección |

## 9. Instrucciones de importación en MindView

1. Abrir MindView 9.
2. Menú **Archivo → Importar → Microsoft Project → Documento XML de Microsoft Project**.
3. Seleccionar `entregables/Cronograma_MindView.xml`.
4. La importación genera el árbol de tareas con fechas, duraciones, dependencias y recursos asignados.
5. Cambiar a la vista **Gantt** para el diagrama de Gantt.
6. Cambiar a la vista **Mapa mental** o **Esquema** para el diagrama de la EDT.

No se requiere tener Microsoft Project instalado.
