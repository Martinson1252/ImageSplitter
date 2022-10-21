from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit,QVBoxLayout, QWidget,QMainWindow,QPushButton,QProgressBar,QMessageBox,QDialog)
from threading import Thread
import cv2,os

class BackendClass:
    def __init__(self,ui) -> None:
        super().__init__()
        print(ui.ratioHint.text())
        if not os.path.isdir("source"):
            os.mkdir("source")
        if not os.path.isdir("cropped"):
            os.mkdir("cropped")
        self.all_filesnumber = 0
        self.cropped = 0
        
    
    def start(self,ui):
        #self.lock = Lock()
        
        ui.insertField.setText(ui.insertField.text().replace(",","."))
        try:
            self.crop_ratio = float(ui.insertField.text())
        except:
            self.ShowErrorBoxNonNUMERIC(ui)
            return
        
        if float(ui.insertField.text()) > 1 or float(ui.insertField.text()) < 0:
            self.ShowErrorBoxNotFractional(ui)
            return
        img_list = os.listdir("source")

        
        for i in img_list:
            self.all_filesnumber+=1
        print(self.all_filesnumber)
        #print(App.crop_ratio)

        if img_list.count == 0: return
        if ui.startButton.text() == "Start":
            ui.startButton.setText("Stop")
            ui.progressBar.setVisible(True)
        elif ui.startButton.text() == "Stop":
            ui.startButton.setText("Start")
            self.cropped = self.all_filesnumber

        divisior = 10
        parts = self.all_filesnumber/divisior
        partsL = [  [] for a in range(divisior)  ]
        im_num = 0
        part = 0
        for i in img_list:
            
            if im_num >= parts:
                part+=1
                im_num = 0
            partsL[part].append(i)
            im_num += 1

        
        
        
        r = 0
        for i in range(divisior):
            print(r)
            t = Thread(target = lambda: self.Split(partsL[r]))
            t.start()
            #t.join()
            r+=1
            
        #ImageSplitter.C(self)
        ui_ = Thread(target= lambda: self.ChangeBar(ui))
        # #t2 = Thread(target=lambda: ImageSplitter.Split(self))
        ui_.start()

    def ShowErrorBoxNonNUMERIC(self,ui):
        dlg = QMessageBox(ui)
        dlg.setWindowTitle("Error. Wrong value!")
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setText("Value in crop input field is wrong! Should be numerical and fractional")
        dlg.setIcon(QMessageBox.Critical)
        dlg.exec()
    def ShowErrorBoxNotFractional(self,ui):
        dlg = QMessageBox(ui)
        dlg.setWindowTitle("Error. Wrong value!")
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setText("Value in crop input field is wrong! Should be a fraction; more than 0, and less than 1")
        dlg.setIcon(QMessageBox.Critical)
        dlg.exec()
    
    def Split(self,img_list):

        #img_list = os.listdir("source")
        
        print(img_list)
        
        for f in img_list:

            #self.lock.acquire()
            #cropped_images = self.cropped
            if self.cropped >= self.all_filesnumber: return
            image = cv2.imread(os.path.join("source",f))
            height,width,channels = image.shape
            crop_imageR = image 
            crop_imageL = image
            name = f
            name = name.removesuffix(".png")
            name = name + "a"+".png"
            width_begin=0
            height_begin=0
            h=height
            w=int(width*self.crop_ratio)
            crop_imageL = crop_imageL[height_begin:h, width_begin:w]
            cv2.imwrite(os.path.join("cropped",name),crop_imageL)

            name = f
            name = name.removesuffix(".png")
            name = name + "b"+".png"
            width_begin=int(width*self.crop_ratio)
            height_begin=0
            h=height
            w=width
            crop_imageR = crop_imageR[height_begin:h, width_begin:w]
            cv2.imwrite(os.path.join("cropped",name),crop_imageR)
            self.cropped +=1
            #cropped_images +=1
            #sleep(0.0000001)
            #self.cropped = cropped_images
            #self.lock.release()
            #print("image "+f+" ready")
            
    def ChangeBar(self,ui):
        while self.cropped < self.all_filesnumber:
            ui.progressBar.setValue( round( self.cropped/self.all_filesnumber*100 ) )
            #self.ids.proc.text = str(round(self.cropped/self.all_filesnumber*100))+"%"
        ui.progressBar.setValue(0)
        #self.ids.proc.text = ""
        ui.startButton.setText("Start")
        self.all_filesnumber = 0
        self.cropped = 0
        ui.progressBar.setVisible(False)