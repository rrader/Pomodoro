#!/usr/bin/env python

import sys

import wx
from tray import TrayIcon
from state import PomodoroState
from controller import PomodoroController

class Main(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Pomodoro it!", style=wx.BORDER_DEFAULT, size=(140,120,))
        self.tray = TrayIcon(self)
        self.state = PomodoroState()
        self.state.percent = 1
        self.state.active = False
        self.state.minutes = 25
        self.construct_frame()
        self.update_ui()
        self.controller = PomodoroController()
        
    def construct_frame(self):
        self.panel = wx.Panel(self)
        wx.StaticText(self.panel, pos=(10,10), label="Pomodoro!")
        self.timer_ctrl = wx.TextCtrl(self.panel, pos=(10,30), size=(120,-1),
                                      style=wx.TE_READONLY | wx.TE_CENTER)
        self.start_button = wx.Button(self.panel, pos=(20,70), label="Start!")
    
    def update_ui(self):
        self.timer_ctrl.SetValue(self.state.text)
        self.start_button.SetLabel("1")
        
        
        
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