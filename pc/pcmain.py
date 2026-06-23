import requests
import voice
import os
import requests
from flask import Flask, request

ruta_long_memory = "memory/long_term_memory.txt"
ruta_short_memory = "memory/short_term_memory.txt"
ruta_contexto_hal = "memory/context.txt"

# Input usuario
mensaje="" # De momento es nada

app = Flask(__name__) #Por lo que he entendido, inicializa flask

def funcion():
    # Lectura memoria largo plazo
    with open(ruta_long_memory, "r", encoding="utf-8") as f:
        long_term = f.read()

    # Lectura memoria corto plazo
    with open(ruta_short_memory, "r", encoding="utf-8") as f:
        short_term = f.read()

    # Lectura contexto HAL
    with open(ruta_contexto_hal, "r", encoding="utf-8") as f:
        contexto_hal_text = f.read()
        print(contexto_hal_text)

    #screenshoot=captura.enviar_captura() --> actualmente en desarollo

    # Construir contexto usuario  (Las memorias no estan construidas, HAL olvida las conversaciones actualmente)
    contexto = f"""
    MEMORIA LARGO PLAZO:
    {long_term}

    MEMORIA CORTO PLAZO:
    {short_term}

    USUARIO:
    {mensaje}
    """

    # Request a LM Studio
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "model": "local-model",
            "messages": [
                {
                    "role": "system",
                    "content": contexto_hal_text
                },
                {
                    "role": "user",
                    "content": contexto
                }
            ],
            "temperature": 0.7
        }
    )

    # DEBUG
    print(response.json())

    # Obtener respuesta
    respuesta = response.json()["choices"][0]["message"]["content"]

    print(respuesta)

    estado=voice.generaraudio(respuesta)

    if estado==True:
        print("Ciclo completado")
