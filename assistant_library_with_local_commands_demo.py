#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import subprocess
from distance_sensor import DistanceSensor
import sys
from motor_practice import Movements
from google.assistant.library.event import EventType

from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant
from aiy.board import Board, Led
from aiy.voice import tts
from time import sleep
from gpiozero import PWMOutputDevice
##import RPi.GPIO as GPIO
#Global Variables
stopflag = 0


def power_off_pi():
    tts.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    tts.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    tts.say('My IP address is %s' % ip_address.decode('utf-8'))


def process_event(assistant, led, event, piloto, distanceSensor, break_flag):   
    logging.info(event)
    
    if event.type == EventType.ON_START_FINISHED:
        led.state = Led.BEACON_DARK  # Ready.
        print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        led.state = Led.ON  # Listening.
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'move forward':
            piloto.set_changed_direction(True)
            piloto.move('move forward')
            while distanceSensor.get_distance() > 0.3 :
                distanceSensor.get_distance()
            piloto.set_changed_direction(True)
            piloto.move('stop')
        elif text =='stop':
            piloto.set_changed_direction(True)
            piloto.move('stop')
        elif text == 'move backwards':
            piloto.set_changed_direction(True)
            piloto.move('move backwards')
        elif text == 'turn right':
            #piloto.set_changed_direction(True)
            piloto.move('turn right')
            piloto.move('stop')
        elif text == 'turn left':
            piloto.set_changed_direction(True)
            piloto.move('turn left')  
            piloto.move('stop') 
        elif text == 'turn around':
            piloto.set_changed_direction(True)
            piloto.move('turn around')
            piloto.move('stop')
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
    elif event.type == EventType.ON_END_OF_UTTERANCE:
        led.state = Led.PULSE_QUICK  # Thinking.
    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        led.state = Led.BEACON_DARK  # Ready.
    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)

def main():
    logging.basicConfig(level=logging.INFO)
    piloto = Pilot()
    print(piloto)
    distanceSensor = DistanceSensor()
    credentials = auth_helpers.get_assistant_credentials()
    with Board() as board, Assistant(credentials) as assistant:
        #For each event that happens when the assitant start we process the event.
        while True:
            print("Wicho ultrasonic sensor:  " + str(distanceSensor.get_distance()))
            for event in assistant.start():
                break_flag = False
                process_event(assistant, board.led, event, piloto, distanceSensor, break_flag)

class Pilot:
    def __init__(self):
        self.changed_direction = False
        self.movements = Movements()
        print("Wicho Initiating distance sensor")
        self.distanceSensor =  DistanceSensor()
        print("Pilot Instance has been created " + str(self.changed_direction))
        
    def set_changed_direction(self, value):
        self.changed_direction = value

    def __repr__(self):
        return "This is the Pilot Instance "
    
    def nomames(self):
        print("this fucntion works just fine ")

    def move(self, direction):
        ##Use Machine learnining to classify commends to remove all the if statements 
        print("Pilot Move has been executed!! " + str(self.changed_direction))
        if direction == 'move forward':
            self.movements.move_forward()
            self.changed_direction = False
        elif direction =='stop':
            self.movements.stop()
            self.changed_direction = False
        elif direction == 'move backwards':
            self.movements.move_backward()
            self.changed_direction = False
        elif direction == 'turn right':
            self.movements.turn_right()
            self.changed_direction = False
            sleep(0.5)
        elif direction == 'turn left':
            self.movements.turn_left()
            self.changed_direction = False
            sleep(0.5)
            print("5 Seconds passed")
        elif direction == 'turn around':
            self.movements.turn_right()
            self.changed_direction = False
            sleep(0.7)

    def check_distance(self):
        print("wicho 2this is the distance" + str(self.distanceSensor.get_distance()))
        try:
            while self.distanceSensor.get_distance() > 0.3 :
                self.distanceSensor.get_distance()
                #time.sleep(1)
        except KeyboardInterrupt:
            print("GPIO Pins for Ultrasonic sensors was interrupted by KeyboardInterrupt")
        finally:
            GPIO.cleanup()
if __name__ == '__main__':
    main()
