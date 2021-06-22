import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import random
from random import randrange
from random import randint


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

def assigNum(flags):
    sizeOptimal = np.count_nonzero(flags)
    generationsOptimals = np.array(np.zeros(sizeOptimal));
    cont = 0
    for i in range(len(flags)):
        if(flags[i]==1):
            generationsOptimals[cont]  = i;
            cont+=1
    return generationsOptimals
            

def getGrows(dias,temps,alpha,a,tableTau,step,umbralTemp,umbralGrow = 400):
    intervals = [0]
    grows = np.zeros((int(len(dias)),int(len(dias))))
#    print(len(grows))
    growLast = np.array(np.zeros(int(len(dias))))
    growNew = np.array(np.zeros(int(len(dias))))
    deltaGrowLast =np.array(np.zeros(int(len(dias))))
    deltaGrowNew = np.array(np.zeros(int(len(dias))))
    growLast_a = np.array(np.zeros(int(len(dias))))
    grow = np.array(np.zeros(int(len(dias))))
    it = 0;
    growNew_a = np.array(np.zeros(int(len(dias))))
    grow = np.array(alpha*np.ones(int(len(dias))))
    deltas = np.array(np.ones(int(len(dias))))
    #grow2 = alpha
    indexI = 0
   # print(grows.shape)
    countingGrows = np.array(np.zeros(len(dias)))
    flagsOptimals = np.array(np.zeros(len(dias)))
    for i in dias:
        #print(intervals)
       # print(temps[it])
        if(temps[it]<= umbralTemp ):
            intervals.append(i)
           # print(intervals)
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
                grows[it][indexI] = grow[indexI]
                if(grow[indexI]<=umbralGrow):
                    countingGrows[indexI] += 1
                if(grow[indexI]>umbralGrow):
                    flagsOptimals[indexI] = 1
                    
            else:
                continue
            indexI += 1
        indexI=0#Itera sobre cada generación
        it=it+1#Itera por cada día.
        optimalGen = assigNum(flagsOptimals)
    return grows,intervals,countingGrows,optimalGen
 

###-------------------------Parámetros-----------------------------------------
alpha = 0.1; 
a = 3500;
tempMin = 18
tempMax = 27
dayMax = 365;
step = 1; 
umbralTemp = 18;
umbralGrow = 350;
###-------------------------Finaliza parámetros--------------------------------


temps = [] 
dias = range(0,dayMax,step)#Definimos un rango de días.
temp = []
for i in range(len(dias)):
    temps.append(randrange(tempMin,tempMax))

grows,intervals,countingGrows,generGood = getGrows(dias, temps, alpha, a, tableTau, step,umbralTemp,umbralGrow)

plt.figure(num=0,figsize=(15,10),
           facecolor='white')
plt.xlabel("Día")
plt.ylabel("Crecimiento acumulado")
plt.title("G(t,a,a)")
plt.plot(dias,grows[:,:])
#plt.plot(dias,grows[:,1],'k')
plt.axhline(y=umbralGrow, xmin=0, xmax=dayMax,color='r')
plt.axvline(x = 0)
xpoints = intervals
colors = []
for i in range(len(intervals)):
    colors.append('#%06X' % randint(0, 0xFFFFFF))
for p,c in zip(xpoints,colors):
     plt.axvline(p,  label='line: {}'.format(p),c=c)
#plt.plot(dias2,grows2,'k')
     
fig = plt.figure(num=1,figsize=(10,5),
           facecolor='white')
ax = fig.add_axes([0,0,1,1])     
ax.set_title('Optimal Generations with counting days')
ax.set_ylabel('Days')
ax.set_xlabel('Generations')
colorsGen = []
for i in range(len(generGood)):
    colorsGen.append('#%06X' % randint(0, 0xFFFFFF))
for i,c in zip(generGood,colorsGen):
    ax.bar(int(i),countingGrows[int(i)],color= c)
    
plt.show()






