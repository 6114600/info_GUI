import os
import time
import wx
import wx.grid
from utils import get_textctrl_bold, excel_output
from utils.getData import get_data
from utils.PandasToGrid import PandasToGrid
import wx.adv

# 此面板还需实现的功能
# 多表导出（加弹窗设置：选房间、选表的种类、是否合并）

class DatePicker( wx.adv.DatePickerCtrl):  #日期选择类
    def __init__(self,parent,dt,style=wx.adv.DP_DEFAULT):
        super(DatePicker,self).__init__(parent,dt=dt,style=style)
        self.SetInitialSize((120,-1))

class HistoryPanel(wx.Panel):
    def __init__(self, parent, frame, room_num):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        self.room = room_num
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        self.text_room = get_textctrl_bold(self, '0201', 24)
        self.img_room = wx.StaticBitmap(self,-1,wx.Bitmap(20,20))
        self.img_room.SetBitmap(wx.Bitmap(wx.Image('images/room.png',type=wx.BITMAP_TYPE_PNG)))
        hbox0.Add(self.img_room,wx.ALIGN_CENTRE)
        hbox0.AddSpacer(30)
        hbox0.Add(self.text_room,wx.ALIGN_CENTRE)

        grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(500, 600),
                            wx.NO_BORDER | wx.WANTS_CHARS)
        grid.CreateGrid(50, 20)
        self.grid_history = grid
        self.data_refresh()
        self.grid_history.EnableEditing(False)
        self.grid_history.EnableDragGridSize(False)
        self.grid_history.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTRE)

        Box = wx.BoxSizer(wx.HORIZONTAL)
        Box.AddSpacer(30)
        box_l = wx.BoxSizer(wx.VERTICAL)

        box_l.Add(hbox0,wx.ALIGN_CENTER)

        text3 = get_textctrl_bold(self,'数据种类',12)
        self.combobox0 = wx.ComboBox(self,-1,value='热水表',choices=['热水表','冷水表','电表'],style=wx.CB_READONLY)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(text3,wx.ALL|wx.ALIGN_CENTRE)
        hbox.AddSpacer(20)
        hbox.Add(self.combobox0,wx.ALL|wx.ALIGN_CENTRE)
        box_l.AddSpacer(20)
        box_l.Add(hbox,wx.ALIGN_CENTRE)

        now = wx.DateTime.Now()
        self.__dp1 = DatePicker(self, now, wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.__dp2 = DatePicker(self, now, wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.combobox1 = wx.ComboBox(self,-1,value='0时',choices=[f'{i}时' for i in range(0,24)])
        self.combobox2 = wx.ComboBox(self,-1,value='0时',choices=[f'{i}时' for i in range(0,24)])
        text1 = get_textctrl_bold(self, '起始日期', 12)
        text2 = get_textctrl_bold(self, '终止日期', 12)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(text1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hbox1.AddSpacer(20)
        hbox1.Add(self.__dp1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hbox1.AddSpacer(10)
        hbox1.Add(self.combobox1,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(text2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hbox2.AddSpacer(20)
        hbox2.Add(self.__dp2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hbox2.AddSpacer(10)
        hbox2.Add(self.combobox2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        box_l.Add(hbox1,wx.ALIGN_CENTRE)
        box_l.Add(hbox2,wx.ALIGN_CENTRE)

        self.button1 = wx.Button(self,wx.ID_ANY,'查询',size=(150,40))
        self.button2 = wx.Button(self,wx.ID_ANY,'导出',size=(150,40))
        self.button3 = wx.Button(self, wx.ID_ANY, '多表导出',size=(150,40))

        box_l.AddSpacer(30)
        box_l.Add(self.button1,0, wx.ALIGN_CENTER)
        box_l.AddSpacer(15)
        box_l.Add(self.button2, 0,  wx.ALIGN_CENTER)
        box_l.AddSpacer(15)
        box_l.Add(self.button3, 0,  wx.ALIGN_CENTER)

        Box.Add(box_l,0,wx.ALIGN_CENTER)
        Box.AddSpacer(75)
        Box.Add(self.grid_history,0,wx.ALIGN_CENTER)
        wx.Panel.SetSizer(self,Box)

        self.Bind(wx.EVT_BUTTON,self.OnSearchClick,self.button1)
        self.Bind(wx.EVT_BUTTON, self.OnOutputClick, self.button2)
        self.Bind(wx.adv.EVT_DATE_CHANGED,self.OnStartDateChange,self.__dp1)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnEndDateChange, self.__dp2)

    def OnStartDateChange(self,event):
        date = event.GetDate()
        self.start_date = date.Format().split(' ')[0]
        self.start_date = self.start_date.split('/')
        self.start_date = '%d-%02d-%02d %02d:00:00'%(int(self.start_date[0]),int(self.start_date[1]),
                                                int(self.start_date[2]),int(self.combobox1.GetValue()[:-1]))
        # print(self.start_date,type(self.start_date))

    def OnEndDateChange(self,event):
        date = event.GetDate()
        self.end_date = date.Format().split(' ')[0]
        self.end_date = self.end_date.split('/')
        self.end_date = '%d-%02d-%02d %02d:00:00' % (int(self.end_date[0]), int(self.end_date[1]),
                                            int(self.end_date[2]),int(self.combobox2.GetValue()[:-1]))

    def OnSearchClick(self,event):
        #TODO: 日期比较
        assert self.end_date > self.start_date, "起始日期必须早于终止日期"
        table_type = self.combobox0.GetValue()
        if table_type == '热水表':
            table_type = 'water_h'
        elif table_type == '冷水表':
            table_type = 'water_c'
        elif table_type == '冷电表':
            table_type = 'electri'
        self.data_refresh([self.start_date,self.end_date,table_type])

    def OnOutputClick(self,event):
        self.data_refresh()
        excel_output(self,self.data_)

    def OnMultiOutputClick(self,event):
        #TODO: 多表导出
        pass

    def data_refresh(self,constrains=None):
        self.data_ = get_data(self.room,constrains)
        self.text_room.SetLabel(self.room)
        PandasToGrid(self.grid_history, self.data_)
        self.grid_history.AutoSizeColumns(True)

    def room_change(self,num):
        self.room = num
        self.data_refresh()

