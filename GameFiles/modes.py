from constants import *

#Defines the modes that objects are in
#most of these will be used by ghosts   
class MainMode(object):    
    def __init__(self):
        self.timer = 0
        self.scatter()

    #every update for modes is based on a timing sequence
    #the first seven seconds is in scatter mode, then 20 seconds
    #in chase mode and then back again
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()
        
    #MODE when each ghost tries to go each corner of the map
    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    #mode where they try to chase pacman
    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0

#controls which mode a ghost is in
class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity

    #when pacman eats a power pellet
    #the mode the ghosts are in swtich
    def setFreightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0

    
    #Will switch the mode's depending on how long
    #a mode as been active
    def update(self, dt):
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.entity.normalMode()
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            if self.entity.node == self.entity.spawnNode:
                self.entity.normalMode()
                self.current = self.mainmode.mode
    
    #will change the mode to spawn mode whenever a ghost is 
    #eaten
    def setSpawnMode(self):
        if self.current is FREIGHT:
            self.current = SPAWN