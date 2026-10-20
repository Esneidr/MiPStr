"""Eficiencia y paralelismo en Python — app de apoyo a la clase.

Ejecutar localmente:  streamlit run app.py
"""
import multiprocessing as mp
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

import tareas

st.set_page_config(page_title="Paralelismo en Python", page_icon="⚡", layout="centered")

NUCLEOS = os.cpu_count() or 1
CTX = mp.get_context("fork")          # forma de crear procesos que funciona en Linux / Streamlit Cloud
AZUL, NARANJA, VERDE, GRIS = "#2a78d6", "#eb6834", "#1baf7a", "#9aa0a6"

if "resultados" not in st.session_state:
    st.session_state.resultados = {}
R = st.session_state.resultados


# ------------------------------------------------------------------ utilidades
def cronometrar(funcion):
    inicio = time.perf_counter()
    salida = funcion()
    return salida, time.perf_counter() - inicio


def amdahl(p, n):
    return 1 / ((1 - p) + p / n)


def grafica_barras(etiquetas, valores, colores, titulo, eje_x, formato=".2f", sufijo=" s"):
    df = pd.DataFrame({"x": etiquetas, "y": valores, "texto": [f"{v:{formato}}{sufijo}" for v in valores]})
    base = alt.Chart(df).encode(
        x=alt.X("x:N", sort=None, title=eje_x, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("y:Q", title="Tiempo (s)", scale=alt.Scale(domain=[0, max(valores) * 1.2])),
    )
    barras = base.mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, size=48).encode(
        color=alt.Color("x:N", scale=alt.Scale(domain=etiquetas, range=colores), legend=None),
        tooltip=[alt.Tooltip("x:N", title=eje_x), alt.Tooltip("texto:N", title="Tiempo")],
    )
    texto = base.mark_text(dy=-8).encode(text="texto:N")
    st.altair_chart((barras + texto).properties(height=280, title=titulo), width="stretch")


# ------------------------------------------------------------------ encabezado
st.title("⚡ Eficiencia y paralelismo en Python")
st.caption("Computación Avanzada · Módulo 11 · App de apoyo al Colab introductorio")

tab_inicio, tab_hilos, tab_procesos, tab_numpy, tab_amdahl, tab_preguntas = st.tabs(
    ["Inicio", "1 · Hilos", "2 · Procesos", "3 · NumPy", "4 · Ley de Amdahl", "📝 Preguntas"]
)

# ================================================================== INICIO
with tab_inicio:
    st.markdown(
        """
Esta app repite los experimentos del Colab para que pueda **ejecutarlos, cambiar valores y comparar**.
Recorra las pestañas en orden y al final responda las preguntas de la pestaña **📝 Preguntas**.

Hay dos formas de hacer que un programa sea más rápido:
1. **Paralelismo:** hacer varias tareas al mismo tiempo, con `concurrent.futures`.
2. **Vectorización:** hacer las cuentas sobre todos los datos de una vez, con **NumPy**.

Y la **ley de Amdahl** dice cuánto se puede acelerar un programa.
"""
    )

    st.metric("Núcleos del servidor donde corre esta app", NUCLEOS)

    st.subheader("Vocabulario")
    st.markdown(
        """
| Palabra | Qué significa | En un supermercado |
|---|---|---|
| **Tarea** | Un trabajo pequeño que hay que hacer | Atender a un cliente |
| **Worker** | Un "trabajador" que toma tareas y las hace | Un cajero |
| **`max_workers`** | Cuántos workers hay | Cuántas cajas están abiertas |
| **Executor** | El que reparte las tareas entre los workers | El supervisor que manda a cada cliente a una caja |
| **Hilo** | Worker liviano que comparte la memoria del programa. Sirve cuando las tareas **esperan** | — |
| **Proceso** | Worker independiente, con su propia memoria. Sirve cuando las tareas **calculan** | — |
| **Vectorizar** | Operar sobre toda una lista de números de una vez | Pasar todo el mercado por un escáner |
"""
    )

    st.subheader("Las dos herramientas básicas")
    st.markdown("**Medir el tiempo** con `time.perf_counter()`:")
    st.code(
        """inicio = time.perf_counter()
# ... lo que se quiere medir ...
print(f"Tardó {time.perf_counter() - inicio:.2f} s")""",
        language="python",
    )
    st.markdown("**`map`** aplica una función a cada elemento de una lista. Las herramientas de paralelismo usan la misma idea:")
    st.code(
        """resultados = list(map(al_cuadrado, [1, 2, 3, 4, 5]))   # [1, 4, 9, 16, 25]""",
        language="python",
    )
    st.info("A `map` se le pasa el **nombre** de la función, sin paréntesis: `al_cuadrado`, no `al_cuadrado()`.")

