import random
import wx
from utils import get_textctrl_bold
from utils.getData import get_data,get_status
import wx.lib.scrolledpanel as scrolled

# 此面板还需实现的功能
# 添加数据库数据来源
# 异常的识别、图标的替换
# 异常的报警提示

class AllRoomsPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, frame,):
        scrolled.ScrolledPanel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize,)
        self.SetScrollbar(0,1,0,1200)
        self.SetupScrolling()
        self.parent = parent
        self.SetBackgroundColour(wx.Colour('WHITE'))


        self.all_image_list = []
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        self.Button = wx.Button(self,-1,'查找异常',size=(100,40))

        vbox0.Add(self.Button,wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        vbox0.AddSpacer(30)
        for floor in range(2,11):
            vbox0.Add(get_textctrl_bold(self,f'{floor} 楼',25))
            vbox0.AddSpacer(30)
            temp_grid = wx.GridSizer(7,6,40,40)
            temp_image_list = []
            for room in range(1,38):
                temp_s = wx.BoxSizer(wx.VERTICAL)
                temp_img = wx.StaticBitmap(self,-1,wx.Bitmap(f'images/{111 if  room % 2 else random.choice([101,100,110])}.png' ,wx.BITMAP_TYPE_PNG))
                temp_hbox = wx.BoxSizer(wx.HORIZONTAL)
                temp_text1 = get_textctrl_bold(self,'%02d%02d'%(floor,room),16)
                temp_text2 = get_textctrl_bold(self, '正常' if room % 2 else '异常', 16)
                temp_text2.SetForegroundColour('green' if room % 2 else 'red')
                temp_hbox.Add(temp_text1)
                temp_hbox.AddSpacer(10)
                temp_hbox.Add(temp_text2)
                temp_s.Add(temp_img,0,wx.ALIGN_CENTER)
                temp_s.AddSpacer(10)
                temp_s.Add(temp_hbox,wx.ALIGN_CENTER)
                temp_image_list.append(temp_img)
                temp_grid.Add(temp_s)
            vbox0.Add(temp_grid,0,wx.ALIGN_CENTER)
        self.SetSizer(vbox0)
        self.Bind(wx.EVT_BUTTON,self.OnLookError,self.Button)

    def OnLookError(self,event):
        all_num = 4
        hot_water_num = 2
        cold_water_num = 1
        electri_num = 1
        location1 = ['0202','0725']
        location2 = ['0805']
        location3 = ['0405']
        wx.MessageBox(f'共有{all_num}只表异常。\n其中，\n'
                      f'热水表{hot_water_num}只，位于{"".join(str(i)+"," for i in location1)[:-1]};\n'
                      f'冷水表{cold_water_num}只，位于{"".join(str(i)+"," for i in location2)[:-1]};\n'
                      f'电表{electri_num}只，位于{"".join(str(i)+"," for i in location3)[:-1]};\n')




