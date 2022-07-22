import os
import cv2
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from threading import Thread, Lock
from time import sleep


class MainWidget(Widget):
    startB = ObjectProperty(None)
    cropVal = ObjectProperty(None)
    progressB = ObjectProperty(None)
    proc = ObjectProperty(None)
    
    def start(self):
        self.cropped = 0
        #self.lock = Lock()
        try:
            if float(self.cropVal.text) > 1 or float(self.cropVal.text) < 0: return
        except:
            return
        App.crop_ratio = float(self.cropVal.text)
        img_list = os.listdir("source")

        self.all_filesnumber = 0
        for i in img_list:
            self.all_filesnumber+=1
        print(self.all_filesnumber)
        #print(App.crop_ratio)

        if img_list.count == 0: return
        if self.startB.text == "Start":
            self.startB.text = "Stop"
        elif self.startB.text == "Stop":
            self.startB.text = "Start"
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
        for te in range(divisior):
            print(r)
            t = Thread(target = lambda: ImageSplitter.Split(self,partsL[r]))
            t.start()
            #t.join()
            r+=1
            
        #ImageSplitter.C(self)
        ui = Thread(target= lambda: ImageSplitter.ChangeBar(self))
        # #t2 = Thread(target=lambda: ImageSplitter.Split(self))
        ui.start()
        #t2.start()
        
        #ImageSplitter.Split(self)

class ImageSplitter(App):
    def build(self):
        
        Window.size = (400, 400)
        Window.clearcolor = (0.2, 0.2, 0.2, 1)
        if not os.path.isdir("source"):
            os.mkdir("source")
        if not os.path.isdir("cropped"):
            os.mkdir("cropped")
        return MainWidget()
    App.crop_ratio = 0.0

  

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
            w=int(width*App.crop_ratio)
            crop_imageL = crop_imageL[height_begin:h, width_begin:w]
            cv2.imwrite(os.path.join("cropped",name),crop_imageL)

            name = f
            name = name.removesuffix(".png")
            name = name + "b"+".png"
            width_begin=int(width*App.crop_ratio)
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
            
    def ChangeBar(self):
        while self.cropped < self.all_filesnumber:
            self.ids.progressB.value = self.cropped/self.all_filesnumber
            self.ids.proc.text = str(round(self.cropped/self.all_filesnumber*100))+"%"
        self.ids.progressB.value = 0
        self.ids.proc.text = ""
        self.startB.text = "Start"
ImageSplitter().run()




#0.462
#0.477

