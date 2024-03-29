import pygame
from vector import Vector2
from constants import*
import numpy as np

#Both of these classes below are the foundation of the game
#It enables objects to move and the direction they can go in
#also specfies certain nodes/locations to do specifc things
class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x,y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT: None, PORTAL: None}
        self.access = {UP:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       DOWN:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       LEFT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       RIGHT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}
    
    #method used to help visualize our nodes/maze. Will
    #not be used when the game is done. Just for us to see how our game is being mapped out
    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start =  self.position.asTuple()
                line_end =  self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)
    
    #Denies access to a particular node
    #For example, pacman not being able to access
    #the ghost's home base
    def denyAccess(self, direction, entity):
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    #allows access to a paritcular node
    def allowAccess(self, direction, entity):
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)
    


#Creates all the Nodes, intead of having to init every single one, just like
#the GhostGroup class. Nodes are read in based off of input from a txt file. This class
#will help define those methods
class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodesLut = {}
        self.nodeSymbols = ['+', 'P','n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.homekey = None
    

    #reads and loads the mazefield to create our nodes
    #and maze map
    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    #creates a node from the maze.txt file based on position
    #in rows and columns
    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLut[(x,y)] = Node(x,y)

    #converts a row and columns to an actual pixel value on the screen
    def constructKey(self, x, y):
        return x*TILEWIDTH, y*TILEHEIGHT

    #when two nodes are found to be connected horizontally (when ... is found)
    #from the maze.txt. file, their neighbors are updated
    def connectHorizontally(self, data, xoffset = 0, yoffset = 0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLut[key].neighbors[RIGHT] = self.nodesLut[otherkey]
                        self.nodesLut[otherkey].neighbors[LEFT] = self.nodesLut[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None
    
    #when two nodes are found to be connected vertically
    #from the maze.txt. file, their neighbors are updated
    def connectVertically(self,data, xoffset = 0, yoffset = 0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row + yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLut[key].neighbors[DOWN] = self.nodesLut[otherkey]
                        self.nodesLut[otherkey].neighbors[UP] = self.nodesLut[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    #creaetes the starting location of our ghosts
    #We add this in since the maze file only uses
    #integers as columns and not floating points
    def createHomeNodes(self, xoffset, yoffset):
        homedata = np.array([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])
        self.createNodeTable(homedata, xoffset, yoffset)
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset + 2, yoffset)
        return self.homekey

    #connects the 'home base' to the rest of the maze
    def connectHomeNodes(self, homekey, otherkey, direction):
        key = self.constructKey(*otherkey)
        self.nodesLut[homekey].neighbors[direction] = self.nodesLut[key]
        self.nodesLut[key].neighbors[direction*-1] = self.nodesLut[homekey]

    #Defines the nodes in terms of pixels on the screen. Useful for sizing purposes
    def getNodeFromPixels(self, xpixel, ypixel):
        if(xpixel, ypixel) in self.nodesLut.keys():
            return self.nodesLut[(xpixel, ypixel)]
        return None
    
    #Defines the nodes in term of tiles on the screen, Useful for sizing purposes
    def getNodeFromTiles(self, col, row):
        x,y = self.constructKey(col, row)
        if (x,y) in self.nodesLut.keys():
            return self.nodesLut[(x,y)]
        return None
    
    #tells use what node pacman is going to start out on
    def getStartTempNode(self):
        nodes = list(self.nodesLut.values())
        return nodes[0]

    #renders the node group to the screen
    def render(self, screen):
        for node in self.nodesLut.values():
            node.render(screen)
    
    #If two nodes exist within this method, then we connect
    #them to signify a "portal". 
    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLut.keys() and key2 in self.nodesLut.keys():
            self.nodesLut[key1].neighbors[PORTAL] = self.nodesLut[key2]
            self.nodesLut[key2].neighbors[PORTAL] = self.nodesLut[key1]

    #gets the node from its row column position
    #if a node exits, then access will be denied
    def denyAccess(self, col, row, direction, entity):
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.denyAccess(direction, entity)
    
    #gets the node from its row column positino
    #if a node exits, then access will be allowed
    def allowAccess(self, col, row, direction, entity):
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.allowAccess(direction, entity)
    
    #Adds the node to the deny list
    def denyAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.denyAccess(col, row, direction, entity)

    #Adds the node to the access list
    def allowAccessList(self, col, row, direction, entites):
        for entity in entites:
            self.allowAccess(col, row, direction, entity)
    #denies an entity to the home area
    def denyHomeAccess(self, entity):
        self.nodesLut[self.homekey].denyAccess(DOWN, entity)
    #gives home access to an entity
    def allowHomeAccess(self, entity):
        self.nodesLut[self.homekey].allowAccess(DOWN, entity)

    def denyHomeAccessList(self, entities):
        for entity in entities:
            self.denyHomeAccess(entity)

    def allowHomeAccessList(self, entities):
        for entity in entities:
            self.allowHomeAccess(entity)