# ================================================================== HILOS
with tab_hilos:
    st.header("Hilos: para tareas que **esperan**")
    st.markdown(
        "Ejemplo de **toma de datos**: leer un sensor por WiFi tarda 0.5 s, y casi todo ese tiempo "
        "el computador **solo espera** la respuesta."
    )
    st.code(
        """def leer_sensor(id_sensor):
    time.sleep(0.5)                    # espera la respuesta del sensor
    return f"Sensor {id_sensor}: {random.uniform(18, 30):.1f} °C"

with ThreadPoolExecutor(max_workers=8) as executor:
    lecturas = list(executor.map(leer_sensor, SENSORES))""",
        language="python",
    )

    st.subheader("Experimento: ¿cuántos workers conviene usar?")
    n_sensores = st.slider("Número de sensores", 2, 16, 8, key="h_sensores")
    opciones = st.multiselect(
        "Workers (hilos) a probar", [1, 2, 4, 8, 16], default=[1, 2, 4, 8], key="h_opciones"
    )
    if st.button("▶ Ejecutar experimento", key="h_btn", disabled=not opciones):
        sensores = list(range(1, n_sensores + 1))
        tiempos, barra = [], st.progress(0.0, "Leyendo sensores...")
        for k, w in enumerate(sorted(opciones)):
            def correr(w=w):
                with ThreadPoolExecutor(max_workers=w) as executor:
                    return list(executor.map(tareas.leer_sensor, sensores))
            lecturas, t = cronometrar(correr)
            tiempos.append(t)
            barra.progress((k + 1) / len(opciones), f"{w} workers: {t:.2f} s")
        barra.empty()
        R["hilos"] = {"sensores": n_sensores, "workers": sorted(opciones), "tiempos": tiempos, "lecturas": lecturas}

    if "hilos" in R:
        h = R["hilos"]
        grafica_barras([str(w) for w in h["workers"]], h["tiempos"], [AZUL] * len(h["workers"]),
                       f"Leer {h['sensores']} sensores", "Número de workers (hilos)", ".1f")
        with st.expander("Ver las lecturas"):
            st.write(h["lecturas"])
        st.success(
            f"El servidor tiene {NUCLEOS} núcleo(s), y aun así los hilos aceleran la lectura: "
            "mientras un hilo espera, los demás pueden lanzar sus consultas."
        )

    st.divider()
    st.subheader("Más herramientas")
    with st.expander("Funciones con dos argumentos"):
        st.markdown("A `executor.map` se le pasan **dos listas** y toma un elemento de cada una, en orden.")
        st.code(
            """lecturas_crudas = [21.4, 22.0, 19.8, 23.5]
ajustes =         [-0.5, 0.2,  0.0, -1.1]

with ThreadPoolExecutor(max_workers=4) as executor:
    corregidas = list(executor.map(calibrar, lecturas_crudas, ajustes))""",
            language="python",
        )
        if st.button("▶ Ejecutar", key="arg_btn"):
            def correr():
                with ThreadPoolExecutor(max_workers=4) as executor:
                    return list(executor.map(tareas.calibrar, [21.4, 22.0, 19.8, 23.5], [-0.5, 0.2, 0.0, -1.1]))
            corregidas, t = cronometrar(correr)
            st.write(f"Resultado: `{corregidas}` en {t:.2f} s (uno por uno serían 1.2 s)")

    with st.expander("Tareas diferentes al mismo tiempo: submit y result"):
        st.markdown(
            "`executor.submit(función, argumento)` lanza una tarea y devuelve un *vale* (*future*). "
            "`vale.result()` espera a que termine y entrega el resultado."
        )
        st.code(
            """with ThreadPoolExecutor(max_workers=3) as executor:
    vale1 = executor.submit(leer_sensor, 5)
    vale2 = executor.submit(leer_gps)
    vale3 = executor.submit(leer_bateria)
    print(vale1.result(), vale2.result(), vale3.result())""",
            language="python",
        )
        if st.button("▶ Ejecutar", key="submit_btn"):
            def correr():
                with ThreadPoolExecutor(max_workers=3) as executor:
                    vales = [executor.submit(tareas.leer_sensor, 5),
                             executor.submit(tareas.leer_gps),
                             executor.submit(tareas.leer_bateria)]
                    return [v.result() for v in vales]
            salidas, t = cronometrar(correr)
            st.write(salidas)
            st.write(f"Tiempo: {t:.2f} s (por separado serían 2.5 s)")

