import cv2

cap = cv2.VideoCapture(0)  # 打开相机

# 创建VideoWriter类对象
fourcc = cv2.VideoWriter_fourcc(*’XVID’)
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while (True):
    ret, frame = cap.read()  # 捕获一帧图像
    out.write(frame)  # 保存帧
    cv2.imshow('frame', frame)  # 显示帧
    # 判断按键，如果按键为q，退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # 关闭相机
out.release()
cv2.destroyAllWindows()  # 关闭窗口import cv2
