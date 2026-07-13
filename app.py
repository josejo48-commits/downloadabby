import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA (Coloca el nombre de la app)
st.set_page_config(
    page_title="DownloadAbby",
    page_icon="📥",  # Icono temporal de la pestaña mientras subimos la imagen real
    layout="centered"
)

# 2. ESTILOS CSS PERSONALIZADOS (Para darle el fondo rosa y la apariencia de la app)
st.markdown("""
    <style>
    /* Cambiar el fondo de toda la aplicación a rosa pastel */
    .stApp {
        background-color: #FCE4EC;
    }
    
    /* Estilo para los títulos principales */
    .titulo-principal {
        text-align: center; 
        color: #EC407A; 
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .subtitulo {
        text-align: center; 
        color: #555555; 
        font-size: 18px;
        margin-top: 0px;
        margin-bottom: 20px;
    }
    
    /* Estilo para las tarjetas blancas redondeadas */
    .tarjeta-blanca {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CONTENIDO VISUAL DE LA APP

# Imagen del logo centrada (Aquí es donde colocaremos tu logo en el siguiente paso)
# Por ahora dejamos el espacio listo y centrado
st.markdown("<div style='text-align: center;'><h2>📥</h2></div>", unsafe_allow_html=True)

# Títulos
st.markdown("<h1 class='titulo-principal'>DOWNLOAD ABBY</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo'>Tu descargador tierno y rápido</p>", unsafe_allow_html=True)

# Caja Blanca Redondeada para pegar el enlace
st.markdown("<div class='tarjeta-blanca'>", unsafe_allow_html=True)
st.subheader("🎵 Pegar Enlace")
url = st.text_input("Introduce la URL del video de YouTube o TikTok:", placeholder="https://...")
formato = st.radio("Elige el formato de descarga:", ["Audio (MP3)", "Video (MP4)"], horizontal=True)
st.markdown("</div>", unsafe_allow_html=True)

# Caja Blanca Redondeada para el Historial Simulada
st.markdown("<h3 style='color: black;'>Download History</h3>", unsafe_allow_html=True)

st.markdown("""
    <div class='tarjeta-blanca' style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: black;'>Down Abby's Final Vid</strong><br>
            <span style='color: gray; font-size: 13px;'>75% - Descargando...</span>
        </div>
        <span style='font-size: 24px;'>⏳</span>
    </div>
""", unsafe_allow_html=True)
