# -*- coding: utf-8 -*-

class PomodoroState(object): #singleton

    class __impl(object):

        def __init__(self):
            self._percent = 1.0
            self._minutes = 25
        
        StateNoState = 0
        StateInPomodoro = 1
        StateInRest = 2
        StateWaitingPomodoro = 3
        StateWaitingRest = 4
        StatePomodoroKilled = 5
        
        text = ""
        caption = ""
        active = StateNoState
        max_minutes = 25
        inwork = False
        
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
            self._percent = float(self._minutes)/self.max_minutes
            
        def delm(self):
            del self._minutes
            
        minutes = property(getm, setm, delm, "I'm the 'minutes' property.")
            
    __instance = None
    
    def __init__(self):
        if PomodoroState.__instance is None:
            PomodoroState.__instance = PomodoroState.__impl()
        
    def getval(self):
        return PomodoroState.__instance
    
    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
        
class PomodoroStateProxy(object):
    def __init__( self ):
        self.__subject = PomodoroState()
    def __getattr__( self, name ):
        return getattr( self.__subject, name )
   