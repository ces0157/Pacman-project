import pygame
from constants import *
import numpy as np

#height and width of sprite sheeet
#is 16 x 16 tiles
BASETILEWIDTH = 16
BASETILEHEIGHT = 16

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet.png").convert() #loads our sheet
        transcolor = self.sheet.get_at((0,0))  #ignores the background color when drawing to the screen
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH) #modifies width based on the size of our spritesheet
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT) #modifies height based on the size of our spiretsheet
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
    
    #extracts an image from the spirte sheet
    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x,y,width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

#used to easily refrence the pacman sprites
class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()

    #Retrieves the starting sprite image
    def getStartImage(self):
        return self.getImage(8,0)
    
    #retreives image based on row columns or x y position of
    #the sprite image
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2 *TILEHEIGHT)


class GhostSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6} ##sets the column position
        self.entity = entity
        self.entity.image = self.getStartImage()

    #Provides a default image based on row column position
    def getStartImage(self):
        return self.getImage(self.x[self.entity.name],4)

    #Gets the image of a sprite based on row columns position
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x,y, 2*TILEWIDTH, 2*TILEHEIGHT)

class FruitSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()

    #provides a default image based on row and columns
    def getStartImage(self):
        return self.getImage(16,8)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2 *TILEHEIGHT)

class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.resetLives(numlives)
    
    #removes the "life" or pacman image off the screen
    #when he dies
    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)
    
    #Will append the images to a list based on the number of lives
    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0,0))
    
    #Gets the row and columns and returns the image
    def getImage(self, x, y):
        return Spritesheet.getImage(self,x,y, 2*TILEWIDTH, 2*TILEHEIGHT)

class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)
    
    #gets the sprite image based on row, column position
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH / 2, TILEHEIGHT / 2)
    
    #loads the txt file
    def readMazeFile(self, mazeFile):
        return np.loadtxt(mazeFile, dtype = '<U1')
    
    #goes throught the maze file and roatation file and
    #finds places where spirtes need to be located and
    #at what degree
    #based on if they are digits or not.
    #will then construct/show to screen
    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x,y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10,8)
                    background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))

        return background
    
    #roates the spirte based off of data from the 
    #rotate.txt file
    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value*90)
