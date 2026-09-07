"""
App Didáctica de Streamlit — Nivel de ríos/quebradas (CORNARE / MARCO)
--------------------------------------------------------------------
Para correr localmente:
    pip install streamlit pandas requests numpy plotly
    streamlit run aplicacion_datos.py
"""

from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ------------------------------------------------------------------
# Configuración y Constantes
# ------------------------------------------------------------------
NOMBRE_ESTUDIANTE = "Esneider Cordoba"
CODIGO_ESTACION = "14"
NOMBRE_ESTACION = "El Retiro - Quebrada La Agudelo"

# Coordenadas por defecto (Ubicación aproximada de El Retiro, Antioquia)
LAT_DEFECTO = 6.0583
LON_DEFECTO = -75.4267

API_BASE_URL = "https://marco.cornare.gov.co/api/v1/estaciones"
LLAVE_FECHA = "level_date"
LLAVE_VALOR = "level"
CANDIDATOS_LAT = ["lat", "latitude", "latitud"]
CANDIDATOS_LON = ["lng", "lon", "longitude", "longitud"]

st.set_page_config(
    page_title=f"Monitoreo {NOMBRE_ESTACION}", page_icon="🌊", layout="wide"
)


# ------------------------------------------------------------------
# Funciones de Lógica y API
# ------------------------------------------------------------------
@st.cache_data(ttl=600)
def consultar_api_cornare(codigo_estacion, desde, hasta, calidad=1):
    url = f"{API_BASE_URL}/{codigo_estacion}/nivel"
    params = {"desde": desde, "hasta": hasta, "calidad": calidad}
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
    }
    try:
        resp = requests.get(
            url, params=params, headers=headers, timeout=30, verify=False
        )
        if resp.status_code == 200:
            datos_json = resp.json()
            registros = list(datos_json.get("values", []))
            siguiente_url = datos_json.get("next")

            # Paginación
            while siguiente_url:
                try:
                    r_next = requests.get(
                        siguiente_url, timeout=30, verify=False
                    )
                    if r_next.status_code == 200:
                        p_json = r_next.json()
                        registros.extend(p_json.get("values", []))
                        siguiente_url = p_json.get("next")
                    else:
                        break
                except Exception:
                    break
            return registros, datos_json, None
        return None, None, f"Error HTTP {resp.status_code}"
    except Exception as e:
        return None, None, f"Error de conexión: {e}"


def detectar_coordenadas(datos_json):
    if not isinstance(datos_json, dict):
        return LAT_DEFECTO, LON_DEFECTO, False

    lat = next(
        (datos_json[k] for k in CANDIDATOS_LAT if k in datos_json), None
    )
    lon = next(
        (datos_json[k] for k in CANDIDATOS_LON if k in datos_json), None
    )

    if lat is not None and lon is not None:
        try:
            return float(lat), float(lon), True
        except (TypeError, ValueError):
            pass
    return LAT_DEFECTO, LON_DEFECTO, False


def calcular_indice_calidad(df):
    if df.empty or len(df) < 2:
        return 0.0, 0, 0

    df_idx = df.set_index("fecha")
    frecuencia_tipica = df["fecha"].diff().dropna().mode()
    if len(frecuencia_tipica) == 0:
        return 0.0, 0, 0
    freq = frecuencia_tipica[0]

    rango_completo = pd.date_range(
        start=df_idx.index.min(), end=df_idx.index.max(), freq=freq
    )
    esperados = len(rango_completo)
    huecos = esperados - len(df_idx)
    completitud = max(0.0, 1 - (huecos / esperados)) if esperados > 0 else 0.0

    Q1, Q3 = df["nivel"].quantile(0.25), df["nivel"].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf, lim_sup = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    es_outlier = (
        (df["nivel"] < lim_inf) | (df["nivel"] > lim_sup) | (df["nivel"] < 0)
    )
    proporcion_outliers = es_outlier.mean()

    indice = (completitud * 0.7 + (1 - proporcion_outliers) * 0.3) * 100
    return round(indice, 1), int(huecos), int(es_outlier.sum())


# ------------------------------------------------------------------
# Interfaz de Usuario (Sidebar)
# ------------------------------------------------------------------
st.sidebar.title("🎛️ Filtros de Consulta")

# Fechas dinámicas por defecto (últimos 7 días)
hoy = datetime.now().date()
hace_siete_dias = hoy - timedelta(days=7)

