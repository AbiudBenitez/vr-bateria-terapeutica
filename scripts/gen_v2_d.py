# -*- coding: utf-8 -*-
import sys, os, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
from docx.shared import Cm
from collections import Counter
import rc257 as R
M, O = R.V2, R.ORIG
f = R.fnum
FIG = "/Users/abiudbenitez/Documents/Claude/Projects/vr-bateria-terapeutica/entregables/figuras-ruta-critica/"
doc = Document('/tmp/_v2_c.docx')

def alcanza(MM, i, fin="QX"):
    vis={i}; p=[i]
    while p:
        k=p.pop()
        if k==fin: return True
        for s in MM["suc"].get(k,[]):
            if s not in vis: vis.add(s); p.append(s)
    return False

doc.add_page_break()
# ================================================================ 12
H(doc,"12. Contraste con el análisis anterior",1)
P(doc,"La versión 1.0 de este análisis, del 7 de septiembre, se hizo sobre la red tal como estaba declarada. "
  "Identificó que la red no cerraba y recomendó que cada área declarara en qué entregable se integra el "
  "resultado de sus tareas. El documento de cambios del 9 de septiembre hace exactamente eso. Esta sección "
  "compara ambos estados.")

H(doc,"12.1 Cuadro comparativo",2)
alc1 = sum(1 for k in R.ORD if alcanza(O,k))
alc2 = sum(1 for k in R.ORD if alcanza(M,k))
table(doc,["Dimensión","Versión 1.0","Versión 2.0","Lectura"],[
 ("Duración de la ruta crítica", f"{O['TOTAL']:.2f} días", f"{M['TOTAL']:.2f} días",
  f"Crece {M['TOTAL']-O['TOTAL']:.2f} días. No es un empeoramiento: es la duración que siempre tuvo el proyecto, ahora visible."),
 ("Actividades sin consecuente", f"{len(R.TERMINALES_V1)}", f"{len(R.TERMINALES)}",
  "Queda solo QX, la presentación final, que es la única que debe carecer de consecuentes."),
 ("Actividades que alcanzan el entregable final", f"{alc1} de 257", f"{alc2} de 257",
  "Todo el trabajo del proyecto contribuye ahora a un entregable."),
 ("Actividades críticas", f"{len(O['CRIT'])}", f"{len(M['CRIT'])}",
  "Más actividades sin holgura, porque las cadenas ahora están conectadas."),
 ("Actividades en la ruta crítica", "28", f"{len(R.CADENA)}",
  "La cadena se alarga con AA.4, AD.1, AO.2 y las actividades de validación QV.1 y QV.2."),
 ("Áreas que atraviesa la ruta crítica", "3", "4",
  "Se suma una actividad de interfaz. Siguen ausentes desarrollo VR, juego de ritmo, música y sonido."),
],widths=[4.2,2.6,2.6,6.6],fs=9)

H(doc,"12.2 Efecto sobre las holguras de cada área",2)
P(doc,"La holgura mínima de un área indica cuánto margen tiene su actividad más ajustada. Un valor de cero "
  "significa que el área contiene actividades críticas.")
rows=[]
for a in sorted(R.AREAS, key=lambda x: -R.CARGA[x]):
    ks=[k for k in R.ORD if R.T[k]["area"]==a]
    h1=min(O["HT"][k] for k in ks); h2=min(M["HT"][k] for k in ks)
    n2=sum(1 for k in ks if abs(M["HT"][k])<1e-6)
    rows.append((a, R.RESP[a], f"{h1:.1f} d", f"{h2:.1f} d", n2))
table(doc,["Área","Responsable","Holgura mínima v1.0","Holgura mínima v2.0","Actividades críticas v2.0"],
      rows,widths=[4.8,2.6,3.0,3.0,2.6],fs=9.5)
P(doc,"El sonido es el área que más margen pierde, de 17.6 a 8.0 días, porque SC.2 pasa a ser predecesora de "
  "las pruebas con usuarios. La interfaz pasa de 4.6 días a cero: II.4, II.5 e II.6 entran en la cadena "
  "hacia QT.8 y una de ellas se vuelve crítica. El desarrollo VR y el juego de ritmo siguen con holgura, "
  "aunque menor.")

H(doc,"12.3 Qué corrigieron los cambios",2)
table(doc,["Defecto señalado en la versión 1.0","Estado"],[
 ("Noventa actividades no conducían a ningún entregable. El 35 % del trabajo no llegaba al producto final.",
  "Corregido. Queda una sola actividad terminal, que es la correcta."),
 ("QT.8, «pruebas con usuarios del prototipo integrado», dependía de tres actividades y no del prototipo integrado.",
  "Corregido. Pasa de 3 a 17 predecesoras: juego de ritmo, audio mezclado, interfaz, seguridad del espacio, entorno optimizado, ambientación y los cinco planes de prueba."),
 ("El informe final QI.4 no dependía de las secciones que lo componen.",
  "Corregido. Se le agregan diez predecesoras: la fundamentación teórica, los riesgos, el seguimiento y las siete secciones de documentación técnica."),
 ("La build candidata QB.1 no dependía de la validación integral.",
  "Corregido. Se le agregan QV.2 a QV.5 y el registro de seguimiento QC.1."),
 ("La presentación final QX no dependía de los manuales ni de las evidencias.",
  "Corregido. Se le agregan los manuales, las evidencias y la revisión del informe."),
 ("Las ramas de desarrollo VR y juego de ritmo no convergían.",
  "Corregido. DR.1 recoge siete predecesoras de la rama de batería, y JI.5 nueve de la rama de ritmo."),
],widths=[8.4,7.6],fs=9)

H(doc,"12.4 Qué no cambió",2)
bullets(doc,[
 "La ruta crítica sigue sin atravesar el desarrollo VR ni el juego de ritmo, que son el producto. Ahora es "
 "un resultado más sólido, porque ya no puede atribuirse al defecto de la red.",
 "La cadena del entorno tridimensional sigue siendo la trayectoria más larga, y creció de catorce a "
 "diecisiete actividades seriales a cargo de una sola persona.",
 "Las duraciones de las 257 tareas no se modificaron, de modo que la carga de trabajo por persona es "
 "idéntica. El desequilibrio de recursos descrito en la sección 14 permanece sin cambios.",
])

doc.save('/tmp/_v2_d.docx'); print("D OK")
