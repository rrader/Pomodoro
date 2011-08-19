#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# tray.py
# Pomodoro
#
# Created by Roman Rader on 13.04.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro


import wx
from state import PomodoroStateProxy
import operator


class TrayIcon(wx.TaskBarIcon):

    ICO_HEIGHT = 16
    ICO_WIDTH = 16

    def __init__(self, frame):
        super(TrayIcon, self).__init__()

        self.colors = {1.0: 'green', 0.6: 'yellow', 0.3: 'red'}
        self.state = PomodoroStateProxy()
        self.frame = frame
        self.SetIcon(self.get_icon(), 'Pomodoro')
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.toggle_frame)
        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.popup_menu)
        self.make_menu()

    def toggle_frame(self, m):
        f = self.frame
        csize = wx.ClientDisplayRect()[2:4]
        f.SetPosition(map(operator.__sub__, csize, f.GetSizeTuple()))
        f.Show(not f.IsShown())

    def get_icon(self):
        h = int(self.state.percent * self.ICO_HEIGHT)

        img = wx.EmptyBitmap(self.ICO_WIDTH, self.ICO_HEIGHT)
        dc = wx.MemoryDC(img)
        dc.Brush = wx.Brush('white', wx.TRANSPARENT)
        dc.Clear()
        col = self.colors[min(filter(lambda x: self.state.percent <= x,
                          self.colors))]
        if not self.state.active:
            col = 'white'
        dc.Brush = wx.Brush(col)
        dc.DrawRectangle(3, self.ICO_HEIGHT - h, 10, h)
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(img)
        return icon
    
    def make_menu(self):
        self.menu = wx.Menu()
        item = self.menu.Append(wx.ID_EXIT,"Exit", "Exit from Pomodoro")
        self.menu.Bind(wx.EVT_MENU, self.on_menu_exit, item)
        
        
    def popup_menu(self, m):
        self.PopupMenu(self.menu)
    
    def on_menu_exit(self, m):
        self.controller.Quit()
    
    def update_ui(self):
        self.SetIcon(self.get_icon(), 'Pomodoro %s' % self.state.text)
        
    def Close(self):
        self.RemoveIcon()


