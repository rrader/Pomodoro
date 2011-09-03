#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# pomodoro.py
# Pomodoro
#
# Created by Roman Rader on 13.04.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro

"""

Main file. Contains Application class, controller of application.

"""

__version__='0.3'

import sys
import operator
from time import sleep
from datetime import date
from threading import Thread

import wxversion
wxversion.select(['2.8'])
import wx

from state import PomodoroState
from options import PomodoroOptions
from db import DataBaseController

from tray import TaskbarIconController
from statisticsframe import StatisticsFrameController
from mainframe import MainFrameController

from NotificationCenter.NotificationCenter import NotificationCenter

import optparse
import logging
logging.getLogger('Pomodoro')

class PomodoroController(wx.App):
    """
    Controller of application. All operations must be performed through controller.
    """
    
    def OnInit(self):
        #NotificationCenter().debug = True
        self.__viewControllers = dict()
        
        mainFrame = MainFrameController()
        self.__viewControllers["main"] = mainFrame
        self.__viewControllers["stat"] = StatisticsFrameController()
        self.__viewControllers["icon"] = TaskbarIconController(mainFrame)
        
        #Method MacReopenApp will be called when user clicks on icon in the dock in OSX
        self.MacReopenApp = self.toggleMainFrame
        
        self.initProcess()
        self.SetTopWindow(mainFrame)
        self.didApplicationLoaded()
        
        for view in self.__viewControllers.values():
            view.controller = self
        
        self.Bind(wx.EVT_CLOSE, self.quit)
        self.SetExitOnFrameDelete(True)
        return True
    
    def initProcess(self):
        self.now_creation = True
        
        self.t1 = Timer(1000, self.updateTimer)
        self.t2 = Timer(60000, self.decrementTimer)
        if PomodoroState.debug:
            self.t1.set_delay(1000)
            self.t2.set_delay(1000)
        self.time_str = lambda : str(PomodoroState().minutes) + ' min'
        self._state_info = {
            PomodoroState.StateNoState: {
                'next': PomodoroState.StateWaitingPomodoro,
                'next_early': PomodoroState.StateWaitingPomodoro,
                'upd': False,
                'dec': False,
                'max_min': 0,
                'text': '...',
                'caption': 'Pomodoro!',
                },
            PomodoroState.StatePomodoroKilled: {
                'next': PomodoroState.StateInPomodoro,
                'next_early': PomodoroState.StateInPomodoro,
                'upd': False,
                'dec': False,
                'max_min': 0,
                'text': u"Помидора сброшена",
                'caption': 'Pomodoro!',
                },
            PomodoroState.StateInPomodoro: {
                'next': PomodoroState.StateWaitingRest,
                'next_early': PomodoroState.StatePomodoroKilled,
                'upd': True,
                'dec': True,
                'max_min': 25,
                'text': None,
                'caption': 'Pomodoro!',
                },
            PomodoroState.StateInRest: {
                'next': PomodoroState.StateWaitingPomodoro,
                'next_early': PomodoroState.StateInPomodoro,
                'upd': True,
                'dec': True,
                'max_min_s': lambda times: (20 if times % 4
                        == 0 else 5),
                'cycle': 4,
                'text': None,
                'caption': 'Pomodoro!',
                },
            PomodoroState.StateWaitingPomodoro: {
                'next': PomodoroState.StateInPomodoro,
                'next_early': PomodoroState.StateInPomodoro,
                'upd': False,
                'dec': False,
                'max_min': 0,
                'text': u"Ожидание начала работы...",
                'caption': 'Pomodoro!',
                },
            PomodoroState.StateWaitingRest: {
                'next': PomodoroState.StateInRest,
                'next_early': PomodoroState.StateInRest,
                'upd': False,
                'dec': False,
                'max_min': 0,
                'text': u"Ожидание отдыха...",
                'exec': self.onPomodoroEnd,
                'caption': 'Pomodoro!',
                },
            }
        
        self.initialState()
        self.updateUI()
        self.now_creation = False
        self.initialState()
    
    def toggleMainFrame(self):
        csize = wx.ClientDisplayRect()[2:4]
        mainFrame = self.__viewControllers["main"]
        mainFrame.SetPosition(map(operator.__sub__, csize, mainFrame.GetSizeTuple()))
        mainFrame.Show(not mainFrame.IsShown())
    
    def onPomodoroEnd(self):
        """Calls when pomodoro finished"""
        opts = PomodoroOptions()
        state = PomodoroState()
        
        state.inc_times()
        
        # общее количество выполненых помидор
        opts['last'] = int(opts.getitem_def('last', 0)) + 1
        
        # за текущий день
        dt = state.TodayStr()
        opts[dt] = int(opts.getitem_def(dt, 0)) + 1
        
        desc = self.askPomodoroDescription()
        DataBaseController().newPomodoro(desc)
    
    def askPomodoroDescription(self):
        # FIXME: write to DB BEFORE showing dialog, because application
        #        may halted and pomodoro will not be saved.
        dlg = wx.TextEntryDialog(self.__viewControllers["main"], 'What have you done?','Pomodoro description')
        dlg.SetValue("A lot of amazing things...")
        ret = "No message"
        if dlg.ShowModal() == wx.ID_OK:
            ret = dlg.GetValue()
        dlg.Destroy()
        return ret
    
    def updateTimer(self):
        self.updateUI()
    
    def decrementTimer(self):
        state = PomodoroState()
        state.minutes -= 1
        if state.minutes <= 0:
            state.inwork = False
            self.toggleState(False)
            self.updateUI()
        state.text = self.time_str()
    
    def initTimers(self, info):
        self.t1.start(info['upd'])
        self.t2.start(info['dec'])
    
    def toggleState(self, user=True, active=None):
        state = PomodoroState()
        
        info = self._state_info[(state.active if active == None else active)]
        
        if state.inwork and user:
            state.active = info['next_early']
        else:
            state.active = info['next']
        info = self._state_info[state.active]
        state.inwork = info['dec']
        if info.has_key('max_min'):
            state.max_minutes = info['max_min']
        else:
            state.max_minutes = info['max_min_s'](state.times)
        if info.has_key('exec'):
            info['exec']()
        
        state.percent = 1.0
        state.text = (info['text'] if info['text'] != None else self.time_str())
        state.caption = info['caption']
        self.initTimers(info)
        self.updateUI()
    
    def initialState(self):
        self.toggleState(active=PomodoroState.StateNoState)
    
    def quit(self):
        NotificationCenter().postNotification("beforeQuit", self)
        self.toggleState(PomodoroState.StateNoState)
        map(lambda x: x.Destroy(), self.__viewControllers.values())
        print "Views were destroyed"
    
    def updateUI(self):
        if self.now_creation:
            return
        NotificationCenter().postNotification("updateUI", self)
    
    def showListOfPomodoros(self):
        all = self.db.getAllPomodoros()
        for pomodoro in all:
            logging.info("At %s: %s. #%s" % (pomodoro.getDate(), pomodoro.description, str(pomodoro.id_key)))
    
    def showStatistics(self):
        view = self.__viewControllers["stat"]
        view.Show(not view.IsShown())
    
    def didApplicationLoaded(self):
        NotificationCenter().postNotification("dbUpdated", self)


class Timer(wx.Timer):
    """Adapter for wx.Timer, that calls specifed method"""
    
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


LEVELS = (  logging.ERROR,
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
            )

def main():
    usage = "pomodoro [options]"
    parser = optparse.OptionParser(version="pomodoro %s" % '0.3', usage=usage)
    parser.add_option('-d', '--debug', dest='debug_mode', action='store_true',
                      help='Print the maximum debugging info (implies -vv)')
    parser.add_option('-v', '--verbose', dest='logging_level', action='count',
                      help='set error_level output to warning, info, and then debug')

    parser.set_defaults(logging_level=0)
    (options, args) = parser.parse_args()
    print 'fff'
    if options.debug_mode:
        options.logging_level = 3
    logging.basicConfig(level=LEVELS[options.logging_level], format='%(lineno)d %(asctime)s %(levelname)s %(message)s')
    #FIXME: добавь нормальные настройки конфига.
    #if argv is None:
    #    argv = sys.argv
    logging.info('run pomodoro')
    app = PomodoroController(redirect=False)
    app.MainLoop()


if __name__ == '__main__':
    main()
