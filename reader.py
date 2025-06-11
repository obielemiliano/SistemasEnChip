# Programa para leer tarjetas RFID utilizando un lector conectado por USB

import serial
import time

# Configuración del puerto serial y la velocidad de baudios
SERIAL_PORT = 'COM13'  
BAUD_RATE = 9600

def leer_rfid():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Conectado al lector RFID en {SERIAL_PORT}...")
        
        while True:
            if ser.in_waiting > 0:
                raw_data = ser.readline().decode('utf-8').strip()
                if raw_data and len(raw_data) >= 8: 
                    print(f"Tarjeta detectada - ID: {raw_data}")
                    # Pequeña pausa para evitar múltiples lecturas de la misma tarjeta
                    time.sleep(1)  
                
            time.sleep(0.1)  # Pequeña pausa para no saturar la CPU
            
    except serial.SerialException as e:
        print(f"Error de conexión serial: {e}")
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Conexión serial cerrada")

if __name__ == "__main__":
    leer_rfid()
