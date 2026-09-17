# -*- coding: utf-8 -*-
"""
Mide la latencia golpe -> sonido a partir de una grabación WAV.

Protocolo (ver §7 del spec de diseño): se golpea una superficie física situada exactamente
donde vive el pad virtual. La grabación contiene dos transitorios por golpe:

  - el clic físico del control contra la superficie -> instante REAL del impacto
  - el tambor virtual por las bocinas del visor     -> sonido generado por la app

Delta = t_virtual - t_fisico.
  Positivo -> el sonido llega tarde.
  Negativo -> el sonido se adelanta, porque la predicción del plano armado va por delante
              del contacto físico. Es un resultado esperado, no un error.

Solo depende de numpy y de la biblioteca estándar. Se evitó scipy a propósito: en el entorno
de destino (macOS ARM) los binarios de scipy.signal fallan al cargar con
"section '__DATA/__thread_bss' has a zero-fill section type", y esta herramienta tiene que
correr sin pelearse con el entorno.
"""
import wave

import numpy as np

# --- Detección de transitorios -------------------------------------------------------------
# La envolvente se toma como PICO por bloques, no como RMS. Un RMS de ventana corta riza sobre
# el bombo (barre de 150 a 50 Hz) y la cola decayente cruza el umbral una y otra vez inventando
# transitorios. El pico por bloques de 3 ms apenas varía -3 dB a 50 Hz.
BLOQUE_MS = 3.0

# La guarda decae exponencialmente tras cada transitorio y un candidato debe superarla por este
# margen. Como la guarda TAMBIÉN sigue a la envolvente cuando ésta sube, una cola que decae
# nunca puede superarse a sí misma: los transitorios falsos de la cola desaparecen por
# construcción, sin necesidad de umbral absoluto.
#
# CUIDADO AL RETOCAR: el margen tiene una meseta estrecha. A 5 dB aparecen transitorios de más;
# a 8 dB se pierde el segundo transitorio de los pares muy juntos. 6 dB es el valor validado.
MARGEN_DB = 6.0
TAU_GUARDA_MS = 3.0        # meseta ancha: cualquier valor entre 2 y 4 ms da el mismo resultado
PISO_DB = -45.0
SEPARACION_MIN_MS = 2.5    # NO subir: Δ va de -25 a +25 ms y un refractario grande se tragaría
                           # el segundo transitorio de cada par

# --- Clasificación y emparejado ------------------------------------------------------------
# Ventana corta a propósito: el poder discriminante está en el ATAQUE. Una ventana larga deja
# entrar el cuerpo grave del tambor en el segmento del clic y acerca los dos centroides.
VENTANA_CENTROIDE_MS = 4.0

# El DECAIMIENTO es el discriminador principal, no el centroide.
#
# El centroide falla en grabaciones reales por una razón de hardware: las bocinas del visor
# apenas reproducen graves, y el micrófono de un celular tampoco los capta, así que al bombo
# se le amputa justo la parte que lo hacía grave. Medido sobre una corrida real: clic 1869 Hz
# contra bombo 745 Hz, razón 2.4 — por debajo del umbral de 2.5 que se había fijado a ojo.
#
# El decaimiento no sufre eso. El clic del plástico es un impulso que muere de inmediato; el
# tambor resuena. En la misma corrida: 0 ms contra 19 ms. Separación de sobra.
# El discriminador es la RAZÓN GRAVE/AGUDO de energía, no el decaimiento ni el centroide.
#
# El decaimiento funciona solo cuando los dos eventos no se solapan: si el tambor suena
# primero -que es lo que pasa cuando la predicción se adelanta, y es un resultado válido- su
# cola sigue sonando bajo el clic y contamina la medida. Medido sobre la señal de prueba: el
# clic daba 63 ms de decaimiento cuando dura 2.
#
# El centroide falla por hardware: las bocinas del visor apenas dan graves y el micrófono de un
# celular tampoco los capta, así que al tambor se le amputa lo que lo hacía grave. En una
# corrida real dio 1869 Hz contra 745 Hz, razón 2.4, por debajo del umbral fijado a ojo.
#
# La razón grave/agudo aguanta las dos cosas. Verificada sobre señal sintética con el tambor
# delante (82x de separación) y sobre grabación real de celular (1.4x a 6x, siempre en el
# mismo sentido).
CORTE_GRAVE_HZ = 500.0
VENTANA_BANDA_MS = 12.0
RAZON_GRAVE_MIN = 1.3          # por debajo, los dos transitorios se parecen demasiado

