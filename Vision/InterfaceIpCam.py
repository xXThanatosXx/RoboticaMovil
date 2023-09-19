
from tkinter import *
from PIL import Image, ImageTk

import cv2
import sys

def onClossing():
     root.quit()
     cap.release()
     print("Camera Disconected")
     root.destroy()
     

def callback():
     cap.open(url)
     ret, frame = cap.read()

     if ret:
          img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          img = Image.fromarray(img)
          img.thumbnail((400,400))
          tkimage = ImageTk.PhotoImage(img)
          label.configure(image = tkimage)
          label.image = tkimage
          root.after(1,callback)
     else:
          onClossing()
          
     

     
url =  'http://192.168.1.191:8080/shot.jpg'
cap = cv2.VideoCapture(url)


if cap.isOpened():
    print("Ip Cam initializatized")
else:
    sys.exit("Ip Cam disconnected")


root = Tk()
root.protocol("WM_DELETE_WINDOW",onClossing)
root.title("Vision Artificial")

label = Label(root)
label.grid(row=0)

root.after(1,callback)

root.mainloop()

