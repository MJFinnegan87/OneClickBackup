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
        self.myLastFileXferTextBox = wx.StaticText(panel, -1, "Last File Transfer Was Done: " , pos=(10,150))
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
        self.fileCheckButton = wx.Button(panel, label="Check for .txt files created/modified after the last file transfer.", pos=(10,190), size=(430,25))
        self.fileListBox = wx.ListBox(panel, pos=(10,215), size=(430, 200), style = 1)
        
        wx.StaticText(panel, -1, "Please select what type of file transfer: ", pos=(10, 430))
        self.myRadioButton1 = wx.RadioButton(panel, label="Move", pos=(360,425), size=(80,25), style=wx.RB_GROUP)
        self.myRadioButton2 = wx.RadioButton(panel, label="Copy", pos=(260,425), size=(80,25))
        self.initiateXferButton = wx.Button(panel, label="Transfer .txt files created/modified\nafter the last file transfer.", pos=(10, 465), size=(430,50))

        self.Bind(wx.EVT_TOOL, self.quitProgram, exitItem)
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
            timeStarted = datetime.datetime.now()
            prevFileXfer = getLastFileXferDateTime()
            if prevFileXfer == None:
                prevFileXfer = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)
            fileNames = os.listdir(sourceFolder)
            fileList = []
            fmt = '%Y-%m-%d %H:%M:%S'
            self.fileListBox.Clear()
            for eachName in fileNames:
                if len(eachName) >= 4:
                    if str(eachName[len(eachName)-4:len(eachName)]).upper() == ".TXT" and (prevFileXfer < datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(sourceFolder, eachName)))):
                        self.myStatusBar.SetBackgroundColour('#FFFFFF')
                        self.myStatusBar.SetStatusText( "")
                        fileList.append(eachName)
                        self.fileListBox.Append(eachName)
            if fileList == []:
                self.myStatusBar.SetBackgroundColour('#FF0000')
                self.myStatusBar.SetStatusText( "I didn't find any .txt files that were created/modified after the last file transfer.")
            return fileList, timeStarted
            
        except:
            self.myStatusBar.SetBackgroundColour('#FF0000')
            self.myStatusBar.SetStatusText(  "There was a problem accessing the source folder ")
            
    def xferFiles(self, fileNames, timeStarted):
        try:
            if self.myRadioButton1.GetValue() == True:
                for eachName in fileNames:
                    shutil.move(os.path.join(sourceFolder, eachName), os.path.join(destFolder, eachName))
            else:
                for eachName in fileNames:
                    shutil.copy2(os.path.join(sourceFolder, eachName), os.path.join(destFolder, eachName))
            self.myStatusBar.SetBackgroundColour('#FFFFFF')
            self.myStatusBar.SetStatusText( str(len(fileNames)) + " files were xfered from " + sourceFolder + " to " + destFolder)
            setLastFileXferDateTime(timeStarted)
            self.updateLastXferTextBox(self)
        except:
            self.myStatusBar.SetBackgroundColour('#FF0000')
            self.myStatusBar.SetStatusText(  "There was an error. Check if files are still in " + sourceFolder)

    def xferFilesButton(self, e):
        fileNames, timeStarted = self.getFileList(self)
        if fileNames != []:
            self.xferFiles(fileNames, timeStarted)
        self.fileListBox.Clear()

def setLastFileXferDateTime(timeStarted):
    connection = sqlite3.connect("fileXfer_database.db")
    c = connection.cursor()
    c.execute("DROP TABLE IF EXISTS DateTimeOfLastXferTable")
    c.execute("CREATE TABLE DateTimeOfLastXferTable(DateAndTime varchar(64))")
    c.execute("INSERT INTO DateTimeOfLastXferTable VALUES(?)", (str(datetime.datetime.strftime(datetime.datetime.now(), "%m-%d-%Y %H:%M:%S.%f")),))
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
            c.execute("CREATE TABLE DateTimeOfLastXferTable(DateAndTime varchar(64))")
            connection.close()
            return None

app = wx.App()
myWindow = windowClass(None, size = (470, 600)) # , style = wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
app.MainLoop()
