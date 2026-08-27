import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Módulo 5 — Datos: preparación y estructura", layout="wide")

# ============================================================
# Generación del dataset (sensores IoT sintéticos)
# ============================================================

FEATURES = ["temperatura", "humedad", "presion", "lecturas_hora"]


def generar_dataset(n, semilla, pct_na_temp, pct_na_hum, n_outliers):
    rng = np.random.default_rng(semilla)
    fechas = pd.date_range("2026-01-01", periods=n, freq="30min")

    tipos_sensor = rng.choice(["DHT22", "BMP180", "LDR"], size=n, p=[0.5, 0.3, 0.2])
    ubicaciones = rng.choice(["invernadero_1", "patio", "bodega"], size=n)
    calidad_senal = rng.choice(["baja", "media", "alta"], size=n, p=[0.1, 0.3, 0.6])

    temperatura = rng.normal(loc=24, scale=3, size=n)
    humedad = rng.normal(loc=60, scale=10, size=n)
    presion = rng.normal(loc=1013, scale=5, size=n)
    lecturas_hora = rng.poisson(lam=12, size=n)

    df = pd.DataFrame({
        "timestamp": fechas,
        "tipo_sensor": tipos_sensor,
        "ubicacion": ubicaciones,
        "calidad_senal": calidad_senal,
        "temperatura": temperatura,
        "humedad": humedad,
        "presion": presion,
        "lecturas_hora": lecturas_hora,
    })

    # Missing values
    if pct_na_temp > 0:
        idx = rng.choice(df.index, size=int(pct_na_temp / 100 * n), replace=False)
        df.loc[idx, "temperatura"] = np.nan
    if pct_na_hum > 0:
        idx = rng.choice(df.index, size=int(pct_na_hum / 100 * n), replace=False)
        df.loc[idx, "humedad"] = np.nan

    # Outliers inyectados en temperatura
    if n_outliers > 0:
        idx = rng.choice(df.index, size=min(n_outliers, n), replace=False)
        df.loc[idx, "temperatura"] = rng.choice([-40, 95, 120], size=len(idx))

    return df


def get_df():
    """Dataset base compartido entre todas las páginas (vía session_state)."""
    cfg = (
        st.session_state.get("n", 500),
        st.session_state.get("semilla", 42),
        st.session_state.get("pct_na_temp", 5),
        st.session_state.get("pct_na_hum", 4),
        st.session_state.get("n_outliers", 6),
    )
    if st.session_state.get("_cfg") != cfg or "df_base" not in st.session_state:
        st.session_state["df_base"] = generar_dataset(*cfg)
        st.session_state["_cfg"] = cfg
    return st.session_state["df_base"]


# ============================================================
# Sidebar — configuración global del dataset
# ============================================================

st.sidebar.title("⚙️ Configuración del dataset")
st.sidebar.caption("Sensores IoT sintéticos (temperatura, humedad, presión, lecturas/hora)")

st.session_state["n"] = st.sidebar.slider("Número de muestras", 100, 2000, 500, step=50)
st.session_state["semilla"] = st.sidebar.number_input("Semilla aleatoria", value=42, step=1)
st.session_state["pct_na_temp"] = st.sidebar.slider("% missing en temperatura", 0, 30, 5)
st.session_state["pct_na_hum"] = st.sidebar.slider("% missing en humedad", 0, 30, 4)
st.session_state["n_outliers"] = st.sidebar.slider("N° de outliers inyectados (temperatura)", 0, 30, 6)

st.sidebar.markdown("---")
pagina = st.sidebar.radio(
    "Navegar por el módulo",
    [
        "🏠 Inicio",
        "1️⃣ Tipos de datos",
        "2️⃣ Missing values y outliers",
        "3️⃣ Normalización y estandarización",
        "4️⃣ Train / Val / Test split",
        "5️⃣ Probabilidad y estadística",
    ],
)

df = get_df()

