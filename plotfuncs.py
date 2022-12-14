import numpy as np
import matplotlib.pyplot as plt

def sumplots(meanchanceotherway, meanstepssurvived,devstepssurvived, meanamp, meanvs, meanctr,numberofcreats):
    """
    SUMMARY
    This function creates the plots to show at the end of the simulation.

    PARAMETERS
    meanchanceotherway (list): This is a list of lists of the average weight for each choice per generation
    meanstepssurvived (list): This is a list of the average number of steps the creatures survived each generation
    devstepssurvived (list): This is a list of the standard deviation of the number of steps the creatures survived each generation
    meanamp (list): This is a list of the mean amplitudes of creatures per generation
    meanvs (list): This is a list of the mean vision strength of creatures per generation
    meanctr (list): This is a list of the mean chance to react of creatures per generation
    numberofcreats (list): This is a list of the number of creatures in each generation

    RETURNS
    axis (numpy.ndarray): The plots to summarize what happened over all of the generations
    """    
    figure, axis = plt.subplots(2, 2)
    x=np.linspace(0,len(meanchanceotherway[0]),len(meanchanceotherway[0]))
    axis[0,0].plot(x,meanchanceotherway[0], label='Stay put', color='Blue')
    axis[0,0].plot(x,meanchanceotherway[1], label='Move up', color='Red')
    axis[0,0].plot(x,meanchanceotherway[2], label='Move right', color='Green')
    axis[0,0].plot(x,meanchanceotherway[3], label='Move down', color='Purple')
    axis[0,0].plot(x,meanchanceotherway[4], label='Move left', color='Orange')
    axis[0,0].plot(x,meanctr, label='Chance to react', color='Black')

    axis[0,1].plot(x,meanamp, label='Amplitude', color='Blue')
    axis[0,1].plot(x,meanvs, label='Vision Strength', color='Red')

    #convert to array for subtraction
    meanstepssurvived=np.array(meanstepssurvived)
    devstepssurvived=np.array(devstepssurvived)
    axis[1,0].plot(x, meanstepssurvived, label='Mean')
    axis[1,0].fill_between(x, meanstepssurvived - devstepssurvived, meanstepssurvived + devstepssurvived, color='b', alpha=0.2, label='Standard Deviation')

    axis[1,1].plot(x, numberofcreats, label='Number of Creatures')

    axis[0,0].set_xlabel('Generation')
    axis[0,1].set_xlabel('Generation')
    axis[1,0].set_xlabel('Generation')
    axis[1,1].set_xlabel('Generation')

    axis[0,0].set_ylabel('Weight')
    axis[0,0].set_title('Average Weights')
    axis[0,1].set_title('Amplitude and Vision Strength')
    axis[0,1].set_ylabel('Distance')
    axis[0,0].set_ylim((0,1))
    axis[1,0].set_ylabel('Steps Survived')
    axis[1,0].set_title('Mean Steps Survived')
    axis[1,1].set_ylabel('Number of Creatures')
    axis[1,1].set_title('Number of Creatures')

    axis[0,0].legend(fontsize='x-small')
    axis[0,1].legend(fontsize='x-small')
    axis[1,0].legend(fontsize='x-small')
    axis[1,1].legend(fontsize='x-small')
    return axis