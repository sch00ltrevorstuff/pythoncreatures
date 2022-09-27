import numpy as np

def looking(visionstrength,xpos,ypos,maxx,minx,maxy,miny,validpoints):
    """
    SUMMARY
    This function allow the creature to look straight up, down, left, and right.

    PARAMETERS
    visionstrength (int): How far a creature can see from its current position
    xpos (int): Current x position
    ypos (int): Current y position
    maxx (int): The max x position in the simulation
    minx (int): The min x position in the simulation
    maxy (int): The max y position in the simulation
    miny (int): The min y position in the simulation
    validpoints (list): A list of points [[x,y],[x,y]] that the creature can be

    RETURNS
    detections (list): A list of points that the creature can see are not allowed as [up,right,down,left]
    """
    #make empty lists in a list to be returned
    detections=[[] for _ in range(4)]
    #an array going up from current position
    lookup=np.linspace(ypos,maxy,abs(maxy-ypos)+1)
    pointsup=list(zip([xpos for _ in range(ypos,maxy+1)],lookup))
    #cut list of points on line of sight down to vision strength
    if len(pointsup) > visionstrength:
        pointsup=pointsup[:visionstrength]
    #check if points are allowed
    for i in pointsup:
        if i not in validpoints:
            detections[0]=i
            break
    lookright=np.linspace(xpos,maxx,abs(maxx-xpos)+1)
    pointsright=list(zip([ypos for _ in range(xpos,maxx+1)],lookright))
    if len(pointsright) > visionstrength:
        pointsright=pointsright[:visionstrength]
    for i in pointsright:
        if i not in validpoints:
            detections[1]=i
            break
    lookdown=np.linspace(ypos,miny,abs(miny-ypos)+1)
    pointsdown=list(zip([xpos for _ in range(miny,ypos+1)],lookdown))
    if len(pointsdown) > visionstrength:
        pointsdown=pointsdown[:visionstrength]
    for i in pointsdown:
        if i not in validpoints:
            detections[2]=i
            break
    lookleft=np.linspace(xpos,minx,abs(minx-xpos)+1)
    pointsleft=list(zip([ypos for _ in range(minx,xpos+1)],lookleft))
    if len(pointsleft) > visionstrength:
        pointsleft=pointsleft[:visionstrength]
    for i in pointsleft:
        if i not in validpoints:
            detections[3]=i
            break

    return detections

def react(chancetoreact,weights, detections, xpos, ypos,maxx,minx,maxy,miny):
    """
    SUMMARY
    This changes the weights of a creature to react to nearby danger.

    PARAMETERS
    chancetoreact (float): Between 0-1, the chance to react
    weights (list): A list of length 5 with the movement weights
    detections (list): A list of dangerous points detected in 4 directions
    xpos (int): Current x position
    ypos (int): Current y position
    maxx (int): The max x position in the simulation
    minx (int): The min x position in the simulation
    maxy (int): The max y position in the simulation
    miny (int): The min y position in the simulation

    RETURNS
    reactweights (list): A list of the new move weights
    """
    reactweights=[0 for _ in range(len(weights))]
    #fixes chancetoreact
    if chancetoreact>1: chancetoreact=1
    elif chancetoreact<0: chancetoreact=0
    #if it reacts, output different weights, otherwise output old weights
    if np.random.choice([True, False], p=[chancetoreact, 1-chancetoreact]):
        ordertochange=[]
        #check distances
        dist=[]
        for i in detections:
            #only if point not empty
            if len(i)>0:
                dist.append(((xpos-i[0])**2+(ypos-i[1])**2)**.5)
            else:
                #if no point, then no detection so put distance further away than any detections
                dist.append(abs(maxx)+abs(minx)+abs(maxy)+abs(miny))
        #make independent copy
        distcopy=[i for i in dist]
        #put in ascending order
        dist.sort()
        #get order of indeces
        for i in dist:
            indexcheck=[j for j, k in enumerate(distcopy) if k == i]
            #if tie put in random order
            np.random.shuffle(indexcheck)
            for j in indexcheck:
                if j not in ordertochange:
                    ordertochange.append(j)
        #make new weights
        #stay chance unaffected at least until normalization
        reactweights[0]=weights[0]
        #move sum of all chances except stay to the furthest
        addsum=0
        for i in range(len(ordertochange)):
            addsum+=weights[ordertochange[i]+1]
            if i == len(ordertochange)-1:
                reactweights[ordertochange[i]+1]=addsum
        return reactweights
    else:
        reactweights=weights
    return reactweights