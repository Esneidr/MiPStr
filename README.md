# 📈 Regresión — Conceptos Clave y Modelado Estadístico

Este proyecto es una aplicación educativa e interactiva en **Streamlit** diseñada para enseñar visual e intuitivamente las bases teóricas y prácticas de los **algoritmos de regresión** en Machine Learning. 

Utilizando datos reales del **Censo de Vivienda de California (1990)** de `scikit-learn`, el cuadro de mando permite descomponer y manipular todas las etapas involucradas en el entrenamiento, optimización y evaluación de modelos predictivos continuos.

---

## 🔍 ¿Qué hace este código? (Módulos e Interacciones)

La aplicación está organizada en 5 laboratorios conceptuales que permiten pasar desde la geometría básica de una recta hasta los algoritmos de optimización por gradiente y validación cruzada:

### 1️⃣ Regresión Lineal Simple: Ajuste Manual vs. Óptimo
*   **Fundamento Matemático:** Explora la ecuación básica de la recta $\hat{y} = w \cdot x + b$.
*   **Experimento Interactivo:** Permite al usuario manipular manualmente los hiperparámetros de pendiente ($w$) e intercepto ($b$) mediante deslizadores para intentar ajustar la recta al mapa de dispersión de puntos.
*   **Comparativa:** Calcula el Error Cuadrático Medio (MSE) en tiempo real y contrasta el esfuerzo manual contra la solución óptima encontrada automáticamente por **Mínimos Cuadrados Ordinarios (OLS)**.

### 2️⃣ Regresión Lineal Múltiple: Coeficientes e Importancia
*   **Fundamento Matemático:** Extiende la predicción a múltiples dimensiones:
    $$\hat{y} = w_1 x_1 + w_2 x_2 + \dots + w_k x_k + b$$
*   **Análisis Multivariable:** Permite seleccionar dinámicamente un subconjunto de características del dataset (*Ingreso medio, Edad de la vivienda, Habitaciones promedio, etc.*).
*   **Visualización:** Muestra la magnitud/peso ($w_i$) de cada variable sobre la predicción final mediante un gráfico de barras horizontales, junto a un diagrama de dispersión de *Valor Real vs. Valor Predicho*.

### 3️⃣ Función de Costo ($MSE$) y el Gradiente
*   **Fundamento Matemático:** Visualiza la superficie de error definida por la función de costo:
    $$J(w) = \frac{1}{n}\sum_{i=1}^{n}(w x_i + b - y_i)^2$$
*   **Geometría del Error:** Representa la parábola convexa (el "tazón" de costo) respecto al parámetro $w$.
*   **Interpretación del Gradiente:** Grafica la recta tangente en un punto $w$ específico y calcula su derivada parcial $\frac{\partial J}{\partial w}$. Muestra dinámicamente la regla de decisión: gradiente positivo exige disminuir $w$, mientras que gradiente negativo exige aumentarlo.

### 4️⃣ Algoritmo de Aprendizaje: Descenso de Gradiente
*   **Fundamento Matemático:** Implementa el bucle de actualización iterativa de parámetros:
    $$w \leftarrow w - \alpha \frac{\partial J}{\partial w} \qquad b \leftarrow b - \alpha \frac{\partial J}{\partial b}$$
*   **Simulación de Convergencia:** Permite ajustar la **tasa de aprendizaje ($\alpha$)** y el número de iteraciones (*epochs*).
*   **Monitoreo:** Grafica la curva de pérdida (*loss curve*) a lo largo del tiempo, permitiendo diagnosticar problemas típicos como **suboptimización** ($\alpha$ muy pequeño) o **divergencia/oscilación** ($\alpha$ demasiado grande).

### 5️⃣ Métricas de Evaluación y Generalización
*   **Partición de Datos:** Divide el dataset en subconjuntos de **Entrenamiento (Train)** y **Prueba (Test)** mediante `train_test_split` con una proporción parametrizable.
*   **Evaluación sobre Datos No Vistos:** Mide la capacidad del modelo para generalizar calculando en tiempo real:
    *   **MAE (Mean Absolute Error):** Magnitud promedio del error en las mismas unidades que la variable objetivo.
    *   **RMSE (Root Mean Squared Error):** Raíz del error cuadrático medio (penaliza severamente las desviaciones o *outliers* grandes).
    *   **$R^2$ (Coeficiente de Determinación):** Proporción de la variabilidad total explicada por el modelo ($0$ a $1$).
