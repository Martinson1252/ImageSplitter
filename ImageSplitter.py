from backend import BackendClass 
import sys
from stylesheet import style
from tokenize import Double
from turtle import down
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit,QVBoxLayout, QWidget,QMainWindow,QPushButton,QProgressBar)
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import QCursor,QDoubleValidator,QValidator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window().resize(400,400)
        self.scaleValue = 0.0
        self.InitGUI()
        self.backend = BackendClass(self)
        
    def InitGUI(self):
        #text for info
        self.infoLabel = QLabel(self)
        self.infoLabel.setGeometry(QtCore.QRect(self.GetHalf(340),15,340,170))
        self.infoLabel.setText("This program splits images vertically into 2 parts.\nThe place where the single image is split,\nis defined by user's ratio input.\nProgram creates 2 folders: source and cropped.\nIn source folder user has to manually move all\nimages, wheras cropped folder is use to store\ncropped images. Ratio input value is a fraction\n(eg. 0.33) ")
        
        #hint for ration input
        self.ratioHint = QLabel(self)
        self.ratioHint.setGeometry(QtCore.QRect(self.GetHalf(72),180,72,20))
        self.ratioHint.setText("Ratio input:")
        
        #input field for scale (ratio input)
        self.insertField = QLineEdit(self)
        #validation_rule = QDoubleValidator(0.001,0.9999,12)
        #validation_rule.validate(str(self.scaleValue),12)
        #self.insertField.setValidator(validation_rule)
        self.insertField.setGeometry(QtCore.QRect(self.GetHalf(80),205,80,30))
        self.insertField.textEdited[str].connect(lambda: self.InputChange(self.insertField.text()))

        #button to start process
        self.startButton = QPushButton(self)
        self.startButton.setGeometry(QtCore.QRect(self.GetHalf(100),250,100,30))
        self.startButton.setText("Start")
        self.startButton.clicked.connect(lambda: self.backend.start(self))
        self.startButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.startButton.setFont(font)
        
        #progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(self.GetHalf(160),300,160,20))
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)
    
    def InputChange(self,val):
        print(val)
    #Returns correct middle of the screen value (width), for any widget
    def GetHalf(self,width):
        return int(self.window().width()/2 - width/2)
    
    
if __name__=="__main__":
    style = style
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("ImageSplitter")
    

    window.setStyleSheet(style)
    window.show()

    app.exec()