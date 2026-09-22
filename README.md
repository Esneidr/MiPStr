# 🤖 KNN Interactivo: ¿De qué grupo soy?

Una aplicación web educativa, interactiva y sin dependencias externas diseñada para enseñar y comprender el funcionamiento del algoritmo de aprendizaje automático **K-Nearest Neighbors (KNN)** o **K-Vecinos Más Cercanos**.

Permite explorar los conceptos fundamentales de clasificación, votación por mayoría, hiperparámetro $K$, frontera de decisión, manejo de empates, efecto del ruido y normalización de variables mediante simulaciones en tiempo real.

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Modos de Uso](#-modos-de-uso)
- [Conceptos Educativos Explicados](#-conceptos-educativos-explicados)
- [Estructura del Código](#-estructura-del-código)
- [Instalación y Uso](#-instalación-y-uso)
- [Compatibilidad y Accesibilidad](#-compatibilidad-y-accesibilidad)

---

## ✨ Características Principales

1. **Visualización en Tiempo Real (`HTML5 Canvas`):**
   - Renderizado dinámico de datos bidimensionales.
   - Dibujo de la **Frontera de Decisión (Boundary Map)** en un mapa de calor sombreado.
   - Radio de alcance dinámico que encierra a los $K$ vecinos más cercanos.
   - Conexiones vectoriales directas entre la consulta y sus vecinos.

2. **Interacción Intuitiva:**
   - Haz clic en cualquier lugar del plano para colocar una consulta o nuevos datos.
   - Arrastra el punto de consulta para observar cómo evoluciona la votación en vivo.
   - Ajusta $K$ mediante un deslizador (rango $1$ a $15$).

3. **Modo Juego / Retos Integrados:**
   - Desafíos interactivos con sistema de puntuación para evaluar la comprensión del usuario (ej. forzar errores por ruido, encontrar puntos de desacuerdo según $K$).

4. **Desglose Matemático Transparente:**
   - Panel de "Cálculo de Distancia" que muestra paso a paso la fórmula de distancia euclidiana entre el punto de consulta y el vecino seleccionado.

5. **Soporte de Tema y Adaptabilidad:**
   - Soporte nativo para **Modo Claro** y **Modo Oscuro** (mediante `prefers-color-scheme`).
   - Diseño responsivo compatible con dispositivos móviles y pantallas de escritorio.

---

## 🔀 Modos de Uso

La aplicación cuenta con dos entornos de exploración:

### 1. 🔵 Plano Abstracto (`Clasificación A/B`)
* **Propósito:** Entender el comportamiento geométrico y matemático del algoritmo.
* **Funcionalidades:**
  * Elección entre agregar un punto nuevo (❓), un dato Azul (Clase A) o Naranja (Clase B).
  * Botón **"Agregar dato erróneo"**: Inserta ruido/anomalía para demostrar cómo $K=1$ se equivoca pero un $K$ mayor ($K=5$) mitiga el error.
  * Botón **"Crear empate"**: Ubica el punto en una zona donde se genera igualdad de votos.
  * Botón **"Mostrar cómo piensa KNN"**: Muestra el mapa de frontera de decisión en todo el plano.

### 2. 🌧️ Caso Real: Lluvia (`Predicción Meteorológica`)
* **Propósito:** Aplicar KNN a un problema práctico con variables del mundo real.
* **Variables:** Humedad ($\%$) y Temperatura ($^\circ C$).
* **Probabilidad:** Muestra la estimación de la probabilidad de lluvia según la proporción de días históricos lluviosos en el vecindario $K$.
* **Normalización de Variables:** Permite activar o desactivar la normalización min-max para comprender cómo variables con escalas diferentes alteran las distancias euclidianas.

---

## 🧠 Conceptos Educativos Explicados

El software permite experimentar de forma visual los siguientes pilares de Machine Learning:

| Concepto | Explicación en la App |
| :--- | :--- |
| **Distancia Euclidiana** | $d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$ expresada paso a paso. |
| **Hiperparámetro $K$** | Permite ver cómo valores pequeños de $K$ sufren de *overfitting* (sensibles al ruido) y valores grandes generan fronteras más suaves. |
| **Empates ($K$ Par)** | Ofrece 3 técnicas para resolver empates: elegir $K$ impar, vecino más cercano o votación ponderada por distancia ($w = \frac{1}{d}$). |
| **Escalado / Normalización** | Demuestra por qué la Humedad ($30-100\%$) domina sobre la Temperatura ($10-35^\circ C$) si no se normalizan las escalas. |

---

## 📐 Estructura del Código

Todo el proyecto está contenido en un único archivo autofuncional (`Single-File HTML`), distribuido de la siguiente manera:

```text
├── CSS (Estilos)
│   ├── Variables CSS (:root) -> Paleta de colores, tipografía, modo oscuro.
│   ├── Layout (Grid / Flexbox) -> Adaptación de pantalla y paneles.
│   └── Componentes -> Botones, barras de progreso, etiquetas y chips.
│
├── HTML (Estructura)
│   ├── Header y pestañas de selección de modo.
│   ├── Stage principal (<canvas>, leyendas, notas).
│   ├── Panel lateral (Controles, deslizadores, interruptores).
│   └── Paneles dinámicos (Resultados, cálculo de distancia, retos).
│
└── JavaScript (Lógica)
    ├── CFG / S -> Configuración de modos y estado global de la aplicación.
    ├── rng() / gauss() -> Generador pseudoaleatorio para reproducibilidad de datos.
    ├── knn() -> Implementación nativa del algoritmo K-Nearest Neighbors.
    ├── setGeo() / draw() -> Renderizado en Canvas 2D (puntos, fronteras, radios).
    ├── renderResult() / renderCalc() -> Inyección dinámica de UI y cálculos.
    └── Event Listeners -> Control del mouse, touch (móviles) y teclado.
