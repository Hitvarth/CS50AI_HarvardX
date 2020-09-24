
import cv2
import numpy as np

img=cv2.imread('gtsrb/0/00000_00000.ppm',1)
cv2.imshow('kuch bhi ',img)
cv2.waitKey(0)
print(type(img))
print(img.shape)
img=cv2.resize(img,(1000,100))
cv2.imshow('resized',img)
cv2.waitKey(0)
# print(img[0,0,0])

# s1='this is a string'
# s2='.'
# print(f"{s1}{s2}")