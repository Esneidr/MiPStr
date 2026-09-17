import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    accuracy_score,
    precision_score,
    recall_score,
)

st.set_page_config(page_title="¿Lloverá mañana? — Regresión Logística", layout="wide")


# ----------------------------------------------------------------------
# 1. Datos (los mismos del Colab, generados una sola vez)
# ----------------------------------------------------------------------
@st.cache_data
def generar_datos(n=300, seed=42):
    rng = np.random.default_rng(seed)
    temperatura = rng.normal(24, 5, n)
    humedad = rng.normal(65, 15, n)
    viento = rng.normal(10, 5, n)

    z = -6 + 0.09 * humedad - 0.05 * temperatura + 0.02 * viento
    prob_real = 1 / (1 + np.exp(-z))
    llovio = (rng.random(n) < prob_real).astype(int)

    return pd.DataFrame(
        {
            "temperatura": temperatura.round(1),
            "humedad": humedad.round(1),
            "viento": viento.round(1),
            "llovio": llovio,
        }
    )


df = generar_datos()

st.title("🌧️ ¿Lloverá mañana? — Regresión Logística interactiva")
st.markdown(
    "Complemento del Colab: usa los controles de la izquierda para responder las "
    "preguntas de la actividad (variables, umbral, importancia de cada variable, "
    "falsos positivos vs. falsos negativos)."
)

# ----------------------------------------------------------------------
# 2. Controles (barra lateral)
# ----------------------------------------------------------------------
st.sidebar.header("⚙️ Configuración del modelo")

usar_temp = st.sidebar.checkbox("Usar temperatura", value=True)
usar_humedad = st.sidebar.checkbox("Usar humedad", value=True)
usar_viento = st.sidebar.checkbox("Usar viento", value=True)

variables = [v for v, usar in [
    ("temperatura", usar_temp),
    ("humedad", usar_humedad),
    ("viento", usar_viento),
] if usar]

if len(variables) == 0:
    st.sidebar.error("Selecciona al menos una variable para entrenar el modelo.")
    st.stop()

umbral = st.sidebar.slider(
    "Umbral de clasificación", min_value=0.0, max_value=1.0, value=0.5, step=0.05
)

st.sidebar.header("🌤️ Simular un nuevo día")
temp_input = st.sidebar.slider("Temperatura (°C)", 5.0, 40.0, 24.0, 0.5)
humedad_input = st.sidebar.slider("Humedad (%)", 0.0, 100.0, 85.0, 1.0)
viento_input = st.sidebar.slider("Viento (km/h)", 0.0, 40.0, 12.0, 0.5)

nuevo_dia_completo = pd.DataFrame(
    {"temperatura": [temp_input], "humedad": [humedad_input], "viento": [viento_input]}
)


