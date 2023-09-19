############## Importar modulos #####################

from tkinter import *
from PIL import Image, ImageTk #pip install pil

import cv2
import time
import numpy as np
import sys
def calculateFocal():   
    global isCalculateFocal
    global isCalculateDistance
    isCalculateDistance = False
    isCalculateFocal = True

def calculateDistance():        
    global isCalculateFocal
    global isCalculateDistance
    isCalculateFocal = False
    isCalculateDistance = True


def onClossing():
    print(distanceFocal.get())
    root.quit()                 #Salir del bucle de eventos.
    cap.release()               #Cerrar camara
    print("Ip Cam Disconected")
    root.destroy()              #Destruye la ventana tkinter creada
    

def objectDetection(rawImagen):
    
    isObject = False   # Verdadero si encuentra un objeto
    
    u,v = 0,0  #ancho (u), alto (v) en pixeles
                       
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a BGR a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    obj = leftCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3) # Deteccion de objeto
    
    if len(obj):
        isObject = True
        for (cx,cy,u,v) in obj:
            cv2.rectangle(rawImagen,(cx,cy),(cx+u,cy+v),(255,0,0),2)
            cv2.circle(rawImagen,(int(cx+u/2),int(cy+v/2)), 5, (255,255,0), -1)

    else:
        isObject = False
        
    return isObject,rawImagen,u,v

    
def callback():
    ################## Adquisición de la Imagen ############
    
    cap.open(url) # Antes de capturar el frame abrimos la url
    ret, frame = cap.read() # Leer Frame

    if ret:
        
        isObject,frame,u,v = objectDetection(frame)
        
        if isObject:
            
            w = float(entryWidth.get()) # ancho objeto en metros
            
            if (isCalculateFocal):
                global focal
                distance = float(entryDistance.get())       
                focal = (u*distance)/w
                distanceFocal.set("Distancia Focal: "+str(round(focal,2)))

            if (isCalculateDistance):
                distance = (focal*w)/u
                distanceObject.set("Distancia al objeto: "+str(round(distance,2)))

        # Mostrar imagen en el HMI
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img.thumbnail((400,400)) #Redimensionar imagen
        tkimage = ImageTk.PhotoImage(img)
        label.configure(image = tkimage )
        label.image = tkimage

        root.after(10,callback)

# Objeto haar-cascada
leftCascade = cv2.CascadeClassifier('left.xml')

########################### Ip Cam ###########################

url='http://192.168.1.191:8080/shot.jpg'

cap = cv2.VideoCapture(url)

if cap.isOpened():
    print("Ip Cam initializatized")
else:
    sys.exit("Ip Cam disconnected")
    
############################## Variables #################    
focal = 0
isCalculateFocal = False
isCalculateDistance = False

############################## HMI design #################
root = Tk()
root.protocol("WM_DELETE_WINDOW",onClossing)
root.title("Vision Artificial") # titulo de la ventana


label=Label(root)
label.grid(padx=20,pady=20)

distanceFocal = StringVar(root,"Distancia Focal: 0")
labelF = Label(root, textvariable = distanceFocal)
labelF.grid(row= 0,column=1, padx=20,pady=10)

distanceObject = StringVar(root,"Distancia al objeto: 0")
labelD = Label(root, textvariable = distanceObject)
labelD.grid(row= 0,column=2, padx=20,pady=10)

labelA = Label(root, text = "Ingrese ancho (m): ")
labelA.grid(row= 1,column=1, padx=20,pady=10)

labelIF = Label(root, text = "Ingrese distancia: ")
labelIF.grid(row= 1,column=2, padx=20,pady=10)

entryWidth = Entry(root)
entryWidth.grid(row= 2,column=1,padx=20,pady=20)
entryWidth.insert(0, "0.06")

entryDistance = Entry(root)
entryDistance.grid(row= 2,column=2,padx=20,pady=20)
entryDistance.insert(0, "0.25")

buttonFocal = Button(root,text ="Distancia Focal",command=calculateFocal) 
buttonFocal.grid(row= 3,column=1, padx=20,pady=20)

buttonDis = Button(root,text ="Distancia",command=calculateDistance) 
buttonDis.grid(row= 3,column=2,padx=20,pady=20)


root.after(10,callback) 
root.mainloop()
