#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# singleton.py
# Pomodoro
#
# Created by Roman Rader on 21.04.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro

"""

Contains metaclass Singleton

"""


class Singleton(type):
    """Metaclass for simplifying realization of singletons"""
    
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance