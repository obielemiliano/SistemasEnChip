import tkinter
import customtkinter
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from threading import Thread
import time
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import requests
import math
import pygame

DEVICE_ID = "1d1ca332f5804d3c751bff86f1cd6d103ce32111"

# Configuración de apariencia
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Configuración de ventana
root = customtkinter.CTk()
root.title('Tocayos DJ (Spotify)')
root.geometry('600x500')

# Spotify Auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="3e54ffed78bb40558f63615ed19c9a50",
    client_secret="eaac6f475cf24d9d8ab13aeb66c94edc",
    redirect_uri="http://127.0.0.1:8080",
    scope="user-read-playback-state"
))

# Etiqueta para mostrar canción actual
spotify_label = tkinter.Label(root, text="Cargando...", bg='#222222', fg='white', font=("Arial", 14))
spotify_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

album_frame = customtkinter.CTkFrame(root, width=250, height=250, fg_color="transparent")
album_frame.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

album_cover_label = customtkinter.CTkLabel(album_frame, text="")
album_cover_label.pack()

# Variable para compartir datos entre threads
current_track_info = {"text": "Cargando..."}

def spotify_monitor():
    while True:
        try:
            current = sp.current_playback()
            if current and current['is_playing']:
                song = current['item']['name']
                artist = current['item']['artists'][0]['name']
                current_track_info["text"] = f"🎧 {song} - {artist}"
            else:
                current_track_info["text"] = "⏸ No se está reproduciendo música"
        except Exception as e:
            current_track_info["text"] = f"⚠️ Error: {str(e)}"
        
        time.sleep(3)

def update_spotify_label():
    spotify_label.config(text=current_track_info["text"])
    root.after(1000, update_spotify_label)  # Schedule the next update

def progress():
    a = pygame.mixer.Sound(f'{list_of_songs[n]}')
    song_len = a.get_length() * 3
    for i in range(0, math.ceil(song_len)):
        time.sleep(.4)
        progressbar.set(pygame.mixer.music.get_pos() / 1000000)

def threading():
    t1 = Thread(target=progress)
    t1.start()

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

def update_ui():
    try:
        current = sp.current_playback()
        if current and current['is_playing']:
            # Update progress bar
            progress = current['progress_ms'] / current['item']['duration_ms']
            progressbar.set(progress)
            
            # Update album cover if needed
            if 'album' in current['item'] and 'images' in current['item']['album']:
                album_cover_url = current['item']['album']['images'][0]['url']
                response = requests.get(album_cover_url, stream=True)
                image = Image.open(response.raw)
                image = image.resize((300, 300))
                photo = ImageTk.PhotoImage(image)
                
                if hasattr(root, 'album_cover_label'):
                    root.album_cover_label.configure(image=photo)
                    root.album_cover_label.image = photo
                else:
                    root.album_cover_label = tkinter.Label(root, image=photo)
                    root.album_cover_label.image = photo
                    root.album_cover_label.place(relx=.19, rely=.06)
    except Exception as e:
        print(f"Error updating UI: {e}")
    
    root.after(1000, update_ui)

# Elementos de la interfaz
progressbar = customtkinter.CTkProgressBar(master=root, progress_color='#32a85a', width=250)
progressbar.place(relx=.5, rely=.85, anchor=tkinter.CENTER)

# All Buttons
play_button = customtkinter.CTkButton(master=root, text='Play/Pause', command=play_music)
play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

skip_f = customtkinter.CTkButton(master=root, text='Next', command=skip_forward, width=2)
skip_f.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

skip_b = customtkinter.CTkButton(master=root, text='Previous', command=skip_back, width=2)
skip_b.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root, from_=0, to=1, command=set_volume, width=210)
slider.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)

# Iniciar hilo que monitorea Spotify
t_spotify = Thread(target=spotify_monitor, daemon=True)
t_spotify.start()

# Start the UI update loop
update_spotify_label()
update_ui()

# Ejecutar la interfaz
root.mainloop()