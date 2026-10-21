# -*- coding: utf-8 -*-
"""
Marca como completas las actividades verificadas, en el dialecto de ProjectLibre.

ProjectLibre NO lee los campos Actual*. Su avance sale de tres cosas a la vez:

    <Stop> igual a <Finish>  +  PercentComplete 100  +  PercentWorkComplete 100

Poner solo los porcentajes deja la tarea al 0 % en la vista de Gantt; poner solo <Stop> la
deja a medias. Costó tres intentos entenderlo, así que está escrito aquí y no en la memoria
de nadie.

CADA ACTIVIDAD LLEVA SU EVIDENCIA. Marcar algo como hecho sin poder decir qué lo demuestra es
cómo se llega a un 70 % que nadie puede defender frente a la docente.
"""
import os
import re
import sys

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "entregables", "Cronograma_Operativo.xml")

# clave -> (fecha de cierre, evidencia verificable)
HECHAS = {
    "AA.3": ("2026-10-18",
             "Assets elegidos y copiados: Stage y Stadium Seats de Poly Pizza, "
             "skybox de Kenney, arbol y textura de tierra de Fantasy Forest"),
    "AA.4": ("2026-10-18",
             "Licencia de cada asset verificada en su pagina de origen. "
             "Dos regimenes distintos: CC0/CC BY 3.0 y Standard Unity Asset Store EULA"),
    "AP.1": ("2026-10-18",
             "Escena compuesta por script: Assets/Editor/ConstruirBosque.cs. "
             "Claro de bosque con 20 arboles en tres anillos y suelo texturizado"),
    "AL.2": ("2026-10-18",
             "Iluminacion y ambiente definidos: sol bajo calido o luna rasante, "
             "ambiente de tres tonos, niebla exponencial y sombras suaves"),
    "QC.4": ("2026-10-18",
             "Registro de assets y licencias en Assets/Entorno/ATRIBUCION.txt y "
             "entregables/ATRIBUCION_entorno.txt, con las restricciones de cada EULA"),
    "QT.6": ("2026-10-17",
             "42 pruebas EditMode de bateria: CrossSolver 7, DrumPad 6, PadVisual 7, "
             "SampleSelector 8, HitIntensity 5, KitLayout 4, DrumHitFanout 2, EscenaRig 3"),
    "QT.7": ("2026-10-17",
             "52 pruebas EditMode de ritmo: SessionStats 11, MusicalTime 8, TempoMap 8, "
             "HitJudge 7, HitRing 6, NoteMatcher 6, JuegoDeRitmo 6"),
    "AO.5": ("2026-10-18",
             "Medido en el visor sobre el entorno definitivo: 12949 fotogramas, 12946 en "
             "vsync (100.0 %), 3 vsync perdidos (0.02 %) contra un criterio del 5 %. "
             "Evidencia en entregables/mediciones/fps_20261018_060703.json"),
    "QV.3": ("2026-10-18",
             "Misma corrida que AO.5, desde QA. 71.9 fps de media, mediana y p99 en 13.9 ms, "
             "que es el intervalo exacto de vsync a 72 Hz"),
    # --- cierre del 21 de octubre -------------------------------------------------------
    "IT.2": ("2026-10-20",
             "PasoSeguirPulso con EcoRitmico: 8 notas, 3 aciertos necesarios, ventanas de "
             "25 y 60 ms. Rediseñado como acompañamiento el 20-oct porque la version "
             "anterior callaba el metronomo al empezar el turno del usuario y pedia "
             "reproducir de memoria: fallaba 0 de 9 corridas. Pruebas en "
             "TutorialPasosTests y EcoRitmicoTests"),
    "IT.3": ("2026-10-20",
             "PasoIntensidades: exige los tres niveles suave, medio y fuerte, con el umbral "
             "de velocidad en cada pad y no global, porque un bombo se golpea mas fuerte que "
             "un hi-hat. Assets/Scripts/Tutorial/PasoIntensidades.cs"),
    "IT.4": ("2026-10-20",
             "TutorialRunner conduce los cuatro pasos con baqueta fantasma y rotulo, y "
             "FlujoApp lo arranca desde el menu y lleva a resultados. RegistroTutorial "
             "vuelca a JSON los intentos, el tiempo por paso, el tiempo hasta el primer "
             "golpe y el desfase de cada golpe: es la evidencia de la medida de exito 6"),
    "II.2": ("2026-10-20",
             "ConstruirMenu levanta TOCAR, TUTORIAL y SALIR como pads con disco y rotulo, "
             "cableando los diez campos de FlujoApp. EscenaCompletaTests comprueba el "
             "montaje entero, incluido que el marcador se apague fuera de Tocando"),
    "II.3": ("2026-10-20",
             "Los botones se golpean con las baquetas por el MISMO camino de deteccion que "
             "el kit: StickTracker los lleva en su lista y PadDeMenu filtra que el golpe "
             "venga de una mano. No hay un segundo mecanismo de entrada que mantener"),
    "II.6": ("2026-10-20",
             "PanelResultados y TextoResultados: el resultado dicho en palabras y no solo "
             "en cifras. Pruebas en TextoResultadosTests"),
    "IR.1": ("2026-10-20",
             "Tamaños MEDIDOS sobre la escena, no estimados. JudgePopup en 0.00556, que con "
             "el factor 36 de TMP da 0.200 de cuerpo, el mismo que el Indicador validado en "
             "el visor; el rotulo del tutorial en 0.85, escalado desde el 0.50 validado al "
             "pasar de 0.50 m de los ojos a 0.87; marcador e Indicador con autoajuste. "
             "LosTamanosDeTextoSonLosValidados los fija, porque tres correcciones seguidas "
             "no habian llegado nunca a la escena"),
    "IR.2": ("2026-10-20",
             "Tres posiciones corregidas con medida. El panel del marcador se ancla al kit "
             "en coordenadas de MUNDO tras encontrarse a dieciseis metros por heredar una "
             "posicion local; el rotulo del tutorial pasa del bombo -31 cm fuera del eje, "
             "16 mas alto y 45 cm mas cerca- al punto exacto del marcador; y el promedio "
             "que situa el panel deja de contar los botones del menu. Con sus pruebas de "
             "escena"),
    "SB.5": ("2026-10-19",
             "Crash y Platillo (ride) con cinco capas de velocidad cada uno, del kit AVL "
             "Drumkits Red Zeppelin bajo CC BY-SA 3.0. El crash entro como septima pieza el "
             "19-oct: Assets/Audio/Piezas/Crash.asset y Platillo.asset"),
    "QV.4": ("2026-10-17",
             "Hito Go/No-Go del acta, medido con el protocolo del clic fisico: p90 de "
             "+4.07 ms dentro de la ventana de -10 a +25 ms. Ocho corridas en "
             "entregables/mediciones/latencia_20261017_*.json. El desfase negativo es "
             "valido: la prediccion del plano armado adelanta el sonido"),

    "AS":   ("2026-10-18",
             "LimiteSeguro dibuja el perimetro del espacio con radio calculado del pad mas "
             "lejano mas 0.5 m de margen. Verificado en el visor durante la corrida de FPS "
             "del 18-oct: el circulo se ve y el radio se siente adecuado. La medida 10 habla "
             "de lo que reportan los usuarios, asi que se cierra con observacion, no con un "
             "numero del sistema"),
}

