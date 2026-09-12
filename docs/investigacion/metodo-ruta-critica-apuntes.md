# Método de la Ruta Crítica — apuntes de método

Destilado del documento base «El Método de la Ruta Crítica» (fuente: Agustín Montaño,
adaptación docente) leído el 3-sep-2026. Sirve de referencia para construir la ruta
crítica del proyecto de batería VR y para el ejercicio de clase entregado el 4-sep-2026
(`tareas/2026-09-04-ejemplo-ruta-critica/`).

---

## 1. Origen

| Técnica | Año | Origen | Rasgo distintivo |
|---|---|---|---|
| PERT | 1957 | Marina de EE. UU. + Lockheed + Booz-Allen & Hamilton (programa Polaris) | Tres estimaciones de tiempo: optimista, media, pesimista. Para proyectos con duración incierta. |
| CPM | 1957 | DuPont + Remington Rand (Univac) | Una sola estimación de tiempo. Para proyectos con duraciones conocidas. |

Comparten la misma matemática de red. **Nuestro proyecto usa CPM**: las duraciones de
los paquetes de trabajo ya están fijadas en el cronograma del acta v2.0.

---

## 2. Los dos ciclos y las nueve etapas

**Primer ciclo — planeación y programación**

| # | Etapa | Producto |
|---|---|---|
| 1 | Definición del proyecto | Objetivo, alcance, límites |
| 2 | Lista de actividades | Relación completa, cada una con clave |
| 3 | Matriz de secuencias | Antecedentes / consecuentes de cada actividad |
| 4 | Matriz de tiempos | Duración estimada de cada actividad |
| 5 | Red de actividades (**arreglo lógico**) | Dibujo de la red con eventos numerados |
| 6 | Costos y pendientes | Costo normal, costo límite, pendiente |
| 7 | Compresión de la red | Reducir duración al mínimo costo incremental |
| 8 | Limitaciones de tiempo, recursos y dinero | Ajuste a restricciones reales |
| 9 | Matriz de elasticidad | Holguras y ruta crítica formal |

**Segundo ciclo — ejecución y control:** aprobación, órdenes de trabajo, gráficas de
control, reportes y análisis, toma de decisiones y ajustes.

La **matriz de información** no es una etapa numerada, pero es el cuadro práctico que
consolida etapas 2, 3 y 4 antes de dibujar la red. Conviene siempre construirla.

---

## 3. Elementos de la red (notación AOA — actividad en la flecha)

| Elemento | Dibujo | Significado |
|---|---|---|
| Actividad | Flecha continua | Trabajo real. Consume tiempo y recursos. |
| Evento / nodo | Círculo numerado | Instante. No consume tiempo ni recursos. |
| Actividad ficticia | Flecha punteada | Liga lógica de duración **cero**. |
| Ruta crítica | Trayectoria más larga | Define la duración del proyecto. Holgura cero. |

### Cuándo se necesita una actividad ficticia

1. **Dos actividades comparten el mismo par de eventos.** La notación no lo permite:
   se inserta un evento extra y una ficticia.
2. **Una precedencia parcial.** Cuando varias actividades deben terminar antes de otra,
   pero no todas terminan en el mismo nodo.

### Regla de numeración

Para toda actividad, **i < j** (número del evento de inicio menor que el del evento de
terminación). Garantiza que la red no tenga ciclos y permite recorrerla en un solo sentido.

---

## 4. Las tres preguntas para armar el arreglo lógico

Se aplican a cada renglón de la matriz de información:

1. ¿Qué actividades deben terminar **inmediatamente antes** de que ésta comience?
   → determina el evento de inicio.
2. ¿Qué actividades pueden comenzar **inmediatamente después** de que ésta termine?
   → determina el evento de terminación.
3. ¿Qué actividades pueden ejecutarse **simultáneamente** con ésta?
   → determina las ramas paralelas.

La pregunta 3 es la que responde directamente la observación de la profesora sobre
«indicar qué se puede hacer al mismo tiempo».

---

## 5. Cálculo de tiempos

### Notación

