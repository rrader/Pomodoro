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
            style=wx.BORDER_DEFAULT,
            size=(320, 220),
            )
        self.Centre()

    def update_ui(self):
        #TODO: проверять видимо ли окно. иначе не обновлять
        pass