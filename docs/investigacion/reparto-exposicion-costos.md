# Reparto de la exposición — Análisis de Costos, Calidad y Riesgos

**Documento base:** `entregables/05_Analisis_Costos_Calidad_Riesgos.docx`
**Duración total:** unos 26 minutos, más preguntas.
**Regla general:** cada quien dice **la cifra exacta**, no «aproximadamente». Las cifras están
abajo para que no haya que buscarlas.

---

## Las tres cifras que todos deben saber

Si a cualquiera le preguntan algo fuera de su parte, estas tres salvan la situación:

| | |
|---|---|
| **1,978 horas** | Esfuerzo total, sobre 257 actividades |
| **$294,981** | Presupuesto total del proyecto |
| **$113.72 por hora** | Tarifa media ponderada, de fuentes oficiales |

Y la frase que sostiene todo el documento:

> «Las tarifas no salen de portales de empleo. Salen del Observatorio Laboral de la Secretaría
> del Trabajo, con datos de la Encuesta Nacional de Ocupación y Empleo del INEGI.»

---

## 1 · Misael — Apertura y método

**Secciones 1, 2 y 3 · 3 minutos**

### Qué dice

- El documento cubre tres áreas del PMBOK: costos, calidad y riesgos.
- El plan de gestión de costos define las reglas antes de estimar: unidad de medida
  hora-persona, moneda peso mexicano, exactitud de ±10 %, umbral de control del 10 % por área.
- La regla de medición es **valor ganado 0/100**: una actividad aporta valor solo cuando cumple
  su criterio de aceptación. No se reconoce avance parcial.
- Se evaluaron tres técnicas de estimación y se eligió la **ascendente**.

### El punto fuerte

Explicar **por qué** se descartaron las otras dos:

- **Análoga:** el equipo no ha hecho ningún proyecto de realidad virtual antes. No hay
  referente del cual partir.
- **Paramétrica:** no hay datos históricos propios para calibrar el parámetro.
- **Ascendente:** el trabajo ya está descompuesto en 257 actividades con duración individual.
  Es la más exacta y la única que el estado de la planificación permite aplicar.

### Qué mostrar

La tabla comparativa de las tres técnicas, sección 3.

### Si preguntan

> **¿Por qué no usaron tres valores como en PERT?**
> Porque la lista de tareas del equipo da una sola estimación por actividad, no tres. Cuando
> viene un rango se toma el valor menor, que es el criterio de la hoja de control.

---

## 2 · Benjamín — Las tarifas y sus fuentes

**Sección 4 · 4 minutos** — es la parte que más se va a cuestionar

### Qué dice

Cuatro fuentes, todas oficiales:

| Fuente | Institución | Dato |
|---|---|---|
| Observatorio Laboral | Secretaría del Trabajo, con ENOE del INEGI | TIC **$21,697/mes** · promedio de profesionistas **$19,494/mes** |
| Data México | Secretaría de Economía | Ocupación desarrolladores de software: **$11,000/mes** |
| CONASAMI | — | Salario mínimo **$315.04/día** |
| IMSS | — | Salario base de cotización **$662.80/día** |

Conversión: ingreso mensual ÷ **173.33 horas** laborables al mes.

### El punto fuerte

Decir abiertamente que **una versión previa daba $559,891 y estaba mal**:

> «La primera estimación usaba tarifas de mercado tomadas de referencias no oficiales y daba
> $559,891. Al sustituirlas por datos del Observatorio Laboral, el costo de mano de obra bajó
> 45 %. La diferencia no es cosmética: los portales publican el salario **ofrecido en
> vacantes**, que es sistemáticamente mayor que el **percibido**, porque las vacantes mejor
> pagadas son las que más se publican y el monto anunciado suele ser el tope del rango. La
> ENOE mide lo percibido, que es lo que corresponde para estimar un costo.»

Reconocer el error y explicarlo vale más que esconderlo.

### El remate

> «La tarifa media que nos salió, $113.72 por hora, equivale casi exactamente a dos salarios
> mínimos generales. Son dos caminos independientes que dan el mismo orden de magnitud.»

### Qué mostrar

La tabla de perfiles con su referencia, factor y justificación, sección 4.3.

### Si preguntan