# Piso ABSOLUTO, además de la razón. Dos clics dan razones caprichosas -0.015 contra 0.009 es
# razón 1.7- porque con valores así de pequeños la decide el ruido de fondo. Un tambor real
# tiene cuerpo grave de verdad: medido, 1.4 a 2.0 en grabación de celular y 43 a 297 en señal
# sintética, contra 0.006 a 0.036 de un clic.
GRAVE_MIN_TAMBOR = 0.5

# Corroboración, no decisión.
DECAIMIENTO_MIN_TAMBOR_MS = 6.0
RAZON_CENTROIDE_MIN = 1.5

# Separación máxima entre el clic y el tambor del MISMO golpe.
EMPAREJADO_MAX_MS = 80.0

# Hueco mínimo entre golpes distintos. Los transitorios de un mismo golpe -clic, tambor y sus
# rebotes- caen juntos; el siguiente golpe llega mucho después.
HUECO_ENTRE_GOLPES_MS = 300.0

# Un transitorio por debajo de esta fracción del pico del golpe es un rebote de la sala, no un
# evento propio. Medido: el clic y el tambor llegan a ~1.0 y los rebotes a ~0.05.
FRACCION_MIN_EVENTO = 0.25

# --- Criterio de aceptación del hito Go/No-Go (§7.3 del spec) -------------------------------
# Un adelanto moderado es preferible al retraso: el oído tolera ~10 ms de adelanto y castiga
# con dureza el retraso. Por eso el rango es asimétrico.
DELTA_MIN_MS = -10.0
DELTA_MAX_MS = 25.0


def onset_times(x, sr, margen_db=MARGEN_DB, bloque_ms=BLOQUE_MS,
                tau_ms=TAU_GUARDA_MS, piso_db=PISO_DB,
                separacion_min_ms=SEPARACION_MIN_MS):
    """
    Devuelve los instantes de inicio de cada transitorio, en segundos.

    Dos etapas. Detección gruesa por envolvente de pico contra una guarda que decae, con
    resolución de bloque. Después refinamiento a resolución de muestra buscando el máximo de
    la SUBIDA de la envolvente suavizada — no el cruce de un nivel absoluto, porque cuando el
    tambor ya está sonando el nivel absoluto ya está alto y el clic se localizaría demasiado
    pronto.
    """
    if x.size == 0 or np.max(np.abs(x)) < 1e-12:
        return np.array([])

    x = x / np.max(np.abs(x))

    nb = max(1, int(sr * bloque_ms / 1000))
    n_bloques = len(x) // nb
    if n_bloques < 2:
        return np.array([])

    env = np.abs(x[:n_bloques * nb].reshape(n_bloques, nb)).max(axis=1)
    env_db = 20.0 * np.log10(env + 1e-12)

    decae = np.exp(-bloque_ms / tau_ms)
    factor = 10.0 ** (margen_db / 20.0)
    refract_bloques = max(1, int(separacion_min_ms / bloque_ms))

    guarda, ultimo, picos = 0.0, -(10 ** 9), []
    for k in range(n_bloques):
        es_pico = (env_db[k] > piso_db
                   and env[k] > guarda * factor
                   and k - ultimo >= refract_bloques)
        if es_pico:
            picos.append(k)
            ultimo = k
            guarda = env[k]
        else:
            guarda = max(env[k], guarda * decae)

    # Refinamiento a resolución de muestra sobre la subida de la envolvente.
    ns = max(1, int(sr * 0.0005))
    suave = np.convolve(np.abs(x), np.ones(ns) / ns, mode="same")
    subida = np.diff(suave, prepend=suave[0])

    ts = []
    for k in picos:
        ini = max(0, k * nb - nb)
        fin = min(len(x), k * nb + nb)
        if fin <= ini:
            continue
        j = ini + int(np.argmax(subida[ini:fin]))
        umbral_subida = 0.1 * subida[j]
        while j > ini and subida[j - 1] > umbral_subida:
            j -= 1
        ts.append(j / sr)

    return np.array(ts)


def spectral_centroid(seg, sr):
    """Centroide espectral de un segmento, en Hz. Media de frecuencias pesada por magnitud."""
    if len(seg) < 16:
        return 0.0
    ventana = np.hanning(len(seg))
    mag = np.abs(np.fft.rfft(seg * ventana))
    freqs = np.fft.rfftfreq(len(seg), 1.0 / sr)
    total = np.sum(mag)
    return float(np.sum(freqs * mag) / total) if total > 1e-12 else 0.0


def _centroide_en(x, sr, t, limite_s=None, ventana_ms=VENTANA_CENTROIDE_MS):
    """
    Centroide en el instante t.

    limite_s acota la ventana para que NO alcance al otro transitorio del par: con Δ de 5 ms
    una ventana fija de 10 ms metería el clic dentro del segmento del bombo y la clasificación
    podría invertirse. Se deja medio milisegundo de guarda.
    """
    i = int(t * sr)
    n = int(sr * ventana_ms / 1000)
    if limite_s is not None:
        n = min(n, max(16, int(sr * (limite_s - 0.0005))))
    return spectral_centroid(x[i:i + n], sr)


def _pico_en(x, sr, t, ventana_ms=20.0):
    """Amplitud de pico justo después del transitorio."""
    i = int(t * sr)
    n = int(sr * ventana_ms / 1000)
    seg = np.abs(x[i:i + n])
    return float(seg.max()) if seg.size else 0.0


def razon_grave(x, sr, t, ventana_ms=VENTANA_BANDA_MS, corte=CORTE_GRAVE_HZ):
    """
    Energía por debajo de `corte` dividida entre la de encima, en una ventana tras el
    transitorio. Alta en un tambor, baja en un clic de plástico.

    Es el discriminador principal porque es el único de los tres probados que sobrevive a que
    los dos eventos se solapen, cosa que ocurre siempre que Δ es pequeño o negativo.
    """
    i = int(t * sr)
    n = int(sr * ventana_ms / 1000)
    seg = x[i:i + n]
    if seg.size < 32:
        return 0.0
    mag = np.abs(np.fft.rfft(seg * np.hanning(seg.size)))
    f = np.fft.rfftfreq(seg.size, 1.0 / sr)
    agudo = mag[f >= corte].sum()
    return float(mag[f < corte].sum() / max(agudo, 1e-9))


def decay_ms(x, sr, t, caida_db=20.0, max_ms=400.0):
    """
    Milisegundos que tarda la envolvente en caer `caida_db` desde su pico.

    Es el discriminador principal entre el clic físico y el tambor virtual: un impulso de
    plástico muere de inmediato, un parche resuena.
    """
    i = int(t * sr)
    n = int(sr * max_ms / 1000)
    seg = np.abs(x[i:i + n])
    if seg.size < 10:
        return 0.0

    nb = max(1, int(sr * 0.001))                 # envolvente de pico por bloques de 1 ms
    m = seg.size // nb
    if m < 2:
        return 0.0
    env = seg[:m * nb].reshape(m, nb).max(axis=1)

    pico = env.max()
    if pico <= 0:
        return 0.0
    bajo = np.flatnonzero(env < pico * 10.0 ** (-caida_db / 20.0))
    return float(bajo[0]) if bajo.size else float(m)


def _agrupar_golpes(ts, hueco_ms=HUECO_ENTRE_GOLPES_MS):
    """Parte la lista de transitorios en golpes. Un hueco grande abre un golpe nuevo."""
    grupos = []
    for t in ts:
        if not grupos or (t - grupos[-1][-1]) * 1000 > hueco_ms:
            grupos.append([t])
        else:
            grupos[-1].append(t)
    return grupos


