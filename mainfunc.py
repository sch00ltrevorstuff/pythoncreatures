import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import movefuncs as mf
import creatureclass as crc
import passon as po
import plotfuncs as pf
import checksurvivearea as csa
import sight

def movementsimfunc(maxx=30,minx=-30,maxy=30,miny=-30,startcreatnum=1,steps=300,generations=21,mutationrate=.15,reproductionrate=2,
                    graphcheck=5,startingchance=[.2,.2,.2,.2,.2],startingamplitude=1,startingvisionstrength=0,
                    startingchancetoreact=0, creatcap=1000000, verts=[[[30,30],[29,30],[30,29]]], randomstart=False):
    """
    SUMMARY
    This is the main function of the simulation. Running it will run the simulation, create gifs of generations, and create summary plots.

    PARAMETERS
    maxx (int): Furthest a creature can go right
    minx (int): Furthest a creature can go left
    maxy (int): Furthest a creature can go up
    miny (int): Furthest a creature can go down
    startcreatnum (int): How many creatures in gen 0
    steps (int): How many steps per generation
    generations (int): How many generations there will be including generation 0
    mutationrate (float): MUST BE BELOW 1 AND GREATER THAN 0. The probability per chance that it will change
    reproductionrate (int): How many creatures will be created from each survivor
    graphcheck (int): How many generations between each animation, last will always be animated if under 50 creatures
    startingchance (list): The probabilities for what the creature will do in the form of [nothing, up, right, down, left]
    amplitude (int): How far the creature will move if it moves
    creatcap (int): Maxium nummber of creatures allowed.
    verts (list): The list of lists of vertices of polygons that are out of bounds
    randomstart (bool): If the traits for creatures will be random at gen 0
    """
    creatnum=startcreatnum
    #initialize lists
    creatures, meanchances,meanstepssurvived,devstepssurvived,meanamp,meanvs,meanctr,numberofcreats=[],[],[],[],[],[],[],[]
    #list of lists of weights for the creatures
    if randomstart==False:
        chances=[startingchance for _ in range(startcreatnum)]
        amps=[startingamplitude for _ in range(startcreatnum)]
        vss=[startingvisionstrength for _ in range(startcreatnum)]
        ctrs=[startingchancetoreact for _ in range(startcreatnum)]
    else:
        chances=[list(np.random.uniform(size=5)) for _ in range(startcreatnum)]
        chances=[[j/sum(i) for j in i] for i in chances]
        amps=[np.random.randint(0,int(((abs(minx)+abs(maxx))**2+(abs(miny)+abs(maxy))**2)**.5)) for _ in range(startcreatnum)]
        vss=[np.random.randint(0,int(((abs(minx)+abs(maxx))**2+(abs(miny)+abs(maxy))**2)**.5)) for _ in range(startcreatnum)]
        ctrs=[np.random.uniform() for _ in range(startcreatnum)]
    #adds death zones

    for g in range(generations):
        print('------------------------------------------------------------------------------------------------------------')
        print("".join(["Now starting generation ", str(g)]))
        gensurvivors=creatnum

        numberofcreats.append(creatnum)
        #to keep track of when creatures die
        stepssurvived=[]

        #creates list of allowed points
        invalidpoints=csa.invalidsubzones(verts)
        validpoints=csa.validzones(maxx, minx, maxy, miny, invalidpoints)

        for c in range(creatnum):
            #creates list of objects of class Creat and gives number
            creatures.append(crc.Creat(c))
            #assigns weights and traits to the creatures
            creatures[c].chances(weight=chances[c])
            creatures[c].amplitude=amps[c]
            creatures[c].visionstrength=vss[c]
            creatures[c].chancetoreact=ctrs[c]
            stepssurvived.append(0)
            if randomstart:
                creatures[c].xtrack[0]=np.random.randint(-maxx,maxx+1)
                creatures[c].ytrack[0]=np.random.randint(-maxy,maxy+1)

            for s in range(steps):
                print("Simulating step: " + str(s) + "\t for creature " + str(c), end='\r')
                #start step at last step's last position
                xpos=creatures[c].xtrack[s]
                ypos=creatures[c].ytrack[s]
                #if still alive, if dead stays put
                if creatures[c].alive==True:
                    #assigns weights and chooses move function
                    #using vision strength to look for danger, then react
                    detections=sight.looking(creatures[c].visionstrength,xpos,ypos,maxx,minx,maxy,miny,validpoints)
                    reactweights=sight.react(creatures[c].chancetoreact,creatures[c].weights, detections, xpos, ypos,maxx,minx,maxy,miny)
                    movefunc=mf.funcchoose(reactweights)(creatures[c].amplitude, xpos, ypos)
                    #the point to check if allowed
                    pointcheck=[movefunc[0], movefunc[1]]
                    #checks if went to not allowed point, if so then dies and stays put, else then move
                    if pointcheck not in validpoints:
                        creatures[c].death()
                        gensurvivors=gensurvivors-1
                        creatures[c].changex(xpos)
                        creatures[c].changey(ypos)
                    else:
                        creatures[c].survive()
                        stepssurvived[c]+=1
                        creatures[c].changex(movefunc[0])
                        creatures[c].changey(movefunc[1])
                else:
                    creatures[c].death()
                    creatures[c].changex(xpos)
                    creatures[c].changey(ypos)

        print("".join(["The average weights for generation ", str(g), " are ", str(np.mean(chances, axis=0))]))
        print("".join(["The average weights for generation ", str(g), " are Amp: ", str(np.mean(amps)), " VS: ", str(np.mean(vss)), " CTR: ", str(np.mean(ctrs))]))
        print("".join(["Survivors of this generation: ", str(gensurvivors), "/", str(creatnum)]))
        print('------------------------------------------------------------------------------------------------------------')
        meanchances.append(np.mean(chances, axis=0))
        meanstepssurvived.append(np.mean(stepssurvived))
        devstepssurvived.append(np.std(stepssurvived))
        meanamp.append(np.mean(amps))
        meanvs.append(np.mean(vss))
        meanctr.append(np.mean(ctrs))

        if (g%graphcheck==0 or g==generations-1) and creatnum<50 and creatnum>0 and g!=0:
            print('------------------------------------------------------------------------------------------------------------')
            print("".join(["Now animating generation ", str(g)]))
            print('------------------------------------------------------------------------------------------------------------')

            fig = plt.figure()
            axis = plt.axes(xlim=(minx, maxx), ylim=(miny, maxy))

            #######################################################################################################
            #Adds zone to gif
            poly = csa.getpoly(verts)
            axis.add_collection(poly)
            #######################################################################################################

            #lines and text class of matplotlib
            lines=[plt.plot([],[])[0] for _ in range(creatnum)]
            spoints=[]
            txt_steps=axis.text(minx, maxy+2, '', fontsize=10)
            for c in range(creatnum):
                spoints.append(plt.scatter(0,0, creatures[c].amplitude*10+1))
            def animate(i):
                for c in range(len(lines)):
                    print("Making frame: " + str(i), end='\r')
                    txt_steps.set_text('Gen: ' + str(g) + '\n' + 'Step: ' + str(i) + '\n' + 'Survivors of this generation: ' + str(gensurvivors) + '/' + str(creatnum))
                    #color based on traits, probably not right but it yields good enough results
                    stay=creatures[c].weights[0]
                    up=creatures[c].weights[1]
                    right=creatures[c].weights[2]
                    down=creatures[c].weights[3]
                    left=creatures[c].weights[4]
                    R=(up-down+1)/2 #more likely to go up, the more red
                    G=(right-left+1)/2 #more likely to go right, the more green
                    B=stay #more likely to stay, the more blue
                    lines[c].set_color((R,G,B))
                    lines[c].set_data(creatures[c].xtrack[:i], creatures[c].ytrack[:i])
                    if creatures[c].life[i] == 'Alive':
                        spoints[c].set_color((R,G,B))
                    else:
                        spoints[c].set_color((0,0,0))
                    spoints[c].set_offsets([creatures[c].xtrack[i], creatures[c].ytrack[i]])
                return txt_steps, lines, spoints
            anim = animation.FuncAnimation(fig, animate, frames = steps+1, interval = 20, repeat=False)
            anim.save('Generation ' + str(g) + '.gif')

        #get new chances from surviving creats
        allnewchances=[]
        allnewamps=[]
        allnewvss=[]
        allnewctrs=[]
        for c in creatures:
            #checks if alive
            if c.alive==True:
                for i in range(reproductionrate):
                    allnewchances.append(po.newchances(c.weights, mutationrate=mutationrate))
                    newamp,newvs,newctr=po.newattr(c.amplitude,c.visionstrength,c.chancetoreact,mutationrate)
                    allnewamps.append(newamp)
                    allnewvss.append(newvs)
                    allnewctrs.append(newctr)
        chances=allnewchances
        amps=allnewamps
        vss=allnewvss
        ctrs=allnewctrs
        #new number of creats
        creatnum=len(allnewchances)
        #if too many creatures, then take first 20
        if creatnum>creatcap:
            creatnum=creatcap
        #clears creats list
        creatures=[]
    #reshape and correct null values
    meanchanceotherway=[[] for i in range(len(startingchance))]
    for i in range(len(meanchances)):
        if type(meanchances[i])==np.float64: #for if all creats died
            meanchances[i]=np.array([0,0,0,0,0])
    meanchancesreshaped=[i.reshape(len(startingchance)) for i in meanchances]
    for i in range(len(startingchance)):
        for j in range(len(meanchancesreshaped)):
            meanchanceotherway[i].append(meanchancesreshaped[j][i])
    for i in meanamp:
        if i>=0: pass
        else: i=0
    for i in meanvs:
        if i>=0: pass
        else: i=0
    for i in meanctr:
        if i>=0: pass
        else: i=0
    pf.sumplots(meanchanceotherway, meanstepssurvived, devstepssurvived, meanamp, meanvs, meanctr, numberofcreats)

    plt.tight_layout()
    plt.savefig('Summary Plot')
    plt.show()
    print('Completed')