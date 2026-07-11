import os
import ssl

# Parche para evitar errores de certificados SSL en Android
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

os.environ["SSL_CERT_FILE"] = ""

import flet as ft
from yt_dlp import YoutubeDL

def main(page: ft.Page):
    page.title = "DownloadAbby"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    # Campos de la interfaz
    url_input = ft.TextField(
        label="Enlace de YouTube", 
        placeholder="Pega el link aquí...", 
        width=400
    )
    status_text = ft.Text(value="", color=ft.colors.BLUE, weight=ft.FontWeight.BOLD)
    log_output = ft.Text(value="", color=ft.colors.BLACK54, size=12)

    # Opción para elegir formato
    format_options = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="mp3", label="Audio (MP3)"),
            ft.Radio(value="mp4", label="Video (MP4)")
        ], alignment=ft.MainAxisAlignment.CENTER)
    )
    format_options.value = "mp3"  # Opción por defecto

    def progress_hook(d):
        if d['status'] == 'downloading':
            status_text.value = f"Descargando... {d.get('_percent_str', '0%')}"
            page.update()
        elif d['status'] == 'finished':
            status_text.value = "Procesando archivo... ¡Casi listo!"
            page.update()

    def iniciar_descarga(e):
        url = url_input.value.strip()
        if not url:
            status_text.value = "Por favor, ingresa un enlace válido."
            status_text.color = ft.colors.RED
            page.update()
            return

        status_text.value = "Iniciando descarga..."
        status_text.color = ft.colors.BLUE
        log_output.value = ""
        page.update()

        # Ruta predeterminada en Android (Carpeta descargas pública)
        download_path = "/storage/emulated/0/Download"
        if not os.path.exists(download_path):
            download_path = "downloads"  # Carpeta local si corre en PC

        # Configuración de yt-dlp según formato elegido
        if format_options.value == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
            }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            status_text.value = "¡Descarga completada con éxito! Revisa tu carpeta de descargas."
            status_text.color = ft.colors.GREEN
        except Exception as error:
            status_text.value = "Ocurrió un error al descargar."
            status_text.color = ft.colors.RED
            log_output.value = str(error)
        
        page.update()

    # Botón de descarga
    download_button = ft.ElevatedButton(
        text="Descargar Ahora", 
        icon=ft.icons.DOWNLOAD, 
        on_click=iniciar_descarga,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

    # Construir la pantalla
    page.add(
        ft.Container(height=20),
        ft.Text("DownloadAbby", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
        ft.Text("Descarga música y videos directamente a tu almacenamiento", size=14, color=ft.colors.GREY_600),
        ft.Container(height=20),
        url_input,
        format_options,
        ft.Container(height=10),
        download_button,
        ft.Container(height=20),
        status_text,
        ft.Container(
            content=log_output,
            padding=10,
            bgcolor=ft.colors.GREY_100,
            border_radius=5,
            width=400,
            visible=True
        )
    )

ft.app(target=main)
