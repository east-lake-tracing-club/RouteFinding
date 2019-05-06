import cv2
import numpy as np
# 读取图片并转至灰度模式
imagepath = 'blackwhite.jpg'
img = cv2.imread(imagepath, 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 二值化
ret, threshf = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
thresh=~threshf
#膨胀操作
kernel = np.ones((5,5),np.uint8)
result= cv2.dilate(thresh,kernel,iterations = 1)
#

# 显示图片
cv2.namedWindow('line',0);
cv2.imshow('line', ~result)
cv2.namedWindow('origin',0);
cv2.imshow('origin', img)

cv2.waitKey()