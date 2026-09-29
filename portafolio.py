import streamlit as st
from PIL import Image

# Configuración de página
st.set_page_config(
    page_title="Portafolio de Aplicaciones IA - I.U. Pascual Bravo", 
    layout="wide",
    page_icon="🤖"
)

# CSS Personalizado para las tarjetas y bloques de información
st.markdown("""
<style>
    /* Estilo para tarjetas de proyectos */
    .badge {
        background-color: #1a73e8;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    .date-text {
        color: #5f6368;
        font-size: 14px;
        margin-bottom: 6px;
    }

    .card-title {
        font-size: 20px;
        font-weight: bold;
        color: #1a1a1a;
        margin-bottom: 8px;
        line-height: 1.3;
    }

    .card-description {
        color: #3c4043;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    /* Estilo para información académica */
    .info-header {
        background-color: #f8f9fa;
        border-left: 5px solid #1a73e8;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (INFORMACIÓN ACADÉMICA Y PROYECTO) ---
with st.sidebar:
    st.image("images/Logo_Pascual_Bravo_2.png", use_container_width=True)
    st.title("🎓 Datos del Proyecto")
    
    st.markdown("""
    **👨‍💻 Realizado por:**  
    Esneider Córdoba  
    
    **👨‍🏫 Profesor:**  
    Carlos Mario Correa  
    
    **📚 Asignatura:**  
    Programación Avanzada  
    
    **🎓 Carrera:**  
    Ingeniería en Desarrollo de Software  
    
    **🏛️ Institución:**  
    I.U. Pascual Bravo  
    
    **📍 Ubicación:**  
    Medellín, Colombia  
    """)
    st.divider()
    
    st.subheader("💡 Sobre las Aplicaciones")
    parrafo = (
        "La inteligencia artificial permite mejorar la toma de decisiones con el uso de datos, "
        "automatizar tareas rutinarias y proporcionar análisis avanzados en tiempo real, lo que "
        "resulta en una mayor eficiencia y precisión en diversos campos."
    )
    st.write(parrafo)

# --- ENCABEZADO PRINCIPAL ---
st.title("Aplicaciones de Inteligencia Artificial")

# Bloque destacado con la información del curso e institución
st.markdown("""
<div class="info-header">
    <h4 style="margin:0; color:#1a73e8;">🏛️ I.U. Pascual Bravo | Medellín, Colombia</h4>
    <p style="margin:5px 0 0 0;"><b>Programa:</b> Ingeniería en Desarrollo de Software | <b>Materia:</b> Programación Avanzada</p>
    <p style="margin:2px 0 0 0;"><b>Estudiante:</b> Esneider Córdoba | <b>Docente:</b> Carlos Mario Correa</p>
</div>
""", unsafe_allow_html=True)

url_ia = "https://sites.google.com/view/aplicacionesdeia/inicio"
st.subheader("En el siguiente enlace puedes encontrar páginas y ejercicios prácticos")
st.markdown(f"🔗 [Acceder a Páginas y Ejercicios Prácticos]({url_ia})")
st.divider()

# --- LISTA DE PROYECTOS ---
proyectos = [
    {
        "categoria": "Machine Learning",
        "fecha": "Agosto, 2026",
        "titulo": "Calculo aplicado, gradiente",
        "descripcion": "Una aplicación para explorar visualmente el comportamiento y la convergencia del algoritmo de Descenso de Gradiente en problemas de optimización y Machine Learning.",
        "imagen": "images/gradiente.png",
        "url": "https://mipstr-7wje3fzgnedzpabcgidfqq.streamlit.app/",
        "label_btn": "Explorar"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Agosto, 2026",
        "titulo": "Detección de anomalías",
        "descripcion": "Aplicación web interactiva. Su objetivo principal es demostrar visual y cuantitativamente cómo una misma decisión lógica puede ejecutarse de manera ineficiente usando bucles tradicionales frente a una implementación optimizada (vectorizada) con NumPy.",
        "imagen": "images/detector_anomalias.png",
        "url": "https://mipstr-bn36ak2fzsqtq7ingnpwnt.streamlit.app/",
        "label_btn": "Explorar"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Agosto, 2026",
        "titulo": "Preparación de datos",
        "descripcion": "Este proyecto es una aplicación web interactiva diseñada para visualizar y experimentar con los pasos críticos del Procesamiento y Limpieza de Datos (Pipeline de ETL) antes de entrenar cualquier modelo de Machine Learning o Inteligencia Artificial.",
        "imagen": "images/preparacion_datos.png",
        "url": "https://mipstr-7uddnptkcyerxukdtggxoy.streamlit.app/",
        "label_btn": "Explorar"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Agosto, 2026",
        "titulo": "Monitoreo de nivel de agua",
        "descripcion": "Este proyecto es un panel de control interactivo que se conecta en tiempo real a la API pública de CORNARE. Su propósito es permitir la consulta, visualización geográfica, análisis estadístico y control de calidad de datos hidrológicos (niveles de agua en metros) registrados por estaciones de monitoreo ambiental.",
        "imagen": "images/nivel_rio.png",
        "url": "https://mipstr-5o4jjuy7yrevvawy9rijqn.streamlit.app/#nivel-de-rios-y-quebradas-cornare",
        "label_btn": "Explorar"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Septiembre, 2026",
        "titulo": "Regresión lineal",
        "descripcion": "Aplicación educativa e interactiva diseñada para enseñar las bases teóricas y prácticas de los algoritmos de regresión en Machine Learning. Utilizando datos reales del Censo de Vivienda de California (1990) de scikit-learn, el cuadro de mando permite descomponer y manipular todas las etapas involucradas en el entrenamiento, optimización y evaluación de modelos predictivos continuos.",
        "imagen": "images/regresion_lineal.png",
        "url": "https://mipstr-923mzfjnarosjb8hsfysyq.streamlit.app/",
        "label_btn": "Explorar"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Septiembre, 2026",
        "titulo": "Series de tiempo",
        "descripcion": "Aplicación interactiva que permite explorar, analizar y modelar series temporales continuas mediante la simulación en tiempo real de un sensor de temperatura IoT (DHT22).",
        "imagen": "images/series_tiempo.png",
        "url": "https://mipstr-bp5qqtcjroax2fnudvgjwz.streamlit.app/",
        "label_btn": "Explorar"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Septiembre, 2026",
        "titulo": "Predicción y modelado de la calidad de aire",
        "descripcion": "Permite realizar pronósticos hacia adelante de material particulado (PM2.5 y PM10) utilizando datos de las estaciones de monitoreo ambiental de la cuenca CORNARE.",
        "imagen": "images/prediccion.png",
        "url": "https://mipstr-4gj8evjlxzsjvzp3swkaco.streamlit.app/",
        "label_btn": "Explorar"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Septiembre, 2026",
        "titulo": "Sistema de IOT Captura de datos y procesamiento",
        "descripcion": "Aplicación interactiva que consulta datos en tiempo real desde InfluxDB Cloud (provenientes de un sensor ESP32 + DHT22), procesa la serie de tiempo, entrena un modelo de Regresión Lineal Múltiple con scikit-learn y permite realizar predicciones de sensación térmica.",
        "imagen": "images/IOT.png",
        "url": "https://mipstr-fckie2ywgeueminysuxjar.streamlit.app/",
        "label_btn": "Explorar"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Septiembre, 2026",
        "titulo": "Regresión logísitica",
        "descripcion": "Aplicación interactiva que implementa un modelo de Regresión Logística para predecir si lloverá al día siguiente. Permite ajustar variables predictoras, modificar el umbral de decisión y simular nuevos días de manera interactiva.",
        "imagen": "images/logistica.png",
        "url": "https://mipstr-dcwpxewdzxutuejplyrsmb.streamlit.app/",
        "label_btn": "Explorar"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Septiembre, 2026",
        "titulo": "Clasificación KNN",
        "descripcion": "Una aplicación web educativa, interactiva con un algoritmo de aprendizaje automático K-Nearest Neighbors (KNN) o K-Vecinos Más Cercanos.",
        "imagen": "images/KNN.png",
        "url": "https://mipstr-9etfvoafm54yhpj4nwduyp.streamlit.app/",
        "label_btn": "Explorar"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Septiembre, 2026",
        "titulo": "Clasificación de fertilidad de  suelos",
        "descripcion": "Una aplicación web educativa, interactiva con un algoritmo de aprendizaje automático KNN El proyecto utiliza datos abiertos del Laboratorio de Química y Física de Suelos de AGROSAVIA para abordar el caso de uso real de diagnóstico y clasificación de la fertilidad del suelo en tres categorías: baja, media y alta.",
        "imagen": "images/suelos.png",
        "url": "https://mipstr-9etfvoafm54yhpj4nwduyp.streamlit.app/",
        "label_btn": "Explorar"
    }
]

# --- RENDERIZADO DE LAS TARJETAS (STYLE CARD HORIZONTAL) ---
for proj in proyectos:
    with st.container(border=True):
        col_img, col_info = st.columns([1, 2.5], gap="medium")
        
        with col_img:
            try:
                img = Image.open(proj["imagen"])
                st.image(img, use_container_width=True)
            except Exception:
                st.info(f"Imagen: {proj['imagen']}")
        
        with col_info:
            st.markdown(
                f"""
                <span class="badge">{proj['categoria']}</span>
                <div class="date-text">{proj['fecha']}</div>
                <div class="card-title">{proj['titulo']}</div>
                <div class="card-description">{proj['descripcion']}</div>
                """,
                unsafe_allow_html=True
            )
            st.link_button(proj["label_btn"], proj["url"])
