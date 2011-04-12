#!/usr/bin/env python

import sys

import wx
from tray import TrayIcon
from state import PomodoroState

class Main(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Pomodoro it!", style=wx.BORDER_DEFAULT, size=(240,120,))
        self.tray = TrayIcon(self)
        state = PomodoroState()
        state.percent = 1
        state.active = False
        state.minutes = 25

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