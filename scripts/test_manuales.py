# -*- coding: utf-8 -*-
"""Pruebas de los dos manuales.

LO QUE IMPIDEN: que un manual diga algo que el repo ya no dice. Un manual desfasado es peor
que ninguno, porque el lector lo sigue y falla sin entender por que.

La prueba que compara la cache contra el repo Unity SE SALTA cuando el repo no esta clonado.
Es el unico caso: las demas valen siempre, porque leen la cache commiteada.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import capturas
import manual_datos

from docx import Document

AQUI = os.path.dirname(os.path.abspath(__file__))
TECNICO = os.path.join(AQUI, "..", "entregables", "14_Manual_Tecnico.docx")
USUARIO = os.path.join(AQUI, "..", "entregables", "15_Manual_Usuario.docx")
QUEST = os.path.join(manual_datos.REPO_POR_OMISION, "scripts", "quest.sh")

D = manual_datos.DATOS


def texto(ruta):
    """Todo el texto del documento: parrafos y celdas."""
    d = Document(ruta)
    trozos = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                trozos.append(c.text)
    return "\n".join(trozos)


def encabezados(ruta):
    """[(nivel, texto)] de los encabezados, en orden."""
    d = Document(ruta)
    out = []
    for p in d.paragraphs:
        m = re.fullmatch(r"Heading (\d)", p.style.name)
        if m and p.text.strip():
            out.append((int(m.group(1)), p.text.strip()))
    return out


def cuerpos(ruta):
    """{encabezado: cuantos parrafos y tablas trae debajo}."""
    d = Document(ruta)
    actual, cuenta = None, {}
    for bloque in d.element.body.iterchildren():
        tag = bloque.tag.split("}")[-1]
        if tag == "p":
            from docx.text.paragraph import Paragraph
            p = Paragraph(bloque, d)
            if re.fullmatch(r"Heading \d", p.style.name) and p.text.strip():
                actual = p.text.strip()
                cuenta[actual] = 0
            elif actual and p.text.strip():
                cuenta[actual] += 1
        elif tag == "tbl" and actual:
            cuenta[actual] += 1
    return cuenta


TEC = texto(TECNICO)
USU = texto(USUARIO)


# ------------------------------------------------------------------ el manual tecnico

def test_todo_comando_del_menu_esta_documentado():
    """Un comando que el repo tiene y el manual no es un comando que nadie va a pasar."""
    faltan = []
    for grupo, comandos in D["menu"].items():
        for c in comandos:
            if c not in TEC:
                faltan.append("%s/%s" % (grupo, c))
    assert not faltan, "comandos del menú sin documentar: %s" % ", ".join(faltan)


def test_el_manual_no_inventa_comandos_de_menu():
    """Al revés: un comando documentado que ya no existe manda al lector a buscar un menú vacío."""
    reales = {c for v in D["menu"].values() for c in v}
    # Solo se comprueban las líneas de viñeta de la sección 3.1, que es donde van listados.
    d = Document(TECNICO)
    dentro, listados = False, []
    for p in d.paragraphs:
        if p.text.strip().startswith("3.1 "):
            dentro = True
            continue
        if dentro and re.fullmatch(r"Heading 1", p.style.name):
            break
        if dentro and p.style.name.startswith("List") and p.text.strip():
            listados.append(p.text.strip())
    assert listados, "la sección 3.1 no lista ningún comando"
    sobran = [c for c in listados if c not in reales]
    assert not sobran, "comandos documentados que el repo no tiene: %s" % ", ".join(sobran)


def test_el_orden_de_los_constructores_es_el_del_repo():
    """El orden es obligatorio: pasarlos al revés deja la escena peor que antes.

    SE LEE LA TABLA, no se busca la primera aparición de cada nombre en el documento. La
    sección 3.1 lista los comandos en orden alfabético, así que buscar por texto encontraba
    esa lista y la prueba fallaba con el documento correcto.
    """
    orden = [c[0].replace("Batería → ", "") for c in D["constructores"]]
    assert len(orden) == 4, "se esperaban cuatro constructores, hay %d" % len(orden)
    d = Document(TECNICO)
    tabla = next((t for t in d.tables if t.rows[0].cells[0].text == "Orden"), None)
    assert tabla is not None, "el manual técnico no tiene la tabla de constructores"
    filas = [r.cells[1].text.strip() for r in tabla.rows[1:]]
    assert filas == orden, \
        "la tabla de constructores va en otro orden que el repo.\n  repo:   %s\n  manual: %s" \
        % (orden, filas)


def test_las_pantallas_documentadas_son_las_que_existen():
    for estado in D["estados"]:
        assert estado in TEC, "la pantalla %s no se documenta en el manual técnico" % estado


def test_los_eventos_documentados_son_los_que_existen_y_en_orden():
    posiciones = [TEC.index(e) for e in D["eventos"]]
    assert posiciones == sorted(posiciones), \
        "los eventos no van en el manual en el mismo orden que en el código, y el orden ES " \
        "el dato: se guardan en la escena por su número de posición"


def test_el_manual_declara_las_pruebas_que_hay():
    assert str(D["pruebas"]) in TEC, \
        "el manual no dice las %d pruebas que tiene el repo" % D["pruebas"]


def test_el_manual_declara_la_version_de_unity_y_el_paquete():
    assert D["unity"] in TEC
    assert D["paquete"] in TEC


def test_los_dos_paquetes_ausentes_van_con_su_identificador():
    assert D["ausentes"], "el README ya no declara paquetes ausentes"
    for a in D["ausentes"]:
        assert a["id"] in TEC, "falta el identificador del paquete %s" % a["nombre"]


def test_el_manual_tecnico_cubre_lo_que_se_pidio():
    """Instalar, modificar y desinstalar: las tres cosas que el encargo nombraba."""
    for titulo in ("Instalar el proyecto desde cero", "Cómo modificar la aplicación",
                   "Desinstalar"):
        assert any(titulo in h for _, h in encabezados(TECNICO)), \
            "el manual técnico no tiene sección de %r" % titulo


def test_desinstalar_dice_que_datos_se_pierden():
    """Desinstalar borra la evidencia de las pruebas con usuarios. Callarlo no es una opción."""
    assert "quest.sh pull" in TEC
    for pista in ("Mediciones de sesión", "tutorial_visto", "Screenshots"):
        assert pista in TEC, "la sección de desinstalar no menciona %r" % pista


# ------------------------------------------------------------------ el manual de usuario

def test_los_rotulos_del_menu_son_los_que_el_pad_dice():
    """Un manual que diga TOCAR donde el pad dice JUGAR es peor que no tener manual."""
    menu = D["filas"]["Menu"]
    for plaza in range(D["plazas"]):
        etiqueta = menu.get(plaza, [None])[0]
        if not etiqueta:
            continue
        assert etiqueta in USU, \
            "el pad de la plaza %d dice %r y el manual de usuario no lo menciona" \
            % (plaza + 1, etiqueta)


def test_la_tabla_del_menu_no_quedo_en_guiones():
    """El defecto real: JSON guarda las plazas como texto y la tabla salió entera en guiones."""
    d = Document(USUARIO)
    for t in d.tables:
        if t.rows[0].cells[0].text != "Dice":
            continue
        valores = [r.cells[0].text.strip() for r in t.rows[1:]]
        assert any(v and v != "—" for v in valores), \
            "la tabla del menú del manual de usuario está vacía"
        return
    pytest.fail("el manual de usuario no tiene la tabla del menú")


def test_los_pasos_del_tutorial_son_los_que_hay():
    assert len(D["tutorial"]["pasos"]) == 4, \
        "el tutorial tiene %d pasos y el manual describe cuatro" % len(D["tutorial"]["pasos"])
    assert "cuatro pasos" in USU


def test_las_piezas_del_recorrido_estan_nombradas_en_palabras():
    """El lector no sabe qué es un 'HiHat' en el código: tiene que leer dónde está."""
    import gen_manual_usuario as G
    for pieza in D["tutorial"]["recorrido"]:
        assert pieza in G.PIEZAS, \
            "la pieza %r del recorrido del tutorial no tiene descripción para el usuario" % pieza
        assert G.PIEZAS[pieza] in USU


def test_el_manual_de_usuario_no_usa_jerga_del_codigo():
    """Nombres de clase, de archivo y de comando van en el manual técnico, no aquí."""
    prohibidas = ["EstadoApp", "OpcionesDeMenu", "DrumPad", "quest.sh", "dspTime",
                  "ProjectSettings", ".cs", "batchmode", "MonoBehaviour"]
    d = Document(USUARIO)
    # La nota final es para el equipo y está rotulada como tal: se excluye.
    corte = USU.find("Nota para el equipo")
    cuerpo = USU if corte < 0 else USU[:corte]
    halladas = [p for p in prohibidas if p in cuerpo]
    assert not halladas, "jerga del código en el manual de usuario: %s" % ", ".join(halladas)


def test_avisa_del_malestar_y_de_que_se_puede_parar():
    """Es una prueba con personas. Que se puede parar sin consecuencias va escrito."""
    assert "mareo" in USU
    assert "No hay que aguantarlo" in USU


def test_dice_que_se_guarda_y_que_no():
    assert any("Qué se guarda" in h for _, h in encabezados(USUARIO))
    for pista in ("Tu nombre", "modo libre"):
        assert pista in USU


def test_el_veredicto_lleva_su_color_y_su_palabra():
    for palabra in ("PERFECT", "GOOD", "MISS"):
        assert palabra in USU, "el manual no explica el veredicto %s" % palabra


# ------------------------------------------------------------------ las capturas

def test_toda_captura_del_manifiesto_sale_en_el_documento():
    """Puesta o rotulada como faltante. Lo que no puede es desaparecer sin avisar."""
    for nombre, _, pie, _ in capturas.MANIFIESTO:
        if capturas.existe(nombre):
            continue
        assert nombre in USU, \
            "la captura %r falta y el documento no deja el hueco rotulado" % nombre


def test_el_manifiesto_no_tiene_nombres_repetidos():
    nombres = [m[0] for m in capturas.MANIFIESTO]
    assert len(nombres) == len(set(nombres))


def test_cada_captura_dice_como_tomarla():
    for nombre, _, pie, como in capturas.MANIFIESTO:
        assert len(pie) > 20, "el pie de %s no describe la pantalla" % nombre
        assert len(como) > 20, "%s no dice cómo llegar a esa pantalla" % nombre


def test_la_nota_para_el_equipo_solo_aparece_si_falta_alguna():
    hay_nota = "Nota para el equipo" in USU
    assert hay_nota == bool(capturas.faltantes()), \
        "la nota de capturas pendientes no coincide con las que faltan de verdad"


# ------------------------------------------------------------------ los dos

def test_los_dos_declaran_la_misma_version():
    assert D["version"] in TEC
    assert D["version"] in USU


def test_ninguna_seccion_queda_vacia():
    for ruta in (TECNICO, USUARIO):
        vacias = [h for h, n in cuerpos(ruta).items() if n == 0]
        assert not vacias, "%s tiene secciones sin contenido: %s" \
                           % (os.path.basename(ruta), ", ".join(vacias))


def test_se_remiten_uno_al_otro():
    assert "15_Manual_Usuario" in TEC, "el manual técnico no remite al de usuario"


# ------------------------------------------------------------------ quest.sh y la cache

@pytest.mark.skipif(not os.path.exists(QUEST), reason="el repo Unity no está clonado aquí")
def test_quest_tiene_los_comandos_que_el_manual_documenta():
    s = open(QUEST, encoding="utf-8").read()
    for comando in ("uninstall", "capturas", "install", "pull", "tutorial", "wifi"):
        assert re.search(r"^\s*%s\)" % comando, s, re.M), \
            "quest.sh no tiene el comando %r que el manual documenta" % comando
        assert "quest.sh %s" % comando in s, "quest.sh no lista %r en su ayuda" % comando


@pytest.mark.skipif(not os.path.exists(QUEST), reason="el repo Unity no está clonado aquí")
def test_desinstalar_pide_confirmacion():
    """Borra la evidencia de QT.8. No puede ser un comando que se ejecute por error."""
    s = open(QUEST, encoding="utf-8").read()
    bloque = s[s.index("  uninstall)"):]
    bloque = bloque[:bloque.index("\n  off)")]
    assert "read -r" in bloque, "uninstall no espera confirmación"
    assert "adb uninstall" in bloque
    assert bloque.index("read -r") < bloque.index("adb uninstall"), \
        "uninstall borra antes de preguntar"


@pytest.mark.skipif(manual_datos.repo() is None, reason="el repo Unity no está clonado aquí")
def test_la_cache_coincide_con_el_repo():
    """Si esto falla: python3 manual_datos.py --refrescar y regenerar los dos manuales."""
    import json
    vivo = manual_datos.extraer(manual_datos.repo())
    guardado = json.load(open(manual_datos.CACHE, encoding="utf-8"))
    assert json.dumps(vivo, sort_keys=True) == json.dumps(guardado, sort_keys=True), \
        "la caché de datos del repo Unity está desfasada"


@pytest.mark.skipif(manual_datos.repo() is None, reason="el repo Unity no está clonado aquí")
def test_el_readme_del_repo_unity_dice_las_pruebas_que_hay():
    """El README decía 210 desde el 21 de octubre; el trabajo de noviembre lo dejó corto por 160.

    El README es markdown escrito a mano, no generado, así que la cifra se vigila desde aquí:
    es el único sitio del proyecto donde ese número se teclea.
    """
    s = open(os.path.join(manual_datos.repo(), "README.md"), encoding="utf-8").read()
    assert str(D["pruebas"]) in s, \
        "el README del repo Unity no dice las %d pruebas que tiene: corre " \
        "manual_datos.py --refrescar y actualízalo" % D["pruebas"]


@pytest.mark.skipif(manual_datos.repo() is None, reason="el repo Unity no está clonado aquí")
def test_el_readme_remite_a_los_dos_manuales():
    s = open(os.path.join(manual_datos.repo(), "README.md"), encoding="utf-8").read()
    for nombre in ("14_Manual_Tecnico.docx", "15_Manual_Usuario.docx"):
        assert nombre in s, "el README no remite a %s" % nombre
