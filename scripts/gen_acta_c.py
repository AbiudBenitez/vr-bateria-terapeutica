# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neutro import *
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.table import WD_TABLE_ALIGNMENT
import pdm, edt

doc = Document('/tmp/_acta_b.docx')

# ---------------------------------------------------------------- GANTT
landscape(doc)
H(doc,"4.4 Diagrama de Gantt",2)
P(doc,"El cronograma abarca 11 semanas, del 1 de septiembre al 13 de noviembre de 2026. El 16 de septiembre "
  "es inhábil. La semana del 16 al 20 de noviembre se reserva como colchón de gestión previo al inicio de "
  "exámenes el 23 de noviembre, y no contiene trabajo programado.",size=9)
P(doc,"Las barras que coinciden en la misma columna representan trabajo que se ejecuta simultáneamente. Los "
  "paquetes marcados con la letra C pertenecen a alguna de las dos rutas críticas y no admiten retraso.",size=9)

HDR=["Cód.","Paquete de trabajo"]+[f"S{i+1}" for i in range(len(edt.SEM))]+["Resp.","C"]
SUB=["",""]+[f"{a.day}-{b.day} {edt.MESES[a.month-1]}" for a,b in edt.SEM]+["",""]
t=doc.add_table(rows=2,cols=len(HDR)); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
for i,h in enumerate(HDR):
    c=t.rows[0].cells[i]; c.text=""; c.paragraphs[0].alignment=C
    r=c.paragraphs[0].add_run(h); r.bold=True; r.font.size=Pt(7)
for i,h in enumerate(SUB):
    c=t.rows[1].cells[i]; c.text=""; c.paragraphs[0].alignment=C
    r=c.paragraphs[0].add_run(h); r.font.size=Pt(5.5)

CRIT_PKG={c for c,n,cr,re,rc,a,d in edt.PKG if a!="*" and pdm.HT.get(a,9)==0}
ABREV={"Gerente de proyecto":"Gerente","Gerente / Director":"Gerente/Dir.","Director / Coordinador":"Dir./Coord.",
 "Coordinador / Gerente":"Coord./Ger.","Analista de métricas":"Métricas","Director de proyecto":"Director",
 "Asesor / Métricas":"Asesor/Mét.","Asesor terapéutico":"Asesor","Métricas / Coordinador":"Mét./Coord.",
 "Artista 3D / UX-XR":"Arte/UX","Artista 3D":"Arte 3D","Diseñador UX-XR":"UX-XR",
 "Artista 3D / Dev RV":"Arte/Dev","Desarrollador VR":"Dev RV","Dev RV / Audio":"Dev/Audio",
 "Dev RV / UX-XR":"Dev/UX","Dev RV / Artista 3D":"Dev/Arte","UX-XR / Dev RV":"UX/Dev",
 "Diseñador de audio":"Audio","Audio / Dev RV":"Audio/Dev","Métricas / Dev RV":"Mét./Dev",
 "QA / Métricas":"QA/Mét.","QA / Dev RV":"QA/Dev","Coordinador / UX-XR / Asesor":"Coord./UX/As.",
 "Coordinador / Artista 3D":"Coord./Arte","Métricas / Gerente":"Mét./Ger.","Coordinador":"Coord."}

def fila(cod,nom,res,sems,crit,hito=False):
    cs=t.add_row().cells
    for i,v in enumerate([cod,nom]):
        cs[i].text=""; p=cs[i].paragraphs[0]; p.paragraph_format.space_after=Pt(0)
        r=p.add_run(v); r.font.size=Pt(6.5); r.bold=hito
    for k in range(len(edt.SEM)):
        cs[2+k].text=""; p=cs[2+k].paragraphs[0]; p.alignment=C; p.paragraph_format.space_after=Pt(0)
        if k in sems:
            r=p.add_run("◆" if hito else "██"); r.font.size=Pt(6.5 if hito else 7)
    j=2+len(edt.SEM)
    cs[j].text=""; p=cs[j].paragraphs[0]; p.paragraph_format.space_after=Pt(0)
    r=p.add_run(ABREV.get(res,res)); r.font.size=Pt(5.5)
    cs[j+1].text=""; p=cs[j+1].paragraphs[0]; p.alignment=C; p.paragraph_format.space_after=Pt(0)
    r=p.add_run("C" if crit else ""); r.font.size=Pt(6.5); r.bold=True

