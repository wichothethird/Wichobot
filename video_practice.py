import cv2
import numpy
import io
import picamera


def main():

    stream = io.BytesIO()
    print("open CV was impoted correctly!!!!")
    face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
    img = cv2.imread('sachin.jpg')
    with picamera.PiCamera() as camera:
        print("Wicho esto paso")
        camera.resolution = (320, 240)
        camera.capture(stream, format='jpeg')


    buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)
    image =cv2.imdecode(buff,1)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    print("{} faces detected!!!".format(str(len(faces))))
    print("No mames ")

    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
    cv2.imwrite('result.jpg',image)


if __name__=='__main__':
    main()
