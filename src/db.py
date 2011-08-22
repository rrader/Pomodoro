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
from NotificationCenter.NotificationCenter import NotificationCenter

class DataBaseController(object):
    __metaclass__ = Singleton
    
    def __init__(self):
        self.conn = None
        opts = PomodoroOptions()

        self.dbpath = opts.get_db_path(makedbMethod = self.makeNewDB)
        print 'Using db file: %s' % self.dbpath
        if self.dbpath is None:
            raise ConfigError('No db file')
        
        if not os.path.isfile(self.dbpath):
            self.makeNewDB(self.dbpath)
        
        opts.dbpath = self.dbpath
        self.connectToDB(self.dbpath)
    
    def newPomodoro(self, description):
        if self.conn is None:
            connectToDB(self.dbpath)
        cur = self.conn.cursor()
        curtime = str(int(time.time()))
        cur.execute("insert into pomodoros values (?, ?, NULL)", (curtime, description))
        self.conn.commit()
        cur.close()
        print "New pomodoro written: %s, %s" % (curtime, description)
        NotificationCenter().postNotification("pomodorosUpdated", self)
    
    def connectToDB(self, fname):
        self.conn = sqlite.connect(fname)
        self.dbpath = fname
        NotificationCenter().postNotification("dbConnected", self)
    
    def makeNewDB(self, fname):
        try:
            conn = sqlite.connect(fname)
            cur = conn.cursor()
            cur.execute('''CREATE TABLE pomodoros (finish_time integer, description text, key integer primary key)''')
            conn.commit()
            cur.close()
            print "DB Created"
            return True
        except sqlite3.Error, e:
            print "Error while creating db at %s" % fname
            return False
    
    def allPomodoros(self):
        print "Getting pomodoros.."
        if self.conn is None:
            connectToDB(self.dbpath)
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM pomodoros ORDER BY finish_time ASC")
        ret = []
        for row in cur:
            ret.append(PomodoroEntity(int(row[0]),row[1], row[2]))
        self.conn.commit()
        cur.close()
        print "Returned %d records" % (len(ret))
        return tuple(ret)
    
    def pomodoroCount(self):
        if self.conn is None:
            connectToDB(self.dbpath)
        cur = self.conn.cursor()
        cur.execute("SELECT Count(*) FROM pomodoros")
        (count,) = cur.fetchone()
        cur.close()
        return int(count)
    
    def getPomodoro(self, item):
        if self.conn is None:
            connectToDB(self.dbpath)
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM pomodoros ORDER BY finish_time DESC LIMIT ?, 1", str(item))
        row = cur.fetchone()
        ret = PomodoroEntity(int(row[0]), row[1], row[2])
        cur.close()
        return ret