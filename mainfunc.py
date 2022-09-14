import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import movefuncs as mf
import creatureclass as crc
import passon as po
import plotfuncs as pf
import checksurvivearea as csa

def movementsimfunc(maxx=30,minx=-30,maxy=30,miny=-30,startcreatnum=1,steps=300,generations=21,mutationrate=.25,reproductionrate=2,
                    graphcheck=5,startingchance=[.2,.2,.2,.2,.2],amplitude=1):
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

    for i in range(startcreatnum):
        chances.append(startingchance)


    for g in range(generations):
        gensurvivors=creatnum

        numberofcreats.append(creatnum)
        #to keep track of when creatures die
        stepssurvived=[]

        #creates list of allowed points
        validpoints=csa.validzones(maxx, minx, maxy, miny)

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

        print('-------------------------------------------------------------')
        print('The average weights for generation ' + str(g) + ' are ' + str(np.mean(chances, axis=0)))
        print('The standard deviation is ' + str(np.std(chances, axis=0)))
        print('Survivors of this generation: ' + str(gensurvivors) + '/' + str(creatnum))
        print('-------------------------------------------------------------')
        meanchances.append(np.mean(chances, axis=0))
        devchances.append(np.std(chances, axis=0))

        meanstepssurvived.append(np.mean(stepssurvived, axis=0))
        devstepssurvived.append(np.std(stepssurvived, axis=0))

        if (g%graphcheck==0 or g==generations-1) and creatnum<50 and creatnum>0 and g!=0:
            fig = plt.figure()
            axis = plt.axes(xlim=(minx, maxx), ylim=(miny, maxy))
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
        #clears creats list
        creatures=[]

    meanchanceotherway=[[] for i in range(len(startingchance))]
    devchanceotherway=[[] for i in range(len(startingchance))]
    for i in range(len(meanchances)):
        if type(meanchances[i])==np.float64:
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