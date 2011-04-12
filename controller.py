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
        while self.ok:
            sleep(self.__delay)
            self.__func(self)

class PomodoroController():
    
    def __init__(self):
        self.state = PomodoroState()
        t = Timer(1, self.OnTimer)
        t.start()
    
    def OnTimer(self, t):
        print "ok"
        
    