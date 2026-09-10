# 🌫️ Predictor de PM2.5 / PM10 — API CORNARE (MARCO)

Esta aplicación de **Streamlit** es una herramienta de despliegue y producción (*deployment*) diseñada para consumir modelos de series de tiempo previamente entrenados y serializados (`.pkl`). Permite realizar **pronósticos hacia adelante** de material particulado (PM2.5 y PM10) utilizando datos de las estaciones de monitoreo ambiental de la cuenca **CORNARE** (Sistema MARCO).

Está diseñada como un complemento interactivo para la puesta en marcha de modelos sin necesidad de reejecutar el pipeline de entrenamiento o el cuaderno principal.

---

## 🔍 ¿Qué hace este código? (Flujo y Arquitectura)

El script actúa como un motor de inferencia ágil que carga paquetes de modelos `joblib`, recupera el contexto histórico y genera proyecciones futuras mediante las siguientes capacidades:

### 1️⃣ Carga y Deserialización Dinámica (`joblib`)
*   **Lectura en Memoria:** Permite subir hasta dos archivos `.pkl` simultáneamente utilizando `io.BytesIO`.
*   **Inspección de Metadatos:** Extrae automáticamente la metadata del modelo (variable monitoreada, código de la estación, RMSE en conjunto de prueba, tipo de algoritmo y fecha de entrenamiento).
*   **Compatibilidad Multimodelo:** Soporta arquitecturas de pronóstico directo y recursivo:
    *   **Directos:** *SES (Suavizado Exponencial Simple)*, *Holt-Winters*, *ARIMA* y *SARIMA* (vía métodos `.forecast()`).
    *   **Recursivos / Basados en Ventana:** *Media Móvil* y *Regresión por Ventana Deslizante* (reconstruye de forma iterativa las predicciones paso a paso).

### 2️⃣ Reconstrucción de la Serie Histórica
*   **Anclaje Temporal Automático:** Si el archivo `.pkl` incluye el historial reciente, el script detecta el último registro de fecha/hora registrado y sincroniza el eje del gráfico para iniciar la predicción exactamente en $t+1$.
*   **Soporte Legacy:** En caso de modelos anteriores sin histórico persistido, permite configurar manualmente la fecha y hora de corte para construir un `pd.date_range` sintético.

### 3️⃣ Inferencia y Visualización Interactiva
*   **Horizonte Configurable:** Permite definir el número de pasos hacia adelante ($k$ períodos u horas) a predecir.
*   **Gráficos Comparativos:** Utiliza **Matplotlib** para superponer el tramo histórico reciente junto a los pronósticos proyectados de los modelos cargados.
*   **Exportación de Resultados:** Presenta una tabla con formato numérico estilizado y habilita la descarga directa de las predicciones en formato `.csv`.

---

## 🚀 Guía de Instalación y Ejecución

### Prerrequisitos
Asegúrate de contar con Python 3.9+ y los modelos `.pkl` generados en la sección de modelado.

### 1. Clonar el repositorio e instalar dependencias
```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio
pip install -r requirements.txt
