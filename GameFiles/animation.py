from constants import *

#This class provides a general animation  framework for obects.
#It uses frame and frame speed to determine when an animation
#should occur
class Animator(object):
    def __init__(self, frames = [], speed = 20, loop = True):
        self.frames = frames
        self.current_frame = 0
        self.speed = speed
        self.loop = loop
        self.dt = 0
        self.finished = False
    
    #resets the the current frame we are using
    def reset(self):
        self.current_frame = 0
        self.finished = False

    #updates through the frame list at the speed the user has chosen
    def update(self, dt):
        if not self.finished:
            self.nextFrame(dt)
        if self.current_frame == len(self.frames):
            if self.loop:
                self.current_frame = 0
            else:
                self.finished = True
                self.current_frame = -1
        return self.frames[self.current_frame]
    
    #increments the currentFrame counter
    #used to access the next frame in the frame list
    def nextFrame(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1
            self.dt = 0