fecha_desde = st.sidebar.date_input("Fecha Inicio", hace_siete_dias).strftime(
    "%Y-%m-%d"
)
fecha_hasta = st.sidebar.date_input("Fecha Fin", hoy).strftime("%Y-%m-%d")
calidad = st.sidebar.selectbox(
    "Filtro de Datos",
    [1, 0],
    format_func=lambda x: (
        "Solo Validados (Recomendado)" if x == 1 else "Todos los Datos"
    ),
    index=0,
)

consultar = st.sidebar.button(
    "🔍 Consultar Estación", type="primary", use_container_width=True
)

st.sidebar.markdown("---")
st.sidebar.caption(f"👨‍🎓 **Desarrollado por:** {NOMBRE_ESTUDIANTE}")
st.sidebar.caption(f"📍 **Estación:** {CODIGO_ESTACION} - {NOMBRE_ESTACION}")

# ------------------------------------------------------------------
# Encabezado Principal
# ------------------------------------------------------------------
st.title("🌊 Sistema de Monitoreo de Niveles de Agua")
st.markdown(
    f"**Estación {CODIGO_ESTACION}:** {NOMBRE_ESTACION} | *Fuente de datos: CORNARE (MARCO)*"
)

# Carga automática de datos al iniciar o al presionar el botón
with st.spinner("Cargando y analizando información..."):
    registros, datos_crudos, error = consultar_api_cornare(
        CODIGO_ESTACION, fecha_desde, fecha_hasta, calidad
    )

if error:
    st.error(f"❌ Ocurrió un error al consultar la API: {error}")
elif not registros:
    st.warning(
        "⚠️ No se encontraron lecturas para el rango de fechas seleccionado. Selecciona un rango con fechas pasadas en el panel lateral."
    )
