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



def getGrows(dias,temps,alpha,a,tableTau,step,intervals):

    grows = np.zeros((int(len(dias)),len(intervals)))
#    print(len(grows))
    growLast = np.array(np.zeros(len(intervals)))
    growNew = np.array(np.zeros(len(intervals)))
    deltaGrowLast =np.array(np.zeros(len(intervals)))
    deltaGrowNew = np.array(np.zeros(len(intervals)))
    growLast_a = np.array(np.zeros(len(intervals)))
    grow = np.array(np.zeros(len(intervals)))
    it = 0;
    growNew_a = np.array(np.zeros(len(intervals)))
    grow = np.array(alpha*np.ones(len(intervals)))
    deltas = np.array(np.ones(len(intervals)))
    #grow2 = alpha
    indexI = 0
   # print(grows.shape)
    for i in dias:
        print(i)
        for j in intervals:
            if(i-j>=0):              
                growNew[indexI] = growth_gr(i-j,temps[it],alpha,a,tableTau)
                growNew_a[indexI] = growth_gr(i-step-j,temps[it],alpha,a,tableTau)
            
                deltaGrowNew[indexI] = (growNew[indexI] - growNew_a[indexI])/(2.0)
            
                growLast[indexI] = growth_gr(i-j,temps[it-1],alpha,a,tableTau)
                growLast_a[indexI] = growth_gr(i-step-j,temps[it-1],alpha,a,tableTau)
            
                deltaGrowLast[indexI] = (growLast[indexI] - growLast_a[indexI])/(2.0)
            
                deltas[indexI] =  (deltaGrowNew[indexI] + deltaGrowLast[indexI])
            
                grow[indexI]  =  grow[indexI] + deltas[indexI]
                print(grow[indexI])
                #print(indexI)
                grows[it][indexI] = grow[indexI]
            else:
                continue
            indexI += 1
        indexI=0
        it=it+1
    return grows
 

alpha = 0.1 
a = 3500
temps = []   
tempMin = 18
tempMax = 31
dayMax = 750
step = 30; 

dias = range(0,dayMax,step)#Definimos un rango de días.
temp = []
for i in range(len(dias)):
    temps.append(randrange(tempMin,tempMax))

    
    


#df = pd.read_csv('daysXtemps.txt', skiprows=0,header=None)
#df.columns=['dias','temps']
#dias = df.dias.values

#temps = df.temps.values


intervals=[0,120,240]
grows = getGrows(dias, temps, alpha, a, tableTau, step, intervals)

plt.xlabel("Día")
plt.ylabel("Crecimiento acumulado")
plt.title("G(t,a,a)")
plt.plot(dias,grows[:,0],'-', dias,grows[:,1],'k',dias,grows[:,2],'-')
#plt.plot(dias,grows[:,1],'k')
plt.axhline(y=450, xmin=0, xmax=dayMax,color='r')
plt.axvline(x = 0)
xpoints = intervals
colors = ['g', 'c', 'm']
for p,c in zip(xpoints,colors):
     plt.axvline(p,  label='line: {}'.format(p), c=c)
plt.legend()
#plt.plot(dias2,grows2,'k')
plt.show()






