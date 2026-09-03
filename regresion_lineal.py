"""
Módulo 6 — Regresión
App educativa: visualización interactiva de los conceptos principales

Cubre:
  1. Regresión lineal simple (ajuste manual vs. óptimo)
  2. Regresión lineal múltiple (coeficientes e importancia de variables)
  3. Función de costo (MSE) y el gradiente
  4. Descenso de gradiente (convergencia)
  5. Métricas de evaluación: R², MAE, RMSE

Ejecutar con:  streamlit run regresion_conceptos_app.py
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

st.set_page_config(page_title="Regresión — Conceptos clave", layout="wide")

FEATURES = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup"]
FEATURE_LABELS = {
    "MedInc": "Ingreso medio",
    "HouseAge": "Edad de la vivienda",
    "AveRooms": "Habitaciones promedio",
    "AveBedrms": "Dormitorios promedio",
    "Population": "Población",
    "AveOccup": "Ocupantes promedio",
}

# ------------------------------------------------------------------
# Datos (reales: censo de vivienda de California)
# ------------------------------------------------------------------
@st.cache_data
def cargar_datos():
    housing = fetch_california_housing(as_frame=True)
    df = housing.frame.sample(n=1200, random_state=42).reset_index(drop=True)
    return df

df = cargar_datos()

st.title("📈 Regresión — Conceptos clave")
st.markdown(
    "La regresión permite predecir valores numéricos a partir de datos históricos. "
    "Esta app recorre, de forma interactiva, las piezas que componen un modelo de regresión: "
    "**el modelo, la función de costo, el gradiente, el algoritmo de aprendizaje y las métricas "
    "para evaluar qué tan bien predice.** Todo con datos reales de vivienda en California."
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣ Regresión simple",
    "2️⃣ Regresión múltiple",
    "3️⃣ Costo y gradiente",
    "4️⃣ Descenso de gradiente",
    "5️⃣ Métricas de evaluación",
])

# ====================================================================
# TAB 1 — REGRESIÓN SIMPLE
# ====================================================================
with tab1:
    st.header("Regresión lineal simple")
    st.markdown(
        r"""
Un modelo de regresión lineal simple predice un valor con una sola variable de entrada:

$$\hat{y} = w \cdot x + b$$

Mueve `w` (pendiente) y `b` (intercepto) manualmente y observa cómo cambia el error,
o deja que el algoritmo encuentre el ajuste óptimo.
"""
    )

    col_a, col_b = st.columns([1, 2])

    with col_a:
        var_simple = st.selectbox(
            "Variable predictora", FEATURES,
            format_func=lambda v: f"{v} — {FEATURE_LABELS[v]}",
            key="var_simple",
        )
        x = df[var_simple].values
        y = df["MedHouseVal"].values

        modo = st.radio("Modo", ["Ajuste manual", "Ajuste óptimo (automático)"], key="modo_simple")

        if modo == "Ajuste manual":
            w_manual = st.slider("w (pendiente)", -3.0, 3.0, 0.0, 0.01)
            b_manual = st.slider("b (intercepto)", -3.0, 3.0, float(y.mean()), 0.01)
            w_used, b_used = w_manual, b_manual
        else:
            modelo = LinearRegression()
            modelo.fit(x.reshape(-1, 1), y)
            w_used, b_used = modelo.coef_[0], modelo.intercept_
            st.info(f"w óptimo = {w_used:.4f}  ·  b óptimo = {b_used:.4f}", icon="✅")

        y_pred = w_used * x + b_used
        mse_actual = np.mean((y_pred - y) ** 2)
        st.metric("Error actual (MSE)", f"{mse_actual:.4f}")

    with col_b:
        fig, ax = plt.subplots(figsize=(6, 4.2))
        ax.scatter(x, y, alpha=0.15, s=12, color="#4C72B0")
        x_line = np.linspace(x.min(), x.max(), 100)
        ax.plot(x_line, w_used * x_line + b_used, color="red", linewidth=2.5)
        ax.set_xlabel(f"{var_simple} ({FEATURE_LABELS[var_simple]})")
        ax.set_ylabel("MedHouseVal (valor de vivienda)")
        ax.set_title(f"ŷ = {w_used:.3f}·x + {b_used:.3f}")
        st.pyplot(fig)

    st.caption(
        "💡 En modo manual, intenta minimizar el MSE moviendo los sliders. "
        "Luego compara contra el ajuste automático: ese es exactamente el problema que resuelve el entrenamiento."
    )

# ====================================================================
# TAB 2 — REGRESIÓN MÚLTIPLE
# ====================================================================
with tab2:
    st.header("Regresión lineal múltiple")
    st.markdown(
        r"""
