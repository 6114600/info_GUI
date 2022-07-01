import wx
import json
from utils.loghelper import set_logger

def get_bold_font(size):
    return wx.Font(size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

def get_textctrl_bold(parent,text,size):
    textcrtl = wx.StaticText(parent,-1,text)
    textcrtl.SetFont(get_bold_font(size))
    return textcrtl

def room_num_format(floor,room):
    if floor > 9:
        floor_str = str(floor)
    else:
        floor_str = '0'+str(floor)

    if room > 9:
        room_str = str(room)
    else:
        room_str = '0'+ str(room)
    return floor_str+room_str

def load_config_file():
    logger = set_logger('debug','log/test.log')
    try:
        with open('config/config.json','r') as fp:
            config = json.load(fp)
        return config
    except Exception as e:
        logger.error('配置文件读取错误，请检查配置文件是否在正确位置。')
        logger.error(e)

def edit_config_file(new_config):
    logger = set_logger('debug', 'log/test.log')
    try:
        with open('config/config.json', 'w') as fp:
            json.dump(new_config,fp,sort_keys=False,ensure_ascii=True)
        return True
    except Exception as e:
        logger.error('配置文件读取错误，请检查配置文件是否在正确位置。')
        logger.error(e)
        return False


import wx
# import wx.lib.imagebrowser


class MyNumberValidator(wx.Validator):# 创建验证器子类
    def __init__(self):
        wx.Validator.__init__(self)
        self.ValidInput = ['.','0','1','2','3','4','5','6','7','8','9']
        self.StringLength = 0
        self.Bind(wx.EVT_CHAR,self.OnCharChanged)  #  绑定字符改变事件

    def OnCharChanged(self,event):
        # 得到输入字符的 ASCII 码
        keycode = event.GetKeyCode()
        # 退格（ASCII 码 为8），删除一个字符。
        if keycode == 8:
            self.StringLength -= 1
            #事件继续传递
            event.Skip()
            return


        InputChar = chr(keycode)

        if InputChar in self.ValidInput:
            # 第一个字符为 .,非法，拦截该事件，不会成功输入
            if InputChar == '.' and self.StringLength == 0:
                return False
            # 在允许输入的范围，继续传递该事件。
            else:
                event.Skip()
                self.StringLength += 1
                return True
        return False

    def Clone(self):
        return MyNumberValidator()

    def Validate(self,win):#1 使用验证器方法
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True