for cod,nom,cri,res,rec,act,d in edt.PKG:
    fila(cod,nom,res,edt.semanas_de(cod),cod in CRIT_PKG)

HITOS=[("H1","HITO — Diseño conceptual aprobado","H"),("H2","HITO — Go / No-Go de latencia","N"),
       ("H3","HITO — Modelos integrados con físicas","R"),("H4","HITO — Rutinas y métricas integradas","V"),
       ("H5","HITO — Build candidata congelada","X"),("H6","HITO — Cierre del proyecto","Z")]
for h,nom,act in HITOS:
    dia=pdm.dia(pdm.EF[act]-1)
    sem=[i for i,(a,b) in enumerate(edt.SEM) if a<=dia<=b]
    fila(h,nom,"Director",sem,False,hito=True)

for r_ in t.rows:
    r_.cells[0].width=Cm(1.1); r_.cells[1].width=Cm(6.2)
    for k in range(len(edt.SEM)): r_.cells[2+k].width=Cm(1.25)
    r_.cells[2+len(edt.SEM)].width=Cm(2.0); r_.cells[3+len(edt.SEM)].width=Cm(0.7)
doc.add_paragraph().paragraph_format.space_after=Pt(2)
caption(doc,"Diagrama de Gantt. Las barras en la misma columna indican trabajo simultáneo. La columna C marca los paquetes de la ruta crítica.")

portrait(doc)
# ---------------------------------------------------------------- hitos
H(doc,"4.5 Hitos",2)
table(doc,["Hito","Fecha","Qué se verifica","Consecuencia si no se cumple"],[
 ("H1  Diseño conceptual aprobado","4 sep 2026","Referencias visuales y alcance del modelo aprobados.","Se retrasa toda la rama del modelo tridimensional, que tiene un solo día de holgura."),
 ("H2  Go / No-Go de latencia","14 sep 2026","El retardo entre golpe y sonido se mantiene bajo 30 ms en el visor objetivo.","Se convoca al director para revisar el alcance del sistema de audio antes de continuar. Es el único hito con capacidad de detener el proyecto."),
 ("H3  Modelos integrados con físicas","13 oct 2026","La geometría optimizada responde a las colisiones.","Se desplaza la fecha final: la actividad que lo produce es crítica."),
 ("H4  Rutinas y métricas integradas","27 oct 2026","Rutinas validadas y registro de métricas operando en el simulador.","Se desplaza la fecha final."),
 ("H5  Build candidata congelada","3 nov 2026","Versión estable sobre la que se ejecutan las pruebas con usuarios.","No hay margen: las pruebas con usuarios ocupan la última semana."),
 ("H6  Cierre del proyecto","10 nov 2026","Pruebas cerradas, defectos corregidos y documentación entregada.","Se consume la reserva de gestión del 16 al 20 de noviembre."),
],widths=[4.0,2.2,5.0,4.8],fs=9.5)

# ---------------------------------------------------------------- secuencia
H(doc,"4.6 Secuencia de actividades y dependencias",2)
P(doc,"La secuencia se establece mediante diagramación por precedencias. Se emplean dos tipos de "
  "dependencia: fin → inicio, cuando la actividad sucesora no puede comenzar hasta que la predecesora "
  "termine, e inicio → inicio con demora, cuando la sucesora puede comenzar una vez que la predecesora lleva "
  "cierto avance.")
P(doc,"Las relaciones inicio → inicio son traslapes deliberados. Sin ellos el proyecto duraría 70 días "
  "hábiles y no cabría en el periodo disponible. Se aplicaron únicamente entre actividades cuyo producto es "
  "parcialmente utilizable antes de estar terminado, o que comparten responsable. Ninguna dependencia que "
  "atraviese un hito de decisión fue traslapada: el spike de latencia mantiene relación fin → inicio "
  "estricta con todo lo que le sigue.")
TIPO={"FS":"Fin → inicio","SS":"Inicio → inicio"}
rows=[]
for k in pdm.ORD:
    if not pdm.PRE[k]:
        rows.append((k,pdm.NOM[k][:44],"—","—"))
    else:
        for n,(p,t_,l) in enumerate(pdm.PRE[k]):
            rows.append((k if n==0 else "", pdm.NOM[k][:44] if n==0 else "", p,
                         TIPO[t_]+(f", demora {l} d" if l else "")))
