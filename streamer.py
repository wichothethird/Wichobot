import cv2
import time 
from picamera import PiCamera
from picamera.array import PiRGBArray
from os.path import join
from os import listdir
import os
import numpy as np
from PIL import Image


path = "/home/pi/AIY-projects-python/src/examples/voice/Friends/"
face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
def take_screenshots():


    #initialize the camera 
    print("Camera was initialized!!!")
    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate = 32
    
    output = PiRGBArray(camera, size=(640,480))

    #Classifier to teach the model to learn what a face is.
    print("Teaching the model to learn what a face is!!!")
    

    #Warm up time
    time.sleep(0.1)

    count = 1
    face_id = 1 
    
    for frame in camera.capture_continuous(output, format="bgr",use_video_port=True):

        
        #Image is a 2D array representing the frame
        image = frame.array
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        print("{} faces detected!!!".format(str(len(faces))))
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)        
            cv2.imwrite("/home/pi/AIY-projects-python/src/examples/voice/Friends/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            
        count+=1
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        output.truncate(0)


        if key==ord("q"):
            break

        elif count>50:
            print("100 Pictures were taken for the face!!!")
            break



def detect_people():


    #initialize the camera 
    print("Camera was initialized!!!")
    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate = 32
    
    output = PiRGBArray(camera, size=(640,480))

    #Classifier to teach the model to learn what a face is.
    print("Teaching the model to learn what a face is!!!")
    

    #Warm up time
    time.sleep(0.1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load the trained mode
    recognizer.read('learner/trainer.yml')
    
    for frame in camera.capture_continuous(output, format="bgr",use_video_port=True):

        
       #Image is a 2D array representing the frame
        image = frame.array
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        print("{} faces detected!!!".format(str(len(faces))))
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)        
            Id,probability = recognizer.predict(gray[y:y+h,x:x+w])
            print("this is {}".format(Id))
            # Check the ID if exist 
            if(Id == 1):
                Id = "Wicho"
            #If not exist, then it is Unknown
        
            else:
                print(Id)
                Id = "Unk"

            # Put text describe who is in the picture
            cv2.rectangle(image, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
            cv2.putText(image, str(Id), (x,y-40), font, 2, (255,255,255), 3)
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        output.truncate(0)


        if key==ord("q"):
            break





def get_images():
    lista = []
    lista=os.listdir(path)
    list_of_paths =[]
    faceSamples = []
    ids = []
    for i in lista:
        print("{}".format(i))
        list_of_paths.append(os.path.join(path,i))

    
    for imagePath in list_of_paths:
        
        
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
             
        faces = face_cascade.detectMultiScale(img_numpy)
     
        for (x,y,w,h) in faces:
          
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
  
    return faceSamples,ids
        

def main():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #take_screenshots()
    faces, ids = get_images()
    # Train the model using the faces and IDs
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer.yml
    recognizer.save('learner/trainer.yml')        
    print(ids)
    detect_people()
    
if __name__=='__main__':
    main()
