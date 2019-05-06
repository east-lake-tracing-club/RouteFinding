import cv2
import numpy as np
cv2.namedWindow('canny demo')
def CannyThreshold(lowThreshold):
    detected_edges = cv2.GaussianBlur(gray, (3, 3), 0)
    detected_edges = cv2.Canny(detected_edges, lowThreshold, lowThreshold * ratio, apertureSize=kernel_size)
    dst = cv2.bitwise_and(img, img, mask=detected_edges)  # just add some colours to edges from original image.
    M = cv2.moments(detected_edges)
    cX = int(M["m10"] / M["m00"])  # 计算质心
    #cY = int(M["m01"] / M["m00"])
    cv2.line(dst, (cX, 0), (cX, detected_edges.shape[1]), (0,0,255))
    cv2.imshow('canny demo', dst)

def BlackWhite():
    smallMosaic = cv2.GaussianBlur(gray, (5, 5), 0)
    BigMosaic = cv2.medianBlur(smallMosaic, 3)
    yes,bw=cv2.threshold(BigMosaic,127,255,cv2.THRESH_BINARY)
    bwback=~bw
    cv2.imshow('img',bwback)


lowThreshold = 0
i = 100
max_lowThreshold = i
ratio = 3
kernel_size = 3

img = cv2.imread('Test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


smallMosaic = cv2.GaussianBlur(gray, (5, 5), 0)
BigMosaic = cv2.medianBlur(smallMosaic, 3)
yes,bw=cv2.threshold(BigMosaic,127,255,cv2.THRESH_BINARY)
cv2.namedWindow('Origin',0)
cv2.imshow('Origin',img)

cv2.createTrackbar('Min threshold', 'canny demo', lowThreshold, max_lowThreshold, CannyThreshold)
BlackWhite()
cv2.imwrite("blackwhite.jpg",bw)


CannyThreshold(0)  # initialization
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
