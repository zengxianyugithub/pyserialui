import time

import wx
import wx.lib.gizmos as gizmos  # Formerly wx.gizmos in Classic

#----------------------------------------------------------------------

class MyLedNum(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='nihao', size=(500, 500), style=wx.DEFAULT_FRAME_STYLE)
        # self.log = log
        self.Centre()

        panel = wx.Panel(parent=self)
        # led = gizmos.LEDNumberCtrl(self, -1, (25,25), (280, 50))
        # led.SetValue("012.34")
        #
        # led = gizmos.LEDNumberCtrl(self, -1, (25, 100), (280, 50))
        # led.SetValue("56789")
        # led.SetAlignment(gizmos.LED_ALIGN_RIGHT)
        title1 = wx.StaticText(panel, label='处理后的数据')
        processeddata = wx.TextCtrl(panel, style=wx.TE_READONLY | wx.TE_MULTILINE, name='processeddata')

        led = gizmos.LEDNumberCtrl(self, -1, (25, 200), (500, 20), gizmos.LED_ALIGN_CENTER)# | gizmos.LED_DRAW_FADED)LED_ALIGN_CENTER
        led.SetForegroundColour('red')
        led.SetBackgroundColour('white')
        led.SetDrawFaded(False)
        led.SetForegroundColour('yellow')

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(title1, 1, flag=wx.ALL | wx.EXPAND, border=5)
        box.Add(processeddata, 1, flag=wx.ALL | wx.EXPAND, border=5)
        box.Add(led, 1, flag=wx.ALL | wx.EXPAND, border=5)

        panel.SetSizer(box)

        self.clock = led
        self.OnTimer(None)

        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.OnTimer)


    def OnTimer(self, evt):
        t = time.localtime(time.time())
        st = time.strftime("%S", t)
        self.clock.SetValue(st)


    def ShutdownDemo(self):
        self.timer.Stop()
        del self.timer


class App(wx.App):

    def OnInit(self):
        # 创建窗口对象
        frame = MyLedNum()
        frame.Show()
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()  # 进入主事件循环