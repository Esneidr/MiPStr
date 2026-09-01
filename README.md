# 🌊 Monitor de Nivel de Ríos y Quebradas — CORNARE / MARCO

Este proyecto es un panel de control interactivo en **Streamlit** que se conecta en tiempo real a la API pública de **CORNARE** (Corporación Autónoma Regional de las Cuencas de los Ríos Negro y Nare). 

Su propósito es permitir la **consulta, visualización geográfica, análisis estadístico y control de calidad de datos hidrológicos** (niveles de agua en metros) registrados por estaciones de monitoreo ambiental.

---

## 🔍 ¿Qué hace este código? (Descripción del Flujo)

El script actúa como una interfaz cliente que consume servicios web tipo REST API, procesa datos en memoria con **Pandas** y renderiza un cuadro de mando con las siguientes capacidades:

### ⚙️ 1. Barra Lateral de Configuración (Sidebar)
Permite al usuario/estudiante personalizar la consulta en tiempo real:
*   **Identificación:** Nombre del analista a cargo de la consulta.
*   **Filtros de API:** Selección del código de la estación hidrológica, rango de fechas (*Desde / Hasta*) y filtrado por calidad del dato (datos validados vs. datos crudos).

### 🌐 2. Módulo de Peticiones y Manejo de Paginación (`requests`)
*   **Consulta HTTP Asíncrona:** Realiza peticiones `GET` a la API de CORNARE pasando parámetros de fecha y calidad.
*   **Paginación Automática:** Implementa un bucle inteligente (`obtener_todas_las_paginas`) que detecta la propiedad `next` en las respuestas JSON para extraer el 100% de los registros, sin importar cuántas páginas abarque la consulta.
*   **Inspección de Metadatos:** Analiza dinámicamente las claves del JSON entrante buscando coordenadas geográficas (`lat`, `lon`, `latitude`, etc.). Si la API no provee ubicación exacta, utiliza una coordenada de referencia geográfica por defecto.

### 📊 3. Motor de Cálculo de Calidad del Dato
Incluye un algoritmo interno (`calcular_indice_calidad`) que evalúa la confiabilidad de la serie de tiempo asignando una puntuación de **0 a 100%**:
1.  **Completitud de la serie (70% del peso):** Detecta la frecuencia típica entre lecturas y calcula cuántos "huecos" o intervalos de tiempo faltan en el rango solicitado.
2.  **Detección de Anomalías (30% del peso):** Aplica el método estadístico del **Rango Intercuartílico ($1.5 \times \text{IQR}$)** para identificar valores atípicos (*outliers*) o lecturas físicamente imposibles (niveles de agua negativos).

### 📈 4. Visualización e Interfaz Gráfica (Streamlit)
Una vez procesados los datos, la aplicación genera:
*   **KPIs en Tiempo Real:** Métricas destacadas con el total de lecturas, el nivel promedio de la fuente hídrica, la calificación del índice de calidad y la cantidad de anomalías detectadas.
*   **Serie Temporal Graficada:** Un gráfico de líneas interactivo con el comportamiento hidrológico a lo largo del tiempo.
*   **Geolocalización:** Mapa interactivo integrado que marca el punto exacto de la estación de monitoreo.
*   **Auditoría y Exportación:** Desplegables con el detalle técnico de los datos crudos y un botón de descarga directa en formato `.csv` para posteriores análisis en Excel o Python.
