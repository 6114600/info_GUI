import wx
import numpy as np
from utils import get_textctrl_bold,room_num_format
from utils.getData import get_data,get_status
import wx.lib.scrolledpanel as scrolled

# 此面板还需实现的功能
# 替换数据来源

class SingleRoomPanel(wx.Panel):
    def __init__(self, parent, frame, room_num):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize,)

        self.parent = parent
        self.SetBackgroundColour(wx.Colour('WHITE'))

        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.AddSpacer(40)
        text1 = get_textctrl_bold(self,'水电表组状态',24)
        vbox0.Add(text1,0,wx.ALIGN_CENTRE)
        vbox0.AddSpacer(60)

        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        img0 = wx.StaticBitmap(self,-1,wx.Bitmap(20,20))
        img0.SetBitmap(wx.Bitmap(wx.Image('images/hwater.png',wx.BITMAP_TYPE_PNG)))
        hbox0.Add(img0,0,wx.ALIGN_LEFT)
        hbox0.AddSpacer(20)
        text2 = get_textctrl_bold(self,'热水表组',16)
        self.hwater_text = get_textctrl_bold(self,'正常运行',16)
        self.hwater_text.SetForegroundColour('green')
        hbox0.Add(text2, 0, wx.ALIGN_CENTRE)
        hbox0.AddSpacer(20)
        hbox0.Add(self.hwater_text,0,wx.ALIGN_CENTRE)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        img1 = wx.StaticBitmap(self,-1,wx.Bitmap(20,20))
        img1.SetBitmap(wx.Bitmap(wx.Image('images/cwater.png',wx.BITMAP_TYPE_PNG)))
        hbox1.Add(img1, 0, wx.ALIGN_LEFT)
        hbox1.AddSpacer(20)
        text3 = get_textctrl_bold(self, '冷水表组', 16)
        self.cwater_text = get_textctrl_bold(self, '正常运行', 16)
        self.cwater_text.SetForegroundColour('green')
        hbox1.Add(text3, 0, wx.ALIGN_CENTRE)
        hbox1.AddSpacer(20)
        hbox1.Add(self.cwater_text, 0, wx.ALIGN_CENTRE)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        text3 = get_textctrl_bold(self, '电表组', 16)
        img2 = wx.StaticBitmap(self, -1, wx.Bitmap(20, 20))
        img2.SetBitmap(wx.Bitmap(wx.Image('images/electri.png', wx.BITMAP_TYPE_PNG)))
        hbox2.Add(img2, 0, wx.ALIGN_LEFT)
        hbox2.AddSpacer(20)
        self.e_text = get_textctrl_bold(self, '正常运行', 16)
        self.e_text.SetForegroundColour('green')
        hbox2.Add(text3, 0, wx.ALIGN_CENTRE)
        hbox2.AddSpacer(20)
        hbox2.Add(self.e_text, 0, wx.ALIGN_CENTRE)

        vbox0.Add(hbox0,0,wx.ALIGN_CENTRE)
        vbox0.AddSpacer(20)
        vbox0.Add(hbox1, 0, wx.ALIGN_CENTRE)
        vbox0.AddSpacer(20)
        vbox0.Add(hbox2, 0, wx.ALIGN_CENTRE)
        vbox0.AddSpacer(20)

        self.button0 = wx.Button(self,-1,'查看异常表位置',size=(120,60))
        vbox0.Add(self.button0,0,wx.ALIGN_CENTRE)

        self.SetSizer(vbox0)

        self.timer = wx.Timer(self)
        self.timer.Start(15000)
        self.Bind(wx.EVT_TIMER,self.Ontimer,self.timer)
        self.Bind(wx.EVT_BUTTON,self.LookErrors,self.button0)

    def Ontimer(self,evt):
        self.update()

    def data_refresh(self):
        self.hw_errors = []
        self.cw_errors = []
        self.e_errors = []
        for floor in range(2,11):
            for room in range(1,38):
                room_num = room_num_format(floor,room)
                df = get_data(room_num,None)
                df = df.head(1)
                hwater_status = df.isnull()['water_h'][0]
                cwater_status = df.isnull()['water_c'][0]
                electri_status = df.isnull()['electri'][0]
                if hwater_status:
                    self.hw_errors.append([room_num,1])
                if cwater_status:
                    self.cw_errors.append([room_num,1])
                if electri_status:
                    self.e_errors.append([room_num,1])

    def update(self):
        self.data_refresh()
        if not self.parent.login:
            return
        if len(self.hw_errors)<= 0 and len(self.hw_errors)<= 0 and len(self.hw_errors)<= 0:
            self.iferror = False
            pass
        else:
            self.iferror = True
            if len(self.hw_errors) > 0:
                self.hwater_text.SetLabel(f'{len(self.hw_errors)} 只表异常')
                self.hwater_text.SetForegroundColour('Red')
            if len(self.cw_errors) > 0:
                self.cwater_text.SetLabel(f'{len(self.cw_errors)} 只表异常')
                self.cwater_text.SetForegroundColour('Red')
            if len(self.e_errors) > 0:
                self.e_text.SetLabel(f'{len(self.e_errors)} 只表异常')
                self.e_text.SetForegroundColour('Red')
            wx.MessageBox('表组异常！ 请至实时监控界面查看！','异常报警',style=wx.OK|wx.ICON_ERROR)
        self.button0.Enable(self.iferror)

    def LookErrors(self,evt):
        all_num = len(self.hw_errors) + len(self.cw_errors) + len(self.e_errors)
        errors1 = np.array(self.hw_errors)
        errors2 = np.array(self.cw_errors)
        errors3 = np.array(self.e_errors)

        wx.MessageBox(f'共有{all_num}只表异常。\n其中，\n'
                      f'热水表{len(self.hw_errors)}只，位于{"".join(str(i) + "," for i in errors1[:,0])[:-1]};\n'
                      f'冷水表{len(self.cw_errors)}只，位于{"".join(str(i) + "," for i in errors2[:,0])[:-1]};\n'
                      f'电表{len(self.e_errors)}只，位于{"".join(str(i) + "," for i in errors3[:,0])[:-1]};\n')