# ================================================================== PROCESOS
with tab_procesos:
    st.header("Procesos: para tareas que **calculan**")
    st.markdown(
        "Ejemplo de **procesamiento**: calcular el promedio de 2 millones de lecturas de cada sensor. "
        "Aquí el procesador **trabaja todo el tiempo**, no espera."
    )
    st.code(
        """def procesar_sensor(id_sensor):
    suma = 0
    for i in range(2_000_000):                 # muchas cuentas
        suma += (i * id_sensor) % 100
    return 20 + 0.05 * suma / 2_000_000

with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
    resultados = list(executor.map(procesar_sensor, SENSORES))""",
        language="python",
    )
    st.info(f"Este servidor tiene **{NUCLEOS} núcleo(s)**, así que se usan {NUCLEOS} procesos.")

    if st.button("▶ Comparar serial, hilos y procesos", key="p_btn"):
        sensores = [1, 2, 3, 4]
        with st.spinner("Calculando de tres formas..."):
            _, t_serial = cronometrar(lambda: list(map(tareas.procesar_sensor, sensores)))

            def con_hilos():
                with ThreadPoolExecutor(max_workers=4) as executor:
                    return list(executor.map(tareas.procesar_sensor, sensores))

            def con_procesos():
                with ProcessPoolExecutor(max_workers=NUCLEOS, mp_context=CTX) as executor:
                    return list(executor.map(tareas.procesar_sensor, sensores))

            _, t_hilos = cronometrar(con_hilos)
            res, t_proc = cronometrar(con_procesos)
        R["procesos"] = {"serial": t_serial, "hilos": t_hilos, "procesos": t_proc, "resultados": res}

    if "procesos" in R:
        p = R["procesos"]
        grafica_barras(["Serial", "Hilos (4)", f"Procesos ({NUCLEOS})"],
                       [p["serial"], p["hilos"], p["procesos"]], [GRIS, NARANJA, AZUL],
                       "Procesar 4 sensores", "Forma de ejecutar")
        c1, c2 = st.columns(2)
        c1.metric("Speedup con hilos", f"{p['serial'] / p['hilos']:.2f}x")
        c2.metric("Speedup con procesos", f"{p['serial'] / p['procesos']:.2f}x")
        with st.expander("Ver resultados"):
            st.write(p["resultados"])

    st.markdown("#### ¿Por qué los hilos no ayudan aquí?")
    st.markdown(
        """
En Python, dentro de un mismo programa **solo un hilo puede hacer cálculos a la vez**. Esa regla se llama **GIL**.
Es como un salón con varios estudiantes y **un solo marcador** para escribir en el tablero: se turnan.

- Si la tarea **espera**, el hilo suelta el marcador mientras espera y otro puede trabajar. Por eso los hilos sirven para leer sensores.
- Si la tarea **calcula**, todos necesitan el marcador todo el tiempo. Los hilos se turnan y no se gana nada.
- Cada **proceso** es otro salón, con su propio tablero y su propio marcador. Por eso sí calculan en paralelo, uno por núcleo.
"""
    )
    st.markdown(
        """
| | Hilo | Proceso |
|---|---|---|
| Memoria | Compartida con el programa | Propia: los datos se copian |
| Calculan en paralelo | No (GIL) | Sí, uno por núcleo |
| Cuántos usar | Muchos, si esperan | `os.cpu_count()` |
| Sirve para | Esperar: sensores, APIs, archivos | Calcular: estadísticas, simulaciones |
"""
    )

