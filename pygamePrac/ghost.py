import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController

class Ghost(Entity):
    def __init__(self, node, pacman = None, blinky = None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node
    
    #gives our ghost a goal postion to reach.
    #Based on the current node it is at, it will
    #try to find the shortest distance to it
    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]


    #updates to see what mode the ghost is in.
    #this will change the desired/ objective position
    #of the ghost.
    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    #ghots tries to move to differnt corners
    def scatter(self):
        self.goal = Vector2()

    #ghots tries to chase pacman based on his position
    def chase(self):
        self.goal = self.pacman.position

    #when a ghosts enters freights mode,
    #it reduces its speed and goes in a randomDirection
    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection
    
    #when normalmode is called, it brings back the ghosts
    #speed and puts it pack into another mode
    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection

    #sets the goal to be the spawn postion
    #defined in the next method
    def spawn(self):
        self.goal = self.spawnNode.position

    #sets the Spawn node
    def setSpawnNode(self, node):
        self.spawnNode = node

    #checks tos see if we can even go back to the spawn
    #only way to start in spawn is at the beggining of the game
    #or being eaten by pacman in freighmode
    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    #reset's the ghosts attributes. Typically occurs after level
    #advacing or death of pacman
    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection


class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
       Ghost.__init__(self, node, pacman, blinky)
       self.name = BLINKY
       self.color = RED

class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK

    #Pinky's scatter goal is to be in the top left corner
    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    #Pink'ys chase goals is to tagert
    #4 tiles ahead of pacman and "sandwhich"
    #him in
    def chase(self):
        self.gaol = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL

    #Inky's scatter goals is the lower right corner of the maze
    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT *NROWS)

    #chases pacman based on his and blinky's position
    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2

class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORAGNE

    #clyde's scatter goal is the bottom left corner
    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT *NROWS)
    
    #If clyde is less than 8 tiles away he goes back to his scatter goal
    #If this is not the case then we treat it like Pinky's chase
    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node,pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    #Loops though the ghosts list
    def __iter__ (self):
        return iter(self.ghosts)
    
    def update(self, dt):
        for ghost in self:
            ghost.update(dt)

    def startFreight(self):
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)
    
    #updates the points of a ghost after pacman
    #has eaten one
    def updatePoints(self):
        for ghost in self:
            ghost.points *=2
    
    #resets the points back when pacman eats a new
    #power pellet
    def resetPoints(self):
        for ghost in self:
            ghost.points= 200
    
    def reset(self):
        for ghost in self:
            ghost.reset()
    
    #changes the physical visbilty of a ghost
    def hide(self):
        for ghost in self:
            ghost.visible = False
    
    #changes the physical visibilty of a ghost
    def show(self):
        for ghost in self:
            ghost.visible = True
    
    def render(self, screen):
        for ghost in self:
            ghost.render(screen)