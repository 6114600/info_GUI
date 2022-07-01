import wx
from utils import get_textctrl_bold
from utils.getData import get_data
from utils.PandasToGrid import PandasToGrid
from utils import load_config_file,edit_config_file
from utils import MyNumberValidator
import wx.adv


class DatePicker(wx.adv.DatePickerCtrl):  # 日期选择类
    def __init__(self, parent, dt, style=wx.adv.DP_DEFAULT):
        super(DatePicker, self).__init__(parent, dt=dt, style=style)
        self.SetInitialSize((120, -1))


class SettingPanel(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        self.config = load_config_file()
        self.parent = parent

        vbox = wx.BoxSizer(wx.VERTICAL)
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        h3 = wx.BoxSizer(wx.HORIZONTAL)
        fontButton = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)

        self.text1 = get_textctrl_bold(self, '定时抄表：', 20)
        self.combobox1 = wx.ComboBox(self,-1, value='开' if bool(self.config['dscb']) else '关',choices=['开','关'],style=wx.CB_READONLY)


        self.text2 = get_textctrl_bold(self, '定时抄表周期：', 20)
        self.combobox2 = wx.ComboBox(self, -1, value='每年',choices=['每年','每月','每日','每隔'],style=wx.CB_READONLY)
        self.combobox3 = wx.ComboBox(self, -1, value='1月', choices=[f'{i + 1}月' for i in range(12)],style=wx.CB_READONLY)
        self.combobox4 = wx.ComboBox(self, -1, value='1日', choices=[f'{i + 1}日' for i in range(31)],style=wx.CB_READONLY)
        self.textctrl = wx.TextCtrl(self,-1,'',size=(30,-1),validator=MyNumberValidator(),style=wx.TE_CENTER)

        self.button1 = wx.Button(self, -1, '确认设置', size=(150, 50))
        self.button1.SetFont(fontButton)

        h1.AddSpacer(40)
        h1.Add(self.text1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        h1.AddSpacer(20)
        h1.Add(self.combobox1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        h2.AddSpacer(40)
        h2.Add(self.text2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        h2.AddSpacer(20)
        h2.Add(self.combobox2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        h2.AddSpacer(20)
        h2.Add(self.combobox3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        h2.Add(self.textctrl,0,wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        h2.Add(self.combobox4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.h2 = h2

        h3.AddSpacer(20)
        h3.Add(self.button1,0,wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        vbox.AddSpacer(40)
        vbox.Add(h1, 0, wx.ALL | wx.ALIGN_LEFT)
        vbox.AddSpacer(40)
        vbox.Add(h2, 0, wx.ALL | wx.ALIGN_LEFT)
        vbox.AddSpacer(40)
        vbox.Add(h3, 0, wx.ALL | wx.ALIGN_CENTER)
        # vbox.Add(self.button1,wx.ALIGN_CENTER)
        self.SetSizer(vbox)
        # self.textctrl.Hide()
        self.Bind(wx.EVT_COMBOBOX,self.OnTypeChange,self.combobox2)
        self.Bind(wx.EVT_COMBOBOX,self.OnMonthChange,self.combobox3)
        self.Bind(wx.EVT_BUTTON,self.OnConfirmChange,self.button1)

    def OnTypeChange(self,event):
        item_index = event.GetSelection()
        self.combobox3.Show()
        self.textctrl.Hide()
        if item_index == 0:
            self.combobox3.SetValue('1月')
            self.combobox3.SetItems([f'{i+1}月' for i in range(12)])
            self.combobox4.SetValue('1日')
            self.combobox4.SetItems([f'{i + 1}日' for i in range(31)])
        elif item_index == 1:
            self.combobox4.SetValue('1时')
            self.combobox4.SetItems([f'{i }时' for i in range(24)])
            self.combobox3.SetValue('1日')
            self.combobox3.SetItems([f'{i + 1}日' for i in range(31)])
        elif item_index == 2:
            self.combobox3.SetValue('1时')
            self.combobox3.SetItems([f'{i}时' for i in range(24)])
            self.combobox4.SetValue('0分')
            self.combobox4.SetItems([f'{i}分' for i in range(60)])
        elif item_index == 3:
            self.combobox3.Hide()
            self.textctrl.Show()
            self.combobox4.SetValue('分')
            self.combobox4.SetItems(['分','小时','天'])

    def OnMonthChange(self,event):
        if self.combobox2.GetValue() == '每年':
            month = self.combobox3.GetValue()[0]
            if month == '2':
                self.combobox4.SetValue('1日')
                self.combobox4.SetItems([f'{i + 1}日' for i in range(28)])
            elif month in ['1','3','5','7','8','10','12']:
                self.combobox4.SetValue('1日')
                self.combobox4.SetItems([f'{i + 1}日' for i in range(31)])
            else:
                self.combobox4.SetValue('1日')
                self.combobox4.SetItems([f'{i + 1}日' for i in range(30)])

    def OnConfirmChange(self,event):
        # 获取所有的值
        if_open = True if self.combobox1.GetValue() == '开' else False
        period_param = [self.combobox2.GetValue(),self.combobox3.GetValue()[:-1],self.combobox4.GetValue()[:-1],self.textctrl.GetValue()]

        if period_param[0] != '每隔':
            period_code = 'Every_'
            if period_param[0] == '每年':
                period_code += 'Year_'+period_param[1]+'_'+period_param[2]
            elif period_param[1] == '每月':
                period_code += 'Month_'+period_param[1]+'_'+period_param[2]
            elif period_param[2] == '每日':
                period_code += 'Day_'+period_param[1]+'_'+period_param[2]
        else:
            period_code = period_param[3] +'_' + str(self.combobox4.GetSelection())

        config = load_config_file()
        config['dscb'] = str(if_open)
        config['cb_period'] = str(period_code)
        wx.MessageBox('是否修改配置文件？','提示',style=wx.YES_NO)
        if edit_config_file(config):
            wx.MessageBox('成功修改配置文件','提示',style=wx.OK)
            self.parent._mgr.GetPane('Setting Panel').Hide()
            self.parent._mgr.GetPane('Cb Panel').Show()
            self.parent._mgr.Update()
        else:
            wx.MessageBox('配置文件修改异常','错误',style=wx.OK)

