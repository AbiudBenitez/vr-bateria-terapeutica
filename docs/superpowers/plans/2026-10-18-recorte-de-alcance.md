# Recorte de alcance — Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development
> (recomendado) o superpowers:executing-plans para ejecutar este plan tarea por tarea. Los pasos
> usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Goal:** Llevar el proyecto de 257 actividades a 157, marcando cada recorte con la razón y la
medida de éxito que no servía, y producir el documento formal que lo declara.

**Architecture:** Un módulo de datos (`recorte.py`) declara qué sobrevive, qué se recorta y qué
estaba hecho sin registrar, cada entrada con su justificación. Un generador (`gen_recorte.py`)
produce el documento leyendo las cifras del cronograma en tiempo de generación. Un script
aparte marca las actividades recortadas en el XML sin borrarlas.

**Tech Stack:** Python 3 · openpyxl · python-docx · `scripts/neutro.py` · ProjectLibre (MSPDI)

**Spec:** `docs/superpowers/specs/2026-10-18-recorte-de-alcance-design.md`

---

## Mapa de archivos

| Archivo | Responsabilidad |
|---|---|
| `scripts/recorte.py` | Las tres listas con su justificación. Única fuente de verdad del recorte |
| `scripts/gen_recorte.py` | Genera el documento formal |
| `scripts/marcar_recorte.py` | Marca las recortadas en el XML del cronograma |
| `scripts/test_recorte.py` | Pruebas de consistencia de las listas |
| `entregables/10_Recorte_de_Alcance.docx` | El documento con firmas |

**Por qué `recorte.py` separado de `gen_recorte.py`:** las listas son datos que se consultan
desde varios sitios —el documento, el marcado del XML y las pruebas—. Mezclarlas con el
generador obligaría a importar python-docx solo para preguntar si una clave sobrevive.

**Convenciones del proyecto:**
- Las cifras se **leen** del cronograma, nunca se escriben a mano.
- Comentarios en español explicando el porqué.
- Formato de los Word: neutral, con `neutro.py`.
- **Nunca editar el XML del cronograma a mano para cambiar porcentajes.** ProjectLibre usa su
  propio `<Stop>` y al recalcular mueve fechas. Marcar notas sí es seguro; los porcentajes los
  pone la herramienta.

---

### Task 1: `recorte.py` — las listas con su justificación

**Files:**
- Create: `scripts/recorte.py`

- [ ] **Step 1: Escribir el módulo**

Crear `scripts/recorte.py`:

