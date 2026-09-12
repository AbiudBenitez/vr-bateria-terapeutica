# -*- coding: utf-8 -*-
"""EDT: 42 paquetes de trabajo con responsable, criterio de aceptacion, recursos y fechas."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdm

# codigo, nombre, criterio de aceptacion, responsable, recursos, actividad de la red, dias
PKG = [
("1.1","Acta constitutiva","El documento está aprobado y firmado por la patrocinadora.","Gerente de proyecto","2 p","A",2),
("1.2","Plan de alcance y estructura de desglose del trabajo","La EDT cubre el 100 % del alcance y ningún paquete excede 80 horas.","Gerente de proyecto","3 p","A",3),
("1.3","Cronograma y línea base","El cronograma refleja la red de precedencias y cabe en el periodo disponible.","Gerente de proyecto","2 p","A",2),
("1.4","Registro de riesgos","Cada riesgo tiene probabilidad, impacto, responsable y respuesta definida.","Gerente / Director","2 p","A",2),
("1.5","Seguimiento y control del proyecto","Existe reporte semanal de avance sobre las actividades críticas.","Coordinador / Gerente","2 p","*",50),
("1.6","Cierre y presentación final","La documentación completa está entregada y la presentación realizada.","Director / Coordinador","8 p","Z",1),

("2.1","Investigación de musicoterapia y percusión","Se documentan al menos cinco fuentes revisadas por pares sobre percusión con fines terapéuticos.","Analista de métricas","2 p","B",9),
("2.2","Definición del perfil y gestión del asesor","El perfil está definido y existe al menos un candidato con contacto establecido.","Coordinador","2 p","C",5),
("2.3","Confirmación y contratación del asesor","El asesor acepta por escrito el alcance y el calendario de su participación.","Director de proyecto","1 p","D",3),
("2.4","Diseño de rutinas rítmicas terapéuticas","Existen al menos tres rutinas graduadas por dificultad, con su fundamento documentado.","Asesor / Métricas","2 p","E",6),
("2.5","Validación de rutinas con el asesor","El asesor dictamina por escrito que las rutinas son pertinentes.","Asesor terapéutico","1 p","E",4),
("2.6","Definición de métricas motrices","Cada métrica tiene unidad, método de cálculo y rango esperado.","Analista de métricas","2 p","F",6),
("2.7","Validación de métricas con el asesor","El asesor confirma que las métricas son interpretables clínicamente.","Asesor terapéutico","1 p","F",4),
("2.8","Protocolo de sesión y consentimiento informado","El protocolo define duración, progresión y criterios de suspensión.","Métricas / Coordinador","2 p","G",6),
("2.9","Validación final previa a pruebas","El asesor autoriza el inicio de las pruebas con usuarios.","Asesor terapéutico","1 p","G",4),

("3.1","Diseño conceptual y referencias visuales","Existe un tablero de referencias aprobado por el equipo.","Artista 3D / UX-XR","2 p","H",4),
("3.2","Modelado de la batería","Todos los componentes de la batería están modelados y nombrados según el estándar.","Artista 3D","1 p","I",10),
("3.3","Modelado de baquetas y entorno","Baquetas y escenario modelados, con escala verificada respecto al usuario.","Diseñador UX-XR","1 p","J",10),
("3.4","Texturizado y materiales","Cada componente tiene material asignado y se ve correctamente en el visor.","Artista 3D","2 p","K",10),
("3.5","Optimización de geometría para realidad virtual","La escena completa se mantiene bajo el presupuesto de polígonos definido.","Artista 3D / Dev RV","2 p","L",10),

("4.1","Configuración del proyecto Unity y SDK de Meta","El proyecto compila y se ejecuta en el visor objetivo.","Desarrollador VR","2 p","M",5),
("4.2","Spike de latencia (Go / No-Go)","Se mide el retardo entre golpe y sonido y se documenta si es menor a 30 ms.","Dev RV / Audio","2 p","N",5),
("4.3","Mapeo de controles de realidad virtual","Los controles se comportan como baquetas con seguimiento estable.","Dev RV / UX-XR","2 p","O",10),
("4.4","Detección de colisiones","El sistema identifica el componente golpeado en el 95 % de los intentos.","Desarrollador VR","2 p","P",10),
("4.5","Medición de velocidad de impacto","El sistema distingue tres niveles de intensidad de golpe.","Desarrollador VR","1 p","Q",5),
("4.6","Integración de modelos tridimensionales con físicas","Los modelos optimizados responden a las colisiones sin penetración visible.","Dev RV / Artista 3D","2 p","R",5),
("4.7","Ergonomía y prevención de mareo por movimiento","Ningún probador reporta molestia tras una sesión de 15 minutos.","UX-XR / Dev RV","2 p","S",5),

("5.1","Selección y edición de la librería de muestras","Cada componente tiene muestras en al menos tres niveles de intensidad.","Diseñador de audio","1 p","T",8),
("5.2","Capas de intensidad y variación por repetición","Golpes repetidos no producen un sonido idéntico.","Diseñador de audio","1 p","T",7),
("5.3","Integración de audio con físicas","El sonido corresponde al componente y a la intensidad del golpe.","Audio / Dev RV","2 p","U",10),
("5.4","Implementación de rutinas rítmicas","Las rutinas validadas se ejecutan dentro del simulador.","Dev RV / Audio","2 p","V",6),
("5.5","Guía visual y metrónomo","La guía marca el pulso de forma visible sin obstruir la interacción.","Dev RV / UX-XR","2 p","V",4),

("6.1","Menús y navegación","El usuario alcanza cualquier función en tres pasos o menos.","Diseñador UX-XR","1 p","W",3),
("6.2","Interfaz de usuario adaptativa","La interfaz se ajusta a la altura y al alcance del usuario.","Diseñador UX-XR","2 p","W",4),
("6.3","Módulo de registro de métricas","El sistema exporta las métricas de la sesión en formato legible.","Métricas / Dev RV","2 p","W",3),
("6.4","Integración general y build candidata","La versión integrada se ejecuta sin errores en el flujo completo.","Dev RV / UX-XR","3 p","X",5),

("7.1","Plan de pruebas y casos","Existe un caso de prueba por cada medida de éxito declarada.","QA / Métricas","2 p","Y-1",5),
("7.2","Pruebas de rendimiento y latencia","Se sostienen 72 cuadros por segundo y el retardo se mantiene bajo 30 ms.","QA / Dev RV","2 p","Y-2",5),
("7.3","Pruebas con usuarios","Se completan las sesiones previstas bajo el protocolo aprobado.","Coordinador / UX-XR / Asesor","4 p","Z",2),
("7.4","Corrección de defectos","No queda abierto ningún defecto de severidad alta.","Dev RV / UX-XR","3 p","Z",2),
("7.5","Manual técnico y de usuario","Un tercero puede instalar y operar el sistema siguiendo el manual.","Coordinador / Artista 3D","2 p","Z",3),
("7.6","Informe de pruebas y resultados","El informe presenta las métricas obtenidas por sesión.","Métricas / Gerente","2 p","Z",2),
]

# fechas: los paquetes se reparten dentro del rango de su actividad.
# Si la suma de sus duraciones cabe en la actividad van en secuencia; si no,
# se traslapan de forma proporcional para que el ultimo cierre con la actividad.
ORDEN_ACT = {}          # actividad -> lista de codigos en orden de ejecucion
for cod, nom, cri, res, rec, act, d in PKG:
    ORDEN_ACT.setdefault(act, []).append(cod)
ORDEN_ACT["Z"] = ["7.3","7.4","7.5","7.6","1.6"]     # el cierre va al final

DUR_PKG = {x[0]: x[6] for x in PKG}
FECHAS = {}
for act, codigos in ORDEN_ACT.items():
    if act == "*":
        for c in codigos: FECHAS[c] = (0, pdm.TOTAL)
        continue
    ini, D = pdm.ES[act], pdm.DUR[act]
    S = sum(DUR_PKG[c] for c in codigos)
    cum = 0
    for c in codigos:
        d = DUR_PKG[c]
        if S <= D:
            off = cum
        else:
            off = round(cum * (D - d) / max(1, S - d))
        FECHAS[c] = (ini + off, ini + min(off + d, D))
        cum += d

def rango(cod):
    a, b = FECHAS[cod]
    return pdm.dia(a), pdm.dia(max(a, b-1))

MESES = "ene feb mar abr may jun jul ago sep oct nov dic".split()
def fmt(d): return f"{d.day}-{MESES[d.month-1]}"

# semanas del proyecto
import datetime as dt
SEM = []
d = dt.date(2026,9,1)
while d <= dt.date(2026,11,13):
    fin = d + dt.timedelta(days=(4 - d.weekday()))
    SEM.append((d, min(fin, dt.date(2026,11,13))))
    d = fin + dt.timedelta(days=3)

def semanas_de(cod):
    a, b = rango(cod)
    return [i for i,(s,e) in enumerate(SEM) if not (b < s or a > e)]

if __name__ == "__main__":
    print(f"paquetes: {len(PKG)}   semanas: {len(SEM)}")
    for cod, nom, cri, res, rec, act, d in PKG:
        a, b = rango(cod)
        print(f"{cod:<5}{nom[:44]:<46}{act:<5}{d:>3}d  {fmt(a):>7} - {fmt(b):<7}  S{[i+1 for i in semanas_de(cod)]}")
