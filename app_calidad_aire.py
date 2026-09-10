"""
App de Streamlit — Predictor de PM2.5 / PM10 (API de CORNARE / MARCO)
======================================================================

Compañera del notebook "Módulo puente — Pronóstico de PM2.5 y PM10 con la
API de CORNARE". Carga uno o dos modelos `.pkl` generados en la sección 11B
del notebook (Media móvil, SES, Holt-Winters, ARIMA, SARIMA o Ventana
deslizante) y genera pronósticos hacia adelante sin volver a correr el
notebook.

Cómo correrla localmente:
    pip install -r requirements.txt
    streamlit run app_pronostico_cornare.py
"""

import io

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Predictor PM2.5 / PM10 — CORNARE",
    page_icon="🌫️",
    layout="wide",
)

TIPOS_DIRECTOS = {"ses", "holt_winters", "arima", "sarima"}
NOMBRES_TIPO = {
    "media_movil": "Media móvil",
    "ses": "SES",
    "holt_winters": "Holt-Winters",
    "arima": "ARIMA",
    "sarima": "SARIMA",
    "ventana_deslizante": "Ventana deslizante",
}


# --------------------------------------------------------------------------
# Funciones de pronóstico — misma lógica que la sección 11B del notebook
# --------------------------------------------------------------------------

def pronosticar(paquete, pasos):
    """Genera `pasos` valores hacia adelante a partir de un paquete cargado
    con joblib.load(...), reproduciendo exactamente la lógica de cada tipo
    de modelo tal como quedó documentada en el notebook."""
    tipo = paquete["tipo"]

    if tipo in TIPOS_DIRECTOS:
        return np.asarray(paquete["modelo"].forecast(pasos))

    if tipo == "ventana_deslizante":
        modelo = paquete["modelo"]
        ventana = paquete["tamano_ventana"]
        historial = list(paquete["ultimos_valores"])
        predicciones = []
        for _ in range(pasos):
            entrada = np.array(historial[-ventana:]).reshape(1, -1)
            siguiente = modelo.predict(entrada)[0]
            predicciones.append(siguiente)
            historial.append(siguiente)
        return np.array(predicciones)

    if tipo == "media_movil":
        ventana = paquete["ventana"]
        historial = list(paquete["ultimos_valores"])
        predicciones = []
        for _ in range(pasos):
            siguiente = np.mean(historial[-ventana:])
            predicciones.append(siguiente)
            historial.append(siguiente)
        return np.array(predicciones)

    raise ValueError(f"Tipo de modelo desconocido: '{tipo}'. ¿Es un .pkl generado por este notebook?")


def extraer_historico(paquete):
    """Devuelve una pd.Series con el histórico guardado en el .pkl (sección
    11B del notebook), o None si el archivo es de una versión anterior que
    no lo incluía."""
    historico = paquete.get("historico")
    if not historico:
        return None
    fechas = pd.to_datetime(historico["fechas"])
    return pd.Series(historico["valores"], index=fechas)


def etiqueta_modelo(paquete, nombre_archivo):
    meta = paquete.get("metadata", {})
    nombre = meta.get("nombre_modelo") or NOMBRES_TIPO.get(paquete.get("tipo"), paquete.get("tipo"))
    return nombre or nombre_archivo


def cargar_paquete(archivo_subido):
    """joblib.load acepta tanto rutas como objetos tipo archivo en memoria."""
    return joblib.load(io.BytesIO(archivo_subido.getvalue()))


# --------------------------------------------------------------------------
# Interfaz
# --------------------------------------------------------------------------

st.title("🌫️ Predictor de calidad del aire — CORNARE (MARCO)")
st.caption(
    "Carga los modelos `.pkl` que descargaste en la sección 11B del notebook "
    "de pronóstico y genera predicciones de PM2.5 / PM10 hacia adelante."
)

st.sidebar.header("1. Carga tus modelos")
archivos_subidos = st.sidebar.file_uploader(
    "Sube uno o dos archivos .pkl",
    type=["pkl"],
    accept_multiple_files=True,
    help="Los genera la sección 11B del notebook: modelo_{VARIABLE}_{modelo}.pkl",
)

if not archivos_subidos:
    st.info("👈 Sube al menos un archivo `.pkl` en la barra lateral para comenzar.")
    st.markdown(
        """
        **¿No tienes los archivos a mano?** Corre la sección 11B del notebook
        *Módulo puente — Pronóstico de PM2.5 y PM10*; ahí se guardan y
        descargan automáticamente los dos mejores modelos según RMSE.
        """
    )
    st.stop()

if len(archivos_subidos) > 2:
    st.sidebar.warning("Solo se usarán los dos primeros archivos que subiste.")
    archivos_subidos = archivos_subidos[:2]

paquetes = []
for archivo in archivos_subidos:
    try:
        paquetes.append((archivo.name, cargar_paquete(archivo)))
    except Exception as e:
        st.sidebar.error(f"No pude cargar **{archivo.name}**: {e}")

