#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# mainframe.py
# Pomodoro
#
# Created by Roman Rader on 22.06.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro

"""

Contains main frame of application.

"""


import wx
from state import PomodoroStateProxy as PomodoroState
from NotificationCenter.NotificationCenter import NotificationCenter
import logging
logging.getLogger('Pomodoro')

class MainFrameController(wx.Frame):
    """Main frame of Pomodoro"""
    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'Pomodoro it!',
            style=wx.BORDER_DEFAULT | wx.STAY_ON_TOP,
            size=(220, 120),
            )
        state = PomodoroState()
        self.__state_dict = {
            state.StateNoState: {'bs': '...'},
            state.StateInPomodoro: {'bs': u"Отменить..."},
            state.StateInRest: {'bs': u"Отдыхайте!"},
            state.StateWaitingPomodoro: {'bs': u"Начать помидору"},
            state.StateWaitingRest: {'bs': u"Начать отдых"},
            state.StatePomodoroKilled: {'bs': u"Начать помидору"},
            }
        self.buildFrame()
        self.updateUI()
        self.makeMenu()
        self.Show(False)
        NotificationCenter().addObserver(self,self.onDBUpdate,"dbUpdated")
        NotificationCenter().addObserver(self,self.onUpdateUI,"updateUI")

    def buildFrame(self):
        self.panel = wx.Panel(self)
        self.txt = wx.StaticText(self.panel, pos=(10, 10),
                                 label='Pomodoro!')
        self.times_l = wx.StaticText(self.panel, pos=(120, 10),
                label=u"0 помидор")
        self.timer_ctrl = wx.TextCtrl(self.panel, pos=(10, 30),
                size=(200, -1), style=wx.TE_READONLY | wx.TE_CENTER)
        self.start_button = wx.Button(self.panel, pos=(20, 70), label=''
                , size=(170, -1))
        self.start_button.Bind(wx.EVT_BUTTON, self.bClick)
    
    def onUpdateUI(self, event):
        self.updateUI()
    
    def updateUI(self):
        #TODO: проверять видимо ли окно. иначе не обновлять
        #TODO: remove this ugly method
        state = PomodoroState()
        self.timer_ctrl.SetValue(state.text)
        self.start_button.SetLabel(self.__state_dict[state.active]['bs'])
        self.txt.SetLabel(state.caption)
        self.times_l.SetLabel(u"%d помидор" % state.GetTodayCount())

    def bClick(self, m):
        logging.debug("Toggle state")
        self.controller.toggleState()
    
    def onExit(self,m):
        logging.debug("Quit")
        self.controller.quit()
    
    def makeMenu(self):
        self.menuBar = wx.MenuBar()
        
        self.menu = wx.Menu()
        item = self.menu.Append(wx.ID_ANY, "Toggle pomodoro")
        self.menu.Bind(wx.EVT_MENU, self.bClick, item)
        item = self.menu.Append(wx.ID_EXIT, "&Quit", "quit")
        self.menu.Bind(wx.EVT_MENU, self.onExit, id=wx.ID_EXIT)
        
        self.menuBar.Append(self.menu, "&File")
        self.SetMenuBar(self.menuBar)
    
    def onDBUpdate(self, obj):
        pass
