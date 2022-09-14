import numpy as np
import random

def newchances(oldchances, mutationrate):
    """
    SUMMARY
    This passes down the traits of a creature to its offspring, including if there is mutations.

    PARAMETERS
    oldchances (list): List of the creature's chances to pass down
    mutationrate (int): MUST BE BELOW 1 AND GREATER THAN 0. The probability per chance that it will change

    RETURNS
    newchancesnorm (list): The list of new weights for the new creatures.
    """
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
