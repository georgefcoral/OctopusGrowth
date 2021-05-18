import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import random
from random import randrange


def growth_gr(t,temp,alpha,a,tableTau):
    tau = tableTau[temp]
    return (alpha*a)/(alpha + (a - alpha)*np.exp(-t/tau) ) 


#Definimos una tabla en forma de diccionario para cada una de las TAU 
#Dependientes de la temperatura.
tableTau = {
    18:32.71,
    19:33.69,
    20:34.680,
    21:35.66,
    22:36.65,
    23:35.95,
    24:35.26,
    25:39.27,   
    26:43.28,
    27:68.34,
    28:93.34,
    29:118.37,
    30:143.4,
    31:168.43,
    32:168.43,
    }

def getGrows(dias,temps,alpha,a,tableTau,step):
    grows = []
    grows2 = []
    growLast = 0.0
    growNew = 0.0
    deltaGrowLast = 0.0
    deltaGrowNew = 0.0
    growLast_a = 0
    grow = 0.0
    it = 0;
    growNew_a = 0
    grow = alpha
    grow2 = alpha
    for i in dias:       
    
        growNew =  growth_gr(i,temps[it],alpha,a,tableTau)
        growNew_a = growth_gr(i-step,temps[it],alpha,a,tableTau)
        
        deltaGrowNew = (growNew - growNew_a)/(2.0)
        
        growLast =  growth_gr(i,temps[it-1],alpha,a,tableTau)
        growLast_a = growth_gr(i-step,temps[it-1],alpha,a,tableTau)
        
        deltaGrowLast = (growLast - growLast_a)/(2.0)
        
        deltas =  (deltaGrowNew + deltaGrowLast)
        
        grow =  grow + deltas
        if(i >=120):
            growNew2 =  growth_gr(i-120,temps[it],alpha,a,tableTau)
            growNew_a2 = growth_gr(i-step-120,temps[it],alpha,a,tableTau)
            deltaGrowNew2 = (growNew2 - growNew_a2)/(2.0)
            growLast2 =  growth_gr(i-120,temps[it-1],alpha,a,tableTau)
            growLast_a2 = growth_gr(i-step-120,temps[it-1],alpha,a,tableTau)
            deltaGrowLast2 = (growLast2 - growLast_a2)/(2.0)
            deltas2 =  (deltaGrowNew2 + deltaGrowLast2)
            grow2 =  grow2 + deltas2
            grows2.append(grow2)
        
        print("Dia: "   ,i," temps[it]: " , temps[it],"Crecimiento acumulado: ",grow)
        
        grows.append(grow)
        it=it+1
    return grows,grows2
 

alpha = 1 
a = 3500
temps = []   
tempMin = 18
tempMax = 31
dayMax = 720
step = 1; 

dias = range(0,dayMax,step)#Definimos un rango de días.
temp = []
for i in range(len(dias)):
    temps.append(randrange(tempMin,tempMax))
    temp.append(450)
    
    


#df = pd.read_csv('daysXtemps.txt', skiprows=0,header=None)
#df.columns=['dias','temps']
#dias = df.dias.values

#temps = df.temps.values

grows,grows2 = getGrows(dias,temps,alpha,a,tableTau,step)


dias2 =  range(120,dayMax)
plt.xlabel("Día")
plt.ylabel("Crecimiento acumulado")
plt.title("G(t,a,a)")
plt.plot(dias,grows,'.',dias,temp,'*', dias2,grows2,'k')
#plt.plot(dias2,grows2,'k')
plt.show()
grows





