#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# db.py
# Pomodoro
#
# Created by Roman Rader on 20.08.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro

from singleton import Singleton
from options import PomodoroOptions, ConfigError
from sqlite3 import dbapi2 as sqlite
import time
import os
from pomodoro_entity import PomodoroEntity

class DataBaseController(object):
    __metaclass__ = Singleton
    
    def __init__(self):
        opts = PomodoroOptions()

        self.dbpath = opts.get_db_path(makedbMethod = self.makeNewDB)
        print 'Using db file: %s' % self.dbpath
        if self.dbpath is None:
            raise ConfigError('No db file')
        
        if not os.path.isfile(self.dbpath):
            self.makeNewDB(self.dbpath)
        
        opts.dbpath = self.dbpath
    
    def newPomodoro(self, description):
        conn = sqlite.connect(PomodoroOptions().dbpath)
        cur = conn.cursor()
        curtime = str(int(time.time()))
        cur.execute("insert into pomodoros values (?, ?)", (curtime, description))
        conn.commit()
        cur.close()
        print "New pomodoro written: %s, %s" % (curtime, description)
    
    def makeNewDB(self, fname):
        try:
            conn = sqlite.connect(fname)
            cur = conn.cursor()
            cur.execute('''create table pomodoros (finish_time integer, description text)''')
            conn.commit()
            cur.close()
            print "DB Created"
            return True
        except sqlite3.Error, e:
            print "Error while creating db at %s" % fname
            return False
        
    def allPomodoros(self):
        print "Getting pomodoros.."
        conn = sqlite.connect(self.dbpath)
        cur = conn.cursor()
        cur.execute("select * from pomodoros order by finish_time")
        ret = []
        for row in cur:
            ret.append(PomodoroEntity(int(row[0]),row[1]))
        conn.commit()
        cur.close()
        print "Returned %d records" % (len(ret))
        return tuple(ret)