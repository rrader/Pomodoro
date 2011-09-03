#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# localization.py
# Pomodoro
#
# Created by Roman Rader on 28.08.11.
# New BSD License 2011 Antigluk

"""

Python library for localization

"""

import os
from sqlite3 import dbapi2 as sqlite
import threading
from Queue import Queue
from singleton import Singleton

#load from file to sqlite. from internet. reloading

class LocaleError(Exception):
    pass

class LocaleManager(object):
    __metaclass__ = Singleton
    
    def __init__(self, localeDir):
        self.__localeDir = localeDir
        self.__locale = None
        self.selectLocale("english")
    
    def selectLocale(self, codeName):
        if self.__locale is not None:
            del self.__locale
        file = self.__dbFileNameForLocale(codeName)
        self.__locale = Locale(file)
    
    def getString(self, englishString):
        return self.__locale.getString(englishString)
    
    def __dbFileNameForLocale(self, codeName):
        return "%s%s.locale" % (self.__localeDir, codeName)

class Locale(object):
    def __init__(self, fileName = None):
        self.__localedb = None
        if fileName is not None:
            self.loadLocale(fileName)
    
    def loadLocale(self, dbFileName):
        print "Loading locale %s" % dbFileName
        self.__dbFileName = dbFileName
        if not os.path.isfile(dbFileName):
            self.updateLocale(dbFileName)
        
        self.__localedb = LocaleDB(dbFileName)
        self.__localedb.start()
    
    def getString(self, englishString):
        return self.__locale.getString(englishString)
    
    def updateLocale(self, filename):
        "Loads db from text file to sqlite file"
        sourceFile = "%s.src" % filename
        if not os.path.isfile(sourceFile):
            print "locale not found"
            raise LocaleError("Localization %s not found" % filename)
    
    def __del__(self):
        self.__localedb.terminate()
        del self.__localedb

class LocaleDB(threading.Thread):
    def __init__(self, fileName):
        self.__workString = None
        self.__workResult = None
        self.__terminated = False
        self.__dbFileName = fileName
    
    def getString(self, englishString):
        while self.__workString is not None: pass
        self.__workString = englishString
        
        while self.__workResult is None: pass
        ret = self.__workResult
        self.__workResult = None
        
        return ret
    
    def run(self):
        self.__connectToDB(self.__dbFileName)
        
        while not self.__terminated:
            if self.__workString is not None:
                self.__workResult = self.__getLocalizedString(self.__workString)
                self.__workString = None
    
    def terminate(self):
        self.__terminated = True
    
    def __connectToDB(self, fname):
        if not os.path.isfile(fname):
            if not self.__makeNewDB(fname):
                return False
        self.conn = sqlite.connect(fname)
        return True
    
    def __makeNewDB(self, fname):
        try:
            conn = sqlite.connect(fname)
            cur = conn.cursor()
            cur.execute('CREATE TABLE locale (key integer primary key, english text, value text)')
            conn.commit()
            cur.close()
            print "DB Created: %s" % fname
            return True
        except sqlite3.Error, e:
            print "Error while creating db at %s" % fname
            return False
    
    def __getLocalizedString(self, englishString):
        if self.conn is None:
            connectToDB(self.__dbFileName)
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM locale WHERE english=?", englishString)
        (str,) = cur.fetchone()
        cur.close()
        return str