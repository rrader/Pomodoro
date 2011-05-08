#!/usr/bin/python
# -*- coding: utf-8 -*-

from singleton import Singleton
import ConfigParser
import os


class ConfigError(Exception):

    pass


class PomodoroOptions(object):

    __metaclass__ = Singleton

    default = None

    def __init__(self, sdef=None):
        self.config = ConfigParser.ConfigParser()
        self.path = self.get_path()
        print 'Using config file: %s' % self.path  # gh-13
        if self.path is None:
            raise ConfigError('No config file')
        self.config.read(self.path)
        self.default = sdef

    def __getitem__(self, name):
        return self.getitem_def(name, self.default)

    def getitem_def(self, name, default):
        r = None
        if self.config.has_option('config', name):
            r = self.config.get('config', name)
        else:
            r = default
        return r

    def __setitem__(self, name, val):
        if not self.config.has_section('config'):
            self.config.add_section('config')
        self.config.set('config', name, val)
        self.config.write(open(self.path, 'w'))
        self.config.read(self.path)

    def get_path(self):
        checkpathes = (os.path.realpath('./pomodoro.conf'),
                       os.path.realpath('./.pomodororc'),
                       '%s/.pomodororc' % os.path.expanduser('~'),
                       '/etc/pomodoro.conf')
        p = filter(os.path.exists, checkpathes)
        if p != ():
            return p[0]
        else:
            return None


