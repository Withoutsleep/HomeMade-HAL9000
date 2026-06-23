from gpiozero import Button
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import requests

button = Button(27)
fs = 44100

IP_PC = "100.x.x.x"  #<-- AQUI PONES TU IP DEL PC DE TAILSCALE
SERVER_URL = f"http://{IP_PC}:5000/sendaudio"

print(sd.query_devices())

sd.default.device = (1, None)  # INPUT, OUTPUT

while True:
    button.wait_for_press()
    print("Escuchando...")

    frames = []

    def callback(indata, frames_count, time, status):
        frames.append(indata.copy())

    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        while button.is_pressed:
            pass

    print("rabación terminada")

    if len(frames) == 0:
        print("in audio")
        continue

    audio_data = np.concatenate(frames, axis=0)

    # guardar wav
    filename = "input.wav"
    write(filename, fs, audio_data)

    # enviar al servidor
    try:
        with open(filename, "rb") as f:
            response = requests.post(
                SERVER_URL,
                files={"pregunta": f}
            )
        print("Enviado:", response.status_code)

    except Exception as e:
        print(" Error enviando audio:", e)
