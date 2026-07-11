import flet as ft
import yt_dlp
import os


def get_download_folder() -> str:
    """
    Devuelve una carpeta donde la app SÍ tiene permiso de escribir
    sin pedir permisos especiales de almacenamiento.

    En Android 10+ (scoped storage), escribir directo en
    /storage/emulated/0/Download requiere permisos que esta app no
    solicita, así que usamos la carpeta externa propia de la app,
    que siempre es escribible por la app dueña sin permisos extra:

        /storage/emulated/0/Android/data/<package>/files/Download

    Es visible para el usuario con un explorador de archivos
    (o conectando el celular a la PC), aunque no aparece dentro de
    la carpeta "Download" pública del sistema.
    """
    package_name = "com.flet.downloadabby"
    candidatos = [
        f"/storage/emulated/0/Android/data/{package_name}/files/Download",
        os.path.join(os.path.expanduser("~"), "Download"),
        os.path.join(os.getcwd(), "Download"),
    ]

    for carpeta in candidatos:
        try:
            os.makedirs(carpeta, exist_ok=True)
            # Verificamos que de verdad se pueda escribir aquí.
            prueba = os.path.join(carpeta, ".write_test")
            with open(prueba, "w") as f:
                f.write("ok")
            os.remove(prueba)
            return carpeta
        except OSError:
            continue

    # Último recurso: carpeta interna de la app (siempre funciona).
    return os.getcwd()


def main(page: ft.Page):
    page.title = "Descargador Pro"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    url_input = ft.TextField(label="Pega la URL de YouTube aquí", width=400, border_color=ft.Colors.BLUE_ACCENT)

    opcion = ft.RadioGroup(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
        ft.Radio(value="1", label="Audio (M4A)"),
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

        carpeta = get_download_folder()

        opciones = {
            'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
            'http_headers': {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'},
        }

        # IMPORTANTE: no usamos postprocesadores de FFmpeg (FFmpegExtractAudio,
        # merge_output_format) porque el APK no incluye el binario de ffmpeg
        # y Android no lo trae instalado. En vez de convertir/fusionar,
        # pedimos formatos que ya vienen listos para usar tal cual.
        if opcion.value == "1":
            # Mejor pista de audio ya empaquetada (normalmente m4a), sin
            # necesitar conversión a mp3.
            opciones.update({
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
            })
        else:
            # Un solo archivo mp4 que ya trae video+audio combinados,
            # así no hace falta fusionar pistas con ffmpeg.
            opciones.update({
                'format': 'best[ext=mp4]/best',
            })

        try:
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url_input.value])
            status.value = f"¡Completado! Guardado en: {carpeta}"
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
