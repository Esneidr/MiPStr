# ⚡ Modelo de Consumo Energético — Inspección y Producción POO

Esta aplicación en **Streamlit** es una herramienta interactiva para la **inspección técnica, auditoría de herencia y prueba en tiempo real** de un pipeline de Machine Learning previamente entrenado y serializado con `joblib`. 

A través de un objeto contenedor (`FlujoConsumo`), la app descompone un modelo de regresión que predice el **consumo de energía (kWh)** en función de la temperatura, ocupación del edificio y humedad.

---

## 🔍 ¿Qué hace este código? (Descripción de Pestañas y POO)

El script actúa como una consola de inspección de objetos Python, utilizando la librería estándar `inspect` para mostrar la estructura interna y la lógica de negocio de los objetos cargados en memoria.

### 1️⃣ Atributos: Estado Interno de los Objetos
Muestra los valores que aprendió o guardó el modelo durante el proceso de entrenamiento:
*   **Preprocesador (`Estandarizador`):** Expone la `media` ($\mu$) y la desviación estándar ($\sigma$) calculadas para cada variable (`temperatura`, `ocupacion`, `humedad`).
*   **Modelo (`RegresionLinealGD`):** Muestra los hiperparámetros de entrenamiento (`tasa`, `iteraciones`), el sesgo aprendido (`b` / intercepto) y los pesos de características (`w`).
*   **Historial de Pérdida:** Grafica la curva de convergencia de la función de costo ($MSE$) a lo largo de las iteraciones.

### 2️⃣ Métodos y Herencia: Inspección del Código en Ejecución
Aprovecha el módulo `inspect` de Python para auditar la arquitectura orientada a objetos:
*   **Árbol de Herencia (`__mro__`):** Muestra la línea de ancestros/clases de las cuales hereda cada objeto (`flujo`, `pre`, `modelo`).
*   **Firma de Métodos:** Genera una tabla automática con todos los métodos disponibles, sus parámetros y en qué clase exacta están definidos (*resolución de nombres*).
*   **Lectura de Código Fuente:** Permite seleccionar cualquier método del modelo (`fit`, `predict`, `score`, `__init__`) y renderiza su código fuente Python directo desde la memoria.

### 3️⃣ Probar el Modelo: Inferencia Paso a Paso
Permite ingresar lecturas nuevas mediante deslizadores interactivos y realiza la predicción descomponiendo la matemática en tiempo real:
*   **Paso 1 — Transformación (`preprocesador.transform`):** Aplica la estandarización $Z$-Score a los datos de entrada:
    $$x_{\text{std}} = \frac{x - \text{media}}{\text{desv}}$$
*   **Paso 2 — Producto Punto y Aporte:** Multiplica cada variable estandarizada por su peso correspondiente ($w_i \cdot x_{\text{std}, i}$).
*   **Paso 3 — Suma de Sesgo (`modelo.predict`):** Suma los aportes individuales más el valor de corte ($b$) para obtener la lectura final en **kWh**:
    $$\hat{y} = \sum (w_i \cdot x_{\text{std}, i}) + b$$

---

## 🚀 Guía de Ejecución Local

### Prerrequisitos
Tener instalado Python 3.9+ y disponer del archivo `modelo_consumo.joblib` en la raíz del proyecto.

### 1. Instalar dependencias
```bash
pip install streamlit pandas numpy joblib