def analizar(x, sr, razon_grave_min=RAZON_GRAVE_MIN):
    """
    Devuelve una lista de dicts, uno por golpe, con todo lo que se midió.

    Por cada golpe se toman los DOS transitorios más fuertes -el clic y el tambor- y se
    descartan los rebotes de la sala, que llegan mucho más flojos. La clasificación es por
    decaimiento; el centroide corrobora.
    """
    ts = onset_times(x, sr)
    salida = []

    for grupo in _agrupar_golpes(ts):
        cand = [(t, _pico_en(x, sr, t)) for t in grupo]
        pico_golpe = max(p for _, p in cand) if cand else 0.0
        if pico_golpe <= 0:
            continue

        # Fuera los rebotes.
        cand = [(t, p) for t, p in cand if p >= FRACCION_MIN_EVENTO * pico_golpe]
        if len(cand) < 2:
            salida.append(dict(t=grupo[0], ok=False,
                               motivo="solo se detectó un transitorio fuerte en este golpe"))
            continue

        # Los dos más fuertes, devueltos a orden temporal.
        dos_mas_fuertes = sorted(cand, key=lambda c: -c[1])[:2]
        ta, tb = (t for t, _ in sorted(dos_mas_fuertes, key=lambda c: c[0]))

        sep_ms = (tb - ta) * 1000
        if sep_ms > EMPAREJADO_MAX_MS:
            salida.append(dict(t=ta, ok=False,
                               motivo=f"los dos transitorios fuertes están a {sep_ms:.0f} ms, "
                                      f"más de los {EMPAREJADO_MAX_MS:.0f} ms admitidos"))
            continue

        # Ventana acotada en el primero para que no se coma al segundo.
        vent_a = min(VENTANA_BANDA_MS, max(1.0, sep_ms - 0.5))
        ga = razon_grave(x, sr, ta, ventana_ms=vent_a)
        gb = razon_grave(x, sr, tb)
        da, db = decay_ms(x, sr, ta), decay_ms(x, sr, tb)

        alto, bajo = max(ga, gb), min(ga, gb)
        if alto < GRAVE_MIN_TAMBOR:
            salida.append(dict(t=ta, ok=False, grave=(ga, gb), decay=(da, db),
                               motivo=f"ninguno de los dos transitorios tiene cuerpo grave "
                                      f"({ga:.3f} y {gb:.3f}, hace falta {GRAVE_MIN_TAMBOR}). "
                                      f"Los dos parecen clics: ¿está sonando el tambor virtual, "
                                      f"y por las bocinas del visor y no por Bluetooth?"))
            continue

        if bajo <= 0 or alto / bajo < razon_grave_min:
            salida.append(dict(t=ta, ok=False, grave=(ga, gb), decay=(da, db),
                               motivo=f"los dos transitorios tienen el mismo balance de graves "
                                      f"({ga:.2f} y {gb:.2f}, razón {alto / max(bajo, 1e-9):.1f}). "
                                      f"No puedo saber cuál es el clic y cuál el tambor. "
                                      f"Usa un sample con más cuerpo grave"))
            continue

        # El más grave es el tambor.
        if ga > gb: t_tambor, t_clic = ta, tb
        else:       t_tambor, t_clic = tb, ta

        # Corroboración por decaimiento, solo si los eventos están lo bastante separados
        # para medirlo sin contaminación.
        coherente = None
        if sep_ms > 10.0:
            d_tambor = da if t_tambor == ta else db
            d_clic   = db if t_tambor == ta else da
            coherente = d_tambor > d_clic

        salida.append(dict(t=ta, ok=True,
                           delta_ms=(t_tambor - t_clic) * 1000.0,
                           grave=(ga, gb), decay=(da, db), coherente=coherente))
    return salida


def deltas_ms(x, sr, **kw):
    """Los Δ de los golpes que se pudieron medir. Los que no, se omiten."""
    return [g["delta_ms"] for g in analizar(x, sr) if g["ok"]]


def stats(deltas):
    """Estadística de una corrida y veredicto contra el criterio de aceptación."""
    if not deltas:
        raise ValueError("Corrida sin golpes detectados.")
    a = np.asarray(deltas, dtype=np.float64)
    p90 = float(np.percentile(a, 90))
    return {
        "n": int(a.size),
        "mediana": float(np.median(a)),
        "p90": p90,
        "min": float(a.min()),
        "max": float(a.max()),
        "aprueba": bool(DELTA_MIN_MS <= p90 <= DELTA_MAX_MS),
    }


def load_wav(ruta):
    """
    Carga un WAV y devuelve (sample_rate, señal mono float64 en [-1, 1]).

    Usa el módulo wave de la estándar en lugar de scipy.io: una dependencia menos, y scipy
    está roto en el entorno de destino. Acepta PCM de 8, 16 y 32 bits.
    """
    with wave.open(ruta, "rb") as w:
        canales = w.getnchannels()
        ancho = w.getsampwidth()
        sr = w.getframerate()
        crudo = w.readframes(w.getnframes())

    if ancho == 1:                                   # PCM 8 bits: sin signo, centrado en 128
        x = (np.frombuffer(crudo, dtype=np.uint8).astype(np.float64) - 128.0) / 128.0
    elif ancho == 2:
        x = np.frombuffer(crudo, dtype="<i2").astype(np.float64) / 32768.0
    elif ancho == 4:
        x = np.frombuffer(crudo, dtype="<i4").astype(np.float64) / 2147483648.0
    else:
        raise ValueError(f"Ancho de muestra no soportado: {ancho} bytes.")

    if canales > 1:
        x = x.reshape(-1, canales).mean(axis=1)
    return sr, x


