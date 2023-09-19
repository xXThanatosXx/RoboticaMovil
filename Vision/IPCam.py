import cv2
import sys

url =  'http://192.168.1.191:8080/shot.jpg'
cap = cv2.VideoCapture(url)


if cap.isOpened():
    print("Ip Cam initializatized")
else:
    sys.exit("Ip Cam disconnected")


while(cap.isOpened()):
    
     cap.open(url) # Antes de capturar el frame abrimos la url
     ret, frame = cap.read()
    
     if ret:
         cv2.imshow('img',frame)
     else:
         print("Ip Cam disconnected")
         break
        
     if (cv2.waitKey(1) & 0xFF == 27):
         break
    
cap.release()
cv2.destroyAllWindows()