# ================================================================== NUMPY
with tab_numpy:
    st.header("Vectorización con NumPy")
    st.markdown(
        "Un ciclo `for` revisa los números **uno por uno**. NumPy hace la operación sobre **todos a la vez**, "
        "con código interno muy rápido. Antes de paralelizar, conviene preguntarse si se puede vectorizar."
    )

    st.subheader("Ejemplo: convertir lecturas de °C a °F")
    tam = st.select_slider("Cantidad de lecturas", options=[100_000, 500_000, 1_000_000, 2_000_000],
                           value=1_000_000, format_func=lambda v: f"{v:,}".replace(",", "."))
    st.code(
        """# Ciclo for                                  # NumPy
fahrenheit = []                              fahrenheit = celsius * 9 / 5 + 32
for c in celsius:
    fahrenheit.append(c * 9 / 5 + 32)""",
        language="python",
    )
    if st.button("▶ Comparar ciclo for y NumPy", key="n_btn"):
        celsius_lista = [random.uniform(18, 30) for _ in range(tam)]
        celsius_array = np.array(celsius_lista)

        def con_for():
            salida = []
            for c in celsius_lista:
                salida.append(c * 9 / 5 + 32)
            return salida

        _, t_for = cronometrar(con_for)
        _, t_np = cronometrar(lambda: celsius_array * 9 / 5 + 32)
        R["conversion"] = {"lecturas": tam, "for": t_for, "numpy": t_np}

    if "conversion" in R:
        c = R["conversion"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Ciclo for", f"{c['for']:.3f} s")
        c2.metric("NumPy", f"{c['numpy']:.4f} s")
        c3.metric("NumPy es", f"{c['for'] / c['numpy']:.0f}x más rápido")

    st.subheader("Funciones útiles con datos de sensores")
    lecturas = np.array([21.5, 22.0, 26.3, 19.8, 27.1, 23.4, 25.9, 20.2])
    umbral = st.slider("Umbral de alerta (°C)", 20.0, 28.0, 25.0, 0.5)
    st.code(f"lecturas = np.array({lecturas.tolist()})", language="python")
    tabla = pd.DataFrame({
        "Código": ["np.mean(lecturas)", "np.max(lecturas)", "np.std(lecturas)",
                   f"(lecturas > {umbral}).sum()", f"lecturas[lecturas > {umbral}]"],
        "Resultado": [f"{np.mean(lecturas):.2f}", f"{np.max(lecturas):.1f}", f"{np.std(lecturas):.2f}",
                      str(int((lecturas > umbral).sum())), str(lecturas[lecturas > umbral].tolist())],
    })
    st.dataframe(tabla, hide_index=True)

    st.subheader("El cálculo de los sensores de tres formas")
    st.code(
        """def procesar_sensor_numpy(id_sensor):
    i = np.arange(2_000_000)
    codigos = (i * id_sensor) % 100            # la misma fórmula, sin ciclo for
    return 20 + 0.05 * codigos.sum() / 2_000_000""",
        language="python",
    )
    if st.button("▶ Comparar serial, procesos y NumPy", key="n3_btn"):
        sensores = [1, 2, 3, 4]
        with st.spinner("Calculando..."):
            _, t_serial = cronometrar(lambda: list(map(tareas.procesar_sensor, sensores)))

            def con_procesos():
                with ProcessPoolExecutor(max_workers=NUCLEOS, mp_context=CTX) as executor:
                    return list(executor.map(tareas.procesar_sensor, sensores))

            _, t_proc = cronometrar(con_procesos)
            _, t_np = cronometrar(lambda: list(map(tareas.procesar_sensor_numpy, sensores)))
        R["tres_formas"] = {"serial": t_serial, "procesos": t_proc, "numpy": t_np}

    if "tres_formas" in R:
        f = R["tres_formas"]
        grafica_barras(["Serial", f"Procesos ({NUCLEOS})", "NumPy (1 núcleo)"],
                       [f["serial"], f["procesos"], f["numpy"]], [GRIS, AZUL, NARANJA],
                       "Procesar 4 sensores", "Forma de ejecutar")

    st.success(
        "**Orden recomendado:** 1) medir cuánto tarda cada parte · 2) vectorizar con NumPy · "
        "3) paralelizar lo que siga lento: hilos si espera, procesos si calcula."
    )

# ================================================================== AMDAHL
with tab_amdahl:
    st.header("La ley de Amdahl")
    st.markdown(
        """
Casi ningún programa se puede repartir completo: siempre hay una parte que se hace **una sola vez**
(leer la configuración, unir resultados, guardar el archivo).

> 🍳 Un almuerzo toma 20 min de picar y 40 min de horno. Si 4 personas pican, el picado baja a 5 min,
> pero el horno sigue tardando 40. El almuerzo pasa de 60 a 45 min, no a 15.

- **p**: fracción del tiempo que **sí** se puede repartir (entre 0 y 1).
- **N**: cuántos workers trabajan al mismo tiempo (núcleos si la tarea calcula, hilos si espera).
"""
    )
    st.latex(r"\text{Speedup} = \frac{1}{(1-p) + \dfrac{p}{N}} \qquad \text{Speedup máximo} = \frac{1}{1-p}")

    st.subheader("Simulador")
    c1, c2 = st.columns(2)
    p_sim = c1.slider("p (fracción paralelizable)", 0.0, 0.99, 0.80, 0.01)
    n_sim = c2.slider("N (workers)", 1, 128, 4)
    s = amdahl(p_sim, n_sim)
    s_max = 1 / (1 - p_sim)
    m1, m2, m3 = st.columns(3)
    m1.metric("Speedup", f"{s:.2f}x")
    m2.metric("Speedup máximo", f"{s_max:.2f}x")
    m3.metric("Un programa de 100 s tardaría", f"{100 / s:.1f} s")

    n_vals = np.arange(1, 129)
    curva = pd.DataFrame({"N": n_vals, "Speedup": amdahl(p_sim, n_vals)})
    linea = alt.Chart(curva).mark_line(color=AZUL, strokeWidth=2).encode(
        x=alt.X("N:Q", title="Workers (N)"), y=alt.Y("Speedup:Q", title="Speedup"),
        tooltip=["N", alt.Tooltip("Speedup:Q", format=".2f")],
    )
    punto = alt.Chart(pd.DataFrame({"N": [n_sim], "Speedup": [s]})).mark_point(
        color=NARANJA, filled=True, size=120).encode(x="N:Q", y="Speedup:Q")
    techo = alt.Chart(pd.DataFrame({"y": [s_max]})).mark_rule(color=GRIS, strokeDash=[5, 4]).encode(y="y:Q")
    st.altair_chart((linea + punto + techo).properties(
        height=300, title=f"Curva de Amdahl con p = {p_sim:.2f} (línea punteada: máximo {s_max:.1f}x)"),
        width="stretch")

    st.markdown("**Comparación rápida** (speedup para distintos p y N):")
    comp = pd.DataFrame(
        {f"N = {n}": [round(amdahl(p, n), 2) for p in [0.5, 0.8, 0.95]] for n in [2, 4, 8, 100]},
        index=["p = 0.50", "p = 0.80", "p = 0.95"],
    )
    st.dataframe(comp)

    st.subheader("Comprobar la ley con un programa de sensores")
    st.markdown(
        """
El programa tiene dos partes:
- **Leer la configuración**: 0.5 s, se hace una sola vez (**serial**).
- **Leer 8 sensores**: 8 × 0.25 s = 2 s, se reparte con hilos (**paralelizable**).

Entonces p = 2 / 2.5 = **0.8**.
"""
    )
    if st.button("▶ Ejecutar con 1, 2, 4 y 8 workers", key="a_btn"):
        def programa_completo(n_workers):
            time.sleep(0.5)                                       # parte serial
            with ThreadPoolExecutor(max_workers=n_workers) as executor:
                list(executor.map(tareas.leer_sensor_rapido, range(8)))   # parte paralelizable

        filas = []
        with st.spinner("Ejecutando el programa 4 veces..."):
            _, t1 = cronometrar(lambda: programa_completo(1))
            for n in [1, 2, 4, 8]:
                _, t = (None, t1) if n == 1 else cronometrar(lambda n=n: programa_completo(n))
                filas.append({"Workers": n, "Tiempo (s)": round(t, 2),
                              "Speedup predicho": round(amdahl(0.8, n), 2),
                              "Speedup real": round(t1 / t, 2)})
        R["amdahl"] = filas

    if "amdahl" in R:
        st.dataframe(pd.DataFrame(R["amdahl"]), hide_index=True)
        st.caption("Aun con 8 workers el programa no pasa de unos 3.3x: el medio segundo de configuración siempre está ahí.")

# ================================================================== PREGUNTAS
with tab_preguntas:
    st.header("📝 Preguntas")
    st.markdown(
        "Responda usando lo que observa en la app. Al final descargue el archivo con sus respuestas "
        "y súbalo donde le indique el docente. El archivo incluye automáticamente los resultados de los experimentos que ejecutó."
    )
    nombre = st.text_input("Nombre completo")

    st.markdown(
        """
**Pregunta 1 · Hilos.** En la pestaña **1 · Hilos**, ejecute el experimento con 8 sensores y 1, 2, 4 y 8 workers.
¿Qué pasa con el tiempo cada vez que se duplican los workers? ¿Por qué se pueden usar 8 hilos aunque el servidor tenga pocos núcleos?
"""
    )
    r1 = st.text_area("Respuesta 1", key="r1", height=120)

    st.markdown(
        """
**Pregunta 2 · Procesos y NumPy.** Ejecute las comparaciones de las pestañas **2 · Procesos** y **3 · NumPy**.
¿Cuál fue la forma más rápida de procesar los 4 sensores y cuántas veces más rápida que la serial?
¿Por qué los hilos no ayudaron en este caso?
"""
    )
    r2 = st.text_area("Respuesta 2", key="r2", height=120)

    st.markdown(
        """
**Pregunta 3 · Ley de Amdahl.** En el simulador de la pestaña **4 · Ley de Amdahl**, ponga p = 0.75.
Anote el speedup con N = 2, 8 y 64, y el speedup máximo. ¿Vale la pena comprar una máquina de 64 núcleos
para este programa? Justifique.
"""
    )
    r3 = st.text_area("Respuesta 3", key="r3", height=120)

    # ---- armar el archivo
    lineas = [
        "ACTIVIDAD · EFICIENCIA Y PARALELISMO EN PYTHON",
        f"Estudiante: {nombre or '(sin nombre)'}",
        f"Fecha: {datetime.now():%Y-%m-%d %H:%M}",
        f"Núcleos del servidor: {NUCLEOS}",
        "",
        "--- RESPUESTAS ---",
        f"1. {r1 or '(sin responder)'}",
        "",
        f"2. {r2 or '(sin responder)'}",
        "",
        f"3. {r3 or '(sin responder)'}",
        "",
        "--- RESULTADOS MEDIDOS EN LA APP ---",
    ]
    if "hilos" in R:
        h = R["hilos"]
        lineas.append(f"Hilos ({h['sensores']} sensores): " +
                      ", ".join(f"{w} workers = {t:.2f} s" for w, t in zip(h["workers"], h["tiempos"])))
    if "procesos" in R:
        p = R["procesos"]
        lineas.append(f"Procesar 4 sensores: serial {p['serial']:.2f} s, hilos {p['hilos']:.2f} s, procesos {p['procesos']:.2f} s")
    if "tres_formas" in R:
        f = R["tres_formas"]
        lineas.append(f"Tres formas: serial {f['serial']:.2f} s, procesos {f['procesos']:.2f} s, NumPy {f['numpy']:.2f} s")
    if "conversion" in R:
        c = R["conversion"]
        lineas.append(f"°C a °F ({c['lecturas']} lecturas): for {c['for']:.3f} s, NumPy {c['numpy']:.4f} s")
    if "amdahl" in R:
        lineas.append("Amdahl (p = 0.8): " + ", ".join(
            f"N={f['Workers']}: predicho {f['Speedup predicho']}x, real {f['Speedup real']}x" for f in R["amdahl"]))
    if lineas[-1].startswith("---"):
        lineas.append("(no se ejecutó ningún experimento)")

    faltan = [n for n, r in [(1, r1), (2, r2), (3, r3)] if not r.strip()]
    if faltan or not nombre.strip():
        st.warning("Antes de descargar: escriba su nombre y responda las 3 preguntas.")
    st.download_button(
        "⬇ Descargar mis respuestas (.txt)",
        data="\n".join(lineas),
        file_name=f"respuestas_paralelismo_{(nombre or 'estudiante').strip().replace(' ', '_')}.txt",
        mime="text/plain",
        disabled=bool(faltan) or not nombre.strip(),
        type="primary",
    )
