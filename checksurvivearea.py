from matplotlib.collections import PolyCollection
from matplotlib.path import Path

def getpoly(vertssets):
    """
    SUMMARY
    This returns polygon object(s) to be plotted.

    PARAMETERS
    vertssets (list): list of list of vertices in order of connection like [[[x1,y1], [x2,y2], [x3,y3]],[x1,y1], [x2,y2], [x3,y3]]

    RETURNS
    poly (matplotlib.collections.PolyCollection): The poly object to be plotted
    """
    poly = PolyCollection(vertssets, facecolors="black")
    return poly


def invalidsubzones(vertssets):
    """
    SUMMARY
    This returns a list of pointss within polygons for use in checking if a creature dies upon going to a point.

    PARAMETERS
    vertssets (list): list of list of vertices in order of connection like [[[x1,y1], [x2,y2], [x3,y3]],[x1,y1], [x2,y2], [x3,y3]]

    RETURNS
    invalidpoints (list): list of points in polygons
    """
    invalidpoints=[]
    for verts in vertssets:
        p = Path(verts) # make a polygon
        xvert=[]
        yvert=[]
        for i in range(len(verts)):
            xvert.append(verts[i][0])
            yvert.append(verts[i][1])
        for i in range(min(xvert), max(xvert)+1):
            for j in range(min(yvert), max(yvert)+1):
                if p.contains_point([i,j]):
                    invalidpoints.append([i,j])
    return invalidpoints

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
