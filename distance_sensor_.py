import RPi.GPIO as GPIO
import time


class DistanceSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        TRIG = 18
        ECHO = 32
        self.minDistance = 12
        
        #setting default Ultrasonic sensor options
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)


    def set_min_distance(distance):
        print("Setting Distance to " + distance)
        self.minDistance = distance

    def get_distance():
        print("Current distance is ")
        GPIO.output(TRIG,0)
        
        time.sleep(0.1)
        GPIO.output(TRIG,True)
        time.sleep(0.00001)
        GPIO.output(TRIG,False)

        start=time.time()
        stop=time.time()

        while GPIO.input(ECHO)==0:
            start = time.time()

        while GPIO.input(ECHO)==1:
            stop = time.time()
        distance = (stop - start) * 170

        print(distance)
        return distance

    def has_passed_min_distance(currentDistance):
        return currentDistance <= self.minDistance



def main():
    distSensor = DistanceSensor()
    while True:
        distSensor.get_distance()
        time.sleep(1)


if __name__ =='__main__':
    main()





    