# ----------------------------------------------------------------------
# 3. Entrenamiento (se re-entrena al vuelo según variables elegidas)
# ----------------------------------------------------------------------
@st.cache_data
def entrenar_modelo(df, variables):
    X = df[variables]
    y = df["llovio"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    modelo = LogisticRegression(solver="lbfgs")
    modelo.fit(X_train, y_train)
    return modelo, X_test, y_test


modelo, X_test, y_test = entrenar_modelo(df, variables)
prob_test = modelo.predict_proba(X_test)[:, 1]
pred_test = (prob_test >= umbral).astype(int)

prob_nuevo = modelo.predict_proba(nuevo_dia_completo[variables])[0, 1]
pred_nuevo = "Sí lloverá 🌧️" if prob_nuevo >= umbral else "No lloverá ☀️"

# ----------------------------------------------------------------------
# 4. Layout principal
# ----------------------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📍 Predicción para el nuevo día")
    st.metric("Probabilidad de lluvia", f"{prob_nuevo:.2%}")
    st.metric("Predicción (con el umbral elegido)", pred_nuevo)

    st.subheader("📈 Curva sigmoide")
    z_vals = np.linspace(-10, 10, 200)
    sigmoide = 1 / (1 + np.exp(-z_vals))
    z_nuevo = np.log(prob_nuevo / (1 - prob_nuevo)) if 0 < prob_nuevo < 1 else 0

    fig_sig, ax_sig = plt.subplots(figsize=(5, 3.5))
    ax_sig.plot(z_vals, sigmoide, color="darkblue")
    ax_sig.axhline(umbral, color="gray", linestyle="--", linewidth=1, label=f"Umbral = {umbral}")
    ax_sig.scatter([z_nuevo], [prob_nuevo], color="red", zorder=5, label="Nuevo día")
    ax_sig.set_xlabel("z")
    ax_sig.set_ylabel("Probabilidad")
    ax_sig.legend()
    st.pyplot(fig_sig)

with col2:
    st.subheader("🗺️ Temperatura vs. Humedad")
    colores = df["llovio"].map({0: "skyblue", 1: "darkblue"})
    fig_scatter, ax_scatter = plt.subplots(figsize=(5, 4))
    ax_scatter.scatter(df["temperatura"], df["humedad"], c=colores, alpha=0.6, edgecolor="k")
    ax_scatter.scatter(
        [temp_input], [humedad_input], color="red", s=120, edgecolor="black",
        marker="*", zorder=5, label="Nuevo día"
    )
    ax_scatter.set_xlabel("Temperatura (°C)")
    ax_scatter.set_ylabel("Humedad (%)")
    ax_scatter.legend()
    st.pyplot(fig_scatter)

    st.subheader("⚖️ Importancia de cada variable")
    coefs = pd.Series(modelo.coef_[0], index=variables).sort_values(key=abs, ascending=False)
    fig_coef, ax_coef = plt.subplots(figsize=(5, 2.5))
    coefs.plot(kind="barh", color="steelblue", ax=ax_coef)
    ax_coef.set_xlabel("Coeficiente (peso en el modelo)")
    ax_coef.invert_yaxis()
    st.pyplot(fig_coef)

st.divider()

# ----------------------------------------------------------------------
# 5. Métricas sobre el conjunto de prueba
# ----------------------------------------------------------------------
st.subheader("📊 Desempeño del modelo (conjunto de prueba)")

col3, col4 = st.columns([1, 1])

with col3:
    matriz = confusion_matrix(y_test, pred_test)
    fig_cm, ax_cm = plt.subplots(figsize=(4, 4))
    disp = ConfusionMatrixDisplay(matriz, display_labels=["No llueve", "Sí llueve"])
    disp.plot(cmap="Blues", values_format="d", ax=ax_cm, colorbar=False)
    st.pyplot(fig_cm)

with col4:
    exactitud = accuracy_score(y_test, pred_test)
    precision = precision_score(y_test, pred_test, zero_division=0)
    recall = recall_score(y_test, pred_test, zero_division=0)

    vn, fp, fn, vp = matriz.ravel()

    st.metric("Accuracy", f"{exactitud:.2%}")
    st.metric("Precisión", f"{precision:.2%}")
    st.metric("Recall", f"{recall:.2%}")
    st.write(f"**Falsos positivos:** {fp}  |  **Falsos negativos:** {fn}")

    if fp > fn:
        st.info("Con este umbral y estas variables, el modelo comete más **falsos positivos** (falsas alarmas de lluvia).")
    elif fn > fp:
        st.info("Con este umbral y estas variables, el modelo comete más **falsos negativos** (lluvias no detectadas).")
    else:
        st.info("El modelo comete la misma cantidad de falsos positivos y falsos negativos.")

st.divider()
st.markdown(
    """
### 🧠 Preguntas para responder interactuando con la app

1. Desmarca **viento** en la barra lateral. ¿Cambian mucho el accuracy, la precisión o el recall?
2. Sube el umbral a **0.7**. ¿El modelo predice más o menos días de lluvia? ¿Qué pasa con los falsos negativos?
3. Mirando el gráfico de **importancia de variables**, ¿cuál tiene el coeficiente más grande en valor absoluto?
4. Ajusta la humedad del "nuevo día" a un valor muy alto (>90%) y luego muy bajo (<30%). ¿Cómo cambia la probabilidad de lluvia?
5. ¿En qué combinación de umbral y variables el modelo comete más falsos positivos que falsos negativos? ¿Y al revés?
"""
)
