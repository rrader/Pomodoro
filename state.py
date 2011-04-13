# -*- coding: utf-8 -*-

class ReadOnly(Exception): pass

class PomodoroState(object): #singleton
    class __impl(object):
        text = ""
        active = False
        percent = 1.0
        minutes = 25
    
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
   