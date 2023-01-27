import pygame
from vector import Vector2
from constants import *

class Text(object):
    def __init__(self, text, color, x, y, size, time = None, id = None, visible = True):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector2(x,y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setupFont("PressStart2P-Regular.ttf")
        self.createLabel()

    #sets our deisred font and size
    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)
    
    #sets the lable that we create
    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)

    #creates the lable of the text we entered
    def setText(self, newtext):
        self.text = str(newtext)
        self.createLabel()
    
    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True
    
    def render(self, screen):
        if self.visible:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x,y))

class TextGroup(object):
    def __init__(self):
        self.nextid = 10
        self.alltext = {}
        self.setupText()
        self.showText(READYTXT)
    
    #adds the Score and Level text to a dictionary
    #We don't need to know their id's because they
    #will conststnly be on the screen, so this method 
    #creates if for them
    def addText(self, text, color, x, y, size, time = None, id = None):
        self.nextid += 1
        self.alltext[self.nextid] = Text(text, color, x, y, size, time = time, id = id)
        return self.nextid
    
    #removes text from the dictionary
    def removeText(self, id):
        self.alltext.pop(id)

    #sets up and creates all the text we will need
    #for the game
    def setupText(self):
        size = TILEHEIGHT
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, size)
        self.alltext[LEVELTXT] = Text(str(1).zfill(3),WHITE, 23*TILEWIDTH, TILEHEIGHT, size)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 11.25*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 10.625*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 10*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.addText("SCORE", WHITE, 0,0, size)
        self.addText("Level", WHITE, 23*TILEWIDTH, 0, size)

    #checks to see if text needs to be updated or remvoed
    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.removeText(tkey)

    #changes the visiblity status of text to true       
    def showText(self, id):
        self.hideText()
        self.alltext[id].visible = True

    #changes the visibility status of the text to false
    def hideText(self):
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    #updates the score text on the screen
    def updateScore(self, score):
        self.updateText(SCORETXT, str(score).zfill(8))

    #updates the level we are on
    def updateLevel(self, level):
        self.updateText(LEVELTXT, str(level + 1).zfill(3))
    
    #updates any text in general, to a new value
    def updateText(self, id, value):
        if id in self.alltext.keys():
            self.alltext[id].setText(value)

    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)