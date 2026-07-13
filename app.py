import streamlit as st
import yt_dlp
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="DownloadAbby",
    page_icon="logo_abby.png",
    layout="centered"
)

# 2. ESTILOS CSS PERSONALIZADOS
st.markdown("""
    <style>
    .stApp {
        background-color: #FCE4EC;
    }
    .titulo-principal {
        text-align: center; 
        color: #EC407A; 
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 0px;
    }
    .subtitulo {
        text-align: center; 
        color: #555555; 
        font-size: 18px;
        margin-top: 0px;
        margin-bottom: 20px;
    }
    .tarjeta-blanca {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    /* Estilo para el botón de Streamlit */
    .stButton>button {
        background-color: #EC407A !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 100%;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CONTENIDO VISUAL Y LÓGICA
col1, col2, col3 = st.columns([1, 1.2, 1])
with col2:
    try:
        st.image("logo_abby.png", width=160)
    except:
        pass

st.markdown("<h1 class='titulo-principal'>DOWNLOAD ABBY</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo'>Tu descargador tierno y rápido</p>", unsafe_allow_html=True)

# Contenedor del formulario
st.markdown("<div class='tarjeta-blanca'>", unsafe_allow_html=True)
st.subheader("🎵 Pegar Enlace")
url = st.text_input("Introduce la URL del video de YouTube o TikTok:", placeholder="https://...")
formato = st.radio("Elige el formato de descarga:", ["Audio (MP3)", "Video (MP4)"], horizontal=True)

# BOTÓN REAL DE DESCARGA
if st.button("✨ ¡Descargar Ahora! ✨"):
    if url:
        with st.spinner("Procesando tu enlace con Abby Chef... 👩‍🍳⏳"):
            try:
                # Configuración de yt-dlp según el formato elegido
                if formato == "Audio (MP3)":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 'downloads/%(title)s.%(ext)s',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }
                else:
                    ydl_opts = {
                        'format': 'best[ext=mp4]/best',
                        'outtmpl': 'downloads/%(title)s.%(ext)s',
                    }

                # Descargar el archivo al servidor temporal
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # Si era MP3, la extensión real cambia después del postprocesador
                    if formato == "Audio (MP3)":
                        filename = os.path.splitext(filename)[0] + ".mp3"

                # Ofrecer el botón de guardado local al usuario
                with open(filename, "rb") as f:
                    st.success("¡Tu descarga está lista!")
                    st.download_button(
                        label="💾 Guardar archivo en tu dispositivo",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="audio/mpeg" if formato == "Audio (MP3)" else "video/mp4"
                    )
            except Exception as e:
                st.error(f"Hubo un problema al descargar: {e}")
    else:
        st.warning("Por favor, introduce una URL válida primero.")

st.markdown("</div>", unsafe_allow_html=True)

# Historial estático visual (Lo mantenemos abajo para rellenar la apariencia)
st.markdown("<h3 style='color: black;'>Download History</h3>", unsafe_allow_html=True)
st.markdown("""
    <div class='tarjeta-blanca' style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: black;'>Última descarga completada</strong><br>
            <span style='color: gray; font-size: 13px;'>Listo para recibir nuevos enlaces</span>
        </div>
        <span style='font-size: 24px;'>✅</span>
    </div>
""", unsafe_allow_html=True)
