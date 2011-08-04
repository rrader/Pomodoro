#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from state import PomodoroStateProxy

class Main(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            'Pomodoro it!',
            style=wx.BORDER_DEFAULT | wx.STAY_ON_TOP,
            size=(220, 120),
            )
        self.state = PomodoroStateProxy()
        self.__state_dict = {
            self.state.StateNoState: {'bs': '...'},
            self.state.StateInPomodoro: {'bs': "Отменить..."},
            self.state.StateInRest: {'bs': "Отдыхайте!"},
            self.state.StateWaitingPomodoro: {'bs': "Начать помидору"},
            self.state.StateWaitingRest: {'bs': "Начать отдых"},
            self.state.StatePomodoroKilled: {'bs': "Начать помидору"},
            }
        self.construct_frame()
        self.update_ui()

    def construct_frame(self):
        self.panel = wx.Panel(self)
        self.txt = wx.StaticText(self.panel, pos=(10, 10),
                                 label='Pomodoro!')
        self.times_l = wx.StaticText(self.panel, pos=(120, 10),
                label="0 помидор")
        self.timer_ctrl = wx.TextCtrl(self.panel, pos=(10, 30),
                size=(200, -1), style=wx.TE_READONLY | wx.TE_CENTER)
        self.start_button = wx.Button(self.panel, pos=(20, 70), label=''
                , size=(170, -1))
        self.start_button.Bind(wx.EVT_BUTTON, self.BClick)

    def update_ui(self):
        #TODO: проверять видимо ли окно. иначе не обновлять
        self.timer_ctrl.SetValue(self.state.text)
        self.start_button.SetLabel(self.__state_dict[self.state.active]['bs'
                                   ])
        self.txt.SetLabel(self.state.caption)
        self.times_l.SetLabel("%d помидор"
                              % self.state.GetTodayCount())

    def BClick(self, m):
        self.controller.ToggleState()