import sys, os, difflib
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QColorDialog, QLineEdit
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QUrl
from PyQt5.QtWinExtras import QWinTaskbarProgress, QWinTaskbarButton
from os import path



width = 1200    #MAKE THIS A BUTTON TO A FUNCTION
height = 800   

class AllowHyperLinks(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setParent(parent)

class allTheThings(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(allTheThings, self).__init__(parent)

        self.checkBoxStore = []                                                                                                     #Stores state of the checkboxes

        self.mainTabWidget = QtWidgets.QTabWidget()                                                                                 #Creates the tabs
        self.mainWindow = QtWidgets.QWidget()                                                                                       #Creates tab 1
        self.importWindow = QtWidgets.QWidget()                                                                                     #Creates tab 2
        self.compareWindow = QtWidgets.QWidget()                                                                                    #Creates tab 3
        self.telnetWindow = QtWidgets.QWidget()                                                                                     # Creates tab 4 (RM)
        self.settingsWindow = QtWidgets.QWidget()                                                                                   #Creates tab 5

        self.mainTabWidget.addTab(self.mainWindow,"Main")                                                                           #Makes tab 1 view-able
        self.mainTabWidget.addTab(self.importWindow, "Import")                                                                      #Makes tab 2 view-able
        self.mainTabWidget.addTab(self.compareWindow,"Compare")                                                                     #Makes tab 3 view-able
        self.mainTabWidget.addTab(self.telnetWindow, "Telnet")                                                                      #Makes tab 4 view-able (RM)
        self.mainTabWidget.addTab(self.settingsWindow,"Settings")                                                                   #Makes tab 5 view-able

        self.setWindowTitle("Quagga")                                                                                               #Sets the window title
        self.setWindowIcon(QIcon('Qlogo.png'))

        self.setCentralWidget(self.mainTabWidget)

        self.mainWindow.layout = QtWidgets.QVBoxLayout(self)                                                                        #Initializes layout for tab mainWindow
        linkTemplate = '<a href={0}>{1}</a>'                                                                                        #Template for the link? idek
        self.labelWebsite = AllowHyperLinks(self)                                                                                   #Makes a variable to reference AllowHyperLinks class
        self.labelWebsite.setText(linkTemplate.format('https://Google.com', 'Google'))                                              #Sets the text of the label to display our website -> replace the https://Google.com with our URL and replace Google with the text to display
        self.mainWindow.layout.addWidget(self.labelWebsite)                                                                         #Adds the Hyperlink to the mainWindow
        self.mainWindow.setLayout(self.mainWindow.layout)                                                                           #Sets the layout of the mainWindow Window

        self.importWindow.layout = QtWidgets.QVBoxLayout(self)                                                                      #Initializes layout for tab importWindow
        self.btnChangeFolder = QtWidgets.QPushButton("Choose a folder", clicked = self.readFolder)                                  #Makes a button on importWindow that says "Choose a folder" then runs readFolder function
        self.btnChangeToCompare = QtWidgets.QPushButton("Compare", clicked = self.importToCompare)                                  #Makes a button on importWindow that says "Compare" then runs importToCompare function
        self.importWindow.layout.addWidget(self.btnChangeFolder)                                                                    #Adds btnChangeFolder to importWindow window
        self.importWindow.layout.addWidget(self.btnChangeToCompare)                                                                 #Adds btnChangeToCompare to importWindow window
        self.importWindow.setLayout(self.importWindow.layout)                                                                       #sets the layout of importWindow window

        
        

        self.compareWindow.layout = QtWidgets.QVBoxLayout(self)                                                                     #Initializes layout for tab compareWindow
        self.btnAnotherCompare = QtWidgets.QPushButton("New Compare", clicked = self.removeCompareBoxes)                               #Makes a button on compareWindow that says "New Compare" then runs compareToImport function
        self.compareWindow.layout.addWidget(self.btnAnotherCompare)                                                                 #adds btnAnotherCompare to compareWindow window
        self.compareWindow.setLayout(self.compareWindow.layout)                                                                     #sets the layout of compareWindow window

        self.nameHost = QLabel("Enter your device IP: ", self.telnetWindow)                                                         # Creates a Hostname Label (RM)
        self.nameHost.move(10, 30)                                                                                                  # Moves it to desire location (RM)
        self.HOST = QLineEdit(self.telnetWindow)                                                                                    # Creates a Host Line Editor (RM)
        self.HOST.move(150, 30)                                                                                                     # Moves it to desire location (RM)
        self.nameTelnet = QLabel("Enter telnet password: ", self.telnetWindow)                                                      # Creates a Telnetpassword Label (RM) Wednesday night Eureka moment Me and Richard
        self.nameTelnet.move(10, 80)                                                                                                # Moves it to desire location (RM)
        self.telnetPass = QLineEdit(self.telnetWindow)                                                                              # Creates a Telnet Line Editor (RM)
        self.telnetPass.move(150, 80)                                                                                               # Moves it to desire location (RM)
        self.nameEnable = QLabel("Enter enable password: ", self.telnetWindow)                                                      # Creates a Enable password label (RM)
        self.nameEnable.move(10, 130)                                                                                               # Moves it to desire location (RM)
        self.enablePass = QLineEdit(self.telnetWindow)                                                                              # Creates a Enable Line Editor (RM)
        self.enablePass.move(150, 130)                                                                                              # Moves it to desire location (RM)



        self.settingsWindow.layout = QtWidgets.QVBoxLayout(self)                                                                    #Initializes layout for tab settingWindow
        self.fontSettings = QtWidgets.QPushButton("Fonts", clicked = self.userInputFonts)                                           #Makes a button on settingWindow that sats "Change Font" then runs userInputFonts
        self.settingsWindow.layout.addWidget(self.fontSettings)                                                                     #adds btnfontSettings to settingsWindow window
        self.settingsWindow.setLayout(self.settingsWindow.layout)                                                                   #sets the layout of settingsWindow window

    def fileCheck(self):
        if (path.exists("properties.txt")) == False:                                                                                #Checks to see if the properties.txt file exists
            self.propertiesFile = open("properties.txt", "x")                                                                       #If it doesnt, create the file
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)                                                                       #Make a popup if the file doesn't exist
            msgBox.setText("This seems to be the first time you are opening Quagga \n Would you like to see the tutorial?")         #What the popup says
            msgBox.setWindowTitle("Welcome to Quagga!")                                                                             #Window title of popup
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)                                         #buttons on the popup, eventually these will actually do something

            returnValue = msgBox.exec()

    def userInputFonts(self):
        font, ok = QtWidgets.QFontDialog.getFont()                                                                                  #Opens Font dialog, letting user choose fonts and text size etc, then waits for the button "ok" to be pressed

        if ok:                                                                                                                      #When the "OK" button is pressed, change the fonts of the following widgets MAKE SURE TO AdD ALL NEW WIDGETS TO THIS OR >:(
            self.btnChangeFolder.setFont(font)
            self.btnChangeToCompare.setFont(font)
            self.btnAnotherCompare.setFont(font)
            self.fontSettings.setFont(font)
            self.labelWebsite.setFont(font)
            self.nameHost.setFont(font)
            self.nameTelnet.setFont(font)
            self.nameEnable.setFont(font)



    def readFolder(self):                                                                                                           #Function that reads what folder the user would like to look in
        self.TextFiles = []                                                                                                         #Initialzes the self.Textfiles list
        self.folderChosen = QtWidgets.QFileDialog.getExistingDirectory()                                                            #Asks the user what folder he wants to use, Opens File Explorer, then assigns the chosen folder to folderChosen
        self.btnChangeFolder.setText(self.folderChosen)                                                                             #Changes the text of self.btnChangeFolder to folderChosen(The folder the user chooses)

        for files in os.listdir(self.folderChosen):                                                                                 #Finds all files in selected directory ending with .txt and adds them to list
            if files.endswith(".txt"):
                self.TextFiles.append(files) 

        
        if len(self.TextFiles) == 0:                                                                                                #If the folder the user has chosen does not have any text files, show an error popup asking if theyd like to choose a different folder
            alert = QtWidgets.QMessageBox.warning(self, "Error","Your folder has no files! \n Would you like try again?", 
                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Close)
            if alert == QtWidgets.QMessageBox.Yes:
                self.readFolder()

        self.deleteCheckboxes()                                                                                                     #Runs deleteCheckboxes function ---- This is needed to clear checkboxes if the user chooses multiple folders

    def createCheckBoxes(self):                                                                                                     #Function that creates checkboxes for each textfile in the folderChosen                                                                                                       

        for file in self.TextFiles:                                                                                                 #for each .txt in the TextFiles list, create a checkbox and add it to the screen
            self.checkBoxState = QtWidgets.QCheckBox(file, self)
            self.checkBoxStore.append(self.checkBoxState)
            self.importWindow.layout.addWidget(self.checkBoxState)

    def deleteCheckboxes(self):                                                                                                     #Function that deletes the checkboxes, Otherwise they overlay and blehh --- Runs BEFORE createCheckboxes
        for i in range(len(self.checkBoxStore)):
            if i >= 0:
                i=-1
            self.checkBoxStore[i].deleteLater()                                                                                     #actually deletes the checkboxes
            self.checkBoxStore.pop()                                                                                                #removes the instance of the checkbox from the list

        self.createCheckBoxes()                                                                                                     #Runs createCheckbox Function

    def importToCompare(self):                                                                                                      #Changes the focus of the program to the 3rd tab(compareWindow) then runs compareStuff function
            self.mainTabWidget.setCurrentIndex(2)
            self.compareStuff()

    def compareStuff(self):                                                                                                         #This is where we need to add the comparison shit
        context = 2
        i=0
        j=[]
        folderDirectory = self.folderChosen                                                                                         #Folder where files are stored

        while i < len(self.TextFiles):                                                                                              #Find which files have been chosen from check boxes
            if self.checkBoxStore[i].isChecked():                                                                                   
                j.append(i)                                                                                                         #j is a list that stores chosen check boxes location
            i+=1
                       
        file1 = folderDirectory + "/" + self.TextFiles[j.pop(0)]                                                                    #create full file location of first file
        file2 = folderDirectory + "/" + self.TextFiles[j.pop(0)]                                                                    #create full file location of first file
        file1Lines = open(file1).readlines()                                                                                        #Read and append each line of file into list
        file2Lines = open(file2).readlines()                                                                                        #Read and append each line of file into list 
        self.diff = list(difflib.Differ().compare(file1Lines, file2Lines))                                                          #Create list of comparison 

        file1Changes = []                                                                                                           #actual changes in file 1 ex//hostname
        file2Changes = []                                                                                                           #actual changes in file 2 ex//hostname

        file1LineChanges = []                                                                                                       #line that the changes happen on
        file2LineChanges = []                                                                                                       #line that the changes happen on
        g = 0

        for line in self.diff:                                                                                                      #Organize compare file into seperate lists
            check = True
            if line.startswith('-'):                                                                                                #File 1 changes
                file1Changes.append(line)
                file1LineChanges.append(g)
                g-=1
            elif line.startswith('+'):                                                                                              #File 2 Changes
                file2Changes.append(line)
                file2LineChanges.append(g)
            elif line.startswith('?'):                                                                                              #skip lines
                check = False
                pass
            if check == True:                
                g+=1

        self.display = QtWidgets.QListWidget(self)                                                                                  #list widget
        self.display2 = QtWidgets.QListWidget(self)
        y=0
        for z in range(0,len(file1Lines)):                                                                                          #adding line color
            b = QListWidgetItem(file1Lines[z])
            for y in range(len(file1LineChanges)):                                                                                  #y count the amount of changes in the file
                if z == file1LineChanges[y]:                                                                                        #if line # of orignal line == line change #
                    b.setBackground( QColor('#E9401C'))                                                                             #Change color of line
                    self.display.addItem(b)
                    y+=1
            self.display.addItem(b)

            z+=1
        y=0
        z=0
        for z in range(0,len(file2Lines)):                                                                                          #File #2 line color changes
            b = QListWidgetItem(file2Lines[z])
            for y in range(0, len(file2LineChanges)): 
                if z == file2LineChanges[y]:
                    b.setBackground( QColor('#E9401C'))
                    self.display2.addItem(b)
                    y+=1 
            self.display2.addItem(b)


            z+=1

        self.compareWindow.layout.addWidget(self.display)
        self.compareWindow.layout.addWidget(self.display2)
        

    def removeCompareBoxes(self):
        self.compareToImport()
        self.display.deleteLater()
        self.display2.deleteLater()

        

    def compareToImport(self):                                                                                                      #Changes the focus of the program to the 1st(compareWindow)
        self.mainTabWidget.setCurrentIndex(1)

  


if __name__ == "__main__":                                                                                                          #I Have no idea what this actually does, but everyone else has it and im a sheep                                                  

    app = QtWidgets.QApplication(sys.argv)                                                                                          #Makes the program an app? I honest dont know either
    #screen_rect = app.desktop().screenGeometry()                                                                                   #Finds your current screen resolution
    #width, height = screen_rect.width(), screen_rect.height()                                                                      #Sets width and height to your monitor resolution
    w = allTheThings()                                                                                                              #makes w  = the class allTheThings
    w.resize(width, height)                                                                                                         #Sets default screensize
    w.show()                                                                                                                        #Show the class allTheThings to the screens
    w.fileCheck()
    sys.exit(app.exec_())