from PIL import Image
import tkinter as tk
from tkinter import filedialog
import cv2
import os
import numpy as np

def toWebp(path):
    with Image.open(path) as image:
        image = image.convert('RGB')
        file_name, file_extension = os.path.splitext(path)
        new_file = file_name + '.webp'
        image.save(new_file, 'webp')
        return new_file

# creating a window
root = tk.Tk()
root.withdraw()

# letting the user select an image and showing it
filePath = filedialog.askopenfilename()
originalImg = cv2.imread(filePath)

# converting the image to webp
newFilePath = toWebp(filePath)

# reading the converted image
newImage = cv2.imread(newFilePath)

# turning images into arrays
originalImg = np.array(originalImg)
newImage = np.array(newImage)
