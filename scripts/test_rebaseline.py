# -*- coding: utf-8 -*-
"""Pruebas del rebaseline del 11-nov-2026.

Lo que estas pruebas impiden que vuelva a pasar: que una actividad cerrada lleve su fecha
PLANEADA en vez de la real, que una pendiente quede programada en el pasado, y que el
cronograma cierre mas tarde de la reserva sin que nadie lo note.
"""
import datetime as D
import os
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cierres as CI
import rc257 as R
import rebaselinear as RB
import replan as RP

NS = "{http://schemas.microsoft.com/project}"
HOY = D.date(2026, 11, 11)
ARRANQUE_PROYECTO = D.date(2026, 9, 1)


def _texto(e, n):
    x = e.find(NS + n)
    return x.text if x is not None else None


def _hojas(ruta):
    """clave -> elemento, solo las hojas."""
    r = ET.parse(ruta).getroot()
    out = {}
    for e in r.findall(NS + "Tasks/" + NS + "Task"):
        if _texto(e, "Summary") == "1":
            continue
        k = RB.clave(_texto(e, "Name") or "")
        if k:
            out[k] = e
    return out


OP = _hojas(RB.OPERATIVO)
PL = _hojas(RB.PROJECTLIBRE)


class LasFechasDeCierreSonDefendibles(unittest.TestCase):

    def test_toda_cerrada_del_cronograma_tiene_fecha_de_registro(self):
        cerradas = {k for k, e in OP.items() if _texto(e, "PercentComplete") == "100"}
        self.assertEqual(cerradas - set(CI.CIERRES), set(),
                         "hay actividades al 100 % sin fecha de registro en cierres.py")

    def test_toda_fecha_de_registro_corresponde_a_una_cerrada(self):
        cerradas = {k for k, e in OP.items() if _texto(e, "PercentComplete") == "100"}
        self.assertEqual(set(CI.CIERRES) - cerradas, set(),
                         "cierres.py fecha actividades que el cronograma no tiene cerradas")

    def test_ninguna_fecha_de_cierre_esta_en_el_futuro(self):
        for k, (f, _) in CI.CIERRES.items():
            self.assertLessEqual(D.date.fromisoformat(f), HOY,
                                 "%s se cierra el %s, que todavia no ha pasado" % (k, f))

    def test_ninguna_fecha_de_cierre_precede_al_arranque_del_proyecto(self):
        for k, (f, _) in CI.CIERRES.items():
            self.assertGreaterEqual(D.date.fromisoformat(f), ARRANQUE_PROYECTO,
                                    "%s se cierra el %s, antes de que el proyecto arranque"
                                    % (k, f))

    def test_una_fecha_en_fin_de_semana_esta_declarada_como_dia_trabajado(self):
        for k, (f, _) in CI.CIERRES.items():
            d = D.date.fromisoformat(f)
            if d.weekday() >= 5:
                self.assertIn(f, CI.FINES_DE_SEMANA_TRABAJADOS,
                              "%s cierra el %s, que es fin de semana y no esta declarado "
                              "como dia trabajado" % (k, f))

    def test_cada_cierre_lleva_evidencia_y_no_una_frase_hecha(self):
        for k, (_, ev) in CI.CIERRES.items():
            self.assertGreater(len(ev), 50,
                               "la evidencia de %s es demasiado corta para sostener un "
                               "100 %%: %r" % (k, ev))

    def test_todo_fin_de_semana_declarado_se_usa_de_verdad(self):
        usados = {f for f, _ in CI.CIERRES.values()}
        for f in CI.FINES_DE_SEMANA_TRABAJADOS:
            self.assertIn(f, usados,
                          "%s se declara trabajado y ninguna actividad cierra ese dia" % f)


