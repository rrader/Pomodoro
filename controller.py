import wx
from threading import Thread

from state import PomodoroState
from time import sleep

class Timer(Thread):
    ok = True
    def __init__(self, delay, func):
        Thread.__init__(self)
        self.__func = func
        self.__delay = delay
    
    def run(self):
        while True:
            if self.ok:
                sleep(self.__delay)
                self.__func(self)

class PomodoroController(object):
    def __init__(self, view):
        self.state = PomodoroState()
        self.__view = view
        self.t1 = Timer(1, self.UpdateTimer)
        self.t2 = Timer(60, self.DecrementTimer)
        self.RunTimers()
    
    def UpdateTimer(self, t):
        self.__view.update_ui()
        
    def DecrementTimer(self, t):
        self.state.minutes -= 1
        self.state.text = str(self.state.minutes)+" min"
        if self.state.minutes <= 0:
            self.StopTimers()
    
    def RunTimers(self):
        self.t1.start()
        self.t2.start()
        self.state.active = True
    
    def StartTimers(self, toggle=True):
        self.t1.ok = toggle
        self.t2.ok = toggle
        self.state.active = toggle
        
    def ToggleState():
        pass