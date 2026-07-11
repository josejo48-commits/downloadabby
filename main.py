import flet as ft
import yt_dlp
import os

def main(page: ft.Page):
    page.title = "Descargador Pro"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    url_input = ft.TextField(label="Pega la URL de YouTube aquí", width=400, border_color=ft.Colors.BLUE_ACCENT)
    
    opcion = ft.RadioGroup(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
        ft.Radio(value="1", label="Audio (MP3)"),
        ft.Radio(value="2", label="Video (MP4)")
    ]))
    opcion.value = "1"
    
    status = ft.Text("", size=14, color=ft.Colors.GREEN)
    progress = ft.ProgressBar(width=400, visible=False)
    
    def descargar(e):
        if not url_input.value:
            status.value = "Introduce un enlace válido."
            status.color = ft.Colors.RED
            page.update()
            return
            
        status.value = "Descargando multimedia..."
        status.color = ft.Colors.BLUE_200
        progress.visible = True
        page.update()
        
        carpeta = "/storage/emulated/0/Download"
        if not os.path.exists(carpeta):
            carpeta = os.path.join(os.path.expanduser("~"), "Downloads")

        opciones = {
            'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
            'http_headers': {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'}
        }
        
        if opcion.value == "1":
            opciones.update({
                'format': 'bestaudio/best', 
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio', 
                    'preferredcodec': 'mp3', 
                    'preferredquality': '192'
                }]
            })
        else:
            opciones.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
                'merge_output_format': 'mp4'
            })
            
        try:
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url_input.value])
            status.value = "¡Completado! Revisa las descargas de tu celular."
            status.color = ft.Colors.GREEN
        except Exception as ex:
            status.value = f"Error: {ex}"
            status.color = ft.Colors.RED
        finally:
            progress.visible = False
            page.update()

    btn = ft.ElevatedButton("Descargar Ahora", icon=ft.Icons.DOWNLOAD, on_click=descargar, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_ACCENT, color=ft.Colors.WHITE))
    
    page.add(ft.Column(alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, controls=[
        ft.Text("Mi Descargador Personal", size=26, weight="bold", color=ft.Colors.BLUE_ACCENT), 
        url_input, 
        opcion, 
        btn, 
        progress,
        status
    ]))

if __name__ == "__main__":
    ft.app(target=main)
