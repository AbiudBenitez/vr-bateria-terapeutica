# -*- coding: utf-8 -*-
"""Ruta critica v3: la red despues del recorte de alcance del 18-oct-2026.

Sustituye a Ruta_Critica_257_Tareas_v2.docx, que calculaba sobre las 257
actividades. Aquella no se borra: pasa a entregables/superados/ porque es la
linea base contra la que se mide la desviacion.

Todo sale de rc_recorte.py, que a su vez lee recorte.py, rc257.py y el avance
real del cronograma. Aqui no se escribe ninguna cifra a mano.
"""
import datetime as dt
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm
from neutro import C, H, P, bullets, caption, landscape, nuevo, portada, portrait, table

import rc257 as R
import rc_recorte as X
import recorte as C_

SAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entregables")
FIG = os.path.join(SAL, "figuras-ruta-critica-v3")
DOC = os.path.join(SAL, "Ruta_Critica_257_Tareas_v3.docx")

CORTE = dt.date(2026, 10, 22)      # fecha de corte del calculo
ARRANQUE = dt.date(2026, 10, 23)   # primer dia habil despues del corte
ENTREGA = dt.date(2026, 11, 13)
FER = {dt.date(2026, 11, 16)}
MES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
       "septiembre", "octubre", "noviembre", "diciembre"]

M = X.REMANENTE


def fijar(t, anchos):
    """Fija el ancho de las columnas de verdad.

    Word y LibreOffice reparten el ancho por contenido mientras la tabla no
    declare disposicion fija. Sin esto, los anchos que se piden se ignoran y
    una columna de descripcion acaba partiendo las palabras."""
    pr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    pr.append(lay)
    grid = t._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        for col, ancho in zip(grid.findall(qn("w:gridCol")), anchos):
            col.set(qn("w:w"), str(int(Cm(ancho).twips)))
    for fila in t.rows:
        for celda, ancho in zip(fila.cells, anchos):
            celda.width = Cm(ancho)
    return t


def dia(n, ini=ARRANQUE):
    """n-esimo dia habil desde el arranque, con n en base cero."""
    c, k = ini, 0
    while True:
        if c.weekday() < 5 and c not in FER:
            if k >= n:
                return c
            k += 1
        c += dt.timedelta(days=1)


def habiles(a, b):
    n, c = 0, a
    while c <= b:
        if c.weekday() < 5 and c not in FER:
            n += 1
        c += dt.timedelta(days=1)
    return n


def f(d):
    return "%d/%s" % (d.day, MES[d.month - 1][:3])


