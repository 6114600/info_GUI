import wx
from utils import get_textctrl_bold
from utils.getData import get_data
from utils.PandasToGrid import PandasToGrid

class InfoPanel(wx.Panel):
    def __init__(self, parent, frame):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize)

        self.SetSize((1000,50))
        vbox = wx.BoxSizer(wx.VERTICAL)
        box = wx.BoxSizer(wx.HORIZONTAL)
        img = wx.StaticBitmap(self,-1,wx.Bitmap(30,30))
        img.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_INFORMATION,size=(30, 30)))
        box.Add(img,0,wx.ALL|wx.ALIGN_CENTRE_VERTICAL)
        box.AddSpacer(20)
        box.Add(get_textctrl_bold(self,'正在抄表',16),0,wx.ALL|wx.ALIGN_CENTRE_VERTICAL)
        vbox.AddSpacer(5)
        vbox.Add(box,0,wx.ALIGN_CENTRE)
        self.SetSizer(vbox)


