# 🎯 App Interactiva de Descenso de Gradiente

Una aplicación web educativa desarrollada con **Streamlit** para explorar visualmente el comportamiento y la convergencia del algoritmo de Descenso de Gradiente en problemas de optimización y Machine Learning.

Este proyecto forma parte del **Módulo 3: Cálculo Aplicado** de la materia *Matemáticas para IA* en la **Universidad EAFIT**.

## 🚀 Características principales

* **Visualización 3D Interactiva:** Gráficos en tiempo real de la superficie de una función matemática y la trayectoria exacta que recorre el algoritmo.
* **Control de Hiperparámetros:** Deslizadores interactivos para modificar la tasa de aprendizaje ($\eta$), el punto de partida $(x_0, y_0)$ y el número de iteraciones.
* **Modo de Comparación:** Panel para contrastar simultáneamente 4 tasas de aprendizaje diferentes y observar de primera mano la convergencia, oscilación o divergencia.
* **Caso Práctico Integrado:** Aplicación real del algoritmo para resolver una **Regresión Lineal** que predice el consumo energético (kWh) en base a la temperatura ambiente, minimizando el Error Cuadrático Medio (MSE).

## 🛠️ Requisitos e Instalación

Asegúrate de tener Python instalado y ejecuta el siguiente comando para instalar las dependencias necesarias:

```bash
pip install streamlit numpy matplotlib
