from typing import Tuple

import numpy as np
import cv2
#开运算计算来算出路径位置
#我们添加了质心计算和平行线方差

#确定kernel矩阵（不需要迭代计算）
kernel = np.ones((5,5),np.uint8)
def OpenFun(iterErode,iterDilate):
    #从摄像头读取图片
    sucess,img=cap.read()
    #转为灰度图片
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #进行高斯模糊
    gaussiaenresult = cv2.GaussianBlur(gray, (3, 3), 0)
    #转化为二值数据，反色
    ret, threshf = cv2.threshold(gaussiaenresult, 90, 255, cv2.THRESH_BINARY)
    thresh=~threshf
    #膨胀操作
    mid= cv2.erode(thresh,kernel,iterations =iterErode)
    result= cv2.dilate(mid,kernel,iterations =iterDilate)
    dst=cv2.cvtColor(~result,cv2.COLOR_GRAY2BGR)

    #dst = cv2.bitwise_and(img, img, mask=showed)  # just add some colours to edges from original image.
    M = cv2.moments(result)
    cv2.rectangle(dst, topRectangleLeftTop,topRectangleRightBot,(240,207,137 ), 3)
    cv2.rectangle(dst, (0,0),sideShape,(240,207,137 ), 3)
    Toprectangle=result[topRectangleLeftTop[1]:topRectangleLeftBot[1],topRectangleLeftTop[0]:topRectangleLeftBot[0]]#1 是 列数， 2 是行数
    try:
        cX = int(M["m10"] / M["m00"])  # 计算质心
        cY = int(M["m01"] / M["m00"])
        cv2.circle(dst, (cX,cY), 3, (255, 0, 0), -1)
        meanjudge=np.mean(Toprectangle)
        print (meanjudge)
        print ("Center Location:(",cX, ",",cY ,")")
        if LeftlineBotom[0] > cX:
            cv2.line(dst,LeftlineBotom,LeftlineTop ,(0,0,255))
            cv2.line(dst,RihtlineBotom,RihtlineTop ,(0,255,0))
            print("Turn Left")
        elif RihtlineBotom[0] < cX:
            cv2.line(dst,LeftlineBotom,LeftlineTop ,(0,255,0))
            cv2.line(dst,RihtlineBotom,RihtlineTop ,(0,0,255))
            print("Turn Right")
        else:
            cv2.line(dst,LeftlineBotom,LeftlineTop ,(0,255,0))
            cv2.line(dst,RihtlineBotom,RihtlineTop ,(0,255,0))
            print("Keep strght")
    except:
        cv2.line(dst, (imgmiddlehori,0), (imgmiddlehori,imgshape[0]),(0,0,255))
        print ("No signal")
    cv2.imshow('Open demo', dst)


#调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
cap=cv2.VideoCapture(0)
cv2.namedWindow('Open demo')
cv2.createTrackbar('Iteration of Erode', 'Open demo',0,10, OpenFun)
cv2.createTrackbar('Iteration of Dilate', 'Open demo',0,10, OpenFun)

#接下来是平行线位置
#首先读取图片,然后寻找中线之类的。。
sucess,img=cap.read()
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#设定图像
imgshape=       (int(gray.shape[0])     ,int(gray.shape[1]))#0 是行数， 1 是列数
imgmiddlehori=   int(gray.shape[1]/2)
LeftlineBotom=  (int(gray.shape[1]*0.45),int(gray.shape[0]*0.5))
LeftlineTop=    (int(gray.shape[1]*0.45),0)#int(gray.shape[0]))
RihtlineBotom=  (int(gray.shape[1]*0.55),int(gray.shape[0]*0.5))
RihtlineTop=    (int(gray.shape[1]*0.55),0)#int(gray.shape[0]))

topshape= (int(imgshape[0]*0.1),int(imgshape[1]*0.1))#0是高度，1是宽度
topRectangleLeftTop=(imgmiddlehori-int(topshape[1]/2),0)#0是横坐标，1是纵坐标
topRectangleLeftBot=(imgmiddlehori-int(topshape[1]/2),topshape[0])
topRectangleRightTop=(imgmiddlehori+int(topshape[1]/2),0)
topRectangleRightBot=(imgmiddlehori+int(topshape[1]/2),topshape[0])

sideShape= (int(imgshape[0]*0.1),int(imgshape[1]*0.1))#0是高度，1是宽度
#sideRectangleLeftTop=(sideshape[1],0)#0是横坐标，1是纵坐标
sideRectangleLeftBot=(imgmiddlehori-int(topshape[1]/2),topshape[0])
sideRectangleRightTop=(imgmiddlehori+int(topshape[1]/2),0)
sideRectangleRightBot=(imgmiddlehori+int(topshape[1]/2),topshape[0])
#接下来是主循环
while True:
    #显示摄像头，背景是灰度。
    OpenFun(cv2.getTrackbarPos('Iteration of Erode', 'Open demo'),cv2.getTrackbarPos('Iteration of Dilate', 'Open demo'))
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