> **¿Por qué el director cobra más que la referencia de TIC?**
> Lleva un factor de 1.40 por responsabilidad directiva sobre alcance y presupuesto. Todos los
> factores están declarados con su justificación en la misma tabla.

> **Data México dice $11,000, ustedes usan $21,697. ¿Por qué el más alto?**
> Miden universos distintos. Data México mide la ocupación completa, incluye gente sin estudios
> superiores y un 14.2 % de informalidad. El Observatorio Laboral mide profesionistas
> titulados, que es el perfil que el proyecto requiere.

---

## 3 · Kimberly — Perfiles y agregación ascendente

**Secciones 5 y 6 · 3 minutos**

### Qué dice

- La tarifa se asignó por **grupo de claves**, no por área. Son 68 grupos.
- Razón: dentro de un área conviven perfiles distintos. El caso claro es QA, que reúne
  planificación, pruebas y redacción de manuales. Cobrarlas al mismo precio distorsionaría.
- El costo sube por tres niveles: actividad → grupo → área → proyecto. Cada nivel es una cuenta
  de control.

### Las cifras

| Área | Responsable | Horas | Costo | % |
|---|---|---|---|---|
| QA, documentación y gestión | Diana | 511 | $59,280 | 26.4 % |
| Juego de ritmo | Benjamín | 264 | $33,048 | 14.7 % |
| Entorno 3D y assets | Kimberly | 254 | $28,567 | 12.7 % |
| Interfaz / UX-UI | Sarai | 228 | $25,643 | 11.4 % |
| Desarrollo VR y batería | Misael | 192 | $24,035 | 10.7 % |
| Experiencia emocional | María | 186 | $20,919 | 9.3 % |
| Música | Javier | 185 | $18,036 | 8.0 % |
| Sonido | Christian | 158 | $15,403 | 6.8 % |
| **Total** | | **1,978** | **$224,931** | **100 %** |

### El punto fuerte

Explicar el 26.4 % de QA sin que suene a error:

> «No es un error de estimación. Son 60 de las 257 actividades, y además de las pruebas absorbe
> la planificación, el seguimiento y toda la documentación, porque la organización del equipo
> no asignó a nadie los roles de dirección, gerencia y coordinación.»

### Qué mostrar

La figura 3, distribución del costo por área y por perfil.

---

## 4 · Christian — Costos no laborales y presupuesto

**Secciones 7 y 8 · 3 minutos y medio**

### Qué dice

**Primero, lo que la Facultad presta y por eso no es costo:**

> «Los visores los presta la Facultad. Conforme al PMBOK, los recursos que aporta la
> organización ejecutante no se cargan al presupuesto, pero sí se registran: valen $18,998 y su
> disponibilidad es un supuesto del que depende el proyecto. Por eso generan el riesgo R5.»

**Después los cuatro niveles del presupuesto**, y quién dispone de cada uno:

| Nivel | Monto | Quién dispone |
|---|---|---|
| Costos directos | $248,681 | El gerente, dentro de cada cuenta de control |
| **Línea base de costos** | **$280,981** | El gerente. Incluye la reserva de contingencia |
| Presupuesto total | **$294,981** | La patrocinadora. Incluye la reserva de gestión |

Desglose: mano de obra $224,931 + no laborales $23,750 + contingencia $32,300 + gestión $14,000.

### El punto fuerte

> «La reserva de contingencia no es un porcentaje inventado. Son $32,300 que salen del valor
> monetario esperado de nueve riesgos identificados. Un 10 % fijo, que es la práctica por
> defecto, habría dado $24,868: una cifra sin sustento.»

### Qué mostrar

La figura 1, curva S. Y señalar que es **frontal**: cerca del 60 % del costo se acumula en la
primera mitad, porque las ocho áreas arrancan a la vez. Consecuencia práctica: **el desembolso
se necesita temprano, no repartido.**

---

## 5 · Javier — Escenarios de sensibilidad

**Sección 9 · 2 minutos y medio**

### Qué dice

El presupuesto valora el trabajo a tarifas de profesionista titulado. Hay otras dos formas
legítimas de costear un proyecto académico:

