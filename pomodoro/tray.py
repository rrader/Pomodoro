#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# tray.py
# Pomodoro
#
# Created by Roman Rader on 13.04.11.
# New BSD License 2011 Antigluk https://github.com/antigluk/Pomodoro

"""

Wrapper for tray icon: Using AppIndicator or wxTaskBarIcon

"""

import wx
from state import PomodoroStateProxy as PomodoroState
from NotificationCenter.NotificationCenter import NotificationCenter
import threading
import os
import logging
logging.getLogger('Pomodoro')


#check if AppIndicators aviable
print("Is there AppIndicator?")
have_appindicator = True
try:
    import appindicator
    import gtk
    import gobject
    print("AppIndicator is here! I loaded it. And GTK too.")
except:
    have_appindicator = False
    print("Nope. Using wx taskbar icon.")

# === AppIndicator ===

# FIXME: It's the terrible hack. I'd like to avoid it.
# If you know how to, please send me email: antigluk@gmail.com

# AppIndicator and gtk.main() must be in another thread
class GtkThread(threading.Thread):
    """gtk.main() is running in this thread"""
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        #run gtk.main()
        logging.debug("gtk.main() starting... in another thread.")
        gtk.gdk.threads_init()
        gtk.main()
        logging.warn("GTK thread terminated")
    
    def quitGTK(self):
        gtk.main_quit()
        logging.info("gtk.main_quit() called.")

# AppIndicator Icon
class AITrayIcon(object):
    """Adapter and decorator for AppIndicator"""
    def __init__(self):
        self.makeIndicator()
        self.thread = GtkThread()
        self.thread.start()
        logging.debug("GtkThread started. Do you see AppIndicator?")
        NotificationCenter().addObserver(self,self.willQuit,"beforeQuit")
    
    def makeIndicator(self):
        #init appindicator
        self.ind = appindicator.Indicator("Pomodoro","gtk-execute",
                            appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
    
    def makeAndSetMenu(self, menuItems):
        self.menu = gtk.Menu()
        self.menuItemsMethods = dict()
        for (itemName, desc, method) in menuItems:
            item = gtk.MenuItem(itemName)
            item.connect("activate", self.menuItemSelected)
            item.show()
            self.menu.append(item)
            self.menuItemsMethods[item] = method
        self.ind.set_menu(self.menu)
    
    def menuItemSelected(self, data=None):
        logging.debug("Item '%s' selected, performing %s" % (data.get_label(),self.menuItemsMethods[data]))
        self.menuItemsMethods[data]()
    
    def canToggleByClick(self):
        return False
    
    def updateUI(self):
        pass
    
    def willQuit(self, obj):
        self.thread.quitGTK()
        # FIXME: it's hack. i don't know how stop it gracefully.
        # gtk.main_quit() is not works. absolutely.
        self.thread._Thread__stop()
    
    def destroyView(self):
        self.thread.quitGTK()
    
    def closeView(self):
        pass


# === wxWidgets icon ===

# wxTaskBarIcon Icon
class WXTrayIcon(wx.TaskBarIcon):
    """Adapter and decorator of wxTaskBarIcon"""
    
    #TODO: change icon size for types of OS and tray bar
    ICO_HEIGHT = 16
    ICO_WIDTH = 16
    
    def __init__(self):
        super(WXTrayIcon, self).__init__()

        self.colors = {1.0: 'green', 0.6: 'yellow', 0.3: 'red'}
        self.state = PomodoroState()
        self.SetIcon(self.getIcon(), 'Pomodoro')
#        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.popup_menu) # check it in Windows and Linux (non-unity)
    
    def setToggleFrameMethod(self, method):
        self.toggleFrameMethod = method
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.doToggleFrame)
    
    def doToggleFrame(self, m):
        self.toggleFrameMethod()
    
    def getIcon(self):
        h = int(self.state.percent * self.ICO_HEIGHT)

        img = wx.EmptyBitmap(self.ICO_WIDTH, self.ICO_HEIGHT)
        dc = wx.MemoryDC(img)
        dc.Brush = wx.Brush('white', wx.TRANSPARENT)
        dc.Clear()
        col = self.colors[min(filter(lambda x: self.state.percent <= x,
                          self.colors))]
        if not self.state.active:
            col = 'white'
        dc.Brush = wx.Brush(col)
        dc.DrawRectangle(3, self.ICO_HEIGHT - h, 10, h)
        del dc # issue #41
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(img)
        return icon
    
    def makeAndSetMenu(self, menuItems):
        #TODO: test in MacOS and Windows
        self.menu = wx.Menu()
        self.items = menuItems
        self.menuItemsDict = dict()
        for (itemName, description, method) in menuItems:
            item = self.menu.Append(wx.ID_ANY, itemName, description)
            self.menu.Bind(wx.EVT_MENU, self.menuItemSelected, item)
            self.menuItemsDict[item.GetId()] = method
        logging.info("Menu generated")
    
    def menuItemSelected(self, event):
        logging.info("Item %d selected, performing %s" % (event.GetId(),self.menuItemsDict[event.GetId()]))
        self.menuItemsDict[event.GetId()]()
    
    def CreatePopupMenu(self):
        logging.debug("Popup..")
        self.makeAndSetMenu(self.items)
        return self.menu
    
    def updateUI(self):
        #TODO: remove this ugly method
        self.SetIcon(self.getIcon(), 'Pomodoro %s' % self.state.text)
    
    def Close(self):
        self.RemoveIcon()
    
    def canToggleByClick(self):
        return True
    
    def destroyView(self):
        self.Destroy()
    
    def closeView(self):
        self.Close()



class TaskbarIconController(object):
    """Bridge for tray icon controllers"""
    
    def __init__(self, frame):
        self.frame = frame
        
        menuItems = [("All pomodoros", "List of pomodoros", self.listOfPomodoros),
                     ("Statistics", "Statistics", self.showStatistics),
                     ("Quit", "Quit of Pomodoro", self.quitSelected)]
        
        if have_appindicator:
            self.iconController = AITrayIcon()
        else:
            self.iconController = WXTrayIcon()
        
        if self.iconController.canToggleByClick():
            self.iconController.setToggleFrameMethod(self.toggleWindow)
        else:
            menuItems.insert(0, ("Toggle pomodoro window", "Show/hide window", self.toggleWindow))
        self.makeAndSetMenu(menuItems)
        NotificationCenter().addObserver(self,self.onUpdateUI,"updateUI")
    
    def makeAndSetMenu(self, menuItems):
        self.iconController.makeAndSetMenu(menuItems)
    
    def onUpdateUI(self, event):
        self.iconController.updateUI()
    
    def Destroy(self):
        self.iconController.destroyView()
    
    def Close(self):
        self.iconController.closeView()
    
    # menu handlers
    def listOfPomodoros(self):
        self.controller.showListOfPomodoros()
    
    def showStatistics(self):
        self.controller.showStatistics()
    
    def quitSelected(self):
        self.controller.quit()
    
    def toggleWindow(self):
        self.controller.toggleMainFrame()
