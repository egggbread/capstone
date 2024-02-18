import numpy as np
import cv2
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image
import pillow_avif

def show(img):
    img=np.uint8(img)
    cv2.imshow("img",img)
    cv2.waitKey(0)

def normalize(img):
    img=img*1
    img=img-img.min()
    img=img/img.max()
    return np.uint8(255*img)

def rgb2gray(img):

    #r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def standardDev (img, path):
    with Image.open(path) as image:
        img=rgb2gray(img)
        stdDev=np.std(img)
        print("Standard deviation:", stdDev)

def  edgeDetect (img, path):
    with Image.open(path) as image:
        img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(img, 100, 200)
        numEdges = cv2.countNonZero(edges)
        print("Number of edges:", numEdges)

def fileSize (img, path):
        with Image.open(path) as image:
            print (os.path.getsize(filePath))

root = tk.Tk()
root.withdraw()
#------------------
#--letting the user create an image and showing it--
filePath = filedialog.askopenfilename()
originalImg=cv2.imread(filePath)
print(filePath)
show(originalImg)

standardDev(originalImg,filePath)
edgeDetect(originalImg,filePath)
fileSize(originalImg,filePath)
