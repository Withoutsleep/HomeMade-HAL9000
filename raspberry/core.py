from gpiozero import LED

led_ojo=LED(17)  #Si cambias esto puedes colocar aquí el GPIO pin que tu quieras 

while True:
	led_ojo.on() #Indica el funcionamiento de Hal



