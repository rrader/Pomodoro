#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# ListCtrlDataSource.py
# Pomodoro
#
# Created by Roman Rader on 21.08.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro

import wx
from db import DataBaseController

idColumnDate = 0
idColumnDescription = 1

class PomodoroListCtrl (wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.LC_VIRTUAL | wx.SUNKEN_BORDER | wx.LC_VRULES | wx.LC_HRULES)
        self.parent = parent
        self.InsertColumn(idColumnDate, "Pomodoro finished", width=200)
        self.InsertColumn(idColumnDescription, "Description", width=200)
        PomodoroListCtrl.cache = dict()
    
    def OnGetItemText(self, item, column):
        pItem = None
        ret = None
#        if item not in PomodoroListCtrl.cache:
        pItem = DataBaseController().getPomodoro(item)
#            PomodoroListCtrl.cache[item] = pItem
#        else:
#            pItem = PomodoroListCtrl.cache[item]
            
        if column == idColumnDate:
            ret = pItem.getDate()
        if column == idColumnDescription:
            ret = pItem.description
        return ret
    
    def updateList(self):
        self.SetItemCount(DataBaseController().pomodoroCount())