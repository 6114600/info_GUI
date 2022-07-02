import wx
from utils import get_textctrl_bold
from utils.getData import get_data
from utils.PandasToGrid import PandasToGrid
from utils import load_config_file

# 此面板还需实现的功能
# 数据库联动
# 其他按钮功能

class CbPanel(wx.Panel):
    def __init__(self, parent, frame):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        self.config = load_config_file()
        self.parent = parent

        vbox = wx.BoxSizer(wx.VERTICAL)
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        h3 = wx.BoxSizer(wx.HORIZONTAL)
        fontButton = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)

        self.text1 = get_textctrl_bold(self,'抄表中心',40)
        self.text2 = get_textctrl_bold(self, '定时抄表状态：', 25)
        self.text3 = get_textctrl_bold(self, '已开启' if self.config['dscb'] else '已关闭',22)
        h1.Add(self.text2,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        h1.AddSpacer(20)
        h1.Add(self.text3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.button1 = wx.Button(self,-1,'立即抄表',size=(300,100))
        self.button1.SetFont(fontButton)
        self.button2 = wx.Button(self, -1, '抄表日志', size=(300, 100))
        self.button2.SetFont(fontButton)
        h2.Add(self.button1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        h2.AddSpacer(20)
        h2.Add(self.button2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        h2.AddSpacer(20)
        self.button3 = wx.Button(self, -1, '抄表设置', size=(300, 100))
        self.button3.SetFont(fontButton)
        self.button4 = wx.Button(self, -1, '关闭定时', size=(300, 100))
        self.button4.SetFont(fontButton)
        h3.Add(self.button3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        h3.AddSpacer(20)
        h3.Add(self.button4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        h3.AddSpacer(20)

        vbox.AddSpacer(40)
        vbox.Add(self.text1,0,wx.ALL|wx.ALIGN_CENTER)
        vbox.AddSpacer(80)
        vbox.Add(h1, 0, wx.ALL | wx.ALIGN_CENTER)
        vbox.AddSpacer(40)
        vbox.Add(h2, 0, wx.ALL | wx.ALIGN_CENTER)
        vbox.AddSpacer(40)
        vbox.Add(h3, 0, wx.ALL | wx.ALIGN_CENTER)
        self.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON,self.parent.ToSettingPanel,self.button3)

    def OnLJCB(self,event):
        pass
        # TODO: 服务器立即读取三表数据存入数据库中

    def OnCBRZ(self,event):
        pass

        # TODO： 读取本地日志文件或读取数据库文件

    def OnCBSZ(self,event):
        pass
