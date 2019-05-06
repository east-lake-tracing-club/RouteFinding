import cv2
import numpy as np

# 新建512*512的空白图片
img = np.zeros((512,512,3), np.uint8)
# 平面点集
pts = np.array([[200,250], [250,300], [300, 270], [270,200], [120, 240]], np.int32)
pts = pts.reshape((-1,1,2))
# 绘制填充的多边形
cv2.fillPoly(img, [pts], (255,255,255))
# 保存图片
cv2.imwrite('polygon.png', img)