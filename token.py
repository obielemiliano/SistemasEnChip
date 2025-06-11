# Programa para la generación de un token de acceso para la API de Spotify utilizando las credenciales del cliente

from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '1804f7fd9cdc4d4fa06a0d976f3bf967'
CLIENT_SECRET = '2aed68bcd368477fa32a4f32451a3e3d'
REDIRECT_URI = 'http://127.0.0.1:8080'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope='user-read-playback-state,user-modify-playback-state')

token_info = sp_oauth.get_access_token(as_dict=True)
print("Access token:", token_info['access_token'])
print("Refresh token:", token_info['refresh_token'])