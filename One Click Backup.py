import wx
import shutil
import os
import time
import datetime
import sqlite3

#PYTHON 2.7
sourceFolder = "C:\\Users\\Mike\\Desktop\\A"
destFolder = "C:\\Users\\Mike\\Desktop\\B"

class windowClass(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, **kwargs)
        self.basicGUI()

    def basicGUI(self):
        panel = wx.Panel(self)
        self.myLastFileXferTextBox = wx.StaticText(panel, -1, "Last File Transfer Was Done: " , pos=(10,430))
        self.updateLastXferTextBox(self)
        menuBar = wx.MenuBar()
        fileButton = wx.Menu()
        #settingsItem = wx.Menu()
        #settingsItem = wx.MenuItem(fileButton, wx.ID_ANY, "Settings")
        exitItem = wx.MenuItem(fileButton, wx.ID_EXIT, "Quit\tCtrl+Q")
        exitItem.SetBitmap(wx.Bitmap('Quit.bmp'))
        #fileButton.AppendItem(settingsItem)
        fileButton.AppendItem(exitItem)
        menuBar.Append(fileButton, "&File")
        self.SetMenuBar(menuBar)
        self.truncatingExtBox = False
        wx.StaticText(panel, -1, "Please select what type of file transfer: ", pos=(10, 130))
        self.myRadioButton1 = wx.RadioButton(panel, label="Move", pos=(360,125), size=(80,25), style=wx.RB_GROUP)
        self.myRadioButton2 = wx.RadioButton(panel, label="Copy", pos=(260,125), size=(80,25))
        wx.StaticText(panel, -1, "Limit backup to file extension: ", pos=(10, 165))
        self.fileExtension = wx.TextCtrl(panel, -1, "", pos=(180, 160), size=(70, 25))
        self.updateFileExtensionTextBox(self)
        wx.StaticText(panel, -1, "Create/Modify During The Day Folder (From Folder):", pos=(10,10))
        self.sourceFolderText = wx.TextCtrl(panel, -1, sourceFolder, pos=(10,30), size=(350,25))
        self.sourceFolderText.SetBackgroundColour("white")
        wx.StaticText(panel, -1, "Temporary Folder For Holding Before Moving (To Folder):", pos=(10,70))
        self.destFolderText = wx.TextCtrl(panel, -1, destFolder, pos=(10,90), size=(350,25))
        self.destFolderText.SetBackgroundColour("white")
        self.myStatusBar = self.CreateStatusBar()
        self.prevFileXfer = self.updateLastXferTextBox
        self.sourcePathChange = wx.Button(panel, label="Change", pos=(360,30), size=(80,25))
        self.destPathChange = wx.Button(panel, label="Change", pos=(360,90), size=(80,25))
        self.fileCheckButton = wx.Button(panel, label="Check for " + self.fileExtension.Value + " files created/modified after the last file transfer.", pos=(10,190), size=(430,25))
        self.fileListBox = wx.ListBox(panel, pos=(10,215), size=(430, 200), style = 1)
        self.initiateXferButton = wx.Button(panel, label="Transfer " + self.fileExtension.Value + " files created/modified\nafter the last file transfer.", pos=(10, 465), size=(430,50))
        self.fileExtensionTextBoxChanged(self)
        self.Bind(wx.EVT_TOOL, self.quitProgram, exitItem)
        self.Bind(wx.EVT_TEXT, self.fileExtensionTextBoxChanged, self.fileExtension)
        self.Bind(wx.EVT_BUTTON, self.sourcePathChangeButton, self.sourcePathChange)
        self.Bind(wx.EVT_TEXT, self.sourcePathChangeText, self.sourceFolderText)
        self.Bind(wx.EVT_BUTTON, self.destPathChangeButton, self.destPathChange)
        self.Bind(wx.EVT_TEXT, self.destPathChangeText, self.destFolderText)
        self.Bind(wx.EVT_BUTTON, self.xferFilesButton, self.initiateXferButton)
        self.Bind(wx.EVT_BUTTON, self.getFileList, self.fileCheckButton)
        self.Bind(wx.EVT_BUTTON, self.radioButtonClick, self.myRadioButton1)
        self.Bind(wx.EVT_BUTTON, self.radioButtonClick, self.myRadioButton2)
        self.myStatusBar.SetStatusWidths([-2])
        self.SetTitle("File Transfer Tool")
        self.SetBackgroundColour("#DFDFDF")
        self.Show(True)
        
    def quitProgram(self, e):
        self.Close()

    def sourcePathChangeText(self, e):
        global sourceFolder
        sourceFolder = self.sourceFolderText.Value
        
    def destPathChangeText(self, e):
        global destFolder
        destFolder = self.destFolderText.Value

    def sourcePathChangeButton(self, e):
        openDirDialog = wx.DirDialog(self)
        if openDirDialog.ShowModal() != wx.ID_CANCEL:
            input_stream = openDirDialog.GetPath()
            self.sourceFolderText.Value = input_stream

    def destPathChangeButton(self, e):
        openDirDialog = wx.DirDialog(self)
        if openDirDialog.ShowModal() != wx.ID_CANCEL:
            input_stream = openDirDialog.GetPath()
            self.destFolderText.Value = input_stream

    def radioButtonClick(self, e):
        pass

    def fileExtensionTextBoxChanged(self, e):
        if self.fileExtension.Value == "":
            self.fileCheckButton.SetLabel("Check for any files created/modified after the last file transfer.")
            self.initiateXferButton.SetLabel("Transfer any files created/modified\nafter the last file transfer.")
        else:
            self.fileCheckButton.SetLabel("Check for " + self.fileExtension.Value + " files created/modified after the last file transfer.")
            self.initiateXferButton.SetLabel("Transfer " + self.fileExtension.Value + " files created/modified\nafter the last file transfer.")
        if self.truncatingExtBox == False:
            if len(self.fileExtension.Value)>15:
                self.myStatusBar.SetBackgroundColour('#FF0000')
                self.truncatingExtBox = True
                self.myStatusBar.SetStatusText("Sorry I can't handle file extensions this long.")
                self.fileExtension.Value = self.fileExtension.Value[0:len(self.fileExtension.Value)-1] #TRUNCATE THE LAST CHAR
                self.truncatingExtBox = False
            else:
                self.myStatusBar.SetBackgroundColour('#FFFFFF')
                self.myStatusBar.SetStatusText("")



    def updateFileExtensionTextBox(self, e):
        fileExt = getPrevChosenFileExtension()
        if fileExt == None:
            fileExt = ""
        self.fileExtension.Value = fileExt

    def updateLastXferTextBox(self, e):
        prevFileXfer = getLastFileXferDateTime()
        if prevFileXfer == None or prevFileXfer == "" :
            prevFileXfer = "Never"
        else:
            prevFileXfer = (str(datetime.datetime.strftime(prevFileXfer, "%m-%d-%Y %H:%M:%S.%f")))
        self.myLastFileXferTextBox.SetLabelText("Last File Transfer Was Done: " + prevFileXfer)
    
    def getFileList(self, e):
        self.updateLastXferTextBox(self)
        try:
            timeStarted = datetime.datetime.now() #GRABBING THIS IMMEDIATELY SO IF SOMEONE CREATES A FILE AT THE SAME TIME AS THIS PROGRAM IS CHECKING WHAT TO BACKUP, THEN THOSE FILES WILL HAVE A CREATE DATETIME AFTER THIS BACKUP DATETIME
            prevFileXfer = getLastFileXferDateTime()
            if prevFileXfer == None:
                prevFileXfer = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)
            fileNames = os.listdir(sourceFolder)
            fileList = []
            fmt = '%Y-%m-%d %H:%M:%S'
            self.fileListBox.Clear()
            if self.fileExtension.Value != "":
                for eachName in fileNames:
                    if len(eachName) >= len(self.fileExtension.Value):
                        if str(eachName[len(eachName)-len(self.fileExtension.Value):len(eachName)]).lower() == str(self.fileExtension.Value).lower() and (prevFileXfer < datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(sourceFolder, eachName)))):
                            self.myStatusBar.SetBackgroundColour('#00FF00')
                            self.myStatusBar.SetStatusText( "")
                            fileList.append(eachName)
                            self.fileListBox.Append(eachName)
            else:
                for eachName in fileNames:
                    if (prevFileXfer < datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(sourceFolder, eachName)))):
                        self.myStatusBar.SetBackgroundColour('#FFFFFF')
                        self.myStatusBar.SetStatusText( "")
                        fileList.append(eachName)
                        self.fileListBox.Append(eachName)
                
            if fileList == []:
                self.myStatusBar.SetBackgroundColour('#FF0000')
                if self.fileExtension.Value == "":
                    self.myStatusBar.SetStatusText( "I didn't find any files that were created/modified after the last file transfer.")
                else:
                    self.myStatusBar.SetStatusText( "I didn't find any " + self.fileExtension.Value + " files that were created/modified after the last file transfer.")
            return fileList, timeStarted
            
        except:
            self.myStatusBar.SetBackgroundColour('#FF0000')
            self.myStatusBar.SetStatusText(  "There was a problem accessing the source folder")
            
    def xferFiles(self, fileNames, timeStarted):
        try:
            if self.myRadioButton1.GetValue() == True:
                for eachName in fileNames:
                    shutil.move(os.path.join(sourceFolder, eachName), os.path.join(destFolder, eachName))
            else:
                for eachName in fileNames:
                    shutil.copy2(os.path.join(sourceFolder, eachName), os.path.join(destFolder, eachName))
            self.myStatusBar.SetBackgroundColour('#00FF00')
            if len(fileNames) > 1:
                self.myStatusBar.SetStatusText( str(len(fileNames)) + " files were xfered from " + sourceFolder + " to " + destFolder)
            else:
                self.myStatusBar.SetStatusText( str(len(fileNames)) + " file was xfered from " + sourceFolder + " to " + destFolder)
            updateDatabase(timeStarted, str(self.fileExtension.Value).lower())
            self.updateLastXferTextBox(self)
        except:
            self.myStatusBar.SetBackgroundColour('#FF0000')
            self.myStatusBar.SetStatusText(  "There was an error. Check if files are still in " + sourceFolder)

    def xferFilesButton(self, e):
        fileNames, timeStarted = self.getFileList(self)
        if fileNames != []:
            self.xferFiles(fileNames, timeStarted)
        self.fileListBox.Clear()

