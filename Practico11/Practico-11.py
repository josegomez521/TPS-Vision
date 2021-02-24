import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10


img1 = cv2.imread('img22edit.png')
img2 = cv2.imread('img11edit.png')

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Iniciamos el algoritmo SIFT

sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(gray1, None)  # De cada característica me devuelve el descriptor y la escala
kp2, des2 = sift.detectAndCompute(gray2, None)

# creamos el objeto BFMatcher
bf = cv2.BFMatcher(cv2.NORM_L2)

# BFMatcher with default params
matches = bf.knnMatch(des1, des2, k=2)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)

if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

else:
    print("No se encontraron matches - {}/{}".format(len(good), MIN_MATCH_COUNT) )


img3 = cv2.drawMatches(gray1, kp1, gray2, kp2, good, None, flags=2)
plt.imshow(img3), plt.show()

dst = cv2.warpPerspective(img1, M, (640, 480))

alpha = 0.5
blend = np.array(dst * alpha + img2 * (1 - alpha), dtype=np.uint8)

cv2.imshow('1', img1)
cv2.imshow('2', img2)
cv2.imshow('blend', blend)


cv2.waitKey(0)


