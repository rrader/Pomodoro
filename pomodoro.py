#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import wxversion
wxversion.select(['2.8'])
import wx
from tray import TrayIcon
from state import PomodoroStateProxy
from controller import PomodoroController
from StatisticsFrame import StatisticsFrame
from mainframe import Main as MainFrame

class MyApp(wx.App):

    def OnInit(self):
        self.frame = MainFrame(None)
        self.stat_frame = StatisticsFrame(None)
        self.frame.Show(False)
        self.stat_frame.Show(False)
        self.tray = TrayIcon(self.frame)
        views = [self.frame, self.tray, self.stat_frame]
        self.controller = PomodoroController(views)
        self.controller.InitialState()
        
        def set_controller(x):
            x.controller=self.controller
        
        map(set_controller, views)
        return True


def main(argv=None):
    if argv is None:
        argv = sys.argv

    app = MyApp()
    app.MainLoop()


if __name__ == '__main__':
    main()
