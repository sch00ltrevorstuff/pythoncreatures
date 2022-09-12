class Creat:
    def __init__(self, creatnum, amplitude):
        self.creatnum=creatnum
        self.amplitude=amplitude
        self.alive=True
        self.life=['Alive']
        self.weights=[]
        self.xtrack=[0]
        self.ytrack=[0]
    def chances(self, weight):
        self.weights=[]
        self.weights=weight
    def changex(self, xpos):
        self.xtrack.append(xpos)
    def changey(self, ypos):
        self.ytrack.append(ypos)
    def survive(self):
        self.life.append('Alive')
    def death(self):
        self.life.append('Dead')
        self.alive=False