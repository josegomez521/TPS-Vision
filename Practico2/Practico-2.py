import cv2

imagen = cv2.imread('Lenna.png',0)
imagenorig = imagen.copy()

umbral = 150


for i in range(len(imagen)):
    for f in range(len(imagen[0])):
         if imagen[f][i] <= umbral:
             imagen[f][i] = 0
         else:
             imagen[f][i] = 255


cv2.imshow('imagen',imagen)
cv2.imshow('imagen original',imagenorig)
cv2.imwrite('resultado-tp2.png ',imagen)

"""
imagen2 = cv2.imread('Lenna.png', 0)
_, binarizada = cv2.threshold(imagen2, 150, 255, cv2.THRESH_BINARY)
cv2.imshow('Binary',binarizada)
"""

cv2.waitKey(0)