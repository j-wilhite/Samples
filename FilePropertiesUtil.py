import wx
import os
import sys
import re
import winutils
from collections import defaultdict
#from Utils import getFileProperty, getAllFileProperties
from ModifyPropertiesDlg import ModifyPropertyDialog
import getopt
from ScrolledMessageDialog import ScrolledMessageDialog

class FilePropertiesTestDialog(wx.Dialog):
    def __init__(self, parent, workDir, isEnovia, isProe, dlgTitle='', iconStyle=wx.ICON_WARNING):

        wx.Dialog.__init__(self, parent, title=dlgTitle, style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX)
        
        self.intVer = ''
        self.plmVer = ''
        self.cadFilePropertiesDict = defaultdict(list)
        self.workDir = workDir
        self.isEnovia = isEnovia
        self.isProe = isProe
        self.workDirBtn = wx.Button(self, wx.ID_ANY, "Select Working Directory")
        self.workingDirectory = wx.TextCtrl(self, -1, "", size = (300, 25), style = wx.TE_PROCESS_ENTER)
        self.workingDirectory.SetValue(self.workDir)


        self.proeRadioBtn = wx.RadioButton(self, -1, 'Pro/E', style=wx.RB_GROUP)
        #self.proeRadioBtn.Unbind(wx.EVT_KEY_DOWN)
        self.NXradioBtn = wx.RadioButton(self, -1, 'NX')
        #self.NXradioBtn.Unbind(wx.EVT_KEY_DOWN)
        self.arasRadioBtn = wx.RadioButton(self, -1, 'Aras', style=wx.RB_GROUP)
        #self.arasRadioBtn.Unbind(wx.EVT_KEY_DOWN)
        self.enoviaRadioBtn = wx.RadioButton(self, -1, 'Enovia')
        #self.enoviaRadioBtn.Unbind(wx.EVT_KEY_DOWN)
        self.allVersionCheckbox = wx.CheckBox(self, -1, 'Show All Pro/E Versions')
        self.allVersionCheckbox.SetValue(False)

        if self.isEnovia:
            self.enoviaRadioBtn.SetValue(True)
        else:
            self.arasRadioBtn.SetValue(True)                

        if self.isProe:
            self.proeRadioBtn.SetValue(True)
        else:
            self.NXradioBtn.SetValue(True)                
 
        self.readAllPropertiesBtn = wx.Button(self, wx.ID_ANY, "Read All File Properties")

        #self.displayPropertiesListCtrl = EditableListCtrl(self, wx.ID_ANY, size=(700, 400), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.displayPropertiesListCtrl = wx.ListCtrl(self, size=(700, 400), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.displayPropertiesListCtrl.InsertColumn(0, 'CAD File')
        self.displayPropertiesListCtrl.InsertColumn(1, 'Property')
        self.displayPropertiesListCtrl.InsertColumn(2, 'Value')
        self.displayPropertiesListCtrl.SetColumnWidth(0, 200)
        self.displayPropertiesListCtrl.SetColumnWidth(1, 200)
        self.displayPropertiesListCtrl.SetColumnWidth(2, 200)


        self.closeBtn = wx.Button(self, wx.ID_CANCEL, "Close") 

        self.__set_properties() 
        self.__do_layout()

        self.workingDirectory.Bind(wx.EVT_TEXT_ENTER, self.onTextEnter)
        self.Bind(wx.EVT_BUTTON, self.onSelectWorkDir, self.workDirBtn)
        self.Bind(wx.EVT_BUTTON, self.onReadAllFileProperties, self.readAllPropertiesBtn)
        self.Bind(wx.EVT_RADIOBUTTON, self.updateDisplay, id=self.proeRadioBtn.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.updateDisplay, id=self.NXradioBtn.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.updateDisplay, id=self.arasRadioBtn.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.updateDisplay, id=self.enoviaRadioBtn.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.updateDisplay, id=self.allVersionCheckbox.GetId())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onSelectItem, self.displayPropertiesListCtrl)


        self.onReadAllFileProperties(None)
        
    def onTextEnter(self, event):
        pass

    def __set_properties(self):

        self.SetMinSize((850, 650))
        self.SetSize((850, 650))

    def __do_layout(self):

        # create main sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Creates panel and sizers for the file properties options
        # Includes aras/enovia, proe/nx, which file property 
        radioBtnBoxSizer = wx.BoxSizer(wx.VERTICAL)
        arasEnoviaButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        proeNXButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

         # Adds the items to the sizers for File Properties Options panel 
        arasEnoviaButtonSizer.Add(self.arasRadioBtn, 1, wx.ALL, 1)
        arasEnoviaButtonSizer.Add(self.enoviaRadioBtn, 1, wx.ALL, 1)
        proeNXButtonSizer.Add(self.proeRadioBtn, 1, wx.ALL, 1)
        proeNXButtonSizer.Add(self.NXradioBtn, 1, wx.ALL, 2)

        # Adds the sizers to the File Properties options panel
        radioBtnBoxSizer.Add(arasEnoviaButtonSizer, 0, wx.ALL|wx.ALIGN_LEFT, 10)
        radioBtnBoxSizer.Add(proeNXButtonSizer, 0, wx.ALL|wx.ALIGN_LEFT, 10)
        radioBtnBoxSizer.Add(self.allVersionCheckbox, 0, wx.ALL|wx.ALIGN_LEFT, 10)

        # Sizer for selecting working directory
        workingDirSizer = wx.BoxSizer(wx.HORIZONTAL)
        workingDirSizer.Add(self.workDirBtn, 1, wx.ALL, 5)
        workingDirSizer.Add(self.workingDirectory, 1, wx.ALL, 5)

        # Sizer for reading all file properties button
        filePropertiesButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        filePropertiesButtonSizer.Add(self.readAllPropertiesBtn, 1, wx.ALL, 1)

        # Sizer to hold working directory buttons and read properties button
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer.Add(workingDirSizer, 1, wx.ALL|wx.ALIGN_LEFT, 5)
        buttonSizer.Add(filePropertiesButtonSizer, 1, wx.ALL, 5)

        # ObjectListView sizer
        listCtrlSizer = wx.BoxSizer(wx.HORIZONTAL)
        listCtrlSizer.Add(self.displayPropertiesListCtrl, wx.ALL, 5)

        # Close btn sizer
        closeSizer = wx.BoxSizer(wx.HORIZONTAL)
        closeSizer.Add(self.closeBtn, 1, wx.ALL, 5)

        topSizer.Add(radioBtnBoxSizer, 0, wx.ALL|wx.ALIGN_LEFT, 5)
        topSizer.Add(buttonSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        mainSizer.Add(topSizer, 0, wx.ALL, 10)
        mainSizer.Add(listCtrlSizer, 0, wx.ALL|wx.EXPAND, 1)
        mainSizer.Add(closeSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        self.SetSizer(mainSizer)
        self.Layout()
        self.Centre()

#==============================================================================================#
    def setPLMVer(self):
        '''
        Sets the version to Aras or Enovia based on radio button selection
        '''
        if self.arasRadioBtn.GetValue() == 1:
            self.plmVer = "Aras"
        else:
            self.plmVer = "Enovia"
        return self.plmVer
#==============================================================================================#
    def setIntVer(self):
        '''
        Sets the version to PROE or NX based on radio button selection
        '''
        if self.proeRadioBtn.GetValue() == 1:
            self.intVer = "PROE"
            self.allVersionCheckbox.Enable(True)
        else:
            self.intVer = "NX"
            self.allVersionCheckbox.Enable(False)
        return self.intVer
#==============================================================================================#
    def updateDisplay(self, event):
        '''
        Updates the display based on the plm version and cad version selected
        '''
        # keycode = event.KeyCode()
        # keycode = event.GetKeyCode()
        # if keycode != WXK_RETURN:
        #     plmVer = self.setPLMVer()
        #     intVer = self.setIntVer()
        #     updatedFilePropertiesList = self.sortFiles(plmVer, intVer)
        #     versionUpdatedFilePropertiesList = self.getProVersions(updatedFilePropertiesList)
        #     self.displayFileProperties(versionUpdatedFilePropertiesList)
        # keycode = event.EventType
        # if keycode == wx.EVT_KEY_DOWN.typeId or keycode == wx.EVT_TEXT_ENTER.typeId:
        plmVer = self.setPLMVer()
        intVer = self.setIntVer()
        updatedFilePropertiesList = self.sortFiles(plmVer, intVer)
        versionUpdatedFilePropertiesList = self.getProVersions(updatedFilePropertiesList)
        self.displayFileProperties(versionUpdatedFilePropertiesList)
#==============================================================================================#
    def getProVersions(self, updatedFilePropertiesDict):
        '''
        Sorts to get either all the ProE versions of the files or the latest versions
        '''
        updatedVersionDict = defaultdict(list)
        # If all versions is checked, returns all versions
        allVersions = self.allVersionCheckbox.GetValue()
        if allVersions == 1:
            return updatedFilePropertiesDict
        elif not allVersions == 1 and self.setIntVer() == "NX":
            return updatedFilePropertiesDict
        # If all versions is not checked, returns latest versions
        else:
            for cadFile in updatedFilePropertiesDict:
                latest = self.getLatestVer(cadFile, updatedFilePropertiesDict)
                if latest not in updatedVersionDict:  
                    for index in range(len(updatedFilePropertiesDict[latest])):
                        updatedVersionDict[latest].append((self.cadFilePropertiesDict[latest][index][0], self.cadFilePropertiesDict[latest][index][1]))
            return updatedVersionDict
#==============================================================================================#
    def getLatestVer(self, cadFile, updatedFilePropertiesDict):
        '''
        Gets the latest version of a ProE file
        '''

        versionList = []
        for item in updatedFilePropertiesDict:
            # If the versionless filename exists more than once in the dict, append file to list
            cadFileSplitList = cadFile.split(".")
            itemSplitList = item.split(".")
            if cadFileSplitList[0].lower() == itemSplitList[0].lower():
                versionList.append(item)
        # Get latest version
        sortedList = sorted(versionList)
        latestVer = max(sortedList)
        return latestVer

#==============================================================================================#
    def sortFiles(self, plmVer, intVer):
        '''
        Sorts files based on the radio button selections.
        Returns specified dictionaries based on sorting.
        Looks messy, but haven't come up with a better way to sort.
        '''
        self.ARPROFilePropertiesDict = defaultdict(list)
        self.ARNXFilePropertiesDict = defaultdict(list)
        self.ENPROFilePropertiesDict = defaultdict(list)
        self.ENNXFilePropertiesDict = defaultdict(list)

        for cadFile in self.cadFilePropertiesDict:
            fileExtMatchGeneric = re.search('(\.prt$)|(\.asm$)|(\.drw$)|(\.frm$)|(\.dgm$)|(\.lay$)|(\.mfg$)|(\.xpr$)', cadFile, re.I)
            fileExtMatchInstance = re.search( '(prt\..$)|(asm\..$)|(drw\..$)|(frm\..$)|(dgm\..$)|(lay\..$)|(mfg\..$)|(\.xpr\..$)', cadFile, re.I)
            for index in range(len(self.cadFilePropertiesDict[cadFile])):
                if self.isArasProperty(plmVer, self.cadFilePropertiesDict[cadFile]):
                    if self.isArasProeProperty(intVer, index, self.cadFilePropertiesDict[cadFile]):
                        self.ARPROFilePropertiesDict[cadFile].append((self.cadFilePropertiesDict[cadFile][index][0], self.cadFilePropertiesDict[cadFile][index][1]))
                    elif self.isArasNXProperty(intVer, index, self.cadFilePropertiesDict[cadFile]):
                        self.ARNXFilePropertiesDict[cadFile].append((self.cadFilePropertiesDict[cadFile][index][0], self.cadFilePropertiesDict[cadFile][index][1]))
                elif self.isEnoviaProperty(plmVer, self.cadFilePropertiesDict[cadFile]):
                    if self.isEnoviaProeProperty(intVer, self.cadFilePropertiesDict[cadFile][index][0]):
                        self.ENPROFilePropertiesDict[cadFile].append((self.cadFilePropertiesDict[cadFile][index][0], self.cadFilePropertiesDict[cadFile][index][1]))
                    elif self.isEnoviaNXProperty(intVer, self.cadFilePropertiesDict[cadFile][index][0]):
                        self.ENNXFilePropertiesDict[cadFile].append((self.cadFilePropertiesDict[cadFile][index][0], self.cadFilePropertiesDict[cadFile][index][1]))
                elif intVer == "PROE" and (fileExtMatchInstance or fileExtMatchGeneric) and self.cadFilePropertiesDict[cadFile][index][0] == "NO FILE PROPERTY":
                    self.ARPROFilePropertiesDict[cadFile].append((self.cadFilePropertiesDict[cadFile][index][0], self.cadFilePropertiesDict[cadFile][index][1]))
                    self.ENPROFilePropertiesDict[cadFile].append((self.cadFilePropertiesDict[cadFile][index][0], self.cadFilePropertiesDict[cadFile][index][1]))
                elif intVer == "NX" and fileExtMatchGeneric and self.cadFilePropertiesDict[cadFile][index][0] == "NO FILE PROPERTY":
                    self.ARNXFilePropertiesDict[cadFile].append((self.cadFilePropertiesDict[cadFile][index][0], self.cadFilePropertiesDict[cadFile][index][1]))
                    self.ENNXFilePropertiesDict[cadFile].append((self.cadFilePropertiesDict[cadFile][index][0], self.cadFilePropertiesDict[cadFile][index][1]))
               
        if plmVer == "Aras" and intVer == "PROE":
            return self.ARPROFilePropertiesDict
        elif plmVer == "Aras" and intVer == "NX":
            return self.ARNXFilePropertiesDict
        elif plmVer == "Enovia" and intVer == "PROE":
            return self.ENPROFilePropertiesDict
        elif plmVer == "Enovia" and intVer == "NX":
            return self.ENNXFilePropertiesDict

    #==============================================================================================#
    def isArasProperty(self, plmVer, properties):
        isArasProperty = False
        if plmVer == "Aras":
            if self.isNameStartWithInProperties("AR", properties):
               isArasProperty = True
        return isArasProperty  

    #==============================================================================================#
    def isEnoviaProperty(self, plmVer, properties):
        isEnoviaProperty = False
        if plmVer == "Enovia":
            if self.isNameStartWithInProperties("MX", properties):
               isEnoviaProperty = True
        return isEnoviaProperty  
                
    #==============================================================================================#
    def isArasNXProperty(self, intVer, index, properties):
        isArasNXProperty = False
        if intVer == "NX":
            if "UG" in properties[index][0]:
                isArasNXProperty = True
#             elif "CON" in properties[index][0] and self.isNameInProperties("UG", properties):
            elif self.isNameInProperties("UG", properties):
                isArasNXProperty = True
        return isArasNXProperty
    
   
    #==============================================================================================#
    def isArasProeProperty(self, intVer, index, properties):
        isArasProeProperty = False
        if intVer == "PROE":
            if "PRO" in properties[index][0]:
                isArasProeProperty = True
#             elif "CON" in properties[index][0] and self.isNameInProperties("PRO", properties):
            elif self.isNameInProperties("PRO", properties):
                isArasProeProperty = True
        return isArasProeProperty

    #==============================================================================================#
    def isNameInProperties(self, name, properties):
        isNameInProperties = False
        for prop in properties:
            if name in prop[0]:
                isNameInProperties = True
                break
        return isNameInProperties
                    
    #==============================================================================================#
    def isNameStartWithInProperties(self, name, properties):
        isNameInProperties = False
        for prop in properties:
            if prop[0].startswith(name):
                isNameInProperties = True
                break
        return isNameInProperties
                    

    #==============================================================================================#
    def isEnoviaNXProperty(self, intVer, property):
        isEnoviaNXProperty = False
        if intVer == "NX":
            if "UG" in property:
                isEnoviaNXProperty = True
        return isEnoviaNXProperty

    #==============================================================================================#
    def isEnoviaProeProperty(self, intVer, property):
        isEnoviaProeProperty = False
        if intVer == "PROE":
            if "PRO" in property:
                isEnoviaProeProperty = True
        return isEnoviaProeProperty
                    
#==============================================================================================#
    def returnInvalidProperties(self, invalidProperties):
        if invalidProperties:
            invalidPropertiesList = ''
            for item in invalidProperties:
                invalidPropertiesList = invalidPropertiesList + str(item[0] + "    " + item[1] + "\n")
            invalidPropertiesMsg = "These file properties are invalid."
            warningDlg = ScrolledMessageDialog(None, 'Invalid Properties', invalidPropertiesMsg, wx.OK | wx.ICON_WARNING | wx.STAY_ON_TOP)
            warningDlg.report_txt.AppendText(invalidPropertiesList)
            ret = warningDlg.ShowModal()
            if ret == wx.ID_OK:
                warningDlg.Destroy()
            else:
                warningDlg.Destroy()

#==============================================================================================#
    def onSelectWorkDir(self, event):
        '''
        Brings up a file selection dialog to choose the working/checkout directory
        '''
        selectWorkDirDlg = wx.DirDialog(self, "Select Working Directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if selectWorkDirDlg.ShowModal() == wx.ID_CANCEL:
            return
        self.workingDirectory.SetValue('')
        self.workingDirectory.AppendText(selectWorkDirDlg.GetPath())
#==============================================================================================#
    def getWorkingDir(self):
        '''
        Gets the value selected for the working directory/checkout directory
        '''
        return str(self.workingDirectory.GetValue())
#==============================================================================================#        
    def getAllFileProperties(self, filename):
        '''
        Duplicated method from the Utils file
        Gets all file properties for a file
        '''
        propValue = []
        if os.path.exists(filename):
            try:
                propValue = winutils.GetPropertiesList(filename)
            except:
                pass

        return propValue
#==============================================================================================#
    def getFileProperty(self, filename, propName):
        '''
        Duplicated method from the Utils file
        Gets a specified file property for a file
        '''
        propValue = None
        if os.path.exists(filename):
            try:
                propValue = winutils.ReadProperty(filename, propName)
            except:
                pass

        return propValue
#==============================================================================================#
    def retrieveFileProperties(self):
        '''
        Gets a list of all cad files in the specified directory
        Gets all the file properties of each cad file
        Puts the cad files and their properties into a dictionary of lists 
        '''
        self.cadFilePropertiesDict = defaultdict(list)
        checkoutDir = self.getWorkingDir()
        invalidPropertiesList = []
        for cadFile in os.listdir(checkoutDir):
            filename = os.path.join(checkoutDir, cadFile)
            fileExtMatchInstance = re.search( '(\.prt\..$)|(\.asm\..$)|(\.drw\..$)|(\.frm\..$)|(\.dgm\..$)|(\.lay\..$)|(\.mfg\..$)|(\.xpr\..$)', cadFile, re.I)
            fileExtMatchGeneric = re.search('(\.prt$)|(\.asm$)|(\.drw$)|(\.frm$)|(\.dgm$)|(\.lay$)|(\.mfg$)|(\.xpr$)', cadFile, re.I)
            if fileExtMatchGeneric or fileExtMatchInstance :
                fileTNR = self.getAllFileProperties(filename)
                if fileTNR:   
                    for fileProperty in fileTNR:
                        filePropertyList = fileProperty.split('|', 1)
                        filePropertyName = str(filePropertyList[0])
                        filePropertyValue = str(filePropertyList[1])  
#                         if not filePropertyName.startswith("AR") and not filePropertyName.startswith("MX"):
#                             invalidPropertiesList.append((str(cadFile), filePropertyName))
#                         else:
#                             self.cadFilePropertiesDict[cadFile].append((filePropertyName, filePropertyValue))
                        self.cadFilePropertiesDict[cadFile].append((filePropertyName, filePropertyValue))
                else:
                    self.cadFilePropertiesDict[cadFile].append(("NO FILE PROPERTY", " "))
        self.returnInvalidProperties(invalidPropertiesList)
        return self.cadFilePropertiesDict
#==============================================================================================#
    def onReadAllFileProperties(self, event):
        '''
        Processes the action of getting all the file properties and displaying them 
        '''
        filePropertiesDict = self.retrieveFileProperties()
        self.displayFileProperties(filePropertiesDict)
#==============================================================================================#        
    def onSelectItem(self, event):
        '''
        Event for when an item in the list is double-clicked
        Allows modification of file property on that cadfile 
        '''
        checkoutDir = self.getWorkingDir()
        # ListCtrl's stupid way of getting the text of a selected item in its respective columns
        selectedItem = self.displayPropertiesListCtrl.GetFirstSelected()
        col1 = self.displayPropertiesListCtrl.GetItem(selectedItem, 0)
        col2 = self.displayPropertiesListCtrl.GetItem(selectedItem, 1)
        col3 = self.displayPropertiesListCtrl.GetItem(selectedItem, 2)
        # Gets the cadFile name, property name, property value of selected item
        cadFile = col1.GetText()
        propName = col2.GetText()
        propValue = col3.GetText()
        # If the row selected does not have an adjacent cad file name, get the cad file that matches
        # the property value from the cad file properties dict
        if str(cadFile) == ' ':
            for name, prop in self.cadFilePropertiesDict.iteritems():
                for index in range(len(prop)):
                    if prop[index][1] == str(propValue):
                        cadFile = name
        # Opens the dialog to modify file properties
        modifyDlg = ModifyPropertyDialog(None, cadFile, propName, propValue, checkoutDir, "Modify Properties", wx.OK)
        ret = modifyDlg.ShowModal()
        if ret == wx.ID_OK:
            modifyDlg.Destroy()
            # Update the display when selecting ok in the modify dialog
            filePropertiesDict = self.retrieveFileProperties()
            self.displayFileProperties(filePropertiesDict)
#==============================================================================================#
    def displayFileProperties(self, cadFilePropertiesDict):
        '''
        Handles creating the display in the listCtrl 
        '''        
        self.displayPropertiesListCtrl.DeleteAllItems()
        plmVer = self.setPLMVer()
        intVer = self.setIntVer()
        updatedFilePropertiesDict = self.sortFiles(plmVer, intVer)
        versionUpdatedFilePropertiesDict = self.getProVersions(updatedFilePropertiesDict)
        propertiesList = self.alphabetizeDict(versionUpdatedFilePropertiesDict)
        
        for cadFileIndex in range(len(propertiesList)):
            for propertyIndex in range(len(propertiesList[cadFileIndex][1])):
                #If the cad file has more than one file property, don't display cad file name twice
                # Group its multiple file properties underneath
                cadFileExists = self.displayPropertiesListCtrl.FindItem(-1, propertiesList[cadFileIndex][0])
                if not cadFileExists == -1:
                    newRow = self.displayPropertiesListCtrl.InsertStringItem(self.displayPropertiesListCtrl.GetItemCount(), " ")
                else:
                    newRow = self.displayPropertiesListCtrl.InsertStringItem(self.displayPropertiesListCtrl.GetItemCount(), propertiesList[cadFileIndex][0])
                propertyName = propertiesList[cadFileIndex][1][propertyIndex][0]
                propertyValue = propertiesList[cadFileIndex][1][propertyIndex][1]
                self.displayPropertiesListCtrl.SetStringItem(newRow, 1, propertyName)
                self.displayPropertiesListCtrl.SetStringItem(newRow, 2, propertyValue)
#==============================================================================================#    
    def alphabetizeDict(self, versionUpdatedFilePropertiesDict):
        propertiesList = []
        for cadFile in versionUpdatedFilePropertiesDict:
            propertiesList.append((cadFile.lower(), versionUpdatedFilePropertiesDict[cadFile]))
        propertiesList.sort()
        return propertiesList 
#==============================================================================================#
def main(argv):
    workDir = ''
    isEnovia = True
    isProe = False
    try: 
        options, args = getopt.getopt(argv, "hd:ap", ["--directory="])
    except getopt.GetoptError:
        print 'FilePropertiesUtil.py -d <working directory>'
        sys.exit(2)
    for option, arg in options:
        if option == '-h':
            print 'FilePropertiesUtil.py -d <working directory> -a -p'
            sys.exit()
        elif option in ("-d", "--directory"):
            workDir = arg
        elif option in ("-a", "--aras"):
            isEnovia = False
        elif option in ("-p", "--proe"):
            isProe = True
    return workDir, isEnovia, isProe
    

if __name__ == "__main__":
    (workDir, isEnovia, isProe) = main(sys.argv[1:])
    app = wx.PySimpleApp(0)
    FilePropertiesTestDialog = FilePropertiesTestDialog(None, workDir, isEnovia, isProe, "Read File Properties")
    app.SetTopWindow(FilePropertiesTestDialog)
    FilePropertiesTestDialog.Show()
    app.MainLoop()