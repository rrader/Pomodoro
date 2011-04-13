# -*- coding: utf-8 -*-

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
        self.state.text = "Помидоры!"
        self.InitialState()
        self.__view.update_ui()
        self.t1 = Timer(5, self.UpdateTimer)
        self.t2 = Timer(60, self.DecrementTimer)
        self.RunTimers()
        self.time_str = lambda: str(self.state.minutes)+" min"
    
    def UpdateTimer(self, t):
        self.__view.update_ui()
        
    def DecrementTimer(self, t):
        self.state.minutes -= 1
        self.state.text = self.time_str()
        if self.state.minutes <= 0:
            self.StopTimers()
            self.state.text = "Отдыхайте сейчас!"
            self.__view.update_ui()
    
    def RunTimers(self):
        self.t1.start()
        self.t2.start()
    
    def StartTimers(self, toggle=True):
        self.t1.ok = toggle
        self.t2.ok = toggle
        self.state.active = toggle
        
    def ToggleState(self):
        self.state.active = not self.state.active
        self.StartTimers(self.state.active)
        if not self.state.active:
            self.state.text = "Pomodoro killed"
            self.__view.update_ui()
        else:
            self.state.text = self.time_str()
            self.__view.update_ui()
    
    def InitialState(self):
        self.state.percent = 1
        self.state.active = False
        self.state.minutes = 1