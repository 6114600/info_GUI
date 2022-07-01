import wx
from utils import get_textctrl_bold
from utils.getData import get_data,get_status
import wx.lib.scrolledpanel as scrolled

class SingleRoomPanel(wx.Panel):
    def __init__(self, parent, frame, room_num):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize,)

        # TODO: 获得数据
        self.parent = parent
        self.SetBackgroundColour(wx.Colour('WHITE'))
        self.data_ = get_data(room_num)
        self.status = get_status(room_num)
        self.room = room_num

        # 单间模式
        self.Room_num = get_textctrl_bold(self,str(room_num),20)

        Box = wx.BoxSizer(wx.VERTICAL)
        s1 = wx.BoxSizer(wx.HORIZONTAL)

        self.electri_icon = wx.StaticBitmap(self,wx.ID_ANY,wx.Bitmap(100,100))
        self.electri_icon.SetBitmap(wx.Bitmap(wx.Image('images/pure_white.png',wx.BITMAP_TYPE_PNG)))
        electri_text = get_textctrl_bold(self,'电 表',16)

        s1.Add(self.electri_icon,0,  wx.ALL|wx.EXPAND, 20)
        s1.AddSpacer(20)
        s1.Add(electri_text,0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 20)
        s1.AddSpacer(20)

        self.electri_num = get_textctrl_bold(self,'',16)
        s1.Add(self.electri_num,0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 20)

        s2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hotwater_icon = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(100, 100))
        self.hotwater_icon.SetBitmap(wx.Bitmap(wx.Image('images/pure_white.png', wx.BITMAP_TYPE_PNG)))
        hotwater_text = get_textctrl_bold(self,'热水表',16)
        s2.Add(self.hotwater_icon, 0, wx.ALL | wx.EXPAND, 20)
        s2.AddSpacer(20)
        s2.Add(hotwater_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)
        s2.AddSpacer(20)
        self.hotwater_num = get_textctrl_bold(self,'', 16)
        s2.Add(self.hotwater_num, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)

        s3 = wx.BoxSizer(wx.HORIZONTAL)
        self.coldwater_icon = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(100, 100))
        self.coldwater_icon.SetBitmap(wx.Bitmap(wx.Image('images/pure_white.png', wx.BITMAP_TYPE_PNG)))
        coldwater_text = get_textctrl_bold(self,'冷水表',16)
        s3.Add(self.coldwater_icon, 0, wx.ALL | wx.EXPAND, 20)
        s3.AddSpacer(20)
        s3.Add(coldwater_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)
        s3.AddSpacer(20)
        self.coldwater_num = get_textctrl_bold(self, '', 16)
        s3.Add(self.coldwater_num, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)

        s4 = wx.BoxSizer(wx.HORIZONTAL)
        self.bill_icon = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(100, 100))
        self.bill_icon.SetBitmap(wx.Bitmap(wx.Image('images/bill.png', wx.BITMAP_TYPE_PNG)))
        coldwater_text = get_textctrl_bold(self, '账户余额', 16)
        s4.Add(self.bill_icon, 0, wx.ALL | wx.EXPAND, 20)
        s4.AddSpacer(20)
        s4.Add(coldwater_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)
        s4.AddSpacer(20)
        self.bill_num = get_textctrl_bold(self, str(self.data_['账户余额'][len(self.data_['账户余额'])-1]) + '  元', 16)
        s4.Add(self.bill_num, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)

        # Box.Add(self.combobox,0,wx.ALL|wx.ALIGN_LEFT)
        Box.Add(self.Room_num,0,wx.ALL|wx.ALIGN_CENTER)

        Box.Add(s1,0,wx.ALL|wx.ALIGN_CENTER)
        Box.AddSpacer(20)
        Box.Add(s2,0,wx.ALL|wx.ALIGN_CENTER)
        Box.AddSpacer(20)
        Box.Add(s3,0,wx.ALL|wx.ALIGN_CENTER)
        Box.AddSpacer(20)
        Box.Add(s4, 0, wx.ALL | wx.ALIGN_CENTER)
        Box.AddSpacer(20)
        self.Box = Box
        wx.Panel.SetSizer(self,self.Box)
        self.update(None)



    def room_change(self,num):
        self.room = num
        self.update(None)

    def update(self,event):
        self.data_ = get_data(self.room)
        self.status = get_status(self.room)
        self.Room_num.SetLabel(self.room)
        self.electri_num.SetLabel(str(self.data_['电表读数'][len(self.data_['账户余额']) - 1]) + '  kwh'
                                  if self.status['电表状态'][0] else '通讯中断')
        self.hotwater_num.SetLabel(str(self.data_['热水表读数'][len(self.data_['账户余额']) - 1]) + '  t'
                                   if self.status['热水表状态'][0] else '通讯中断')
        self.coldwater_num.SetLabel(str(self.data_['冷水表读数'][len(self.data_['账户余额']) - 1]) + '  t'
                                    if self.status['冷水表状态'][0] else '通讯中断')
        self.electri_icon.SetBitmap(wx.Bitmap(wx.Image('images/lightening.png'
                                                       if self.status['电表状态'][0] else 'images/lightening_gray.png',
                                                       wx.BITMAP_TYPE_PNG)))
        self.hotwater_icon.SetBitmap(wx.Bitmap(wx.Image('images/hot_water.png'
                                                       if self.status['热水表状态'][0] else 'images/hot_water_gray.png',
                                                       wx.BITMAP_TYPE_PNG)))
        self.coldwater_icon.SetBitmap(wx.Bitmap(wx.Image('images/cold_water.png'
                                                       if self.status['冷水表状态'][0] else 'images/cold_water_gray.png',
                                                       wx.BITMAP_TYPE_PNG)))
        self.bill_num.SetLabel(str(self.data_['账户余额'][len(self.data_['账户余额']) - 1]) + '  元')