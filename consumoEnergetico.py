import inspect

import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Modelo de consumo", page_icon="⚡")

# ------------------------------------------------------------------
# Cargar el modelo entrenado en el Colab
# ------------------------------------------------------------------
@st.cache_resource
def cargar_modelo():
    return joblib.load("modelo_consumo.joblib")


flujo = cargar_modelo()
pre = flujo.preprocesador
modelo = flujo.modelo
COLUMNAS = ["temperatura", "ocupacion", "humedad"]

st.title("⚡ Modelo de consumo energético")
st.write(
    f"Objeto cargado: **{type(flujo).__name__}**, que contiene un "
    f"**{type(pre).__name__}** y un **{type(modelo).__name__}**."
)

tab1, tab2, tab3 = st.tabs(["1. Atributos", "2. Métodos", "3. Probar el modelo"])

# ------------------------------------------------------------------
# 1. ATRIBUTOS: lo que cada objeto sabe (lo que guardó el .joblib)
# ------------------------------------------------------------------
with tab1:
    st.subheader(f"Atributos de {type(pre).__name__}")
    st.table(pd.DataFrame({"media": pre.media, "desv": pre.desv}, index=COLUMNAS).round(2))

    st.subheader(f"Atributos de {type(modelo).__name__}")
    st.write(f"`tasa` = {modelo.tasa}  ·  `iteraciones` = {modelo.iteraciones}  ·  `b` = {modelo.b:.2f}")
    st.table(pd.DataFrame({"w (peso)": modelo.w}, index=COLUMNAS).round(2))

    st.write(f"`historial`: lista con {len(modelo.historial)} valores del costo durante el entrenamiento")
    st.line_chart(pd.DataFrame({"costo (MSE)": modelo.historial}))

    st.info("Prueba: ¿qué variable tiene el peso más grande? ¿Qué dice eso del consumo del edificio?")

# ------------------------------------------------------------------
# 2. MÉTODOS: lo que cada objeto sabe hacer, y en qué clase está escrito
# ------------------------------------------------------------------
with tab2:
    st.write("La columna **definido en** muestra la herencia: si no es la clase del objeto, el método se heredó.")

    for objeto in [flujo, pre, modelo]:
        clase = type(objeto)
        st.subheader(clase.__name__)
        st.caption("Herencia: " + " → ".join(c.__name__ for c in clase.__mro__))

        filas = []
        for nombre, funcion in inspect.getmembers(clase, inspect.isfunction):
            if nombre.startswith("_") and nombre != "__init__":
                continue
            filas.append({
                "método": nombre,
                "parámetros": str(inspect.signature(funcion)),
                "definido en": funcion.__qualname__.split(".")[0],
            })
        st.table(pd.DataFrame(filas))

    st.subheader("Ver el código de un método")
    nombre = st.selectbox("Método del modelo", ["fit", "predict", "score", "__init__"])
    st.code(inspect.getsource(getattr(type(modelo), nombre)), language="python")

    st.info("Prueba: ¿en qué clase está escrito `fit`? ¿Y `predict`? ¿Por qué no están en la misma?")

# ------------------------------------------------------------------
# 3. PROBAR EL MODELO: una lectura nueva, paso a paso
# ------------------------------------------------------------------
with tab3:
    t = st.slider("Temperatura (°C)", 18.0, 34.0, 26.0)
    o = st.slider("Ocupación (personas)", 0, 50, 25)
    h = st.slider("Humedad (%)", 40.0, 90.0, 70.0)
    lectura = np.array([[t, o, h]])

    st.metric("Consumo estimado", f"{flujo.predecir(lectura)[0]:.1f} kWh")

    st.subheader("Qué hizo `flujo.predecir()` por dentro")
    x_std = pre.transform(lectura)[0]
    st.write("**Paso 1 · `preprocesador.transform()`** usa `media` y `desv`:")
    st.table(pd.DataFrame(
        {"lectura": lectura[0], "estandarizada": x_std, "w (peso)": modelo.w, "aporte = w · x": modelo.w * x_std},
        index=COLUMNAS,
    ).round(2))
    st.write(
        f"**Paso 2 · `modelo.predict()`** suma los aportes y el sesgo: "
        f"{np.sum(modelo.w * x_std):.2f} + b ({modelo.b:.2f}) = **{np.sum(modelo.w * x_std) + modelo.b:.1f} kWh**"
    )

    st.info("Prueba: mueve la ocupación de 0 a 50 y luego la humedad de 40 a 90. ¿Cuál cambia más el consumo? ¿Coincide con los pesos de la pestaña 1?")
