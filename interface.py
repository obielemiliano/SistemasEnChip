# Código para la interfaz gráfica y almacenamiento de historial de reproducción de Spotify

import colorsys
from colorthief import ColorThief
import io
import tkinter
import customtkinter
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from threading import Thread
import time
from PIL import Image, ImageTk
import requests
import pygame
import datetime

# Configuración inicial
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Crear ventana principal
root = customtkinter.CTk()
root.title('Tocayos DJ (Spotify)')
root.geometry('750x650')

# Configuración de Spotify
DEVICE_ID = "1d1ca332f5804d3c751bff86f1cd6d103ce32111"  

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="3e54ffed78bb40558f63615ed19c9a50",
    client_secret="eaac6f475cf24d9d8ab13aeb66c94edc",
    redirect_uri="http://127.0.0.1:8080",
    scope="user-read-playback-state,user-modify-playback-state"
))

# Variable para compartir datos entre threads
current_track_info = {
    "text": "Cargando...",
    "image_url": None,
    "colors": None
}

def get_dominant_color(image_url):
    """Extrae el color predominante de la imagen del álbum"""
    try:
        response = requests.get(image_url)
        img_data = io.BytesIO(response.content)
        color_thief = ColorThief(img_data)
        dominant_color = color_thief.get_color(quality=1)
        return dominant_color
    except:
        return (40, 40, 40)  # Color gris oscuro por defecto

def apply_dynamic_theme(dominant_color):
    """Aplica un tema basado en el color predominante"""
    try:
        # Convertir RGB a HSL para ajustes
        r, g, b = [x/255.0 for x in dominant_color]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        
        # Ajustar luminosidad para el fondo
        bg_l = max(0.1, min(0.3, l * 0.7))
        bg_r, bg_g, bg_b = colorsys.hls_to_rgb(h, bg_l, s)
        bg_color = (int(bg_r*255), int(bg_g*255), int(bg_b*255))
        
        # Convertir a formato hexadecimal
        bg_hex = '#%02x%02x%02x' % bg_color
        
        # Aplicar a la interfaz
        root.configure(fg_color=bg_hex)
        album_frame.configure(fg_color=bg_hex)
        song_info.configure(fg_color=bg_hex)
        controls_frame.configure(fg_color=bg_hex)
        volume_frame.configure(fg_color=bg_hex)
        
        # Color de texto basado en luminosidad
        text_color = 'white' if l < 0.5 else 'black'
        song_info.configure(text_color=text_color)
        
    except Exception as e:
        print(f"Error aplicando tema dinámico: {e}")
        # Tema por defecto si hay error
        default_theme()

def default_theme():
    """Establece el tema por defecto"""
    root.configure(fg_color='#222222')
    album_frame.configure(fg_color='#222222')
    song_info.configure(fg_color='#222222', text_color='white')
    controls_frame.configure(fg_color='#222222')
    volume_frame.configure(fg_color='#222222')

# Contenedor principal para la imagen del álbum
album_frame = customtkinter.CTkFrame(root, width=400, height=400, fg_color='#222222')
album_frame.pack(pady=20)

# Label para la portada del álbum
album_cover = customtkinter.CTkLabel(album_frame, text="", width=350, height=350, fg_color='#222222')
album_cover.pack()

# Label para la información de la canción
song_info = customtkinter.CTkLabel(
    root, 
    text="Cargando...", 
    font=("Arial", 14, "bold"),
    wraplength=400,
    justify="center",
    fg_color='#222222',
    text_color='white'
)
song_info.pack(pady=10)

# Barra de progreso
progressbar = customtkinter.CTkProgressBar(
    root, 
    progress_color='#1DB954', 
    width=400,
    height=4,
    fg_color='#333333'
)
progressbar.pack(pady=10)

# Controles de reproducción
controls_frame = customtkinter.CTkFrame(root, fg_color='#222222')
controls_frame.pack(pady=15)

# Funciones de control con device_id incluido
def play_music():
    try:
        current = sp.current_playback()
        if current and current['is_playing']:
            sp.pause_playback(device_id=DEVICE_ID)
        else:
            sp.start_playback(device_id=DEVICE_ID)
    except Exception as e:
        print(f"Error en play/pause: {e}")

def skip_forward():
    try:
        sp.next_track(device_id=DEVICE_ID)
    except Exception as e:
        print(f"Error al saltar canción: {e}")

def skip_back():
    try:
        sp.previous_track(device_id=DEVICE_ID)
    except Exception as e:
        print(f"Error al retroceder canción: {e}")

def set_volume(value):
    try:
        sp.volume(int(float(value) * 100), device_id=DEVICE_ID)
    except Exception as e:
        print(f"Error al ajustar volumen: {e}")