# Escritas pero SIN VERIFICAR. No se marcan: el codigo existe, la medicion no.
# Marcar una medicion que nadie ha hecho es exactamente el tipo de dato que luego
# no se puede sostener.
# Nada pendiente de medir ahora mismo. La lista se conserva porque es donde se declara lo
# que esta ESCRITO pero no VERIFICADO, que es la distincion que impide inflar el avance.
PENDIENTES_DE_MEDIR = {}


def clave(nombre):
    m = re.match(r"^([A-Z]{1,2}(?:\.\d+)?)\s*[—\-]", nombre or "")
    return m.group(1) if m else None


def main():
    texto = open(RUTA, encoding="utf-8").read()
    bloques = re.findall(r"<Task>.*?</Task>", texto, re.S)

    marcadas, nohay, yaestaban = [], [], []

    for b in bloques:
        nm = re.search(r"<Name>(.*?)</Name>", b, re.S)
        if not nm:
            continue
        k = clave(nm.group(1))
        if k not in HECHAS:
            continue

        pc = re.search(r"<PercentComplete>(\d+)</PercentComplete>", b)
        if pc and pc.group(1) == "100":
            yaestaban.append(k)
            continue

        fin = re.search(r"<Finish>(.*?)</Finish>", b)
        if not fin:
            nohay.append(k)
            continue

        nuevo = b
        # Stop = Finish: es de donde ProjectLibre deduce que la tarea cerro.
        if "<Stop>" in nuevo:
            nuevo = re.sub(r"<Stop>.*?</Stop>", "<Stop>%s</Stop>" % fin.group(1), nuevo)
        else:
            nuevo = nuevo.replace("<Finish>", "<Stop>%s</Stop><Finish>" % fin.group(1), 1)

        nuevo = re.sub(r"<PercentComplete>\d+</PercentComplete>",
                       "<PercentComplete>100</PercentComplete>", nuevo)
        nuevo = re.sub(r"<PercentWorkComplete>\d+</PercentWorkComplete>",
                       "<PercentWorkComplete>100</PercentWorkComplete>", nuevo)

        # La evidencia va en las notas: sin ella, un 100 % es una afirmacion sin respaldo.
        ev = "[HECHA %s] %s" % HECHAS[k]
        if "<Notes>" in nuevo:
            nuevo = re.sub(r"<Notes>(.*?)</Notes>",
                           lambda m: "<Notes>%s\n%s</Notes>" % (m.group(1), ev), nuevo, flags=re.S)
        else:
            nuevo = nuevo.replace("</Task>", "<Notes>%s</Notes></Task>" % ev)

        texto = texto.replace(b, nuevo, 1)
        marcadas.append(k)

    open(RUTA, "w", encoding="utf-8").write(texto)

    print("Marcadas %d:" % len(marcadas))
    for k in sorted(marcadas):
        print("  %-6s %s" % (k, HECHAS[k][1][:66]))
    if yaestaban:
        print("\nYa estaban al 100 %%: %s" % ", ".join(sorted(yaestaban)))
    if nohay:
        print("\nNO ENCONTRADAS: %s" % ", ".join(sorted(nohay)))
    print("\nSin marcar a proposito, falta medirlas:")
    for k, por in sorted(PENDIENTES_DE_MEDIR.items()):
        print("  %-6s %s" % (k, por))


if __name__ == "__main__":
    main()
