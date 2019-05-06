import cv2
import numpy as np

# 读取图片并转至灰度模式
imagepath = 'blackwhite.jpg'
img = cv2.imread(imagepath, 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#转化成阈值模式
ret, threshf = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
thresh=~threshf
#转化为二值模式
zero_one=np.where(thresh<100,0,1)
#蒙版操作
#这个操作是为了将整个图片范围集中在摄像影像中央by增加中间的权重
#下面的注释是蒙版矩阵
"""
11...1122...2233....3322....2211....11
11...1122...2233....3322....2211....11
.
.
.
11...1122...2233....3322....2211....11
11...1122...2233....3322....2211....11
"""
#显然，这个方式很傻逼，不如我们用单位矩阵，并且给每行加权
#我们需要把我们之前算的阈值阵列先转化为方阵
#接下来进行阶段操作
#################################
#################################
squaresize=zero_one.shape[0]
STARTCOL=int((zero_one.shape[0]-squaresize)/2)
ENDCOL=int((zero_one.shape[0]+squaresize)/2)
STARTLIN=int((zero_one.shape[1]-squaresize)/2)
ENDLIN=int((zero_one.shape[1]+squaresize)/2)
square=zero_one[STARTCOL:ENDCOL,STARTLIN:ENDLIN]
#################################
#################################
#接下来形成矩阵
subsubvalue=1;
subvalue=2;
centervalue=3;
subsublength=int(squaresize/5);
sublength=int(squaresize/5);
centerlength=square.shape[0]-2*subsublength-2*sublength
subsubmatrix=subsubvalue*np.ones([squaresize,subsublength])
submatrix=subvalue*np.ones([squaresize,sublength])
cenmatrix=centervalue*np.ones([squaresize,centerlength])
noobmask=np.hstack((subsubmatrix,submatrix,cenmatrix,submatrix,subsubmatrix))
noobmask=noobmask.astype(int)
#power=np.hstack((subsubvalue*np.ones(subsublength,int),subvalue*np.ones(sublength,int),centervalue*np.ones(centerlength,int),subvalue*np.ones(sublength,int),subsubvalue*np.ones(subsublength,int)))
#noobmask=np.diag(power)
#接下来进行蒙版
powersquare=cv2.multiply(square,noobmask)
#膨胀操作
kernel = np.ones((5,5),np.uint8)
mid= cv2.erode(thresh,kernel,iterations =2)
result= cv2.dilate(mid,kernel,iterations =8)
showed=~result

#接下来是数组操作：
#1.先把图像矩阵分割成128*128个子矩阵
#PS；这里的‘128’之后可以改为Matrix_Size

#2.对每个子矩阵求平均值
#3.对每个子矩阵求方差
#PS：此方差没有上限，有下限


print (showed.shape)
# 只输出行数
print (showed.shape[0]) # 4
# 只输出列数
print (showed.shape[1]) # 3
