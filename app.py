import streamlit as st
import yt_dlp
import os

# Configuración visual de la aplicación
st.set_page_config(page_title="Descargador Abby", page_icon="🎵", layout="centered")

# Estilos personalizados (Color rosa de fondo y botones)
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF0F5;
    }
    div.stButton > button:first-child {
        background-color: #FF69B4;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #FF1493;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 Pegar Enlace")
st.markdown("Introduce la URL del video de YouTube o TikTok:")

# Entrada de la URL
url = st.text_input("URL del video:", label_visibility="collapsed", placeholder="https://youtu.be/...")

st.markdown("Elige el formato de descarga:")
tipo = st.radio("Formato:", ("Audio (MP3)", "Video (MP4)"), label_visibility="collapsed", horizontal=True)

if st.button("✨ ¡Descargar Ahora! ✨"):
    if not url:
        st.error("Por favor, introduce una URL válida.")
    else:
        with st.spinner("Conectando con el servidor... Por favor espera."):
            # Configuración blindada contra bloqueos de YouTube en servidores nube
            opciones = {
                'outtmpl': '%(title)s.%(ext)s',
                # Forzamos a simular un cliente móvil Android para evitar el "Video unavailable"
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
                }
            }
            
            if "Audio" in tipo:
                opciones.update({
                    'format': 'bestaudio/best',
                })
            else:
                opciones.update({
                    'format': 'best[ext=mp4]/best',
                })
                
            try:
                with yt_dlp.YoutubeDL(opciones) as ydl:
                    info = ydl.extract_info(url, download=True)
                    archivo = ydl.prepare_filename(info)
                    
                    nombre_base, _ = os.path.splitext(archivo)
                    ext_final = ".mp3" if "Audio" in tipo else ".mp4"
                    archivo_final = nombre_base + ext_final
                    
                    if os.path.exists(archivo) and archivo != archivo_final:
                        if os.path.exists(archivo_final):
                            os.remove(archivo_final)
                        os.rename(archivo, archivo_final)
                        
                if os.path.exists(archivo_final):
                    with open(archivo_final, "rb") as file:
                        st.success("¡Procesado con éxito!")
                        st.download_button(
                            label="📥 Guardar en mi dispositivo",
                            data=file,
                            file_name=os.path.basename(archivo_final),
                            mime="audio/mpeg" if "Audio" in tipo else "video/mp4"
                        )
                    os.remove(archivo_final)
                    
                    # Actualiza el estado del historial visual
                    st.markdown("### Download History")
                    st.info("Última descarga completada: Listo para recibir nuevos enlaces")
                else:
                    st.error("No se encontró el archivo convertido.")
            except Exception as e:
                st.error(f"Hubo un problema al descargar: {e}")
