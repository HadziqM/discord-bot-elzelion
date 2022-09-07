import cv2

list = ["1", "2", "3", "4", "5", "6", "7", "d", "r", "f"]


def conv(a):
    img = cv2.imread(a+".png", cv2.IMREAD_UNCHANGED)
    cv2.imwrite(a+".jpg", img)


def resize(a):
    img = cv2.imread(a+".png", cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (126, 211), interpolation=cv2.INTER_AREA)
    cv2.imwrite(a+".jpg", img)


for i in list:
    resize(i)
conv("board")
