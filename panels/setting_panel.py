import wx
from utils import get_textctrl_bold, get_textctrl_light
from utils.getData import get_data
from utils.PandasToGrid import PandasToGrid
from utils import load_config_file,edit_config_file
from utils import MyNumberValidator
from utils.getData import get_address,edit_database
import wx.adv


class DatePicker(wx.adv.DatePickerCtrl):  # 日期选择类
    def __init__(self, parent, dt, style=wx.adv.DP_DEFAULT):
        super(DatePicker, self).__init__(parent, dt=dt, style=style)
        self.SetInitialSize((120, -1))


class SettingPanel(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent,wx.ID_ANY,wx.DefaultPosition,
                          (700,525))
        self.parent = parent

        self.room_show = get_textctrl_bold(self,'0201',14)
        self.room_now = '0201'
        room_text = get_textctrl_bold(self,'当前房间',14)
        h0 = wx.BoxSizer(wx.HORIZONTAL)
        h0.Add(room_text, 0, wx.ALIGN_CENTRE)
        h0.AddSpacer(5)
        h0.Add(self.room_show,0,wx.ALIGN_CENTRE)


        hbox = wx.BoxSizer(wx.VERTICAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        h3 = wx.BoxSizer(wx.HORIZONTAL)
        h4 = wx.BoxSizer(wx.HORIZONTAL)
        h5 = wx.BoxSizer(wx.HORIZONTAL)
        h6 = wx.BoxSizer(wx.HORIZONTAL)
        self.now_value_list = []
        self.input_box_list = []
        hbox_list = [h1,h2,h3,h4,h5,h6]
        for i in range(6):
            hbox_list[i].Add(get_textctrl_bold(self,'当前值',10),0,wx.ALIGN_CENTRE_VERTICAL)
            hbox_list[i].AddSpacer(5)
            temp_value = get_textctrl_light(self,'                ',10)
            self.now_value_list.append(temp_value)
            hbox_list[i].Add(temp_value,0,wx.ALIGN_CENTRE_VERTICAL)
            hbox_list[i].AddSpacer(10)
            hbox_list[i].Add(get_textctrl_bold(self, '修改值', 10),0,wx.ALIGN_CENTRE_VERTICAL)
            hbox_list[i].AddSpacer(5)
            temp_box = wx.TextCtrl(self, -1, size=(180, 30))
            self.input_box_list.append(temp_box)
            hbox_list[i].Add(temp_box,0,wx.ALIGN_CENTRE_VERTICAL)
            

        text1 = get_textctrl_bold(self,'热水表控制器ip',12)
        text2 = get_textctrl_bold(self,'热水表地址',12)
        text3 = get_textctrl_bold(self, '冷水表控制器ip', 12)
        text4 = get_textctrl_bold(self, '冷水表地址', 12)
        text5 = get_textctrl_bold(self, '电表控制器ip', 12)
        text6 = get_textctrl_bold(self, '电水表地址', 12)

        vbox1.Add(text1,0,wx.ALL | wx.ALIGN_CENTER)
        vbox1.AddSpacer(10)
        vbox1.Add(h1,0,wx.ALIGN_CENTRE)
        vbox1.AddSpacer(10)
        vbox1.Add(text2,0,wx.ALIGN_CENTRE)
        vbox1.AddSpacer(10)
        vbox1.Add(h2,0,wx.ALIGN_CENTRE)
        vbox1.AddSpacer(25)
        vbox2.Add(text3,0,wx.ALIGN_CENTRE)
        vbox2.AddSpacer(10)
        vbox2.Add(h3,0,wx.ALIGN_CENTRE)
        vbox2.AddSpacer(10)
        vbox2.Add(text4,0,wx.ALIGN_CENTRE)
        vbox2.AddSpacer(10)
        vbox2.Add(h4,0,wx.ALIGN_CENTRE)
        vbox2.AddSpacer(25)
        vbox3.Add(text5,0,wx.ALIGN_CENTRE)
        vbox3.AddSpacer(10)
        vbox3.Add(h5,0,wx.ALIGN_CENTRE)
        vbox3.AddSpacer(10)
        vbox3.Add(text6,0,wx.ALIGN_CENTRE)
        vbox3.AddSpacer(10)
        vbox3.Add(h6,0,wx.ALIGN_CENTRE)
        vbox3.AddSpacer(25)

        hbox.AddSpacer(10)
        hbox.Add(h0, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        hbox.AddSpacer(10)
        hbox.Add(vbox1,0,wx.ALIGN_CENTRE_HORIZONTAL)
        hbox.AddSpacer(10)
        hbox.Add(vbox2,0,wx.ALIGN_CENTRE_HORIZONTAL)
        hbox.AddSpacer(10)
        hbox.Add(vbox3,0,wx.ALIGN_CENTRE_HORIZONTAL)
        hbox.AddSpacer(10)

        h7 = wx.BoxSizer(wx.HORIZONTAL)
        self.button1 = wx.Button(self,-1,label='确认设置',size=(100,40))
        self.button2 = wx.Button(self,-1,label='返  回',size=(100,40))
        self.button3 = wx.Button(self, -1, label='批量设置', size=(100, 40))
        h7.Add(self.button1,0,wx.ALIGN_CENTRE)
        h7.AddSpacer(50)
        h7.Add(self.button2,0,wx.ALIGN_CENTRE)
        h7.AddSpacer(50)
        h7.Add(self.button3, 0, wx.ALIGN_CENTRE)

        hbox.Add(h7,0,wx.ALIGN_CENTRE_HORIZONTAL)

        self.SetSizer(hbox)
        # self.room_change(self.room_now)
        self.Bind(wx.EVT_BUTTON,self.OnConfirm,self.button1)
        self.Bind(wx.EVT_BUTTON, self.OnBack, self.button2)

    def data_refresh(self):
        self.address = get_address(self.room_now)
        # print(self.address)

    def room_change(self,num):
        self.room_now = num
        self.update()

    def update(self):
        self.data_refresh()
        if self.address.empty:
            for i in self.now_value_list:
                i.SetLabel('未设置')
        self.room_show.SetLabel(str(self.room_now))
        item_names = ['water_h_ip','water_h_address','water_c_ip','water_c_address','electri_ip','electri_address']
        for i,text in enumerate(self.now_value_list):
            if self.address.isnull()[item_names[i]][0]:
                text.SetLabel('未设置')
            else:
                text.SetLabel(self.address[item_names[i]][0])

    def OnBack(self,event):
        self.parent._mgr.GetPane('Setting Panel').Hide()
        self.parent._mgr.GetPane('Cb Panel').Show()

    def OnConfirm(self,event):
        sql_text = f"UPDATE address_config set water_h_ip={self.input_box_list[0].GetValue()}, water_h_address={self.input_box_list[1].GetValue()}," \
                   f"water_c_ip={self.input_box_list[2].GetValue()}, water_c_address={self.input_box_list[3].GetValue()}," \
                   f"electri_ip={self.input_box_list[4].GetValue()}, electri_address={self.input_box_list[5].GetValue()} " \
                   f"where room_num={self.room_now}"
        edit_database(sql_text)