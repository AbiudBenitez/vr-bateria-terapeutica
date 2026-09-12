# Diseño — Costos, calidad y riesgos

**Fecha:** 11-sep-2026
**Entregables:** análisis de costos, planes de calidad y riesgos, y comparativa de software.

## Problema

La docente pidió cuatro cosas: tabla de compresión, costos conforme al PMBOK con estimación
ascendente, análisis de calidad y riesgos, y una revisión de certificaciones. Además señaló
que el proyecto estaba **muy caro** y exigió que las tarifas salieran de fuentes del gobierno,
no de portales tipo LinkedIn. Por separado, la prueba de MindView caduca a los 30 días y
ProjectLibre no abre en la Mac del usuario.

## El hallazgo que originó el recálculo

La primera estimación dio **$559,891**. Usaba tarifas de mercado puestas a ojo: $45,000/mes
para un desarrollador VR, $65,000 para un director.

Los datos oficiales dicen otra cosa. El Observatorio Laboral de la STPS, con datos de la ENOE
del INEGI para el 2.º trimestre de 2026, reporta **$21,697/mes** para profesionistas del área
de TIC y **$19,494/mes** de promedio nacional. Es decir, mis tarifas estaban al doble.

La causa es conocida y vale la pena dejarla escrita: los portales de empleo publican el
salario **ofrecido en las vacantes**, no el **percibido**. Las vacantes mejor pagadas son las
que más se publican y el monto anunciado suele ser el tope del rango. La ENOE mide lo
percibido, que es lo que corresponde para estimar un costo.

Recalculado: mano de obra −45%, presupuesto **$315,034**, un 44% menos.

## Decisiones

| Decisión | Alternativa descartada | Razón |
|---|---|---|
| Tarifas solo de fuentes oficiales mexicanas | Portales de empleo, o mantener las estimaciones previas | Petición explícita de la docente, y el contraste demostró que tenía razón. |
| Escenario C (profesionista oficial) como línea base, con A y B de sensibilidad | Un solo escenario | Elección del usuario. C responde «cuánto costaría que una empresa lo ejecutara», que es la pregunta que da sentido al ejercicio; A es el desembolso real y B el intermedio. Los tres documentados permiten defender cualquiera sin rehacer nada. |
| Tarifa por grupo de claves (68), no por área (8) | Una tarifa por persona | Elección del usuario. En QA conviven gestión, pruebas y redacción, con costos muy distintos. Una tarifa promedio ocultaba que esa área concentra el 27% del costo. |
| Visores fuera del presupuesto, como recurso proporcionado por la Facultad | Comprarlos ($18,998) | Petición del usuario. Conforme al PMBOK, lo que aporta la organización ejecutante no se carga al proyecto, pero se registra: es un supuesto y genera el riesgo R5. |
| Assets y muestras con licencia libre | Comprarlos ($7,500) | Petición del usuario. Sube la probabilidad del riesgo R4 (licencias ambiguas), que se ajustó en consecuencia. |
| Licencias musicales se conservan ($3,500) | Sustituirlas también por música libre | La oferta libre con la estructura rítmica que exige el juego de ritmo es insuficiente, y una licencia dudosa costaría más que el ahorro. |
| Reserva de contingencia por valor monetario esperado | 10% fijo sobre costos directos | El EMV de nueve riesgos da $32,300; un 10% habría dado $26,773, una cifra sin sustento. |
| Modelo de compresión por tiempo extraordinario | Compresión por recurso adicional | Cada área tiene una sola persona: no hay a quién añadir sin quitarlo de otra área. |
| Las dos acepciones de «compresión» | Solo una | Elección del usuario. La tabla de simultaneidad es lo que ella describió; la compresión formal con pendientes de costo es la etapa 7 del método y sale casi gratis teniendo los costos. |
| ProjectLibre como recomendación principal | Migrar a otra herramienta | El fallo tiene causa identificada (`libharfbuzz`) y solución en diez minutos. Si funciona, no hay que migrar ni recapturar el cronograma. |

## Hallazgos

1. **Las tarifas estaban al doble de los datos oficiales.** Presupuesto de $559,891 a $315,034.

2. **Validación cruzada independiente:** la tarifa media resultante ($113.69/h) coincide casi
   exactamente con dos salarios mínimos generales ($110.51/h). Dos caminos distintos dan el
   mismo orden de magnitud.

3. **La pendiente de compresión es constante por perfil.** Bajo el modelo de tiempo
   extraordinario resulta ser exactamente 4 × la tarifa horaria, con independencia de la
   duración de la actividad. Conclusión práctica: comprimir primero los perfiles más baratos
   que estén sobre la ruta crítica.

4. **La compresión no resuelve el problema real.** El proyecto puede bajar a 37 días por
   $4,354, pero la restricción dominante es la carga de QA (567 h en una ventana de ~362 h).
   Comprimir la ruta crítica no corrige eso; redistribuir trabajo, sí.

5. **El costo de la calidad es 19.1% de la mano de obra**, por encima de la referencia de la
   industria (~15%). La causa es que la documentación es en sí misma un entregable evaluable.
   La proporción interna sí es sana: más prevención que corrección.

6. **GanttProject queda descartada por una limitación específica:** duración mínima de 1 día.
   Con 100 de las 257 tareas por debajo de un día, inflaría el cronograma. Era el candidato
   gratuito más obvio.

7. **ProjectLibre falla por `libharfbuzz`**, no por el chip. Tiene arreglo documentado.

## Verificaciones

- Las cifras de los tres documentos y las cuatro figuras se derivan de `costos.py`: no hay
  ningún monto escrito a mano.
- Los PNG incrustados coinciden por hash con los de disco.
- Los cuatro SVG son XML válido con texto editable.
- Sin markdown literal filtrado a los Word.

## Fuera de alcance

- Actualizar el acta constitutiva y la carta sponsor con el presupuesto nuevo: siguen
  desalineadas del proyecto de 257 tareas. Ver `brecha-acta-vs-lista-lider.md`.
- Generar archivos de importación para las herramientas alternativas: se recomienda arreglar
  ProjectLibre primero.
- Propuesta cuantificada de redistribución de la carga de QA: decisión del equipo.
