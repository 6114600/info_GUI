import wx
from utils import get_textctrl_bold


class LoginPanel(wx.Panel):
    def __init__(self, parent, frame):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        Box = wx.BoxSizer(wx.VERTICAL)

        text1 = get_textctrl_bold(self,'水电信息管理系统',24)

        h1 = wx.BoxSizer(wx.HORIZONTAL)
        text2 = get_textctrl_bold(self,'账号',18)
        self.textbox1 = wx.TextCtrl(self,-1,"",size=(200,-1))
        h1.Add(text2,0,wx.ALL | wx.ALIGN_LEFT)
        h1.AddSpacer(30)
        h1.Add(self.textbox1, 0, wx.ALL | wx.ALIGN_LEFT)

        h2 = wx.BoxSizer(wx.HORIZONTAL)
        text3 = get_textctrl_bold(self, '密码', 18)
        self.textbox2 = wx.TextCtrl(self, -1, "", size=(200, -1),style = wx.TE_PASSWORD)
        h2.Add(text3, 0, wx.ALL | wx.ALIGN_LEFT)
        h2.AddSpacer(30)
        h2.Add(self.textbox2, 0, wx.ALL | wx.ALIGN_LEFT)

        self.button1 = wx.Button(self,-1,'登录',size=(300,60))

        Box.AddSpacer(30)
        Box.Add(text1, 0, wx.ALL | wx.ALIGN_CENTER)
        Box.AddSpacer(30)
        Box.Add(h1,0,wx.ALL | wx.ALIGN_CENTER)
        Box.AddSpacer(30)
        Box.Add(h2, 0, wx.ALL | wx.ALIGN_CENTER)
        Box.AddSpacer(20)
        Box.Add(self.button1,0,wx.ALL | wx.ALIGN_CENTER)
        self.Box = Box
        self.SetSizer(self.Box)

        self.Bind(wx.EVT_BUTTON,self.OnLogin,self.button1)

        self.login_flag = False

    def OnLogin(self,event):
        username = self.textbox1.GetValue()
        pasw = self.textbox2.GetValue()
        # TODO:通过数据库查询用户信息与密码，得到匹配的正确密码
        correct_pasw = '123456'
        if pasw == correct_pasw:
            self.Box.Clear(True)
            text4 = get_textctrl_bold(self, username+'  您好！', 20)
            # t = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
            # self.text5 = get_textctrl_bold(self, t, 16)
            text6 = get_textctrl_bold(self, '请选择左侧房间与右上角功能选项以开始使用', 20)
            self.Box.Add(text4, 0, wx.ALL | wx.ALIGN_CENTER)
            self.Box.AddSpacer(20)
            # self.new_box.Add(self.text5, 0, wx.ALL | wx.ALIGN_CENTER)
            # self.new_box.AddSpacer(20)
            self.Box.Add(text6, 0, wx.ALL | wx.ALIGN_CENTER)
            self.SetSizer(self.Box)
            self.login_flag = True
        else:
            wx.MessageBox('密码错误，请重试。',caption='错误')