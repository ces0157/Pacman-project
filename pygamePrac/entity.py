import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint

class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {UP:Vector2(0,-1), DOWN:Vector2(0,1),
                            LEFT:Vector2(-1,0), RIGHT:Vector2(1,0), STOP:Vector2()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)

    #defines the starting node of an entity
    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()
    
    #Sets the position of the entity based
    #on a copy
    def setPosition(self):
        self.position = self.node.position.copy()

    
    #makes sure the direction that a ghost or 
    #pacman is going is a valid place
    def validDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False
    
    #if the direction is valid, based on user input (for pacman)
    #it will go to that next node
    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        
        return self.node

    #checks to see if the distance traveled is not 
    #farther than the actualy boundary or "node" we have 
    #set
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

     #Allows pacman to reverse the direction at any time
     #when opposite key is pressed
    def reverseDirection(self):
        self.direction *= -1
        temp =  self.node
        self.node = self.target
        self.target = temp

    # checks to see if the input is in the opposite direction
    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False
    
    #Pacman "speed" changes depening on the size of the maze
    #A biggermaze creates the illusion he is going slower
    #allows us to set a custom speed
    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16

    #renders the object to the screen
    def render(self, screen):
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)
    
    #when the object reaches a node it chooses a random
    #and valid direction to go
    def update(self, dt):
        self.position += self.directions[self.direction] *self.speed*dt

        if self.overshotTarget():
            self.node =  self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()
    
    #when an object has reached a node, it checks to see
    #what direction is can move in. If it can move in another direction
    #besides the one it came, it will chose so randomly. If not
    #then it goes the direction it came.
    def validDirections(self):
        directions = []
        for key in [UP,DOWN,LEFT,RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    #radonmy chooses a direction to go
    def randomDirection(self, directions):
        return directions[randint(0, len(directions)-1)]

    #Set's an object to be placed between two nodes, such
    # as pacman at the start, or when a fruit appears
    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0    
    
    #resets the node an entity is on. 
    #this will usually occur when pacman dies or advaces
    #to the next level. Also resets his visibility, direction
    #and speed
    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True
