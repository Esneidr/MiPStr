# 📊 Módulo 5 — Datos: Preparación y Estructura

Este proyecto es una aplicación web interactiva diseñada para visualizar y experimentar con los pasos críticos del **Procesamiento y Limpieza de Datos (Pipeline de ETL)** antes de entrenar cualquier modelo de Machine Learning o Inteligencia Artificial.

A través de un simulador de **sensores IoT sintéticos** (que generan datos de temperatura, humedad, presión y lecturas por hora), el script permite manipular las imperfecciones del mundo real y observar cómo impactan las diferentes técnicas de la ciencia de datos.

---

## 🔍 ¿Qué hace este código? (Por Secciones)

El código divide el flujo de trabajo de datos en una barra de configuración global y 5 laboratorios conceptuales:

### ⚙️ Panel de Control Global (Sidebar)
Permite alterar la naturaleza del dataset en tiempo real. Puedes cambiar el tamaño de la muestra, modificar la semilla matemática de aleatoriedad e **inyectar imperfecciones intencionales**, como un porcentaje de datos faltantes (*Missing Values*) o valores atípicos extremos (*Outliers*) en la temperatura.

### 1️⃣ Laboratorio de Tipos de Datos
*   **Análisis Teórico:** Explica la diferencia entre variables continuas, discretas, categóricas nominales, categóricas ordinales y temporales.
*   **Optimización en Acción:** Muestra cómo optimizar el uso de memoria RAM del sistema convirtiendo objetos de texto (`strings`) al tipo de datos optimizado `category` de Pandas, calculando el ahorro exacto en Kilobytes.

### 2️⃣ Tratamiento de Errores: Missing Values y Outliers
*   **Gestión de Faltantes (`NaN`):** Permite comparar cuatro estrategias clásicas para lidiar con vacíos: dejarlos como están, eliminarlos completamente (`dropna`), rellenarlos con el promedio matemático de la columna (`mean`), o usar una **interpolación lineal** basada en el tiempo.
*   **Filtro de Ruido (Método IQR):** Implementa el algoritmo del **Rango Intercuartílico** para calcular límites matemáticos de aceptación. Si un dato escapa de estos límites, se detecta como anomalía. La sección genera dos diagramas de caja (*Boxplots*) interactivos: uno antes del filtro y otro después de remover los datos atípicos.

### 3️⃣ Transformación Matemática: Normalización y Estandarización
Demuestra cómo transformar la escala de las variables para que los modelos no se confundan con las diferencias de unidades (por ejemplo, comparar valores de presión de `1013 hPa` con humedades de `60%`).
*   **Normalización (Min-Max):** Comprime los datos estrictamente entre `0` y `1`.
*   **Estandarización (Z-score):** Desplaza y escala los datos para que su media sea exactamente `0` y su desviación estándar sea `1`.
*   Grafica un histograma dinámico que muestra cómo se redistribuyen los datos tras aplicar cada fórmula.

### 4️⃣ Estrategias de Partición: Train / Val / Test Split
Simula la división del dataset para el entrenamiento de modelos, calculando los tamaños óptimos en proporción. Permite comparar dos filosofías críticas:
*   **Partición Aleatoria:** Distribuye los datos al azar (ideal para datos independientes).
*   **Partición Cronológica:** Corta los datos respetando estrictamente la línea de tiempo. Es fundamental para datos de sensores (series de tiempo), evitando que el modelo "prediga el pasado con datos del futuro" (*Data Leakage*).

### 5️⃣ Análisis de Probabilidad y Estadística Básica
*   **Estadística Descriptiva:** Genera la tabla resumen de momentos estadísticos (Media, Varianza y Desviación Estándar) de los sensores.
*   **Estudio de Relaciones (Correlación):** Construye un mapa de calor (*Heatmap*) con el coeficiente de Pearson para evaluar qué variables se afectan entre sí, junto a un gráfico de dispersión (*Scatter plot*) que calcula la covarianza matemática en tiempo real al cruzar dos sensores elegidos por el usuario.
