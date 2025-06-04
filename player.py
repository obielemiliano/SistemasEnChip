import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import serial

# Configuracion de Spotify
DEVICE_ID = "98bb0735e28656bac098d927d410c3138a4b5bca"

# Token de acceso directo
ACCESS_TOKEN = "BQBMPgHTbnOvIZFIrCiBY0dgGH9clJqK7by3pi4lPOI-g8bIdUYuwEKSOf0tjUCeQkLg-hch7MEFRlL361-Ks8KmGnok32Tt7jeqy-QbiD_qBa75qUDh69vtS4uDj82vrFDJOmONZAL9yabCfx5FuJT-MLskuK7_cge-RXOfsXjkzWGZr1XHTmwXzZ0j2PWjno6f7ot1yoJapRIteib5RfyN453_V7QF"

# Crear cliente de Spotify
sp = spotipy.Spotify(auth=ACCESS_TOKEN)

# Conectar al puerto serial
try:
    lector = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    print("Puerto serial conectado exitosamente")
except serial.SerialException as e:
    print(f"Error al conectar puerto serial: {e}")
    exit(1)

print("Esperando tarjetas...")

ultimo_uid = None  # Para evitar repeticiones

while True:
    try:
        if lector.in_waiting > 0:
            raw_uid = lector.readline().decode('utf-8', errors='ignore').strip()

            # Limpiar UID
            uid_clean = raw_uid.upper().replace('\r', '').replace('\n', '').replace(' ', '')
            uid_clean = uid_clean.replace('\x02', '').replace('\x03', '')  # STX/ETX
            uid_clean = ''.join(char for char in uid_clean if ord(char) > 31)

            # Validar UID: ignorar si es vacio o muy corto
            if not uid_clean or len(uid_clean) < 6:
                continue

            # Evitar repetir UID si es el mismo
            if uid_clean == ultimo_uid:
                continue

            ultimo_uid = uid_clean  # Guardar nuevo UID
            print(f"UID nuevo leido: {uid_clean}")

            # Transferir reproduccion
            try:
                sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
            except Exception as e:
                print(f"Error al transferir reproduccion: {e}")
                continue

            # Reproducir musica segun UID
            if uid_clean == '4F0056AF0ABC':
                try:
                    sp.start_playback(
                        device_id=DEVICE_ID,
                        uris=['spotify:track:1lRYofIUSURrWsUVafsmzH']
                    )
                    print("Reproduciendo cancion")
                except Exception as e:
                    print(f"Error al reproducir cancion: {e}")

            elif uid_clean == '52000047CFDA':
                try:
                    sp.start_playback(
                        device_id=DEVICE_ID,
                        uris=['spotify:track:5TFD2bmFKGhoCRbX61nXY5']
                    )
                    print("Reproduciendo cancion")
                except Exception as e:
                    print(f"Error al reproducir cancion: {e}")
                    
            elif uid_clean == '500094696BC6':
                try:
                    sp.start_playback(
                        device_id=DEVICE_ID,
                        uris=['spotify:track:5TRPicyLGbAF2LGBFbHGvO']
                    )
                    print("Reproduciendo cancion")
                except Exception as e:
                    print(f"Error al reproducir cancion: {e}")
            else:
                print(f"UID no reconocido: '{uid_clean}'")

        else:
            # Si no hay datos, no hacer nada
            sleep(0.1)

    except KeyboardInterrupt:
        print("\nDeteniendo programa...")
        break
    except Exception as e:
        print(f"Error general: {e}")
        sleep(1)

lector.close()
print("Puerto serial cerrado")