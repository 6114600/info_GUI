#!/usr/bin/env python
import threading

import wx
import wx.grid
import wx.html
import wx.aui as aui
import mysql.connector
from utils.getData import get_login_info

from utils import room_num_format
from panels.room_panel import SingleRoomPanel
from panels.history_panel import HistoryPanel
from panels.login_panel import LoginPanel
from panels.info_panel import InfoPanel
from panels.cb_panel import CbPanel
from panels.setting_panel import SettingPanel
from panels.all_rooms_panel import AllRoomsPanel
from database.LookUp import LookUp_Helper
import time
import json

from six import BytesIO

# 函数ID号
ID_Supervise = wx.NewId() #100
ID_History = wx.NewId()
ID_Bill = wx.NewId()
ID_Cb = wx.NewId()
ID_Login = wx.NewId()
ID_Mode = wx.NewId()

ID_CreateTree = wx.NewId()
ID_CreateGrid = wx.NewId()
ID_CreateText = wx.NewId()
ID_CreateHTML = wx.NewId()
ID_CreateSizeReport = wx.NewId()
ID_GridContent = wx.NewId()
ID_TextContent = wx.NewId()
ID_TreeContent = wx.NewId()
ID_HTMLContent = wx.NewId()
ID_SizeReportContent = wx.NewId()
ID_CreatePerspective = wx.NewId()
ID_CopyPerspective = wx.NewId()

ID_TransparentHint = wx.NewId()
ID_VenetianBlindsHint = wx.NewId()
ID_RectangleHint = wx.NewId()
ID_NoHint = wx.NewId()
ID_HintFade = wx.NewId()
ID_AllowFloating = wx.NewId()
ID_NoVenetianFade = wx.NewId()
ID_TransparentDrag = wx.NewId()
ID_AllowActivePane = wx.NewId()
ID_NoGradient = wx.NewId()
ID_VerticalGradient = wx.NewId()
ID_HorizontalGradient = wx.NewId()

ID_Settings = wx.NewId()
ID_About = wx.NewId()
ID_FirstPerspective = ID_CreatePerspective+1000

#----------------------------------------------------------------------
def GetMondrianData():
    return \
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82'


def GetMondrianBitmap():
    return wx.Bitmap(GetMondrianImage())


def GetMondrianImage():
    stream = BytesIO(GetMondrianData())
    return wx.Image(stream)


def GetMondrianIcon():
    icon = wx.Icon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon


