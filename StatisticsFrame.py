#!/usr/bin/python
# -*- coding: utf-8 -*-

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