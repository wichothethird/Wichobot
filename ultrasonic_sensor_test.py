import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TRIG = 18
ECHO = 32

GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG,0)


GPIO.setup(ECHO,GPIO.IN)
time.sleep(0.1)

GPIO.output(TRIG,True)
time.sleep(0.00001)
GPIO.output(TRIG,False)

print("Iniciando Programa Cabrones!!!!")
while True:
    start=time.time()
    stop=time.time()
    while GPIO.input(ECHO)==0:
        start = time.time()

    while GPIO.input(ECHO)==1:
        stop = time.time()
    distance = (stop - start) * 170

    print(distance)
    time.sleep(1) 



