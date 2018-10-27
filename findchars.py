# -*- coding: utf-8 -*-
import wordgenerators_sequential as wg
import cv2
with open('OCR_RAW/100000/100000.txt', 'r') as fp:
    read_lines = fp.readlines()
    ab = read_lines
with open('OCR_RAW/200000/augment.txt', 'r') as fp:
    read_lines2 = fp.readlines()
    ab2 = read_lines
import numpy as np
from PIL import Image

i=0
labelss=[]
labelss2=[]
L = []
labels = []
SourceString = []
LabelLengh = []
input_len = []
labels = np.ones([1159, 120])

Cur = 0
for ok in read_lines:
    labelss.append(ok[:len(ok)-1])
for ok in read_lines2:
    labelss.append(ok[:len(ok)-1])

label=[]

print(len(labelss))
for text in labelss:
    label.append(wg.labelingNewDataset(text))

for i in range(1000):
    for j in range(120):
        labels[i][j] = -1
Run = 0
for i in range(100001, 101001):

    if(i==101000):
        ix=1001000
        L.append("OCR_RAW/100000/" + str(ix) + ".jpg")
    else:
        L.append("OCR_RAW/100000/" + str(i) + ".jpg")


    SourceString.append(labelss[Run])
    Lab = wg.labelingNewDataset(labelss[Run])
    # print(len(Lab))
    for k in range(len(Lab)):
        labels[Cur][k] = Lab[k]
    Cur += 1
    LabelLengh.append(len(Lab))
    input_len.append(120)
    Run+=1
for i in range(1, 165):
    if(i<139 or i>143):

        L.append("OCR_RAW/200000/200" + str(i) + ".jpg")


        SourceString.append(labelss[Run])
        Lab = wg.labelingNewDataset(labelss[Run])
        # print(len(Lab))
        for k in range(len(Lab)):
            labels[Cur][k] = Lab[k]
        Cur += 1
        LabelLengh.append(len(Lab))
        input_len.append(120)
        Run+=1


for file in L:
    # print(file)
    img = cv2.imread(file)
    col_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    im = np.asarray(col_img)
    image = cv2.resize(col_img, (564, 64))
    # print(np.asarray(image).shape)
    cv2.imwrite(file, image)
labels = np.array(labels)
X_data = np.array([np.array(Image.open(fname)) for fname in L])



print(labels.shape)
print(X_data.shape)
print(len(SourceString))
print(len(input_len))
import matplotlib.pyplot as plt


# plt.imshow(X_data[2],cmap='gray')
# plt.show()
X_data = X_data.reshape(X_data.shape[0], 64, 564)

x_data = np.ones([X_data.shape[0], 564, 64, 1])
x_data[0, 0:564, :, 0] = X_data[0, :, :].T



print(x_data.shape)
