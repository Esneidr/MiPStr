# 🌧️ Predicción de Lluvia — Regresión Logística Interactiva

Aplicación interactiva desarrollada en **Python** con **Streamlit** que implementa un modelo de **Regresión Logística** para predecir si lloverá al día siguiente. Permite ajustar variables predictoras, modificar el umbral de decisión y simular nuevos días de manera interactiva.

---

## 🧩 Estructura y Componentes del Código

El archivo principal se organiza en cinco secciones funcionales:

### 1. Configuración y Generación de Datos Sintéticos
* **`st.set_page_config`:** Define el título de la pestaña ("¿Lloverá mañana?") y configura el diseño en formato ancho (`wide`).
* **`generar_datos(n=300, seed=42)`:** Función optimizada con `@st.cache_data` que crea un dataset sintético de 300 días con tres variables climáticas: `temperatura`, `humedad` y `viento`. Calcula la variable objetivo binaria (`llovio`) mediante la función sigmoide aplicada a un valor lineal $z$.

### 2. Panel Lateral (Sidebar) y Parámetros
* **Filtro de Variables:** Casillas de verificación (`st.sidebar.checkbox`) para activar o desactivar dinámicamente `temperatura`, `humedad` y `viento`. Detiene la ejecución si no hay ninguna seleccionada.
* **Umbral de Clasificación:** Deslizador (`st.sidebar.slider`) que permite cambiar el umbral de probabilidad para clasificar entre lluvia ($1$) y no lluvia ($0$), variando entre 0.0 y 1.0.
* **Simulador de Clima:** Entradas interactivas para configurar las condiciones climáticas de un "nuevo día" y predecir su probabilidad de lluvia.

### 3. Entrenamiento del Modelo
* **`entrenar_modelo(...)`:** Función en caché (`@st.cache_data`) que divide los datos en conjuntos de entrenamiento (75%) y prueba (25%), ajustando un modelo de `LogisticRegression` de `scikit-learn`.
* **Evaluación en Tiempo Real:** Calcula las probabilidades predichas sobre el conjunto de prueba y asigna la clasificación final según el umbral configurado por el usuario.

### 4. Layout Principal y Visualizaciones
Organizado en dos columnas principales (`col1` y `col2`):

* **Columna 1:**
  * **Métricas Diarias:** Despliega la probabilidad estimada y el resultado del "nuevo día".
  * **Curva Sigmoide:** Grafica la función sigmoide con `matplotlib`, señalando la posición exacta del punto simular y la línea del umbral seleccionado.
* **Columna 2:**
  * **Diagrama de Dispersión:** Visualiza la relación entre Temperatura y Humedad diferenciando los días con y sin lluvia.
  * **Importancia de Variables:** Muestra un gráfico de barras horizontales con los coeficientes del modelo para comparar el peso de cada variable.

### 5. Evaluación de Desempeño y Guía Pedagógica
* **Matriz de Confusión y Métricas:** Despliega una `ConfusionMatrixDisplay` junto con los valores de **Accuracy**, **Precisión** y **Recall**.
* **Detección de Sesgo de Clasificación:** Emite mensajes de información condicionales (`st.info`) comparando la presencia de **Falsos Positivos** frente a **Falsos Negativos**.
* **Cuestionario Interactivo:** Incluye una guía de 5 preguntas orientadas a evaluar el impacto de los hiperparámetros y variables en el rendimiento del modelo.

---

## 🚀 Requisitos e Instalación

Para ejecutar la aplicación localmente, instala las librerías necesarias:

```bash
pip install streamlit pandas numpy matplotlib scikit-learn