En la práctica, varias variables influyen a la vez en la predicción:

$$\hat{y} = w_1 x_1 + w_2 x_2 + \dots + w_k x_k + b$$

Selecciona qué variables incluir y observa cómo cambian los coeficientes y el desempeño del modelo.
"""
    )

    vars_multiples = st.multiselect(
        "Variables a incluir en el modelo",
        FEATURES,
        default=["MedInc", "HouseAge", "AveRooms"],
        format_func=lambda v: f"{v} — {FEATURE_LABELS[v]}",
    )

    if len(vars_multiples) == 0:
        st.warning("Selecciona al menos una variable.")
    else:
        X = df[vars_multiples]
        y = df["MedHouseVal"]

        modelo_m = LinearRegression()
        modelo_m.fit(X, y)
        y_pred_m = modelo_m.predict(X)

        col_c, col_d = st.columns(2)

        with col_c:
            st.markdown("**Coeficientes aprendidos**")
            coefs = pd.Series(modelo_m.coef_, index=vars_multiples).sort_values()
            fig2, ax2 = plt.subplots(figsize=(5, 3.5))
            coefs.plot(kind="barh", ax=ax2, color="#55A868")
            ax2.axvline(0, color="black", linewidth=0.8)
            ax2.set_xlabel("Coeficiente (w)")
            st.pyplot(fig2)
            st.caption(f"Intercepto (b) = {modelo_m.intercept_:.4f}")

        with col_d:
            st.markdown("**Real vs. predicho**")
            fig3, ax3 = plt.subplots(figsize=(5, 3.5))
            ax3.scatter(y, y_pred_m, alpha=0.15, s=12, color="#C44E52")
            lims = [min(y.min(), y_pred_m.min()), max(y.max(), y_pred_m.max())]
            ax3.plot(lims, lims, "--", color="black", linewidth=1)
            ax3.set_xlabel("Valor real")
            ax3.set_ylabel("Valor predicho")
            r2_m = r2_score(y, y_pred_m)
            ax3.set_title(f"R² = {r2_m:.3f}")
            st.pyplot(fig3)

        st.caption(
            "💡 Agrega o quita variables y observa: más variables relevantes normalmente mejora el R², "
            "pero cada coeficiente representa el efecto de esa variable manteniendo las demás fijas."
        )

# ====================================================================
# TAB 3 — FUNCIÓN DE COSTO Y GRADIENTE
# ====================================================================
with tab3:
    st.header("Función de costo (MSE) y el gradiente")
    st.markdown(
        r"""
El error cuadrático medio mide qué tan mal predice el modelo:

$$J(w) = \frac{1}{n}\sum_{i=1}^{n}(w x_i + b - y_i)^2$$

