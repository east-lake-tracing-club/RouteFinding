import cv2
import numpy as np
# 读取图片并转至灰度模式
imagepath = 'blackwhite.jpg'
img = cv2.imread(imagepath, 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, threshf = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
thresh=~threshf
#膨胀操作
kernel = np.ones((5,5),np.uint8)
mid= cv2.erode(thresh,kernel,iterations =1)
result= cv2.dilate(mid,kernel,iterations =1)
showed=~result

img = cv2.GaussianBlur(result, (3, 3), 0)
canny = cv2.Canny(img, 80, 240)

cv2.namedWindow('Canny',0)
cv2.imshow('Canny', canny)
"""

#Canny 算子

lowThreshold = 0
i = 100
max_lowThreshold = i
ratio = 3
kernel_size = 3
def CannyThreshold(lowThreshold):
    img = cv2.GaussianBlur(thresh, (3, 3), 0)
    canny = cv2.Canny(thresh, lowThreshold, lowThreshold * ratio, apertureSize=kernel_size)
    dst = cv2.bitwise_and(canny, canny, mask=canny)  # just add some colours to edges from original image.
    cv2.namedWindow('Canny',0)
    cv2.imshow('Canny', dst)

cv2.createTrackbar('Min threshold', 'canny demo', lowThreshold, max_lowThreshold, CannyThreshold)

"""
# 显示图片
cv2.namedWindow('showed',0);
cv2.imshow('showed', ~result)
cv2.waitKey()
