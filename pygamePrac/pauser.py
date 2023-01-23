class Pause(object):
    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        self.pauseTime = None
        self.func = None
    
    #used for pause events that are timed. Such as transitions
    #to other levels
    def update(self, dt):
        if self.pauseTime is not None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                self.timer = 0;
                self.paused = False
                self.pauseTime = None
                return self.func
        return None
    
    #Sets the length of time something is paused
    def setPause(self, playerPaused = False, pauseTime = None, func = None):
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        self.flip()

    #flips the status of pause to either true or false
    def flip(self):
        self.paused = not self.paused
