# -*- coding: utf-8 -*-

from singleton import Singleton
import ConfigParser
import os

class ConfigError(Exception): pass

class PomodoroOptions(object):
    __metaclass__ = Singleton
    
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.path = self.get_path()
        print "Using config file: %s" % self.path
        if self.path is None:
            raise ConfigError("No config file")
        self.config.read(self.path)
    
    def __getitem__(self, name):
        try:
            r = self.config.get('config', name)
        except Exception as x:
            print x.args
            r = None
        return r
    
    def __setitem__(self, name, val):
        self.config.set('config', name, val)
    
    def get_path(self):
        checkpathes = (os.path.realpath("./pomodoro.conf"),
                       os.path.realpath("./.pomodororc"),
                       "%s/.pomodororc" % os.path.expanduser("~"),
                       "/etc/pomodoro.conf",)
        p = filter(os.path.exists,checkpathes)
        if p!=():
            return p[0]
        else:
            return None