```python
# -*- coding: utf-8 -*-
"""
Qué sobrevive al recorte de alcance, qué se recorta, y qué estaba hecho sin registrar.

Es la única fuente de verdad del recorte. El documento, el marcado del cronograma y las
pruebas leen de aquí; si una clave cambia de lista, cambia en los tres sitios a la vez.

El criterio no es «lo que dio tiempo»: sobrevive lo que sirve a una medida de éxito de la
carta sponsor, y se recorta lo que no sirve a ninguna.
"""

# Las diez medidas de la carta sponsor, con su criterio de verificación resumido.
MEDIDAS = {
    1: "El usuario distingue y alcanza los componentes sin indicación externa",
    2: "El sistema registra el golpe en el componente correcto en ≥95 % de los intentos",
    3: "El sonido reproducido corresponde siempre al componente golpeado",
    4: "El retardo entre golpe y sonido se mantiene por debajo de 30 ms",
    5: "La simulación sostiene 72 fps durante una sesión completa",
    6: "Un usuario sin experiencia comprende el uso sin instrucción escrita",
    7: "El sistema distingue golpe suave, medio y fuerte y modifica el sonido",
    8: "El asesor externo dictamina pertinencia terapéutica de las rutinas",
    9: "El sistema exporta precisión temporal, amplitud y constancia por sesión",
    10: "Ningún participante reporta mareo, fatiga ni molestia articular",
}

MEDIDA_RETIRADA = 8

# Actividades terminadas que el área responsable nunca registró.
#
# Se hicieron desde desarrollo VR mientras se construía la batería, y el área de sonido las
# seguía marcando como bloqueadas. Contarlas como recortadas daría por perdido trabajo real.
YA_HECHAS = {
    "SI.1": "DrumVoice reproduce la muestra de la pieza golpeada",
    "SI.2": "SampleSelector elige la muestra por intensidad, con dinámica timbral",
    "SI.3": "Audio 2D por decisión de diseño: la espacialización cuesta y no aporta aquí",
    "SI.4": "Medido en el hito Go/No-Go: p90 de +4.07 ms",
    "SE.1": "Las 82 muestras no tienen silencio inicial",
    "SE.3": "Ganancia de normalización por muestra, calculada al analizar el kit",
    "SE.4": "48 kHz, mono, PCM: el formato nativo del visor",
    "SB.1": "Bombo del pack Dustyroom, CC BY 4.0",
    "SB.2": "Tarola del mismo pack",
    "SB.3": "Dos toms del mismo pack",
    "SB.4": "Hi-hat del mismo pack",
    "SB.6": "Tres niveles por pieza, desde la velocidad de la baqueta",
}

# Lo que sobrevive, con la medida de éxito a la que sirve.
SOBREVIVEN = {
    # Entorno 3D — el área deja de modelar y pasa a integrar
    "AA.3": (None, "Assets de entorno con licencia libre. Sin esto no hay escenario"),
    "AA.4": (None, "Revisar licencias. Obligación legal, no opcional"),
    "AL.2": (6,    "Iluminación: un escenario oscuro no se entiende sin instrucción"),
    "AP.1": (1,    "Composición del escenario con los assets"),
    "AO.5": (5,    "Medir FPS en el visor. Es la medida 5 y hoy está sin verificar"),
    "AS":   (10,   "Límites visuales de seguridad del espacio de interacción"),

    # Sonido — solo falta una pieza del kit
    "SB.5": (3,    "Falta el crash. El pack no incluye ninguno"),

    # Música — lo mínimo que alimenta un beatmap real
    "MP.1": (None, "Una pista de prueba con licencia"),
    "MP.2": (None, "Su BPM exacto. Un BPM aproximado desincroniza a los pocos compases"),
    "MP.3": (None, "Su estructura: dónde cae el primer beat y el compás"),
    "MB.1": (None, "El patrón de batería de esa pista"),
    "MB.4": (None, "Convertir el patrón en beatmap"),

    # Interfaz — solo el flujo que se demuestra
    "II.2": (6,    "Menú principal dentro de Unity"),
    "II.3": (6,    "Interacción con botones por mando"),
    "II.6": (9,    "Pantalla de resultados: es donde se ven las métricas"),
    "IR.1": (6,    "Legibilidad en el visor. El análisis ya existe; falta corregir"),
    "IR.2": (6,    "Tamaño, distancia y posición de los paneles"),
    "IT.1": (6,    "Tutorial: cómo sujetar las baquetas"),
    "IT.2": (6,    "Tutorial: cómo seguir el ritmo"),
    "IT.4": (6,    "Implementar el flujo del tutorial"),

    # QA — el informe final ES la entrega
    "QB.1": (None, "Build candidata"),
    "QB.2": (None, "Probarla en el visor"),
    "QB.3": (None, "Corregir lo crítico"),
    "QB.4": (None, "Versión definitiva"),
    "QC.1": (None, "Registro de versiones"),
    "QC.4": (None, "Registro de assets y licencias. Obligación legal"),
    "QE.2": (None, "Registrar lo que reporten los usuarios"),
    "QE.3": (None, "Clasificar por gravedad"),
    "QE.4": (None, "Asignar a su área"),
    "QE.5": (None, "Verificar la corrección de lo crítico"),
    "QG.2": (None, "Acciones de mitigación por riesgo"),
    "QI.1": (None, "Analizar los resultados de las pruebas"),
    "QI.2": (None, "Redactar resultados"),
    "QI.3": (None, "Redactar conclusiones y limitaciones"),
    "QI.4": (None, "Integrar el informe"),
    "QI.5": (None, "Revisión final de redacción y formato"),
    "QM.1": (6,    "Manual de usuario"),
    "QM.2": (None, "Manual técnico de instalación"),
    "QT.1": (2,    "Plan de pruebas de la batería: es donde se mide el 95 %"),
    "QT.6": (2,    "Ejecutar las pruebas de batería"),
    "QT.7": (None, "Pruebas del sistema de ritmo"),
    "QT.8": (6,    "Pruebas con usuarios del prototipo"),
    "QV.1": (None, "Sesión completa de principio a fin"),
    "QV.2": (5,    "Estabilidad y cierres inesperados"),
    "QV.3": (5,    "Medir FPS"),
    "QV.4": (4,    "Evaluar la latencia en la build final"),
    "QV.5": (10,   "Comodidad de la experiencia"),
    "QX":   (None, "Presentación y demostración final"),

    # Desarrollo VR
    "DT.4": (None, "Incorporar el modelo 3D cuando llegue del área de entorno"),
    "DT.5": (None, "Reajustar los planos de golpe a ese modelo"),

    # Experiencia emocional
    "ET.2": (None, "Actualizar la fundamentación a lo que el prototipo realmente mide"),
}

# Actividad que NO existía en el plan original y se añade.
#
# Es el único sitio donde este recorte suma alcance, y la razón es la desproporción: el
# marcador del juego de ritmo ya calcula precisión temporal y constancia del pulso, así que
# volcarlas a un archivo cierra la medida 9, que hoy está en cero.
NUEVAS = {
    "DM.1": (9, "Exportar las métricas de sesión a JSON: precisión temporal y constancia"),
}

# Lo que se recorta, agrupado por la razón.
RECORTADAS = {
    # --- Entorno 3D: el área deja de modelar ---
    "AA.1": "Catálogo de assets. Se buscan directamente los que se van a usar",
    "AA.2": "Límites de polígonos. Ya están escritos en el diseño técnico del proyecto",
    "AB.1": "Modelo de batería. El kit de primitivas ya funciona y está medido",
    "AB.2": "Depende de AB.1",
    "AB.3": "Modelos de baquetas. Las actuales cumplen",
    "AB.4": "Depende de AB.1",
    "AB.5": "Depende de AB.1",
    "AB.6": "Depende de AB.1",
    "AC.1": "Teoría del color. YA EXISTE el documento de paleta del equipo",
    "AC.2": "La paleta ya está definida en ese documento",
    "AC.3": "Moodboard. No sirve a ninguna medida",
    "AD.1": "Elementos ambientales secundarios",
    "AD.2": "Depende de AD.1",
    "AE.1": "Investigar tipo de entorno. Se decide al elegir los assets",
    "AE.2": "Comparar ambientes. Misma razón",
    "AE.3": "Dirección artística. Misma razón",
    "AO.1": "Optimizar texturas. Se cubre eligiendo assets ya optimizados",
    "AO.2": "LOD. Innecesario con una escena de pocos objetos",
    "AO.3": "Revisar luces en tiempo real. Se cubre en AL.2",
    "AO.4": "Iluminación horneada. Se cubre en AL.2",
    "AO.6": "Optimizar hasta cumplir. Se cubre en AO.5 si la medición falla",
    "AP.2": "Posición del jugador. Ya resuelta: el kit está medido y calibrado",
    "AP.3": "Aplicar la paleta. Se cubre al componer en AP.1",
    "AR.1": "Revisión cruzada con experiencia emocional",
    "AR.2": "Ajustes finales de ambientación",

    # --- Sonido ---
    "SA.1": "Sonidos ambientales del escenario",
    "SA.2": "Depende de SA.1",
    "SC.1": "Controles de volumen por canal. Ninguna medida los pide",
    "SC.2": "Mezcla general. Misma razón",
    "SE.2": "Eliminar ruidos. Las muestras del pack vienen limpias",
    "SM.1": "AUDIO MIXER: añade un nodo al camino del audio y obligaría a remedir la "
            "latencia, que es la medida 4 y la única ya ganada con margen",
    "SM.2": "Depende de SM.1",
    "SP.2": "Investigar bancos de sonidos. El pack actual ya cubre el kit",
    "SU":   "Sonidos de interfaz",

    # --- Música ---
    "MA.1": "Pistas adicionales. Con una basta para demostrar",
    "MA.2": "Pistas para modo libre. El modo libre se recortó en R14",
    "MB.2": "Momentos de intensidad en el patrón",
    "MB.3": "Tres versiones de dificultad. Las dificultades se recortaron en R14",
    "MB.5": "Probar el beatmap con el desarrollador. Se cubre en QT.7",
    "MB.6": "Corregir patrones. Requiere iteración que no cabe",
    "MN.1": "Normalizar todas las pistas. Solo hay una",
    "MR.1": "Investigar características musicales",
    "MR.2": "Analizar BPM de referencias",
    "MR.3": "Analizar compases para principiantes",
    "MR.4": "Definir estilos musicales. Se recorta a una pista",
    "MR.5": "Definir duración de las pistas",

    # --- Interfaz ---
    "IE":   "Estilo visual general. Las pantallas ya existen como diseño",
    "II.1": "Importar recursos de Canva/Figma. Se implementa directo en Unity",
    "II.4": "Configuración de volumen. Depende de los canales recortados en SC",
    "II.5": "Menú de pausa. La pausa se recortó en R14",
    "IR.3": "Corregir navegación tras pruebas. Requiere iteración que no cabe",
    "IS.1": "Selección de canción y dificultad. Hay una canción y no hay dificultades",
    "IS.2": "Diseñar menú de configuración",
    "IS.3": "Diseñar controles de volumen. Depende de SC",
    "IS.4": "Diseñar menú de pausa. Depende de II.5",
    "IS.5": "Pantalla de confirmación de salida",
    "IS.6": "Diseñar resultados. La pantalla ya existe como prototipo",
    "IW.4": "Wireframe del tutorial. Se implementa directo",
    "IW.6": "Wireframe de resultados. Ya existe como prototipo",

    # --- QA ---
    "QD.1": "Documentación de arquitectura. YA EXISTEN la guía de 8 capítulos y los specs",
    "QD.2": "Diagrama de flujo. Se cubre en el informe final",
    "QD.3": "Documentar detección de golpes. Está en la guía y en el spec",
    "QD.4": "Documentar el juego de ritmo. Está en su spec y su plan",
    "QD.5": "Documentar intensidad. Está en la guía",
    "QD.6": "Documentar el entorno. El entorno se recortó a integración",
    "QD.7": "Documentar la música. Se cubre con MP.3",
    "QD.8": "Documentar la interfaz. Se cubre en el informe final",
    "QF.1": "Capturas de pantalla. Se obtienen al preparar QX",
    "QF.2": "Video de evidencia. Misma razón",
    "QT.2": "Plan de pruebas del juego de ritmo. Se cubre con QT.7",
    "QT.3": "Plan de pruebas de interfaz. Se cubre con QT.8",
    "QT.4": "Plan de pruebas de audio. La latencia ya se midió con su protocolo",
    "QT.5": "Plan de pruebas de rendimiento. Se cubre con QV.3",

    # --- Desarrollo VR ---
    "DB.2": "Baquetas interactuables. Van solidarias al control, decisión del acta",
    "DB.4": "Física de baquetas. No hay física que ajustar",
    "DO":   "Agarrar y soltar objetos. Misma decisión del acta",
    "DT.3": "Colliders por componente. La detección es por plano armado",

    # --- Juego de ritmo: ya recortadas por R14 ---
    "JC.1": "Cuenta regresiva. Recortada en R14; los compases de entrada la cubren",
    "JC.2": "Pausa y reanudación. Recortada en R14",
    "JC.3": "Reiniciar actividad. Recortada en R14",
    "JC.4": "Abandonar actividad. Recortada en R14",
    "JF.1": "Feedback visual. Lo cubre JudgePopup",
    "JF.2": "Feedback auditivo. La batería ya suena al golpear",
    "JI.2": "Sustituir teclado por VR. El teclado nunca se construyó",
    "JI.3": "Intensidad dentro del juego. DrumHit ya la lleva",
    "JI.4": "Mecánicas por intensidad. Recortada en R14",
    "JI.5": "Integrar con el flujo general. Depende de los menús",
    "JK":   "Sistema de teclado. Sin objeto: la interacción VR ya existe",
    "JL.1": "Niveles de dificultad. Recortada en R14",
    "JL.2": "Selección de dificultad. Depende de JL.1",
    "JM.1": "Modo libre. La batería ya es tocable fuera del juego",
    "JM.2": "Música de fondo en modo libre. Depende de JM.1",
    "JM.3": "Tocar sin música. Depende de JM.1",
    "JP.2": "Combo. Recortada en R14",
    "JP.4": "Resumen de resultados. Lo cubre II.6",
    "JW.3": "Detectar golpes anticipados por separado. Se registran como fallo",
    "JW.4": "Detectar golpes atrasados por separado. Misma razón",
    "JW.6": "Ajustar ventanas tras pruebas. Requiere iteración que no cabe",
    "JY":   "Calibración de latencia. Ya resuelta: p90 de +4.07 ms",
}


def resumen():
    """Cifras del recorte, calculadas de las listas. Nunca escritas a mano."""
    return dict(
        ya_hechas=len(YA_HECHAS),
        sobreviven=len(SOBREVIVEN),
        nuevas=len(NUEVAS),
        recortadas=len(RECORTADAS),
    )


if __name__ == "__main__":
    r = resumen()
    for k, v in r.items():
        print(f"  {k:12s} {v}")
    print(f"  {'suma 257':12s} "
          f"{r['ya_hechas'] + r['sobreviven'] + r['recortadas']} + 93 hechas previas")
```

