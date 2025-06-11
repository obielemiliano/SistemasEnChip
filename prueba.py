# Prueba de interfaz utilizando como base el código abierto de Spotify para el controlador de iFrame

from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Spotify Embed Controller</title>
    <script>
        let spotifyEmbedController = null;
        let iFrameAPI = undefined;
        let playerLoaded = false;
        let currentUri = "{{ uri }}";

        window.onload = function() {
            const script = document.createElement("script");
            script.src = "https://open.spotify.com/embed/iframe-api/v1";
            script.async = true;
            document.body.appendChild(script);

            window.onSpotifyIframeApiReady = (SpotifyIframeApi) => {
                iFrameAPI = SpotifyIframeApi;
                createController();
            };
        };

        function createController() {
            if (!iFrameAPI) return;
            iFrameAPI.createController(
                document.getElementById("embed"),
                {
                    width: "100%",
                    height: "352",
                    uri: currentUri,
                },
                (controller) => {
                    spotifyEmbedController = controller;
                    controller.addListener("ready", () => {
                        playerLoaded = true;
                        document.getElementById("loading").style.display = "none";
                    });
                    controller.addListener("playback_update", (e) => {
                        const { position, duration, isBuffering, isPaused, playingURI } = e.data;
                        console.log(
                            `Playback State updates:
                            position - ${position},
                            duration - ${duration},
                            isBuffering - ${isBuffering},
                            isPaused - ${isPaused},
                            playingURI - ${playingURI},
                            duration - ${duration}`
                        );
                    });
                    controller.addListener("playback_started", (e) => {
                        const { playingURI } = e.data;
                        console.log(`The playback has started for: ${playingURI}`);
                    });
                }
            );
        }

        function onPlayClick() {
            if (spotifyEmbedController) {
                spotifyEmbedController.play();
            }
        }

        function onPauseClick() {
            if (spotifyEmbedController) {
                spotifyEmbedController.pause();
            }
        }

        function onUriChange(event) {
            currentUri = event.target.value;
            if (spotifyEmbedController) {
                spotifyEmbedController.loadUri(currentUri);
            } else {
                // If controller not ready, recreate it
                createController();
            }
        }
    </script>
</head>
<body>
    <div id="embed"></div>
    <p id="loading">Loading...</p>
    <div>
        <button aria-label="Play" onclick="onPlayClick()">Play</button>
        <button aria-label="Pause" onclick="onPauseClick()">Pause</button>
    </div>
    <div>
        <p>Change URI:</p>
        <input
            type="text"
            value="{{ uri }}"
            onchange="onUriChange(event)"
            placeholder="Enter Spotify URI"
            id="uriInput"
        />
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    uri = request.args.get("uri", "spotify:playlist:37i9dQZF1DZ06evO3eIivx")
    return render_template_string(HTML, uri=uri)

if __name__ == "__main__":
    app.run(debug=True)