def updateDatabase(timeStarted, fileExtension):
    connection = sqlite3.connect("fileXfer_database.db")
    c = connection.cursor()
    c.execute("DROP TABLE IF EXISTS DateTimeOfLastXferTable")
    c.execute("CREATE TABLE DateTimeOfLastXferTable(DateAndTime varchar(64), FileExtension varchar(16))")
    c.execute("INSERT INTO DateTimeOfLastXferTable VALUES(?,?)", (str(datetime.datetime.strftime(datetime.datetime.now(), "%m-%d-%Y %H:%M:%S.%f")), fileExtension))
    connection.commit()
    connection.close()    

def getLastFileXferDateTime():
    connection = sqlite3.connect("fileXfer_database.db")
    c = connection.cursor()
    try:
        c.execute( "SELECT * FROM DateTimeOfLastXferTable")
        for row in c.fetchall():
            myReturnValue = datetime.datetime.strptime(str(row[0]), "%m-%d-%Y %H:%M:%S.%f")
            connection.close()
            return myReturnValue
    except:
            c.execute("DROP TABLE IF EXISTS DateTimeOfLastXferTable")
            c.execute("CREATE TABLE DateTimeOfLastXferTable(DateAndTime varchar(64), FileExtension varchar(16))")
            connection.close()
            return None

def getPrevChosenFileExtension():
    connection = sqlite3.connect("fileXfer_database.db")
    c = connection.cursor()
    try:
        c.execute( "SELECT * FROM DateTimeOfLastXferTable")
        for row in c.fetchall():
            myReturnValue = str(row[1])
            connection.close()
            return myReturnValue
    except:
            c.execute("DROP TABLE IF EXISTS DateTimeOfLastXferTable")
            c.execute("CREATE TABLE DateTimeOfLastXferTable(DateAndTime varchar(64), FileExtension varchar(16))")
            connection.close()
            return None

app = wx.App()
myWindow = windowClass(None, size = (470, 600)) # , style = wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
app.MainLoop()
