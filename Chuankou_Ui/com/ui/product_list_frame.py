# coding=utf-8


"""窗口"""
import threading

import wx
import wx.grid
import datetime
import re

# from com.zhijieketang.petstore.dao.product_dao import ProductDao
from com.ui.my_frame import MyFrame
# from com.zhijieketang.petstore.ui.cart_frame import CartFrame
from com.ui.product_list_gridtable import ProductListGridTable
from com.ui.login_frame import LoginFrame
import serial
import serial.serialutil
import serial.tools.list_ports

import logging
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(threadName)s - '
                           '%(name)s - %(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProductListFrame(MyFrame):
    def __init__(self):
        super().__init__(title='串口调试', size=(700, 520))

        #  购物车，键是选择的商品Id，值是商品的数量
        self.cart = {}
        # 选中商品
        self.selecteddata = {}
        self.RXnum = 0
        self.TXnum = 0
        dao = [['a', '1'], ['B', '2']]
        # 创建DAO对象
        # dao = ProductDao()
        # 查询所有数据
        self.data = dao
        self.serialcom = serial.Serial()
        self.serialcom.close()
        self.Already_opened_COM = ''
        # 创建分隔窗口



        splitter = wx.SplitterWindow(self.contentpanel, style=wx.SP_3DBORDER)
        # 创建分隔窗口中的左侧面板
        self.leftpanel = self.createleftpanel(splitter)
        # 创建分隔窗口中的右侧面板
        self.rightpanel = self.createrightpanel(splitter)

        # 设置分隔窗口左右布局
        splitter.SplitVertically(self.leftpanel,
                                 self.rightpanel,
                                 500)
        # 设置最小窗口尺寸
        splitter.SetMinimumPaneSize(200)

        # 设置整个窗口布局是垂直Box布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.contentpanel.SetSizer(vbox)

        # vbox.Add(self.createtopbox(), 1, flag=wx.EXPAND | wx.ALL, border=5)

        vbox.Add(splitter, 1, flag=wx.EXPAND | wx.ALL, border=5)
        # 添加顶部对象（topbox）到vbox
        self.timer = wx.Timer(self)  # 创建定时器
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)  # 绑定一个定时器事件
        self.timer.Start(1000)

        # 添加底部对象(splitter)到vbox
        # 创建一个子线程
        self.t1 = threading.Thread(target=self.comthread_body)
        # 启动线程t1
        # 停止当前子线程
        self.isrunning = False
        self.flagconnectcom = False
        # self.t1.join()
        # self.t1 = None

        # 在当前创建（Frame对象）创建并添加默认状态栏

        self.statusbar1 = wx.StatusBar(self, -1)
        self.statusbar1.SetFieldsCount(5)
        self.statusbar1.SetStatusWidths([-1, -2, -2, -2, -2])
        self.statusbar1.SetStatusText('准备就绪', 1)
        self.statusbar1.SetStatusText('TX:{0}'.format(self.TXnum), 2)
        self.statusbar1.SetStatusText('RX:{0}'.format(self.RXnum), 3)

        self.SetStatusBar(self.statusbar1)
        # self.CreateStatusBar()
        #
        # self.SetStatusText('准备就绪')

        # 线程体函数
        self.next_frame = LoginFrame(self)
        # self.next_frame.Show()
        # self.next_frame.ShowFullScreen(True, wx.FULLSCREEN_NOTOOLBAR)
        # self.next_frame.Hide()

    def OnTimer(self, evt):  # 显示时间事件处理函数
        t = time.localtime(time.time())
        # print(t)
        # StrYMDt = time.strftime("%Y-%B-%d:%I:%M:%S:%z:", t)
        # self.statusbar1.SetStatusText(StrYMDt, 0)  # 显示年月日
        StrIMSt = time.strftime("%I:%M:%S", t)
        self.statusbar1.SetStatusText(StrIMSt, 4)  # 显示时间

    def createtopbox(self):
        """创建顶部布局管理器topbox"""


        # 创建静态文本
        # pc_st = wx.StaticText(parent=self.contentpanel, label='选择商品类别：', style=wx.ALIGN_RIGHT)
        # dantiaodata = wx.StaticText(parent=self.contentpanel, label='单条发送数据')

        singlesenddata = wx.TextCtrl(parent=self.contentpanel, style=wx.TE_MULTILINE, name='singlesenddata')
        # 创建按钮对象
        search_btn = wx.Button(parent=self.contentpanel, label='查询')
        reset_btn = wx.Button(parent=self.contentpanel, label='重置')
        # choice = wx.Choice(self.contentpanel, choices=CATEGORYS, name='choice')
        # 绑定事件处理
        self.Bind(wx.EVT_BUTTON, self.search_btn_onclick, search_btn)
        self.Bind(wx.EVT_BUTTON, self.reset_btn_onclick, reset_btn)

        cb6 = wx.CheckBox(self.contentpanel, 6, '16进制发送')
        cb7 = wx.CheckBox(self.contentpanel, 7, '发送回车换行')
        cb8 = wx.CheckBox(self.contentpanel, 8, '定时发送')
        self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=6, id2=8)

        # vbox = wx.BoxSizer(wx.VERTICAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)

        vbox1.Add(search_btn, 1, flag=wx.FIXED_MINSIZE | wx.ALL)
        vbox1.Add(reset_btn, 1, flag=wx.FIXED_MINSIZE | wx.ALL)
        vbox2.Add(cb6, 1, flag=wx.FIXED_MINSIZE | wx.ALL)
        vbox2.Add(cb7, 1, flag=wx.FIXED_MINSIZE | wx.ALL)
        vbox2.Add(cb8, 1, flag=wx.FIXED_MINSIZE | wx.ALL)

        fgs1 = wx.FlexGridSizer(1, 3, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        # box.AddSpacer(200)
        # box.Add(dantiaodata, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)
        fgs1.Add(singlesenddata, 1, flag=wx.EXPAND | wx.ALL, border=5)
        fgs1.Add(vbox1, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)
        fgs1.Add(vbox2, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)

        fgs1.AddGrowableCol(0, 8)
        fgs1.AddGrowableCol(1, 1)
        fgs1.AddGrowableCol(2, 1)

        box.Add(fgs1, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)
        # box.AddSpacer(260)

        return box

    def createleftpanel(self, parent):
        """创建分隔窗口中的左侧面板"""

        panel = wx.Panel(parent)

        fgs = wx.FlexGridSizer(6, 1, 5, 5)

        title1 = wx.StaticText(panel, label='处理后的数据')
        processeddata = wx.TextCtrl(panel, style=wx.TE_READONLY | wx.TE_MULTILINE, name='processeddata')

        title2 = wx.StaticText(panel, label='接收的原始数据')
        receivedata = wx.TextCtrl(panel, style=wx.TE_READONLY | wx.TE_MULTILINE, name='receivedata')

        imagepath = 'resources/guanbi.jpg'
        image = wx.Bitmap(imagepath, wx.BITMAP_TYPE_ANY)
        image_sbitmap = wx.StaticBitmap(panel, bitmap=image, name='switchstate')
        # image_sbitmap = wx.BitmapButton(panel, -1, image)

        fgs.AddMany([title1, (processeddata, 1, wx.EXPAND),
                     image_sbitmap,
                     title2, (receivedata, 1, wx.EXPAND)])

        # fgs.AddGrowableRow(0, 1)
        # fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableRow(1, 5)
        # fgs.AddGrowableRow(2, 5)
        fgs.AddGrowableRow(4, 3)
        fgs.AddGrowableCol(0, 1)
        # 创建垂直Box管理管理
        box = wx.BoxSizer(wx.VERTICAL)
        # 设置垂直Box管理
        box.Add(fgs, 1, flag=wx.ALL | wx.EXPAND, border=5)
        # box.Add(tc3, 1, flag=wx.ALL | wx.EXPAND, border=5)
        panel.SetSizer(box)

        return panel

    def initgrid(self):
        """初始化网格对象"""

        # 通过网格名字获得网格对象
        grid = self.FindWindowByName('grid')

        # 创建网格中所需的表格
        table = ProductListGridTable(self.data)
        # 设置网格的表格属性
        grid.SetTable(table, True)

        rowsizeinfo = wx.grid.GridSizesInfo(40, [])
        # 设置网格所有行高
        grid.SetRowSizes(rowsizeinfo)
        colsizeinfo = wx.grid.GridSizesInfo(0, [100, 80, 130, 200])
        # 设置网格所有列宽
        grid.SetColSizes(colsizeinfo)
        # 设置单元格默认字体
        grid.SetDefaultCellFont(wx.Font(11, wx.FONTFAMILY_DEFAULT,
                                        wx.FONTSTYLE_NORMAL,
                                        wx.FONTWEIGHT_NORMAL, faceName='微软雅黑'))
        # 设置行和列标题的默认字体
        grid.SetLabelFont(wx.Font(9, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL,
                                  wx.FONTWEIGHT_NORMAL, faceName='微软雅黑'))
        # 设置网格选择模式为行选择
        grid.SetSelectionMode(grid.wxGridSelectRows)
        # 设置行不能通过拖动改变高度
        grid.DisableDragRowSize()
        # 设置列不能通过拖动改变宽度
        grid.DisableDragColSize()

    def createrightpanel(self, parent):
        """创建分隔窗口中的右侧面板"""

        panel = wx.Panel(parent, style=wx.TAB_TRAVERSAL | wx.BORDER_DOUBLE)
        panel.SetBackgroundColour(wx.WHITE)

        # hbox = wx.BoxSizer(wx.HORIZONTAL)



        com_list1 = []
        serial_port_list = list(serial.tools.list_ports.comports())
        # print(serial_port_list)
        if len(serial_port_list) == 0:
            print('无可用串口')
        else:
            for i in range(0, len(serial_port_list)):
                # print(serial_port_list[i])
                str1 = str(serial_port_list[i])
                # str2 = re.search('COM[1-9]', str1).group()
                # print(str2)
                com_list1.append(str1)

            # print(self.com_list1)

        title3 = wx.StaticText(panel, label='串口选择')

        # self.st.Clear()
        # self.st.Append('3')
        # self.st.Append('4')

        ch1 = wx.ComboBox(panel, id=30, choices=com_list1, style=wx.CB_SORT, name='comcombobox')
        # self.Bind(wx.EVT_COMBOBOX, self.on_combobox, ch1)
        self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_combobox_dropdown, ch1)
        if len(com_list1) > 0:
            ch1.SetValue(com_list1[0])
        # ch1.SetSelection(self, self.com_list1)

        botelv = wx.StaticText(panel, label='波特率')
        list2 = ['115200', '9600', '19200', '4800']
        ch2 = wx.ComboBox(panel, id=31, choices=list2, value='115200', style=wx.CB_SORT,  name='botelvvalue')
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox, ch2)

        tingzhiwei = wx.StaticText(panel, label='停止位')
        list3 = ['1', '1.5', '2']
        ch3 = wx.ComboBox(panel, id=32, choices=list3,  value='1', style=wx.CB_SORT, name='tingzhiweivalue')
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox, ch3)

        shujuwei = wx.StaticText(panel, label='数据位')
        list4 = ['5', '6', '7', '8']
        ch4 = wx.ComboBox(panel, id=33, choices=list4, value='8', style=wx.CB_SORT, name='shujuweivalue')
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox, ch4)

        jiaoyan = wx.StaticText(panel, label='奇偶校验')
        list5 = ['N', 'E', 'O', 'M', 'S']
        ch5 = wx.ComboBox(panel, id=34, choices=list5, value='N', style=wx.CB_SORT, name='jiaoyanvalue')
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox, ch5)

        chuankoucaozuo = wx.StaticText(panel, label='串口操作')
        imagepath = 'resources/1-1.jpg'  # images/' + self.data[0]['image']
        image = wx.Bitmap(imagepath, wx.BITMAP_TYPE_ANY)

        # image_sbitmap = wx.StaticBitmap(panel, bitmap=image, name='image_sbitmap')
        image_sbitmap = wx.BitmapButton(panel, 10, image, name='image_sbitmap')
        self.Bind(wx.EVT_BUTTON, self.kaiguan_btn_onclick, image_sbitmap)

        # 创建按钮对象
        savedata_btn = wx.Button(panel, id=11, label='保存窗口')
        clearrec_btn = wx.Button(panel, id=12, label='清除原数据')
        clearrechal_btn = wx.Button(panel, id=13, label='清除处理数据')
        # 绑定事件处理
        self.Bind(wx.EVT_BUTTON, self.savedata_btn_onclick, savedata_btn)
        self.Bind(wx.EVT_BUTTON, self.clear_recdata_btn_onclick, clearrec_btn)
        self.Bind(wx.EVT_BUTTON, self.clear_recdata_btn_onclick, clearrechal_btn)

        cb1 = wx.CheckBox(panel, 1, '16进制显示', name='rxhexdisplay')
        cb2 = wx.CheckBox(panel, 2, '白底黑字')
        cb2.SetValue(True)
        cb3 = wx.CheckBox(panel, 3, 'RTS')
        cb4 = wx.CheckBox(panel, 4, 'DTR')
        cb5 = wx.CheckBox(panel, 5, '时间戳')
        self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=1, id2=5)

        fgs = wx.FlexGridSizer(10, 2, 5, 5)

        fgs.AddMany([title3, (ch1, 1, wx.EXPAND),
                    botelv, (ch2, 1, wx.EXPAND),
                    tingzhiwei, (ch3, 1, wx.EXPAND),
                    shujuwei, (ch4, 1, wx.EXPAND),
                    jiaoyan, (ch5, 1, wx.EXPAND),
                     chuankoucaozuo, (image_sbitmap, 1, wx.EXPAND),
                     (clearrechal_btn, 1, wx.EXPAND), (clearrec_btn, 1, wx.EXPAND),
                     (savedata_btn, 1, wx.EXPAND),
                     (cb1, 1, wx.ALL), (cb2, 1, wx.ALL),
                     (cb3, 1, wx.ALL), (cb4, 1, wx.ALL),
                     (cb5, 1, wx.ALL)
                     ])

        fgs.AddGrowableCol(0, 1)
        fgs.AddGrowableCol(1, 1)

        #数据发送框
        singlesenddata = wx.TextCtrl(panel, style=wx.TE_MULTILINE, name='singlesenddata') # TE_READONLY

        # 创建按钮对象
        senddata = wx.Button(panel, label='发送')
        reset_alldata = wx.Button(panel, label='清除发送')

        # 绑定事件处理
        self.Bind(wx.EVT_BUTTON, self.senddata_btn_onclick, senddata)
        self.Bind(wx.EVT_BUTTON, self.clear_senddata_btn_onclick, reset_alldata)

        cb6 = wx.CheckBox(panel, 6, '16进制发送', name='hexsenddata')
        cb7 = wx.CheckBox(panel, 7, '发送回车换行', name='huichehuanhang')
        cb8 = wx.CheckBox(panel, 8, '定时ms发送')
        self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=6, id2=8)
        timingms = wx.TextCtrl(panel, size=[50, 20], name='timingms')


        hbox11 = wx.BoxSizer(wx.HORIZONTAL)
        vbox11 = wx.BoxSizer(wx.VERTICAL)
        vbox21 = wx.BoxSizer(wx.VERTICAL)

        vbox11.Add(senddata, 1, flag=wx.FIXED_MINSIZE | wx.ALL)
        vbox11.AddSpacer(20)
        vbox11.Add(reset_alldata, 1, flag=wx.FIXED_MINSIZE | wx.ALL)
        vbox21.Add(cb6, 1, flag=wx.FIXED_MINSIZE | wx.ALL)
        vbox21.Add(cb7, 1, flag=wx.FIXED_MINSIZE | wx.ALL)
        vbox21.Add(cb8, 1, flag=wx.FIXED_MINSIZE | wx.ALL)
        vbox21.Add(timingms, 1, flag=wx.FIXED_MINSIZE | wx.ALL)

        hbox11.AddMany([(vbox11, 1, wx.EXPAND),
                        (vbox21, 1, wx.EXPAND)
                      ])

        fgs1 = wx.FlexGridSizer(2, 1, 5, 5)

        fgs1.AddMany([(singlesenddata, 1, wx.EXPAND),
                      (hbox11, 1, wx.EXPAND)
                     ])

        fgs1.AddGrowableCol(0, 1)
        fgs1.AddGrowableRow(0, 5)
        fgs1.AddGrowableRow(1, 1)
        # hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # hbox1.Add(statictext, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        # hbox1.Add(cb1, 1, flag=wx.ALL | wx.FIXED_MINSIZE)
        # hbox1.Add(cb2, 1, flag=wx.ALL | wx.FIXED_MINSIZE)
        # hbox1.Add(cb3, 1, flag=wx.ALL | wx.FIXED_MINSIZE)



        # 显示第一张图片

        # 商品市场价格
        # slistprice = "商品市场价：￥{0:.2f}".format(1)
        # listprice_st = wx.StaticText(panel, label=slistprice, name='listprice')
        # # 市场价格
        # sunitcost = "商品单价：￥{0:.2f}".format(2)
        # unitcost_st = wx.StaticText(panel, label=sunitcost, name='unitcost')
        # # 商品描述
        # descn = "商品描述：{0}".format(3)
        # descn_st = wx.StaticText(panel, label=descn, name='descn')

        # vbox.Add(self.createtopbox(), 1, flag=wx.EXPAND | wx.ALL, border=5)

        # 创建垂直Box布局管理器
        box = wx.BoxSizer(wx.VERTICAL)
        # box.AddSpacer(50)
        # box.Add(title3, 1, flag=wx.ALL | wx.EXPAND, border=0)
        box.Add(fgs, 1, flag=wx.ALL | wx.EXPAND, border=5)
        box.Add(fgs1, 1, flag=wx.ALL | wx.EXPAND, border=5)
        # box.Add(self.createtopbox(), 1, flag=wx.CENTER | wx.ALL, border=5)
        # box.AddSpacer(220)
        # box.Add(listprice_st, 1, flag=wx.EXPAND | wx.ALL, border=10)
        # box.Add(unitcost_st, 1, flag=wx.EXPAND | wx.ALL, border=10)
        # box.Add(descn_st, 1, flag=wx.EXPAND | wx.ALL, border=10)
        # box.AddSpacer(20)
        # box.Add(addcart_btn, 1, flag=wx.EXPAND | wx.ALL, border=5)
        # box.Add(seecart_btn, 1, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(box)

        return panel

    def search_btn_onclick(self, event):
        """查询按钮事件处理"""
        print('search')
        # 通过名字查询choice控件
        #
        receivedata = self.FindWindowByName('receivedata')
        print(receivedata)
        str = receivedata.GetValue()
        print(str)
        # # 获得选中类别索引
        # selectcatidx = choice.GetSelection()
        # if selectcatidx >= 0:
        #     # 获得选中的商品类别
        #     catname = CATEGORYS[selectcatidx]

            # 根据类别查询商品
            # dao = ProductDao()
            # self.data = dao.findbycat(catname)
            # # 初始化网格
            # self.initgrid()

    def reset_btn_onclick(self, event):
        """重置按钮事件处理"""
        print('reset')
        processeddata = self.FindWindowByName('processeddata')
        print(processeddata)
        processeddata.SetValue('处理数据')
        # str = receivedata.GetValue()
        # print(str)
        # 查询所有商品
        # dao = ProductDao()
        # self.data = dao.findall()
        # # 初始化网格
        # self.initgrid()

    def addcart_btn_onclick(self, event):
        """添加到购物车事件处理"""
        print('addcart')
        # if len(self.selecteddata) == 0:
        #     self.SetStatusText('请先选择商品')
        #     return
        #
        # # 获得选择的商品id
        productid = 2
        # if productid in self.cart.keys():  # 判断购物车中已经有该商品
        #     # 获得商品数量
        #     quantity = self.cart[productid]
        #     self.cart[productid] = (quantity + 1)
        # else:  # 购物车中还没有该商品
        #     self.cart[productid] = 1

        # 显示在状态栏
        # self.SetStatusText('商品{0}添加到购物车'.format(productid))
        print(self.cart)

    def seecart_btn_onclick(self, event):
        """查看添加到购物车事件处理"""
        print('see_cart')
        # next_frame = CartFrame(self.cart, self)
        # next_frame.Show()
        # self.Hide()

    def selectrow_handler(self, event):
        """选择网格行事件处理"""
        print('selecrow')
        # srowidx = event.GetRow()
        # if srowidx >= 0:
        #     print(self.data[srowidx])
        #     self.selecteddata = self.data[srowidx]
        #     self.SetStatusText('选择第{0}行数据'.format(srowidx + 1))
        #
        #     # 显示选择的图片
        #     imagepath = 'resources/images/' + self.selecteddata['image']
        #     image = wx.Bitmap(imagepath, wx.BITMAP_TYPE_ANY)
        #     # 通过名字查询子窗口
        #     image_sbitmap = self.FindWindowByName('image_sbitmap')
        #     image_sbitmap.SetBitmap(image)
        #
        #     # 商品市场价格
        #     slistprice = "商品市场价：￥{0:.2f}".format(self.selecteddata['listprice'])
        #     listprice_st = self.FindWindowByName('listprice')
        #     listprice_st.SetLabelText(slistprice)
        #
        #     # 市场价格
        #     sunitcost = "商品单价：￥{0:.2f}".format(self.selecteddata['unitcost'])
        #     unitcost_st = self.FindWindowByName('unitcost')
        #     unitcost_st.SetLabelText(sunitcost)
        #
        #     # 商品描述
        #     descn = "商品描述：{0}".format(self.selecteddata['descn'])
        #     descn_st = self.FindWindowByName('descn')
        #     descn_st.SetLabelText(descn)
        #
        #     self.rightpanel.Layout()

        event.Skip()

    def on_combobox_dropdown(self, event):
        event_id = event.GetId()
        # print('event_id = {0} 选择'.format(event_id))
        # print(event)
        # list2 = []
        # self.com_list1 = ['com1', 'com2']
        #
        #
        # comcombobox.Append('3')
        # comcombobox.Append('4')
        if event_id == 30:
            comcombobox = self.FindWindowByName('comcombobox')
            # if len(self.com_list1) > 0:
            #     print(len(self.com_list1))
            #     del self.com_list1[-len(self.com_list1):]

            comcombobox.Clear()
            serial_port_list = list(serial.tools.list_ports.comports())
            # print(str(serial_port_list))

            if len(serial_port_list) == 0:
                print('无可用串口')
            else:
                # plist_0 = list(serial_port_list[0])
                # serialName = plist_0[1]
                # print(serialName)
                for i in range(0, len(serial_port_list)):
                    str1 = str(serial_port_list[i])
                    # str2 = re.search('COM[1-9]', str1)
                    # if str2 is None:
                    #     print('No available serial port')
                    # else:
                    #     str2 = str2.group()
                    print(str1)
                    comcombobox.Append(str1)

                # print(self.com_list1)
                # comcombobox = self.FindWindowByName('comcombobox')
                # comcombobox.Layout()
                # TODO


    def on_combobox(self, event):
        str1 = event.GetString()
        event_id = event.GetId()
        print('event_id = {1} 选择 {0}'.format(str1, event_id))




    def kaiguan_btn_onclick(self, event):
        print('选择 {0}'.format(event.GetId()))
        # image_sbitmap = self.FindWindowByName('image_sbitmap')
        # image_sbitmap.ConvertToDisabled()

        # self.isrunning = False
        # self.t1.join()
        # self.t1 = None
        print(str(self.t1))
        if re.search('stopped', str(self.t1)) is None:
            print('没有线程等待关闭')
        else:
            print('有停止的线程等待关闭')
            self.t1.join()
            self.t1 = None
        # else:
        #     self.t1.join()
        #     self.t1 = None

        if self.serialcom.is_open == True:
            if self.isrunning == True:
                self.flagconnectcom = False
                # 停止当前子线程
                self.isrunning = False
                self.t1.join()
                self.t1 = None
            self.serialcom.close()  # 关闭串口
            self.Already_opened_COM = ' '  # 清除串口号
            print('关闭串口,停止线程')
            # 显示选择的图片
            imagepath = 'resources/guanbi.jpg'
            image = wx.Bitmap(imagepath, wx.BITMAP_TYPE_ANY)
            # 通过名字查询子窗口
            switchstate = self.FindWindowByName('switchstate')
            switchstate.SetBitmap(image)
            #// self.SetStatusText('串口已关闭')
        else:

            if self.isrunning == True:

                # 停止当前子线程
                self.isrunning = False
                self.flagconnectcom = False
                self.t1.join()
                self.t1 = None
            print('请求打开串口')
            comcombobox = self.FindWindowByName('comcombobox').GetValue()
            print(comcombobox)
            botelvvalue = self.FindWindowByName('botelvvalue').GetValue()
            tingzhiweivalue = self.FindWindowByName('tingzhiweivalue').GetValue()
            shujuweivalue = self.FindWindowByName('shujuweivalue').GetValue()
            jiaoyanvalue = self.FindWindowByName('jiaoyanvalue').GetValue()
            # tingzhiweivalue = self.FindWindowByName('tingzhiweivalue').GetValue()
            # tingzhiweivalue = self.FindWindowByName('tingzhiweivalue')
            print('{0}, {1}, {2}, {3}, {4}'.format(comcombobox, botelvvalue,
                                                   tingzhiweivalue, shujuweivalue,
                                                   jiaoyanvalue))
            # comcombobox = comcombobox[0:4]
            comcombobox1 = re.search('COM\d{2}', comcombobox)#.group()
            print(str(comcombobox1))
            if comcombobox1 is None:
                comcombobox = re.search('COM[1-9]', comcombobox)
                # print(comcombobox.group())
            else:
                comcombobox = comcombobox1

            if comcombobox is None:
                print('COM is none')
                logger.info('无可用串口')
                dlg = wx.MessageDialog(self, '请选择可用串口',
                                       '打开串口失败',
                                       wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                comcombobox = comcombobox.group()
                if comcombobox[0:3] == 'COM':
                    try:
                        timex = 0
                        self.serialcom = serial.Serial(port=comcombobox, baudrate=botelvvalue,
                                                       bytesize=int(shujuweivalue), stopbits=int(tingzhiweivalue),
                                                       parity=jiaoyanvalue,
                                                       timeout=timex)
                        print("串口详情参数：", self.serialcom)
                        self.Already_opened_COM = comcombobox  # 保存串口号
                        # print(ser.is_open)
                        # self.SetStatusText('串口已打开')
                        #// 十六进制的发送
                        # result = ser.write(chr(0x06).encode("utf-8"))  # 写数据
                        # print("写总字节数:", result)

                        # 十六进制的读取
                        # print(ser.read().hex())  # 读一个字节

                        # print("---------------")
                        # if self.isrunning == False:
                        #     self.serialcom.close()  # 关闭串口
                        #     print('停止线程关闭串口！！')
                        imagepath = 'resources/dakai.jpg'
                        image = wx.Bitmap(imagepath, wx.BITMAP_TYPE_ANY)
                        # 通过名字查询子窗口
                        switchstate = self.FindWindowByName('switchstate')
                        switchstate.SetBitmap(image)
                    except Exception as e:
                        print("---异常---：", e)
                        dlg = wx.MessageDialog(self, str(e),
                                               '打开串口失败',
                                               wx.OK | wx.ICON_ERROR)
                        dlg.ShowModal()
                        dlg.Destroy()
                else:
                # print('无可用串口')
                #// self.SetStatusText('准备就绪')
                    logger.info('无可用串口')
                    dlg = wx.MessageDialog(self, '没有可用串口',
                                           '打开串口失败',
                                           wx.OK | wx.ICON_ERROR)
                    dlg.ShowModal()
                    dlg.Destroy()

            if self.serialcom.is_open == True:
                self.resettread()

        # print(self.Already_opened_COM)

    def on_checkbox_click(self, event):
        cb = event.GetEventObject()
        event_id = event.GetId()
        print('选择 {0}，状态{1}, ID{2}'.format(cb.GetLabel(), event.IsChecked(), event_id))

        #
        # print(rxhexdisplay.IsChecked())next_frame.
        if event_id == 1:
            receivedata = self.FindWindowByName('receivedata')

            strtemp = receivedata.GetValue()
            receivedata.Clear()
            if event.IsChecked() == True:

                # print(type(strtemp))
                # print(strtemp.encode("gbk"))
                try:
                    receivedata.AppendText((strtemp.encode("gbk")).hex())

                except Exception as e:
                    # print("---异常---：", e)
                    logger.info(e)

            else:
                try:
                    receivedata.AppendText((bytes.fromhex(strtemp).decode("gbk")))
                except Exception as e:
                    # print("---异常---：", e)
                    logger.info(e)
            # receivedata.AppendText(strrcd.decode("gbk"))

        if event_id == 4:
            if event.IsChecked() == True:
                print('id=4')
                try:
                    self.next_frame.timer2_Start(event)
                    accountid_st = self.FindWindowByName('responder_txt')
                    print(accountid_st.GetValue())
                except Exception as e:
                    # print("---异常---：", e)
                    logger.info(e)
            else:
                self.next_frame.timer2_Stop(event)


        if event_id == 5:
            if event.IsChecked() == True:
                # next_frame = LoginFrame(self)
                self.next_frame.Show()
                self.next_frame.ShowFullScreen(True, wx.FULLSCREEN_NOMENUBAR)
                # self.next_frame
            else:
                self.next_frame.Hide()
                # self.Hide()

        if event_id == 6:
            singlesenddata = self.FindWindowByName('singlesenddata')

            strtemp = singlesenddata.GetValue()
            singlesenddata.Clear()
            if event.IsChecked() == True:

                # print(type(strtemp))
                # print(strtemp.encode("gbk"))
                try:
                    singlesenddata.AppendText((strtemp.encode("gbk")).hex())

                except Exception as e:
                    # print("---异常---：", e)
                    logger.info(e)

            else:
                try:
                    singlesenddata.AppendText((bytes.fromhex(strtemp).decode("gbk")))
                except Exception as e:
                    # print("---异常---：", e)
                    logger.info(e)
            # receivedata.AppendText(strrcd.decode("gbk"))

        elif event_id == 8:
            if event.IsChecked() == True:
                timingms = self.FindWindowByName('timingms')
                print(timingms.GetValue())



    def savedata_btn_onclick(self, event):
        print('保存接收数据')
        receivedata = self.FindWindowByName('receivedata')
        receivedata.AppendText('保存窗口')

        processeddata = self.FindWindowByName('processeddata')
        processeddata.AppendText('保存窗口')

    def clear_recdata_btn_onclick(self, event):
        event_id = event.GetId()
        if event_id == 12:
            print('清空接收原始数据 id {0}'.format(event_id))
            receivedata = self.FindWindowByName('receivedata')
            # receivedata.SetValue('')
            self.RXnum = 0
            self.statusbar1.SetStatusText('RX:{0}'.format(self.RXnum), 3)
            receivedata.Clear()
            # receivedata.AppendText('保存窗口')
        else:
            print('清空接收处理数据 id {0}'.format(event_id))
            processeddata = self.FindWindowByName('processeddata')
            processeddata.SetValue('')
        # print(singlesenddata.GetValue())

    def senddata_btn_onclick(self, event):
        # print('发送数据按键')
        singlesenddata = self.FindWindowByName('singlesenddata')
        strsd = singlesenddata.GetValue()
        # print(strsd)
        try:
            if self.serialcom.is_open == True:
                hexsenddata = self.FindWindowByName('hexsenddata')
                res = 0
                if hexsenddata.IsChecked() == True:
                    try:
                        res = self.serialcom.write(bytes.fromhex(strsd))
                    except Exception as e:
                        logger.info(e)
                else:
                    res = self.serialcom.write(strsd.encode("gbk"))
                if res > 0:
                    # print(res)
                    self.TXnum += res
                    self.statusbar1.SetStatusText('TX:{0}'.format(self.TXnum), 2)
                    if hexsenddata.IsChecked() == True:
                        print('发送数据:{0}'.format(bytes.fromhex(strsd)))
                    else:
                        print('发送数据:{0}'.format(strsd))

                    huichehuanhang = self.FindWindowByName('huichehuanhang')

                    if huichehuanhang.IsChecked() == True:
                        res = self.serialcom.write(chr(0x0D).encode("gbk"))  # 写数据
                        self.TXnum += res
                        self.statusbar1.SetStatusText('TX:{0}'.format(self.TXnum), 2)
                        res = self.serialcom.write(chr(0x0A).encode("gbk"))  # 写数据
                        self.TXnum += res
                        self.statusbar1.SetStatusText('TX:{0}'.format(self.TXnum), 2)

                        print('{0}{1}'.format(chr(0x0D).encode("gbk"), chr(0x0A).encode("gbk")))

                    self.statusbar1.SetStatusText('发送完成', 1)

            else:
                logger.info('没有打开串口')
                dlg = wx.MessageDialog(self, '没有打开串口',
                                           '请打开串口',
                                           wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
        except Exception as e:

            logger.info(e)
            if self.isrunning == True:
                # self.flagconnectcom = False
                # 停止当前子线程
                self.isrunning = False
                self.flagconnectcom = False
                self.t1.join()
                self.t1 = None
            self.serialcom.close()  # 关闭串口
            imagepath = 'resources/guanbi.jpg'
            image = wx.Bitmap(imagepath, wx.BITMAP_TYPE_ANY)
            # 通过名字查询子窗口
            switchstate = self.FindWindowByName('switchstate')
            switchstate.SetBitmap(image)
            print('异常停止线程关闭串口')

    def clear_senddata_btn_onclick(self, event):
        print('清空发送数据')
        singlesenddata = self.FindWindowByName('singlesenddata')
        singlesenddata.Clear()
        # strs = singlesenddata.GetValue()
        # strss = self.str_to_hex(strs)
        # singlesenddata.SetValue(strss)
        self.statusbar1.SetStatusText('清除数据', 1)
        self.TXnum = 0
        self.statusbar1.SetStatusText('TX:{0}'.format(self.TXnum), 2)
        print(singlesenddata.GetValue())

    # def comrequest(self):

    def comthread_body(self):
        # 当前线程对象
        print('线程开始运行')
        # comcombobox = self.FindWindowByName('comcombobox').GetValue()
        # print(comcombobox)
        # botelvvalue = self.FindWindowByName('botelvvalue').GetValue()
        # tingzhiweivalue = self.FindWindowByName('tingzhiweivalue').GetValue()
        # shujuweivalue = self.FindWindowByName('shujuweivalue').GetValue()
        # jiaoyanvalue = self.FindWindowByName('jiaoyanvalue').GetValue()
        # # tingzhiweivalue = self.FindWindowByName('tingzhiweivalue').GetValue()
        # # tingzhiweivalue = self.FindWindowByName('tingzhiweivalue')
        # print('{0}, {1}, {2}, {3}, {4}'.format(comcombobox, botelvvalue,
        #                                        tingzhiweivalue, shujuweivalue,
        #                                        jiaoyanvalue))
        # comcombobox = comcombobox[0:4]
        # print(comcombobox)
        #
        # if comcombobox[0:3] == 'COM':
        #     try:
        #         timex = 5
        #         self.serialcom = serial.Serial(port=comcombobox, baudrate=botelvvalue,
        #                             bytesize=int(shujuweivalue), stopbits=int(tingzhiweivalue),
        #                             parity=jiaoyanvalue,
        #                             timeout=timex)
        #         print("串口详情参数：", self.serialcom)
        #         # print(ser.is_open)
        #         self.SetStatusText('串口已打开')
        #         # 十六进制的发送
        #         # result = ser.write(chr(0x06).encode("utf-8"))  # 写数据
        #         # print("写总字节数:", result)
        #
        #         # 十六进制的读取
        #         # print(ser.read().hex())  # 读一个字节
        #
        #         # print("---------------")
        #         if self.isrunning == False:
        #             self.serialcom.close()  # 关闭串口
        #             print('停止线程关闭串口！！')
        #
        #     except Exception as e:
        #         print("---异常---：", e)
        # else:
        #     # print('无可用串口')
        #     logger.info('无可用串口')
        #     dlg = wx.MessageDialog(self, '没有可用串口',
        #                            '打开串口失败',
        #                            wx.OK | wx.ICON_ERROR)
        #     dlg.ShowModal()
        #     dlg.Destroy()
        # 循环接收等待下一个字节的时间
        # timeoutcom = 0.0000001  # 5 / self.serialcom.get_settings().get('baudrate')
        timeoutcom =10 / (self.serialcom.get_settings().get('baudrate'))
        # print(type(timeoutcom))
        print(timeoutcom)
        while self.isrunning:
            try:
                if (self.serialcom.is_open):
                    # #######
                    # n = self.serialcom.inWaiting()
                    # if n:
                    #     data = data + self.serialcom.read(n)
                    #     print('get data from serial port:', data)
                    #     print(type(data))
                    #
                    # n = self.serialcom.inWaiting()
                    # if len(data) > 0 and n == 0:
                    #     try:
                    #         temp = data.decode('gb18030')
                    #         print(type(temp))
                    #         print(temp)
                    #         car, temp = str(temp).split("\n", 1)
                    #         print(car, temp)
                    #
                    #         string = str(temp).strip().split(":")[1]
                    #         str_ID, str_data = str(string).split("*", 1)
                    #
                    #         print(str_ID)
                    #         print(str_data)
                    #         print(type(str_ID), type(str_data))
                    #
                    #         if str_data[-1] == '*':
                    #             break
                    #         else:
                    #             print(str_data[-1])
                    #             print('str_data[-1]!=*')
                    #     except:
                    #         print("读卡错误，请重试！\n")
                    # #######
                    ###
                    self.flagconnectcom = False
                    # str2 = re.search('COM[1-9]', str1)
                    # if str2 is None:
                    #     print('No available serial port')
                    # else:
                    #     str2 = str2.group()
                    serial_port_list2 = list(serial.tools.list_ports.comports())
                    if len(serial_port_list2) == 0:
                        print('打开的串口不存在了')
                        self.serialcom.close()  # 关闭串口
                        imagepath = 'resources/guanbi.jpg'
                        image = wx.Bitmap(imagepath, wx.BITMAP_TYPE_ANY)
                        # 通过名字查询子窗口
                        switchstate = self.FindWindowByName('switchstate')
                        switchstate.SetBitmap(image)
                        comcombobox = self.FindWindowByName('comcombobox')
                        comcombobox.Clear()
                        self.isrunning = False
                        # self.Already_opened_COM = ''

                    else:
                        for i in range(0, len(serial_port_list2)):
                            plist_0 = list(serial_port_list2[i])
                            # serialName = plist_0[0]
                            if self.Already_opened_COM == plist_0[0]:
                                self.flagconnectcom = True
                    if  self.flagconnectcom == True:
                        strrcd = self.serialcom.read(self.serialcom.in_waiting)
                        if (len(strrcd)):
                            whilet = True
                            while whilet:
                                time.sleep(timeoutcom)
                                # print(self.Already_opened_COM)
                                n1 = self.serialcom.inWaiting()
                                # print(self.serialcom.get_settings())
                                if n1 > 0:
                                    strrcd = strrcd + self.serialcom.read(n1)
                                else:
                                    whilet = False
                                # print('次数{0}'.format(n1))
                            # str2 = strrcd.hex()
                            # print(type(str2))
                            #
                            # print(str2)
                            # print(bytes.fromhex(str2))

                            print('接收到数据{0}'.format(strrcd))
                            self.RXnum += len(strrcd)
                            self.statusbar1.SetStatusText('RX:{0}'.format(self.RXnum), 3)

                            receivedata = self.FindWindowByName('receivedata')
                            #16进制显示
                            rxhexdisplay = self.FindWindowByName('rxhexdisplay')
                            # print(rxhexdisplay.IsChecked())
                            if rxhexdisplay.IsChecked() == True:
                                receivedata.AppendText(strrcd.hex())
                            else:
                                try:
                                    receivedata.AppendText(strrcd.decode("gbk"))
                                except Exception as e:
                                    logger.info(e)

                    else:
                        print('打开的串口不存在了')
                        self.serialcom.close()  # 关闭串口
                        imagepath = 'resources/guanbi.jpg'
                        image = wx.Bitmap(imagepath, wx.BITMAP_TYPE_ANY)
                        # 通过名字查询子窗口
                        switchstate = self.FindWindowByName('switchstate')
                        switchstate.SetBitmap(image)
                        comcombobox = self.FindWindowByName('comcombobox')
                        comcombobox.Clear()
                        self.isrunning = False

                    ###

                        # print(self.RXnum)
                        # strrcd = ''
                # else:

                #     comcombobox = self.FindWindowByName('comcombobox').GetValue()
                #     comcombobox.SetValue('')
            except Exception:
                continue
                print('线程异常')
        # time.sleep(2)
        # print('线程没有关闭')
        # TODO

    # 重启子线程
    def resettread(self):
        # 子线程运行状态
        self.isrunning = True
        # 创建一个子线程
        self.t1 = threading.Thread(target=self.comthread_body)
        # 启动线程t1
        self.t1.start()

    def OnClose(self, event):
        self.timer.Stop()
        # 停止当前子线程
        if self.isrunning == True:
            self.isrunning = False
            self.t1.join()
            self.t1 = None

        # 关闭窗口，并退出系统
        super().OnClose(event)

