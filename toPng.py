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
#--convert to png function--
def toPng (path):
    with Image.open(path) as image:
        # Convert to png format
        format=os.path.splitext(filePath)[1]
        new_file=filePath.replace(format, '.png')
        #print(new_file)
        image.convert('RGB').save(new_file, "PNG")
    print("Image converted and saved to", new_file)
    return new_file
#------------------
#--creating a window--
root=tk.Tk()
root.withdraw()
#------------------
#--letting the user create an image and showing it--
filePath=filedialog.askopenfilename()
originalImg=cv2.imread(filePath)
#show(originalImg[::8,::8])
#------------------

#--run the main loop--
#root.mainloop()
#------------------
newImage=cv2.imread(toPng(filePath))
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

