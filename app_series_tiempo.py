"""
Módulo 7 — Series de Tiempo (Computación Avanzada · ET0197)
App interactiva de apoyo al cuaderno de Colab.

Ejecutar localmente:
    streamlit run app_series_tiempo.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(page_title="Series de Tiempo — Sensor IoT", layout="wide")

# -----------------------------------------------------------------
# Generación de datos (cacheada por parámetros)
# -----------------------------------------------------------------
@st.cache_data
def generar_datos(n_dias, amplitud_estacional, nivel_ruido, pendiente_tendencia):
    n_horas = n_dias * 24
    tiempo = pd.date_range(start="2025-01-01", periods=n_horas, freq="h")
    t = np.arange(n_horas)

    tendencia = pendiente_tendencia * t
    estacionalidad = amplitud_estacional * np.sin(2 * np.pi * t / 24 - np.pi / 2)
    ruido = np.random.default_rng(42).normal(0, nivel_ruido, n_horas)

    temperatura = 22 + tendencia + estacionalidad + ruido
    serie = pd.Series(temperatura, index=tiempo, name="temperatura")
    return serie


def crear_ventanas(serie, tamano_ventana):
    valores = serie.values
    X, y = [], []
    for i in range(len(valores) - tamano_ventana):
        X.append(valores[i:i + tamano_ventana])
        y.append(valores[i + tamano_ventana])
    return np.array(X), np.array(y)


def metrica_texto(y_real, y_pred):
    mae = mean_absolute_error(y_real, y_pred)
    rmse = mean_squared_error(y_real, y_pred) ** 0.5
    return f"MAE = {mae:.3f}  |  RMSE = {rmse:.3f}"


# -----------------------------------------------------------------
# Sidebar — controles globales de la serie simulada
# -----------------------------------------------------------------
st.sidebar.header("⚙️ Parámetros del sensor simulado")
n_dias = st.sidebar.slider("Días simulados", min_value=10, max_value=90, value=45, step=5)
amplitud = st.sidebar.slider("Amplitud del ciclo diario (°C)", min_value=0.0, max_value=10.0, value=4.0, step=0.5)
ruido = st.sidebar.slider("Nivel de ruido", min_value=0.0, max_value=3.0, value=0.6, step=0.1)
tendencia_pendiente = st.sidebar.slider("Pendiente de la tendencia", min_value=-0.05, max_value=0.05, value=0.01, step=0.005)

serie = generar_datos(n_dias, amplitud, ruido, tendencia_pendiente)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Estos controles simulan un sensor DHT22 (temperatura). "
    "Cámbialos y observa cómo se transforma cada gráfica en las pestañas."
)

# -----------------------------------------------------------------
# Encabezado
# -----------------------------------------------------------------
st.title("🌡️ Series de Tiempo — Sensor IoT interactivo")
st.caption("Computación Avanzada · ET0197 — Acompaña al cuaderno *Módulo 7 — Series de Tiempo*")

tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Componentes",
    "2️⃣ ACF / PACF",
    "3️⃣ Ventanas deslizantes",
    "4️⃣ Modelos clásicos",
])

# -----------------------------------------------------------------
# Tab 1: Componentes de la serie
# -----------------------------------------------------------------
with tab1:
    st.subheader("Tendencia, estacionalidad y ruido")
    st.write(
        "Ajusta los controles de la barra lateral y observa cómo cada componente "
        "afecta la forma de la serie y su descomposición."
    )

    fig1, ax1 = plt.subplots(figsize=(11, 3))
    ax1.plot(serie.index, serie.values, color="tomato")
    ax1.set_title("Serie simulada — Temperatura (°C)")
    st.pyplot(fig1)

    descomposicion = seasonal_decompose(serie, model="additive", period=24)
    fig2 = descomposicion.plot()
    fig2.set_size_inches(11, 6)
    st.pyplot(fig2)

    st.info(
        "💡 Sube el **ruido** al máximo: el residuo debería crecer y volverse menos estructurado. "
        "Sube la **amplitud del ciclo diario**: la estacionalidad se hace más pronunciada."
    )

# -----------------------------------------------------------------
# Tab 2: ACF / PACF
# -----------------------------------------------------------------
with tab2:
    st.subheader("Autocorrelación (ACF) y autocorrelación parcial (PACF)")
    n_lags = st.slider("Número de lags a mostrar", min_value=12, max_value=168, value=72, step=12)

    col1, col2 = st.columns(2)
    with col1:
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        plot_acf(serie, lags=n_lags, ax=ax3)
        ax3.set_title("ACF")
        st.pyplot(fig3)
    with col2:
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        plot_pacf(serie, lags=n_lags, ax=ax4, method="ywm")
        ax4.set_title("PACF")
        st.pyplot(fig4)

    st.info(
        "💡 Con el ciclo diario activo deberías ver picos de ACF cada 24 horas. "
        "Baja la amplitud del ciclo diario a 0 en la barra lateral y observa cómo desaparecen los picos."
    )

# -----------------------------------------------------------------
# Tab 3: Ventanas deslizantes
# -----------------------------------------------------------------
with tab3:
    st.subheader("De serie de tiempo a datos tabulares (X, y)")
    tamano_ventana = st.slider("Tamaño de la ventana (horas pasadas usadas como predictor)",
                                min_value=3, max_value=72, value=24, step=3)

    X, y = crear_ventanas(serie, tamano_ventana)

    st.write(f"Con esta ventana se generaron **{X.shape[0]} muestras**, cada una con **{X.shape[1]} predictores**.")
    ejemplo = pd.DataFrame(X[:5], columns=[f"t-{tamano_ventana - i}" for i in range(tamano_ventana)])
    ejemplo["y (siguiente valor)"] = y[:5]
    st.dataframe(ejemplo.round(2))

    corte = int(len(X) * 0.8)
    X_train, X_test = X[:corte], X[corte:]
    y_train, y_test = y[:corte], y[corte:]

    modelo = LinearRegression().fit(X_train, y_train)
    pred = modelo.predict(X_test)

    fig5, ax5 = plt.subplots(figsize=(11, 3))
    ax5.plot(y_test, label="Real", color="black")
    ax5.plot(pred, label="Predicho (regresión sobre ventanas)", linestyle="--")
    ax5.legend()
    ax5.set_title("Regresión lineal entrenada sobre ventanas deslizantes")
    st.pyplot(fig5)

    st.success(metrica_texto(y_test, pred))
    st.info(
        "💡 Prueba ventanas muy pequeñas (3-6 horas) vs. muy grandes (48-72 horas) "
        "y observa cómo cambia el error."
    )

# -----------------------------------------------------------------
# Tab 4: Modelos clásicos de pronóstico
# -----------------------------------------------------------------
with tab4:
    st.subheader("Media móvil, suavizado exponencial y ARIMA")

    horas_test = st.slider("Horas a pronosticar (conjunto de prueba)", min_value=24, max_value=240, value=120, step=24)
    train = serie.iloc[:-horas_test]
    test = serie.iloc[-horas_test:]

    modelo_elegido = st.selectbox(
        "Modelo",
        ["Media móvil", "Suavizado exponencial simple", "Holt-Winters", "ARIMA", "SARIMA"],
    )

    if modelo_elegido == "Media móvil":
        ventana_mm = st.slider("Tamaño de la ventana de la media móvil", 6, 72, 24, step=6)
        historial = list(train.values[-ventana_mm:])
        pred_vals = []
        for _ in range(horas_test):
            siguiente = np.mean(historial[-ventana_mm:])
            pred_vals.append(siguiente)
            historial.append(siguiente)
        pronostico = pd.Series(pred_vals, index=test.index)

    elif modelo_elegido == "Suavizado exponencial simple":
        alpha = st.slider("Alpha (peso de la observación más reciente)", 0.05, 0.95, 0.3, step=0.05)
        modelo_fit = SimpleExpSmoothing(train, initialization_method="estimated").fit(smoothing_level=alpha)
        pronostico = modelo_fit.forecast(horas_test)

    elif modelo_elegido == "Holt-Winters":
        modelo_fit = ExponentialSmoothing(
            train, trend="add", seasonal="add", seasonal_periods=24,
            initialization_method="estimated",
        ).fit()
        pronostico = modelo_fit.forecast(horas_test)

    elif modelo_elegido == "ARIMA":
        p = st.slider("p (orden autorregresivo)", 0, 4, 4)
        d = st.slider("d (diferenciación)", 0, 2, 1)
        q = st.slider("q (orden de media móvil)", 0, 4, 2)
        with st.spinner("Ajustando ARIMA..."):
            modelo_fit = ARIMA(train, order=(p, d, q)).fit()
        pronostico = modelo_fit.forecast(horas_test)
        st.caption(
            "💡 Este modelo NO tiene noción explícita de estacionalidad: solo puede "
            "'imitar' el ciclo de 24 horas subiendo p. Compáralo con SARIMA más abajo."
        )

    else:  # SARIMA
        st.markdown("**Parte no estacional** — igual que ARIMA, sobre los rezagos cercanos:")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            p = st.slider("p", 0, 3, 2)
        with col_b:
            d = st.slider("d", 0, 2, 0)
        with col_c:
            q = st.slider("q", 0, 3, 2)

        st.markdown("**Parte estacional** — los mismos conceptos, aplicados cada `s` horas:")
        col_d, col_e, col_f, col_g = st.columns(4)
        with col_d:
            P = st.slider("P (AR estacional)", 0, 2, 1)
        with col_e:
            D = st.slider("D (diferenciación estacional)", 0, 1, 0)
        with col_f:
            Q = st.slider("Q (MA estacional)", 0, 2, 1)
        with col_g:
            s = st.slider("s (período estacional)", 6, 48, 24, step=6)

        with st.spinner("Ajustando SARIMA..."):
            modelo_fit = SARIMAX(
                train, order=(p, d, q), seasonal_order=(P, D, Q, s),
                enforce_stationarity=False, enforce_invertibility=False,
            ).fit(disp=False)
        pronostico = modelo_fit.forecast(horas_test)

        if s != 24:
            st.warning(
                f"⚠️ Declaraste s={s}, pero el ciclo real del sensor es de 24 horas. "
                "Observa cómo empeora el error cuando el período estacional no coincide con el real."
            )
        else:
            st.caption(
                "💡 s=24 le dice al modelo 'compara cada hora con la misma hora del día anterior'. "
                "Prueba subir P o Q, o cambiar s, y observa el efecto en el error."
            )

    fig6, ax6 = plt.subplots(figsize=(11, 4))
    ax6.plot(test.index, test.values, label="Real", color="black", linewidth=2)
    ax6.plot(test.index, pronostico.values, label=f"Pronóstico ({modelo_elegido})", linestyle="--", color="tomato")
    ax6.legend()
    ax6.set_title(f"Pronóstico — {modelo_elegido}")
    st.pyplot(fig6)

    st.success(metrica_texto(test.values, pronostico.values))
    st.info(
        "💡 Compara los cinco modelos con los mismos parámetros del sensor. "
        "¿Cuál mantiene el error más bajo cuando subes el ruido en la barra lateral? "
        "¿SARIMA logra superar a Holt-Winters?"
    )
