#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# pomodoro_entity.py
# Pomodoro
#
# Created by Roman Rader on 20.08.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro

"""

Contains class that describes entity of pomodoro

"""


import time

class PomodoroEntity (object):
    """Class that describes entity of pomodoro"""
    
    def __init__(self, p_date = None, p_description = None, p_key = None):
        self.date = p_date
        self.description = p_description
        self.id_key = p_key
    
    def getDate(self):
        if self.date != None:
            return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(self.date))
        return "No time"