def n(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


DISPONIBLES = habiles(ARRANQUE, ENTREGA)
FIN = dia(math.ceil(M["TOTAL"]) - 1)

doc = nuevo(margen=2.5, fuente="Arial", tam=11)
portada(doc,
        "RUTA CRÍTICA DEL PROYECTO",
        "Simulación de batería en realidad virtual\nLa red después del recorte de alcance",
        [("Versión", "3.0"),
         ("Fecha", "22 de octubre de 2026"),
         ("Sustituye a", "Ruta crítica de las 257 actividades, versión 2.0 del 9 de septiembre"),
         ("Unidad de aprendizaje", "Administración de Proyectos de Software"),
         ("Docente y patrocinadora", "Dra. Leticia Amalia Neira Tovar"),
         ("Equipo", "Equipo A"),
         ("Actividades en el alcance", "%d, de las 257 originales" % len(X.VIVAS)),
         ("Duración de la red recortada", "%s días hábiles" % n(X.PUENTE["TOTAL"])),
         ("Duración de lo que falta", "%s días hábiles desde el 23 de octubre" % n(M["TOTAL"]))])

# ───────────────────────────────── 1
H(doc, "1. Por qué hay una versión 3", 1)
P(doc, "El 18 de octubre de 2026 el proyecto recortó su alcance. La versión 2.0 de este "
       "documento calcula la ruta crítica sobre las 257 actividades del plan original, y desde "
       "ese día describe un proyecto que ya no existe. Esta versión recalcula la red sobre las "
       "%d actividades que quedan dentro del alcance." % len(X.VIVAS))
P(doc, "El recorte no es un ajuste de cronograma: es un cambio de alcance aprobado. Por eso el "
       "tratamiento no consiste en borrar filas y ver qué sale, sino en reemplazar la línea "
       "base y dejar escrito contra qué se medirá el proyecto de aquí en adelante.")

H(doc, "1.1 Cómo se trata un recorte de alcance en la red", 2)
table(doc, ["Regla", "Qué implica"], [
    ("La línea base anterior no se borra",
     "Sin ella no se puede explicar de qué se está desviando el proyecto. La versión 2.0 de este "
     "documento pasa a la carpeta de superados y se sigue citando."),
    ("El recorte entra como cambio aprobado",
     "No es una corrección del cronograma. Produce una línea base nueva, con su fecha, su razón "
     "y su autorización, y a partir de ahí el control se hace contra esa."),
    ("Las actividades recortadas se marcan, no se borran",
     "Cada una lleva la etiqueta de fuera de alcance y la razón en el campo de notas del "
     "cronograma. Una fila borrada no deja rastro de por qué se quitó."),
    ("Los enlaces rotos se deciden uno por uno",
     "Al quitar una actividad intermedia, sus sucesoras se quedan colgando. Si nadie decide qué "
     "pasa con cada enlace, la sucesora flota al día cero y la red se acorta sola. La sección 3 "
     "documenta esa decisión enlace por enlace."),
    ("La ruta crítica cambia de sitio",
     "Al quitar trabajo de una cadena, la criticidad se muda a otra. Hay que volver a publicar "
     "cuál es, porque el equipo sigue vigilando la anterior."),
    ("El valor ganado necesita rebase",
     "El valor planeado de lo recortado sale del denominador. Si no, el índice de desempeño del "
     "cronograma se desploma midiendo contra un alcance que ya no existe."),
    ("Lo que el recorte libera es reserva, no ahorro",
     "Los días que se ganan no se reparten en más trabajo: se quedan como margen frente a una "
     "fecha de entrega que no se movió."),
], widths=[5.0, 11.0], fs=9)

# ───────────────────────────────── 2
H(doc, "2. Las cuatro lecturas de la red", 1)
P(doc, "La misma red admite cuatro lecturas, y conviene no confundirlas. Las dos de en medio "
       "son el mismo alcance con distinta decisión sobre los enlaces rotos; la diferencia entre "
       "ellas es lo que cuesta no decidir.")
table(doc, ["Lectura", "Actividades", "Duración", "Críticas", "Qué es"], [
    ("Línea base anterior", len(R.ORD), "%s d" % n(R.V2["TOTAL"]), len(R.V2["CRIT"]),
     "El plan completo del 9 de septiembre, con los 38 cambios de dependencias del líder."),
    ("Recortada, reconectando", len(X.VIVAS), "%s d" % n(X.PUENTE["TOTAL"]),
     len(X.PUENTE["CRIT"]),
     "El alcance vigente. Cuando se corta B en A → B → C, se conecta A → C."),
    ("Recortada, sin reconectar", len(X.VIVAS), "%s d" % n(X.INGENUA["TOTAL"]),
     len(X.INGENUA["CRIT"]),
     "Lo que sale si se borran las filas y nadie mira los enlaces. No se adopta."),
    ("Lo que falta", len(X.PENDIENTES), "%s d" % n(M["TOTAL"]), len(M["CRIT"]),
     "La red vigente para dirigir: solo el trabajo pendiente, desde la fecha de corte."),
], widths=[4.0, 2.2, 1.9, 1.6, 6.3], fs=9)

P(doc, "Los %s días de diferencia entre reconectar y no reconectar son trabajo que la red "
       "ingenua se ahorra sin justificarlo: actividades que pasan a arrancar el día cero porque "
       "perdieron a su antecedente, no porque alguien haya decidido que ya no dependen de nada."
       % n(X.PUENTE["TOTAL"] - X.INGENUA["TOTAL"]))

doc.add_picture(os.path.join(FIG, "Fig1_Comparacion_de_redes.png"), width=Cm(15.5))
caption(doc, "Figura 1. Las cuatro lecturas de la red, en días hábiles.")

# ───────────────────────────────── 3
H(doc, "3. Los enlaces que el recorte rompió", 1)
P(doc, "El recorte retira %d actividades. Eso deja %d dependencias sin antecedente, repartidas "
       "en %d actividades que sí siguen dentro del alcance. De ellas, %d se quedan sin ningún "
       "antecedente vivo: son las que arrancarían el día cero si nadie interviniera."
       % (len(X.CORTADAS), sum(len(v) for v in X.ROTOS.values()), len(X.ROTOS),
          len(X.HUERFANAS)))

H(doc, "3.1 La regla que se aplicó", 2)
P(doc, "Cuando se corta B en la cadena A → B → C, se conecta A → C. La dependencia se hereda "
       "hacia arriba hasta encontrar una actividad viva, bajo el supuesto de que C necesitaba el "
       "producto que venía de aguas arriba y no la actividad B en sí. Es la lectura "
       "conservadora: nunca acorta la red por descuido.")
P(doc, "Pero el puente no es automático. Cada enlace heredado afirma algo sobre por qué C "
       "dependía de B, y esa afirmación hay que revisarla. La sección 3.3 documenta las que no "
       "se sostuvieron.")

H(doc, "3.2 Las actividades que quedaron sin antecedente", 2)
P(doc, "Quince de las dieciséis ya están terminadas, de modo que la herencia no mueve su fecha: "
       "una actividad cerrada tiene fecha real y no se reprograma detrás de un antecedente. La "
       "única pendiente es IT.1, y hereda dos actividades ya cerradas, así que puede arrancar de "
       "inmediato.")
avance = X.AVANCE
filas = []
for k in sorted(X.HUERFANAS):
    filas.append((k, R.T[k]["desc"][:52],
                  "%d %%" % avance.get(k, 0),
                  ", ".join(X.HUERFANAS[k]),
                  ", ".join(X.PUENTE["pre"][k]) or "ninguno"))
table(doc, ["Clave", "Actividad", "Avance", "Antecedentes que pierde", "Antecedentes que hereda"],
      filas, widths=[1.2, 5.0, 1.3, 3.0, 5.5], fs=8)

H(doc, "3.3 Los puentes que no se sostienen", 2)
P(doc, "Todos tienen el mismo defecto: el puente subió por una cadena cortada y arrastró "
       "trabajo de otra área que nunca habilitó a la sucesora. Se retiran %d enlaces."
       % len(X.REVISADAS))
table(doc, ["Sucesora", "Antecedente retirado", "Por qué no se sostiene"],
      [(a, b, razon) for (a, b), razon in sorted(X.REVISADAS.items())],
      widths=[1.8, 2.4, 11.8], fs=8.5)
P(doc, "Ninguno de los %d movía la fecha: todos eran enlaces entre actividades ya cerradas. "
       "Se retiran por higiene del registro, no por aritmética. Una dependencia que nunca "
       "existió no debe quedar inventada en la línea base nueva." % len(X.REVISADAS))

H(doc, "3.4 La dependencia que hubo que declarar de nuevo", 2)
P(doc, "El puente solo encuentra antecedentes que ya estaban aguas arriba. No puede encontrar a "
       "la actividad que ocupó el lugar de la cortada dentro del alcance, porque esa nunca fue "
       "su antecedente. Hubo un caso:")
table(doc, ["Sucesora", "Antecedente que se declara", "Razón"],
      [(k, p, razon) for k, lista in sorted(X.ANADIDAS.items()) for p, razon in lista],
      widths=[1.8, 2.8, 11.4], fs=8.5)

# ───────────────────────────────── 4
H(doc, "4. Dos actividades que la revisión mandó recortar", 1)
P(doc, "La revisión de los enlaces encontró un caso que el recorte del 18 de octubre no había "
       "visto: DT.4, incorporar el modelo tridimensional definitivo, y DT.5, reajustar los "
       "planos de golpe a ese modelo. Sobrevivieron al recorte, pero su insumo no: el modelado "
       "de la batería quedó fuera cuando el área de entorno dejó de modelar y pasó a integrar "
       "recursos de licencia libre.")
P(doc, "Quedaban vivas, pendientes y sin colgar de nada. Mantenerlas prometía un modelo que "
       "nadie iba a entregar. Se recortan con el mismo argumento con el que se cortó el modelado "
       "de la batería: el conjunto de primitivas ya funciona y está medido.")
table(doc, ["Clave", "Actividad", "Razón del recorte"],
      [(k, R.T[k]["desc"][:46], C_.RECORTADAS[k]) for k in ("DT.4", "DT.5")],
      widths=[1.2, 4.6, 10.2], fs=8.5)
P(doc, "Con estas dos, el alcance queda en %d actividades y el recorte acumulado en %d."
       % (len(X.VIVAS), len(X.CORTADAS)))

# ───────────────────────────────── 5
H(doc, "5. La red recortada y dónde quedó la criticidad", 1)
P(doc, "La red del alcance vigente dura %s días hábiles y tiene %d actividades sin holgura. La "
       "cadena crítica cambió por completo: antes pasaba por el entorno tridimensional, que es "
       "justo lo que se recortó." % (n(X.PUENTE["TOTAL"]), len(X.PUENTE["CRIT"])))
cad = X.cadena(X.PUENTE)
P(doc, " → ".join(cad), bold=True, align=C, after=10)
antes = set(R.CADENA)
table(doc, ["Movimiento", "Actividades"], [
    ("Entran a la cadena crítica", ", ".join(k for k in cad if k not in antes) or "ninguna"),
    ("Salen de la cadena crítica",
     ", ".join(k for k in R.CADENA if k not in set(cad)) or "ninguna"),
], widths=[4.0, 12.0], fs=9)
P(doc, "La lectura de dirección es ésta: la criticidad se fue del entorno tridimensional a la "
       "interfaz y a la documentación final. Quien antes estaba vigilado ya no lo está, y quien "
       "no lo estaba pasó a estarlo.")
doc.add_picture(os.path.join(FIG, "Fig3_Criticidad_por_area.png"), width=Cm(15.5))
caption(doc, "Figura 2. Actividades sin holgura por área, antes y después del recorte.")

# ───────────────────────────────── 6
doc.add_page_break()
H(doc, "6. La red que sirve para dirigir: lo que falta", 1)
P(doc, "Las redes anteriores programan desde el día cero, como si no se hubiera hecho nada. Con "
       "%d de %d actividades cerradas, esa lectura ya no describe al proyecto. La red que sirve "
       "para dirigir es la del trabajo pendiente, contada desde la fecha de corte del %d de "
       "octubre de 2026." % (len(X.HECHAS), len(X.VIVAS), CORTE.day))
table(doc, ["Concepto", "Valor"], [
    ("Actividades en el alcance", len(X.VIVAS)),
    ("Cerradas al %d de octubre" % CORTE.day, len(X.HECHAS)),
    ("Pendientes", len(X.PENDIENTES)),
    ("Suma de las duraciones pendientes", "%s días hábiles"
     % n(sum(R.T[k]["dur"] for k in X.PENDIENTES))),
    ("Duración de la red remanente", "%s días hábiles" % n(M["TOTAL"])),
    ("Primer día hábil disponible", "%d de octubre de 2026" % ARRANQUE.day),
    ("Fin que arroja la red", "%d de noviembre de 2026" % FIN.day),
    ("Entrega comprometida", "%d de noviembre de 2026" % ENTREGA.day),
    ("Días hábiles disponibles", DISPONIBLES),
    ("Margen", "%s días hábiles" % n(DISPONIBLES - M["TOTAL"])),
], widths=[7.0, 9.0], fs=9.5)

P(doc, "Veintitrés de las %d pendientes son de QA, documentación y gestión. Lo que queda del "
       "proyecto son las pruebas con usuarios y el informe final." % len(X.PENDIENTES))

H(doc, "6.1 Cadena crítica de lo que falta", 2)
P(doc, " → ".join(M["CRIT"]), bold=True, align=C, after=10)
P(doc, "Las pruebas con usuarios abren la cadena y la presentación la cierra. Entre una y otra "
       "no hay nada que se pueda adelantar: cada eslabón necesita el resultado del anterior.")

H(doc, "6.2 Qué puede arrancar de inmediato", 2)
libres = [k for k in X.PENDIENTES if not M["pre"][k]]
table(doc, ["Clave", "Actividad", "Duración", "Holgura"],
      [(k, R.T[k]["desc"][:62], "%s d" % n(R.T[k]["dur"]), "%s d" % n(M["HT"][k]))
       for k in sorted(libres, key=lambda x: M["HT"][x])],
      widths=[1.3, 9.0, 2.6, 3.1], fs=9)

doc.add_page_break()
landscape(doc, margen=1.5)
H(doc, "6.3 Matriz de información de lo que falta", 2)
P(doc, "Los tiempos van en días hábiles desde la fecha de corte. Las fechas ya descuentan "
       "sábados, domingos y el 16 de noviembre, que es inhábil.")
filas = []
for k in sorted(X.PENDIENTES, key=lambda x: (M["ES"][x], x)):
    filas.append((k, R.T[k]["desc"][:52], R.T[k]["resp"],
                  ", ".join(M["pre"][k]) or "—",
                  n(R.T[k]["dur"]), n(M["ES"][k]), n(M["EF"][k]), n(M["LS"][k]),
                  n(M["LF"][k]), n(M["HT"][k]),
                  "Sí" if abs(M["HT"][k]) < 1e-6 else "",
                  f(dia(math.floor(M["ES"][k]))),
                  f(dia(max(0, math.ceil(M["EF"][k]) - 1)))))
_ANCHOS = [1.2, 6.9, 2.1, 2.8, 1.0, 0.9, 0.9, 0.9, 0.9, 0.9, 1.3, 1.5, 1.5]
fijar(table(doc, ["Clave", "Actividad", "Responsable", "Antecedentes", "Días", "TPI", "TPT",
                  "TRI", "TRT", "HT", "Crítica", "Inicio", "Fin"], filas,
            widths=_ANCHOS, fs=7.5, autofit=False), _ANCHOS)

H(doc, "6.4 Red medida de lo que falta", 2)
doc.add_picture(os.path.join(FIG, "Fig2_Red_remanente.png"), width=Cm(24.0))
caption(doc, "Figura 3. Red remanente. Barra oscura: actividad crítica. Recuadro punteado: "
             "holgura total. La línea continua marca la entrega comprometida del 13 de noviembre.")

portrait(doc, margen=2.5)

# ───────────────────────────────── 7
H(doc, "7. Qué cambia en el control del proyecto", 1)
bullets(doc, [
    "El margen es de %s días hábiles sobre la entrega del 13 de noviembre, y no incluye la "
    "reserva de gestión del 17 al 20. Es holgura del plan, no colchón adicional."
    % n(DISPONIBLES - M["TOTAL"]),
    "La cadena crítica es toda de QA y documentación. El riesgo del proyecto dejó de ser "
    "técnico y pasó a ser de redacción y de disponibilidad de usuarios de prueba.",
    "Las pruebas con usuarios abren la cadena: cualquier día que se tarde en convocarlos es un "
    "día que pierde el informe final.",
    "El valor ganado hay que rebasearlo contra las %d actividades del alcance vigente. Medido "
    "contra las 257 originales, el avance aparenta ser menor de lo que es." % len(X.VIVAS),
    "Las %d actividades recortadas siguen en el cronograma, marcadas como fuera de alcance y "
    "con su razón. No se borran: son la evidencia de por qué el proyecto cabe en su fecha."
    % len(X.CORTADAS),
])

H(doc, "8. Trazabilidad del cálculo", 1)
table(doc, ["Archivo", "Qué aporta"], [
    ("scripts/rc257.py", "La red de las 257 actividades y la línea base anterior."),
    ("scripts/recorte.py", "Qué sobrevive y qué se recorta, con la razón de cada una. Única "
                           "fuente de verdad del recorte, con ocho pruebas."),
    ("scripts/rc_recorte.py", "Las tres redes de este documento, la revisión de los enlaces "
                              "heredados y la red remanente con el avance real."),
    ("scripts/validacion.py", "El avance leído del cronograma, no escrito a mano."),
    ("scripts/fig_rc3.py", "Las tres figuras."),
    ("entregables/superados/", "La versión 2.0 de este documento, que es la línea base anterior."),
], widths=[5.0, 11.0], fs=9)

doc.save(DOC)
print("OK", DOC)
print("   %d vivas | recortada %s d | remanente %s d | margen %s d"
      % (len(X.VIVAS), n(X.PUENTE["TOTAL"]), n(M["TOTAL"]), n(DISPONIBLES - M["TOTAL"])))
