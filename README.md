# Simulación de batería en realidad virtual con enfoque terapéutico

Proyecto de la unidad de aprendizaje **Administración de Proyectos de Software**
Facultad de Ingeniería Mecánica y Eléctrica · Universidad Autónoma de Nuevo León
Docente: Dra. Leticia Amalia Neira Tovar · **Equipo A**

Un simulador de batería en realidad virtual concebido como apoyo a la rehabilitación motriz
de miembro superior, con un módulo de juego de ritmo. El usuario toca una batería virtual
siguiendo rutinas rítmicas graduadas, y el sistema registra su desempeño.

**Periodo:** 7 de septiembre al 13 de noviembre de 2026.

---

## ¿Qué busco y dónde está?

| Si buscas… | Ve a |
|---|---|
| Los documentos que se entregan a la docente | [`entregables/`](entregables/) |
| El cronograma para abrir en ProjectLibre | [`entregables/Cronograma_ProjectLibre.xml`](entregables/Cronograma_ProjectLibre.xml) |
| Cómo colaborar sin pisar el trabajo de otro | **[`COMO-COLABORAR.md`](COMO-COLABORAR.md)** |
| Practicar el flujo de ramas y pull requests | [`FIRMAS.md`](FIRMAS.md) |
| El código del prototipo en Unity | [`proyecto-unity/`](proyecto-unity/) |
| Guía técnica del sistema de percusión | [`prototipo/`](prototipo/) |
| Tareas individuales de la materia | [`tareas-individuales/`](tareas-individuales/) |
| Investigación y decisiones de diseño | [`docs/`](docs/) |

---

## Entregables

Van numerados en el orden en que los produce la metodología: primero se autoriza el proyecto,
luego se define, después se programa y por último se costea y controla.

| Archivo | Qué es | Procesos del PMBOK |
|---|---|---|
| `01_Carta_Sponsor.docx` | Autorización del proyecto, beneficios y medidas de éxito | Inicio |
| `02_Acta_Constitutiva.docx` | Alcance, estructura de desglose del trabajo, organización y presupuesto | 4.1, 5.4 |
| `03_Ruta_Critica.docx` | Red de precedencias, ruta crítica y matriz de elasticidad sobre 257 actividades | 6.2 a 6.6 |
| `04_Planes_Costos_Calidad_Riesgos.docx` | Los tres planes de gestión y el diseño de las pruebas | 7, 8 y 11 |
| `05_Analisis_Costos_Calidad_Riesgos.docx` | Análisis numérico que sustenta al anterior | 7.2 a 7.4 |
| `06_Entregable_Medio_Curso.docx` | Compromiso de entrega del 21 de septiembre | — |
| `Cronograma_ProjectLibre.xml` | Cronograma completo, con costos y avance | 6.5 |

Las versiones anteriores están en `entregables/superados/`. No se borran: son evidencia de
cómo evolucionó el proyecto.

---

## Cifras del proyecto

| | |
|---|---|
| Actividades | 257, con 417 dependencias |
| Esfuerzo | 1,978 horas |
| Duración de la red | 38.25 días hábiles |
| Reserva de cronograma | 10.75 días hábiles |
| Presupuesto | $104,013 MXN |
| Casos de prueba diseñados | 30 (14 de caja blanca, 16 de caja negra) |
| Riesgos identificados | 18 en siete categorías |

---

## Equipo

| Área | Responsable |
|---|---|
| Desarrollo VR y batería | Misael |
| Juego de ritmo y sistemas | Benjamín |
| Investigación y experiencia emocional | María |
| Música y diseño rítmico | Javier |
| Sonido y audio | Christian |
| Interfaz y tutorial | Sarai |
| Entorno 3D, assets y ambientación | Kimberly |
| Aseguramiento de calidad, documentación y gestión | Diana |

---

## Los documentos se generan con scripts

Ninguno de los documentos de `entregables/` se edita a mano. Todos salen de los scripts de
[`scripts/`](scripts/), que a su vez leen un modelo común de datos.

La razón es práctica: las mismas cifras —duración, costo, ruta crítica— aparecen en varios
documentos a la vez. Editar un Word a mano las desincroniza y ya pasó antes.

Si cambia una duración o una dependencia, se edita el módulo de datos y se regenera. El
detalle está en [`scripts/README.md`](scripts/README.md).

```bash
cd scripts
python3 rc257.py      # ruta crítica y holguras
python3 costos.py     # presupuesto y reservas
```
