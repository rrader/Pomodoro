#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# db.py
# Pomodoro
#
# Created by Roman Rader on 20.08.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro

"""

Data base controller.

"""


from singleton import Singleton
from options import PomodoroOptions, ConfigError
from sqlite3 import dbapi2 as sqlite
import time
import os
from pomodoro_entity import PomodoroEntity
from NotificationCenter.NotificationCenter import NotificationCenter
import threading
from Queue import Empty as QueueEmpty
from Queue import Queue

# Producer of tasks
class DataBaseController(object):
    """
    Controller for DB. Generator of tasks (DBTask) for DataBaseThread
    (producer-consumer pattern), which process it from shared Queue.
    """
    __metaclass__ = Singleton
    
    DBREQUEST_TIMEOUT = 5
    
    def __init__(self):
        self.queue = Queue()
        self.dbThread = DataBaseThread(self.queue)
        self.dbThread.start()
        NotificationCenter().addObserver(self,self.willQuit,"beforeQuit")
    
    def willQuit(self, obj):
        print "Waiting for finishing all operations with DB..."
        self.queue.join()
        print "Terminating DB thread..."
        self.dbThread.terminate()
    
    def newPomodoro(self, description):
        curtime = str(int(time.time()))
        task = DBTask(DBTask.DBTASK_ADD, {"time": curtime,
                                          "desc": description})
        self.queue.put(task, True, self.DBREQUEST_TIMEOUT)
        self.queue.join()
        NotificationCenter().postNotification("dbUpdated", self)
        return task.result
    
    def getAllPomodoros(self):
        task = DBTask(DBTask.DBTASK_GET_ALL)
        self.queue.put(task, True, self.DBREQUEST_TIMEOUT)
        self.queue.join()
        return task.result
    
    def getPomodoro(self, number):
        task = DBTask(DBTask.DBTASK_GET_ONE, {"number": number})
        self.queue.put(task, True, self.DBREQUEST_TIMEOUT)
        self.queue.join()
        return task.result
    
    def pomodoroCount(self):
        task = DBTask(DBTask.DBTASK_GET_COUNT)
        self.queue.put(task, True, self.DBREQUEST_TIMEOUT)
        self.queue.join()
        return task.result
    
    def makeDB(self, fileName):
        task = DBTask(DBTask.DBTASK_MAKEDB, {"file": fileName})
        self.queue.put(task, True, self.DBREQUEST_TIMEOUT)
        self.queue.join()
        return task.result


# Task for DB
class DBTask(object):
    """Describes task for DataBaseThread"""
    DBTASK_NOTASK = 0
    DBTASK_ADD = 1
    DBTASK_MAKEDB = 2
    DBTASK_GET_ALL = 3
    DBTASK_GET_COUNT = 4
    DBTASK_GET_ONE = 5
    def __init__(self, act, parameters=None, callback=None):
        self.action = act
        self.data = parameters
        self.result = None
        self.callback = callback
    
    def sendCallback(self):
        if self.callback is not None:
            self.callback(self)


# Consumer, handler
class DataBaseThread(threading.Thread):
    """
    Thread that handles requests to DB.
    Contains connection object to SQLite.
    Consumer in producer-consumer pattern.
    """
    def __init__(self, queue):
        threading.Thread.__init__(self)
        
        self.queue = queue
        
        self.conn = None
        opts = PomodoroOptions()
        
        self.dbpath = opts.getDBPath(makedbMethod = self.makeNewDB)
        print 'Using db file: %s' % self.dbpath
        if self.dbpath is None:
            raise ConfigError('No db file')
        
        if not os.path.isfile(self.dbpath):
            self.makeNewDB(self.dbpath)
        
        opts.dbpath = self.dbpath
        self.__terminated = False
    
    def run(self):
        self.connectToDB(self.dbpath)
        
        while not self.__terminated:
            try:
                task = self.queue.get_nowait()
            except QueueEmpty:
                continue
            ret = None
            
            if task.action == DBTask.DBTASK_ADD:
                ret = self.newPomodoro(task.data["time"], task.data["desc"])
                print "New pomodoro written: %s, %s" % ret
            
            if task.action == DBTask.DBTASK_MAKEDB:
                ret = self.makeNewDB(task.data["file"])
            
            if task.action == DBTask.DBTASK_GET_ALL:
                ret = self.allPomodoros()
            
            if task.action == DBTask.DBTASK_GET_ONE:
                ret = self.getPomodoro(task.data["number"])
            
            if task.action == DBTask.DBTASK_GET_COUNT:
                ret = self.pomodoroCount()
            
            task.result = ret
            self.queue.task_done()
            task.sendCallback()
        print "Data Base Thread terminated"
    
    def connectToDB(self, fname):
        self.conn = sqlite.connect(fname)
        self.dbpath = fname
        NotificationCenter().postNotification("dbConnected", self)
    
    def terminate(self):
        self.__terminated = True
    
    # Tasks
    def newPomodoro(self, time, description):
        if self.conn is None:
            connectToDB(self.dbpath)
        cur = self.conn.cursor()
        cur.execute("insert into pomodoros values (?, ?, NULL)", (time, description))
        self.conn.commit()
        cur.close()
        return (time, description)
    
    def makeNewDB(self, fname):
        try:
            conn = sqlite.connect(fname)
            cur = conn.cursor()
            cur.execute('CREATE TABLE pomodoros (finish_time integer, description text, key integer primary key)')
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
        cur.execute("SELECT * FROM pomodoros ORDER BY finish_time DESC LIMIT ?, 1", [str(item)])
        row = cur.fetchone()
        ret = PomodoroEntity(int(row[0]), row[1], row[2])
        cur.close()
        return ret