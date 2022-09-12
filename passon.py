import numpy as np
import random

def newchances(oldchances, mutationrate):
    newchances=[]
    for i in oldchances:
        #if mutate
        mutateornot=[True, False]
        mutateisgo=np.random.choice(mutateornot, p=[mutationrate,1-mutationrate])
        if mutateisgo==True:
            mutateamplitude=random.uniform(0,2)
            newchances.append(i*mutateamplitude)
        else:
            newchances.append(i)
    #normalize the newchances
    newchancesnorm=[i/sum(newchances) for i in newchances]
    return newchancesnorm
