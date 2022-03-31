# -*- coding: utf-8 -*-
import cv2
import numpy as np
import cv2 as cv



if __name__ == '__main__':
    def nothing(*arg):
        pass

cv2.namedWindow("result") 
cv2.namedWindow("settings")  # создаем окно настроек

cap = cv2.VideoCapture(0)
# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
crange = [0, 0, 0, 0, 0, 0]

color_blue = (255, 0, 0)
color_red = (0, 0, 0)

kernel = np.ones((5, 5), np.uint8)
count = 0

while True:
    flag, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    median = cv2.medianBlur(opening, 15)  # накладываем блюр на видеопоток
    cv2.imshow('Opening', opening)

    hsv = cv.cvtColor(median, cv.COLOR_BGR2HSV)
    #для желтого min(16,74,128) max(30,230,249)
    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)
    cv2.imshow('result', thresh)

    try:
        # hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # thresh1 = cv.inRange(hsv, hsv_min, hsv_max)
        #!
        #_, contours, _= cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours0, _ = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        #!
        cv2.line(img, (300, 1), (300, 800), color_red, thickness=2, lineType=8, shift=0) #Центральные линии
        cv2.line(img, (320, 1), (320, 800), color_blue, thickness=2, lineType=8, shift=0)

        cv2.line(img, (100, 1), (100, 800), color_blue, thickness=2, lineType=8, shift=0) #Боковые линии
        cv2.line(img, (500, 1), (500, 800), color_blue, thickness=2, lineType=8, shift=0)
        # (x1,y1) (x2,y2)
        #count = 0
        for cnt in contours0:

            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            center = (int(rect[0][0]), int(rect[0][1]))
            area = int(rect[1][0] * rect[1][1])

            """
            #подсчет угла
            edge1 = np.int0((box[1][0] - box[0][0],box[1][1] - box[0][1]))
            edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

            usedEdge = edge1
            if cv.norm(edge2) > cv.norm(edge1):
                usedEdge = edge2


            reference = (1,0) # horizontal edge
            angle = 180.0/math.pi * math.acos((reference[0]*usedEdge[0] + reference[1]*usedEdge[1]) / (cv.norm(reference) *cv.norm(usedEdge)))
            """
            
            if 20000 > area > 1000:
                cv.drawContours(img, [box], 0, color_blue, 2)
                cv.circle(img, center, 5, color_red, 2)

                isk_X = int(rect[0][0])  # горизонтальная координата
                isk_Y = int(rect[0][1])  # вертикальная координата
                #print('Координаты x' + "\n")
                #print(isk_X)
                #print('Координаты y' + "\n")
                #print(isk_Y)
                print(count)

        cv.imshow('result2', img)
        cv2.imshow('result', thresh)
    except:
        cap.release()
        raise


    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()
