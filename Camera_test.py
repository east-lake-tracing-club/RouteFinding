import numpy as np
import cv2
#Canny 算法阈值函数（不懂）
#我们添加了质心计算和平行线方差

#Canny 算法参数配置
lowThreshold = 0
i = 100
max_lowThreshold = i
ratio = 3
kernel_size = 3
def CannyThreshold(lowThreshold):
    gaussianresult = cv2.GaussianBlur(gray, (3, 3), 0)
    detected_edges = cv2.Canny(gaussianresult, lowThreshold, lowThreshold * ratio, apertureSize=kernel_size)
    dst = cv2.bitwise_and(img, img, mask=detected_edges)  # just add some colours to edges from original image.
    M = cv2.moments(detected_edges)
    try:
        cX = int(M["m10"] / M["m00"])  # 计算质心
        cY = int(M["m01"] / M["m00"])
        cv2.circle(dst, (cX,cY), 3, (255, 0, 0), -1)
        #cv2.line(dst, (cX, 0), (cX, detected_edges.shape[1]), (0,255,0))
        print ("Center Location:(",cX, ",",cY ,")")
        if LeftlineBotom[0] > cX:
            cv2.line(dst,LeftlineBotom,LeftlineTop ,(0,0,255))
            cv2.line(dst,RihtlineBotom,RihtlineTop ,(0,255,0))
        elif RihtlineBotom[0] < cX:
            cv2.line(dst,LeftlineBotom,LeftlineTop ,(0,255,0))
            cv2.line(dst,RihtlineBotom,RihtlineTop ,(0,0,255))
            print("Turn Right")
        else:
            cv2.line(dst,LeftlineBotom,LeftlineTop ,(0,255,0))
            cv2.line(dst,RihtlineBotom,RihtlineTop ,(0,255,0))
            print("Keep strght")
    except:
        cv2.line(dst, (imgmiddlehori,0), (imgmiddlehori,imgshape[0])(0,0,255))
        print ("No signal")
    cv2.imshow('canny demo', dst)


#调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
cap=cv2.VideoCapture(0)
cv2.namedWindow('canny demo')
cv2.createTrackbar('Min threshold', 'canny demo', lowThreshold, max_lowThreshold, CannyThreshold)

#接下来是平行线位置
sucess,img=cap.read()
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

imgshape=       (int(gray.shape[0])     ,int(gray.shape[1]))
imgmiddlehori=   int(gray.shape[1]/2)
LeftlineBotom=  (int(gray.shape[1]*0.33),int(gray.shape[0]*0.5))
LeftlineTop=    (int(gray.shape[1]*0.33),0)#int(gray.shape[0]))
RihtlineBotom=  (int(gray.shape[1]*0.66),int(gray.shape[0]*0.5))
RihtlineTop=    (int(gray.shape[1]*0.66),0)#int(gray.shape[0]))
#接下来是主循环
while True:
    #从摄像头读取图片
    sucess,img=cap.read()
    #转为灰度图片
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #显示摄像头，背景是灰度。
    CannyThreshold(cv2.getTrackbarPos('Min threshold', 'canny demo'))
    #保持画面的持续。
    k=cv2.waitKey(1)
    if k == 27:
        #通过esc键退出摄像
        cv2.destroyAllWindows()
        break
    elif k==ord("s"):
        #通过s键保存图片，并退出。
        cv2.imwrite("image2.jpg",img)
        cv2.destroyAllWindows()
        break
#关闭摄像头
cap.release()
