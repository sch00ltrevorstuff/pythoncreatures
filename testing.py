class Dog:
    kind='animal'
    yee='haw'
    def __init__(self, name):
        self.name= name
        self.colors=[]
    def descolors(self, color):
        self.colors.append(color)

Fido=Dog('Fido')
Ruff=Dog('Ruff')
Fido.descolors('brown')
Fido.descolors('blue')
Ruff.descolors('black')

import numpy as np
import passon

x=passon.newchances([1,2,3,4],.5)
y=[i/sum(x) for i in x]
print(x)
print(y)

import checksurvivearea as csa
maxx=30
minx=-30
maxy=30
miny=-30
validpoints=csa.validzones(maxx, minx, maxy, miny)
print(validpoints)