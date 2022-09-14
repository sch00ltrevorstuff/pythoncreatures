class Creat:
    """
    SUMMARY
    The creature class to contain the information of a specific creature.

    ATTRIBUTES
    creatnum (int): Which number creature it is
    amplitude (int): How much the creature will move when it moves
    """
    def __init__(self, creatnum, amplitude):
        """
        SUMMARY
        This constructs the object, sets the creature as Alive, sets its position as the origin, and initializes lists.

        PARAMETERS
        creatnum (int): Which number creature it is
        amplitude (int): How much the creature will move when it moves
        """
        self.creatnum=creatnum
        self.amplitude=amplitude
        self.alive=True
        self.life=['Alive']
        self.weights=[]
        #These track where the creature has moved each step.
        self.xtrack=[0]
        self.ytrack=[0]
    def chances(self, weight):
        """
        SUMMARY
        This clears the weights list, then gives it the new weights.

        PARAMETERS
        weight (list): The chances that it uses to pick which action to do.
        """
        self.weights=[]
        self.weights=weight
    def changex(self, xpos):
        """
        SUMMARY
        This adds where the creature moved this step to the xtrack list.

        PARAMETERS
        xpos (int): The new x position.
        """
        self.xtrack.append(xpos)
    def changey(self, ypos):
        """
        SUMMARY
        This adds where the creature moved this step to the ytrack list.

        PARAMETERS
        ypos (int): The new y position.
        """
        self.ytrack.append(ypos)
    def survive(self):
        """
        SUMMARY
        This adds that the creature is alive to the list that keeps track of what steps the creature is alive.
        """
        self.life.append('Alive')
    def death(self):
        """
        SUMMARY
        This adds that the creature is dead to the list that keeps track of what steps the creature is alive.
        This also changes the creatures status of being alive to false.
        """
        self.life.append('Dead')
        self.alive=False