- [ ] **Step 2: Correr el módulo**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python scripts/recorte.py
```

Expected:
```
  ya_hechas    12
  sobreviven   51
  nuevas       1
  recortadas   101
  suma 257     164 + 93 hechas previas
```

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add scripts/recorte.py
git commit -m "feat: listas del recorte de alcance con su justificacion

Unica fuente de verdad del recorte: el documento, el marcado del cronograma y las pruebas leen
de aqui. Cada clave recortada lleva escrito POR QUE, y cada superviviente la medida de exito a
la que sirve.

Doce actividades de sonido van en su propia lista: estan terminadas y el area nunca las
registro. Contarlas como recortadas daria por perdido trabajo real.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: Pruebas de consistencia de las listas

Un error en las listas no se ve al leerlas: una clave repetida en dos listas, o una que no
existe en el cronograma, produce un documento que afirma algo falso.

**Files:**
- Create: `scripts/test_recorte.py`

- [ ] **Step 1: Escribir las pruebas que fallan**

Crear `scripts/test_recorte.py`:

```python
# -*- coding: utf-8 -*-
"""
Consistencia de las listas del recorte.

Un error aquí no se ve leyendo: una clave en dos listas a la vez, o una que no existe en el
cronograma, produce un documento que afirma algo falso con toda seriedad.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recorte
import validacion


def test_ninguna_clave_en_dos_listas():
    ya = set(recorte.YA_HECHAS)
    sob = set(recorte.SOBREVIVEN)
    rec = set(recorte.RECORTADAS)
    nue = set(recorte.NUEVAS)

    assert not (ya & sob), f"en YA_HECHAS y SOBREVIVEN: {ya & sob}"
    assert not (ya & rec), f"en YA_HECHAS y RECORTADAS: {ya & rec}"
    assert not (sob & rec), f"en SOBREVIVEN y RECORTADAS: {sob & rec}"
    assert not (nue & (ya | sob | rec)), f"NUEVAS choca: {nue & (ya | sob | rec)}"


def test_las_listas_cubren_todo_lo_pendiente():
    """Cada actividad pendiente del cronograma tiene que estar en exactamente una lista."""
    f = validacion.fusion()
    pendientes = {k for k, t in f.items() if not t["hecha"]}
    clasificadas = set(recorte.YA_HECHAS) | set(recorte.SOBREVIVEN) | set(recorte.RECORTADAS)

    sin_clasificar = pendientes - clasificadas
    assert not sin_clasificar, \
        f"{len(sin_clasificar)} pendientes sin clasificar: {sorted(sin_clasificar)}"


def test_no_se_clasifica_algo_que_no_existe():
    """Una clave inventada produciría un documento que habla de trabajo imaginario."""
    f = validacion.fusion()
    clasificadas = set(recorte.YA_HECHAS) | set(recorte.SOBREVIVEN) | set(recorte.RECORTADAS)

    inexistentes = clasificadas - set(f)
    assert not inexistentes, f"claves que no están en el cronograma: {sorted(inexistentes)}"


def test_no_se_clasifica_algo_ya_terminado():
    """Recortar una actividad terminada sería borrar trabajo hecho."""
    f = validacion.fusion()
    hechas = {k for k, t in f.items() if t["hecha"]}

    choque = hechas & set(recorte.RECORTADAS)
    assert not choque, f"actividades terminadas marcadas como recortadas: {sorted(choque)}"


def test_cada_recortada_tiene_razon():
    vacias = [k for k, v in recorte.RECORTADAS.items() if not v or len(v.strip()) < 10]
    assert not vacias, f"recortadas sin razón escrita: {vacias}"


def test_cada_superviviente_tiene_justificacion():
    malas = [k for k, (m, j) in recorte.SOBREVIVEN.items() if not j or len(j.strip()) < 10]
    assert not malas, f"supervivientes sin justificación: {malas}"


def test_las_medidas_citadas_existen():
    citadas = {m for m, _ in recorte.SOBREVIVEN.values() if m is not None}
    citadas |= {m for m, _ in recorte.NUEVAS.values() if m is not None}
    assert citadas <= set(recorte.MEDIDAS), \
        f"medidas citadas que no existen: {citadas - set(recorte.MEDIDAS)}"


def test_la_medida_retirada_no_la_sirve_nadie():
    """Si una actividad sirviera a la medida 8, retirarla sería incoherente."""
    sirven = [k for k, (m, _) in recorte.SOBREVIVEN.items() if m == recorte.MEDIDA_RETIRADA]
    assert not sirven, \
        f"estas sobreviven sirviendo a la medida retirada: {sirven}"
```

- [ ] **Step 2: Correr para verificar**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python -m pytest scripts/test_recorte.py -v 2>&1 | tail -15
```

Expected: 8 pruebas. Si alguna falla, **el mensaje dice exactamente qué clave sobra o falta** —
arreglar `recorte.py` hasta que pasen las ocho.

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add scripts/test_recorte.py
git commit -m "test: consistencia de las listas del recorte

Un error en las listas no se ve leyendolas: una clave en dos listas a la vez, o una que no
existe en el cronograma, produce un documento que afirma algo falso con toda seriedad.

Se comprueba que las listas cubren TODO lo pendiente y nada mas, que ninguna clave esta en dos,
que no se recorta nada ya terminado, y que ninguna superviviente sirve a la medida que el
documento retira.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: El documento formal

**Files:**
- Create: `scripts/gen_recorte.py`

- [ ] **Step 1: Escribir el generador**

Crear `scripts/gen_recorte.py`:

```python
# -*- coding: utf-8 -*-
"""Genera el documento de recorte de alcance."""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import neutro
import recorte
import validacion

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")
HOY = "18 de octubre de 2026"

AREAS = {
    "D": "Desarrollo VR y batería", "J": "Juego de ritmo", "Q": "QA y gestión",
    "E": "Experiencia emocional", "S": "Sonido", "M": "Música",
    "I": "Interfaz", "A": "Entorno 3D",
}


def por_area(claves):
    d = collections.Counter(k[0] for k in claves)
    return {AREAS.get(a, a): n for a, n in sorted(d.items(), key=lambda kv: -kv[1])}


def doc():
    f = validacion.fusion()
    hechas_previas = sum(1 for t in f.values() if t["hecha"])
    r = recorte.resumen()

    hechas = hechas_previas + r["ya_hechas"]
    total_nuevo = hechas + r["sobreviven"] + r["nuevas"]

    d = neutro.nuevo()
    neutro.portada(
        d,
        "Recorte de alcance del proyecto",
        "Simulación de Batería en Realidad Virtual con Enfoque Terapéutico",
        [("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Facultad", "Ingeniería Mecánica y Eléctrica, UANL"),
         ("Docente", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Fecha", HOY),
         ("Proceso", "PMBOK 4.6 Control Integrado de Cambios · 5.6 Controlar el Alcance")],
    )

    # ---------------------------------------------------------------- 1
    neutro.H(d, "1. Por qué se recorta", 1)
    neutro.P(d,
             f"El proyecto registra {hechas_previas} de 257 actividades terminadas con "
             "diecinueve días hábiles hasta el cierre del periodo. Al ritmo actual no cabe, y "
             "el hueco no se reparte parejo: dos áreas están cerradas y tres apenas han "
             "arrancado.")
    neutro.table(
        d, ["Área", "Terminadas", "Total", "Avance"],
        [[AREAS[p],
          str(sum(1 for t in f.values() if t["clave"][0] == p and t["hecha"])),
          str(sum(1 for t in f.values() if t["clave"][0] == p)),
          f"{100.0 * sum(1 for t in f.values() if t['clave'][0] == p and t['hecha']) / max(1, sum(1 for t in f.values() if t['clave'][0] == p)):.0f} %"]
         for p in AREAS],
        widths=[6.0, 3.4, 3.0, 3.6], fs=9.0,
    )
    neutro.P(d,
             "La cadena de Entorno 3D tiene diecisiete actividades estrictamente seriales en "
             "una sola persona. Diecisiete tareas en fila dentro de diecinueve días hábiles "
             "exigen una por día sin un solo tropiezo, y la cadena lleva seis semanas sin "
             "arrancar. No es un retraso recuperable.")

    # ---------------------------------------------------------------- 2
    neutro.H(d, "2. El criterio", 1)
    neutro.P(d,
             "Sobrevive lo que sirve a una medida de éxito. Se recorta lo que no sirve a "
             "ninguna.", bold=True)
    neutro.P(d,
             "El criterio no es «lo que dio tiempo». La carta del patrocinador comprometió "
             "diez resultados verificables, no doscientas cincuenta y siete tareas: las tareas "
             "eran el camino, las medidas son el destino. Recortar contra las medidas se "
             "defiende; recortar contra el reloj, no.")
    neutro.table(
        d, ["#", "Medida de éxito", "Estado"],
        [["1", recorte.MEDIDAS[1], "Cumplida: seis piezas con indicador"],
         ["2", recorte.MEDIDAS[2], "Funciona; falta la medición formal"],
         ["3", recorte.MEDIDAS[3], "Cumplida"],
         ["4", recorte.MEDIDAS[4], "Cumplida y medida: p90 de +4.07 ms"],
         ["5", recorte.MEDIDAS[5], "Sin medir"],
         ["6", recorte.MEDIDAS[6], "Requiere pruebas con usuarios"],
         ["7", recorte.MEDIDAS[7], "Cumplida: tres niveles"],
         ["8", recorte.MEDIDAS[8], "SE RETIRA. Ver sección 5"],
         ["9", recorte.MEDIDAS[9], "A un paso. Ver sección 4"],
         ["10", recorte.MEDIDAS[10], "Requiere pruebas con usuarios"]],
        widths=[0.8, 8.4, 6.8], fs=8.0,
    )

    # ---------------------------------------------------------------- 3
    neutro.H(d, "3. El recorte", 1)
    neutro.table(
        d, ["Concepto", "Actividades"],
        [["Terminadas y ya registradas", str(hechas_previas)],
         ["Terminadas que el área no había registrado", str(r["ya_hechas"])],
         ["Sobreviven al recorte", str(r["sobreviven"])],
         ["Se recortan", str(r["recortadas"])],
         ["Se añaden", str(r["nuevas"])],
         ["TOTAL ANTERIOR", "257"],
         ["TOTAL NUEVO", str(total_nuevo)]],
        widths=[10.0, 6.0], fs=9.5, negritas_col0=True,
    )
    neutro.P(d)
    neutro.P(d, "Sobre el porcentaje de avance", bold=True)
    neutro.P(d,
             f"El avance pasa de {100.0 * hechas_previas / 257:.0f} % a "
             f"{100.0 * hechas / total_nuevo:.0f} %. Conviene decir con claridad de dónde sale "
             "ese salto, porque leído solo se parece demasiado a maquillaje.")
    neutro.P(d,
             f"El numerador sube de {hechas_previas} a {hechas} por una razón acotada: "
             f"{r['ya_hechas']} actividades de sonido estaban terminadas y no se habían "
             f"registrado. El resto del salto es del denominador, que baja de 257 a "
             f"{total_nuevo} por la decisión que este documento declara. El proyecto no avanzó "
             "de golpe: dejó de medirse contra trabajo que nunca se iba a hacer.",
             italic=True)

    neutro.H(d, "3.1 Trabajo terminado que no estaba registrado", 2)
    neutro.P(d,
             "Se hizo desde desarrollo VR mientras se construía la batería, y el área que lo "
             "tenía asignado seguía marcándolo como bloqueado. Contarlo como recortado daría "
             "por perdido trabajo real.")
    neutro.table(
        d, ["Clave", "Por qué está terminada"],
        [[k, v] for k, v in sorted(recorte.YA_HECHAS.items())],
        widths=[2.0, 14.0], fs=8.0,
    )

    neutro.H(d, "3.2 Reparto del recorte por área", 2)
    neutro.table(
        d, ["Área", "Sobreviven", "Se recortan"],
        [[a, str(por_area(recorte.SOBREVIVEN).get(a, 0)),
          str(por_area(recorte.RECORTADAS).get(a, 0))]
         for a in AREAS.values()],
        widths=[7.0, 4.5, 4.5], fs=9.0,
    )

    # ---------------------------------------------------------------- 4
    neutro.H(d, "4. Qué sobrevive, y a qué medida sirve", 1)
    neutro.table(
        d, ["Clave", "Medida", "Justificación"],
        [[k, str(m) if m else "—", j]
         for k, (m, j) in sorted(recorte.SOBREVIVEN.items())],
        widths=[1.6, 1.4, 13.0], fs=7.5,
    )
    neutro.H(d, "4.1 La única actividad que se añade", 2)
    neutro.P(d,
             "La medida 9 pide exportar por sesión precisión temporal, amplitud de movimiento "
             "y constancia del pulso. El marcador del juego de ritmo ya calcula la precisión "
             "temporal y la constancia; falta volcarlas a un archivo.")
    neutro.table(
        d, ["Clave", "Medida", "Actividad"],
        [[k, str(m), j] for k, (m, j) in recorte.NUEVAS.items()],
        widths=[1.6, 1.4, 13.0], fs=8.5,
    )
    neutro.P(d,
             "Es el único punto donde este documento añade alcance mientras recorta. La razón "
             "es la desproporción: una actividad de trabajo cierra una medida que hoy está "
             "en cero.", italic=True)

    # ---------------------------------------------------------------- 5
    neutro.H(d, "5. La medida 8 se retira", 1)
    neutro.P(d,
             "El asesor terapéutico externo tenía fecha límite de confirmación el 10 de "
             "septiembre y nunca se concretó. No es cuestión de tiempo disponible: sin asesor "
             "no hay dictamen, y sin dictamen la medida no se puede verificar por ningún "
             "camino.")
    neutro.P(d, "Se declara retirada. En su lugar:")
    neutro.bullets(d, [
        "El respaldo terapéutico se apoya en protocolos publicados de Neurologic Music "
        "Therapy, citados en el documento de fundamentación.",
        "La ausencia de validación terapéutica externa se documenta como limitación "
        "explícita del proyecto, en el informe final y en la presentación.",
        "El proyecto no se presenta como tratamiento de ninguna condición de salud.",
    ])
    neutro.P(d,
             "Es exactamente la contingencia que el acta constitutiva había previsto para este "
             "caso. Que el plan anticipara el fallo y nombrara la salida es, en sí mismo, "
             "evidencia de gestión.", italic=True)

    # ---------------------------------------------------------------- 6
    neutro.H(d, "6. Qué se recorta, y por qué", 1)
    neutro.P(d,
             "Ninguna actividad se borra del cronograma. Se marcan como fuera de alcance con "
             "la razón escrita, de modo que el recorte quede auditable: una actividad borrada "
             "no deja rastro de que existió ni de por qué se quitó.")
    for pref, nombre in AREAS.items():
        claves = sorted(k for k in recorte.RECORTADAS if k[0] == pref)
        if not claves:
            continue
        neutro.H(d, f"6.{list(AREAS).index(pref) + 1} {nombre} — {len(claves)}", 2)
        neutro.table(
            d, ["Clave", "Razón"],
            [[k, recorte.RECORTADAS[k]] for k in claves],
            widths=[1.8, 14.2], fs=7.5,
        )

    # ---------------------------------------------------------------- 7
    neutro.H(d, "7. Lo que el proyecto sigue comprometiendo", 1)
    neutro.P(d,
             "Nueve de las diez medidas de éxito siguen en pie. El recorte reduce el camino, "
             "no el destino.")
    neutro.bullets(d, [
        "Una batería de seis piezas tocable en realidad virtual, que identifica la pieza "
        "golpeada y distingue tres niveles de intensidad.",
        "Latencia por debajo del umbral comprometido, medida y documentada.",
        "Un juego de ritmo que mide la precisión temporal del usuario contra un patrón.",
        "Exportación de métricas por sesión.",
        "Un entorno funcional, optimizado al presupuesto de rendimiento del visor.",
        "Pruebas con usuarios que respalden las medidas de interacción y seguridad.",
        "El informe final completo, conforme a PMBOK.",
    ])

    # ---------------------------------------------------------------- 8
    neutro.H(d, "8. Acuerdos y firmas", 1)
    neutro.P(d, "El equipo acuerda lo contenido en este documento:")
    neutro.bullets(d, [
        f"El alcance del proyecto pasa de 257 a {total_nuevo} actividades.",
        "La medida de éxito 8 se retira, con la sustitución descrita en la sección 5.",
        "Las actividades recortadas se conservan en el cronograma marcadas como fuera de "
        "alcance, no se borran.",
        "El recorte se comunica a la docente como parte del informe de avance.",
    ])
    neutro.P(d)
    neutro.table(
        d, ["Rol", "Nombre", "Firma"],
        [["Dirección de proyecto", "Sarai Galindo García", "_" * 26],
         ["Gerencia de proyecto", "Abiud Misael Benítez Franco", "_" * 26],
         ["QA y documentación", "Diana Laura Tello Salinas", "_" * 26],
         ["Entorno 3D", "Kimberly González Sepúlveda", "_" * 26],
         ["Sonido", "Christian Salvador Valadez Gallegos", "_" * 26],
         ["Música", "Javier Alejandro Hernández Caloca", "_" * 26],
         ["Experiencia emocional", "María Fernanda Montoya Valdez", "_" * 26]],
        widths=[4.4, 6.6, 5.0], fs=9.0,
    )
    neutro.P(d)
    neutro.P(d, "Fecha del acuerdo: " + "_" * 30)
    neutro.P(d)
    neutro.P(d, "Visto bueno de la docente: " + "_" * 30)

    ruta = os.path.join(SALIDA, "10_Recorte_de_Alcance.docx")
    d.save(ruta)
    return ruta, total_nuevo, hechas


if __name__ == "__main__":
    ruta, total, hechas = doc()
    print(f"  {os.path.basename(ruta)}")
    print(f"    {hechas} de {total} ({100.0 * hechas / total:.0f} %)")
```

- [ ] **Step 2: Generar y verificar**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python scripts/gen_recorte.py
~/.pyenv/versions/redes/bin/python -c "
import docx
d = docx.Document('entregables/10_Recorte_de_Alcance.docx')
txt = ' '.join(p.text for p in d.paragraphs)
celdas = ' '.join(c.text for t in d.tables for r in t.rows for c in r.cells)
todo = txt + ' ' + celdas
print(f'  parrafos {len(d.paragraphs)} · tablas {len(d.tables)}')
for k in ('157','105','4.07','medida 8','Audio Mixer','Neurologic'):
    print(f\"    '{k}': {'si' if k in todo else 'NO'}\")
"
```

Expected: el documento abre, y las seis comprobaciones salen «si».

- [ ] **Step 3: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add scripts/gen_recorte.py entregables/10_Recorte_de_Alcance.docx
git commit -m "feat: documento de recorte de alcance

Control integrado de cambios sobre el alcance. Cada recorte lleva escrito por que, y cada
superviviente la medida de exito a la que sirve.

Declara sin rodeos de donde sale el salto del porcentaje: doce actividades que estaban hechas
sin registrar suben el numerador, y el recorte baja el denominador. Un porcentaje que sube sin
explicacion destruye la credibilidad del resto del documento.

Retira formalmente la medida 8, que no se puede verificar sin el asesor que nunca llego, y
documenta la sustitucion que el acta ya habia previsto.

Las cifras se leen del cronograma en tiempo de generacion.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: Marcar las recortadas en el cronograma

**Files:**
- Create: `scripts/marcar_recorte.py`

- [ ] **Step 1: Escribir el marcador**

Crear `scripts/marcar_recorte.py`:

```python
# -*- coding: utf-8 -*-
"""
Marca las actividades recortadas en el cronograma, sin borrarlas.

