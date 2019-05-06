import cv2
import numpy as np
#新建一个画布

canvas = np.zeros((300,300,3), dtype ="uint8")

class ImageProperty:
    imglength=canvas.shape[0]
    imgwidth=canvas.shape[1]
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

#line=Parallel(0.2,0.2)
#line.drawLeftline(canvas,0,0,255)
toprec=Rectanle(0.2,0.5,2)
toprec.draw(canvas,137,207,240)
meanjudge=toprec.calcumean(canvas)
cv2.namedWindow('class demo')
cv2.imshow('class demo', canvas)
print(meanjudge)
cv2.waitKey(0)

