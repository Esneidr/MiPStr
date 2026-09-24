"""Aprende KNN con suelos de AGROSAVIA: una sola página, cinco pestañas."""
import numpy as np, pandas as pd, requests, streamlit as st, matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

st.set_page_config(page_title="KNN con suelos de AGROSAVIA", page_icon="🌱", layout="wide")

# =============================================================== constantes
SEED = 42
URL = "https://www.datos.gov.co/resource/ch4u-f3i5.json"
ORDEN = ["baja", "media", "alta"]
COL = {"baja": "#d95f02", "media": "#e6ab02", "alta": "#1b9e77"}
UMBRALES = {"mo": (3, 5), "p": (15, 30), "k": (0.2, 0.4)}    # didácticos, no oficiales
EXCLUIDAS = ["mo", "p", "k", "cice"]                          # definen la etiqueta + cice (contiene K)
KS = (1, 3, 5, 9, 15, 21, 31, 45, 61)
NS = (0, 5, 10, 20, 40, 80)                                   # columnas de ruido para la pestaña 8
NUM = {"ph": "ph_agua_suelo", "mo": "materia_organica", "p": "fosforo_bray_ii",
       "s": "azufre_fosfato_monocalcico", "acidez": "acidez_kcl", "al": "aluminio_intercambiable",
       "ca": "calcio_intercambiable", "mg": "magnesio_intercambiable", "k": "potasio_intercambiable",
       "na": "sodio_intercambiable", "cice": "capacidad_de_intercambio_cationico",
       "ce": "conductividad_electrica", "fe": "hierro_disponible_olsen", "cu": "cobre_disponible",
       "mn": "manganeso_disponible_olsen", "zn": "zinc_disponible_olsen", "b": "boro_disponible"}
NOMBRES = {"ph": "pH", "mo": "Materia orgánica", "p": "Fósforo (Bray II)", "s": "Azufre", "acidez": "Acidez",
           "al": "Aluminio", "ca": "Calcio", "mg": "Magnesio", "k": "Potasio", "na": "Sodio", "cice": "CICE",
           "ce": "Conductividad eléctrica", "fe": "Hierro", "cu": "Cobre", "mn": "Manganeso", "zn": "Zinc", "b": "Boro"}
WHERE = " AND ".join(f"{c} IS NOT NULL" for c in
                     ["ph_agua_suelo", "materia_organica", "fosforo_bray_ii", "potasio_intercambiable"])