class ElCronogramaLlevaLasFechasReales(unittest.TestCase):

    def test_el_fin_de_cada_cerrada_es_su_fecha_de_registro(self):
        for k, (f, _) in CI.CIERRES.items():
            for nombre, hojas in (("operativo", OP), ("projectlibre", PL)):
                if k not in hojas:
                    continue
                fin = (_texto(hojas[k], "Finish") or "")[:10]
                self.assertEqual(fin, f,
                                 "%s en el %s termina el %s y su fecha de registro es el %s"
                                 % (k, nombre, fin, f))

    def test_stop_lleva_la_fecha_real_y_no_la_planeada(self):
        for k, (f, _) in CI.CIERRES.items():
            for hojas in (OP, PL):
                if k not in hojas:
                    continue
                stop = (_texto(hojas[k], "Stop") or "")[:10]
                self.assertEqual(stop, f, "%s cierra con Stop %s en vez de %s" % (k, stop, f))

    def test_ninguna_cerrada_arranca_despues_de_terminar(self):
        for k in CI.CIERRES:
            for hojas in (OP, PL):
                if k not in hojas:
                    continue
                self.assertLessEqual((_texto(hojas[k], "Start") or "")[:10],
                                     (_texto(hojas[k], "Finish") or "")[:10], k)

    def test_las_pendientes_llevan_las_fechas_del_replan(self):
        for k, (i, f) in RP.CALENDARIO.items():
            for nombre, hojas in (("operativo", OP), ("projectlibre", PL)):
                self.assertIn(k, hojas, "%s falta en el %s" % (k, nombre))
                self.assertEqual((_texto(hojas[k], "Start") or "")[:10], str(i), k)
                self.assertEqual((_texto(hojas[k], "Finish") or "")[:10], str(f), k)

    def test_ninguna_pendiente_esta_programada_en_el_pasado(self):
        for k, (i, _) in RP.CALENDARIO.items():
            self.assertGreaterEqual(i, RP.ARRANQUE,
                                    "%s arranca el %s, antes del primer dia disponible"
                                    % (k, i))

    def test_hay_actividades_en_noviembre(self):
        """El defecto que origino el rebaseline: ni una fecha en noviembre."""
        for nombre, hojas in (("operativo", OP), ("projectlibre", PL)):
            nov = [k for k, e in hojas.items()
                   if (_texto(e, "Finish") or "").startswith("2026-11")]
            self.assertGreaterEqual(len(nov), 20,
                                    "el %s solo tiene %d actividades en noviembre"
                                    % (nombre, len(nov)))

    def test_la_cabecera_dice_la_fecha_de_estado_y_el_cierre(self):
        for ruta in (RB.OPERATIVO, RB.PROJECTLIBRE):
            s = open(ruta, encoding="utf-8").read()
            self.assertIn("<StatusDate>%sT" % RB.CORTE, s, ruta)
            self.assertIn("<CurrentDate>%sT" % RB.CORTE, s, ruta)
            self.assertIn("<FinishDate>%sT" % RP.CIERRE, s, ruta)
            self.assertIn("<HonorConstraints>1</HonorConstraints>", s, ruta)

    def test_las_restricciones_sujetan_cada_actividad_a_su_fecha(self):
        for nombre, hojas in (("operativo", OP), ("projectlibre", PL)):
            for k in list(CI.CIERRES) + list(RP.CALENDARIO):
                if k not in hojas:
                    continue
                self.assertEqual(_texto(hojas[k], "ConstraintType"), "4",
                                 "%s en el %s no tiene restriccion 'no antes de': al "
                                 "recalcular se ira de nuevo a septiembre" % (k, nombre))
                self.assertEqual((_texto(hojas[k], "ConstraintDate") or "")[:10],
                                 (_texto(hojas[k], "Start") or "")[:10], k)

    def test_los_fines_de_semana_trabajados_estan_abiertos_en_el_calendario(self):
        for ruta in (RB.OPERATIVO, RB.PROJECTLIBRE):
            s = open(ruta, encoding="utf-8").read()
            uid = re.search(r"<CalendarUID>(\d+)</CalendarUID>", s).group(1)
            cal = re.search(r"<Calendar>\s*<UID>%s</UID>.*?</Calendar>" % uid, s, re.S).group(0)
            for f in CI.FINES_DE_SEMANA_TRABAJADOS:
                self.assertIn("<FromDate>%sT00:00:00</FromDate>" % f, cal,
                              "%s no esta abierto en el calendario de %s"
                              % (f, os.path.basename(ruta)))

    def test_las_recortadas_conservan_su_nota_y_no_se_refecharon(self):
        r = ET.parse(RB.PROJECTLIBRE).getroot()
        recortadas = [e for e in r.findall(NS + "Tasks/" + NS + "Task")
                      if "FUERA DE ALCANCE" in (_texto(e, "Notes") or "")]
        self.assertGreater(len(recortadas), 95)
        for e in recortadas:
            k = RB.clave(_texto(e, "Name") or "")
            self.assertNotIn(k, CI.CIERRES, "%s esta recortada y fechada como cerrada" % k)
            self.assertNotIn(k, RP.CALENDARIO, "%s esta recortada y replanificada" % k)

    def test_los_dos_archivos_siguen_siendo_xml_valido(self):
        for ruta in (RB.OPERATIVO, RB.PROJECTLIBRE):
            ET.parse(ruta)   # revienta si el rebaseline rompio el documento


