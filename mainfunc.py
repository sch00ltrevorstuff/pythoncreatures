import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import PolyCollection
import movefuncs as mf
import creatureclass as crc
import passon as po
import plotfuncs as pf
import checksurvivearea as csa

def movementsimfunc(maxx=30,minx=-30,maxy=30,miny=-30,startcreatnum=1,steps=300,generations=21,mutationrate=.25,reproductionrate=2,
                    graphcheck=5,startingchance=[.2,.2,.2,.2,.2],amplitude=1, creatcap=1000000):
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
    """
    #initialize lists
    creatnum=startcreatnum
    creatures=[]
    meanchances=[]
    devchances=[]
    meanstepssurvived=[]
    devstepssurvived=[]
    numberofcreats=[]
    chances=[] #list of lists of weights for the creatures
    #adds death zones
    verts=[[[30,20],[20,20],[20,30],[30,30]],[[-30,-20],[-20,-20],[-20,-30],[-30,-30]]]

    for i in range(startcreatnum):
        chances.append(startingchance)


    for g in range(generations):
        print('------------------------------------------------------------------------------------------------------------')
        print("Now starting generation " + str(g) + " with estimated time to finish " + str(int(creatnum*.025*(steps/300))) + " seconds.")
        gensurvivors=creatnum

        numberofcreats.append(creatnum)
        #to keep track of when creatures die
        stepssurvived=[]

        #creates list of allowed points
        invalidpoints=csa.invalidsubzones(verts)
        validpoints=csa.validzones(maxx, minx, maxy, miny, invalidpoints)

        for c in range(creatnum):
            #creates list of objects of class Creat and gives number and amplitude
            creatures.append(crc.Creat(c, amplitude))
            #assigns weights to the creatures
            creatures[c].chances(weight=chances[c])

            stepssurvived.append(0)

            for s in range(steps):
                    #start step at last step's last position
                    xpos=creatures[c].xtrack[s]
                    ypos=creatures[c].ytrack[s]
                    #if still alive, if death stays put
                    if creatures[c].alive==True:
                        #assigns weights and chooses move function
                        movefunc=mf.funcchoose(creatures[c].weights)(amplitude, xpos, ypos)
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

        print('The average weights for generation ' + str(g) + ' are ' + str(np.mean(chances, axis=0)))
        print('The standard deviation is ' + str(np.std(chances, axis=0)))
        print('Survivors of this generation: ' + str(gensurvivors) + '/' + str(creatnum))
        print('------------------------------------------------------------------------------------------------------------')
        meanchances.append(np.mean(chances, axis=0))
        devchances.append(np.std(chances, axis=0))

        meanstepssurvived.append(np.mean(stepssurvived, axis=0))
        devstepssurvived.append(np.std(stepssurvived, axis=0))

        if (g%graphcheck==0 or g==generations-1) and creatnum<50 and creatnum>0 and g!=0:
            print('------------------------------------------------------------------------------------------------------------')
            print("Now animating generation " + str(g) + " with estimated time to finish " + str(int(15+creatnum*(steps/300))) + " seconds.")
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
            txt_steps=axis.text(minx, maxy+2, '', fontsize=10)
            txts_creaturesstatus=[]
            for c in range(creatnum):
                txts_creaturesstatus.append(plt.text(maxx+1, maxy-3-7*c, '', fontsize=10))
            def animate(i):
                for c in range(len(lines)):
                    txt_steps.set_text('Gen: ' + str(g) + '\n' + 'Step: ' + str(i) + '\n' + 'Survivors of this generation: ' + str(gensurvivors) + '/' + str(creatnum))
                    txts_creaturesstatus[c].set_text(str(c)+': '+ str(creatures[c].life[i]))
                    lines[c].set_label(c)
                    #color based on traits, probably not right but it yields good enough results
                    stay=creatures[c].weights[0] #more likely to go up, the more red
                    up=creatures[c].weights[1] #more likely to go up, the more red
                    right=creatures[c].weights[2] #more likely to go right, the more purple
                    down=creatures[c].weights[3] #more likely to go down, the more cyan
                    left=creatures[c].weights[4] #more likely to go left, the more yellow
                    #R=(2*up+.5*right+.5*left-2*down)
                    R=(up-down+1)/2 #more likely to go up, the more red
                    #if R<0: R=0
                    #if R>1: R=1
                    #G=(.5*down+2*left-.5*up-.5*right)
                    G=(right-left+1)/2 #more likely to go right, the more green
                    #if G<0: G=0
                    #if G>1: G=1
                    #B=(2*down+.5*right+.5*left-2*up)
                    B=stay #more likely to stay, the more blue
                    #if B<0: B=0
                    #if B>1: B=1
                    lines[c].set_color((R,G,B))
                    lines[c].set_data(creatures[c].xtrack[:i], creatures[c].ytrack[:i])
                plt.legend()
                return txt_steps, txts_creaturesstatus, lines
            anim = animation.FuncAnimation(fig, animate, frames = steps+1, interval = 20, repeat=False)
            anim.save('Generation ' + str(g) + '.gif')

        #get new chances from surviving creats
        allnewchances=[]
        for c in creatures:
            #checks if alive
            if c.alive==True:
                for i in range(reproductionrate):
                    allnewchances.append(po.newchances(c.weights, mutationrate=mutationrate))
        chances=allnewchances
        #new number of creats
        creatnum=len(allnewchances)
        if creatnum>creatcap: creatnum=creatcap
        #clears creats list
        creatures=[]

    meanchanceotherway=[[] for i in range(len(startingchance))]
    devchanceotherway=[[] for i in range(len(startingchance))]
    for i in range(len(meanchances)):
        if type(meanchances[i])==np.float64: #for if all creats died
            meanchances[i]=np.array([0,0,0,0,0])
    for i in range(len(devchances)):
        if type(devchances[i])==np.float64:
            devchances[i]=np.array([0,0,0,0,0])
    meanchancesreshaped=[i.reshape(len(startingchance)) for i in meanchances]
    devchancesreshaped=[i.reshape(len(startingchance)) for i in devchances]
    for i in range(len(startingchance)):
        for j in range(len(meanchancesreshaped)):
            meanchanceotherway[i].append(meanchancesreshaped[j][i])
            devchanceotherway[i].append(devchancesreshaped[j][i])

    pf.sumplots(meanchanceotherway, devchanceotherway, meanstepssurvived ,devstepssurvived , numberofcreats)

    plt.tight_layout()
    plt.savefig('Summary Plot')
    plt.show()
    print('Completed')