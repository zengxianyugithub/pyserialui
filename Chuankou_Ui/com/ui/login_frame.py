# coding=utf-8
# 代码文件：chapter22/PetStore/com/zhijieketang/petstore/ui/login_frame.py

"""用户登录窗口"""
import sys
import wx
import datetime
from com.ui.my_frame import MyFrame
# from com.ui.product_list_frame import ProductListFrame

# from com.zhijieketang.petstore.dao.account_dao import AccountDao
# from com.zhijieketang.petstore.ui.my_frame import MyFrame
# from com.zhijieketang.petstore.ui.product_list_frame import ProductListFrame
#

class LoginFrame(MyFrame):
    def __init__(self, product_list_frame):
        super().__init__(title='智能抢答系统', size=(340, 230))
        self.product_list_frame = product_list_frame
        # 创建界面控件
        accountid_st = wx.StaticText(self.contentpanel, label='账号：')
        password_st = wx.StaticText(self.contentpanel, label='密码：')
        self.responder_id = wx.TextCtrl(self.contentpanel, name='responder_id')
        self.responder_txt = wx.TextCtrl(self.contentpanel, style=wx.TE_READONLY | wx.TE_MULTILINE, name='responder_txt')
        self.time2_txt = wx.TextCtrl(self.contentpanel, name='time2_txt')

        self.timer_start_point = 0

        # 创建按钮对象
        okb_btn = wx.Button(parent=self.contentpanel, label='确定')
        self.Bind(wx.EVT_BUTTON, self.okb_btn_onclick, okb_btn)
        cancel_btn = wx.Button(parent=self.contentpanel, label='取消')
        self.Bind(wx.EVT_BUTTON, self.cancel_btn_onclick, cancel_btn)

        font = wx.Font(90, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.time2_txt.SetFont(font)
        font = wx.Font(100, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.responder_id.SetFont(font)

        # 创建水平Box布局hbox对象
        # hbox = wx.BoxSizer(wx.HORIZONTAL)

        vbox1 = wx.BoxSizer(wx.VERTICAL)

        vbox1.Add(self.responder_id, -1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        vbox1.Add(self.responder_txt, -1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        # 创建FlexGrid布局fgs对象
        fgs = wx.FlexGridSizer(3, 2, 20, 20)
        fgs.AddMany([(accountid_st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
                     (password_st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
                     (self.time2_txt, 1, wx.CENTER | wx.EXPAND),
                     (vbox1, 1, wx.CENTER | wx.EXPAND),
                     (okb_btn, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
                     (cancel_btn, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE)])

        # 设置FlexGrid布局对象
        fgs.AddGrowableRow(0, 1)
        fgs.AddGrowableRow(1, 8)
        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(0, 1)
        fgs.AddGrowableCol(1, 1)



        # 创建垂直Box布局，把fgs和hbox添加到垂直Box布局对象上
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(fgs, -1, wx.CENTER | wx.ALL | wx.EXPAND, border=25)
        # vbox.Add(hbox, -1, wx.CENTER | wx.BOTTOM, border=20)

        self.contentpanel.SetSizer(vbox)

        self.timer2 = wx.Timer(self)  # 创建定时器
        self.Bind(wx.EVT_TIMER, self.OnTimer2, self.timer2)  # 绑定一个定时器事件
        # self.timer2.Start(10)

    def OnTimer2(self, evt):  # 显示时间事件处理函数

        time_now = datetime.datetime.now().strftime('%M%S%f')
        timetemp = int(int(time_now) - self.timer_start_point)

        if timetemp / 1000000 > 1:

            timetemp_min = timetemp[0:2]
            timetemp_s = '0'
        # elif len(timetemp) == 7:
        #     timetemp_min = timetemp[1:3]
        #     timetemp_s = timetemp[0]
        # elif len(timetemp) == 8:
        #     timetemp_min = timetemp[2:4]
        #     timetemp_s = timetemp[0:1]

        # timetemp = '{0}.{1}'.format(timetemp_s, timetemp_min)
        # print(timetemp)


        time2_txt = self.FindWindowByName('time2_txt')
        time2_txt.SetValue(timetemp)
        # self.statusbar1.SetStatusText(time_now, 0)  # 显示时间

    def timer2_Start(self, event):
        """打开定时器"""
        self.timer2.Start(10)

    def timer2_Stop(self, event):
        """打开定时器"""
        self.timer2.Stop()

    def okb_btn_onclick(self, event):
        """确定按钮事件处理"""

        # dao = AccountDao()
        # account = dao.findbyid(self.accountid_txt.GetValue())
        # password = self.password_txt.GetValue()

        # if account is not None and account['password'] == password:
        print('登录成功。')
        # self.product_list_frame.Show()
        # self.Hide()
        time_now = datetime.datetime.now().strftime('%M%S%f')
        timetemp = str(int(time_now) - self.timer_start_point)

        print(timetemp)

            # next_frame = ProductListFrame()
            # next_frame.Show()
            # self.Hide()

            # 登录成功保存用户Session
            # MyFrame.Session = account

        # else:
        #     print('登录失败。')
        #     dlg = wx.MessageDialog(self, '您输入的账号或密码有误，请重新输入。',
        #                            '登录失败',
        #                            wx.OK | wx.ICON_ERROR)
        #     dlg.ShowModal()
        #     dlg.Destroy()

    def cancel_btn_onclick(self, event):
        """取消按钮事件处理"""

        time_now = datetime.datetime.now().strftime('%M%S%f')
        self.timer_start_point = int(time_now)



        responder_txt = self.FindWindowByName('responder_txt')
        responder_txt.AppendText('{0}\n'.format(time_now))
        # self.timer2.Start(10)
        # 退出系统
        # self.Destroy()
        # sys.exit(0)
