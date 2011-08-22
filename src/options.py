#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# options.py
# Pomodoro
#
# Created by Roman Rader on 21.04.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro


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

    def get_config_file(self, checkpathes, method = None):
        p = filter(os.path.exists, checkpathes)
        if p != ():
            return p[0]
        else:
            for path in checkpathes:
                try:
                    if not os.path.exists(os.path.dirname(path)):
                        os.makedirs(os.path.dirname(path))
                    if method is not None:
                        if method(path):
                            break
                        else:
                            continue
                    else:
                        try:
                            self.config.write(file(path, 'w'))
                            os.chmod(path, 0600)
                            break
                        except IOError:
                            continue
                except OSError:
                    # what to do if impossible?
                    sys.stderr.write("ERROR: couldn't create the config directory\n")
            if not os.path.exists(path):
                return None
            else:
                return path

    def get_path(self):
        #TODO: remove ./*
        checkpathes = (os.path.realpath('./pomodoro.conf'),
                       os.path.realpath('./.pomodororc'),
                       os.path.join(os.path.expanduser('~'),'.pomodororc'),
                       '/etc/pomodoro.conf')
        return self.get_config_file(checkpathes)
                
    def get_db_path(self, makedbMethod = None):
        #TODO: remove ./*
        checkpathes = (os.path.realpath('./pomodoro.db'),
                       os.path.realpath('./.pomodorodb'),
                       os.path.join(os.path.expanduser('~'),'.pomodorodb'))
        return self.get_config_file(checkpathes, makedbMethod)