Es una función con forma de "tazón": tiene un único mínimo. El **gradiente** es la pendiente
de esa curva en un punto — indica hacia dónde y qué tanto hay que mover `w` para reducir el error.
"""
    )

    var_costo = st.selectbox(
        "Variable", FEATURES, format_func=lambda v: f"{v} — {FEATURE_LABELS[v]}", key="var_costo"
    )
    x_c = df[var_costo].values
    y_c = df["MedHouseVal"].values
    x_norm = (x_c - x_c.mean()) / x_c.std()
    y_norm = (y_c - y_c.mean()) / y_c.std()

    modelo_c = LinearRegression()
    modelo_c.fit(x_norm.reshape(-1, 1), y_norm)
    w_opt, b_opt = modelo_c.coef_[0], modelo_c.intercept_

    w_probe = st.slider(
        "Explora distintos valores de w (b fijo en su valor óptimo)",
        float(w_opt - 2), float(w_opt + 2), float(w_opt), 0.01,
    )

    def mse(w, b, x, y):
        return np.mean((w * x + b - y) ** 2)

    def grad_w(w, b, x, y):
        return (2 / len(x)) * np.sum((w * x + b - y) * x)

    w_range = np.linspace(w_opt - 2, w_opt + 2, 200)
    costos = [mse(w, b_opt, x_norm, y_norm) for w in w_range]

    costo_actual = mse(w_probe, b_opt, x_norm, y_norm)
    gradiente_actual = grad_w(w_probe, b_opt, x_norm, y_norm)

    col_e, col_f = st.columns([2, 1])

    with col_e:
        fig4, ax4 = plt.subplots(figsize=(6, 4.2))
        ax4.plot(w_range, costos, color="#4C72B0", linewidth=2)
        ax4.axvline(w_opt, color="green", linestyle="--", linewidth=1, label=f"w óptimo ≈ {w_opt:.3f}")
        ax4.scatter([w_probe], [costo_actual], color="red", s=80, zorder=5, label="Tu punto actual")

        # Recta tangente (visualiza el gradiente)
        tang_x = np.linspace(w_probe - 0.6, w_probe + 0.6, 20)
        tang_y = costo_actual + gradiente_actual * (tang_x - w_probe)
        ax4.plot(tang_x, tang_y, color="orange", linewidth=2, label="Tangente (gradiente)")

        ax4.set_xlabel("w")
        ax4.set_ylabel("J(w)  —  MSE")
        ax4.set_title("Función de costo — el 'tazón'")
        ax4.legend(fontsize=8)
        st.pyplot(fig4)

    with col_f:
        st.metric("Costo J(w)", f"{costo_actual:.4f}")
        st.metric("Gradiente ∂J/∂w", f"{gradiente_actual:.4f}")
        if abs(gradiente_actual) < 0.02:
            st.success("Gradiente ≈ 0 → estás cerca del mínimo ✅")
        elif gradiente_actual > 0:
            st.warning("Gradiente positivo → hay que **disminuir** w")
        else:
            st.warning("Gradiente negativo → hay que **aumentar** w")

    st.caption(
        "💡 El gradiente es la pendiente de la tangente (línea naranja). Cuando es 0, estás en el mínimo — "
        "el punto de menor error. Esa es la señal que usa el descenso de gradiente para actualizar w."
    )

# ====================================================================
# TAB 4 — DESCENSO DE GRADIENTE
# ====================================================================
with tab4:
    st.header("Descenso de gradiente")
    st.markdown(
        r"""
El algoritmo que "aprende" los parámetros óptimos, iteración por iteración:

$$w \leftarrow w - \alpha \frac{\partial J}{\partial w} \qquad b \leftarrow b - \alpha \frac{\partial J}{\partial b}$$

