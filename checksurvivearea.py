
def invalidsubzones():

    return

def validzones(maxx, minx, maxy, miny, invalidpoints=[]):
    """
    SUMMARY
    This creates a list of points that a creature won't die if it goes to.

    PARAMETERS
    maxx (int): The furthest right a creature could go
    minx (int): The furthest left a creature could go
    maxy (int): The furthest up a creature could go
    miny (int): The furthest down a creature could go
    invalidpoints (list): List of points where the creature would die if it goes there

    RETURNS
    validpoint (list): The list of points that a creature won't die if it goes to
    """
    validpoints=[]
    for i in range(minx, maxx+1):
        for j in range(miny, maxy+1):
            if [i,j] not in invalidpoints:
                validpoints.append([i,j])
    return validpoints
