
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import movefuncs as mf
import creatureclass as crc
import passon as po

maxx=30
minx=-30
maxy=30
miny=-30
startcreatnum=1
steps=300
generations=21 #including generation 0
mutationrate=.25
reproductionrate=2
graphcheck=5 #how many generations between each animation, last will always be animated if under 50 creatures

creatnum=startcreatnum
creatures=[]
meanchances=[]
devchances=[]

#starting chances
startingchance=[.2,.2,.2,.2,.2]
amplitude=1
chances=[]
for i in range(startcreatnum):
    chances.append(startingchance)

for g in range(generations):
    gensurvivors=creatnum
    for c in range(creatnum):
        #creates list of objects of class Creat and gives number and amplitude
        creatures.append(crc.Creat(c, amplitude))
        #assigns weights to the creatures
        creatures[c].chances(weight=chances[c])

        for s in range(steps):
                #start step at last step's last position
                xpos=creatures[c].xtrack[s]
                ypos=creatures[c].ytrack[s]
                #if still alive, if death stays put
                if creatures[c].alive==True:
                    #assigns weights and chooses move function
                    movefunc=mf.funcchoose(creatures[c].weights)(amplitude, xpos, ypos)
                    #checks if go out of bounds, if so then dies and stays put, else then move
                    if movefunc[0]>maxx or movefunc[0]<minx or movefunc[1]>maxy or movefunc[1]<miny:
                        creatures[c].death()
                        gensurvivors=gensurvivors-1
                        creatures[c].changex(xpos)
                        creatures[c].changey(ypos)
                    else:
                        creatures[c].survive()
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

figure, axis = plt.subplots(1, 2)
x=np.linspace(0,generations,generations)
axis[0].plot(x,meanchanceotherway[0], label='Stay put')
axis[0].plot(x,meanchanceotherway[1], label='Move up')
axis[0].plot(x,meanchanceotherway[2], label='Move right')
axis[0].plot(x,meanchanceotherway[3], label='Move down')
axis[0].plot(x,meanchanceotherway[4], label='Move left')

axis[1].plot(x,devchanceotherway[0], label='Stay put')
axis[1].plot(x,devchanceotherway[1], label='Move up')
axis[1].plot(x,devchanceotherway[2], label='Move right')
axis[1].plot(x,devchanceotherway[3], label='Move down')
axis[1].plot(x,devchanceotherway[4], label='Move left')
axis[0].set_xlabel('Generation')
axis[1].set_xlabel('Generation')
axis[0].set_ylabel('Weight')
axis[0].set_title('Average Weights')
axis[1].set_title('Standard Deviation')
axis[0].set_ylim((0,1))
axis[1].set_ylim((0,1))
plt.legend()
plt.tight_layout()
plt.savefig('meanchances')
plt.show()
print('Completed')