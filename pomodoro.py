#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import wx
from tray import TrayIcon
from state import PomodoroStateProxy
from controller import PomodoroController

class Main(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Pomodoro it!", style=wx.BORDER_DEFAULT, size=(200,120,))
        self.state = PomodoroStateProxy()
        self.tray = TrayIcon(self)
        self.construct_frame()
        self.controller = PomodoroController([self, self.tray])
        self.controller.InitialState()
        self.update_ui()
        
    def construct_frame(self):
        self.panel = wx.Panel(self)
        wx.StaticText(self.panel, pos=(10,10), label="Pomodoro!")
        self.timer_ctrl = wx.TextCtrl(self.panel, pos=(10,30), size=(180,-1),
                                      style=wx.TE_READONLY | wx.TE_CENTER)
        self.start_button = wx.Button(self.panel, pos=(20,70), label="", size=(160,-1))
        self.start_button.Bind(wx.EVT_BUTTON, self.BClick)
    
    def update_ui(self):
        self.timer_ctrl.SetValue(self.state.text)
        self.start_button.SetLabel("Начать работу!" if not self.state.active else
                                   "Сброс помидоры")
    
    def BClick(self, m):
        self.controller.ToggleState()
        
class MyApp(wx.App):
    def OnInit(self):
        frame = Main(None)
        frame.Show(False)
        return True
    
def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    app = MyApp()
    app.MainLoop()
    
if __name__ == '__main__':
    main()