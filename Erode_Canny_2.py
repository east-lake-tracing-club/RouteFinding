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
mid= cv2.erode(thresh,kernel,iterations =2)
result= cv2.dilate(mid,kernel,iterations =8)
showed=~result
#Canny 算子
lowThreshold = 0
i = 100
max_lowThreshold = i
ratio = 3
kernel_size = 3
def CannyThreshold(lowThreshold):
    detected_edges = cv2.GaussianBlur(showed, (3, 3), 0)
    detected_edges = cv2.Canny(detected_edges, lowThreshold, lowThreshold * ratio, apertureSize=kernel_size)
    dst = cv2.bitwise_and(showed, showed, mask=detected_edges)  # just add some colours to edges from original image.
    cv2.imshow('canny demo', dst)

"""

def BlackWhite():
    smallMosaic = cv2.GaussianBlur(gray, (5, 5), 0)
    BigMosaic = cv2.medianBlur(smallMosaic, 3)
    yes,bw=cv2.threshold(BigMosaic,127,255,cv2.THRESH_BINARY)
    bwback=~bw
    cv2.namedWindow('Black and white of the origin',0)
    cv2.imshow('Black and white of the origin',bwback)

smallMosaic = cv2.GaussianBlur(gray, (5, 5), 0)
BigMosaic = cv2.medianBlur(smallMosaic, 3)
yes,bw=cv2.threshold(BigMosaic,127,255,cv2.THRESH_BINARY)
BlackWhite()
"""

cv2.namedWindow('Closed result',0)
cv2.imshow('Closed result',showed)

#cv2.imwrite("blackwhite.jpg",bw)
#Lines to run the canny
cv2.namedWindow('canny demo',0)
CannyThreshold(0)  # initialization
cv2.createTrackbar('Min threshold', 'canny demo', lowThreshold, max_lowThreshold, CannyThreshold)

if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
