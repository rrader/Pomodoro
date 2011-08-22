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
from NotificationCenter.NotificationCenter import NotificationCenter


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
#        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.popup_menu)
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
        item = self.menu.Append(wx.ID_ANY,"All pomodoros", "List of pomodoros")
        self.menu.Bind(wx.EVT_MENU, self.list_of_pomodoros, item)
        item = self.menu.Append(wx.ID_ANY,"Statistics", "Statistics")
        self.menu.Bind(wx.EVT_MENU, self.show_statistics, item)
        item = self.menu.Append(wx.ID_EXIT,"Exit", "Exit from Pomodoro")
        self.menu.Bind(wx.EVT_MENU, self.on_menu_exit, item)
        
    def CreatePopupMenu(self):
        self.make_menu()
        return self.menu
    
    def on_menu_exit(self, m):
        self.controller.Quit()
    
    def update_ui(self):
        #TODO: remove this ugly method
        self.SetIcon(self.get_icon(), 'Pomodoro %s' % self.state.text)
    
    def list_of_pomodoros(self, m):
        self.controller.show_list_of_pomodoros()
    
    def show_statistics(self,m):
        self.controller.show_statistics()
    
    def Close(self):
        self.RemoveIcon()