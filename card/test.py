import cv2

yaxis = [64, 300]
xaxis = [56, 211, 367, 522, 677]

cardd = (126, 211)
textd = (121, 44)
textp = (846, 64)


card_list = [1, 2, 3, 4, 5, 6, 7, "d", "r", "f"]
card_list = [str(i)+".jpg" for i in card_list]

bg = cv2.imread("board.jpg", cv2.IMREAD_UNCHANGED)
bg = cv2.cvtColor(bg, cv2.COLOR_BGRA2BGR)


def put_text(text, bg):
    text = str(text)+"Bc"
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    size = cv2.getTextSize(text, font, 1, 1)[0]
    x = int((textd[0] - size[0])/2 + textp[0])
    y = int((textd[1] + size[1])/2 + textp[1])
    cv2.putText(bg, text, (x, y), font, 1, (255, 255, 255), 1)
    return bg


def card_pos(x):
    if x > 4:
        return tuple([xaxis[x-5], yaxis[1]])
    else:
        return tuple([xaxis[x], yaxis[0]])


def card_slot(bg, card, pos):
    img = cv2.imread(card, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    bg[pos[1]:pos[1]+cardd[1], pos[0]:pos[0]+cardd[0]] = img
    return bg


for i in range(10):
    bg = card_slot(bg, card_list[i], card_pos(i))
bg = put_text(1000, bg)
cv2.imwrite("test.jpg", bg)
