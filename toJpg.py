import numpy as np
import cv2
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog
def show(img):
    img=np.uint8(img)
    cv2.imshow("img",img)
    cv2.waitKey(0)
def normalize(img):
    img=img*1
    img=img-img.min()
    img=img/img.max()
    return np.uint8(255*img)
#--convert to jpg function--
def toJpg (path):
    with Image.open(path) as image:
        # Convert to JPG format
        format=os.path.splitext(filePath)[1]
        new_file=filePath.replace(format, '.jpg')
        #print(new_file)
        image.convert('RGB').save(new_file, "JPEG")
    print("Image converted and saved to", new_file)
    return new_file

# Open the image file

#--creating a window--
root=tk.Tk()
root.withdraw()
#------------------
#--letting the user create an image and showing it--
filePath=filedialog.askopenfilename()
originalImg=cv2.imread(filePath)
#show(originalImg)
#------------------

#--converting the image to jpg--

#--run the main loop--
#root.mainloop()
#------------------
newImage=cv2.imread(toJpg(filePath))
#------------------

#--turning images into arrays--
originalImg=np.array(originalImg)
newImage=np.array(newImage)
# originalImageArray=np.array(file_path)
# newImageArray=np.array(toJpeg(file_path))
#------------------

#--finding the difference between the images--
#diff=(np.uint8(abs(originalImg)-np.uint8(abs(newImage))))
#show(normalize(diff))
#cv2.imwrite(r"diff.jpg",(normalize(diff)[::8,::8]))
#------------------

