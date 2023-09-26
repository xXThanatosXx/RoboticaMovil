from pyRobotics import *
import time
from pyArduino import *
import matplotlib.pyplot as plt

#################### TIEMPO ###################

tf = 18 # tiempo de simulacion
ts = 0.1 #  tiempo de muestreo
t = np.arange(0,tf+ts,ts) # vector tiempo

N = len(t) # cantidad de muestras

################### CONDICIONES INICIALES ###################

# Asignar memoria 
hx = np.zeros(N+1) 
hy = np.zeros(N+1)
phi = np.zeros(N+1)

hx[0] = 0  # Posicion inicial en el eje x en metros [m]
hy[0] = 0  # Posicion inicial en el eje y en metros [m]
phi[0] = 0 # Orientacion inicial en radianes [rad]

################### POSICION DESEADA ####################
hxd = 1
hyd = -1
phid = np.pi/2

################### VELOCIDADES DE REFERENCIA #################### 

uRef = np.zeros(N)  # Velocidad lineal en metros/segundos [m/s]
wRef = np.zeros(N) # Velocidad angular en radianes/segundos [rad/s]

################### VELOCIDADES MEDIDAS #################### 

uMeas = np.zeros(N)  # Velocidad lineal en metros/segundos [m/s]
wMeas = np.zeros(N)  # Velocidad angular en radianes/segundos [rad/s]

################## COMUNICACION SERIAL #########################
port = 'COM6'
baudRate = 115200 # Baudios
arduino = serialArduino(port,baudRate,2)
arduino.readSerialStart()

################### ERRORES ####################

l=np.zeros(N)
rho=np.zeros(N)
thetha=np.zeros(N)

################### PARAMETROS DE CONTROL ####################
gain = np.zeros(N)

################### BUCLE ####################  
for k in range(N):

     start_time = time.time() # Tiempo actual
     
     #################### CONTROL #####################

     # Errores
     l[k] = np.sqrt((hxd-hx[k])**2+(hyd-hy[k])**2)
     rho[k] = np.arctan2((hyd-hy[k]),(hxd-hx[k]))-phi[k]
     thetha[k] = np.arctan2((hyd-hy[k]),(hxd-hx[k]))-phid

     # Parametros de control
     kmax = 1.7
     g = 10
     gain[k] = kmax/(1+g*l[k])
     
     # Parametros de control
     K1=gain[k] 
     K2=gain[k] 

     # Ley de control
     uRef[k] = K1*np.cos(rho[k])*l[k]
     wRef[k] = K2*rho[k]+(K1/rho[k])*np.cos(rho[k])*np.sin(rho[k])*(rho[k]+thetha[k])
     

     #################### APLICAR ACCIONES DE CONTROL #####################

     arduino.sendData([uRef[k],wRef[k]])

     uMeas[k] = arduino.rawData[0]
     wMeas[k] = arduino.rawData[1]
     
     # Integral numerica
     phi[k+1] = phi[k]+ts*wMeas[k]

     # Modelo cinemático
     
     hxp = uMeas[k]*np.cos(phi[k+1])
     hyp = uMeas[k]*np.sin(phi[k+1])
     
     # Integral numerica
     hx[k+1] = hx[k] + ts*hxp
     hy[k+1] = hy[k] + ts*hyp

     elapsed_time = time.time() - start_time # Tiempo transcurrido
     
     time.sleep(ts-elapsed_time) # Esperar hasta completar el tiempo de muestreo
     
################## COMUNICACION SERIAL #########################

arduino.sendData([0,0]) # Detener robot     
arduino.close() # Cerrar puerto serial
     
################### SIMULACION VIRTUAL #################### 

# Cargar componentes del robot
pathStl = "stl"
color = ['black','black','gray','gray','white','blue']
uniciclo = robotics(pathStl,color)

# Configurar escena
xmin = -3
xmax = 3
ymin = -3
ymax = 3
zmin = 0
zmax = 2
bounds = [xmin, xmax, ymin, ymax, zmin, zmax]
uniciclo.configureScene(bounds)

# Mostrar graficas 
uniciclo.initTrajectory(hx,hy) # Graficar Trayectoria realizada por el robot

# Mostrar robots
escala = 5
uniciclo.initRobot(hx,hy,phi,escala)

# Iniciar simulacion
uniciclo.startSimulation(1,ts)

############################## Graficas ######################
# https://matplotlib.org/3.3.1/api/_as_gen/matplotlib.pyplot.plot.html

# Errores
fig = plt.figure()
plt.subplot(211)
plt.plot(t,l,'b',linewidth = 2, label='l')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Error [m]')
plt.grid()

plt.subplot(212)
plt.plot(t,rho,'r',linewidth = 2,  label='rho')
plt.plot(t,thetha,'g',linewidth = 2,  label='tetha')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Error [rad]')
plt.grid()

# Acciones de control
fig = plt.figure()
plt.subplot(211)
plt.plot(t,uMeas,label='Velocidad lineal medida')     
plt.plot(t,uRef,label='Velocidad lineal referencia')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [m/s]')
plt.grid()

plt.subplot(212)
plt.plot(t,wMeas,label='Velocidad angular medida')     
plt.plot(t,wRef,label='Velocidad angular referencia')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [rad/s]')
plt.grid()

# Parametros de control
fig = plt.figure()
plt.plot(t,gain,'b',linewidth = 2, label='gain')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Ganancia')
plt.grid()

plt.show()

plt.show()