NO SE BORRAN. Una actividad borrada no deja rastro de que existió ni de por qué se quitó, y
el valor de este recorte está justamente en que sea auditable.

Se escribe la razón en el campo de notas de cada tarea. NO se tocan los porcentajes ni las
fechas: ProjectLibre usa su propio <Stop> para el avance y al recalcular mueve fechas; editar
eso a mano ya costó tres intentos entenderlo.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recorte

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "entregables", "Cronograma_ProjectLibre.xml")
MARCA = "[FUERA DE ALCANCE]"


def clave(nombre):
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre)
    return m.group(1) if m else None


def escapar(t):
    """XML seguro: una razón con & o < rompería el archivo en silencio."""
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def marcar():
    with open(RUTA, encoding="utf-8", errors="ignore") as fh:
        s = fh.read()

    marcadas = []

    def arregla(m):
        t = m.group(1)
        nm = re.search(r"<Name>(.*?)</Name>", t)
        if not nm:
            return m.group(0)
        k = clave(nm.group(1))
        if k not in recorte.RECORTADAS:
            return m.group(0)
        if MARCA in t:
            return m.group(0)

        nota = f"{MARCA} {recorte.RECORTADAS[k]}"

        if "<Notes>" in t:
            t = re.sub(r"<Notes>.*?</Notes>", f"<Notes>{escapar(nota)}</Notes>", t, flags=re.S)
        else:
            # Notes va justo después de Name en el esquema MSPDI.
            t = t.replace(nm.group(0), nm.group(0) + f"\n\t\t\t<Notes>{escapar(nota)}</Notes>", 1)

        marcadas.append(k)
        return "<Task>" + t + "</Task>"

    s2 = re.sub(r"<Task>(.*?)</Task>", arregla, s, flags=re.S)

    with open(RUTA, "w", encoding="utf-8") as fh:
        fh.write(s2)

    return marcadas


