# 🤖 KNN con Suelos de AGROSAVIA: Aplicación Interactiva en Streamlit

Una aplicación web educativa, interactiva y autofuncional desarrollada en **Python** con **Streamlit**, diseñada para enseñar y experimentar de forma práctica con el algoritmo **K-Nearest Neighbors (KNN)** o **K-Vecinos Más Cercanos**.

El proyecto utiliza datos abiertos del **Laboratorio de Química y Física de Suelos de AGROSAVIA** (Portal datos.gov.co, dataset `ch4u-f3i5`) para abordar el caso de uso real de **diagnóstico y clasificación de la fertilidad del suelo** en tres categorías: `baja`, `media` y `alta`.

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Pestañas y Módulos de Aprendizaje](#-pestañas-y-módulos-de-aprendizaje)
- [Conceptos Educativos Explicados](#-conceptos-educativos-explicados)
- [Estructura del Código](#-estructura-del-código)
- [Requisitos e Instalación](#-requisitos-e-instalación)
- [Uso y Flujo de Trabajo](#-uso-y-flujo-de-trabajo)

---

## ✨ Características Principales

1. **Conexión Directa a Datos Abiertos (API SODA / datos.gov.co):**
   - Descarga y procesamiento de muestras dinámicas en tiempo real mediante consultas HTTP (`requests`).
   - Mantenimiento de fallback mediante carga manual de archivos CSV si falla la API.
   - Limpieza automática de datos: conversión de censura de detección (`"<0.1"`), imputación por mediana (`SimpleImputer`) y winsorización/recorte de valores atípicos.

2. **Cálculos Optimizados con Caché:**
   - Uso intensivo de `@st.cache_data` para evitar reentrenar modelos o rehacer particiones de datos innecesariamente durante la interacción del usuario.

3. **Pipelines de Machine Learning Robustos (`scikit-learn`):**
   - Construcción de flujos limpios con `Pipeline`, evitando la contaminación de datos (*data leakage*) entre particiones de entrenamiento y prueba.
   - Evaluación rigurosa mediante validación cruzada estratificada (`StratifiedKFold`).

4. **Visualizaciones Didácticas (`matplotlib`):**
   - Gráficos interactivos de dispersión 2D en espacios estandarizados.
   - Gráficos de barra con desviación estándar entre pliegues de validación.
   - Curvas de ajuste (bias/variance) y matrices de confusión personalizables.

---

## 🗂️ Pestañas y Módulos de Aprendizaje

La aplicación se organiza en **8 pestañas temáticas**, cada una orientada a resolver una pregunta clave sobre KNN:

| # | Pestaña | Propósito Interactivo |
| :-: | :--- | :--- |
| **1** | **Vecinos** | Visualiza en un plano 2D (MO vs. P) la consulta de un suelo, resaltando sus $K$ vecinos más cercanos y el resultado del conteo de votos. |
| **2** | **Escalado** | Demuestra el impacto devastador de las magnitudes de medida (ej. Hierro vs. Conductividad) al calcular la distancia euclidiana con y sin `StandardScaler`. |
| **3** | **Elegir $K$** | Muestra la curva de F1 Macro comparando el conjunto de entrenamiento vs. validación cruzada para identificar sobreajuste y subajuste según el valor de $K$. |
| **4** | **Distancia y Pesos** | Evalúa combinaciones de métricas de distancia (*Euclidiana* vs. *Manhattan*) y esquemas de votación (*Uniformes* vs. *Ponderados por Distancia*). |
| **5** | **Exactitud vs. F1** | Simula desbalance de clases usando un multiplicador de umbrales para comparar la efectividad de un modelo base (`DummyClassifier`) contra KNN. |
| **6** | **Matriz de Confusión** | Visualiza los aciertos y sesgos de clasificación entre las tres clases (`baja`, `media`, `alta`) en formatos de conteo, % por fila o % por columna. |
| **7** | **Fuga de Datos** | Demuestra el fenómeno de *Data Leakage* al incorporar variables que fueron utilizadas directamente en la definición de la etiqueta sintética. |
| **8** | **Variables Inútiles** | Muestra el impacto negativo de la "maldición de la dimensionalidad" mediante la adición progresiva de columnas de ruido aleatorio Gaussianas. |

---

## 🧠 Conceptos Educativos Explicados

El software permite experimentar en tiempo real con los siguientes fundamentos de Machine Learning:

* **Estandarización / Escalado de Funciones:** ¿Por qué medir variables en escalas heterogéneas destruye las métricas de distancia en algoritmos basados en espacio geométrico?
* **Selección del Hiperparámetro $K$:**
  * **$K$ muy pequeño (ej. $1$):** Sensible al ruido, frontera de decisión compleja (*Overfitting* / Alto Sesgo).
  * **$K$ muy grande (ej. $61$):** Suavizado excesivo, ignora patrones locales (*Underfitting* / Alta Varianza).
* **Fuga de Información (*Data Leakage*):** Ocurre cuando se incluyen en el entrenamiento predictores que no estarán disponibles en producción o que contienen directamente la respuesta.
* **Métricas de Evaluación ante Desbalance:** Demuestra por qué la **Exactitud (Accuracy)** es engañosa en clases desbalanceadas y por qué el **F1 Macro** ofrece una evaluación objetiva.

---

## 📐 Estructura del Código

El script está construido en un único archivo modular en Python:

```text
├── Configuración e Importaciones
│   ├── Parametrización de página Streamlit (layout="wide").
│   ├── Definición de constantes, mapeos de columnas, diccionario de nombres y umbrales.
│
├── Carga y Preparación de Datos
│   ├── descargar_muestra() -> Consulta a la API de datos.gov.co usando un generador aleatorio.
│   ├── a_numero() / preparar() -> Limpieza, conversión numérica y filtrado de nulos.
│   ├── etiquetar() -> Generación de la variable objetivo 'fertilidad' según umbrales.
│
├── Motores de Cálculo y Pipelines ML
│   ├── pipe() -> Encadenamiento de SimpleImputer + StandardScaler + Estimador.
│   ├── Funciones cacheadas (@st.cache_data) para curva_k, tabla_hiper, f1_cv, evaluar_mult.
│   
├── Componentes de la Interfaz
│   ├── sugerencias() / pregunta() -> Renderizado de guías pedagógicas.
│   └── tab_vecinos(), tab_escalado(), ..., tab_ruido() -> Funciones de renderizado para cada pestaña.
│
└── Ejecución Principal (Streamlit App)
    ├── Validación de la fuente de datos (API o subida de CSV).
    └── Inicialización del contenedor st.tabs.