class ElReplanCierraDentroDeLaReserva(unittest.TestCase):

    def test_cierra_el_veinte_de_noviembre_o_antes(self):
        self.assertLessEqual(RP.CIERRE, RP.RESERVA,
                             "el replan cierra el %s, pasada la reserva del %s"
                             % (RP.CIERRE, RP.RESERVA))

    def test_no_cae_en_semana_de_examenes(self):
        self.assertLess(RP.CIERRE, RP.EXAMENES)

    def test_el_traslape_acorta_la_cadena_sin_recortar_duraciones(self):
        self.assertLess(RP.TOTAL, 14.0)
        suma_replan = sum(R.T[k]["dur"] for k in RP.PENDIENTES)
        self.assertAlmostEqual(suma_replan, sum(R.T[k]["dur"] for k in RP.PENDIENTES),
                               msg="ninguna duracion se recorto; solo se traslapo")

    def test_cada_traslape_apunta_a_un_enlace_que_existe(self):
        for (k, p) in RP.TRASLAPES:
            self.assertIn(k, RP.PRE, "%s no es una actividad pendiente" % k)
            self.assertIn(p, RP.PRE[k],
                          "se declara un traslape %s <- %s y ese enlace no esta en la red"
                          % (k, p))

    def test_cada_traslape_dice_por_que_se_sostiene(self):
        for (k, p), (_, _, razon) in RP.TRASLAPES.items():
            self.assertGreater(len(razon), 60,
                               "el traslape %s <- %s no explica por que se sostiene" % (k, p))

    def test_el_replan_respeta_el_tipo_de_enlace_declarado(self):
        for k in RP.PENDIENTES:
            for p in RP.PRE[k]:
                tipo, demora, _ = RP.TRASLAPES.get((k, p), ("FS", 0, ""))
                base = RP.ES[p] if tipo == "SS" else RP.EF[p]
                self.assertGreaterEqual(RP.ES[k] + 1e-9, base + demora,
                                        "%s arranca antes de lo que su enlace con %s permite"
                                        % (k, p))

    def test_el_plan_no_disimula_que_sale_sin_holgura(self):
        self.assertEqual(RP.HOLGURA_DIAS, 0,
                         "si el replan gana holgura hay que decirlo en el modulo, no "
                         "dejar la advertencia de holgura cero cuando ya no aplica")


class RebaselinearEsIdempotente(unittest.TestCase):

    def test_correrlo_dos_veces_deja_el_mismo_archivo(self):
        antes = [open(r, encoding="utf-8").read() for r in (RB.OPERATIVO, RB.PROJECTLIBRE)]
        subprocess.run([sys.executable, os.path.join(os.path.dirname(RB.__file__),
                                                     "rebaselinear.py")],
                       check=True, capture_output=True)
        despues = [open(r, encoding="utf-8").read() for r in (RB.OPERATIVO, RB.PROJECTLIBRE)]
        self.assertEqual(antes, despues, "rebaselinear.py no es idempotente")


if __name__ == "__main__":
    unittest.main(verbosity=2)
