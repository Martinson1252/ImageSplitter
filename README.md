# ImageSplitter  
It's a simple program that splits images vertically into 2 parts.  
The spot where a single image will be is splitted, is defined by user's ratio input.  
Program creates 2 folders: **source** and **cropped**.  
User has to manually move all images to the source folder,  
wheras cropped folder is used to store cropped images.  
Program uses multiple threads to complete the task.  
Project uses libraries such as cv2 and pyqt5.  
Compiled version is stored in `dist/ImageSplitter.exe`  

Also there is a version that uses kivy instead of pyqt5 and is located in `kivy` folder,  
however this version is not compiled.



## Great for splitting scans
<p float="left">
<img src="https://user-images.githubusercontent.com/39278140/180551386-86e4cb95-188a-4c50-bab3-011ab4c96435.png" height="450" width="600"  />
</p>



Pyqt5 version:

https://user-images.githubusercontent.com/39278140/197249345-caf8966d-83cb-4b3f-9a20-53caef076aae.mp4



Kivy version:

https://user-images.githubusercontent.com/39278140/181821572-fe63ecf4-857f-41f9-9b09-8436ac0cc066.mp4  















