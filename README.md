# 🌡️ Predictor de Sensación Térmica — Taller IoT

Aplicación interactiva construida en **Python** con **Streamlit** que consulta datos en tiempo real desde **InfluxDB Cloud** (provenientes de un sensor **ESP32 + DHT22**), procesa la serie de tiempo, entrena un modelo de **Regresión Lineal Múltiple** con `scikit-learn` y permite realizar predicciones de sensación térmica.

---

## 🧩 Estructura y Componentes del Código

El archivo principal está organizado en cuatro secciones funcionales:

### 1. Configuración Inicial y Librerías
* **`st.set_page_config`:** Establece el título de la pestaña, el icono (🌡️) y el diseño centrado de la interfaz.
* **`COLUMNAS`:** Define la lista de variables requeridas (`temperatura`, `humedad`, `sensacion_termica`).
* **Importación de módulos:** Utiliza `pandas`, `numpy`, `matplotlib`, `scikit-learn` y el cliente oficial de `influxdb_client`.

### 2. Funciones de Datos y Machine Learning

* **`obtener_datos_crudos(...)`:** Conecta a InfluxDB con un *context manager* (`with`), ejecuta una consulta Flux sobre el bucket seleccionado, pivota las métricas por fecha, ajusta la zona horaria a `America/Bogota` y retorna un DataFrame con los datos brutos.
* **`preparar_datos(...)`:** Aplica interpolación basada en tiempo (`method="time"`) para corregir vacíos de lectura del sensor y elimina los nulos sobrantes.
* **`detectar_outliers_iqr(...)`:** Calcula el Rango Intercuartílico ($IQR = Q3 - Q1$) para identificar registros atípicos fuera de los límites aceptables.
* **`entrenar_modelo(...)`:**
  * Divide la información en conjuntos de entrenamiento (70%) y prueba (30%).
  * Ajusta un modelo de `LinearRegression` con las variables predictoras (`temperatura` y `humedad`).
  * Calcula y retorna las métricas de error: $MAE$, $RMSE$ y el coeficiente de determinación $R^2$.

### 3. Barra Lateral (Sidebar)
* Formulario para ingresar las **credenciales de InfluxDB** (URL, Token, Org, Bucket y Measurement).
* Control deslizable (*slider*) para seleccionar el historial de consulta (de 1 a 12 horas).
* Botón **"🔄 Consultar datos y entrenar modelo"**, activo únicamente cuando todas las credenciales han sido completadas.

### 4. Interfaz Principal y Pestañas

Una vez realizada la consulta, guarda el DataFrame y el modelo en `st.session_state` y despliega:

* **Métricas Principales:** Muestra los valores de la última lectura registrada (Temperatura, Humedad y Sensación Térmica real).
* **Pestaña 📊 Estadísticos:** Contiene la gráfica temporal de las variables, estadísticas descriptivas (`describe()`) y diagramas de caja (*boxplots*).
* **Pestaña 🧹 Preparación de datos:** Muestra el tipo de datos, recuento de faltantes, gráfico del efecto de interpolación y tabla de outliers detectados por IQR.
* **Pestaña 📈 Análisis del modelo:** Despliega un diagrama de dispersión en 3D, la ecuación final en formato LaTeX ($\text{sensación} = \beta_0 + \beta_1 \cdot \text{temp} + \beta_2 \cdot \text{hum}$) y las métricas de desempeño ($MAE$, $RMSE$, $R^2$).
* **Pestaña 🔮 Predicción:** Ofrece una calculadora interactiva donde el usuario puede ingresar sus propios coeficientes ($\beta_0, \beta_1, \beta_2$) y evaluar valores arbitrarios de temperatura y humedad.

---

## 🚀 Requisitos de Ejecución

```bash
pip install streamlit pandas numpy matplotlib scikit-learn influxdb-client
streamlit run app.py