# ============================================================
# PÁGINA: INICIO
# ============================================================
if pagina == "🏠 Inicio":
    st.title("Módulo 5 — Datos: preparación y estructura")
    st.markdown("""
    Antes de construir cualquier modelo o método computacional, es necesario entender,
    limpiar y estructurar los datos disponibles. Esta aplicación acompaña el notebook del módulo
    y permite **experimentar en vivo** con cada concepto usando un dataset sintético de sensores IoT.

    Usa el menú de la izquierda para:
    - Configurar el dataset (tamaño, % de valores faltantes, outliers inyectados)
    - Navegar por las 5 secciones del módulo
    """)
    st.dataframe(df.head(10), use_container_width=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Filas", len(df))
    c2.metric("Columnas", len(df.columns))
    c3.metric("Missing totales", int(df.isna().sum().sum()))

# ============================================================
# PÁGINA 1: TIPOS DE DATOS
# ============================================================
elif pagina == "1️⃣ Tipos de datos":
    st.header("1️⃣ Tipos de datos")
    st.markdown("""
    Cada columna del dataset representa un tipo distinto: numérico continuo, numérico discreto,
    categórico nominal, categórico ordinal o temporal. Identificarlo correctamente determina
    qué operaciones tienen sentido sobre esa variable.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tipos originales (detectados por pandas)")
        st.dataframe(df.dtypes.astype(str).rename("dtype"), use_container_width=True)
        mem_antes = df.memory_usage(deep=True).sum() / 1024
        st.metric("Memoria total (antes)", f"{mem_antes:.2f} KB")

    with col2:
        st.subheader("Conversión explícita de tipos")
        aplicar = st.checkbox("Convertir columnas categóricas a tipo `category`", value=False)
        df_conv = df.copy()
        if aplicar:
            df_conv["tipo_sensor"] = df_conv["tipo_sensor"].astype("category")
            df_conv["ubicacion"] = df_conv["ubicacion"].astype("category")
            orden = ["baja", "media", "alta"]
            df_conv["calidad_senal"] = pd.Categorical(df_conv["calidad_senal"], categories=orden, ordered=True)
        st.dataframe(df_conv.dtypes.astype(str).rename("dtype"), use_container_width=True)
        mem_despues = df_conv.memory_usage(deep=True).sum() / 1024
        st.metric("Memoria total (después)", f"{mem_despues:.2f} KB",
                   delta=f"{mem_despues - mem_antes:.2f} KB")

    st.info("💡 `calidad_senal` es una categoría **ordinal** (baja < media < alta): el orden importa, "
            "a diferencia de `ubicacion` o `tipo_sensor`, que son nominales.")

# ============================================================
# PÁGINA 2: MISSING VALUES Y OUTLIERS
# ============================================================
elif pagina == "2️⃣ Missing values y outliers":
    st.header("2️⃣ Missing values y outliers")

    st.subheader("Missing values")
    faltantes = df.isna().sum()
    faltantes_pct = (faltantes / len(df) * 100).round(2)
    st.dataframe(
        pd.DataFrame({"faltantes": faltantes, "% del total": faltantes_pct})[faltantes > 0],
        use_container_width=True,
    )

    metodo_imputacion = st.selectbox(
        "Método de tratamiento para 'temperatura' y 'humedad'",
        ["Ninguno (dejar NaN)", "Interpolación lineal", "Eliminar filas (dropna)", "Imputar con la media"],
    )

    df_tratado = df.sort_values("timestamp").reset_index(drop=True).copy()
    if metodo_imputacion == "Interpolación lineal":
        df_tratado[["temperatura", "humedad"]] = df_tratado[["temperatura", "humedad"]].interpolate()
    elif metodo_imputacion == "Eliminar filas (dropna)":
        df_tratado = df_tratado.dropna(subset=["temperatura", "humedad"])
    elif metodo_imputacion == "Imputar con la media":
        df_tratado["temperatura"] = df_tratado["temperatura"].fillna(df_tratado["temperatura"].mean())
        df_tratado["humedad"] = df_tratado["humedad"].fillna(df_tratado["humedad"].mean())

    st.metric("Missing restantes tras el tratamiento", int(df_tratado[["temperatura", "humedad"]].isna().sum().sum()))

    st.markdown("---")
    st.subheader("Outliers — método IQR")

    variable = st.selectbox("Variable a analizar", FEATURES, index=0)
    multiplicador = st.slider("Multiplicador IQR", 0.5, 4.0, 1.5, step=0.1)

    serie = df_tratado[variable].dropna()
    Q1, Q3 = serie.quantile(0.25), serie.quantile(0.75)
    IQR = Q3 - Q1
    lim_inf = Q1 - multiplicador * IQR
    lim_sup = Q3 + multiplicador * IQR
    mask = (serie < lim_inf) | (serie > lim_sup)

    c1, c2, c3 = st.columns(3)
    c1.metric("Límite inferior", f"{lim_inf:.2f}")
    c2.metric("Límite superior", f"{lim_sup:.2f}")
    c3.metric("Outliers detectados", int(mask.sum()))

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    axes[0].boxplot(serie)
    axes[0].set_title(f"{variable} — con outliers")
    axes[1].boxplot(serie[~mask])
    axes[1].set_title(f"{variable} — sin outliers detectados")
    st.pyplot(fig)

# ============================================================
# PÁGINA 3: NORMALIZACIÓN Y ESTANDARIZACIÓN
# ============================================================
elif pagina == "3️⃣ Normalización y estandarización":
    st.header("3️⃣ Normalización y estandarización")
    st.markdown("Cada fila del dataset es un vector; el dataset completo es una matriz. "
                "Aquí puedes comparar el efecto de cada transformación sobre una variable.")

    variable = st.selectbox("Variable", FEATURES, index=2)
    metodo = st.radio("Transformación", ["Ninguna", "Normalización (Min-Max)", "Estandarización (Z-score)"], horizontal=True)

    serie = df[variable].dropna().to_numpy()

    if metodo == "Normalización (Min-Max)":
        transformada = (serie - serie.min()) / (serie.max() - serie.min())
    elif metodo == "Estandarización (Z-score)":
        transformada = (serie - serie.mean()) / serie.std()
    else:
        transformada = serie

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mínimo", f"{transformada.min():.3f}")
    c2.metric("Máximo", f"{transformada.max():.3f}")
    c3.metric("Media", f"{transformada.mean():.3f}")
    c4.metric("Desv. estándar", f"{transformada.std():.3f}")

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.hist(transformada, bins=30, color="steelblue", alpha=0.8)
    ax.set_title(f"{variable} — {metodo}")
    st.pyplot(fig)

# ============================================================
# PÁGINA 4: TRAIN / VAL / TEST SPLIT
# ============================================================
elif pagina == "4️⃣ Train / Val / Test split":
    st.header("4️⃣ Train / Val / Test split")

    tipo_split = st.radio("Tipo de partición", ["Aleatoria", "Cronológica"], horizontal=True)

    col1, col2, col3 = st.columns(3)
    pct_train = col1.slider("% Train", 40, 90, 70)
    pct_val = col2.slider("% Validation", 5, 40, 15)
    pct_test = 100 - pct_train - pct_val
    col3.metric("% Test (calculado)", f"{max(pct_test, 0)}%")

    if pct_test < 0:
        st.error("La suma de Train + Validation supera el 100%. Ajusta los sliders.")
    else:
        df_ordenado = df.sort_values("timestamp").reset_index(drop=True)
        n_total = len(df_ordenado)
        n_train = int(n_total * pct_train / 100)
        n_val = int(n_total * pct_val / 100)

        if tipo_split == "Cronológica":
            train = df_ordenado.iloc[:n_train]
            val = df_ordenado.iloc[n_train:n_train + n_val]
            test = df_ordenado.iloc[n_train + n_val:]
        else:
            barajado = df_ordenado.sample(frac=1, random_state=int(st.session_state["semilla"])).reset_index(drop=True)
            train = barajado.iloc[:n_train]
            val = barajado.iloc[n_train:n_train + n_val]
            test = barajado.iloc[n_train + n_val:]

        fig, ax = plt.subplots(figsize=(9, 1.6))
        sizes = [len(train), len(val), len(test)]
        colors = ["#4C72B0", "#DD8452", "#55A868"]
        left = 0
        for size, color, label in zip(sizes, colors, ["Train", "Val", "Test"]):
            ax.barh(0, size, left=left, color=color)
            ax.text(left + size / 2, 0, f"{label}\n{size}", ha="center", va="center", color="white", fontsize=9)
            left += size
        ax.set_xlim(0, n_total)
        ax.axis("off")
        st.pyplot(fig)

        if tipo_split == "Cronológica":
            st.write(f"**Rango Train:** {train['timestamp'].min()} → {train['timestamp'].max()}")
            st.write(f"**Rango Validation:** {val['timestamp'].min()} → {val['timestamp'].max()}")
            st.write(f"**Rango Test:** {test['timestamp'].min()} → {test['timestamp'].max()}")
            st.info(f"📌 Fecha de corte Train → Validation: **{val['timestamp'].min()}**")

# ============================================================
# PÁGINA 5: PROBABILIDAD Y ESTADÍSTICA
# ============================================================
elif pagina == "5️⃣ Probabilidad y estadística":
    st.header("5️⃣ Probabilidad y estadística básica")

    resumen = df[FEATURES].agg(["mean", "var", "std"]).T
    resumen.columns = ["media", "varianza", "desv_estandar"]
    st.subheader("Estadística descriptiva")
    st.dataframe(resumen.round(3), use_container_width=True)

    st.subheader("Matriz de correlación")
    corr = df[FEATURES].corr()
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(FEATURES))); ax.set_xticklabels(FEATURES, rotation=45, ha="right")
    ax.set_yticks(range(len(FEATURES))); ax.set_yticklabels(FEATURES)
    for i in range(len(FEATURES)):
        for j in range(len(FEATURES)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, fraction=0.046)
    st.pyplot(fig)

    st.subheader("Relación entre dos variables (dispersión)")
    var_x = st.selectbox("Variable X", FEATURES, index=0)
    var_y = st.selectbox("Variable Y", FEATURES, index=1)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.scatter(df[var_x], df[var_y], alpha=0.4, s=15)
    ax2.set_xlabel(var_x); ax2.set_ylabel(var_y)
    ax2.set_title(f"Covarianza: {df[[var_x, var_y]].cov().iloc[0,1]:.2f} | Correlación: {df[[var_x, var_y]].corr().iloc[0,1]:.2f}")
    st.pyplot(fig2)
