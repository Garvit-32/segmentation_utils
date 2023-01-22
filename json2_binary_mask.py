import json
import os
import numpy as np
import PIL.Image
import cv2
import matplotlib.pyplot as plt


with open("10044.json", "r") as read_file:
    data = json.load(read_file)[0]

img = np.asarray(PIL.Image.open('10044.tiff'))    

data = np.asarray(data)    
y = data[:,1]
x = data[:,0]


fig = plt.figure()

plt.imshow(img.astype(np.uint8)) 
plt.scatter(x,y,zorder=2,color='red',marker = '.', s= 55)

ab=np.stack((x, y), axis=1)

img2=cv2.drawContours(img, [ab], -1, (255,255,255), -1)

mask = np.zeros((img.shape[0],img.shape[1]))
img3=cv2.drawContours(mask, [ab], -1, 255, -1)


mask = cv2.resize(mask,(448,448))

cv2.imwrite('binary_test.png',mask.astype(np.uint8))
    
