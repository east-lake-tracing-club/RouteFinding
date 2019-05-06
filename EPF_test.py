import cv2

def bi_demo(image):
    dst = cv2.bilateralFilter(src=image, d=0, sigmaColor=100, sigmaSpace=15)
    cv2.imshow("bi_demo", dst)

img=cv2.imread('Test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bi_demo(gray)
