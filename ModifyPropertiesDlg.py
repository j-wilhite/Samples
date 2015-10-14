import wx
import os
import sys
import winutils
#from Utils import setFileProperty

class ModifyPropertyDialog(wx.Dialog):
    def __init__(self, parent, cadFile, propertyName, propertyValue, checkoutDir, dlgTitle='', iconStyle=wx.ICON_WARNING):

        wx.Dialog.__init__(self, parent, title=dlgTitle, style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX)
        
        self.checkoutDir = checkoutDir
        self.cadFile = cadFile
        self.property = propertyName
        self.value = propertyValue

        self.labelMsg = wx.StaticText(self, -1, "CAD file", style=wx.ALIGN_CENTER)
        self.cadFileName = wx.StaticText(self, -1, self.cadFile, style=wx.ALIGN_CENTER)
        self.propertyTxt = wx.StaticText(self, -1, "Property", style=wx.ALIGN_CENTER)
        self.propertyTxtCtrl = wx.TextCtrl(self, -1, self.property, size = (150, 20))
        self.valueTxt = wx.StaticText(self, -1, "Value", style=wx.ALIGN_CENTER)
        self.valueTxtCtrl = wx.TextCtrl(self, -1, self.value, size = (150, 20))
        self.modifyBtn = wx.Button(self, wx.ID_ANY, "Add/Modify Property")
        self.okBtn = wx.Button(self, wx.ID_OK, "OK")

        self.__set_properties() 
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onModify, self.modifyBtn)

    def __set_properties(self):

        self.SetMinSize((400, 250))
        self.SetSize((400, 250))

    def __do_layout(self):

        # create main sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        propertySizer = wx.BoxSizer(wx.HORIZONTAL)
        valueSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        nameSizer.Add(self.labelMsg, 1, wx.ALL|wx.ALIGN_LEFT, 5)
        nameSizer.Add(self.cadFileName, 1, wx.ALL|wx.ALIGN_RIGHT, 5)
        propertySizer.Add(self.propertyTxt, 1, wx.ALL|wx.ALIGN_LEFT, 5)
        propertySizer.Add(self.propertyTxtCtrl, 1, wx.ALL|wx.ALIGN_RIGHT, 5)
        valueSizer.Add(self.valueTxt, 1, wx.ALL|wx.ALIGN_LEFT, 5)
        valueSizer.Add(self.valueTxtCtrl, 1, wx.ALL|wx.ALIGN_RIGHT, 5)
        buttonSizer.Add(self.modifyBtn, 1, wx.ALL, 5)
        buttonSizer.Add(self.okBtn, 1, wx.ALL, 5)

        mainSizer.Add(nameSizer, 1, wx.ALL|wx.ALIGN_LEFT, 25)
        mainSizer.Add(propertySizer, 1, wx.ALL|wx.ALIGN_LEFT, 5)
        mainSizer.Add(valueSizer, 1, wx.ALL|wx.ALIGN_LEFT, 5)
        mainSizer.Add(buttonSizer, 1, wx.ALL|wx.ALIGN_RIGHT, 5)

        self.SetSizer(mainSizer)
        self.Layout()

    def setFileProperty(self, filename, propName, propValue):
        if os.path.exists(filename):
            try:
                winutils.WriteProperty(filename, propName, propValue)
            except:
                pass

    def onModify(self, event):

        newProp = self.propertyTxtCtrl.GetValue()
        newValue = self.valueTxtCtrl.GetValue()
        filename = os.path.join(self.checkoutDir, self.cadFile)
        self.setFileProperty(filename, newProp, newValue)

        

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    ScrolledMessageDialog = ScrolledMessageDialog(None, -1, "")
    app.SetTopWindow(ScrolledMessageDialog)
    ScrolledMessageDialog.Show()
    app.MainLoop()