class PyAUIFrame(wx.Frame):

    # 初始化函数
    def __init__(self, parent, id=-1, title="宿舍水电管理系统", pos=wx.DefaultPosition,  # 标题可在此处修改
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                                            wx.SUNKEN_BORDER |
                                            wx.CLIP_CHILDREN):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        # 窗口居中显示
        self.Centre()
        # tell FrameManager to manage this frame
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self._perspectives = []
        self.n = 0
        self.x = 0

        # 窗口图标在此修改，替换图片即可
        self.SetIcon(GetMondrianIcon())

        # 创建右侧树状选择面板
        self.main_tree = self.CreateTreeCtrl()

        # 查表类
        self._LH = LookUp_Helper()

        # 登录状态
        self.login = False
        self.l_login = True

        # 实时监控模式
        self.supervise_mode = False # 1 单间 0 全局

        # 树双击事件
        self.main_tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeChanged)

        # 用于面板切换
        self.centre_pane_list = ['Room Panel','History Panel','Login Panel','Cb Panel','Setting Panel']
        self.centre_pane_id = [ID_Supervise, ID_History, ID_Login, ID_Cb, ID_Settings]

        # 创建面板
        # 初始界面&登录界面
        self.login_panel = LoginPanel(self,self)
        # 单间当前信息显示
        self.room_panel = SingleRoomPanel(self,self,'0201')
        # 单间历史信息显示
        self.history_panel = HistoryPanel(self,self,'0201')
        # 提示界面
        self.info_panel = InfoPanel(self, self)
        # 抄表中心
        self.cb_panel = CbPanel(self,self)
        # 抄表设置面板
        self.setting_panel = SettingPanel(self,self)
        # # 总览面板
        # self.allroom_panel = AllRoomsPanel(self,self)

        # 创建菜单栏
        mb = wx.MenuBar()

        # 创建退出选项
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "Exit")
        #
        # view_menu = wx.Menu()
        # view_menu.Append(ID_CreateText, "Create Text Control")
        # view_menu.Append(ID_CreateHTML, "Create HTML Control")
        # view_menu.Append(ID_CreateTree, "Create Tree")
        # view_menu.Append(ID_CreateGrid, "Create Grid")
        # view_menu.Append(ID_CreateSizeReport, "Create Size Reporter")
        # view_menu.AppendSeparator()
        # view_menu.Append(ID_GridContent, "Use a Grid for the Content Pane")
        # view_menu.Append(ID_TextContent, "Use a Text Control for the Content Pane")
        # view_menu.Append(ID_HTMLContent, "Use an HTML Control for the Content Pane")
        # view_menu.Append(ID_TreeContent, "Use a Tree Control for the Content Pane")
        # view_menu.Append(ID_SizeReportContent, "Use a Size Reporter for the Content Pane")
        #
        # options_menu = wx.Menu()
        # options_menu.AppendRadioItem(ID_TransparentHint, "Transparent Hint")
        # options_menu.AppendRadioItem(ID_VenetianBlindsHint, "Venetian Blinds Hint")
        # options_menu.AppendRadioItem(ID_RectangleHint, "Rectangle Hint")
        # options_menu.AppendRadioItem(ID_NoHint, "No Hint")
        # options_menu.AppendSeparator();
        # options_menu.AppendCheckItem(ID_HintFade, "Hint Fade-in")
        # options_menu.AppendCheckItem(ID_AllowFloating, "Allow Floating")
        # options_menu.AppendCheckItem(ID_NoVenetianFade, "Disable Venetian Blinds Hint Fade-in")
        # options_menu.AppendCheckItem(ID_TransparentDrag, "Transparent Drag")
        # options_menu.AppendCheckItem(ID_AllowActivePane, "Allow Active Pane")
        # options_menu.AppendSeparator();
        # options_menu.AppendRadioItem(ID_NoGradient, "No Caption Gradient")
        # options_menu.AppendRadioItem(ID_VerticalGradient, "Vertical Caption Gradient")
        # options_menu.AppendRadioItem(ID_HorizontalGradient, "Horizontal Caption Gradient")
        # options_menu.AppendSeparator();
        # options_menu.Append(ID_Settings, "Settings Pane")
        #
        # self._perspectives_menu = wx.Menu()
        # self._perspectives_menu.Append(ID_CreatePerspective, "Create Perspective")
        # self._perspectives_menu.Append(ID_CopyPerspective, "Copy Perspective Data To Clipboard")
        # self._perspectives_menu.AppendSeparator()
        # self._perspectives_menu.Append(ID_FirstPerspective+0, "Default Startup")
        # self._perspectives_menu.Append(ID_FirstPerspective+1, "All Panes")
        # self._perspectives_menu.Append(ID_FirstPerspective+2, "Vertical Toolbar")
        #
        # help_menu = wx.Menu()
        # help_menu.Append(ID_About, "About...")
        #
        mb.Append(file_menu, "File")
        # mb.Append(view_menu, "View")
        # mb.Append(self._perspectives_menu, "Perspectives")
        # mb.Append(options_menu, "Options")
        # mb.Append(help_menu, "Help")
        #
        self.SetMenuBar(mb)

        self.statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)  # 控制下部状态栏分栏个数
        self.statusbar.SetStatusWidths([-8, -2])  # 控制下部状态栏比例
        # TODO: 加状态提示
        self.statusbar.SetStatusText("Ready", 0)
        self.statusbar.SetStatusText("Loading...", 1)

        # min size for the frame itself isn't completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size

        # 设置窗口为固定大小
        self.SetSize((1000, 750))
        self.SetMinSize(wx.Size(1000, 750))
        self.SetMaxSize(wx.Size(1000, 750))

        # create some toolbars
        # tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
        #                  wx.TB_FLAT | wx.TB_NODIVIDER)
        # self.combobox1 = (self,555,value='')
        # tb1.SetToolBitmapSize(wx.Size(48,48))
        # tb1.AddTool(101, "Test", wx.ArtProvider.GetBitmap(wx.ART_ERROR))
        # tb1.AddSeparator()
        # tb1.AddTool(102, "Test", wx.ArtProvider.GetBitmap(wx.ART_QUESTION))
        # tb1.AddTool(103, "Test", wx.ArtProvider.GetBitmap(wx.ART_INFORMATION))
        # tb1.AddTool(103, "Test", wx.ArtProvider.GetBitmap(wx.ART_WARNING))
        # tb1.AddTool(103, "Test", wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE))
        # tb1.Realize()
        #
        # tb2 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
        #                  wx.TB_FLAT | wx.TB_NODIVIDER)
        # tb2.SetToolBitmapSize(wx.Size(16,16))
        # tb2_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))
        # tb2.AddTool(101, "Test", tb2_bmp1)
        # tb2.AddTool(101, "Test", tb2_bmp1)
        # tb2.AddTool(101, "Test", tb2_bmp1)
        # tb2.AddTool(101, "Test", tb2_bmp1)
        # tb2.AddSeparator()
        # tb2.AddTool(101, "Test", tb2_bmp1)
        # tb2.AddTool(101, "Test", tb2_bmp1)
        # tb2.AddSeparator()
        # tb2.AddTool(101, "Test", tb2_bmp1)
        # tb2.AddTool(101, "Test", tb2_bmp1)
        # tb2.AddTool(101, "Test", tb2_bmp1)
        # tb2.AddTool(101, "Test", tb2_bmp1)
        # tb2.Realize()
        #
        # tb3 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
        #                  wx.TB_FLAT | wx.TB_NODIVIDER)
        # tb3.SetToolBitmapSize(wx.Size(16,16))
        # tb3_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16))
        # tb3.AddTool(101, "Test", tb3_bmp1)
        # tb3.AddTool(101, "Test", tb3_bmp1)
        # tb3.AddTool(101, "Test", tb3_bmp1)
        # tb3.AddTool(101, "Test", tb3_bmp1)
        # tb3.AddSeparator()
        # tb3.AddTool(101, "Test", tb3_bmp1)
        # tb3.AddTool(101, "Test", tb3_bmp1)
        # tb3.Realize()

        # 创建工具栏 此处用于主要功能按钮

        # 创建工具栏
        tb4 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        # 设置工具栏图标大小
        tb4.SetToolBitmapSize(wx.Size(16,16))

        # 获得工具栏图标，若要更换，可读取其他图片创建wx.Bitmap类进行赋值
        tb4_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))

        # 与前面的wx.Newid对应，不同的ID在后面绑定了不同的函数
        tb4.AddTool(ID_Supervise, "实时监控", tb4_bmp1)
        tb4.AddTool(ID_History, "历史记录", tb4_bmp1)
        # tb4.AddTool(ID_Bill, "统计分析", tb4_bmp1)
        # tb4.AddTool(ID_Bill, "缴费明细", tb4_bmp1)
        tb4.AddTool(ID_Cb, "抄表中心", tb4_bmp1)
        # tb4.AddSeparator()
        # self.combo = wx.ComboBox(tb4,-1,value='单间模式',choices=['单间模式','总览模式'],style=wx.CB_READONLY)
        # self.Bind(wx.EVT_COMBOBOX,self.OnModeChange,self.combo)
        # tb4.AddControl(self.combo,label='实时监控模式')
        # tb4.AddCheckTool(ID_Mode,'单间模式',tb4_bmp1)
        tb4.Realize()

        # tb5 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
        #                  wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_VERTICAL)
        # tb5.SetToolBitmapSize(wx.Size(48, 48))
        # tb5.AddTool(101, "Test", wx.ArtProvider.GetBitmap(wx.ART_ERROR))
        # tb5.AddSeparator()
        # tb5.AddTool(102, "Test", wx.ArtProvider.GetBitmap(wx.ART_QUESTION))
        # tb5.AddTool(103, "Test", wx.ArtProvider.GetBitmap(wx.ART_INFORMATION))
        # tb5.AddTool(103, "Test", wx.ArtProvider.GetBitmap(wx.ART_WARNING))
        # tb5.AddTool(103, "Test", wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE))
        # tb5.Realize()

        # add a bunch of panes
        # self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
        #                   Name("test1").Caption("Pane Caption").Top().
        #                   CloseButton(True).MaximizeButton(True))
        #
        # self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
        #                   Name("test2").Caption("Client Size Reporter").
        #                   Bottom().Position(1).CloseButton(True).MaximizeButton(True))
        #
        # self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
        #                   Name("test3").Caption("Client Size Reporter").
        #                   Bottom().CloseButton(True).MaximizeButton(True))
        #
        # self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
        #                   Name("test4").Caption("Pane Caption").
        #                   Left().CloseButton(True).MaximizeButton(True))
        #
        # self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
        #                   Name("test5").Caption("Pane Caption").
        #                   Right().CloseButton(True).MaximizeButton(True))
        #
        # self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
        #                   Name("test6").Caption("Client Size Reporter").
        #                   Right().Row(1).CloseButton(True).MaximizeButton(True))
        #
        # self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
        #                   Name("test7").Caption("Client Size Reporter").
        #                   Left().Layer(1).CloseButton(True).MaximizeButton(True))

        # 将创建的面板添加到aui面板管理器内

        # 将创建的面板（包括工具栏）添加到面板管理器中
        self._mgr.AddPane(self.main_tree, aui.AuiPaneInfo().
                          Name("main_tree").Caption("宿舍楼水电管理系统").MinSize(wx.Size(200,100)).
                          Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))


        self._mgr.AddPane(self.room_panel, aui.AuiPaneInfo().
                          Name("Room Panel").CenterPane().Hide())

        self._mgr.AddPane(self.history_panel, aui.AuiPaneInfo().Name("History Panel").
                          CenterPane().Hide())

        self._mgr.AddPane(self.login_panel, aui.AuiPaneInfo().Name("Login Panel").
                          CenterPane())

        self._mgr.AddPane(self.info_panel, aui.AuiPaneInfo().Name("Info Panel").
                          Bottom().Position(1).CloseButton(False).CaptionVisible(False))

        self._mgr.AddPane(self.cb_panel, aui.AuiPaneInfo().Name("Cb Panel").
                          CenterPane().Hide())

        # self._mgr.AddPane(self.allroom_panel, aui.AuiPaneInfo().Name("Allroom Panel").
        #                   CenterPane().Hide())

        self._mgr.AddPane(self.setting_panel, aui.AuiPaneInfo().Name("Setting Panel").
                          CenterPane().Hide())

        self._mgr.AddPane(tb4, aui.AuiPaneInfo().
                          Name("tb4").Caption("Main Function Toolbar").
                          ToolbarPane().Top().Row(1).
                          LeftDockable(False).RightDockable(False))

        # 对各面板的显示状态进行了设定，注意此处一定要加Update()进行面板刷新
        all_panes = self._mgr.GetAllPanes()
        for ii in range(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()

        # self._mgr.GetPane("main_tree").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("Login Panel").Show()
        self._mgr.GetPane('Info Panel').Show()
        self._mgr.Update()
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        # self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Show How To Use The Closing Panes Event
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)

        # 功能按钮绑定切换函数
        # 此处将不同菜单事件ID传入OnChangeContentPane函数，不同工具栏按钮传入的ID是不同的，以此切换到不同的面板
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_Supervise)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_History)
        # self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_Bill)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_Cb)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_Settings)
        self.Bind(wx.EVT_MENU, self.OnModeChange,id=ID_Mode)


        # 以下是其他的一些事件Bind，基本没有用到
        self.Bind(wx.EVT_MENU, self.OnCreateTree, id=ID_CreateTree)
        self.Bind(wx.EVT_MENU, self.OnCreateGrid, id=ID_CreateGrid)
        self.Bind(wx.EVT_MENU, self.OnCreateText, id=ID_CreateText)
        self.Bind(wx.EVT_MENU, self.OnCreateHTML, id=ID_CreateHTML)
        # self.Bind(wx.EVT_MENU, self.OnCreateSizeReport, id=ID_CreateSizeReport)
        # self.Bind(wx.EVT_MENU, self.OnCreatePerspective, id=ID_CreatePerspective)
        # self.Bind(wx.EVT_MENU, self.OnCopyPerspective, id=ID_CopyPerspective)

        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowFloating)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_RectangleHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_HintFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentDrag)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowActivePane)

        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_NoGradient)
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_VerticalGradient)
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_HorizontalGradient)
        self.Bind(wx.EVT_MENU, self.OnSettings, id=ID_Settings)

        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)

        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_RectangleHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HintFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowFloating)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentDrag)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowActivePane)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VerticalGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HorizontalGradient)

        # self.Bind(wx.EVT_MENU_RANGE, self.OnRestorePerspective, id=ID_FirstPerspective,
        #           id2=ID_FirstPerspective+1000)

        self.Show(True)

        # 登录状态检测计时器
        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.OnTimer1,self.timer1)

        # 时间实时显示计时器
        self.timer2 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer2, self.timer2)

        # 加载配置文件
        with open('config/config.json','r') as f:
            self.config = json.load(f)

        # 检测是否存在用户信息
        df = get_login_info(None)
        if len(df) < 0:
            wx.MessageBox('系统中暂无用户信息，请先创建管理员用户进行登录。','提示')
            # TODO：创建管理员用户界面

        self.checklogin()
        self.timer1.Start(10)
        self.timer2.Start(1000)

    def update_statusbar(self):
        flag = False
        for thread in threading.enumerate():
            if thread.getName() == 'LookUpMeter':
                flag = True
        if flag:
            self.statusbar.SetStatusText("正在查表", 0)
            self.cb_panel.button1.Enable(False)
            if self._mgr.GetPane('Info Panel').IsShown():
                pass
            else:
                self._mgr.GetPane('Info Panel').Show()
                self._mgr.Update()
        else:
            self.statusbar.SetStatusText("正常", 0)
            self.cb_panel.button1.Enable(True)
            if not self._mgr.GetPane('Info Panel').IsShown():
                pass
            else:
                self._mgr.GetPane('Info Panel').Hide()
                self._mgr.Update()



    def OnTimer1(self,event):
        self.checklogin()
        self.update_statusbar()
        # print(self.supervise_mode)

    def OnTimer2(self,event):
        t = time.strftime("%Y-%m-%d  %H:%M:%S",time.localtime())
        self.statusbar.SetStatusText(t,1)

    # 检测登录状态
    # 先检测数据库中有无用户信息
    # 在登录面板中，成功登录后只修改了主窗口中的登录状态，并未实现面板的跳转。跳转在此处实现。
    # 通过定时器定时检测登录状态，未登录只显示登录面板，登录则显示工具栏和右侧树面板
    # 通过设置前一登录状态记录self.l_login和当前登录状态self.login，
    #   每次进行比较，只有在发生变化时进行面板管理器的刷新，避免频繁刷新造成界面闪烁
    def checklogin(self):

        self.login = self.login_panel.login_flag
        if not self.login:
            if not self.l_login:
                pass
            else:
                for name in self.centre_pane_list:
                    self._mgr.GetPane(name).Hide()
                self._mgr.GetPane('main_tree').Hide()
                self._mgr.GetPane('tb4').Hide()
                self._mgr.GetPane('Login Panel').Show()
                self._mgr.Update()
        else:
            if self.l_login:
                pass
            else:
                self._mgr.GetPane('main_tree').Show().Left().Layer(0).Row(0).Position(0)
                self._mgr.GetPane('tb4').Show()
                self._mgr.Update()
        self.l_login = self.login

    def LevelChange(self,level):
        if level == 0:
            pass
        else:
            self.cb_panel.button3.Enable(False)

    # 跳转到设置面板
    # 由于设置面板的跳转在抄表中心面板通过按钮点击而非工具栏触发，因此保留这个函数供按钮调用函数内使用。
    # 其他面板的跳转由OnChangeContentPane统一完成
    def ToSettingPanel(self,event):
        if self.login:
            for name in self.centre_pane_list:
                if not name in ['Setting Panel']:
                    self._mgr.GetPane(name).Hide()
                else:
                    self._mgr.GetPane(name).Show()
            self._mgr.Update()
        self.setting_panel.update()
    # 房间变动事件
    # 当双击右侧树时，触发树变动事件并调用此函数。根据事件返回的树选择项即房间号进行处理。
    # 调用与房间号相关的Room Panel 和 History Panel的room_change函数。
    def OnTreeChanged(self,event):
        item = event.GetItem()
        self.main_tree.Expand(item)
        itemname = self.main_tree.GetItemText(item)
        if str(itemname).endswith('楼'):
            pass
        else:
            self.room_num = self.main_tree.GetItemText(item)
            self.room_panel.room_change(self.room_num)
            self.history_panel.room_change(self.room_num)
            self.setting_panel.room_change(self.room_num)
        # print(item,'\n',self.main_tree.GetItemText(item))

    # 模式切换事件
    # 用于控制实时监控的单间模式和总览模式的切换
    def OnModeChange(self,event):
        self.supervise_mode = bool(1-self.supervise_mode)  # 事件触发，对状态标志取反，切换模式状态
        if self._mgr.GetPane('Room Panel').IsShown() or self._mgr.GetPane('Allroom Panel').IsShown():
            # 先判断当前是否在实时监控界面
            if self.supervise_mode:
                self._mgr.GetPane('Room Panel').Show()
                self._mgr.GetPane('Allroom Panel').Hide()
            else:
                self._mgr.GetPane('Room Panel').Hide()
                self._mgr.GetPane('Allroom Panel').Show()
        self._mgr.Update()

    # 面板关闭事件
    # 目前只有右侧树和设置面板是可关闭的。当这两个面板关闭时触发事件调用此函数。
    # 对于设置面板，设定关闭后回到抄表中心面板，即让抄表中心面板重新显示。
    # 对于右侧树面板，关闭时发出提示。这里建议考虑是否设定右侧树面板无法关闭，因为关闭后目前没有入口可重新创建它。
    def OnPaneClose(self, event):

        caption = event.GetPane().caption
        name = event.GetPane().name

        if name == "Setting Panel":
            self._mgr.GetPane('Cb Panel').Show()
            self._mgr.Update()

        if caption in ["Tree Pane", "Dock Manager Settings", "Fixed Pane"]:
            msg = "Are You Sure You Want To Close This Pane?"
            dlg = wx.MessageDialog(self, msg, "AUI Question",
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

            if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
                event.Veto()
            dlg.Destroy()

    # 面板切换函数
    def OnChangeContentPane(self, event):

        # Show(True)面板显示，Show(False)面板关闭
        # 根据事件传入的ID号来判断按下的时哪一个按钮，转到对应面板。
        self._mgr.GetPane("Login Panel").Hide()
        # 对于实时监控，额外增加当前模式的判断，转向不同的界面。
        self._mgr.GetPane("Room Panel").Show(event.GetId() == ID_Supervise)
        # self._mgr.GetPane('Allroom Panel').Show(event.GetId() == ID_Supervise and not self.supervise_mode)
        self._mgr.GetPane("History Panel").Show(event.GetId() == ID_History)
        self._mgr.GetPane("Cb Panel").Show(event.GetId() == ID_Cb or event.GetId() == ID_Settings)
        self._mgr.GetPane("Setting Panel").Show(event.GetId() == ID_Settings)
        # self._mgr.GetPane("Bill Panel").Show(event.GetId() == ID_Bill)
        self._mgr.Update()


    def OnClose(self, event):
        self._mgr.UnInit()
        del self._mgr
        self.Destroy()


    def OnExit(self, event):
        self.Close()

    # 以下函数基本没有用到
    def OnAbout(self, event):

        msg = "wx.aui Demo\n" + \
              "An advanced window management library for wxWidgets\n" + \
              "(c) Copyright 2005-2006, Kirix Corporation"
        dlg = wx.MessageDialog(self, msg, "About wx.aui Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def GetDockArt(self):

        return self._mgr.GetArtProvider()


    def OnSettings(self, event):

        # show the settings pane, and float it
        floating_pane = self._mgr.GetPane("settings").Float().Show()

        if floating_pane.floating_pos == wx.DefaultPosition:
            floating_pane.FloatingPosition(self.GetStartPosition())

        self._mgr.Update()


    def OnGradient(self, event):

        gradient = 0

        if event.GetId() == ID_NoGradient:
            gradient = aui.AUI_GRADIENT_NONE
        elif event.GetId() == ID_VerticalGradient:
            gradient = aui.AUI_GRADIENT_VERTICAL
        elif event.GetId() == ID_HorizontalGradient:
            gradient = aui.AUI_GRADIENT_HORIZONTAL

        self._mgr.GetArtProvider().SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE, gradient)
        self._mgr.Update()


    def OnManagerFlag(self, event):

        flag = 0
        eid = event.GetId()

        if eid in [ ID_TransparentHint, ID_VenetianBlindsHint, ID_RectangleHint, ID_NoHint ]:
            flags = self._mgr.GetFlags()
            flags &= ~aui.AUI_MGR_TRANSPARENT_HINT
            flags &= ~aui.AUI_MGR_VENETIAN_BLINDS_HINT
            flags &= ~aui.AUI_MGR_RECTANGLE_HINT
            self._mgr.SetFlags(flags)

        if eid == ID_AllowFloating:
            flag = aui.AUI_MGR_ALLOW_FLOATING
        elif eid == ID_TransparentDrag:
            flag = aui.AUI_MGR_TRANSPARENT_DRAG
        elif eid == ID_HintFade:
            flag = aui.AUI_MGR_HINT_FADE
        elif eid == ID_NoVenetianFade:
            flag = aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        elif eid == ID_AllowActivePane:
            flag = aui.AUI_MGR_ALLOW_ACTIVE_PANE
        elif eid == ID_TransparentHint:
            flag = aui.AUI_MGR_TRANSPARENT_HINT
        elif eid == ID_VenetianBlindsHint:
            flag = aui.AUI_MGR_VENETIAN_BLINDS_HINT
        elif eid == ID_RectangleHint:
            flag = aui.AUI_MGR_RECTANGLE_HINT

        self._mgr.SetFlags(self._mgr.GetFlags() ^ flag)


    def OnUpdateUI(self, event):

        flags = self._mgr.GetFlags()
        eid = event.GetId()

        if eid == ID_NoGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(aui.AUI_DOCKART_GRADIENT_TYPE) == aui.AUI_GRADIENT_NONE)

        elif eid == ID_VerticalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(aui.AUI_DOCKART_GRADIENT_TYPE) == aui.AUI_GRADIENT_VERTICAL)

        elif eid == ID_HorizontalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(aui.AUI_DOCKART_GRADIENT_TYPE) == aui.AUI_GRADIENT_HORIZONTAL)

        elif eid == ID_AllowFloating:
            event.Check((flags & aui.AUI_MGR_ALLOW_FLOATING) != 0)

        elif eid == ID_TransparentDrag:
            event.Check((flags & aui.AUI_MGR_TRANSPARENT_DRAG) != 0)

        elif eid == ID_TransparentHint:
            event.Check((flags & aui.AUI_MGR_TRANSPARENT_HINT) != 0)

        elif eid == ID_VenetianBlindsHint:
            event.Check((flags & aui.AUI_MGR_VENETIAN_BLINDS_HINT) != 0)

        elif eid == ID_RectangleHint:
            event.Check((flags & aui.AUI_MGR_RECTANGLE_HINT) != 0)

        elif eid == ID_NoHint:
            event.Check(((aui.AUI_MGR_TRANSPARENT_HINT |
                          aui.AUI_MGR_VENETIAN_BLINDS_HINT |
                          aui.AUI_MGR_RECTANGLE_HINT) & flags) == 0)

        elif eid == ID_HintFade:
            event.Check((flags & aui.AUI_MGR_HINT_FADE) != 0);

        elif eid == ID_NoVenetianFade:
            event.Check((flags & aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE) != 0);

    def GetStartPosition(self):

        self.x = self.x + 20
        x = self.x
        pt = self.ClientToScreen(wx.Point(0, 0))

        return wx.Point(pt.x + x, pt.y + x)


    def OnCreateTree(self, event):
        self._mgr.AddPane(self.CreateTreeCtrl(), aui.AuiPaneInfo().
                          Caption("Tree Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(150, 300)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateGrid(self, event):
        self._mgr.AddPane(self.CreateGrid(), aui.AuiPaneInfo().
                          Caption("Grid").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateHTML(self, event):
        self._mgr.AddPane(self.CreateHTMLCtrl(), aui.AuiPaneInfo().
                          Caption("HTML Content").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateText(self, event):
        self._mgr.AddPane(self.CreateTextCtrl(), aui.AuiPaneInfo().
                          Caption("Text Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    # def OnCreateSizeReport(self, event):
    #     self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
    #                       Caption("Client Size Reporter").
    #                       Float().FloatingPosition(self.GetStartPosition()).
    #                       CloseButton(True).MaximizeButton(True))
    #     self._mgr.Update()


    def CreateTextCtrl(self):

        text = ("This is text box %d")%(self.n + 1)

        return wx.TextCtrl(self,-1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)



    def CreateGrid(self):

        grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(150, 250),
                            wx.NO_BORDER | wx.WANTS_CHARS)

        grid.CreateGrid(50, 20)

        return grid


    def CreateTreeCtrl(self):

        tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)

        root = tree.AddRoot("宿舍楼1")
        items = []

        imglist = wx.ImageList(16, 16, True, 2)

        imglist.Add(wx.Bitmap(r'images\building.png', wx.BITMAP_TYPE_PNG))
        imglist.Add(wx.Bitmap(r'images\house.png',wx.BITMAP_TYPE_PNG))

        # imglist.Add(wx.Bitmap(r'D:\资料\研究生\info_GUI\watch.png',wx.BITMAP_TYPE_PNG))
        tree.AssignImageList(imglist)
        for i in range(2,11):
            items.append(tree.AppendItem(root, f"{i}楼", 0))


        for ii in range(len(items)):
            id = items[ii]
            for j in range(1,38):
                tree.AppendItem(id, room_num_format(ii+2,j), 1)

        tree.Expand(root)

        return tree


    # def CreateSizeReportCtrl(self, width=80, height=80):
    #
    #     ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition,
    #                           wx.Size(width, height), self._mgr)
    #     return ctrl


    def CreateHTMLCtrl(self):
        ctrl = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.Size(400, 300))
        if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
            ctrl.SetStandardFonts()
        ctrl.SetPage(self.GetIntroText())
        return ctrl


    def GetIntroText(self):
        return overview


# -- wx.SizeReportCtrl --
# (a utility control that always reports it's client size)



# class SizeReportCtrl(wx.Control):
#
#     def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
#                  size=wx.DefaultSize, mgr=None):
#
#         wx.Control.__init__(self, parent, id, pos, size, wx.NO_BORDER)
#
#         self._mgr = mgr
#
#         self.Bind(wx.EVT_PAINT, self.OnPaint)
#         self.Bind(wx.EVT_SIZE, self.OnSize)
#         self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
#

#     def OnPaint(self, event):
#
#         dc = wx.PaintDC(self)
#
#         size = self.GetClientSize()
#         s = ("Size: %d x %d")%(size.x, size.y)
#
#         dc.SetFont(wx.NORMAL_FONT)
#         w, height = dc.GetTextExtent(s)
#         height = height + 3
#         dc.SetBrush(wx.WHITE_BRUSH)
#         dc.SetPen(wx.WHITE_PEN)
#         dc.DrawRectangle(0, 0, size.x, size.y)
#         dc.SetPen(wx.LIGHT_GREY_PEN)
#         dc.DrawLine(0, 0, size.x, size.y)
#         dc.DrawLine(0, size.y, size.x, 0)
#         dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2))
#
#         if self._mgr:
#
#             pi = self._mgr.GetPane(self)
#
#             s = ("Layer: %d")%pi.dock_layer
#             w, h = dc.GetTextExtent(s)
#             dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*1))
#
#             s = ("Dock: %d Row: %d")%(pi.dock_direction, pi.dock_row)
#             w, h = dc.GetTextExtent(s)
#             dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*2))
#
#             s = ("Position: %d")%pi.dock_pos
#             w, h = dc.GetTextExtent(s)
#             dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*3))
#
#             s = ("Proportion: %d")%pi.dock_proportion
#             w, h = dc.GetTextExtent(s)
#             dc.DrawText(s, (size.x-w)/2, ((size.y-(height*5))/2)+(height*4))
#
#
    def OnEraseBackground(self, event):
        # intentionally empty
        pass
#
#
#     def OnSize(self, event):
#
#         self.Refresh()
#         event.Skip()

# 下面是示例Demo自带的两种Panel，并未用到

ID_PaneBorderSize = wx.ID_HIGHEST + 1
ID_SashSize = ID_PaneBorderSize + 1
ID_CaptionSize = ID_PaneBorderSize + 2
ID_BackgroundColor = ID_PaneBorderSize + 3
ID_SashColor = ID_PaneBorderSize + 4
ID_InactiveCaptionColor =  ID_PaneBorderSize + 5
ID_InactiveCaptionGradientColor = ID_PaneBorderSize + 6
ID_InactiveCaptionTextColor = ID_PaneBorderSize + 7
ID_ActiveCaptionColor = ID_PaneBorderSize + 8
ID_ActiveCaptionGradientColor = ID_PaneBorderSize + 9
ID_ActiveCaptionTextColor = ID_PaneBorderSize + 10
ID_BorderColor = ID_PaneBorderSize + 11
ID_GripperColor = ID_PaneBorderSize + 12

class SettingsPanel(wx.Panel):

    def __init__(self, parent, frame):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        self._frame = frame

        vert = wx.BoxSizer(wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        self._border_size = wx.SpinCtrl(self, ID_PaneBorderSize, "", wx.DefaultPosition, wx.Size(50,20))
        s1.Add((1, 1), 1, wx.EXPAND)
        s1.Add(wx.StaticText(self, -1, "Pane Border Size:"))
        s1.Add(self._border_size)
        s1.Add((1, 1), 1, wx.EXPAND)
        s1.SetItemMinSize(1, (180, 20))
        #vert.Add(s1, 0, wx.EXPAND | wxLEFT | wxBOTTOM, 5)

        s2 = wx.BoxSizer(wx.HORIZONTAL)
        self._sash_size = wx.SpinCtrl(self, ID_SashSize, "", wx.DefaultPosition, wx.Size(50,20))
        s2.Add((1, 1), 1, wx.EXPAND)
        s2.Add(wx.StaticText(self, -1, "Sash Size:"))
        s2.Add(self._sash_size)
        s2.Add((1, 1), 1, wx.EXPAND)
        s2.SetItemMinSize(1, (180, 20))
        #vert.Add(s2, 0, wx.EXPAND | wxLEFT | wxBOTTOM, 5)

        s3 = wx.BoxSizer(wx.HORIZONTAL)
        self._caption_size = wx.SpinCtrl(self, ID_CaptionSize, "", wx.DefaultPosition, wx.Size(50,20))
        s3.Add((1, 1), 1, wx.EXPAND)
        s3.Add(wx.StaticText(self, -1, "Caption Size:"))
        s3.Add(self._caption_size)
        s3.Add((1, 1), 1, wx.EXPAND)
        s3.SetItemMinSize(1, (180, 20))
        #vert.Add(s3, 0, wx.EXPAND | wxLEFT | wxBOTTOM, 5)

        #vert.Add(1, 1, 1, wx.EXPAND)

        b = self.CreateColorBitmap(wx.BLACK)

        s4 = wx.BoxSizer(wx.HORIZONTAL)
        self._background_color = wx.BitmapButton(self, ID_BackgroundColor, b, wx.DefaultPosition, wx.Size(50,25))
        s4.Add((1, 1), 1, wx.EXPAND)
        s4.Add(wx.StaticText(self, -1, "Background Color:"))
        s4.Add(self._background_color)
        s4.Add((1, 1), 1, wx.EXPAND)
        s4.SetItemMinSize(1, (180, 20))

        s5 = wx.BoxSizer(wx.HORIZONTAL)
        self._sash_color = wx.BitmapButton(self, ID_SashColor, b, wx.DefaultPosition, wx.Size(50,25))
        s5.Add((1, 1), 1, wx.EXPAND)
        s5.Add(wx.StaticText(self, -1, "Sash Color:"))
        s5.Add(self._sash_color)
        s5.Add((1, 1), 1, wx.EXPAND)
        s5.SetItemMinSize(1, (180, 20))

        s6 = wx.BoxSizer(wx.HORIZONTAL)
        self._inactive_caption_color = wx.BitmapButton(self, ID_InactiveCaptionColor, b,
                                                       wx.DefaultPosition, wx.Size(50,25))
        s6.Add((1, 1), 1, wx.EXPAND)
        s6.Add(wx.StaticText(self, -1, "Normal Caption:"))
        s6.Add(self._inactive_caption_color)
        s6.Add((1, 1), 1, wx.EXPAND)
        s6.SetItemMinSize(1, (180, 20))

        s7 = wx.BoxSizer(wx.HORIZONTAL)
        self._inactive_caption_gradient_color = wx.BitmapButton(self, ID_InactiveCaptionGradientColor,
                                                                b, wx.DefaultPosition, wx.Size(50,25))
        s7.Add((1, 1), 1, wx.EXPAND)
        s7.Add(wx.StaticText(self, -1, "Normal Caption Gradient:"))
        s7.Add(self._inactive_caption_gradient_color)
        s7.Add((1, 1), 1, wx.EXPAND)
        s7.SetItemMinSize(1, (180, 20))

        s8 = wx.BoxSizer(wx.HORIZONTAL)
        self._inactive_caption_text_color = wx.BitmapButton(self, ID_InactiveCaptionTextColor, b,
                                                            wx.DefaultPosition, wx.Size(50,25))
        s8.Add((1, 1), 1, wx.EXPAND)
        s8.Add(wx.StaticText(self, -1, "Normal Caption Text:"))
        s8.Add(self._inactive_caption_text_color)
        s8.Add((1, 1), 1, wx.EXPAND)
        s8.SetItemMinSize(1, (180, 20))

        s9 = wx.BoxSizer(wx.HORIZONTAL)
        self._active_caption_color = wx.BitmapButton(self, ID_ActiveCaptionColor, b,
                                                     wx.DefaultPosition, wx.Size(50,25))
        s9.Add((1, 1), 1, wx.EXPAND)
        s9.Add(wx.StaticText(self, -1, "Active Caption:"))
        s9.Add(self._active_caption_color)
        s9.Add((1, 1), 1, wx.EXPAND)
        s9.SetItemMinSize(1, (180, 20))

        s10 = wx.BoxSizer(wx.HORIZONTAL)
        self._active_caption_gradient_color = wx.BitmapButton(self, ID_ActiveCaptionGradientColor,
                                                              b, wx.DefaultPosition, wx.Size(50,25))
        s10.Add((1, 1), 1, wx.EXPAND)
        s10.Add(wx.StaticText(self, -1, "Active Caption Gradient:"))
        s10.Add(self._active_caption_gradient_color)
        s10.Add((1, 1), 1, wx.EXPAND)
        s10.SetItemMinSize(1, (180, 20))

        s11 = wx.BoxSizer(wx.HORIZONTAL)
        self._active_caption_text_color = wx.BitmapButton(self, ID_ActiveCaptionTextColor,
                                                          b, wx.DefaultPosition, wx.Size(50,25))
        s11.Add((1, 1), 1, wx.EXPAND)
        s11.Add(wx.StaticText(self, -1, "Active Caption Text:"))
        s11.Add(self._active_caption_text_color)
        s11.Add((1, 1), 1, wx.EXPAND)
        s11.SetItemMinSize(1, (180, 20))

        s12 = wx.BoxSizer(wx.HORIZONTAL)
        self._border_color = wx.BitmapButton(self, ID_BorderColor, b, wx.DefaultPosition,
                                             wx.Size(50,25))
        s12.Add((1, 1), 1, wx.EXPAND)
        s12.Add(wx.StaticText(self, -1, "Border Color:"))
        s12.Add(self._border_color)
        s12.Add((1, 1), 1, wx.EXPAND)
        s12.SetItemMinSize(1, (180, 20))

        s13 = wx.BoxSizer(wx.HORIZONTAL)
        self._gripper_color = wx.BitmapButton(self, ID_GripperColor, b, wx.DefaultPosition,
                                              wx.Size(50,25))
        s13.Add((1, 1), 1, wx.EXPAND)
        s13.Add(wx.StaticText(self, -1, "Gripper Color:"))
        s13.Add(self._gripper_color)
        s13.Add((1, 1), 1, wx.EXPAND)
        s13.SetItemMinSize(1, (180, 20))

        grid_sizer = wx.GridSizer(cols=2)
        grid_sizer.SetHGap(5)
        grid_sizer.Add(s1)
        grid_sizer.Add(s4)
        grid_sizer.Add(s2)
        grid_sizer.Add(s5)
        grid_sizer.Add(s3)
        grid_sizer.Add(s13)
        grid_sizer.Add((1, 1))
        grid_sizer.Add(s12)
        grid_sizer.Add(s6)
        grid_sizer.Add(s9)
        grid_sizer.Add(s7)
        grid_sizer.Add(s10)
        grid_sizer.Add(s8)
        grid_sizer.Add(s11)

        cont_sizer = wx.BoxSizer(wx.VERTICAL)
        cont_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(cont_sizer)
        self.GetSizer().SetSizeHints(self)

        self._border_size.SetValue(frame.GetDockArt().GetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE))
        self._sash_size.SetValue(frame.GetDockArt().GetMetric(aui.AUI_DOCKART_SASH_SIZE))
        self._caption_size.SetValue(frame.GetDockArt().GetMetric(aui.AUI_DOCKART_CAPTION_SIZE))

        self.UpdateColors()

        self.Bind(wx.EVT_SPINCTRL, self.OnPaneBorderSize, id=ID_PaneBorderSize)
        self.Bind(wx.EVT_SPINCTRL, self.OnSashSize, id=ID_SashSize)
        self.Bind(wx.EVT_SPINCTRL, self.OnCaptionSize, id=ID_CaptionSize)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_BackgroundColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_SashColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_InactiveCaptionColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_InactiveCaptionGradientColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_InactiveCaptionTextColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_ActiveCaptionColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_ActiveCaptionGradientColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_ActiveCaptionTextColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_BorderColor)
        self.Bind(wx.EVT_BUTTON, self.OnSetColor, id=ID_GripperColor)



    def CreateColorBitmap(self, c):
        image = wx.Image(25, 14)

        for x in range(25):
            for y in range(14):
                pixcol = c
                if x == 0 or x == 24 or y == 0 or y == 13:
                    pixcol = wx.BLACK

                image.SetRGB(x, y, pixcol.Red(), pixcol.Green(), pixcol.Blue())

        return image.ConvertToBitmap()


    def UpdateColors(self):

        bk = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_BACKGROUND_COLOUR)
        self._background_color.SetBitmapLabel(self.CreateColorBitmap(bk))

        cap = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR)
        self._inactive_caption_color.SetBitmapLabel(self.CreateColorBitmap(cap))

        capgrad = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR)
        self._inactive_caption_gradient_color.SetBitmapLabel(self.CreateColorBitmap(capgrad))

        captxt = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR)
        self._inactive_caption_text_color.SetBitmapLabel(self.CreateColorBitmap(captxt))

        acap = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR)
        self._active_caption_color.SetBitmapLabel(self.CreateColorBitmap(acap))

        acapgrad = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_ACTIVE_CAPTION_GRADIENT_COLOUR)
        self._active_caption_gradient_color.SetBitmapLabel(self.CreateColorBitmap(acapgrad))

        acaptxt = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR)
        self._active_caption_text_color.SetBitmapLabel(self.CreateColorBitmap(acaptxt))

        sash = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_SASH_COLOUR)
        self._sash_color.SetBitmapLabel(self.CreateColorBitmap(sash))

        border = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_BORDER_COLOUR)
        self._border_color.SetBitmapLabel(self.CreateColorBitmap(border))

        gripper = self._frame.GetDockArt().GetColour(aui.AUI_DOCKART_GRIPPER_COLOUR)
        self._gripper_color.SetBitmapLabel(self.CreateColorBitmap(gripper))


    def OnPaneBorderSize(self, event):

        self._frame.GetDockArt().SetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE,
                                           event.GetInt())
        self._frame.DoUpdate()


    def OnSashSize(self, event):

        self._frame.GetDockArt().SetMetric(aui.AUI_DOCKART_SASH_SIZE,
                                           event.GetInt())
        self._frame.DoUpdate()


    def OnCaptionSize(self, event):

        self._frame.GetDockArt().SetMetric(aui.AUI_DOCKART_CAPTION_SIZE,
                                           event.GetInt())
        self._frame.DoUpdate()


    def OnSetColor(self, event):

        dlg = wx.ColourDialog(self._frame)

        dlg.SetTitle("Color Picker")

        if dlg.ShowModal() != wx.ID_OK:
            return

        var = 0
        if event.GetId() == ID_BackgroundColor:
            var = aui.AUI_DOCKART_BACKGROUND_COLOUR
        elif event.GetId() == ID_SashColor:
            var = aui.AUI_DOCKART_SASH_COLOUR
        elif event.GetId() == ID_InactiveCaptionColor:
            var = aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR
        elif event.GetId() == ID_InactiveCaptionGradientColor:
            var = aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR
        elif event.GetId() == ID_InactiveCaptionTextColor:
            var = aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR
        elif event.GetId() == ID_ActiveCaptionColor:
            var = aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR
        elif event.GetId() == ID_ActiveCaptionGradientColor:
            var = aui.AUI_DOCKART_ACTIVE_CAPTION_GRADIENT_COLOUR
        elif event.GetId() == ID_ActiveCaptionTextColor:
            var = aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR
        elif event.GetId() == ID_BorderColor:
            var = aui.AUI_DOCKART_BORDER_COLOUR
        elif event.GetId() == ID_GripperColor:
            var = aui.AUI_DOCKART_GRIPPER_COLOUR
        else:
            return

        self._frame.GetDockArt().SetColor(var, dlg.GetColourData().GetColour())
        self._frame.DoUpdate()
        self.UpdateColors()



#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        b = wx.Button(self, -1, "Show the aui Demo Frame", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

    def OnButton(self, evt):
        frame = PyAUIFrame(self, wx.ID_ANY, "aui wxPython Demo", size=(750, 590))
        frame.Show()

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """\
<html><body>
<h3>欢迎使用宿舍水电管理系统</h3>
</body></html>
"""

# <br/><b>Overview</b><br/>
#
# <p>aui is an Advanced User Interface library for the wxWidgets toolkit
# that allows developers to create high-quality, cross-platform user
# interfaces quickly and easily.</p>
#
# <p><b>Features</b></p>
#
# <p>With aui developers can create application frameworks with:</p>
#
# <ul>
# <li>Native, dockable floating frames</li>
# <li>Perspective saving and loading</li>
# <li>Native toolbars incorporating real-time, &quot;spring-loaded&quot; dragging</li>
# <li>Customizable floating/docking behavior</li>
# <li>Completely customizable look-and-feel</li>
# <li>Optional transparent window effects (while dragging or docking)</li>
# </ul>
#
#





if __name__ == '__main__':
    app = wx.App()
    frame = PyAUIFrame(None)
    app.MainLoop()

