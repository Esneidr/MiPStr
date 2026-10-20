# ⚡ Eficiencia y Paralelismo en Python

Este proyecto es una aplicación web interactiva desarrollada con **Streamlit** que sirve como material de apoyo práctico para la clase de **Computación Avanzada (Módulo 11)**. 

Su propósito principal es permitir a los estudiantes experimentar en vivo con conceptos de **concurrencia, paralelismo, vectorización y aceleración algorítmica** utilizando un entorno visual e intuitivo, comparando el rendimiento de diferentes enfoques en tiempo real.

---

## 🔍 ¿Qué hace este código? (Descripción de Pestañas)

La aplicación guía al usuario a través de 5 módulos conceptuales más un cuestionario interactivo de evaluación:

### 🏠 Inicio & Conceptos Fundamentales
*   **Inspección del Sistema:** Detecta y muestra automáticamente el número de núcleos (`CPU cores`) disponibles en el servidor/máquina donde se ejecuta.
*   **Glosario y Fundamentos:** Explica la diferencia entre tareas I/O-bound (espera) y CPU-bound (cálculo), además de definir los roles de *workers*, *executors*, hilos (*threads*) y procesos (*multiprocessing*).

### 1️⃣ Hilos (`ThreadPoolExecutor`): Tareas I/O-Bound
*   **Demostración Práctica:** Simula la lectura concurrente de múltiples sensores IoT por red WiFi (`time.sleep`).
*   **Experimento:** Permite variar el número de sensores (2 a 16) y la cantidad de *workers* concurrentes para demostrar cómo los hilos aceleran las tareas de espera, superando el límite de núcleos del procesador al solapar tiempos muertos.

### 2️⃣ Procesos (`ProcessPoolExecutor`): Tareas CPU-Bound
*   **Demostración Práctica:** Procesa millones de operaciones matemáticas intensivas por sensor.
*   **Impacto del GIL (*Global Interpreter Lock*):** Compara el rendimiento entre ejecución **Serial**, **Hilos** y **Procesos**. Demuestra por qué el GIL de Python impide que los hilos aceleren tareas puramente matemáticas y cómo los procesos independientes evitan esta barrera utilizando un núcleo por proceso.

### 3️⃣ Vectorización con NumPy
*   **Comparativa de Rendimiento:** Evalúa la velocidad de un ciclo `for` tradicional de Python frente a la vectorización nativa de **NumPy** en transformaciones masivas (conversión de °C a °F sobre hasta 2,000,000 de lecturas).
*   **Comparativa Tripartita:** Contrasta el procesamiento de sensores ejecutado mediante un bucle Serial, Multiprocesamiento y Operaciones Vectorizadas de NumPy, demostrando por qué vectorizar suele ser el primer paso óptimo antes de paralelizar.

### 4️⃣ Simulador de la Ley de Amdahl
*   **Fundamento Teórico:** Explora el límite matemático de aceleración (*Speedup*) que puede alcanzar un programa en función de su fracción paralelizable ($p$) y el número de *workers* ($N$):
    $$\text{Speedup} = \frac{1}{(1-p) + \frac{p}{N}}$$
*   **Simulación Interactiva:** Incluye controles deslizantes para ajustar $p$ y $N$, generando la curva de rendimiento de Altair y el techo máximo teórico ($\frac{1}{1-p}$).
*   **Validación con Código Real:** Ejecuta un programa que combina una fase serial fija con una fase paralelizable para comprobar si la aceleración empírica coincide con la predicción teórica.

### 📝 Preguntas y Evaluación
*   Formulario interactivo donde los estudiantes responden a 3 preguntas de análisis basadas en las métricas obtenidas durante los experimentos.
*   **Exportación de Resultados:** Genera y permite descargar un archivo de texto (`.txt`) que empaqueta el nombre del estudiante, sus respuestas escritas y los tiempos/métricas medidos automáticamente en la app.

---

## 🛠️ Estructura del Repositorio

*   `app.py`: Script principal de la aplicación Streamlit con la interfaz de usuario, simuladores y lógica de visualización.
*   `tareas.py`: Módulo auxiliar que contiene las funciones de trabajo (I/O y CPU bound). **Nota:** Es indispensable mantener estas funciones en un archivo independiente para permitir la correcta instanciación de procesos vía `multiprocessing` / `ProcessPoolExecutor`.
*   `requirements.txt`: Lista de dependencias del proyecto (`streamlit`, `numpy`, `pandas`, `altair`).

---

## 🚀 Instalación y Ejecución Local

1.  **Clona este repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
    cd tu-repositorio
    ```

2.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecuta la aplicación:**
    ```bash
    streamlit run app.py
    ```

---

## ☁️ Despliegue en Streamlit Community Cloud

1. Suba los tres archivos (`app.py`, `tareas.py`, `requirements.txt`) a un repositorio de GitHub.
2. Inicie sesión en [Streamlit Cloud](https://share.streamlit.io/) y haga clic en **Create app**.
3. Seleccione el repositorio, la rama principal y defina `app.py` como el **Main file path**.
4. Presione **Deploy**.
