import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import sys


filename = sys.argv[1]

img = cv2.imread(filename)

d = 1024 / img.shape[1]
dim = (1024, int(img.shape[0] * d))
resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

img_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

blur_img = cv2.GaussianBlur(img_gray,(35,35), 0)


circles = cv2.HoughCircles(blur_img,cv2.HOUGH_GRADIENT,1,120,param1=40,param2=35, minRadius=50, maxRadius=160)

circles_color = []
for i in circles[0, :]:
    x = int(i[0])
    y = int(i[1])
    d = int(i[2])
    roi = resized[y - d:y + d, x - d:x + d]

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    avg_hsv_per_row = np.average(hsv, axis=0)
    avg_hsv = np.average(avg_hsv_per_row, axis=0)

    if (avg_hsv[2] > 140):
        hsv[:, :, 2] -= 40
        img2 = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        plt.imshow(img2[:, :, ::-1])
        plt.show()
        avg_color_per_row = np.average(img2, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        circles_color.append(avg_color)


    else:
        plt.imshow(roi[:, :, ::-1])
        plt.show()
        avg_color_per_row = np.average(roi, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        circles_color.append(avg_color)


resized_withcircle = resized.copy()

for i in circles[0,:]:
    cv2.circle(resized_withcircle,(i[0],i[1]),i[2],(0,200,0),10)

plt.imshow(resized_withcircle[:,:,::-1])
plt.show()

found_coin_values = 0
found_coins = [0, 0, 0, 0, 0, 0]
coins = [5, 10, 20, 50, 100, 200]
z = 0
b = 80
for i in circles[0, :]:
    if (i[2] <= 130 and circles_color[z][0] < b):
        found_coin_values += 5
        found_coins[0] += 1
    elif (i[2] > 130 and i[2] <= 140 and circles_color[z][0] < b):
        found_coin_values += 100
        found_coins[4] += 1
    elif (i[2] > 144 and i[2] <= 158 and circles_color[z][0] < b):
        found_coin_values += 20
        found_coins[2] += 1
    elif (i[2] > 158 and circles_color[z][0] < b):
        found_coin_values += 200
        found_coins[5] += 1
    elif (i[2] > 135 and i[2] <= 150):
        found_coin_values += 10
        found_coins[1] += 1
    elif (i[2] > 150 and i[2] <= 160):
        found_coin_values += 50
        found_coins[3] += 1

    z = z + 1



print("A ", filename, " fájlban a feltalált érmék darab száma: ", circles.shape[1],
      "a feltalált érmék kiszámított összértéke pedig", found_coin_values, ".")
print ("A feltalált érmék:")
z = 0
for i in found_coins:
    print( i, " db.", coins[z], "Ft-os")
    z = z + 1