def _main():
    import argparse

    ap = argparse.ArgumentParser(
        description="Mide la latencia golpe->sonido desde una grabación WAV."
    )
    ap.add_argument("wav", help="Grabación de la corrida, 48 kHz recomendado.")
    ap.add_argument("--etiqueta", default="", help="Nombre de la corrida, p. ej. 'con predicción'.")
    ap.add_argument("--detalle", action="store_true", help="Imprime el Δ de cada golpe.")
    ap.add_argument("--diagnostico", action="store_true",
                    help="Además del Δ, las características con las que se clasificó cada "
                         "transitorio. Para entender por qué un golpe se omitió.")
    ap.add_argument("--margen-db", type=float, default=MARGEN_DB,
                    help="Sensibilidad del detector en dB. Súbelo si detecta transitorios de "
                         "más, bájalo si se pierde golpes. Por defecto 6.")
    args = ap.parse_args()

    sr, x = load_wav(args.wav)
    ts = onset_times(x, sr, margen_db=args.margen_db)
    golpes = analizar(x, sr)
    ds = [g["delta_ms"] for g in golpes if g["ok"]]
    omitidos = [g for g in golpes if not g["ok"]]

    if not ds:
        print(f"Archivo: {args.wav}  ({sr} Hz, {len(x) / sr:.1f} s)")
        print(f"Transitorios detectados: {len(ts)}   Golpes: {len(golpes)}   Medibles: 0\n")
        print("Ningún golpe se pudo medir. Motivos:")
        for g in omitidos[:10]:
            print(f"  t={g['t']:7.3f}s  {g['motivo']}")
        raise SystemExit(1)

    st = stats(ds)

    if args.etiqueta:
        print(f"Corrida: {args.etiqueta}")
    print(f"Archivo: {args.wav}  ({sr} Hz, {len(x) / sr:.1f} s)")
    print(f"Transitorios detectados: {len(ts)}   "
          f"Golpes medibles: {st['n']}   Omitidos: {len(omitidos)}")
    if args.detalle or args.diagnostico:
        k = 0
        for g in golpes:
            if not g["ok"]:
                print(f"  omitido t={g['t']:7.3f}s  {g['motivo']}")
                continue
            k += 1
            linea = f"  golpe {k:2d}:  {g['delta_ms']:+7.2f} ms"
            if args.diagnostico:
                ga, gb = g["grave"]
                da, db = g["decay"]
                coh = {True: "sí", False: "NO", None: "n/d"}[g["coherente"]]
                linea += (f"   grave {ga:6.2f}/{gb:6.2f}"
                          f"   decae {da:4.0f}/{db:4.0f} ms"
                          f"   decaimiento coincide: {coh}")
            print(linea)

    incoherentes = [g for g in golpes if g["ok"] and g["coherente"] is False]
    if incoherentes:
        print(f"\nAviso: en {len(incoherentes)} golpe(s) el decaimiento contradice al balance de "
              f"graves. Corre con --diagnostico para verlos; si son muchos, el sample puede no "
              f"tener suficiente cuerpo grave.")
    print(f"Mediana: {st['mediana']:+7.2f} ms")
    print(f"p90:     {st['p90']:+7.2f} ms   <- el que decide")
    print(f"Rango:   {st['min']:+7.2f} .. {st['max']:+7.2f} ms")
    print(f"Criterio {DELTA_MIN_MS:+.0f} .. {DELTA_MAX_MS:+.0f} ms  ->  "
          f"{'APRUEBA' if st['aprueba'] else 'NO APRUEBA'}")

    if st["n"] < 20:
        print(f"\nAviso: {st['n']} golpes emparejados. El protocolo pide 20 para que el p90 "
              f"signifique algo. Si grabaste 20 y detectó menos, ajusta --margen-db.")


if __name__ == "__main__":
    _main()