Configura el *learning rate* (`α`) y el número de iteraciones, y observa cómo converge (o diverge).
"""
    )

    col_g, col_h = st.columns([1, 2])

    with col_g:
        var_gd = st.selectbox(
            "Variable", FEATURES, format_func=lambda v: f"{v} — {FEATURE_LABELS[v]}", key="var_gd"
        )
        alpha_gd = st.slider("Learning rate (α)", 0.001, 1.0, 0.1, 0.001, key="alpha_gd")
        epochs_gd = st.slider("Iteraciones", 5, 200, 50, key="epochs_gd")

    x_gd = df[var_gd].values
    y_gd = df["MedHouseVal"].values
    x_gd_n = (x_gd - x_gd.mean()) / x_gd.std()
    y_gd_n = (y_gd - y_gd.mean()) / y_gd.std()

    def descenso_gradiente(x, y, alpha, epochs):
        n = len(x)
        w, b = 0.0, 0.0
        historial = []
        for _ in range(epochs):
            pred = w * x + b
            error = pred - y
            gw = (2 / n) * np.sum(error * x)
            gb = (2 / n) * np.sum(error)
            w -= alpha * gw
            b -= alpha * gb
            historial.append(np.mean(error ** 2))
        return w, b, historial

    w_final, b_final, historial_costo = descenso_gradiente(x_gd_n, y_gd_n, alpha_gd, epochs_gd)

    with col_g:
        st.metric("w final", f"{w_final:.4f}")
        st.metric("b final", f"{b_final:.4f}")
        st.metric("Costo final", f"{historial_costo[-1]:.4f}")
        if historial_costo[-1] > historial_costo[0]:
            st.error("⚠️ El costo aumentó — el α es demasiado grande (diverge)")

    with col_h:
        fig5, ax5 = plt.subplots(figsize=(6, 4.2))
        ax5.plot(historial_costo, color="#DD8452", linewidth=2)
        ax5.set_xlabel("Iteración")
        ax5.set_ylabel("Costo (MSE)")
        ax5.set_title(f"Convergencia — α = {alpha_gd}")
        st.pyplot(fig5)

    st.caption(
        "💡 Prueba un α muy pequeño (converge lento) y uno muy grande (puede oscilar o divergir). "
        "El valor adecuado depende de cada problema — por eso se explora experimentalmente."
    )

# ====================================================================
# TAB 5 — MÉTRICAS DE EVALUACIÓN
# ====================================================================
with tab5:
    st.header("Métricas de evaluación: R², MAE, RMSE")
    st.markdown(
        r"""
Con el modelo entrenado, necesitamos medir qué tan bien predice sobre datos **nunca vistos**:

- **MAE** — error absoluto promedio, en las unidades originales.
- **RMSE** — penaliza más los errores grandes; es $\sqrt{MSE}$.
- **R²** — proporción de la variabilidad de `y` que el modelo logra explicar (0 a 1).
"""
    )

    vars_metricas = st.multiselect(
        "Variables del modelo",
        FEATURES,
        default=["MedInc", "HouseAge", "AveRooms", "Population"],
        format_func=lambda v: f"{v} — {FEATURE_LABELS[v]}",
        key="vars_metricas",
    )
    test_size = st.slider("Proporción de datos de prueba", 0.1, 0.5, 0.2, 0.05)

    if len(vars_metricas) == 0:
        st.warning("Selecciona al menos una variable.")
    else:
        X = df[vars_metricas]
        y = df["MedHouseVal"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        modelo_met = LinearRegression()
        modelo_met.fit(X_train, y_train)
        y_pred_test = modelo_met.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        r2 = r2_score(y_test, y_pred_test)

        col_i, col_j, col_k = st.columns(3)
        col_i.metric("MAE", f"{mae:.3f}")
        col_j.metric("RMSE", f"{rmse:.3f}")
        col_k.metric("R²", f"{r2:.3f}", help="1.0 = predicción perfecta, 0.0 = igual que predecir siempre el promedio")

        fig6, ax6 = plt.subplots(figsize=(6, 4.2))
        ax6.scatter(y_test, y_pred_test, alpha=0.2, s=14, color="#8172B2")
        lims = [min(y_test.min(), y_pred_test.min()), max(y_test.max(), y_pred_test.max())]
        ax6.plot(lims, lims, "--", color="black", linewidth=1, label="Predicción perfecta")
        ax6.set_xlabel("Valor real")
        ax6.set_ylabel("Valor predicho")
        ax6.set_title("Desempeño sobre datos de PRUEBA (nunca vistos)")
        ax6.legend()
        st.pyplot(fig6)

        st.caption(
            "💡 Estas métricas se calculan sobre el conjunto de **prueba**, no el de entrenamiento — "
            "así sabemos si el modelo generaliza a datos nuevos, no solo si memorizó los que ya vio."
        )

st.markdown("---")
st.caption(
    "Datos: censo de vivienda de California (1990), vía scikit-learn. "
    "App complementaria al Módulo 6 — Regresión."
)
