#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# statisticsframe.py
# Pomodoro
#
# Created by Roman Rader on 22.06.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro


import wx

class StatisticsFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            'Статистика',
            style=wx.DEFAULT_FRAME_STYLE,
            size=(450, 300),
            )
        self.Centre()
        self.construct_frame()
        self.Layout()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def update_ui(self):
        #TODO: проверять видимо ли окно. иначе не обновлять
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
        
        pomodoroList = wx.ListCtrl(tabPomodoroList, style=wx.LC_REPORT)
        pomodoroList.InsertColumn(0, "Pomodoro finished", width=200)
        pomodoroList.InsertColumn(1, "Description", width=200)
        plSizer = wx.BoxSizer(wx.VERTICAL)
        plSizer.Add(pomodoroList, 1, wx.EXPAND|wx.ALL,5)
        tabPomodoroList.SetSizer(plSizer)
#        tabPomodoroList.Add(pomodoroList, 1, wx.ALL|wx.EXPAND, 5)
    
    def on_close(self, m):
        self.Show(False)