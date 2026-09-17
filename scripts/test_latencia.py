# -*- coding: utf-8 -*-
"""Pruebas de latencia.py con señales sintéticas de offset conocido."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import latencia

SR = 48000


def clic(sr=SR, dur_ms=2.0, semilla=0):
    """Clic de plástico: ráfaga corta de ruido blanco. Centroide espectral alto."""
    rng = np.random.default_rng(semilla)
    n = int(sr * dur_ms / 1000)
    env = np.exp(-np.linspace(0, 6, n))
    return rng.normal(0, 1, n) * env


def bombo(sr=SR, dur_ms=300.0, f0=150.0, f1=50.0):
    """Bombo: seno con barrido descendente y decaimiento. Centroide espectral bajo."""
    n = int(sr * dur_ms / 1000)
    t = np.arange(n) / sr
    f = np.linspace(f0, f1, n)
    fase = 2 * np.pi * np.cumsum(f) / sr
    return np.sin(fase) * np.exp(-t * 12)


def mezclar(eventos, dur_s=3.0, sr=SR):
    """Coloca (señal, t_segundos) sobre silencio. Devuelve la pista."""
    x = np.zeros(int(dur_s * sr))
    for sig, t in eventos:
        i = int(t * sr)
        x[i:i + len(sig)] += sig
    return x


def test_detecta_dos_transitorios():
    x = mezclar([(clic(), 1.0), (bombo(), 1.012)])
    ts = latencia.onset_times(x, SR)
    assert len(ts) == 2, f"esperaba 2 transitorios, hubo {len(ts)}"


def test_precision_sub_milisegundo():
    x = mezclar([(clic(), 1.0), (bombo(), 1.012)])
    ts = latencia.onset_times(x, SR)
    assert abs(ts[0] - 1.000) < 0.001
    assert abs(ts[1] - 1.012) < 0.001


def test_ignora_silencio():
    x = np.zeros(SR * 2)
    assert len(latencia.onset_times(x, SR)) == 0


def test_centroide_separa_clic_de_bombo():
    sc_clic = latencia.spectral_centroid(clic(), SR)
    sc_bombo = latencia.spectral_centroid(bombo(), SR)
    assert sc_clic > 3000, f"centroide del clic demasiado bajo: {sc_clic:.0f} Hz"
    assert sc_bombo < 1000, f"centroide del bombo demasiado alto: {sc_bombo:.0f} Hz"


def test_delta_positivo_sonido_tarde():
    x = mezclar([(clic(), 1.0), (bombo(), 1.012)])
    ds = latencia.deltas_ms(x, SR)
    assert len(ds) == 1
    assert abs(ds[0] - 12.0) < 1.0


def test_delta_negativo_sonido_adelantado():
    # El bombo suena ANTES del contacto físico: predicción adelantada. Debe dar Δ negativo.
    x = mezclar([(bombo(), 0.995), (clic(), 1.000)])
    ds = latencia.deltas_ms(x, SR)
    assert len(ds) == 1
    assert abs(ds[0] - (-5.0)) < 1.0


def test_varios_golpes():
    eventos = []
    for k, off in enumerate([0.008, 0.012, 0.010]):
        t = 0.5 + k * 0.6
        eventos += [(clic(semilla=k), t), (bombo(), t + off)]
    ds = latencia.deltas_ms(mezclar(eventos, dur_s=3.0), SR)
    assert len(ds) == 3
    assert all(abs(d - e * 1000) < 1.0 for d, e in zip(ds, [0.008, 0.012, 0.010]))


def test_omite_transitorios_indistinguibles():
    """
    Dos clics: mismo balance espectral, no hay forma de saber cuál es el golpe físico.

    Un golpe ambiguo se OMITE y se explica; no aborta la corrida. Antes lanzaba ValueError, y
    eso tiraba veinte golpes buenos por culpa de uno malo — justo al final de una sesión de
    medición, que es cuando más caro sale.
    """
    x = mezclar([(clic(semilla=1), 1.0), (clic(semilla=2), 1.012)])

    assert latencia.deltas_ms(x, SR) == []

    golpes = latencia.analizar(x, SR)
    assert len(golpes) == 1
    assert golpes[0]["ok"] is False
    assert "cuerpo grave" in golpes[0]["motivo"]


def test_un_golpe_malo_no_tira_los_buenos():
    """Dos golpes medibles y uno ambiguo en medio: se reportan los dos buenos."""
    eventos = [(clic(semilla=0), 0.5), (bombo(), 0.512),
               (clic(semilla=1), 1.5), (clic(semilla=2), 1.512),   # ambiguo
               (clic(semilla=3), 2.5), (bombo(), 2.510)]
    ds = latencia.deltas_ms(mezclar(eventos, dur_s=4.0), SR)
    assert len(ds) == 2, f"esperaba 2 golpes medibles, hubo {len(ds)}"
    assert abs(ds[0] - 12.0) < 1.0
    assert abs(ds[1] - 10.0) < 1.0


def escribir_wav(ruta, x, sr=SR, canales=1):
    """Escribe un WAV PCM de 16 bits con la estándar. Sin scipy: está roto en este entorno."""
    import wave
    datos = (np.clip(x / np.max(np.abs(x)), -1, 1) * 32767).astype("<i2")
    if canales > 1:
        datos = np.repeat(datos[:, None], canales, axis=1).ravel()
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(canales)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(datos.tobytes())


def test_estadistica():
    st = latencia.stats([10.0, 12.0, 11.0, 40.0, 9.0])
    assert st["n"] == 5
    assert st["mediana"] == pytest.approx(11.0)
    assert st["p90"] == pytest.approx(28.8, abs=0.1)
    assert st["min"] == pytest.approx(9.0)
    assert st["max"] == pytest.approx(40.0)


def test_veredicto_aprueba_dentro_de_rango():
    assert latencia.stats([18.0] * 20)["aprueba"] is True


def test_veredicto_rechaza_tarde():
    assert latencia.stats([30.0] * 20)["aprueba"] is False


def test_veredicto_rechaza_demasiado_adelantado():
    # Δ = -30 ms: el sonido va tan adelantado que se despega del gesto.
    assert latencia.stats([-30.0] * 20)["aprueba"] is False


def test_estadistica_rechaza_lista_vacia():
    with pytest.raises(ValueError, match="sin golpes"):
        latencia.stats([])


def test_carga_wav_de_disco(tmp_path):
    ruta = tmp_path / "corrida.wav"
    escribir_wav(ruta, mezclar([(clic(), 1.0), (bombo(), 1.012)]))

    sr, y = latencia.load_wav(str(ruta))
    assert sr == SR
    ds = latencia.deltas_ms(y, sr)
    assert len(ds) == 1
    assert abs(ds[0] - 12.0) < 1.0


def test_load_wav_convierte_estereo_a_mono(tmp_path):
    ruta = tmp_path / "estereo.wav"
    escribir_wav(ruta, mezclar([(clic(), 1.0), (bombo(), 1.012)]), canales=2)

    sr, y = latencia.load_wav(str(ruta))
    assert y.ndim == 1
    assert abs(latencia.deltas_ms(y, sr)[0] - 12.0) < 1.0
