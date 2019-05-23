# coding=utf-8


import wx

from com.ui.product_list_frame import ProductListFrame


class App(wx.App):

    def OnInit(self):
        # 创建窗口对象
        frame = ProductListFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()  # 进入主事件循环
