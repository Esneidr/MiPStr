import streamlit as st
from PIL import Image

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================
st.set_page_config(
    page_title="Portafolio de Aplicaciones IA - I.U. Pascual Bravo",
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS PERSONALIZADO
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo general */
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
    }

    /* ---------- HERO ---------- */
    .hero {
        background: linear-gradient(135deg, #1a73e8 0%, #6a4cff 100%);
        padding: 40px 36px;
        border-radius: 20px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 12px 32px rgba(26,115,232,0.25);
        position: relative;
        overflow: hidden;
    }
    .hero::after {
        content: "";
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }
    .hero h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 38px;
        margin: 0 0 8px 0;
        font-weight: 800;
        color: #ffffff;
    }
    .hero p {
        font-size: 16px;
        opacity: 0.95;
        margin: 0;
        max-width: 720px;
    }

    /* ---------- INFO HEADER ---------- */
    .info-header {
        background: #ffffff;
        border-left: 5px solid #1a73e8;
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    }
    .info-header h4 {
        margin: 0;
        color: #1a73e8;
        font-family: 'Poppins', sans-serif;
        font-size: 18px;
    }
    .info-header p {
        margin: 6px 0 0 0;
        color: #3c4043;
        font-size: 14px;
    }

    /* ---------- MÉTRICAS ---------- */
    .metric-strip {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 22px 0 32px 0;
    }
    .metric-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border-top: 3px solid #1a73e8;
        transition: transform 0.2s ease;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-size: 26px;
        font-weight: 800;
        color: #1a73e8;
        margin: 0;
    }
    .metric-label {
        font-size: 13px;
        color: #5f6368;
        margin-top: 4px;
        font-weight: 500;
    }

    /* ---------- TARJETAS DE PROYECTO ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border-radius: 16px !important;
        border: 1px solid #e6e9ef !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        transition: all 0.25s ease;
        padding: 6px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 10px 28px rgba(26,115,232,0.15);
        border-color: #1a73e8 !important;
        transform: translateY(-3px);
    }

    .badge {
        background: linear-gradient(135deg, #1a73e8, #6a4cff);
        color: white;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
        letter-spacing: 0.3px;
    }

    .date-text {
        color: #5f6368;
        font-size: 13px;
        margin-bottom: 6px;
        font-weight: 500;
    }

    .card-title {
        font-family: 'Poppins', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 10px;
        line-height: 1.3;
    }

    .card-description {
        color: #3c4043;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 14px;
    }

    /* ---------- BOTÓN LINK ---------- */
    div[data-testid="stLinkButton"] a {
        background: linear-gradient(135deg, #1a73e8, #6a4cff) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 22px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease;
    }
    div[data-testid="stLinkButton"] a:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(26,115,232,0.35);
    }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f4f7fb 100%);
        border-right: 1px solid #e6e9ef;
    }
    section[data-testid="stSidebar"] h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 20px;
        color: #1a73e8;
    }

    .profile-card {
        background: linear-gradient(135deg, #1a73e8, #6a4cff);
        border-radius: 14px;
        padding: 18px;
        color: white;
        margin-bottom: 16px;
        box-shadow: 0 8px 20px rgba(26,115,232,0.25);
    }
    .profile-card h3 {
        margin: 0 0 4px 0;
        font-family: 'Poppins', sans-serif;
        font-size: 17px;
    }
    .profile-card p {
        margin: 2px 0;
        font-size: 13px;
        opacity: 0.92;
    }

    /* ---------- FOOTER ---------- */
    .footer {
        margin-top: 50px;
        padding: 28px;
        background: #1a1a1a;
        color: #d1d5db;
        border-radius: 16px;
        text-align: center;
        font-size: 13px;
    }
    .footer strong { color: #ffffff; }
    .footer .accent { color: #6a9bff; }
</style>
""", unsafe_allow_html=True)


# =========================================================
# BARRA LATERAL (INFORMACIÓN ACADÉMICA Y PROYECTO)
# =========================================================
with st.sidebar:
    st.image("images/Logo_Pascual_Bravo_2.png", use_container_width=True)

    st.markdown("""
    <div class="profile-card">
        <h3>🎓 Datos del Proyecto</h3>
        <p><b>👨‍💻 Estudiante:</b> Esneider Córdoba</p>
        <p><b>👨‍🏫 Docente:</b> Carlos Mario Correa</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
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


# =========================================================
# HERO PRINCIPAL
# =========================================================
st.markdown("""
<div class="hero">
    <h1>🤖 Aplicaciones de Inteligencia Artificial</h1>
    <p>Portafolio interactivo de proyectos académicos desarrollados en la asignatura de Programación Avanzada.</p>
</div>
""", unsafe_allow_html=True)

# Bloque destacado con la información del curso e institución
st.markdown("""
<div class="info-header">
    <h4>🏛️ I.U. Pascual Bravo | Medellín, Colombia</h4>
    <p><b>Programa:</b> Ingeniería en Desarrollo de Software | <b>Materia:</b> Programación Avanzada</p>
    <p><b>Estudiante:</b> Esneider Córdoba | <b>Docente:</b> Carlos Mario Correa</p>
</div>
""", unsafe_allow_html=True)

# Franja de métricas (visual, sin alterar contenido)
st.markdown("""
<div class="metric-strip">
    <div class="metric-card">
        <p class="metric-value">11</p>
        <p class="metric-label">Aplicaciones publicadas</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">ML</p>
        <p class="metric-label">Categoría principal</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">2026</p>
        <p class="metric-label">Periodo académico</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">Streamlit</p>
        <p class="metric-label">Tecnología base</p>
    </div>
</div>
""", unsafe_allow_html=True)

url_ia = "https://sites.google.com/view/aplicacionesdeia/inicio"
st.subheader("🔗 En el siguiente enlace puedes encontrar páginas y ejercicios prácticos")
st.markdown(f"[Acceder a Páginas y Ejercicios Prácticos]({url_ia})")
st.divider()


# =========================================================
# LISTA DE PROYECTOS
# =========================================================
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


# =========================================================
# RENDERIZADO DE LAS TARJETAS
# =========================================================
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
                <div class="date-text">📅 {proj['fecha']}</div>
                <div class="card-title">{proj['titulo']}</div>
                <div class="card-description">{proj['descripcion']}</div>
                """,
                unsafe_allow_html=True
            )
            st.link_button(proj["label_btn"], proj["url"])


# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    <p><strong>Portafolio de Aplicaciones de Inteligencia Artificial</strong></p>
    <p>I.U. Pascual Bravo · Ingeniería en Desarrollo de Software · Programación Avanzada</p>
    <p>Estudiante: <span class="accent">Esneider Córdoba</span> · Docente: <span class="accent">Carlos Mario Correa</span></p>
    <p style="margin-top:8px; opacity:0.7;">Medellín, Colombia · 2026</p>
</div>
""", unsafe_allow_html=True)