# Botones
skip_back_btn = customtkinter.CTkButton(
    controls_frame, 
    text="⏮", 
    command=skip_back,
    width=50,
    fg_color='#333333',
    hover_color='#555555'
)
skip_back_btn.pack(side="left", padx=10)

play_btn = customtkinter.CTkButton(
    controls_frame, 
    text="⏯", 
    command=play_music,
    width=50,
    fg_color='#333333',
    hover_color='#555555'
)
play_btn.pack(side="left", padx=10)

skip_forward_btn = customtkinter.CTkButton(
    controls_frame, 
    text="⏭", 
    command=skip_forward,
    width=50,
    fg_color='#333333',
    hover_color='#555555'
)
skip_forward_btn.pack(side="left", padx=10)

# Control de volumen
volume_frame = customtkinter.CTkFrame(root, fg_color='#222222')
volume_frame.pack(pady=10)

volume_label = customtkinter.CTkLabel(volume_frame, text="🔈", fg_color='#222222')
volume_label.pack(side="left")

volume_slider = customtkinter.CTkSlider(
    volume_frame,
    from_=0,
    to=1,
    command=set_volume,
    width=200,
    fg_color='#333333',
    progress_color='#1DB954'
)
volume_slider.set(0.7)
volume_slider.pack(side="left", padx=10)

def format_duration_ms(milliseconds):
    """Convierte milisegundos a formato minutos:segundos"""
    seconds = int(milliseconds / 1000)
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

def save_playback_history(song, artist, album, duration_ms):
    """Guarda el historial de reproducción en un archivo de texto"""
    try:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        duration_formatted = format_duration_ms(duration_ms)
        
        with open("historial.txt", "a", encoding="utf-8") as f:
            f.write(f"Canción: {song}\n")
            f.write(f"Artista: {artist}\n")
            f.write(f"Álbum: {album}\n")
            f.write(f"Duración: {duration_formatted}\n")
            f.write(f"Fecha y Hora: {timestamp}\n")
            f.write("-" * 40 + "\n")  # Separador entre entradas
            
    except Exception as e:
        print(f"Error guardando historial: {e}")

# Funciones de Spotify
def spotify_monitor():
    last_track_id = None  # Para rastrear cambios de canción
    
    while True:
        try:
            current = sp.current_playback()
            if current and current['item'] is not None:
                song = current['item']['name']
                artist = current['item']['artists'][0]['name']
                current_track_id = current['item']['id']
                album = current['item']['album']['name'] if 'album' in current['item'] else "Desconocido"
                duration_ms = current['item']['duration_ms'] if 'duration_ms' in current['item'] else 0
                
                # Verificar si es una canción nueva
                if current_track_id != last_track_id:
                    current_track_info["text"] = f"{song}\n{artist}\nÁlbum: {album}"
                    save_playback_history(song, artist, album, duration_ms)  # Guardar en historial
                    last_track_id = current_track_id

                if 'album' in current['item'] and 'images' in current['item']['album']:
                    image_url = current['item']['album']['images'][0]['url']
                    if current_track_info.get("image_url") != image_url:
                        current_track_info["image_url"] = image_url
                        current_track_info["colors"] = get_dominant_color(image_url)
                else:
                    current_track_info["image_url"] = None
                    current_track_info["colors"] = None
            else:
                current_track_info["text"] = "No se está reproduciendo música"
                current_track_info["image_url"] = None
                current_track_info["colors"] = None
                last_track_id = None  # Resetear cuando no hay reproducción

        except Exception as e:
            current_track_info["text"] = f"Error: {str(e)}"
            current_track_info["image_url"] = None
            current_track_info["colors"] = None
        
        time.sleep(3)

def update_ui():
    try:
        song_info.configure(text=current_track_info["text"])
        
        if current_track_info["image_url"]:
            response = requests.get(current_track_info["image_url"], stream=True)
            image = Image.open(response.raw)
            image = image.resize((350, 350), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            album_cover.configure(image=photo)
            album_cover.image = photo
            
            if current_track_info["colors"]:
                apply_dynamic_theme(current_track_info["colors"])
        else:
            album_cover.configure(image=None)
            album_cover.image = None
            default_theme()
            
        current = sp.current_playback()
        if current and current['is_playing']:
            progress = current['progress_ms'] / current['item']['duration_ms']
            progressbar.set(progress)
        else:
            progressbar.set(0)
            
    except Exception as e:
        print(f"Error actualizando UI: {e}")
        default_theme()
    
    root.after(1000, update_ui)

# Instalar colorthief si no está instalado
try:
    from colorthief import ColorThief
except:
    import os
    os.system('pip install colorthief')
    from colorthief import ColorThief

# Iniciar hilos
Thread(target=spotify_monitor, daemon=True).start()
update_ui()

# Establecer tema inicial
default_theme()

# Ejecutar la aplicación
root.mainloop()
