import streamlit as st
from PIL import Image

# Configuración de página
st.set_page_config(page_title="Portafolio de Aplicaciones IA", layout="wide")

# CSS Personalizado para imitar las tarjetas de la imagen de referencia
st.markdown("""
<style>
    /* Estilo para las etiquetas de categoría (badge azul) */
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
    
    /* Fecha o texto secundario */
    .date-text {
        color: #5f6368;
        font-size: 14px;
        margin-bottom: 6px;
    }

    /* Título de la tarjeta */
    .card-title {
        font-size: 20px;
        font-weight: bold;
        color: #1a1a1a;
        margin-bottom: 8px;
        line-height: 1.3;
    }

    /* Descripción */
    .card-description {
        color: #3c4043;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Título Principal
st.title("Aplicaciones de Inteligencia Artificial")

# Barra Lateral
with st.sidebar:
    st.subheader("Aplicaciones con Inteligencia Artificial")
    parrafo = (
        "La inteligencia artificial permite mejorar la toma de decisiones con el uso de datos, "
        "automatizar tareas rutinarias y proporcionar análisis avanzados en tiempo real, lo que "
        "resulta en una mayor eficiencia y precisión en diversos campos."
    )
    st.write(parrafo)

url_ia = "https://sites.google.com/view/aplicacionesdeia/inicio"
st.subheader("En el siguiente enlace puedes encontrar páginas y ejercicios prácticos")
st.markdown(f"🔗 [Acceder a Páginas y Ejercicios Prácticos]({url_ia})")
st.divider()

# Lista de proyectos para renderizar dinámicamente
proyectos = [
    {
        "categoria": "Procesamiento de Audio",
        "fecha": "Septiembre, 2026",
        "titulo": "Conversión de texto a voz",
        "descripcion": "Aplicación basada en Inteligencia Artificial diseñada para transformar texto escrito en habla natural de forma fluida y multimodal.",
        "imagen": "txt_to_audio2.png",
        "url": "https://imultimod.streamlit.app/",
        "label_btn": "Ir a Texto a Voz"
    },
    {
        "categoria": "Procesamiento de Audio",
        "fecha": "Septiembre, 2026",
        "titulo": "Conversión de voz a texto",
        "descripcion": "Sistema de reconocimiento de voz que permite transcribir audio a texto en tiempo real con alta precisión.",
        "imagen": "OIG8.jpg",
        "url": "https://traductorw.streamlit.app/",
        "label_btn": "Ir a Voz a Texto"
    },
    {
        "categoria": "Generación & RAG",
        "fecha": "Septiembre, 2026",
        "titulo": "Generación en Contexto (Chat PDF)",
        "descripcion": "Aplicación de arquitectura RAG que permite realizar preguntas y respuestas fundamentadas a partir de documentos PDF.",
        "imagen": "Chat_pdf.png",
        "url": "https://chatpdf-cc.streamlit.app/",
        "label_btn": "Ir a Chat PDF"
    },
    {
        "categoria": "Visión por Computador",
        "fecha": "Septiembre, 2026",
        "titulo": "Reconocimiento de Objetos (YOLO)",
        "descripcion": "Detección y localización de objetos múltiples en imágenes mediante modelos avanzados de la familia YOLO.",
        "imagen": "txt_to_audio.png",
        "url": "https://yolov5cmc.streamlit.app/",
        "label_btn": "Ir a YOLO Objeto"
    },
    {
        "categoria": "Análisis de Datos",
        "fecha": "Septiembre, 2026",
        "titulo": "Análisis de Datos con Agentes",
        "descripcion": "Plataforma de análisis avanzado de datos potenciada por agentes inteligentes para interpretación de métricas.",
        "imagen": "data_analisis.png",
        "url": "https://dataagente.streamlit.app/",
        "label_btn": "Ir a Agente de Datos"
    },
    {
        "categoria": "Visión por Computador",
        "fecha": "Septiembre, 2026",
        "titulo": "Análisis de Imagen con Visión Multimodal",
        "descripcion": "Uso de modelos de visión avanzada (GPT-4o) para la interpretación, descripción y extracción de contexto en imágenes.",
        "imagen": "OIG4.jpg",
        "url": "https://vision2-gpt4o.streamlit.app/",
        "label_btn": "Ir a Visión GPT-4o"
    },
    {
        "categoria": "Machine Learning",
        "fecha": "Septiembre, 2026",
        "titulo": "Entrenando Modelos",
        "descripcion": "Demostración interactiva sobre cómo desplegar e interactuar con modelos de IA entrenados a medida.",
        "imagen": "OIG5.jpg",
        "url": "https://xn3pg24ztuv6fdiqon8qn3.streamlit.app/",
        "label_btn": "Ir a Modelo Entrenado"
    },
    {
        "categoria": "Procesamiento de Audio / Video",
        "fecha": "Septiembre, 2026",
        "titulo": "Transcriptor Audio y Video (Whisper)",
        "descripcion": "Herramienta de transcripción automática de archivos de audio y video utilizando la tecnología Whisper.",
        "imagen": "OIG3.jpg",
        "url": "https://transcript-whisper.streamlit.app/",
        "label_btn": "Ir a Transcriptor"
    },
    {
        "categoria": "Sistemas Ciberfísicos",
        "fecha": "Septiembre, 2026",
        "titulo": "Sistema Ciberfísico",
        "descripcion": "Interacción entre algoritmos de visión por computador y entornos físicos para aplicaciones avanzadas.",
        "imagen": "OIG6.jpg",
        "url": "https://vision2-gpt4o.streamlit.app/",
        "label_btn": "Ir a Sistema Ciberfísico"
    }
]

# Renderizado de Tarjetas estilo Card (Imagen a la izquierda, texto a la derecha)
for proj in proyectos:
    with st.container(border=True):
        col_img, col_info = st.columns([1, 2.5], gap="medium")
        
        # Columna de la Imagen
        with col_img:
            try:
                img = Image.open(proj["imagen"])
                st.image(img, use_container_width=True)
            except Exception:
                # Placeholder si no se encuentra la imagen local
                st.info(f"Imagen: {proj['imagen']}")
        
        # Columna de la Información (Badge, Fecha, Título, Descripción, Enlace)
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