else:
    # Preprocesamiento de datos
    df = pd.DataFrame(registros)
    df = df.rename(columns={LLAVE_FECHA: "fecha", LLAVE_VALOR: "nivel"})
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["nivel"] = pd.to_numeric(df["nivel"], errors="coerce")
    df = df.dropna(subset=["fecha", "nivel"]).sort_values("fecha").reset_index(
        drop=True
    )

    lat, lon, coords_reales = detectar_coordenadas(datos_crudos)
    indice_calidad, huecos, n_outliers = calcular_indice_calidad(df)

    # Pestañas para organizar la información
    tab_resumen, tab_mapa, tab_graficos, tab_calidad = st.tabs([
        "📊 Dashboard & Diagnóstico",
        "🗺️ Geolocalización",
        "📈 Análisis Gráfico",
        "🔬 Calidad de Datos & Descarga",
    ])

    # ==================================================================
    # PESTAÑA 1: RESUMEN Y DIAGNÓSTICO
    # ==================================================================
    with tab_resumen:
        st.subheader("💡 Diagnóstico Rápido de la Quebrada")
        st.markdown(
            "Esta sección resume las métricas clave para entender el comportamiento del caudal."
        )

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)

        nivel_prom = df["nivel"].mean()
        nivel_max = df["nivel"].max()
        nivel_min = df["nivel"].min()

        col_m1.metric(
            "📏 Nivel Promedio",
            f"{nivel_prom:.2f} m",
            help="Promedio de la altura del agua en el periodo.",
        )
        col_m2.metric(
            "🔺 Nivel Máximo",
            f"{nivel_max:.2f} m",
            help="Punto más alto alcanzado por la corriente.",
        )
        col_m3.metric(
            "🔻 Nivel Mínimo",
            f"{nivel_min:.2f} m",
            help="Punto más bajo registrado.",
        )
        col_m4.metric(
            "🔢 Total Lecturas",
            f"{len(df)}",
            help="Cantidad de datos tomados por el sensor.",
        )

        st.markdown("---")

        # Alerta visual según comportamiento
        st.subheader("🚨 Estado del Cauce")
        if nivel_max > (nivel_prom * 1.8):
            st.error(
                "⚠️ **Atención:** Se detectaron crecientes o picos significativos de agua en el periodo analizado."
            )
        else:
            st.success(
                "✅ **Comportamiento Normal:** El flujo de agua se ha mantenido estable dentro de los parámetros habituales."
            )

        # Gráfico de Línea Temporal Dinámico con Plotly
        st.subheader("📉 Evolución del Nivel en el Tiempo")

        fig_linea = px.line(
            df,
            x="fecha",
            y="nivel",
            labels={
                "fecha": "Fecha y Hora",
                "nivel": "Nivel de Agua (Metros)",
            },
            title="Histórico Temporal del Nivel de la Quebrada",
            template="plotly_white",
        )
        fig_linea.add_hline(
            y=nivel_prom,
            line_dash="dash",
            line_color="orange",
            annotation_text="Promedio",
        )
        fig_linea.update_traces(line_color="#0B5ED7", line_width=2)
        st.plotly_chart(fig_linea, use_container_width=True)

    # ==================================================================
    # PESTAÑA 2: GEOLOCALIZACIÓN
    # ==================================================================
    with tab_mapa:
        st.subheader("📍 Ubicación Geográfica de la Estación")

        col_map1, col_map2 = st.columns([2, 1])

        with col_map1:
            map_df = pd.DataFrame({"lat": [lat], "lon": [lon]})

            # Renderizado directo mediante mapa nativo de Streamlit
            st.map(map_df, zoom=13, use_container_width=True)

        with col_map2:
            st.info("ℹ️ **Información Territorial**")
            st.write("- **Municipio:** El Retiro")
            st.write("- **Fuente Hídrica:** Quebrada La Agudelo")
            st.write("- **Autoridad Ambiental:** CORNARE")
            st.write(f"- **Latitud:** `{lat}`")
            st.write(f"- **Longitud:** `{lon}`")

            if not coords_reales:
                st.warning(
                    "📌 *Nota: La API no devolvió coordenadas exactas, se muestran las coordenadas de referencia del municipio.*"
                )
            else:
                st.success(
                    "📍 Coordenadas confirmadas por el servidor de CORNARE."
                )

    # ==================================================================
    # PESTAÑA 3: OTROS GRÁFICOS Y ANÁLISIS
    # ==================================================================
    with tab_graficos:
        st.subheader("📊 Análisis Estadístico y Comportamiento")
        st.write(
            "Gráficos adicionales para facilitar la interpretación de patrones en el comportamiento del agua."
        )

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("#### 1. Distribución de Niveles (Histograma)")
            st.caption(
                "Muestra con qué frecuencia el agua alcanza ciertos niveles."
            )
            fig_hist = px.histogram(
                df,
                x="nivel",
                nbins=20,
                color_discrete_sequence=["#17A2B8"],
                labels={
                    "nivel": "Nivel (m)",
                    "count": "Frecuencia de Lecturas",
                },
            )
            fig_hist.update_layout(template="plotly_white")
            st.plotly_chart(fig_hist, use_container_width=True)

        with col_g2:
            st.markdown("#### 2. Diagrama de Caja (Outliers y Rango)")
            st.caption(
                "Visualiza la variabilidad de los datos y valores atípicos."
            )
            fig_box = px.box(
                df,
                y="nivel",
                points="all",
                color_discrete_sequence=["#6C757D"],
                labels={"nivel": "Nivel (m)"},
            )
            fig_box.update_layout(template="plotly_white")
            st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 3. Variación del Nivel por Hora del Día")
        st.caption(
            "Permite identificar si hay patrones u horarios fijos de subida del nivel."
        )

        df_hora = df.copy()
        df_hora["hora"] = df_hora["fecha"].dt.hour
        df_prom_hora = (
            df_hora.groupby("hora")["nivel"].mean().reset_index()
        )

        fig_hora = px.bar(
            df_prom_hora,
            x="hora",
            y="nivel",
            labels={
                "hora": "Hora del Día (0-23)",
                "nivel": "Nivel Promedio (m)",
            },
            color_discrete_sequence=["#20C997"],
        )
        fig_hora.update_layout(template="plotly_white")
        st.plotly_chart(fig_hora, use_container_width=True)

    # ==================================================================
    # PESTAÑA 4: CALIDAD DE DATOS Y DESCARGA
    # ==================================================================
    with tab_calidad:
        st.subheader("🔬 Control de Calidad del Sensor")

        c_cal1, c_cal2 = st.columns(2)

        with c_cal1:
            st.metric("🎯 Índice de Calidad", f"{indice_calidad} / 100")
            st.progress(int(indice_calidad))

        with c_cal2:
            st.write(
                f"- **Huecos de reporte (Faltantes):** {huecos} registros"
            )
            st.write(
                f"- **Outliers (Anomalías detectadas):** {n_outliers} lecturas"
            )

        st.info("""
        **¿Cómo se calcula el índice de calidad?**
        Combina dos factores clave:
        1. **Completitud de la serie (70%):** Verifica si el sensor envió datos de forma continua sin perder conexión.
        2. **Ausencia de Anormalidades (30%):** Detecta si hay valores fuera de rango razonable mediante el rango intercuartílico (IQR) o valores negativos.
        """)

        st.markdown("---")
        st.subheader("💾 Tabla de Datos y Descarga")

        st.dataframe(df[["fecha", "nivel"]], use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descargar Serie de Datos (CSV)",
            data=csv,
            file_name=f"nivel_estacion_{CODIGO_ESTACION}.csv",
            mime="text/csv",
            type="primary",
        )
