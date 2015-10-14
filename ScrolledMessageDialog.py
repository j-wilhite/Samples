import wx
import os
#import UIResource

class ScrolledMessageDialog(wx.Dialog):
    def __init__(self, parent, dlgTitle='', staticTxtMsg='', iconStyle=wx.ICON_WARNING):

        wx.Dialog.__init__(self, parent, title=dlgTitle,style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.STAY_ON_TOP)
        
        self.staticMsgSTxt = wx.StaticText(self, -1, staticTxtMsg, style=wx.ALIGN_CENTER)
        self.staticMsgSTxt.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.report_txt = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        #self.okBtn = wx.Button(self, wx.ID_OK, UIResource.get("RESOURCE","BUTTON_OK")) 
        #self.cancelBtn = wx.Button(self, wx.ID_CANCEL, UIResource.get("RESOURCE","BUTTON_CANCEL")) 
        self.okBtn = wx.Button(self, wx.ID_OK, "OK") 
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, "Cancel") 


        self.__set_properties() 
        self.__do_layout()

    def __set_properties(self):

        self.SetMinSize((500, 300))
        self.SetSize((500, 300))
        self.SetFocus()
        self.okBtn.SetFocus()
        # end wxGlade

    def __do_layout(self):

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        messageSizer = wx.BoxSizer(wx.HORIZONTAL)
        txtCtrlSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        messageSizer.Add(self.staticMsgSTxt, 1, wx.ALL|wx.EXPAND, 5)
        txtCtrlSizer.Add(self.report_txt, 1, wx.RIGHT|wx.LEFT|wx.EXPAND|wx.ALIGN_CENTER, 5)
        buttonSizer.Add(self.okBtn, 1, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 10)
        buttonSizer.Add(self.cancelBtn, 1, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 10)
        mainSizer.Add(messageSizer, 0, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(txtCtrlSizer, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(buttonSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        self.SetSizer(mainSizer)
        self.Layout()
        self.Centre()


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    ScrolledMessageDialog = ScrolledMessageDialog(None, -1, "")
    app.SetTopWindow(ScrolledMessageDialog)
    ScrolledMessageDialog.Show()
    app.MainLoop()