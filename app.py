import streamlit as str
import yt_dlp
import os

st.title("🚀 DownloadAbby - Descargador de Videos")
st.write("Pega el enlace de tu video favorito abajo para descargarlo.")

# Cuadro para pegar el enlace
url = st.text_input("Enlace del video:")

if url:
    st.success(f"¡Enlace recibido! Listo para procesar: {url}")
    # Aquí irá la lógica de descarga que limpiaremos juntos
