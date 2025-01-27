import RPi.GPIO as GPIO
import time

class servos:

    '''Parameters 
        1. pins
    '''
    def __init__(self, pins):
        self.pins = pins





def main():
    print("Testing servos!!! ")
    SERVO_PIN = 13
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN,GPIO.OUT)

    p = GPIO.PWM(SERVO_PIN,75) #GPIO PIN 17 with 50hz frequency
    p.start(2.5)

    
    try:
        while True:
            #ChangeDutyCycle only changes the cycle
            p.ChangeDutyCycle(15)
            time.sleep(1)
            p.ChangeDutyCycle(7.5)
            time.sleep(1)
            p.ChangeDutyCycle(30)
            time.sleep(1)
            p.ChangeDutyCycle(12.5)
            time.sleep(1)
            p.ChangeDutyCycle(30)
            time.sleep(1)
            p.ChangeDutyCycle(7.5)
            time.sleep(1)
            p.ChangeDutyCycle(5)
            time.sleep(1)
    except KeyboardInterrupt:
        p.stop()
    
    finally:
        print("clean up")
        p.stop()
        GPIO.cleanup()


if __name__=='__main__':
    main()
