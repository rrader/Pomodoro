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
from state import PomodoroStateProxy
import operator
from NotificationCenter.NotificationCenter import NotificationCenter
import threading
import os

#check if AppIndicators aviable
print "Is there AppIndicator?"
have_appindicator = True
try:
    import appindicator
    import gtk
    import gobject
    print "  AppIndicator is here! I loaded it. And GTK too."
except:
    have_appindicator = False
    print "  Nope. Using wx taskbar icon."

# === AppIndicator ===

# AppIndicator and gtk.main() must be in another thread
class GtkThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        #run gtk.main()
        print 'gtk.main() starting... in another thread.'
        gtk.gdk.threads_init()
        gtk.main()

# AppIndicator Icon
class AITrayIcon(object):
    def __init__(self, frame):
        self.makeIndicator()
        self.thread = GtkThread()
        self.thread.start()
        print 'GtkThread started. Do you see AppIndicator?'
    
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
        print "Item '%s' selected, performing %s" % (data.get_label(),self.menuItemsMethods[data])
        self.menuItemsMethods[data]()
    
    def canToggleByClick(self):
        return False


# === wxWidgets icon ===

# wxTaskBarIcon Icon
class WXTrayIcon(wx.TaskBarIcon):
#TODO: change icon size for types of OS and tray bar
    ICO_HEIGHT = 16
    ICO_WIDTH = 16

    def __init__(self, frame):
        super(TrayIcon, self).__init__()

        self.colors = {1.0: 'green', 0.6: 'yellow', 0.3: 'red'}
        self.state = PomodoroStateProxy()
        self.frame = frame
        self.SetIcon(self.get_icon(), 'Pomodoro')
#        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.popup_menu) # check it in Windows and Linux (non-unity)
        self.make_menu()
    
    def setToggleFrameMethod(self, method):
        self.toggleFrameMethod = method
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.doToggleFrame)
    
    def doToggleFrame(self, m):
        self.toggleFrameMethod()
    
    def get_icon(self):
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
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(img)
        return icon
    
    def makeAndSetMenu(self, menuItems):
        #TODO: test in MacOS and Windows
        self.menu = wx.Menu()
        self.menuItemsDict = dict()
        for (itemName, description, method) in menuItems:
            item = self.menu.Append(wx.ID_ANY, itemName, description)
            self.menu.Bind(wx.EVT_MENU, self.menuItemSelected, item)
            self.menuItemsDict[item.GetId()] = method
    
    def menuItemSelected(self, event):
        print "Item %d selected, performing %s" % (event.GetMenuId(),self.menuItemsDict[event.GetMenuId()])
        self.menuItemsDict[event.GetMenuId()]()
    
    def CreatePopupMenu(self):
        self.make_menu()
        return self.menu
    
    def update_ui(self):
        #TODO: remove this ugly method
        self.SetIcon(self.get_icon(), 'Pomodoro %s' % self.state.text)
    
    def Close(self):
        self.RemoveIcon()
    
    def canToggleByClick(self):
        return True



# === Wrapper for tray icon controllers ===
class TaskbarIconController(object):
    def __init__(self, frame):
        self.frame = frame
        
        menuItems = [("All pomodoros", "List of pomodoros", self.listOfPomodoros),
                     ("Statistics", "Statistics", self.showStatistics),
                     ("Quit", "Quit of Pomodoro", self.quitSelected)]
        
        if have_appindicator:
            self.iconController = AITrayIcon(frame)
        else:
            self.iconController = WXTrayIcon(frame)
        
        if self.iconController.canToggleByClick():
            self.iconController.setToggleFrameMethod(self.toggleWindow)
        else:
            menuItems.insert(0, ("Toggle pomodoro window", "Show/hide window", self.toggleWindow))
        self.makeAndSetMenu(menuItems)

    def makeAndSetMenu(self, menuItems):
        self.iconController.makeAndSetMenu(menuItems)
    
    def update_ui(self):
        pass

    # menu handlers
    def listOfPomodoros(self):
        self.controller.show_list_of_pomodoros()

    def showStatistics(self):
        self.controller.show_statistics()
    
    def quitSelected(self):
        self.controller.Quit()
    
    def toggleWindow(self):
        csize = wx.ClientDisplayRect()[2:4]
        self.frame.SetPosition(map(operator.__sub__, csize, self.frame.GetSizeTuple()))
        self.frame.Show(not self.frame.IsShown())