| Símbolo | Nombre | Significado |
|---|---|---|
| `t` | duración | Días que dura la actividad |
| `TPI` | tiempo próximo de iniciación | Lo más pronto que puede empezar |
| `TPT` | tiempo próximo de terminación | `TPI + t` |
| `TRI` | tiempo remoto de iniciación | `TRT − t` |
| `TRT` | tiempo remoto de terminación | Lo más tarde que puede terminar sin retrasar el proyecto |

### Recorrido hacia adelante (calcula TPI / TPT)

```
TPI(actividad) = máximo de los TPT de todos sus antecedentes
TPI(actividad inicial) = 0
TPT = TPI + t
Duración del proyecto = máximo TPT de la red
```

### Recorrido hacia atrás (calcula TRT / TRI)

```
TRT(actividad) = mínimo de los TRI de todos sus consecuentes
TRT(actividad final) = duración del proyecto
TRI = TRT − t
```

---

## 6. Las cuatro holguras

| Holgura | Fórmula | Interpretación |
|---|---|---|
| **Total** (HT) | `TRT − TPI − t` | Retraso máximo sin afectar la fecha final del proyecto. |
| **Libre** (HL) | `mín(TPI de sucesores) − TPT` | Retraso sin afectar el inicio próximo de ninguna actividad siguiente. |
| **Interferente** (HI) | `HT − HL` | Parte de la holgura total que, si se usa, consume holgura de las actividades siguientes. |
| **Independiente** (HI-ind) | `mín(TPI suc.) − máx(TRT antec.) − t` | Retraso sin afectar ni a antecedentes ni a consecuentes. Puede ser negativa; se toma cero. |

---

## 7. Cuándo una actividad es crítica

Las cuatro condiciones son equivalentes; basta verificar una, pero conviene comprobar
varias como control:

1. `TPI = TRI`
2. `TPT = TRT`
3. `TPT − TRI = t`
4. `HT = HL = HI = 0`

La **ruta crítica** es la cadena continua de actividades críticas que va del evento
inicial al final. Puede haber más de una ruta crítica.

---

## 8. Errores frecuentes (vistos al reconstruir el ejemplo del documento base)

- Una actividad sin antecedentes que no sea la inicial → quedó desconectada por error
  de transcripción de la matriz de secuencias.
- Una actividad sin consecuentes que no sea la final → misma causa.
- Corrimiento de renglones al copiar la matriz de secuencias: la red deja de cerrar y
  las holguras dejan de coincidir con la matriz de elasticidad.
- Duración 0 en una actividad real → la convierte en ficticia y falsea la ruta.
- Confundir la **suma** de todas las duraciones con la duración del proyecto. La suma
  siempre es mucho mayor porque hay actividades en paralelo.

**Método de verificación que funcionó:** reconstruir la red, recalcular TPI/TRT y
comparar contra la matriz de elasticidad publicada. Si coincide renglón por renglón,
la red es correcta. En el ejemplo de los aceites esenciales dio 220 días exactos.

---

## 9. Traslape (fast-tracking) y su relación con la red

La red AOA solo admite relaciones **fin → inicio**. Un cronograma donde una actividad
arranca antes de que termine su antecedente NO es representable directamente: eso es
un traslape.

Dos formas correctas de manejarlo:

- **Subdividir** la actividad antecedente en las partes que realmente condicionan a la
  siguiente, de modo que la relación fin→inicio se cumpla entre las subpartes.
- **Documentarlo como compresión de la red** (etapa 7). La red lógica da la duración
  «sin comprimir»; el Gantt refleja la red ya comprimida por traslape. Ambas cifras son
  válidas y deben reportarse juntas.

Esto es directamente relevante para nuestro proyecto: ver
[[ruta-critica-bateria-insumos]], sección «Brecha entre la red lógica y el Gantt».

---

## Ver también

- [[ruta-critica-bateria-insumos]] — aplicación al proyecto de batería VR
- [[evidencia-musicoterapia]] — fundamentación terapéutica
- `tareas/2026-09-04-ejemplo-ruta-critica/` — ejercicio de clase resuelto
