import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import requests
from flask import Flask, request
import subprocess
import os
import pcmain

PREGUNTAS_FOLDER = "preguntas" #<---- AQUI TIENES QUE PONER LA CARPETA DONDE QUIERES PONER LOS AUDIOS QUE RECIBES DESDE LA RASPBERRY PI

app = Flask(__name__)

@app.route("/sendaudio", methods=["POST"])
def sendaudio():
    if "pregunta" not in request.files:
        return "No file received", 400

    f = request.files["pregunta"]

    path = os.path.join(PREGUNTAS_FOLDER, f.filename)

    f.save(path)
    print(path)

    print("Enviado a hal")

    model = WhisperModel("base", device="cpu", compute_type="int8")

    segments, info = model.transcribe(path, language="es")

    text = ""

    for segment in segments:
        text += segment.text

    print(text)

    pcmain.mensaje = text
    pcmain.funcion()

    return "OK", 200
    

# INICIAR SERVIDOR
app.run(host="0.0.0.0", port=5000)