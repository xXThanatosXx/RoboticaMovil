from pyPso import *
import matplotlib.pyplot as plt
import numpy as np

############################## Respuesta al escalon ########################

def fodt(u,t,*args):

     K     = args[0][0]
     tau   = args[0][1]
     delay = args[0][2]
     
     N = len(t)
     
     y = np.zeros(N)
     
     flag = False

     for k in range(N):
          
          if k == 0:
               du = u[k]
          else:
               du = u[k]-u[k-1]
               
          if du != 0:
               flag=True
               n=0
               
          if flag:
               if n*ts < delay:
                    y[k] = y[k]
               else:
                    y[k] = K*u[k]*(1-np.exp(-(n*ts-delay)/tau))
               n = n+1
                    
     return y

################################## Funcion de costo ############################

def costFunction(x):
     
     K     = x[:,0]
     tau   = x[:,1]
     delay = x[:,2]
     
     cost = np.zeros(swarmsize)
     
     for particle in range(swarmsize):
          ye = fodt(u,t,[K[particle],tau[particle],delay[particle]])
          error = y-ye
          cost[particle] = error.reshape(-1,1).T@error # sum(error^2)  
     
     return cost

     
############################ Cargar señales medidas #######################     
with open('firstResponse.npy', 'rb') as f:
    u  = np.load(f)
    y  = np.load(f)
    t  = np.load(f)
    ts = np.load(f)


############################ Encontrar parametros ###########################    
swarmsize = 20
variables = 3
maxGen = 200

p = pso(costFunction,swarmsize,variables)

p.run(maxGen)

print(f"K = {np.round(p.globalp[0],4)}")
print(f"tau = {np.round(p.globalp[1],4)}")
print(f"delay = {np.round(p.globalp[2],4)}")

###################### Respuesta con valores optimos ###############
ye = fodt(u,t,p.globalp)

###################### Mostrar figuras ######################
plt.figure()
plt.plot(p.summary,label='Global error')
plt.legend(loc='upper left')

plt.figure()
plt.plot(t,ye,label='Pv_estimated')
plt.plot(t,y,label='Pv_real')
plt.plot(t,u,label='Cv')
plt.legend(loc='upper left')

plt.show()


