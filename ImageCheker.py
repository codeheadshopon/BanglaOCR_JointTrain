# -*- coding: utf-8 -*-

from PIL import Image,ImageDraw,ImageFont
import matplotlib.pyplot as plt
import random
import os
import cairocffi as cairo
import editdistance
import numpy as np
from scipy import ndimage
from sys import getdefaultencoding
import sys
import random
import matplotlib.pyplot as plt
from keras.preprocessing import image

def b(x,y):
    return filter(lambda A: A not in y, x)
def a(x,y):
    return [_ for _ in x if _ not in y]

imgwide=564
import cv2
from PIL import Image

img = Image.open('testreal.png')
img2 = Image.open('find5.png')

img = img.resize((imgwide, 64), Image.ANTIALIAS)
img2 = img2.resize((imgwide, 64), Image.ANTIALIAS)


img = np.asarray(img)
img2 = np.asarray(img2)

print(img.shape)
print(img2.shape)

#
img = img[:, :, 0]  # grab single channel
img2 = img2[:, :, 0]  # grab single channel

print(img.shape)
print(img2.shape)

set = {1,2,3,3}


# print(set)

# print(img)

# print(set(img2))
#
#
#
img = img.astype(np.float32) / 255
img2 = img2.astype(np.float32) / 255
img = np.expand_dims(img, 0)
img2 = np.expand_dims(img2, 0)

Flag = 0
MinK=0
MinJ=0

img=img2

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        for k in range(img.shape[2]):
            if(img[i][j][k]<1.0) and Flag == 0 :
                if MinK<img[i][j][k]:
                    MinK=k
                    MinJ=j


print(MinJ,"-",MinK)

#
# X_data = np.ones([1, imgwide, 64, 1])
# X_data[0, 0:imgwide, :, 0] = data[0, :, :].T