| Escenario | Mano de obra | Presupuesto | Qué responde |
|---|---|---|---|
| **A.** Costo de bolsillo | $0 | **$58,850** | Cuánto dinero sale realmente del bolsillo del equipo |
| **B.** Valorizado a practicante | $163,936 | **$230,986** | Qué pagaría una empresa a este equipo por su nivel |
| **C.** Valorizado a profesionista | $224,931 | **$294,981** | Cuánto costaría que una empresa lo ejecutara con personal calificado |

**C es la línea base.**

### El punto fuerte

> «El escenario A es la cifra real de un proyecto escolar: el trabajo se cursa por créditos y no
> se remunera. Lo documentamos porque es el único dinero que de verdad vamos a desembolsar. Pero
> la línea base es C, porque la pregunta que da sentido a un ejercicio de administración de
> proyectos es cuánto costaría ejecutarlo profesionalmente.»

Y el argumento de robustez:

> «B y C se separan solo 22 %. Esa cercanía indica que la estimación principal no está inflada.»

---

## 6 · Sarai — Tabla de simultaneidad

**Sección 10 · 2 minutos y medio**

### Qué dice

Qué trabajo puede ejecutarse al mismo tiempo. Sale directo de la red: dos actividades son
simultáneas cuando sus intervalos se traslapan y ninguna depende de la otra.

| Días | Áreas activas | Tareas en curso |
|---|---|---|
| 0 – 5 | **8** | 72 |
| 5 – 10 | **8** | 78 |
| 10 – 15 | 6 | 59 |
| 15 – 20 | 7 | 38 |
| 20 – 25 | 4 | 18 |
| 25 – 30 | 4 | 12 |
| 30 – 35 | 1 | 15 |
| 35 – 38 | 1 | 3 |

### El punto fuerte

Las dos lecturas que la tabla permite:

> «El máximo paralelismo está en los primeros diez días: las ocho áreas activas y hasta 78
> tareas en curso. A partir del día 30 solo queda QA. Eso explica dos cosas a la vez: la forma
> frontal de la curva S y por qué el área de QA termina sobrecargada.»

Y el matiz que evita una pregunta incómoda:

> «Que haya 78 tareas simultáneas no es un problema mientras cada área tenga su persona, porque
> pertenecen a áreas distintas. El problema aparece dentro de cada área.»

---

## 7 · María — Compresión de la red

**Sección 11 · 3 minutos**

### Qué dice

- Comprimir es acelerar actividades pagando más. Solo tiene sentido sobre la ruta crítica:
  acelerar una actividad con holgura no adelanta nada y sí cuesta.
- **Modelo adoptado: tiempo extraordinario.** Cada área tiene una sola persona, así que no se
  puede comprimir añadiendo gente: no hay a quién añadir sin quitarlo de otra área.
- Jornada de 8 a 10 horas, las 2 extra al 150 %. Reducción máxima del 20 % de la duración.

### Las cifras

| | |
|---|---|
| Duración normal | **38.25 días** |
| Compresión máxima | **34.15 días** |
| Días ganados | 4.10 |
| Sobrecosto total | **$1,964** |
| Costo marginal | de **$401** a más de $2,500 por día |

### El punto fuerte

El hallazgo matemático:

> «La pendiente de costo resultó idéntica dentro de cada perfil: $401 por día en las
> actividades de QA, $450 en las de análisis. No es casualidad. Con el modelo de tiempo
> extraordinario, la pendiente es exactamente cuatro veces la tarifa horaria, sin importar
> cuánto dure la actividad. La conclusión práctica es que conviene comprimir primero el
> trabajo de los perfiles más baratos que estén sobre la ruta crítica.»

### El cierre honesto

> «El proyecto no necesita comprimirse: la ruta crítica son 38.25 días y hay 49 disponibles.
> La compresión es un instrumento de contingencia. Y tiene un límite que conviene declarar:
> resuelve problemas de ruta crítica, no de carga de trabajo.»

### Qué mostrar

La figura 2, curva de compresión. Señalar que los escalones se van haciendo más caros.

---

## 8 · Diana — Calidad, riesgos y cierre

**Secciones 12, 13 y 14 · 5 minutos**

### Parte A — Costo de la calidad

| Categoría | Tipo | Monto |
|---|---|---|
| Prevención | Conformidad | $20,720 |
| Evaluación | Conformidad | $10,615 |
| Fallos internos | No conformidad | $9,068 |
| **Total** | | **$40,403 · 18.0 % de la mano de obra** |

