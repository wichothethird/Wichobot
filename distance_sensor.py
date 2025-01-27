import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 24
ECHO = 12

class DistanceSensor:
    def __init__(self):
        
        self.minDistance = 12
        
        #setting default Ultrasonic sensor options
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)


    def set_min_distance(self, distance):
        print("Setting Distance 2to " + str(distance))
        self.minDistance = distance

    def get_distance(self):
        #print("Current distance is "+ str(TRIG) + str(ECHO))
        GPIO.output(TRIG,0)
        
        time.sleep(0.1)
        GPIO.output(TRIG,True)
        time.sleep(0.00001)
        GPIO.output(TRIG,False)

        start=time.time()
        stop=time.time()
        #print("Wicho time" + str(start) + str(stop))

        while GPIO.input(ECHO)==0:
            start = time.time()

        while GPIO.input(ECHO)==1:
            stop = time.time()
        distance = (stop - start) * 170

        print(distance)
        return distance

    def has_passed_min_distance(self, currentDistance):
        return currentDistance <= self.minDistance

    

def main():
    print("Wicho this is an update and testing")
    distSensor = DistanceSensor()
    try:
        while True:
            print("Wicho ")
            distSensor.get_distance()
            #time.sleep(1)
    except KeyboardInterrupt:
        print("GPIO Pins for Ultrasonic sensors was interrupted by KeyboardInterrupt")
    finally:
        GPIO.cleanup()


if __name__ =='__main__':
    main()





    
