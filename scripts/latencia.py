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

# Razón mínima entre el centroide alto y el bajo para fiarse de la clasificación. No se
# comprueba contra un umbral absoluto: lo que rompe el método es que los dos transitorios se
# PAREZCAN, que es justo lo que pasa si se mide con tarola en lugar de bombo.
RAZON_CENTROIDE_MIN = 2.5
EMPAREJADO_MAX_MS = 80.0

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


def deltas_ms(x, sr, emparejado_max_ms=EMPAREJADO_MAX_MS, razon_min=RAZON_CENTROIDE_MIN):
    """
    Devuelve un Δ en milisegundos por cada par clic/tambor encontrado.

    Empareja transitorios consecutivos separados por menos de emparejado_max_ms y los clasifica
    por centroide espectral: el de centroide más alto es el clic físico. NO se clasifica por
    orden temporal, porque Δ negativo es un resultado válido y frecuente.
    """
    ts = onset_times(x, sr)
    salida = []
    i = 0
    while i < len(ts) - 1:
        t_a, t_b = ts[i], ts[i + 1]
        if (t_b - t_a) * 1000 > emparejado_max_ms:
            i += 1
            continue

        # Ambas ventanas se acotan a la separación del par: ninguna debe alcanzar al otro
        # transitorio, o la clasificación puede invertirse y el Δ saldría con el signo cambiado.
        sep = t_b - t_a
        c_a = _centroide_en(x, sr, t_a, limite_s=sep)
        c_b = _centroide_en(x, sr, t_b, limite_s=sep)

        alto, bajo = max(c_a, c_b), min(c_a, c_b)
        if bajo <= 0 or alto / bajo < razon_min:
            raise ValueError(
                f"Par en t={t_a:.3f}s: centroides demasiado parecidos "
                f"({c_a:.0f} Hz y {c_b:.0f} Hz, razón {alto / max(bajo, 1e-9):.1f}). "
                "No se puede saber cuál es el clic físico y cuál el tambor. Causa habitual: "
                "se midió con tarola en lugar de bombo. El protocolo exige un sample grave, "
                "porque el clic del plástico y la tarola tienen contenido espectral parecido."
            )

        if c_a >= c_b:
            t_clic, t_virtual = t_a, t_b
        else:
            t_clic, t_virtual = t_b, t_a

        salida.append((t_virtual - t_clic) * 1000.0)
        i += 2
    return salida


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
    ap.add_argument("--margen-db", type=float, default=MARGEN_DB,
                    help="Sensibilidad del detector en dB. Súbelo si detecta transitorios de "
                         "más, bájalo si se pierde golpes. Por defecto 6.")
    args = ap.parse_args()

    sr, x = load_wav(args.wav)
    ts = onset_times(x, sr, margen_db=args.margen_db)
    ds = deltas_ms(x, sr)
    st = stats(ds)

    if args.etiqueta:
        print(f"Corrida: {args.etiqueta}")
    print(f"Archivo: {args.wav}  ({sr} Hz, {len(x) / sr:.1f} s)")
    print(f"Transitorios detectados: {len(ts)}   Golpes emparejados: {st['n']}")
    if args.detalle:
        for k, d in enumerate(ds, 1):
            print(f"  golpe {k:2d}:  {d:+7.2f} ms")
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
