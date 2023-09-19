from pyArduino import *
import matplotlib.pyplot as plt
import numpy as np

ts = 0.1 # Tiempo de muestreo
tf = 10  # Tiempo de simulacion
t = np.arange(0,tf+ts,ts) # Array de tiempo
N = len(t) # Numero de muestras

######################## Comunicacion Serial ###############

port = 'COM6'  # Com Arduino
baudRate = 115200 # Baudios

arduino = serialArduino(port,baudRate)# Objeto serial

arduino.readSerialStart() # Inicia lectura de datos

######################### Señales #####################

y  = np.zeros(N) # Variable de proceso (Pv)
u  = np.zeros(N) # Variable de control (Cv)

########################## Loop ########################

for k in range(N):

     start_time = time.time() # Tiempo actual

     # Escalon 
     if k*ts   > 3:  # Escalon a los 3 segundos
          u[k] = 40  # Valor escalon del 0 al 100% (40%)
     else:
          u[k] = 0;
     
     arduino.sendData([u[k]]) # Enviar Cv (debe ser una lista)
     
     y[k] = arduino.rawData[0] # Recibir Pv 
          
     elapsed_time = time.time() - start_time # Tiempo transcurrido
     
     time.sleep(ts-elapsed_time) # Esperar hasta completar el tiempo de muestreo
     
     
arduino.sendData([0]) # Detener motor     
arduino.close() # Cerrar puerto serial

######################## Guardar señales ###########################
with open('firstResponse.npy', 'wb') as f:
     np.save(f,u)
     np.save(f,y)
     np.save(f,t)
     np.save(f,ts)
     
###################### Mostrar figuras ######################
     
plt.plot(t,y,label='Pv')
plt.plot(t,u,label='Cv')
plt.legend(loc='upper left')
plt.show()
