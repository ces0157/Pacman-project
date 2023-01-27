import pygame
from vector import Vector2
from constants import *
import numpy as np

class Pellet(object):
    def __init__(self, row, column):
        self.name = PELLET
        self.position = Vector2(column*TILEWIDTH, row * TILEHEIGHT)
        self.color = WHITE
        self.radius = int(2* TILEWIDTH / 16)
        self.collideRadius = int(2*TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    #renders the pellets on the screen
    def render(self, screen):
        if self.visible:
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            p = self.position + adjust
            pygame.draw.circle(screen, self.color, p.asInt(), self.radius)

class PowerPellet(Pellet):
    def __init__(self, row, column):
        Pellet.__init__(self,row,column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0

    #Turns the super pellet "on and off" to
    #give it the effect of flashing
    def update(self, dt):
        self.timer += dt
        if self.timer >  self.flashTime:
            self.visible =  not self.visible
            self.timer = 0

class PelletGroup(object):
    def __init__(self, pelletfile):
        self.pelletList = []
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.numEaten = 0
    
    #go's through the list of powerpellets to
    #to update their "on and off" cycle
    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    #adds all the pellets from our maze file into a list
    def createPelletList(self, pelletfile):
        data = self.readPelletfile(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.','+']:
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)
    
    #reads and loads our maze file
    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype = '<U1')

    #Checks to see if all pellets are of the board
    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False
    
    #Renders all pellets to the screen
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)