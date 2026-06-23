#!/usr/bin/env python3

from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# TEXTO (solo para pruebas pruebosas)
@app.route("/text", methods=["POST"])
def text():

    data = request.json

    print("TEXTO RECIBIDO:", data["msg"])

    return "Connection established, Hal return"


# ARCHIVOS
@app.route("/subir", methods=["POST"])
def subir():

    # Verifica si llegó el archivo
    if "audiohal" not in request.files:
        return "No file received", 400

    f = request.files["audiohal"]

    path = os.path.join(UPLOAD_FOLDER, f.filename)

    f.save(path)

    subprocess.Popen([
        "aplay",
        path
    ])
    return "Audio received and playing"

# INICIAR SERVIDOR
app.run(host="0.0.0.0", port=5000)
