from gpiozero import PWMOutputDevice
from time import sleep


class Movements:

    speed = 0.8


    def __init__(self):
        pin1 = PWMOutputDevice(26)
        pin2 = PWMOutputDevice(17)
        pin3 = PWMOutputDevice(22)
        pin4 = PWMOutputDevice(27)
        self.GPIO26 = pin1
        self.GPIO17 = pin2
        self.GPIO22 = pin3
        self.GPIO27 = pin4

    def move_forward(self):
        #for Forward movemnet we need pin 4 and 22
        self.GPIO26.value = 0.0
        self.GPIO22.value = 0.0
        self.GPIO27.value = Movements.speed 
        self.GPIO17.value = Movements.speed  
        


    def move_backward(self):
        #you will use pins 17 and 17

        print("I entered the backward function")
        self.GPIO17.value = 0.0
        self.GPIO27.value = 0.0
        self.GPIO26.value = Movements.speed
        self.GPIO22.value = Movements.speed
        
        print("everything was executed!!!")
        
    #def speed_up():
        
    #def slow_down():

    def stop(self):
        self.GPIO26.value = 0.0
        self.GPIO17.value = 0.0
        self.GPIO27.value = 0.0
        self.GPIO22.value = 0.0



    def turn_right(self):
        self.GPIO26.value = 0.0
        self.GPIO27.value = 0.0
        self.GPIO17.value = Movements.speed
        self.GPIO22.value = Movements.speed

    
    def turn_left(self):
        self.GPIO17.value = 0.0
        self.GPIO22.value = 0.0
        self.GPIO26.value = Movements.speed
        self.GPIO27.value = Movements.speed

def main():
    print("This is the start of the Motor practice!!!")
    pin1 = PWMOutputDevice(26)
    pin2 = PWMOutputDevice(17)
    pin3 = PWMOutputDevice(22)
    pin4 = PWMOutputDevice(27)

    m = Movements()

    m.move_forward()
    sleep(6)
    m.move_backward()
    sleep(6)
    m.turn_right()
    sleep(6)
    m.turn_left()
    sleep(6)




if __name__=="__main__":
    main()