if not paquetes:
    st.stop()

st.sidebar.header("2. Modelos cargados")
for nombre_archivo, paquete in paquetes:
    meta = paquete.get("metadata", {})
    with st.sidebar.expander(f"📦 {etiqueta_modelo(paquete, nombre_archivo)}", expanded=True):
        st.write(f"**Archivo:** {nombre_archivo}")
        st.write(f"**Tipo:** {paquete.get('tipo', '—')}")
        st.write(f"**Variable:** {meta.get('variable', '—')}")
        st.write(f"**Estación:** {meta.get('codigo_estacion', '—')}")
        rmse = meta.get("rmse_en_test")
        st.write(f"**RMSE en test:** {rmse:.3f}" if rmse is not None else "**RMSE en test:** —")
        st.write(f"**Entrenado:** {meta.get('fecha_entrenamiento', '—')}")

st.sidebar.header("3. Parámetros del pronóstico")
pasos = st.sidebar.number_input(
    "Pasos hacia adelante a pronosticar", min_value=1, max_value=500, value=24, step=1
)

meta0 = paquetes[0][1].get("metadata", {})
frecuencia = meta0.get("frecuencia") or "h"

historico0 = extraer_historico(paquetes[0][1])

if historico0 is not None:
    # El .pkl trae fechas reales: el pronóstico arranca justo después del
    # último dato histórico, igual que en la sección 11 del notebook.
    inicio_ts = historico0.index[-1]
    st.sidebar.caption(f"Histórico detectado hasta **{inicio_ts}** — el pronóstico arranca justo después.")
    n_mostrar = st.sidebar.slider(
        "Puntos de histórico a mostrar en el gráfico",
        min_value=min(24, len(historico0)),
        max_value=len(historico0),
        value=min(200, len(historico0)),
    )
else:
    st.sidebar.warning(
        "Este .pkl no trae histórico guardado (viene de una versión anterior del notebook). "
        "Puedes seguir generando el pronóstico, pero sin la serie histórica en el gráfico."
    )
    usar_fecha = st.sidebar.checkbox("Usar fecha/hora real para el eje del gráfico", value=False)
    inicio_ts = None
    if usar_fecha:
        col_f, col_h = st.sidebar.columns(2)
        fecha_ultimo_dato = col_f.date_input("Fecha del último dato real")
        hora_ultimo_dato = col_h.time_input("Hora del último dato real")
        inicio_ts = pd.Timestamp.combine(fecha_ultimo_dato, hora_ultimo_dato)
    n_mostrar = 0

generar = st.sidebar.button("🔮 Generar pronóstico", type="primary", use_container_width=True)

# --------------------------------------------------------------------------
# Pronóstico y resultados
# --------------------------------------------------------------------------

if generar:
    resultados = {}
    for nombre_archivo, paquete in paquetes:
        etiqueta = etiqueta_modelo(paquete, nombre_archivo)
        try:
            resultados[etiqueta] = pronosticar(paquete, int(pasos))
        except Exception as e:
            st.error(f"Error al pronosticar con **{etiqueta}**: {e}")

    if resultados:
        if inicio_ts is not None:
            index_futuro = pd.date_range(start=inicio_ts, periods=pasos + 1, freq=frecuencia)[1:]
            nombre_indice = "fecha"
        else:
            index_futuro = pd.RangeIndex(1, pasos + 1)
            nombre_indice = "paso"

        df_resultados = pd.DataFrame(resultados, index=index_futuro)
        df_resultados.index.name = nombre_indice

        variable = meta0.get("variable", "")
        estacion = meta0.get("codigo_estacion", "")

        st.subheader("📈 Histórico + pronóstico")
        fig, ax = plt.subplots(figsize=(12, 4))

        if historico0 is not None:
            tramo_historico = historico0.iloc[-n_mostrar:]
            ax.plot(tramo_historico.index, tramo_historico.values, label="Histórico", color="black")
            ax.axvline(historico0.index[-1], color="gray", linestyle=":")

        colores = ["crimson", "royalblue", "seagreen", "darkorange"]
        for (nombre, color) in zip(df_resultados.columns, colores):
            ax.plot(
                df_resultados.index, df_resultados[nombre],
                label=f"Pronóstico — {nombre}", linestyle="--", color=color,
            )

        titulo = f"Pronóstico — {variable}" + (f" (estación {estacion})" if estacion else "")
        ax.set_title(titulo)
        ax.set_ylabel(variable or "valor")
        ax.legend()
        ax.grid(alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig)

        st.subheader("🔢 Tabla de valores")
        st.dataframe(df_resultados.style.format("{:.2f}"), use_container_width=True)

        csv = df_resultados.to_csv().encode("utf-8")
        st.download_button(
            "⬇️ Descargar pronóstico (CSV)",
            data=csv,
            file_name=f"pronostico_{variable or 'modelo'}.csv",
            mime="text/csv",
        )
else:
    st.info("Configura los parámetros en la barra lateral y presiona **Generar pronóstico**.")
