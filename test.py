import cv2



for i in range(0,4):
    img = cv2.imread("img_copy/traffic"+ str(i))
    cv2.im