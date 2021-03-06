import wx
from utils import get_textctrl_bold
from utils.getData import get_data
from utils.PandasToGrid import PandasToGrid
import wx.adv


class DatePicker( wx.adv.DatePickerCtrl):  #日期选择类
    def __init__(self,parent,dt,style=wx.adv.DP_DEFAULT):
        super(DatePicker,self).__init__(parent,dt=dt,style=style)
        self.SetInitialSize((120,-1))

class HistoryPanel(wx.Panel):
    def __init__(self, parent, frame, room_num):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        self.room = room_num
        grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(500, 600),
                            wx.NO_BORDER | wx.WANTS_CHARS)
        grid.CreateGrid(50, 20)
        self.grid_history = grid
        self.data_refresh()

        Box = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        now = wx.DateTime.Now()
        self.__dp1 = DatePicker(self, now, wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.__dp2 = DatePicker(self, now, wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)

        text1 = get_textctrl_bold(self,'起始日期',12)
        text2 = get_textctrl_bold(self, '终止日期', 12)
        self.button1 = wx.Button(self,wx.ID_ANY,'查询')


        self.sizer.Add(text1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(self.__dp1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.sizer.AddSpacer(50)
        self.sizer.Add(text2,0,wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(self.__dp2,0,wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.sizer.AddSpacer(50)
        self.sizer.Add(self.button1,0,wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        Box.Add(self.sizer,0,wx.ALIGN_CENTER)
        Box.Add(self.grid_history,0,wx.ALIGN_CENTER)
        wx.Panel.SetSizer(self,Box)

        self.Bind(wx.EVT_BUTTON,self.OnSearchClick,self.button1)
        self.Bind(wx.adv.EVT_DATE_CHANGED,self.OnStartDateChange,self.__dp1)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnEndDateChange, self.__dp2)

    def OnStartDateChange(self,event):
        date = event.GetDate()
        self.start_date = date.Format()

    def OnEndDateChange(self,event):
        date = event.GetDate()
        self.end_date = date.Format()


    def OnSearchClick(self,event):
        assert self.end_date > self.start_date, "起始日期必须早于终止日期"
        self.data_['日期'] = self.data_.apply()

    def data_refresh(self):
        # TODO: 获得数据
        self.data_ = get_data(self.room)

        # TODO：计算费用
        price = [0.6, 0.2, 0.1]
        for name, name_ in zip(['电表读数', '热水表读数', '冷水表读数'], ['电用量', '热水用量', '冷水用量']):
            e_consumer = [0]
            for i in range(len(self.data_[name]) - 1):
                e_consumer.append(self.data_[name][i + 1] - self.data_[name][i])
            self.data_[name_] = e_consumer
        temp = []
        for i in range(len(self.data_['电表读数'])):
            temp.append(round(
                self.data_['电用量'][i] * price[0] + self.data_['热水用量'][i] * price[1] + self.data_['电用量'][i] * price[2],2))
        self.data_['消费'] = temp
        PandasToGrid(self.grid_history, self.data_)
        self.grid_history.EnableEditing(False)
        self.grid_history.EnableDragGridSize(False)

    def room_change(self,num):
        self.room = num
        self.data_refresh()