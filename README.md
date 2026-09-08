# 🌡️ Series de Tiempo — Sensor IoT Interactivo

Este proyecto es una aplicación interactiva desarrollada en **Streamlit** que acompaña el cuaderno de aprendizaje del **Módulo 7: Series de Tiempo** (*Computación Avanzada · ET0197*). 

Su objetivo principal es permitir la **exploración visual, descomposición analítica y modelado estadístico/predictivo** de series temporales continuas mediante la simulación en tiempo real de un sensor de temperatura IoT (DHT22).

---

## 🔍 ¿Qué hace este código? (Estructura y Módulos)

La aplicación genera una serie de tiempo sintética parametrizable (con componentes de tendencia, estacionalidad diaria y ruido gaussiano) y ofrece 4 módulos o pestañas interactivas para comprender la teoría y práctica del análisis temporal:

### 1️⃣ Componentes de la Serie (Descomposición Aditiva)
*   **Generador Sintético:** Modula en tiempo real la señal según los parámetros de la barra lateral (días simulados, amplitud del ciclo diario, nivel de ruido y pendiente de la tendencia).
*   **Descomposición Clásica:** Utiliza `statsmodels.tsa.seasonal_decompose` para separar analíticamente la serie en sus tres componentes fundamentales:
    $$\text{Temperatura}(t) = \text{Tendencia}(t) + \text{Estacionalidad}(t) + \text{Residuo}(t)$$

### 2️⃣ Análisis de Autocorrelación (ACF y PACF)
*   **Función de Autocorrelación (ACF):** Mide la correlación directa entre la serie y sus retardos (*lags*), permitiendo identificar patrones estacionales recurrentes (picos cada 24 horas).
*   **Función de Autocorrelación Parcial (PACF):** Mide la correlación entre la serie y un retardo elimando el efecto de los retardos intermedios, clave para determinar los órdenes $p$ de modelos autorregresivos.

### 3️⃣ Regresión con Ventanas Deslizantes (*Feature Engineering*)
*   **Transformación de Datos:** Aplica una ventana móvil de tamaño $k$ para transformar la serie temporal en un problema de aprendizaje supervisado tabular con matriz de características $X$ (retardos $t-k, \dots, t-1$) y vector objetivo $y$ (valor en $t$).
*   **Modelado:** Entrena un modelo de **Regresión Lineal** sobre las ventanas pasadas para predecir el siguiente punto en el tiempo.

### 4️⃣ Modelos Clásicos de Pronóstico (*Forecasting*)
Permite ajustar, evaluar y comparar 5 enfoques clásicos de pronóstico sobre un conjunto de prueba (*test set*):
1.  **Media Móvil:** Pronóstico iterativo basado en el promedio de los últimos $n$ valores.
2.  **Suavizado Exponencial Simple (SES):** Asigna pesos decrecientes exponencialmente a las observaciones pasadas ($\alpha$).
3.  **Holt-Winters (Triple Suavizado Exponencial):** Incorpora componentes explícitos de tendencia y estacionalidad aditiva.
4.  **ARIMA $(p, d, q)$:** Modelo AutoRegresivo Integrado de Media Móvil para series no estacionales.
5.  **SARIMA $(p, d, q) \times (P, D, Q)_s$:** Extensión estacional de ARIMA que modela explícitamente el período del ciclo ($s=24$).

---

## 📐 Métricas de Evaluación

Para validar la precisión de las predicciones en las pestañas 3 y 4, la app calcula automáticamente sobre el conjunto de prueba:

*   **MAE (Error Absoluto Medio):** 
    $$\text{MAE} = \frac{1}{n}\sum_{i=1}^{n} |y_i - \hat{y}_i|$$
*   **RMSE (Raíz del Error Cuadrático Medio):** 
    $$\text{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$

---

## 🚀 Instalación y Ejecución

### Prerrequisitos
Asegúrate de tener Python 3.9+ instalado en tu entorno.

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio
