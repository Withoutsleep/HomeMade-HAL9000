from TTS.api import TTS
import pygame
import torch
from TTS.tts.configs.xtts_config import XttsConfig
import requests

IP_RASPBERRY="100.x.x.x"    #<--- AQUI ESCRIBES TU IP DE TAILSCALE DE TU RASPBERRY

print("Cargando modelo XTTS...")
tts = TTS(
    "tts_models/es/css10/vits",  #"tts_models/multilingual/multi-dataset/xtts_v2" <--- modelo secundario
    gpu=False
)

print("Modelo cargado")

pygame.mixer.init()


def generaraudio(respuesta):

    if respuesta!=".":

        try:
            respuesta = (respuesta or ".").strip()

            if not respuesta:
                print("Respuesta vacía")
                return

            tts.tts_to_file(
                text=respuesta,
                speaker_wav="hal_voice.wav",
                file_path="output.wav"
            )

            print("Audio generado")
            print(respuesta)

            #pygame.mixer.music.load("output.wav")       ----> Este también es debug, funciona junto a lo de abajo
            #pygame.mixer.music.play()                   ----> Este codigo es exclusivo para debug tecnico, ya que reproduce el audio en tu ordenador/computadora (así como dato, prefiero la palabra computadora xd)

            # Enviar archivo
            with open("output.wav", "rb") as f:
                url=f"http://{IP_RASPBERRY}:5000/subir"
                requests.post(
                    url, #Subir es el metodo usado exclusivamente para enviar archivo
                    files={"audiohal": f}
                )

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.music.unload()

            return True

        except Exception as e:
            print(f"Un error ocurrió: {e}")
            return False
    return True