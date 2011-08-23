#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# pomodoro.py
# Pomodoro
#
# Created by Roman Rader on 13.04.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro


import sys

import wxversion
wxversion.select(['2.8'])
import wx
from tray import TaskbarIconController
from state import PomodoroStateProxy
from controller import PomodoroController
from statisticsframe import StatisticsFrame
from mainframe import Main as MainFrame

class MyApp(wx.App):

    def OnInit(self):
        self.frame = MainFrame(None)
        self.stat_frame = StatisticsFrame(None)
        self.frame.Show(False)
        self.stat_frame.Show(False)
        self.tray = TaskbarIconController(self.frame)
        views = [self.frame, self.tray, self.stat_frame]
        self.controller = PomodoroController(views, self)
        self.controller.InitialState()
        self.SetTopWindow(self.frame)
        self.controller.didApplicationLoaded()
        
        def set_controller(x):
            x.controller=self.controller
        
        map(set_controller, views)
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetExitOnFrameDelete(True)
        return True
    
    def MacReopenApp(self):
        self.tray.toggleWindow()
    
    def on_close(self):
        print "close"
        self.controller.Quit()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    app = MyApp(redirect=False)
    app.MainLoop()


if __name__ == '__main__':
    main()
