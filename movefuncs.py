import numpy as np

#no movement
def nochange(amplitude, xpos, ypos):
    return xpos, ypos

#moving in one direction
def ymov(amplitude, xpos, ypos):
    ypos=ypos+amplitude
    return xpos, ypos
def xmov(amplitude, xpos, ypos):
    xpos=xpos+amplitude
    return xpos, ypos

def ymovback(amplitude, xpos, ypos):
    ypos=ypos-amplitude
    return xpos, ypos
def xmovback(amplitude, xpos, ypos):
    xpos=xpos-amplitude
    return xpos, ypos

funclist=[nochange, ymov, xmov, ymovback, xmovback]

def funcchoose(chances):
    #normalizes
    prob=[i/sum(chances) for i in chances]
    fchoice=np.random.choice(funclist, p=prob)
    return fchoice