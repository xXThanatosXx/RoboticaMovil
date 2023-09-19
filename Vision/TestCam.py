import cv2 
import sys

cap =  cv2.VideoCapture(2)

if cap.isOpened():
    print("Usb Cam initializatized")
else:
    sys.exit("Usb Cam Disconnected")


while True:
        ret, frame = cap.read()

        if ret:
            cv2.imshow('Visual',frame)
        else:
            print("Usb Cam disconnected")
            break
        if (cv2.waitKey(1) & 0XFF == 27):
            break
cap.release()
cv2.destroyAllWindows()



