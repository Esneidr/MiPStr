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
    st.image("https://pascualbravo.edu.co/wp-content/uploads/2021/04/logo-pascual-bravo.png", use_container_width=True)
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
        "categoria": "Procesamiento de Audio",
        "fecha": "Septiembre, 2026",
        "titulo": "Conversión de texto a voz",
        "descripcion": "Aplicación basada en Inteligencia Artificial diseñada para transformar texto escrito en habla natural de forma fluida y multimodal.",
        #"imagen": "txt_to_audio2.png",
        "url": "https://imultimod.streamlit.app/",
        "label_btn": "Ir a Texto a Voz"
    },
    {
        "categoria": "Procesamiento de Audio",
        "fecha": "Septiembre, 2026",
        "titulo": "Conversión de voz a texto",
        "descripcion": "Sistema de reconocimiento de voz que permite transcribir audio a texto en tiempo real con alta precisión.",
        #"imagen": "OIG8.jpg",
        "url": "https://traductorw.streamlit.app/",
        "label_btn": "Ir a Voz a Texto"
    },
    {
        "categoria": "Generación & RAG",
        "fecha": "Septiembre, 2026",
        "titulo": "Generación en Contexto (Chat PDF)",
        "descripcion": "Aplicación de arquitectura RAG que permite realizar preguntas y respuestas fundamentadas a partir de documentos PDF.",
        #"imagen": "Chat_pdf.png",
        "url": "https://chatpdf-cc.streamlit.app/",
        "label_btn": "Ir a Chat PDF"
    },
    {
        "categoria": "Visión por Computador",
        "fecha": "Septiembre, 2026",
        "titulo": "Reconocimiento de Objetos (YOLO)",
        "descripcion": "Detección y localización de objetos múltiples en imágenes mediante modelos avanzados de la familia YOLO.",
        #"imagen": "txt_to_audio.png",
        "url": "https://yolov5cmc.streamlit.app/",
        "label_btn": "Ir a YOLO Objeto"
    },
    {
        "categoria": "Análisis de Datos",
        "fecha": "Septiembre, 2026",
        "titulo": "Análisis de Datos con Agentes",
        "descripcion": "Plataforma de análisis avanzado de datos potenciada por agentes inteligentes para interpretación de métricas.",
        #"imagen": "data_analisis.png",
        "url": "https://dataagente.streamlit.app/",
        "label_btn": "Ir a Agente de Datos"
    },
    {
        "categoria": "Visión por Computador",
        "fecha": "Septiembre, 2026",
        "titulo": "Análisis de Imagen con Visión Multimodal",
        "descripcion": "Uso de modelos de visión avanzada (GPT-4o) para la interpretación, descripción y extracción de contexto en imágenes.",
        #"imagen": "OIG4.jpg",
        "url": "https://vision2-gpt4o.streamlit.app/",
        "label_btn": "Ir a Visión GPT-4o"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Septiembre, 2026",
        "titulo": "Entrenando Modelos",
        "descripcion": "Demostración interactiva sobre cómo desplegar e interactuar con modelos de IA entrenados a medida.",
        #"imagen": "OIG5.jpg",
        "url": "https://xn3pg24ztuv6fdiqon8qn3.streamlit.app/",
        "label_btn": "Ir a Modelo Entrenado"
    },
    {
        "categoria": "Procesamiento de Audio / Video",
        "fecha": "Septiembre, 2026",
        "titulo": "Transcriptor Audio y Video (Whisper)",
        "descripcion": "Herramienta de transcripción automática de archivos de audio y video utilizando la tecnología Whisper.",
        #"imagen": "OIG3.jpg",
        "url": "https://transcript-whisper.streamlit.app/",
        "label_btn": "Ir a Transcriptor"
    },
    {
        "categoria": "Sistemas Ciberfísicos",
        "fecha": "Septiembre, 2026",
        "titulo": "Sistema Ciberfísico",
        "descripcion": "Interacción entre algoritmos de visión por computador y entornos físicos para aplicaciones avanzadas.",
        #"imagen": "OIG6.jpg",
        "url": "https://vision2-gpt4o.streamlit.app/",
        "label_btn": "Ir a Sistema Ciberfísico"
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