if __name__ == "__main__":
    ms = marcar()
    print(f"  {len(ms)} actividades marcadas como fuera de alcance")
    print(f"  esperadas: {len(recorte.RECORTADAS)}")
    faltan = set(recorte.RECORTADAS) - set(ms)
    if faltan:
        print(f"  NO ENCONTRADAS EN EL CRONOGRAMA: {sorted(faltan)}")
```

- [ ] **Step 2: Respaldar el cronograma antes de tocarlo**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
cp entregables/Cronograma_ProjectLibre.xml /tmp/Cronograma_ANTES_RECORTE.xml
echo "respaldo en /tmp/Cronograma_ANTES_RECORTE.xml"
```

- [ ] **Step 3: Marcar y verificar que el XML sigue válido**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python scripts/marcar_recorte.py
~/.pyenv/versions/redes/bin/python -c "
import xml.etree.ElementTree as ET, re, pathlib
p = 'entregables/Cronograma_ProjectLibre.xml'
ET.parse(p)
print('  XML bien formado')
s = pathlib.Path(p).read_text(errors='ignore')
print(f\"  marcas [FUERA DE ALCANCE]: {s.count('[FUERA DE ALCANCE]')}\")
NS = '{http://schemas.microsoft.com/project}'
r = ET.parse(p).getroot()
c = sum(1 for t in r.iter(NS+'Task')
        if (pc := t.find(NS+'PercentComplete')) is not None and pc.text == '100')
print(f'  al 100%: {c}  (deben seguir siendo 93)')
"
```

Expected: XML bien formado, 101 marcas, y **93 al 100 %** — el marcado no debe tocar ningún
porcentaje.

- [ ] **Step 4: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add scripts/marcar_recorte.py entregables/Cronograma_ProjectLibre.xml
git commit -m "chore(cronograma): marcar las 101 actividades fuera de alcance

No se borran. Una actividad borrada no deja rastro de que existio ni de por que se quito, y el
valor del recorte esta justamente en que sea auditable: la razon queda escrita en el campo de
notas de cada tarea.

No se tocan porcentajes ni fechas. ProjectLibre usa su propio Stop para el avance y al
recalcular mueve fechas; editar eso a mano ya costo tres intentos entenderlo.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 5: Excluir las recortadas del conteo de avance

**Files:**
- Modify: `scripts/validacion.py`

- [ ] **Step 1: Añadir la exclusión**

En `scripts/validacion.py`, añadir al final de la función `resumen()`, justo antes del
`return`, y cambiar ese return:

```python
    # Las recortadas salen del denominador: medir el avance contra trabajo cancelado daría un
    # porcentaje que no significa nada. Se importa aquí y no arriba para que validacion.py
    # siga funcionando si recorte.py no existe todavía.
    try:
        import recorte
        fuera = set(recorte.RECORTADAS)
    except ImportError:
        fuera = set()

    vigentes = {k: v for k, v in f.items() if k not in fuera}
    hechas_v = [t for t in vigentes.values() if t["hecha"]]

    return dict(
        total=len(vigentes),
        hechas=len(hechas_v),
        pct=100.0 * len(hechas_v) / max(len(vigentes), 1),
        total_original=len(f),
        recortadas=len(fuera),
        por_responsable=dict(sorted(por_resp.items(), key=lambda kv: -kv[1]["hechas"])),
        por_area=dict(sorted(por_area.items(), key=lambda kv: -kv[1])),
        desfase=sorted(t["clave"] for t in f.values()
                       if t["hecha"] and t["estado_hoja"] != "Completado"),
    )
```

- [ ] **Step 2: Verificar el nuevo conteo**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python -c "
import sys; sys.path.insert(0,'scripts')
import validacion
r = validacion.resumen()
print(f\"  vigentes: {r['hechas']} de {r['total']} ({r['pct']:.0f} %)\")
print(f\"  recortadas fuera del conteo: {r['recortadas']}\")
print(f\"  total original: {r['total_original']}\")
"
```

Expected:
```
  vigentes: 93 de 156 (60 %)
  recortadas fuera del conteo: 101
  total original: 257
```

Nota: aquí sale 93 y no 105 porque las doce de sonido todavía no están marcadas al 100 % en el
cronograma. Eso lo hace el equipo desde ProjectLibre, no este plan.

- [ ] **Step 3: Verificar que la carta de validación sigue generándose**

`gen_validacion.py` lee de `resumen()`, así que el cambio lo afecta.

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
~/.pyenv/versions/redes/bin/python scripts/gen_validacion.py
```

Expected: genera sin error y reporta la cifra nueva.

- [ ] **Step 4: Commit**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add scripts/validacion.py entregables/07_Carta_Validacion_Entregables.docx
git commit -m "feat: excluir las recortadas del conteo de avance

Medir el avance contra trabajo cancelado da un porcentaje que no significa nada. El resumen
pasa a contar solo lo vigente, y conserva el total original para poder declarar la diferencia.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 6: Registrar en CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Añadir la sección**

Añadir antes de `## Tareas de clase entregadas`:

```markdown
## Recorte de alcance — 18-oct-2026

El proyecto pasa de **257 a 157 actividades**. 101 recortadas, 12 que estaban hechas sin
registrar, 1 añadida.

| | |
|---|---|
| Spec | `docs/superpowers/specs/2026-10-18-recorte-de-alcance-design.md` |
| Plan | `docs/superpowers/plans/2026-10-18-recorte-de-alcance.md` |
| Documento | `entregables/10_Recorte_de_Alcance.docx` |
| Datos | `scripts/recorte.py` — única fuente de verdad, con 8 pruebas |

### El criterio

**Sobrevive lo que sirve a una medida de éxito de la carta sponsor. Se recorta lo que no sirve
a ninguna.** No es «lo que dio tiempo»: la carta comprometió diez resultados verificables, no
257 tareas.

### La medida 8 se retira

El asesor terapéutico tenía fecha límite el 10-sep y nunca llegó. Sin asesor no hay dictamen,
así que la medida no se puede verificar por ningún camino. Se sustituye por protocolos
publicados de NMT y se documenta la ausencia de validación externa como limitación explícita
— la contingencia que el acta ya había previsto.

### Los tres recortes grandes

- **Entorno 3D, de 31 a 6.** El área deja de modelar y pasa a integrar assets libres.
  Diecisiete tareas seriales de modelado no caben en diecinueve días.
- **Juego de ritmo, de 22 a 0.** Ya estaban recortadas por R14; esto solo lo refleja.
- **Sonido, de 22 a 1.** Doce ya estaban hechas sin registrar. Solo falta un crash.

### El Audio Mixer se descarta, y por qué

Añade un nodo al camino del audio y obligaría a **remedir la latencia**, que es la medida 4 y
la única ya ganada con margen. Ninguna medida pide un mixer.

### Cuidado al tocar el cronograma

Las recortadas **no se borran**: llevan `[FUERA DE ALCANCE]` y la razón en el campo de notas.
Una actividad borrada no deja rastro de por qué se quitó.

`validacion.py` las excluye del denominador. El avance vigente se mide contra 156, no 257.
```

- [ ] **Step 2: Commit y push**

```bash
cd /Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica
git add CLAUDE.md
git commit -m "docs: registrar el recorte de alcance

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push origin main
```

---

## Resumen de verificación

| Qué | Cómo |
|---|---|
| Las listas cubren todo lo pendiente y nada más | 8 pruebas en `test_recorte.py` |
| Ninguna clave en dos listas | Prueba `test_ninguna_clave_en_dos_listas` |
| No se recorta nada terminado | Prueba `test_no_se_clasifica_algo_ya_terminado` |
| Ninguna superviviente sirve a la medida retirada | Prueba `test_la_medida_retirada_no_la_sirve_nadie` |
| El XML sigue válido tras marcar | `ET.parse` tras `marcar_recorte.py` |
| Los porcentajes no se tocaron | Conteo de tareas al 100 % antes y después |
| El documento contiene lo que afirma | Seis comprobaciones de contenido |

## Qué NO cubre este plan

**Marcar las doce de sonido al 100 %.** Lo hace Christian desde ProjectLibre, no un script: el
cronograma ya demostró tres veces que su manejo del avance no sobrevive a ediciones a mano.

**Implementar la actividad nueva** (`DM.1`, exportar métricas). Es trabajo de código con su
propio ciclo de spec y plan.

**Modificar la carta sponsor o el acta.** El recorte es un control de cambios sobre el alcance
vigente; la carta conserva sus diez medidas y este documento declara cuál se retira y por qué.
