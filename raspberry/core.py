from gpiozero import LED
from time import sleep

led_ojo=LED(17)  #Si cambias esto puedes colocar aquí el GPIO pin que tu quieras 

print("Core loaded")

while True:
        #Led normal
        if led_ojo.on() == False:
                led_ojo.on() #Indica el funcionamiento de Hal

        sleep(2)