# ==================================================================== datos
def descargar_muestra(semilla=SEED, n_bloques=5, tam=1000):
    r = requests.get(URL, params={"$select": "count(*)", "$where": WHERE}, timeout=60)
    r.raise_for_status()
    total = int(list(r.json()[0].values())[0])
    n_pos = max(total // tam, 1)
    bloques = sorted(np.random.default_rng(semilla).choice(n_pos, size=min(n_bloques, n_pos), replace=False))
    partes = []
    for b in bloques:
        r = requests.get(URL, params={"$where": WHERE, "$order": ":id", "$limit": tam, "$offset": int(b) * tam}, timeout=60)
        r.raise_for_status()
        partes.append(pd.DataFrame(r.json()))
    return pd.concat(partes, ignore_index=True)

def a_numero(s):
    s = s.astype(str).str.strip().str.replace(",", ".", regex=False)
    censurado = s.str.startswith("<")                       # "<0.1" = bajo el límite de detección
    v = pd.to_numeric(s.str.replace(r"^[<>]\s*", "", regex=True), errors="coerce")
    return v.where(~censurado, v / 2)

def preparar(raw):
    raw = raw.copy()
    for c in NUM.values():
        if c not in raw.columns:
            raw[c] = np.nan
    df = pd.DataFrame({k: a_numero(raw[c]) for k, c in NUM.items()})
    df.loc[~df["ph"].between(2, 11), "ph"] = np.nan
    df = df.clip(lower=df.quantile(.005), upper=df.quantile(.995), axis=1)
    return df, [v for v in df.columns if df[v].isna().mean() <= 0.40]

@st.cache_data(show_spinner="Consultando la API de datos.gov.co…")
def _datos_api(semilla):
    return preparar(descargar_muestra(semilla))

def obtener_datos():
    raw = st.session_state.get("raw_usuario")
    return preparar(raw) if raw is not None else _datos_api(st.session_state.get("semilla", SEED))

def honestas():
    return [v for v in obtener_datos()[1] if v not in EXCLUIDAS]

def etiquetar(df, mult=1.0):
    d = df.dropna(subset=list(UMBRALES)).copy()
    pts = sum(np.where(d[v] < a * mult, 0, np.where(d[v] < b * mult, 1, 2)) for v, (a, b) in UMBRALES.items())
    d["fertilidad"] = pd.cut(pts, [-1, 2, 4, 6], labels=ORDEN).astype(str)
    return d

def pipe(modelo, escalar=True):
    pasos = [("imp", SimpleImputer(strategy="median"))]      # se ajusta solo con train
    if escalar:
        pasos.append(("sc", StandardScaler()))
    return Pipeline(pasos + [("m", modelo)])

def _cv(n=5):
    return StratifiedKFold(n, shuffle=True, random_state=SEED)

# ============================================================ cálculos (caché)
@st.cache_data(show_spinner=False)
def particion(mult=1.0):
    df, us = obtener_datos()
    d = etiquetar(df, mult); y = d["fertilidad"]
    if y.nunique() < 3 or y.value_counts().min() < 10:
        return None
    return train_test_split(d[us], y, test_size=.25, stratify=y, random_state=SEED)

@st.cache_data(show_spinner="Calculando la curva de k…")
def curva_k():
    Xtr, _, ytr, _ = particion(1.0); X = Xtr[honestas()]; filas = []
    for k in KS:
        m = pipe(KNeighborsClassifier(n_neighbors=k))
        sc = cross_val_score(m, X, ytr, cv=_cv(3), scoring="f1_macro")
        filas.append((k, f1_score(ytr, m.fit(X, ytr).predict(X), average="macro"), sc.mean(), sc.std()))
    return pd.DataFrame(filas, columns=["k", "train", "cv", "cv_std"])

@st.cache_data(show_spinner="Comparando distancia y pesos…")
def tabla_hiper(k):
    Xtr, _, ytr, _ = particion(1.0); X = Xtr[honestas()]; filas = []
    for metric in ("euclidean", "manhattan"):
        for w in ("uniform", "distance"):
            sc = cross_val_score(pipe(KNeighborsClassifier(n_neighbors=k, metric=metric, weights=w)),
                                 X, ytr, cv=_cv(3), scoring="f1_macro")
            filas.append((metric, w, sc.mean(), sc.std()))
    return pd.DataFrame(filas, columns=["metric", "weights", "mean", "std"])

@st.cache_data(show_spinner="Entrenando…")
def evaluar_mult(mult):
    part = particion(mult)
    if part is None:
        return None
    Xtr, Xte, ytr, yte = part; F = honestas()
    knn = pipe(KNeighborsClassifier(n_neighbors=9)).fit(Xtr[F], ytr)
    base = pipe(DummyClassifier(strategy="most_frequent")).fit(Xtr[F], ytr)
    yk, yb = knn.predict(Xte[F]), base.predict(Xte[F])
    return {"dist": pd.concat([ytr, yte]).value_counts(normalize=True).reindex(ORDEN).fillna(0),
            "mayoritaria": yb[0], "base_acc": accuracy_score(yte, yb), "base_f1": f1_score(yte, yb, average="macro"),
            "knn_acc": accuracy_score(yte, yk), "knn_f1": f1_score(yte, yk, average="macro"),
            "cm": confusion_matrix(yte, yk, labels=ORDEN)}

@st.cache_data(show_spinner="Evaluando por validación cruzada…")
def f1_cv(feats, n_ruido=0, escalar=True, k=15):
    Xtr, _, ytr, _ = particion(1.0)
    X = Xtr[list(feats)].copy()
    if n_ruido:
        R = pd.DataFrame(np.random.default_rng(SEED).normal(size=(len(X), n_ruido)), index=X.index,
                         columns=[f"ruido{i}" for i in range(n_ruido)])
        X = pd.concat([X, R], axis=1)
    return float(cross_val_score(pipe(KNeighborsClassifier(n_neighbors=k), escalar), X, ytr,
                                 cv=_cv(3), scoring="f1_macro").mean())

# ================================================================ componentes
def sugerencias(items):
    st.markdown("**Qué puedes probar**")
    st.markdown("\n".join(f"- {t}" for t in items))

def pregunta(texto):
    st.divider()
    st.markdown("### Pregunta")
    st.caption("Respóndela fuera de la app (en tu cuaderno o donde indique tu docente).")
    st.markdown(texto)

def barras(ax, etiquetas, valores, colores, yerr=None):
    ax.bar(etiquetas, valores, color=colores, yerr=yerr, capsize=4)
    ax.set_ylim(0, 1); ax.grid(alpha=.3, axis="y")

# ==================================================================== pestañas
def tab_vecinos():
    Xtr, Xte, ytr, yte = particion(1.0)
    st.subheader("¿Quiénes son los vecinos de este suelo?")
    st.markdown("Como cuando eliges un restaurante preguntando a amigos con gustos parecidos, KNN clasifica un suelo nuevo según sus "
                "**k vecinos más cercanos**, que **votan**. Para poder dibujarlo en 2D usamos solo materia orgánica y fósforo.")
    sugerencias(["Mueve k de 1 a 31 y observa qué vecinos quedan resaltados y cómo cambia la votación.",
                 "Pulsa «Probar con otro suelo» varias veces y busca un suelo cuya clase cambie al mover k."])
    v2 = ["mo", "p"]; esc = StandardScaler().fit(Xtr[v2]); Ztr = esc.transform(Xtr[v2])
    n = st.session_state.setdefault("p1_n", 0)
    i = int(np.random.default_rng(1000 + n).integers(len(Xte)))
    zq = esc.transform(Xte[v2].iloc[[i]]); real = yte.iloc[i]
    k = st.slider("Número de vecinos (k)", 1, 31, 5, step=2, key="p1_k")
    nn = KNeighborsClassifier(n_neighbors=k).fit(Ztr, ytr)
    _, idx = nn.kneighbors(zq)
    votos = ytr.iloc[idx[0]].value_counts().reindex(ORDEN, fill_value=0)
    ca, cb = st.columns([3, 2])
    with ca:
        fig, ax = plt.subplots(figsize=(6.5, 4.6))
        mu = np.random.default_rng(0).choice(len(Ztr), size=min(700, len(Ztr)), replace=False)
        for c in ORDEN:
            m = ytr.values[mu] == c
            ax.scatter(Ztr[mu][m, 0], Ztr[mu][m, 1], s=14, alpha=.5, c=COL[c], label=c)
        ax.scatter(Ztr[idx[0], 0], Ztr[idx[0], 1], s=150, facecolors="none", edgecolors="k", linewidths=1.6, label="vecinos")
        ax.scatter(zq[:, 0], zq[:, 1], marker="*", s=330, c="royalblue", edgecolors="k", label="suelo nuevo")
        ax.set(xlabel="materia orgánica (estandarizada)", ylabel="fósforo (estandarizado)")
        ax.legend(fontsize=8); ax.grid(alpha=.3); st.pyplot(fig); plt.close(fig)
    with cb:
        st.markdown("**Votos de los vecinos**")
        st.write(" · ".join(f"{c}: {int(votos[c])}" for c in ORDEN))
        st.metric("Clase asignada por KNN", nn.predict(zq)[0])
        st.caption(f"Clase real de este suelo: **{real}**")
        if st.button("Probar con otro suelo", key="p1_otro"):
            st.session_state["p1_n"] += 1; st.rerun()
    pregunta("¿En qué zona del gráfico están los suelos cuya clase cambia al mover k? ¿Por qué?")

def tab_escalado():
    Xtr = particion(1.0)[0]; FE = honestas(); N = NOMBRES
    st.subheader("¿Importan las unidades de medida?")
    st.markdown("KNN se basa en **distancias**. El hierro se mide en cientos de mg/kg y la conductividad en décimas de dS/m: "
                "¿qué pasa cuando se mezclan en una misma distancia?")
    sugerencias(["Con el interruptor apagado, mira qué variable aporta más a la distancia entre los dos suelos.",
                 "Enciende «Estandarizar» y compara cómo se reparte el aporte.",
                 "Pulsa «Probar con otro par» para ver si ocurre lo mismo con otros suelos.",
                 "Mira los dos valores de F1 al final: comparan el modelo sin escalar y estandarizado."])
    Xh = Xtr[FE]; med = Xh.median(); sd = Xh.std()
    n = st.session_state.setdefault("p2_n", 0)
    i, j = np.random.default_rng(2000 + n).choice(len(Xh), 2, replace=False)
    a, b = Xh.iloc[i].fillna(med), Xh.iloc[j].fillna(med)
    c1, c2 = st.columns([2, 3])
    with c1:
        escalar = st.toggle("Estandarizar las variables", value=False, key="p2_esc")
        if st.button("Probar con otro par", key="p2_otro"):
            st.session_state["p2_n"] += 1; st.rerun()
        par = pd.DataFrame({"Suelo A": a, "Suelo B": b}); par.index = [N[v] for v in par.index]
        st.dataframe(par.round(3))
    with c2:
        d2 = (a - b) ** 2
        if escalar:
            d2 = d2 / (sd ** 2)
        aporte = (d2 / d2.sum() * 100).sort_values()
        fig, ax = plt.subplots(figsize=(6.5, 4.4))
        ax.barh([N[v] for v in aporte.index], aporte.values, color="#2F6B3A" if escalar else "#b5651d")
        ax.set(xlabel="% de la distancia al cuadrado", title=f"Aporte de cada variable ({'estandarizado' if escalar else 'sin escalar'})")
        ax.grid(alpha=.3, axis="x"); st.pyplot(fig); plt.close(fig)
    m1, m2 = st.columns(2)
    m1.metric("F1 macro sin escalar (validación cruzada, k = 15)", f"{f1_cv(tuple(FE), 0, False):.3f}")
    m2.metric("F1 macro estandarizado (validación cruzada, k = 15)", f"{f1_cv(tuple(FE), 0, True):.3f}")
    pregunta("¿Qué cambia en el gráfico al estandarizar y por qué es importante para KNN?")

def tab_elegir_k():
    st.subheader("¿Qué valor de k conviene?")
    st.markdown("Un k pequeño se fija en muy pocos vecinos; uno grande promedia demasiado. La **validación cruzada** estima cómo se comportaría "
                "el modelo con datos que no vio (la franja verde muestra cuánto varía entre pliegues).")
    sugerencias(["Mueve el deslizador y compara las dos líneas en k = 1 y en valores grandes.",
                 "Fíjate dónde la línea de validación alcanza su punto más alto y qué tan plana es a su alrededor."])
    k = st.select_slider("k", options=list(KS), value=9, key="p3_k")
    cv = curva_k(); fila = cv[cv["k"] == k].iloc[0]
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    ax.plot(cv["k"], cv["train"], marker="o", label="Entrenamiento", color="#b5651d")
    ax.plot(cv["k"], cv["cv"], marker="o", label="Validación cruzada", color="#2F6B3A")
    ax.fill_between(cv["k"], cv["cv"] - cv["cv_std"], cv["cv"] + cv["cv_std"], alpha=.2, color="#2F6B3A")
    ax.axvline(k, ls="--", color="gray"); ax.set(xlabel="k", ylabel="F1 macro"); ax.legend(); ax.grid(alpha=.3)
    st.pyplot(fig); plt.close(fig)
    st.write(f"Con k = {k}: entrenamiento **{fila['train']:.3f}** · validación cruzada **{fila['cv']:.3f}** (± {fila['cv_std']:.3f})")
    pregunta("Relaciona el gráfico con los conceptos de sobreajuste y subajuste.")

def tab_distancia():
    st.subheader("Distancia y pesos de los vecinos")
    st.markdown("Además de k, KNN permite elegir cómo medir la distancia (**euclidiana**: línea recta; **Manhattan**: suma de diferencias) y "
                "cómo contar los votos (**uniformes**: todos valen igual; **por distancia**: los más cercanos pesan más).")
    sugerencias(["Cambia k y observa si alguna combinación destaca siempre.",
                 "Compara la diferencia entre las barras con el tamaño de la línea negra (variación entre pliegues)."])
    k = st.select_slider("k", options=list(KS), value=9, key="p4_k")
    t = tabla_hiper(k)
    etiquetas = [f"{'Euclidiana' if r.metric == 'euclidean' else 'Manhattan'}\n{'por distancia' if r.weights == 'distance' else 'uniformes'}"
                 for r in t.itertuples()]
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    barras(ax, etiquetas, t["mean"], ["#4c78a8", "#4c78a8", "#f58518", "#f58518"], yerr=t["std"])
    ax.set_ylabel("F1 macro (validación cruzada)"); st.pyplot(fig); plt.close(fig)
    st.caption("La línea negra de cada barra es ± una desviación estándar entre pliegues.")
    pregunta("¿Alguna combinación es claramente mejor? ¿Cómo lo sabes mirando las líneas negras?")

def tab_metricas():
    st.subheader("Exactitud frente a F1 macro")
    st.markdown("Cuando una clase es mucho más frecuente que las otras, un modelo puede parecer bueno sin haber aprendido nada. La **línea base** "
                "responde siempre la clase más frecuente, sin mirar el suelo.")
    sugerencias(["Con el multiplicador en 1.0, compara las barras de la línea base y de KNN en cada métrica.",
                 "Mueve el multiplicador: con valores altos casi todo el suelo es «baja» y con valores bajos casi todo es «alta». Observa cómo cambian las barras."])
    mult = st.slider("Multiplicador de los umbrales de fertilidad", 0.4, 2.5, 1.0, 0.1, key="p5_mult")
    ev = evaluar_mult(round(mult, 2))
    if ev is None:
        st.warning("Con este multiplicador alguna clase queda con menos de 10 casos y no se puede entrenar. Prueba otro valor.")
    else:
        st.write("Distribución de clases: " + " · ".join(f"{c} {ev['dist'][c] * 100:.0f} %" for c in ORDEN)
                 + f"  |  la línea base responde siempre «{ev['mayoritaria']}»")
        fig, ax = plt.subplots(figsize=(6.5, 3.8)); x = np.arange(2); w = .35
        ax.bar(x - w / 2, [ev["base_acc"], ev["base_f1"]], w, label="Línea base", color="#999999")
        ax.bar(x + w / 2, [ev["knn_acc"], ev["knn_f1"]], w, label="KNN (k = 9)", color="#2F6B3A")
        ax.set_xticks(x); ax.set_xticklabels(["Exactitud", "F1 macro"]); ax.set_ylim(0, 1)
        ax.legend(); ax.grid(alpha=.3, axis="y"); st.pyplot(fig); plt.close(fig)
    pregunta("¿Qué exactitud logra la línea base y por qué eso no la convierte en un buen modelo?")

def tab_confusion():
    st.subheader("Matriz de confusión")
    st.markdown("Muestra **en qué clases acierta y en cuáles se equivoca** el modelo (KNN con k = 9, estandarizado, evaluado en el conjunto de test).")
    sugerencias(["Cambia entre conteos, porcentaje por fila y porcentaje por columna.",
                 "Ubica la diagonal y mira hacia qué clase se van los errores de cada fila."])
    ev = evaluar_mult(1.0)
    if ev is None:
        st.warning("La muestra no tiene suficientes casos de cada clase."); return
    vista = st.radio("Mostrar", ["Conteos", "% por fila", "% por columna"], horizontal=True, key="p6_vista")
    cc = ev["cm"].astype(float)
    if vista == "% por fila":
        M = np.nan_to_num(cc / cc.sum(axis=1, keepdims=True)); fmt, vmax = "{:.2f}", 1
    elif vista == "% por columna":
        M = np.nan_to_num(cc / cc.sum(axis=0, keepdims=True)); fmt, vmax = "{:.2f}", 1
    else:
        M = cc; fmt, vmax = "{:.0f}", cc.max()
    fig, ax = plt.subplots(figsize=(5, 4.2))
    ax.imshow(M, cmap="Blues", vmin=0, vmax=vmax)
    ax.set_xticks(range(3)); ax.set_xticklabels(ORDEN); ax.set_yticks(range(3)); ax.set_yticklabels(ORDEN)
    ax.set(xlabel="Clase predicha", ylabel="Clase real"); ax.grid(False)
    for r in range(3):
        for c in range(3):
            ax.text(c, r, fmt.format(M[r, c]), ha="center", va="center", color="white" if M[r, c] > vmax * .5 else "black")
    st.pyplot(fig); plt.close(fig)
    pregunta("¿Qué clase se identifica mejor y cuál peor? ¿Por qué crees que ocurre?")

def tab_fuga(df):
    FE = tuple(honestas())
    st.subheader("¿Es demasiado bueno para ser cierto?")
    st.markdown("La etiqueta de fertilidad se **calculó** a partir de materia orgánica (MO), fósforo (P) y potasio (K). Aquí puedes agregar esas variables "
                "(y la CICE) a las entradas del modelo y ver qué pasa con el F1 macro por validación cruzada.")
    sugerencias(["Marca MO, P y K, primero una por una y luego las tres juntas.",
                 "Marca también la CICE y observa el cambio.",
                 "Abre la tabla de abajo para ver cómo se relaciona la CICE con las demás columnas."])
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("**Variables que se agregan a las entradas honestas**")
        extra = tuple(v for v in ("mo", "p", "k", "cice") if st.checkbox(f"{NOMBRES[v]} ({v})", key=f"p7_{v}"))
    with c2:
        base, actual = f1_cv(FE, 0), f1_cv(FE + extra, 0)
        fig, ax = plt.subplots(figsize=(5.5, 3.4))
        barras(ax, ["Entradas honestas", "Con tu selección"], [base, actual], ["#2F6B3A", "#b5651d"])
        ax.set_ylabel("F1 macro (validación cruzada)"); st.pyplot(fig); plt.close(fig)
        st.write(f"Entradas honestas: **{base:.3f}** · con tu selección: **{actual:.3f}** ({actual - base:+.3f})")
    cols = ["ca", "mg", "k", "na", "acidez", "cice"]
    ej = df.dropna(subset=cols)
    if len(ej) >= 6:
        with st.expander("Ver seis suelos: ¿qué relación tiene la CICE con las demás columnas?"):
            ej = ej.sample(6, random_state=SEED)[cols]
            ej.insert(5, "suma", ej[["ca", "mg", "k", "na", "acidez"]].sum(axis=1))
            ej.columns = ["Ca", "Mg", "K", "Na", "Acidez", "Ca+Mg+K+Na+Acidez", "CICE"]
            st.dataframe(ej.round(3))
    pregunta("¿Qué pasa con el F1 al agregar MO, P y K? ¿Por qué eso no significa que el modelo sea mejor?")

def tab_ruido():
    FE = tuple(honestas())
    st.subheader("Variables sin información")
    st.markdown("KNN trata **todas** las variables por igual al calcular la distancia. Aquí se agregan columnas de **ruido aleatorio** (sin ninguna información) "
                "a las entradas honestas.")
    sugerencias(["Mueve el deslizador y observa la línea completa y el punto marcado.",
                 "Fíjate en cuánto cae al principio y si la caída continúa igual con muchas columnas."])
    n = st.select_slider("Columnas de ruido agregadas", options=list(NS), value=0, key="p8_n")
    ys = [f1_cv(FE, m) for m in NS]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.plot(NS, ys, marker="o", color="#2F6B3A")
    ax.scatter([n], [ys[NS.index(n)]], s=180, facecolors="none", edgecolors="k", linewidths=2)
    ax.set(xlabel="columnas de ruido agregadas", ylabel="F1 macro (validación cruzada)"); ax.grid(alpha=.3)
    st.pyplot(fig); plt.close(fig)
    st.write(f"Con {n} columnas de ruido: F1 macro **{ys[NS.index(n)]:.3f}**")
    pregunta("¿Por qué le afecta a KNN añadir variables que no tienen relación con la fertilidad?")

# ================================================================ programa
st.title("🌱 Explora KNN con datos de suelos de AGROSAVIA")
st.markdown("**Caso: diagnóstico de fertilidad del suelo** (baja / media / alta). Datos abiertos del Laboratorio de Química y Física de Suelos "
            "de AGROSAVIA (datos.gov.co, `ch4u-f3i5`). En cada pestaña encontrarás sugerencias de qué probar, una interacción y la **pregunta** "
            "que debes responder fuera de la app.")
try:
    df, usables = obtener_datos()
except Exception as e:
    st.error(f"No se pudo consultar la API de datos.gov.co ({e}).")
    st.info("Sube un CSV exportado de datos.gov.co (dataset ch4u-f3i5) para continuar.")
    f = st.file_uploader("Subir CSV", type="csv")
    if f is not None:
        st.session_state["raw_usuario"] = pd.read_csv(f, dtype=str); st.cache_data.clear(); st.rerun()
    st.stop()
if particion(1.0) is None:
    st.error("La muestra no tiene suficientes casos de cada clase de fertilidad."); st.stop()
st.caption(f"Muestra cargada: {len(df):,} registros · {len(usables)} variables usables.")

tabs = st.tabs(["1 · Vecinos", "2 · Escalado", "3 · Elegir k", "4 · Distancia y pesos",
                "5 · Exactitud vs. F1", "6 · Matriz de confusión", "7 · Fuga de datos", "8 · Variables inútiles"])
with tabs[0]: tab_vecinos()
with tabs[1]: tab_escalado()
with tabs[2]: tab_elegir_k()
with tabs[3]: tab_distancia()
with tabs[4]: tab_metricas()
with tabs[5]: tab_confusion()
with tabs[6]: tab_fuga(df)
with tabs[7]: tab_ruido()
