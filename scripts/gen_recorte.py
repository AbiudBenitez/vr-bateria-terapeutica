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
    return {AREAS.get(a, a): n for a, n in d.items()}


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

    neutro.H(d, "1. Por qué se recorta", 1)
    neutro.P(d,
             f"El proyecto registra {hechas_previas} de 257 actividades terminadas con "
             "diecinueve días hábiles hasta el cierre del periodo. Al ritmo actual no cabe, y "
             "el hueco no se reparte parejo: dos áreas están cerradas y tres apenas han "
             "arrancado.")
    filas = []
    for p in AREAS:
        ts = [t for t in f.values() if t["clave"][0] == p]
        h = sum(1 for t in ts if t["hecha"])
        filas.append([AREAS[p], str(h), str(len(ts)),
                      f"{100.0 * h / max(1, len(ts)):.0f} %"])
    filas.sort(key=lambda r_: -float(r_[3].rstrip(" %")))
    neutro.table(d, ["Área", "Terminadas", "Total", "Avance"], filas,
                 widths=[6.0, 3.4, 3.0, 3.6], fs=9.0)
    neutro.P(d,
             "La cadena de Entorno 3D tiene diecisiete actividades estrictamente seriales en "
             "una sola persona. Diecisiete tareas en fila dentro de diecinueve días hábiles "
             "exigen una por día sin un solo tropiezo, y la cadena lleva seis semanas sin "
             "arrancar. No es un retraso recuperable.")

    neutro.H(d, "2. El criterio", 1)
    neutro.P(d, "Sobrevive lo que sirve a una medida de éxito. Se recorta lo que no sirve a "
                "ninguna.", bold=True)
    neutro.P(d,
             "El criterio no es «lo que dio tiempo». La carta del patrocinador comprometió "
             "diez resultados verificables, no doscientas cincuenta y siete tareas: las tareas "
             "eran el camino, las medidas son el destino. Recortar contra las medidas se "
             "defiende; recortar contra el reloj, no.")
    ESTADO = {
        1: "Cumplida: seis piezas con indicador",
        2: "Funciona; falta la medición formal",
        3: "Cumplida",
        4: "Cumplida y medida: p90 de +4.07 ms",
        5: "Sin medir",
        6: "Requiere pruebas con usuarios",
        7: "Cumplida: tres niveles",
        8: "SE RETIRA. Ver sección 5",
        9: "A un paso. Ver sección 4.1",
        10: "Requiere pruebas con usuarios",
    }
    neutro.table(d, ["#", "Medida de éxito", "Estado"],
                 [[str(i), recorte.MEDIDAS[i], ESTADO[i]] for i in sorted(recorte.MEDIDAS)],
                 widths=[0.8, 8.4, 6.8], fs=8.0)

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
        widths=[10.0, 6.0], fs=9.5, negritas_col0=True)
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
             "de golpe: dejó de medirse contra trabajo que nunca se iba a hacer.", italic=True)

    neutro.H(d, "3.1 Trabajo terminado que no estaba registrado", 2)
    neutro.P(d,
             "Se hizo desde desarrollo VR mientras se construía la batería, y el área que lo "
             "tenía asignado seguía marcándolo como bloqueado. Contarlo como recortado daría "
             "por perdido trabajo real.")
    neutro.table(d, ["Clave", "Por qué está terminada"],
                 [[k, v] for k, v in sorted(recorte.YA_HECHAS.items())],
                 widths=[2.0, 14.0], fs=8.0)

    neutro.H(d, "3.2 Reparto del recorte por área", 2)
    sob, rec = por_area(recorte.SOBREVIVEN), por_area(recorte.RECORTADAS)
    neutro.table(d, ["Área", "Sobreviven", "Se recortan"],
                 [[a, str(sob.get(a, 0)), str(rec.get(a, 0))] for a in AREAS.values()],
                 widths=[7.0, 4.5, 4.5], fs=9.0)

    neutro.H(d, "4. Qué sobrevive, y a qué medida sirve", 1)
    neutro.table(d, ["Clave", "Medida", "Justificación"],
                 [[k, str(m) if m else "—", j]
                  for k, (m, j) in sorted(recorte.SOBREVIVEN.items())],
                 widths=[1.6, 1.4, 13.0], fs=7.5)

    neutro.H(d, "4.1 La única actividad que se añade", 2)
    neutro.P(d,
             "La medida 9 pide exportar por sesión precisión temporal, amplitud de movimiento "
             "y constancia del pulso. El marcador del juego de ritmo ya calcula la precisión "
             "temporal y la constancia; falta volcarlas a un archivo.")
    neutro.table(d, ["Clave", "Medida", "Actividad"],
                 [[k, str(m), j] for k, (m, j) in recorte.NUEVAS.items()],
                 widths=[1.6, 1.4, 13.0], fs=8.5)
    neutro.P(d,
             "Es el único punto donde este documento añade alcance mientras recorta. La razón "
             "es la desproporción: una actividad de trabajo cierra una medida que hoy está en "
             "cero.", italic=True)

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
        "La ausencia de validación terapéutica externa se documenta como limitación explícita "
        "del proyecto, en el informe final y en la presentación.",
        "El proyecto no se presenta como tratamiento de ninguna condición de salud.",
    ])
    neutro.P(d,
             "Es exactamente la contingencia que el acta constitutiva había previsto para este "
             "caso. Que el plan anticipara el fallo y nombrara la salida es, en sí mismo, "
             "evidencia de gestión.", italic=True)

    neutro.H(d, "6. Qué se recorta, y por qué", 1)
    neutro.P(d,
             "Ninguna actividad se borra del cronograma. Se marcan como fuera de alcance con "
             "la razón escrita, de modo que el recorte quede auditable: una actividad borrada "
             "no deja rastro de que existió ni de por qué se quitó.")
    n = 0
    for pref, nombre in AREAS.items():
        claves = sorted(k for k in recorte.RECORTADAS if k[0] == pref)
        if not claves:
            continue
        n += 1
        neutro.H(d, f"6.{n} {nombre} — {len(claves)}", 2)
        neutro.table(d, ["Clave", "Razón"],
                     [[k, recorte.RECORTADAS[k]] for k in claves],
                     widths=[1.8, 14.2], fs=7.5)

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
    neutro.table(d, ["Rol", "Nombre", "Firma"],
                 [["Dirección de proyecto", "Sarai Galindo García", "_" * 26],
                  ["Gerencia de proyecto", "Abiud Misael Benítez Franco", "_" * 26],
                  ["QA y documentación", "Diana Laura Tello Salinas", "_" * 26],
                  ["Entorno 3D", "Kimberly González Sepúlveda", "_" * 26],
                  ["Sonido", "Christian Salvador Valadez Gallegos", "_" * 26],
                  ["Música", "Javier Alejandro Hernández Caloca", "_" * 26],
                  ["Experiencia emocional", "María Fernanda Montoya Valdez", "_" * 26]],
                 widths=[4.4, 6.6, 5.0], fs=9.0)
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
