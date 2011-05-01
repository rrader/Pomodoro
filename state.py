# -*- coding: utf-8 -*-

from singleton import Singleton

class PomodoroState(object): #singleton
    __metaclass__ = Singleton

    def __init__(self):
        self._percent = 1.0
        self._minutes = 25
    
    StateNoState = 0
    StateInPomodoro = 1
    StateInRest = 2
    StateWaitingPomodoro = 3
    StateWaitingRest = 4
    StatePomodoroKilled = 5
    
    debug = False
    text = ""
    caption = ""
    active = StateNoState
    max_minutes = 25
    inwork = False
    times = 0
    
    def inc_times(self):
        self.times += 1
    
    def getp(self):
        return self._percent

    def setp(self, v):
        self._percent = v
        self._minutes = int(v*self.max_minutes)
        
    def delp(self):
        del self._percent
        
    percent = property(getp, setp, delp, "I'm the 'percent' property.")
    
    def getm(self):
        return self._minutes

    def setm(self, v):
        self._minutes = v
        if self.max_minutes==0:
            self._percent = 1
        else:
            self._percent = float(self._minutes)/self.max_minutes
        
    def delm(self):
        del self._minutes
        
    minutes = property(getm, setm, delm, "I'm the 'minutes' property.")
        
class PomodoroStateProxy(object):
    def __init__( self ):
        self.__subject = PomodoroState()
    def __getattr__( self, name ):
        return getattr( self.__subject, name )
   