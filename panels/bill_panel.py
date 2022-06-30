import wx
from utils import get_textctrl_bold
from utils.getData import get_data
from utils.PandasToGrid import PandasToGrid
import wx.adv


class DatePicker( wx.adv.DatePickerCtrl):  #日期选择类
    def __init__(self,parent,dt,style=wx.adv.DP_DEFAULT):
        super(DatePicker,self).__init__(parent,dt=dt,style=style)
        self.SetInitialSize((120,-1))

class BillPanel(wx.Panel):
    def __init__(self, parent, frame, room_num):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        # TODO: 获得数据
        self.data_ = get_data(room_num)
        # print(self.data_)
        self.room = room_num

        # TODO：计算费用
        for name, name_ in zip(['电表读数','热水表读数','冷水表读数'],['电用量','热水用量','冷水用量']):
            e_consumer = [0]
            for i in range(len(self.data_[name])-1):
                e_consumer.append(self.data_[name][i+1]-self.data_[name][i])
            self.data_[name_] = e_consumer

        grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(500, 300),
                            wx.NO_BORDER | wx.WANTS_CHARS)

        grid.CreateGrid(150, 150)
        self.grid = grid
        PandasToGrid(self.grid, self.data_)
        self.grid.EnableEditing(False)
        self.grid.EnableDragGridSize(False)
        self.Box = wx.BoxSizer(wx.VERTICAL)
        self.Box.Add(self.grid,0,wx.ALL|wx.ALIGN_CENTER)
        self.SetSizer(self.Box)
