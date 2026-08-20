"""
Módulo 3 — Cálculo Aplicado / Gradiente
App interactiva de Descenso de Gradiente (solo librerías estándar)

Ejecutar con:
    streamlit run app_gradiente.py

Dependencias:
    pip install streamlit numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib import cm
import streamlit as st

# =========================================================
# Configuración general de la página
# =========================================================
st.set_page_config(
    page_title="Descenso de Gradiente — Módulo 3",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Descenso de Gradiente Interactivo")
st.markdown(
    """
Explora en vivo cómo la **tasa de aprendizaje ($\\eta$)** y el **punto inicial**
afectan la convergencia del descenso de gradiente. Este es el complemento
práctico del notebook de Cálculo Aplicado.
"""
)

def f2(x, y):
    """Función objetivo. Por defecto: un 'tazón' con mínimo en (0, 0)."""
    return (x - 3) ** 2 + (y + 2) ** 2


def gradiente_f2(x, y):
    """Gradiente de f2: vector de derivadas parciales [df/dx, df/dy]."""
    return np.array([2 * (x - 3), 2 * (y + 2)])


def descenso_gradiente(grad_func, punto_inicial, tasa_aprendizaje, iteraciones):
    """Ejecuta el descenso de gradiente y devuelve el historial de puntos visitados."""
    punto = np.array(punto_inicial, dtype=float)
    historial = [punto.copy()]
    for _ in range(iteraciones):
        grad = grad_func(*punto)
        punto = punto - tasa_aprendizaje * grad
        if not np.all(np.isfinite(punto)) or np.linalg.norm(punto) > 1e6:
            historial.append(punto.copy())
            break
        historial.append(punto.copy())
    return np.array(historial)


@st.cache_data
def encontrar_minimo(_grid_x, _grid_y, iteraciones=3000, eta=0.05):
    """
    Encuentra el mínimo de f2 de forma automática:
    1. Busca el mejor punto de partida en la rejilla (el de menor f2).
    2. Refina ese punto con descenso de gradiente (usando gradiente_f2)
       muchas iteraciones y una tasa de aprendizaje pequeña, para
       converger con precisión sin importar dónde esté el mínimo real.
    """
    Z = f2(_grid_x, _grid_y)
    idx = np.unravel_index(np.argmin(Z), Z.shape)
    punto_inicial = (float(_grid_x[idx]), float(_grid_y[idx]))
    historial = descenso_gradiente(gradiente_f2, punto_inicial, eta, iteraciones)
    return tuple(historial[-1])


def clasificar_convergencia(historial, minimo):
    """Clasifica el resultado del descenso: converge, oscila o diverge."""
    distancias = np.linalg.norm(historial - np.array(minimo), axis=1)
    if not np.all(np.isfinite(distancias)) or distancias[-1] > distancias[0] * 1.5:
        return "diverge", "🔴"
    diffs = np.diff(historial[:, 0])
    if len(diffs) > 3:
        cambios_signo = np.sum(np.diff(np.sign(diffs)) != 0)
        if cambios_signo > len(diffs) * 0.35:
            return "oscila", "🟠"
    return "converge", "🟢"


# Rejilla fija de la superficie (se reutiliza en varios gráficos)
_grid = np.linspace(-4, 4, 60)
_X, _Y = np.meshgrid(_grid, _grid)
_Z = f2(_X, _Y)

# Mínimo calculado automáticamente a partir de f2 y gradiente_f2
MINIMO = encontrar_minimo(_X, _Y)


def figura_3d(historial, titulo="", elev=25, azim=-50):
    """Superficie 3D + trayectoria del descenso de gradiente (matplotlib)."""
    zs_hist = f2(historial[:, 0], historial[:, 1])

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(_X, _Y, _Z, cmap=cm.viridis, alpha=0.5, linewidth=0)

    ax.plot(historial[:, 0], historial[:, 1], zs_hist, color="red",
            linewidth=2.5, marker="o", markersize=4, label="Trayectoria")
    ax.scatter([historial[0, 0]], [historial[0, 1]], [zs_hist[0]],
               color="orange", s=90, label="Inicio", zorder=10)
    ax.scatter([historial[-1, 0]], [historial[-1, 1]], [zs_hist[-1]],
               color="lime", s=90, label="Final", zorder=10)
    ax.scatter([MINIMO[0]], [MINIMO[1]], [f2(*MINIMO)], color="gold",
               edgecolor="black", s=80, label="Mínimo global", zorder=10)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x, y)")
    ax.set_title(titulo)
    ax.view_init(elev=elev, azim=azim)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    return fig


def figura_convergencia(historial):
    """Curva de f(x,y) contra el número de iteración."""
    valores = f2(historial[:, 0], historial[:, 1])
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.plot(valores, "-o", color="crimson", linewidth=2, markersize=3)
    ax.set_xlabel("Iteración")
    ax.set_ylabel("f(x, y)")
    ax.set_title("Convergencia de f(x, y) por iteración")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


# =========================================================
# Barra lateral — controles interactivos
# =========================================================
with st.sidebar:
    st.header("⚙️ Parámetros")
    st.caption(f"Mínimo detectado automáticamente en ({MINIMO[0]:.2f}, {MINIMO[1]:.2f})")

    eta = st.slider(
        "Tasa de aprendizaje (η)",
        min_value=0.01, max_value=1.1, value=0.1, step=0.01,
        help="Qué tan grande es cada paso del descenso.",
    )
    x0 = st.slider("Punto inicial x₀", -4.0, 4.0, 2.5, 0.1)
    y0 = st.slider("Punto inicial y₀", -4.0, 4.0, 2.5, 0.1)
    iteraciones = st.slider("Número de iteraciones", 5, 150, 30, 5)

    st.markdown("---")
    modo_comparacion = st.checkbox(
        "Comparar 4 tasas de aprendizaje a la vez", value=False
    )

historial = descenso_gradiente(gradiente_f2, (x0, y0), eta, iteraciones)
estado, icono = clasificar_convergencia(historial, MINIMO)

# =========================================================
# Métricas rápidas
# =========================================================
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Estado", f"{icono} {estado.capitalize()}")
col_m2.metric("f(inicio)", f"{f2(x0, y0):.3f}")
valor_final = f2(*historial[-1]) if np.all(np.isfinite(historial[-1])) else float("nan")
col_m3.metric("f(final)", f"{valor_final:.4f}" if np.isfinite(valor_final) else "∞")
col_m4.metric("Pasos dados", f"{len(historial) - 1}")

st.markdown("---")

# =========================================================
# Vista principal
# =========================================================
if not modo_comparacion:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.pyplot(figura_3d(historial, f"Trayectoria con η = {eta}"))
    with col2:
        st.pyplot(figura_convergencia(historial))

        if estado == "diverge":
            st.error(
                "Con esta tasa de aprendizaje el algoritmo **diverge**: cada paso "
                "se aleja más del mínimo en vez de acercarse. Prueba bajar η."
            )
        elif estado == "oscila":
            st.warning(
                "El algoritmo **oscila** alrededor del mínimo: converge, pero de "
                "forma inestable. Bajar un poco η suele suavizar la trayectoria."
            )
        else:
            st.success(
                f"El algoritmo **converge** de forma estable hacia el mínimo global "
                f"en ({MINIMO[0]:.2f}, {MINIMO[1]:.2f})."
            )

else:
    st.subheader("Comparación de tasas de aprendizaje")
    tasas_comparar = [0.01, 0.1, 0.4, 0.9]

    fig, axes = plt.subplots(2, 2, figsize=(11, 9), subplot_kw={"projection": "3d"})
    axes = axes.flatten()

    for ax, eta_c in zip(axes, tasas_comparar):
        hist_c = descenso_gradiente(gradiente_f2, (x0, y0), eta_c, iteraciones)
        zs_c = f2(hist_c[:, 0], hist_c[:, 1])
        estado_c, icono_c = clasificar_convergencia(hist_c, MINIMO)

        ax.plot_surface(_X, _Y, _Z, cmap=cm.viridis, alpha=0.4, linewidth=0)
        ax.plot(hist_c[:, 0], hist_c[:, 1], zs_c, color="red",
                linewidth=2, marker="o", markersize=2)
        ax.scatter([hist_c[0, 0]], [hist_c[0, 1]], [zs_c[0]],
                   color="orange", s=50, zorder=10)
        ax.scatter([MINIMO[0]], [MINIMO[1]], [f2(*MINIMO)], color="gold",
                   edgecolor="black", s=50, zorder=10)

        ax.set_title(f"η = {eta_c}   {icono_c} {estado_c}", fontsize=10)
        ax.set_xlabel("x", fontsize=8)
        ax.set_ylabel("y", fontsize=8)
        ax.view_init(elev=25, azim=-50)

    fig.tight_layout()
    st.pyplot(fig)

    st.info(
        "Con el mismo punto inicial, notarás cómo η = 0.01 avanza muy lento, "
        "η = 0.1 converge de forma estable, η = 0.4 empieza a zigzaguear y "
        "η = 0.9 suele diverger."
    )

st.markdown("---")

# =========================================================
# Caso aplicado: regresión de consumo energético
# =========================================================
with st.expander("🔌 Caso aplicado: ajustar un modelo de consumo energético"):
    st.markdown(
        """
        Aplicamos el mismo algoritmo para ajustar una recta
        $\\hat{y} = w \\cdot x + b$ que predice el **consumo energético (kWh)**
        de una planta a partir de la **temperatura ambiente (°C)**, minimizando
        el Error Cuadrático Medio (MSE).
        """
    )

    eta_reg = st.slider(
        "Tasa de aprendizaje para la regresión", 0.01, 1.0, 0.3, 0.01,
        key="eta_reg",
    )
    iter_reg = st.slider("Iteraciones de la regresión", 20, 400, 200, 20, key="iter_reg")

    @st.cache_data
    def generar_datos_energia(semilla=42, n=60):
        rng = np.random.default_rng(semilla)
        temperatura = rng.uniform(10, 38, n)
        ruido = rng.normal(0, 8, n)
        consumo = 12.5 * temperatura + 40 + ruido
        temp_norm = (temperatura - temperatura.mean()) / temperatura.std()
        return temperatura, consumo, temp_norm

    temperatura, consumo_real, temp_norm = generar_datos_energia()

    def mse(w, b, x, y):
        y_pred = w * x + b
        return np.mean((y - y_pred) ** 2)

    def gradiente_mse(w, b, x, y):
        n = len(x)
        y_pred = w * x + b
        dw = -(2 / n) * np.sum(x * (y - y_pred))
        db = -(2 / n) * np.sum(y - y_pred)
        return np.array([dw, db])

    w, b = 0.0, 0.0
    costos = []
    for _ in range(iter_reg):
        gw, gb = gradiente_mse(w, b, temp_norm, consumo_real)
        w -= eta_reg * gw
        b -= eta_reg * gb
        costos.append(mse(w, b, temp_norm, consumo_real))

    col_a, col_b = st.columns(2)
    with col_a:
        fig_costo, ax_costo = plt.subplots(figsize=(5.5, 4))
        ax_costo.plot(costos, color="crimson", linewidth=2)
        ax_costo.set_xlabel("Iteración")
        ax_costo.set_ylabel("MSE")
        ax_costo.set_title("Convergencia del MSE")
        ax_costo.grid(True, alpha=0.3)
        fig_costo.tight_layout()
        st.pyplot(fig_costo)

    with col_b:
        x_pred = np.linspace(temp_norm.min(), temp_norm.max(), 50)
        temp_pred_original = x_pred * temperatura.std() + temperatura.mean()
        y_pred = w * x_pred + b

        fig_ajuste, ax_ajuste = plt.subplots(figsize=(5.5, 4))
        ax_ajuste.scatter(temperatura, consumo_real, alpha=0.6, color="teal",
                          label="Datos reales")
        ax_ajuste.plot(temp_pred_original, y_pred, color="crimson", linewidth=2.5,
                       label="Modelo ajustado")
        ax_ajuste.set_xlabel("Temperatura (°C)")
        ax_ajuste.set_ylabel("Consumo (kWh)")
        ax_ajuste.set_title("Recta ajustada vs. datos")
        ax_ajuste.legend(fontsize=8)
        ax_ajuste.grid(True, alpha=0.3)
        fig_ajuste.tight_layout()
        st.pyplot(fig_ajuste)

    if np.isfinite(costos[-1]):
        st.caption(f"MSE final: {costos[-1]:.4f} tras {iter_reg} iteraciones con η = {eta_reg}")
    else:
        st.error("El entrenamiento divergió con esta tasa de aprendizaje. Prueba un valor más bajo.")

st.markdown("---")
st.caption(
    "Módulo 3 — Cálculo Aplicado / Gradiente · Matemáticas para IA · "
    "Universidad EAFIT"
)
