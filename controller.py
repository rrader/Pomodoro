# -*- coding: utf-8 -*-

import wx
from threading import Thread

from state import PomodoroState
from time import sleep

class Timer(wx.Timer):
    def __init__(self, delay, f):
        wx.Timer.__init__(self)
        self.__f = f
        self.__d = delay
    
    def start(self, b):
        if b:
            self.Start(self.__d)
        else:
            self.Stop()
    
    def Notify(self):
        self.__f()

class PomodoroController(object):
    def __init__(self, views):
        self.state = PomodoroState()
        self.__views = views
        self.state.text = "Помидоры!"
        self.InitialState()
        self.update_ui()
        self.t1 = Timer(1000, self.UpdateTimer)
        self.t2 = Timer(60000, self.DecrementTimer)
        self.StartTimers(False)
        self.time_str = lambda: str(self.state.minutes)+" min"
    
    def UpdateTimer(self):
        self.update_ui()
        print self.state.active
        
    def DecrementTimer(self):
        self.state.minutes -= 1
        self.state.text = self.time_str()
        if self.state.minutes <= 0:
            self.StartTimers(False)
            self.ResetStateInRest()
            self.update_ui()
    
    def StartTimers(self, toggle=True):
        self.t1.start(toggle)
        self.t2.start(toggle)
        self.state.active = toggle
        
    def ToggleState(self):
        self.state.active = not self.state.active
        self.StartTimers(self.state.active)
        if not self.state.active:
            self.state.text = "Pomodoro killed"
            self.state.caption = "Pomodoro!"
            self.update_ui()
        else:
            self.ResetStateInPomodoro()
            self.state.text = self.time_str()
            self.update_ui()
    
    def InitialState(self):
        self.state.active = False
        self.ResetStateInPomodoro()
        self.state.caption = "Pomodoro!"
    
    def ResetStateInPomodoro(self):
        self.state.max_minutes = 25
        self.state.percent = 1.0
        self.state.caption = "In Pomodoro!"
    
    def ResetStateInRest(self):
        self.state.max_minutes = 5
        self.state.percent = 1.0
        self.state.caption = "Отдыхайте сейчас!"
    
    def update_ui(self):
        map(lambda x:x.update_ui(), self.__views)