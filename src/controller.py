#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# controller.py
# Pomodoro
#
# Created by Roman Rader on 13.04.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro


import wx
from threading import Thread

from state import PomodoroState
from options import PomodoroOptions
from db import DataBaseController

from time import sleep
from datetime import date

from NotificationCenter.NotificationCenter import NotificationCenter


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

    def set_delay(self, d):
        self.__d = d

    def Notify(self):
        self.__f()


class PomodoroController(object):

    def __init__(self, views, app):
        self.now_creation = True
        self.application = app
        self.state = PomodoroState()
        self.opts = PomodoroOptions()
        self.db = DataBaseController()
        self.__views = views
        self.t1 = Timer(1000, self.updateTimer)
        self.t2 = Timer(60000, self.decrementTimer)
        if self.state.debug:
            self.t1.set_delay(1000)
            self.t2.set_delay(1000)
        self.time_str = lambda : str(self.state.minutes) + ' min'
        self._state_info = {
            self.state.StateNoState: {
                'next': self.state.StateWaitingPomodoro,
                'next_early': self.state.StateWaitingPomodoro,
                'upd': False,
                'dec': False,
                'max_min': 0,
                'text': '...',
                'caption': 'Pomodoro!',
                },
            self.state.StatePomodoroKilled: {
                'next': self.state.StateInPomodoro,
                'next_early': self.state.StateInPomodoro,
                'upd': False,
                'dec': False,
                'max_min': 0,
                'text': "Помидора сброшена",
                'caption': 'Pomodoro!',
                },
            self.state.StateInPomodoro: {
                'next': self.state.StateWaitingRest,
                'next_early': self.state.StatePomodoroKilled,
                'upd': True,
                'dec': True,
                'max_min': 25,
                'text': None,
                'caption': 'Pomodoro!',
                },
            self.state.StateInRest: {
                'next': self.state.StateWaitingPomodoro,
                'next_early': self.state.StateInPomodoro,
                'upd': True,
                'dec': True,
                'max_min_s': lambda times: (20 if times % 4
                        == 0 else 5),
                'cycle': 4,
                'text': None,
                'caption': 'Pomodoro!',
                },
            self.state.StateWaitingPomodoro: {
                'next': self.state.StateInPomodoro,
                'next_early': self.state.StateInPomodoro,
                'upd': False,
                'dec': False,
                'max_min': 0,
                'text': "Ожидание начала работы...",
                'caption': 'Pomodoro!',
                },
            self.state.StateWaitingRest: {
                'next': self.state.StateInRest,
                'next_early': self.state.StateInRest,
                'upd': False,
                'dec': False,
                'max_min': 0,
                'text': "Ожидание отдыха...",
                'exec': self.onPomodoroEnd,
                'caption': 'Pomodoro!',
                },
            }

        self.initialState()
        self.updateUI()
        self.now_creation = False

    def onPomodoroEnd(self):
        self.state.inc_times()

        # общее количество выполненых помидор
        self.opts['last'] = int(self.opts.getitem_def('last', 0)) + 1

        # за текущий день
        dt = self.state.TodayStr()
        self.opts[dt] = int(self.opts.getitem_def(dt, 0)) + 1
        
        desc = self.askPomodoroDescription()
        self.db.newPomodoro(desc)
        
    def askPomodoroDescription(self):
        dlg = wx.TextEntryDialog(self.application.frame, 'What have you done?','Pomodoro description')
        dlg.SetValue("A lot of amazing things...")
        ret = "No message"
        if dlg.ShowModal() == wx.ID_OK:
            ret = dlg.GetValue()
        dlg.Destroy()
        return ret
    
    def updateTimer(self):
        self.updateUI()

    def decrementTimer(self):
        self.state.minutes -= 1
        if self.state.minutes <= 0:
            self.state.inwork = False
            self.toggleState(False)
            self.updateUI()
        self.state.text = self.time_str()

    def initTimers(self, info):
        self.t1.start(info['upd'])
        self.t2.start(info['dec'])

    def toggleState(self, user=True, active=None):
        info = self._state_info[(self.state.active if active
                                == None else active)]
        if self.state.inwork and user:
            self.state.active = info['next_early']
        else:
            self.state.active = info['next']
        info = self._state_info[self.state.active]
        self.state.inwork = info['dec']
        if info.has_key('max_min'):
            self.state.max_minutes = info['max_min']
        else:
            self.state.max_minutes = info['max_min_s'](self.state.times)
        if info.has_key('exec'):
            info['exec']()
        self.state.percent = 1.0
        self.state.text = (info['text'] if info['text']
                           != None else self.time_str())
        self.state.caption = info['caption']
        self.initTimers(info)
        self.updateUI()
    
    def initialState(self):
        self.toggleState(active=self.state.StateNoState)
    
    def quit(self):
        NotificationCenter().postNotification("beforeQuit", self)
        self.ToggleState(self.state.StateNoState)
        map(lambda x: x.Destroy(), self.__views)
    
    def updateUI(self):
        if self.now_creation:
            return
        NotificationCenter().postNotification("updateUI", self)
    
    def showListOfPomodoros(self):
        all = self.db.getAllPomodoros()
        for pomodoro in all:
            print "At %s: %s. #%s" % (pomodoro.getDate(), pomodoro.description, str(pomodoro.id_key))
    
    def showStatistics(self):
        stat = self.application.stat_frame
        stat.Show(not stat.IsShown())
    
    def didApplicationLoaded(self):
        NotificationCenter().postNotification("dbUpdated", self)