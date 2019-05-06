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

    try:
        cX = int(M["m10"] / M["m00"])  # 计算质心
        cY = int(M["m01"] / M["m00"])
        cv2.circle(dst, (cX,cY), 3, (255, 0, 0), -1)
        topRec.draw(dst,193,210,240)
        leftRec.draw(dst,193,210,240)
        rightRec.draw(dst,193,210,240)
        topmean=topRec.calcumean(result)
        leftmean=leftRec.calcumean(result)
        rightmean=rightRec.calcumean(result)
        print ("Mean of top rectangle is",topmean)
        print ("Mean of left rectangle is",leftmean)
        print ("Mean of right rectangle is",rightmean)
        print ("Center Location:(",cX, ",",cY ,")")
        if topparalell.LeftlineBotom[0] > cX:
            topparalell.drawLeftline(dst,255,0,0)
            topparalell.drawRihtline(dst,0,255,0)
            print("Turn Left")
        elif topparalell.RihtlineBotom[0] < cX:
            topparalell.drawLeftline(dst,0,255,0)
            topparalell.drawRihtline(dst,255,0,0)
            print("Turn Right")
        else:
            topparalell.drawLeftline(dst,0,255,0)
            topparalell.drawRihtline(dst,0,255,0)
            print("Keep strght")
    except:
        topparalell.drawLeftline(dst,255,0,0)
        topparalell.drawRihtline(dst,255,0,0)
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

class ImageProperty:
    imglength=img.shape[0]
    imgwidth=img.shape[1]
    imgmiddlehori=int(imgwidth/2)

class Parallel(ImageProperty):
    widthRatio=0
    lengthratio=0
    #Follow is the COORDINATE SYSTEM!
    LeftlineTop=(0,0)
    LeftlineBotom=(0,0)
    RihtlineTop=(0,0)
    RihtlineBotom=(0,0)
    def __init__(self,l,w):
        self.lengthratio=   l
        self.widthRatio=    w
        self.LeftlineTop=   (int(self.imgwidth*(0.5-w/2)),0)
        self.LeftlineBotom= (int(self.imgwidth*(0.5-w/2)),int(self.imglength*l))
        self.RihtlineTop=   (int(self.imgwidth*(0.5+w/2)),0)
        self.RihtlineBotom= (int(self.imgwidth*(0.5+w/2)),int(self.imglength*l))
    def drawLeftline(self,paper,R,G,B):
        cv2.line(paper,self.LeftlineBotom,self.LeftlineTop ,(B,G,R))
    def drawRihtline(self,paper,R,G,B):
        cv2.line(paper,self.RihtlineBotom,self.RihtlineTop ,(B,G,R))

class Rectanle(ImageProperty):
    widthratio=0
    lengthratio=0
    type=0
    #type=1 is at top
    #type=2 is at left side
    #type=3 is at right side
    ltloc=(0,0)
    rbloc=(0,0)
    ltcor=(0,0)
    rbcor=(0,0)
    #These locations are for matrix calculation
    def __init__(self, l, w, t):#Rectangle(length,width,type)
        self.widthratio = w
        self.lengthratio= l
        self.type = t
        if t==1:
            self.ltloc=(0,int(self.imgwidth*(0.5-w/2)))#Use standard matrix form.
            self.rbloc=(int(self.imglength*l),int(self.imgwidth*(0.5+w/2)))
        elif t==2:
            self.ltloc=(int(self.imglength*(1-l)),0)
            self.rbloc=(self.imglength,int(self.imgwidth*w))
        elif t==3:
            self.ltloc=(int(self.imglength*(1-l)),int(self.imgwidth*(1-w)))
            self.rbloc=(self.imglength,self.imgwidth)
        else :
            self.ltloc=(0,0)
            self.rbloc=(0,0)

        self.ltcor=(self.ltloc[1],self.ltloc[0])
        self.rbcor=(self.rbloc[1],self.rbloc[0])

    def draw(self,paper,R,G,B):
        cv2.rectangle(paper,self.ltcor,self.rbcor,(B,G,R ),2)

    def calcumean(self,image):
        return np.mean(image[self.ltloc[0]:self.rbloc[0],self.ltloc[1]:self.rbloc[1]])

topparalell = Parallel(0.5,0.3)
topRec=Rectanle(0.3,0.4,1)
leftRec=Rectanle(0.5,0.1,2)
rightRec=Rectanle(0.5,0.1,3)
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