table(doc,["Actividad","Nombre","Predecesora","Tipo de dependencia"],rows,
      widths=[1.8,6.4,2.2,5.6],fs=8.5)

# ---------------------------------------------------------------- simultaneidad
H(doc,"4.7 Trabajo que puede realizarse simultáneamente",2)
P(doc,"El cuadro recorre el proyecto por tramos e indica qué frentes están activos a la vez. Deriva "
  "directamente de la red de precedencias, no de una apreciación.")
table(doc,["Tramo","Fechas","Frentes simultáneos","Por qué son independientes"],[
 ("Días 0 – 4","1 – 4 sep","Gestión (1.1–1.2), investigación terapéutica (2.1), gestión del asesor (2.2), diseño conceptual (3.1), configuración de Unity (4.1)","Cinco paquetes sin predecesora. No comparten insumo ni responsable."),
 ("Días 4 – 10","7 – 14 sep","Modelado de la batería (3.2) y de baquetas y entorno (3.3) en paralelo, confirmación del asesor (2.3), spike de latencia (4.2)","El modelado se reparte entre dos responsables distintos, lo que permite ejecutarlo en paralelo."),
 ("Días 10 – 25","15 sep – 6 oct","Texturizado y optimización (3.4–3.5), mapeo de controles y colisiones (4.3–4.4), librería de audio (5.1–5.2), rutinas y métricas (2.4–2.7)","Punto de máximo paralelismo: cuatro ramas activas con siete paquetes en curso."),
 ("Días 25 – 35","7 – 20 oct","Integración de modelos con físicas (4.6), ergonomía (4.7), integración de audio (5.3), protocolo de sesión (2.8)","Tres frentes técnicos más la preparación del protocolo, que no depende de ellos."),
 ("Días 30 – 40","14 – 27 oct","Rutinas en el simulador (5.4–5.5), interfaz y registro de métricas (6.1–6.3), plan de pruebas (7.1)","Convergen en la build candidata. El plan de pruebas se redacta antes de que exista la versión a probar."),
 ("Días 40 – 45","28 oct – 3 nov","Build candidata (6.4) y pruebas de rendimiento (7.2)","Las pruebas técnicas se ejecutan sobre versiones intermedias durante la integración."),
 ("Días 45 – 50","4 – 10 nov","Pruebas con usuarios, corrección, manual e informe (7.3–7.6)","Cierre. Sin paralelismo entre ramas."),
],widths=[1.9,2.3,6.4,5.4],fs=8.5)

# ---------------------------------------------------------------- ruta critica
H(doc,"4.8 Ruta crítica",2)
P(doc,"La red tiene dos rutas críticas de 50 días hábiles cada una. Ambas parten de la configuración del "
  "entorno de desarrollo, se separan después del hito de latencia y convergen en la build candidata. El "
  "cálculo completo, con las matrices de secuencias, tiempos, información y elasticidad, se desarrolla en el "
  "documento de ruta crítica.")
table(doc,["Ruta","Trayectoria en paquetes de la EDT","Ramas que atraviesa"],[
 ("Ruta crítica 1","4.1 → 4.2 → 4.3 → 4.4 → 4.5 → 4.6 → 4.7 → 6.1–6.3 → 6.4 → 7.2 → 7.3–7.6","Interacción, prototipo y pruebas."),
 ("Ruta crítica 2","4.1 → 4.2 → 5.1–5.2 → 5.3 → 5.4–5.5 → 6.4 → 7.2 → 7.3–7.6","Interacción, audio y pruebas."),
],widths=[2.8,8.4,4.8],fs=9.5)
P(doc,"Advertencia sobre la versión anterior: la versión 2.0 declaraba una sola ruta crítica por la rama de "
  "interacción, sin haberla calculado. El cálculo confirma esa rama, pero identifica además una segunda ruta "
  "crítica por la rama de audio que no estaba declarada. En términos de control, la rama de audio debe "
  "vigilarse con la misma atención que la de interacción.")
P(doc,"La rama del modelo tridimensional queda con holgura total de un solo día. Formalmente no es crítica, "
  "pero el margen es despreciable y se controla como si lo fuera. Antes del rebalanceo descrito en el control "
  "del documento, esta rama era la ruta crítica del proyecto.")

doc.save('/tmp/_acta_c.docx'); print("parte C OK")
