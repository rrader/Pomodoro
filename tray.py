import wx
from state import PomodoroState
import operator

class TrayIcon(wx.TaskBarIcon):
    ICO_HEIGHT = 16
    ICO_WIDTH = 16
    
    def __init__(self,frame):
        super(TrayIcon, self).__init__()
        
        self.colors = {1.0: "green", 0.6: "yellow", 0.3: "red"}
        self.state = PomodoroState()
        self.frame = frame
        self.SetIcon(self.get_icon(), "Pomodoro")
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.toggle_frame)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(1000)
        
    def toggle_frame(self, m):
        f = self.frame
        csize = wx.ClientDisplayRect()[2:4]
        f.SetPosition(map(operator.__sub__,csize,f.GetSizeTuple()))
        f.Show(not f.IsShown())
        
    def get_icon(self):
        h = int(self.state.percent*self.ICO_HEIGHT)
        
        img = wx.EmptyBitmap(self.ICO_WIDTH,self.ICO_HEIGHT)
        dc = wx.MemoryDC(img)
        dc.Brush = wx.Brush("white", wx.TRANSPARENT)
        dc.Clear()
        col = self.colors[min(filter(lambda x: self.state.percent<=x, self.colors))]
        if not self.state.active:
            col = "white"
        dc.Brush = wx.Brush(col)
        dc.DrawRectangle(3,self.ICO_HEIGHT-h,10,h)
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(img)
        return icon
    
    def OnTimer(self, m):
        self.SetIcon(self.get_icon(), "Pomodoro %s" % self.state.text)