**El punto fuerte** — adelantarse a la objeción:

> «18 % está por encima de la referencia de la industria del software, que ronda el 15 %. La
> explicación es concreta: en un proyecto académico la documentación es en sí misma un
> entregable evaluable, así que la prevención incluye tareas que en un proyecto comercial no
> existirían.»

Y la lectura que importa:

> «La proporción sí es sana: $20,720 en prevención contra $9,068 en corregir fallos. Cuesta
> menos evitar un defecto que repararlo. Si fuera al revés, indicaría que estamos descubriendo
> los problemas demasiado tarde.»

### Parte B — Riesgos

Nueve riesgos identificados. Valor monetario esperado total: **$32,260**, que es de donde sale
la reserva de contingencia.

Los tres mayores:

| Id | Riesgo | Valor esperado |
|---|---|---|
| R1 | La latencia supera 30 ms y obliga a rehacer el audio | $6,300 |
| R3 | La carga de QA no cabe en su ventana | $6,000 |
| R2 | La cadena del entorno 3D se retrasa | $5,400 |

**Qué mostrar:** la figura 4, matriz de probabilidad e impacto.

**El que hay que mencionar aunque no sea el mayor:**

> «R5, que la Facultad no concrete el préstamo de los visores, tiene un impacto de $18,998, el
> 80 % de todos nuestros costos no laborales. Es la contrapartida de haber sacado el equipo del
> presupuesto: el ahorro es real, pero traslada una dependencia externa al proyecto.»

### Parte C — Cierre

Las tres recomendaciones, en orden:

1. **Confirmar por escrito el préstamo de los visores** antes de iniciar el desarrollo.
2. **Redistribuir la documentación de QA** entre las ocho áreas. Es la restricción dominante:
   QA tiene 511 horas asignadas y su ventana permite unas 306.
3. **Asignar los roles de dirección, gerencia y coordinación**, que hoy no tiene nadie.

Y la frase final:

> «La restricción del proyecto no es de costo ni de ruta crítica: es de carga de trabajo. Seis
> de las ocho áreas están sobreasignadas y QA al 167 %. Eso no se arregla comprimiendo el
> cronograma; se arregla redistribuyendo.»

---

## Preguntas probables, con respuesta

| Pregunta | Quién responde | Respuesta |
|---|---|---|
| ¿De dónde sacaron los salarios? | Benjamín | Observatorio Laboral de la STPS con datos de la ENOE del INEGI, Data México de la Secretaría de Economía, CONASAMI e IMSS. Ninguna de portales de empleo. |
| ¿Por qué bajó tanto respecto de la vez pasada? | Benjamín | Las tarifas anteriores eran de mercado, sin fuente. Al usar datos oficiales bajó 45 % la mano de obra. |
| ¿Por qué QA cuesta la cuarta parte? | Kimberly | 60 de 257 actividades, y absorbe la gestión del proyecto porque nadie tiene asignados esos roles. |
| ¿Y los visores? | Christian | Los presta la Facultad. No van al presupuesto pero sí al registro de supuestos, y generan el riesgo R5. |
| ¿Por qué la contingencia es de $32,300? | Christian | Es el valor monetario esperado de los nueve riesgos, no un porcentaje fijo. |
| ¿Van a terminar a tiempo? | María o Diana | Por ruta crítica sí: 38.25 días contra 49 disponibles. Por carga de trabajo no, y por eso la recomendación principal es redistribuir. |
| ¿Qué software usan? | Quien esté exponiendo | ProjectLibre. El cronograma completo está cargado ahí con las 257 tareas, 417 dependencias y el avance real. |

---

## Antes de exponer

- [ ] Que cada quien lea **su sección completa** en el documento, no solo esta guía.
- [ ] Ensayar la transición entre partes. El orden encadena: método → tarifas → agregación → presupuesto → escenarios → simultaneidad → compresión → calidad y riesgos.
- [ ] Tener el documento abierto en el PDF para saltar a las tablas si preguntan.
- [ ] Tener ProjectLibre abierto con el cronograma cargado, por si piden verlo.
- [ ] Nadie dice «aproximadamente». Las cifras están arriba.
