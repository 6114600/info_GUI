import wx
from utils import get_textctrl_bold
from utils.getData import get_login_info

# 该面板还需实现的功能
# 与数据库的联动，包括密码验证、身份设定等
# 账号输入框、密码输入框的输入限制



class LoginPanel(wx.Panel):
    def __init__(self, parent, frame):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        self.parent = parent
        # 定义布局器Boxsizer
        Box = wx.BoxSizer(wx.VERTICAL)

        text1 = get_textctrl_bold(self,'水电信息管理系统',24)

        # 嵌套子布局器1，横向
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        text2 = get_textctrl_bold(self,'账号',18)
        self.textbox1 = wx.TextCtrl(self,-1,"",size=(200,-1))  # 账号输入框控件
        h1.Add(text2,0,wx.ALL | wx.ALIGN_LEFT)
        h1.AddSpacer(30)
        h1.Add(self.textbox1, 0, wx.ALL | wx.ALIGN_LEFT)

        # 嵌套子布局器2，横向
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        text3 = get_textctrl_bold(self, '密码', 18)
        self.textbox2 = wx.TextCtrl(self, -1, "", size=(200, -1),style = wx.TE_PASSWORD)  # 密码输入框控件
        h2.Add(text3, 0, wx.ALL | wx.ALIGN_LEFT)
        h2.AddSpacer(30)
        h2.Add(self.textbox2, 0, wx.ALL | wx.ALIGN_LEFT)

        self.button1 = wx.Button(self,-1,'登录',size=(300,60))  # 登录按钮

        # 将嵌套子布局器添加到总体布局器中
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
        # 获得用户名与密码输入
        username = self.textbox1.GetValue()
        pasw = self.textbox2.GetValue()

        # 查询是否存在该用户
        df = get_login_info(username)
        # sql_text = f"SELECT * from users_info where user='{username}'"
        # self.parent.cursor.execute(sql_text)
        # result = self.parent.cursor.fetchall()
        if len(df)<=0:
            wx.MessageBox('系统内没有该用户，请输入正确的用户名。','提示')
            return
        else:
            correct_paswd = df['passwd'][0]
        if pasw == correct_paswd:
            # 若登录成功，显示初始提示界面
            self.Box.Clear(True)
            text4 = get_textctrl_bold(self, '用户:  '+username+'  您好！', 20)
            # t = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
            # self.text5 = get_textctrl_bold(self, t, 16)
            text6 = get_textctrl_bold(self, '请选择左侧房间与左上角功能选项以开始使用', 20)
            self.Box.Add(text4, 0, wx.ALL | wx.ALIGN_CENTER)
            self.Box.AddSpacer(20)
            # self.new_box.Add(self.text5, 0, wx.ALL | wx.ALIGN_CENTER)
            # self.new_box.AddSpacer(20)
            self.Box.Add(text6, 0, wx.ALL | wx.ALIGN_CENTER)
            self.SetSizer(self.Box)
            self.login_flag = True
            self.parent.LevelChange(df['level'][0])
        else:
            wx.MessageBox('密码错误，请重试。',caption='错误')