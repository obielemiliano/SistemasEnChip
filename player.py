import serial
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configuración del puerto serial (ajusta según tu configuración)
SERIAL_PORT = 'COM13'  # En Windows. En Linux/Mac sería '/dev/ttyUSB0' o similar
BAUD_RATE = 9600

# Configuración de Spotify
DEVICE_ID = "YOUR_DEVICE_ID"
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

# Diccionario de tarjetas RFID y sus acciones de Spotify
# Reemplaza los valores con los IDs de tus tarjetas y las URIs correspondientes
RFID_ACTIONS = {
    "TARJETA_ID_1": {
        "type": "track",
        "uri": "spotify:track:2vSLxBSZoK0eha4AuhZlXV"
    },
    "TARJETA_ID_2": {
        "type": "album",
        "uri": "spotify:album:0JGOiO34nwfUdDrD612dOp"
    }
    # Añade más tarjetas según necesites
}

def leer_rfid_y_control_spotify():
    try:
        # Inicializar conexión serial
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Conectado al lector RFID en {SERIAL_PORT}...")
        
        # Configurar Spotify
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri="http://localhost:8080",
            scope="user-read-playback-state,user-modify-playback-state"
        ))
        
        # Transferir la reproducción al dispositivo deseado
        sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
        
        while True:
            if ser.in_waiting > 0:
                # Leer los datos del puerto serial
                raw_data = ser.readline().decode('utf-8').strip()
                
                if raw_data and len(raw_data) >= 8:  # Ajusta según la longitud mínima de tu ID
                    print(f"Tarjeta detectada - ID: {raw_data}")
                    
                    # Verificar si la tarjeta está en nuestro diccionario
                    if raw_data in RFID_ACTIONS:
                        action = RFID_ACTIONS[raw_data]
                        
                        if action["type"] == "track":
                            sp.start_playback(device_id=DEVICE_ID, uris=[action["uri"]])
                            print(f"Reproduciendo canción: {action['uri']}")
                        elif action["type"] == "album":
                            sp.start_playback(device_id=DEVICE_ID, context_uri=action["uri"])
                            print(f"Reproduciendo álbum: {action['uri']}")
                    else:
                        print("Tarjeta no registrada")
                    
                    # Pequeña pausa para evitar múltiples lecturas
                    time.sleep(2)
                
            time.sleep(0.1)  # Pequeña pausa para no saturar la CPU
            
    except serial.SerialException as e:
        print(f"Error de conexión serial: {e}")
    except Exception as e:
        print(f"Error con Spotify: {e}")
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Conexión serial cerrada")

if __name__ == "__main__":
    leer_rfid_y_control_spotify()