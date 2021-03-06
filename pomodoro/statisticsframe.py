#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# statisticsframe.py
# Pomodoro
#
# Created by Roman Rader on 22.06.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro

"""

Contains statistics frame

"""


import wx
from NotificationCenter.NotificationCenter import NotificationCenter
from ListCtrlDataSource import PomodoroListCtrl
from db import DataBaseController
import logging
logging.getLogger('Pomodoro')


class StatisticsFrameController(wx.Frame):
    """View for statistics of pomodoros"""
    
    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
            u"Статистика",
            style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER),
            size=(450, 300),
            )
        self.Centre()
        self.construct_frame()
        self.Layout()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Show(False)
        NotificationCenter().addObserver(self,self.onDBUpdate,"dbUpdated")
        NotificationCenter().addObserver(self,self.onUpdateUI,"updateUI")
    
    def onUpdateUI(self, obj):
        self.updateUI()
    
    def updateUI(self):
        #TODO: проверять видимо ли окно. иначе не обновлять
        #TODO: remove this ugly method
        pass
        
    def construct_frame(self):
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)
        
        tabPomodoroList = wx.Panel(notebook)
        notebook.AddPage(tabPomodoroList, "Pomodoro list")
        
        tabPomodoroStat = wx.Panel(notebook)
        notebook.AddPage(tabPomodoroStat, "Statistics")
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        
        self.pomodoroList = PomodoroListCtrl(tabPomodoroList)
        pomodoroList = self.pomodoroList
        plSizer = wx.BoxSizer(wx.VERTICAL)
        plSizer.Add(pomodoroList, 1, wx.EXPAND|wx.ALL,5)
        tabPomodoroList.SetSizer(plSizer)
#        tabPomodoroList.Add(pomodoroList, 1, wx.ALL|wx.EXPAND, 5)
    
    def onClose(self, m):
        self.Show(False)
    
    def onDBUpdate(self, obj):
        #TODO: Move it to controller
        self.pomodoroList.updateList()
