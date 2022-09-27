from numpy.random import choice
from numpy.random import uniform

def newchances(oldchances, mutationrate):
    """
    SUMMARY
    This passes down the move chances of a creature to its offspring, including if there is mutations.

    PARAMETERS
    oldchances (list): List of the creature's chances to pass down
    mutationrate (float): MUST BE BELOW 1 AND GREATER THAN 0. The probability per chance that it will change

    RETURNS
    newchancesnorm (list): The list of new weights for the new creatures.
    """
    newchances=[]
    for i in oldchances:
        #if mutate
        mutateornot=[True, False]
        mutateisgo=choice(mutateornot, p=[mutationrate,1-mutationrate])
        if mutateisgo==True:
            mutateamplitude=uniform(0,2)
            newchances.append(i*mutateamplitude)
        else:
            newchances.append(i)
    #normalize the newchances
    newchancesnorm=[i/sum(newchances) for i in newchances]
    return newchancesnorm

def newattr(oldamp, oldvs, oldctr, mutationrate):
    """
    SUMMARY
    This passes down attributes to new creatures.

    PARAMETERS
    oldamp (int): The old amplitude
    oldvs (int): The old vision strength
    oldctr (int): The old chance to react
    mutationrate (float): MUST BE BELOW 1 AND GREATER THAN 0. The probability per attribute that it will change

    RETURNS
    newamp (int): The new amplitude
    newvs (int): The new vision strength
    newctr (int): The new chance to react
    """
    #amplitude
    if choice([1,0], p=[mutationrate,1-mutationrate]):
        if oldamp==0: oldamp=1
        mutateamplitude=uniform(0,2)
        newamp=int(round(oldamp*mutateamplitude))
    else:
        newamp=oldamp
    #vision strength
    if choice([1,0], p=[mutationrate,1-mutationrate]):
        if oldvs==0: oldvs=1
        mutateamplitude=uniform(0,2)
        newvs=int(round(oldvs*mutateamplitude))
    else:
        newvs=oldvs
    #chance to react
    if choice([1,0], p=[mutationrate,1-mutationrate]):
        if oldctr==0: oldctr=uniform(0,1)
        mutateamplitude=uniform(0,2)
        newctr=oldctr*mutateamplitude
        if newctr>1: newctr=1
    else:
        newctr=oldctr
    return newamp, newvs, newctr