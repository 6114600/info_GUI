import wx
from utils import get_textctrl_bold
from utils.getData import get_data

class SingleRoomPanel(wx.Panel):
    def __init__(self, parent, frame, room_num):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        # TODO: 获得数据
        data_ = get_data(room_num)

        self.room = room_num

        self.Room_num = get_textctrl_bold(self,str(room_num),20)

        Box = wx.BoxSizer(wx.VERTICAL)
        s1 = wx.BoxSizer(wx.HORIZONTAL)
        self.combobox = wx.ComboBox(self,-1,value='图标模式',choices=['图标模式','列表模式'])


        electri_icon = wx.StaticBitmap(self,wx.ID_ANY,wx.Bitmap(100,100))
        electri_icon.SetBitmap(wx.Bitmap(wx.Image('images/lightening.png',wx.BITMAP_TYPE_PNG)))
        electri_text = get_textctrl_bold(self,'电 表',16)
        s1.Add(electri_icon,0,  wx.ALL|wx.EXPAND, 20)
        s1.AddSpacer(20)
        s1.Add(electri_text,0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 20)
        s1.AddSpacer(20)
        self.electri_num = get_textctrl_bold(self,str(data_['电表读数'][len(data_['账户余额'])-1])+'  kwh',16)
        s1.Add(self.electri_num,0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 20)

        s2 = wx.BoxSizer(wx.HORIZONTAL)
        hotwater_icon = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(100, 100))
        hotwater_icon.SetBitmap(wx.Bitmap(wx.Image('images/hot_water.png', wx.BITMAP_TYPE_PNG)))
        hotwater_text = get_textctrl_bold(self,'热水表',16)
        s2.Add(hotwater_icon, 0, wx.ALL | wx.EXPAND, 20)
        s2.AddSpacer(20)
        s2.Add(hotwater_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)
        s2.AddSpacer(20)
        self.hotwater_num = get_textctrl_bold(self, str(data_['热水表读数'][len(data_['账户余额'])-1]) + '  t', 16)
        s2.Add(self.hotwater_num, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)

        s3 = wx.BoxSizer(wx.HORIZONTAL)
        coldwater_icon = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(100, 100))
        coldwater_icon.SetBitmap(wx.Bitmap(wx.Image('images/cold_water.png', wx.BITMAP_TYPE_PNG)))
        coldwater_text = get_textctrl_bold(self,'冷水表',16)
        s3.Add(coldwater_icon, 0, wx.ALL | wx.EXPAND, 20)
        s3.AddSpacer(20)
        s3.Add(coldwater_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)
        s3.AddSpacer(20)
        self.coldwater_num = get_textctrl_bold(self, str(data_['冷水表读数'][len(data_['账户余额'])-1]) + '  t', 16)
        s3.Add(self.coldwater_num, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)

        s4 = wx.BoxSizer(wx.HORIZONTAL)
        coldwater_icon = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(100, 100))
        coldwater_icon.SetBitmap(wx.Bitmap(wx.Image('images/bill.png', wx.BITMAP_TYPE_PNG)))
        coldwater_text = get_textctrl_bold(self, '账户余额', 16)
        s4.Add(coldwater_icon, 0, wx.ALL | wx.EXPAND, 20)
        s4.AddSpacer(20)
        s4.Add(coldwater_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)
        s4.AddSpacer(20)
        self.bill_num = get_textctrl_bold(self, str(data_['账户余额'][len(data_['账户余额'])-1]) + '  元', 16)
        s4.Add(self.bill_num, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)

        Box.Add(self.combobox,0,wx.ALL|wx.ALIGN_LEFT)
        Box.Add(self.Room_num,0,wx.ALL|wx.ALIGN_CENTER)

        Box.Add(s1,0,wx.ALL|wx.ALIGN_CENTER)
        Box.AddSpacer(20)
        Box.Add(s2,0,wx.ALL|wx.ALIGN_CENTER)
        Box.AddSpacer(20)
        Box.Add(s3,0,wx.ALL|wx.ALIGN_CENTER)
        Box.AddSpacer(20)
        Box.Add(s4, 0, wx.ALL | wx.ALIGN_CENTER)
        Box.AddSpacer(20)
        wx.Panel.SetSizer(self,Box)

    def room_change(self,num):
        self.room = num
        data_ = get_data(self.room)
        # data_.index = list(range(len(data_)))
        self.Room_num.SetLabel(str(num))
        self.electri_num.SetLabel(str(data_['电表读数'][len(data_['账户余额'])-1])+'  kwh')
        self.hotwater_num.SetLabel(str(data_['热水表读数'][len(data_['账户余额'])-1])+'  t')
        self.coldwater_num.SetLabel(str(data_['冷水表读数'][len(data_['账户余额'])-1]) + '  t')
        self.bill_num.SetLabel(str(data_['账户余额'][len(data_['账户余额'])-1]) + '  元')