# 🚨 Detector de Anomalías: Lógica + Big-O + NumPy

Este proyecto es una aplicación web interactiva desarrollada con **Streamlit** diseñada para enseñar conceptos de **Matemáticas Discretas y Complejidad Algorítmica (Módulo 4)**. Su objetivo principal es demostrar visual y cuantitativamente cómo una misma decisión lógica puede ejecutarse de manera ineficiente usando bucles tradicionales frente a una implementación optimizada (vectorizada) con NumPy.

---

## 🛠️ Tecnologías Utilizadas

*   **Python 3**
*   **Streamlit:** Para la interfaz gráfica interactiva.
*   **NumPy:** Para la generación de datos sintéticos y operaciones vectorizadas de alto rendimiento.
*   **Matplotlib:** Para la visualización de datos, dispersión de alarmas y curvas de complejidad.
*   **Pandas:** Para la visualización estructurada de los datos generados.

---

## 🔍 Funcionalidades Clave

La aplicación se divide en tres secciones (pestañas) interactivas:

### 1. Simulación de Alarma
Aplica una regla lógica basada en proposiciones combinadas con un operador **AND**:
$$\text{Alarma} = (\text{temperatura} > \text{umbral}) \land (\text{humedad} < \text{umbral})$$
*   Permite ajustar el tamaño de la muestra ($n$) y los umbrales mediante deslizadores.
*   Muestra un gráfico de dispersión en tiempo real separando los datos normales (azul) de las anomalías (rojo).

### 2. Notación Big-O (Complejidad)
*   Grafica visualmente el crecimiento teórico de distintas complejidades algorítmicas ($O(1)$, $O(n)$, $O(n \log n)$, $O(n^2)$).
*   Explica de forma didáctica que aunque el bucle (`for`) y NumPy comparten la misma complejidad teórica **$O(n)$**, la constante de ejecución real es drásticamente diferente.

### 3. Benchmark en Vivo
*   Permite ejecutar un test de estrés con muestras de datos masivas (hasta 1,000,000 de registros).
*   Mide con alta precisión (`time.perf_counter()`) el tiempo de ejecución de un bucle nativo de Python versus la vectorización de NumPy.
*   Calcula el *speedup* real y genera una gráfica de barras comparativa. ¡NumPy suele ser cientos de veces más rápido!

---

## ⚡ Demostración del Código Principal

El núcleo del proyecto radica en comparar estas dos formas de resolver el mismo problema:

### Enfoque Ingenuo (Bucle tradicional)
```python
def alarma_logica_loop(temperaturas, humedades, temp_umbral, hum_umbral):
    resultados = []
    for temp, hum in zip(temperaturas, humedades):
        resultados.append(temp > temp_umbral and hum < hum_umbral)
    return np.array(resultados)
