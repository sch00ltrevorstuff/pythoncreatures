import numpy as np

#no movement
def nochange(amplitude, xpos, ypos):
    """
    SUMMARY
    This function just returns the current x and y positions for when the creature does not move.

    PARAMETERS
    amplitude (int): How far the creature would move if it would have
    xpos (int): Current x position
    ypos (int): Current y position

    RETURNS
    xpos (int): New x position
    ypos (int): New y position
    """
    return xpos, ypos

#moving in one direction
def ymov(amplitude, xpos, ypos):
    """
    SUMMARY
    This function moves the creature up.

    PARAMETERS
    amplitude (int): How far it will move
    xpos (int): Current x position
    ypos (int): Current y position

    RETURNS
    xpos (int): New x position
    ypos (int): New y position
    """
    ypos=ypos+amplitude
    return xpos, ypos
def xmov(amplitude, xpos, ypos):
    """
    SUMMARY
    This function moves the creature right.

    PARAMETERS
    amplitude (int): How far it will move
    xpos (int): Current x position
    ypos (int): Current y position

    RETURNS
    xpos (int): New x position
    ypos (int): New y position
    """
    xpos=xpos+amplitude
    return xpos, ypos

def ymovback(amplitude, xpos, ypos):
    """
    SUMMARY
    This function moves the creature down.

    PARAMETERS
    amplitude (int): How far it will move
    xpos (int): Current x position
    ypos (int): Current y position

    RETURNS
    xpos (int): New x position
    ypos (int): New y position
    """
    ypos=ypos-amplitude
    return xpos, ypos
def xmovback(amplitude, xpos, ypos):
    """
    SUMMARY
    This function moves the creature left.

    PARAMETERS
    amplitude (int): How far it will move
    xpos (int): Current x position
    ypos (int): Current y position

    RETURNS
    xpos (int): New x position
    ypos (int): New y position
    """
    xpos=xpos-amplitude
    return xpos, ypos

#list of the functions
funclist=[nochange, ymov, xmov, ymovback, xmovback]

def funcchoose(chances):
    """
    SUMMARY
    This chooses the function for movement from the creature's weights.
    It also normalizes the chances so they add to 1.

    PARAMETERS
    chances (list): The creature's weights for each choice

    RETURNS
    fchoice (function): The movement function to use for the creature
    """
    #normalizes
    prob=[i/sum(chances) for i in chances]
    fchoice=np.random.choice(funclist, p=prob)
    return fchoice