# Proyecto: Sistemas en Chip

Este repositorio contiene el desarrollo de un proyecto académico para la materia de **Diseño de Sistemas en Chip**. El proyecto fue realizado en equipo por:

* **Emiliano Camacho Ponce [GitHubEmiliano](https://github.com/Emiliano1410)** 
* **Alfredo Alejandro Soto Herrera [GitHubAlex](https://github.com/AlejandroSH1)**
* **Obiel Emiliano Rangel Moreno [GitHubObiel](https://github.com/obielemiliano)**

## Descripción del Proyecto

El objetivo del proyecto es desarrollar un sistema embebido utilizando Python, que simula la funcionalidad de una Rocola. Se implementan diversas funcionalidades, entre ellas la que más se destaca es la reproducción de música a través de tarjetas RFID, las cuales permiten la interacción con el usuario. Asimismo, este proyecto cuenta con una interfaz gráfica donde los usuarios también pueden interactuar y una base de datos en la cual se registran las canciones que se han escuchado.

## Estructura del Repositorio

A continuación, se describen los archivos principales del repositorio y su funcionalidad:

* **`interface.py`**: La interfaz del sistema. En esta, el usuario puede interactuar y ver algunos datos como nombre del artista o nombre de la canción.

* **`player.py`**: Es el archivo eje del repositorio. Implementa las funcionalidades relacionadas con la reproducción de medios. Permite la gestión y reproducción de  de audioa través de APIs con la cuenta de Spotify enlazada.

* **`prueba.py`**: Archivo basado en el código abierto de Spotify para realizar peticiones y configurar la interfaz. No pertenece al proyecto, unicamente es una prueba para el desarrollo de la interfaz

* **`reader.py`**: Programa de prueba utilizado para leer el ID de cada una de las tarjetas a través del sensor NFC.

* **`token.py`**: Gestiona la creación y validación de un token de Spotify. Es fundamental para la autenticación y autorización de usuarios o procesos.

## Requisitos

* Python 3.3
* Bibliotecas adicionales (Tkinter, FastAPI, Spotipy, SpotifyOAuth, Time y Serial)
* Una Raspberry Pi
* Sensor NFC (Nosotros usamos un Sensor Sparkfun NFC)
* Tarjetas RFID 
* Cuenta Premium en Spotify

## Instrucciones de Uso

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/obielemiliano/SistemasEnChip.git
   ```



2. Navegar al directorio del proyecto:

   ```bash
   cd SistemasEnChip
   ```



3. Ejecutar el archivo principal:

   ```bash
   python player.py
   ```



## Contribuciones

Este proyecto fue desarrollado como parte de la evaluación de la materia de Diseño de Sistemas en Chip. Las contribuciones externas no son aceptadas en este momento.

## Licencia

Este proyecto no cuenta con una licencia específica. Todos los derechos están reservados por los autores.


