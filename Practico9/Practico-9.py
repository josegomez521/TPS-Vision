import cv2
import numpy as np
import imutils

imagen = cv2.imread('imagen.png')
aux = imagen.copy()
ofx = 45
ofy = 80

cv2.circle(imagen, (65, 129), 4, (255, 0, 0), 2)
cv2.circle(imagen, (307, 167), 4, (0, 255, 0), 2)
cv2.circle(imagen, (34, 383), 4, (0, 0, 255), 2)
cv2.circle(imagen, (302, 401), 4, (255, 255, 0), 2)

pts1 = np.float32([[65, 129], [307, 167], [34, 383], [302, 401]])
pts2 = np.float32([[0+ofx, 0+ofy], [300+ofx, 0+ofy], [0+ofx, 300+ofy], [300+ofx, 300+ofy]])
M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(aux, M, (600, 650))


# Cargo la imágen, la convierto a escala de grises y la desenfoco un poco
gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

#kernel = np.ones((2, 2), np.uint8) #Pobando Kernels

bordes = cv2.Canny(gray, 65, 100)
bordes = cv2.dilate(bordes, None, iterations=1) #Dilatcaion y erosion para cerrar los espacios
bordes = cv2.erode(bordes, None, iterations=1)

cnts = cv2.findContours(bordes.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #encontramos los contornos
cnts = imutils.grab_contours(cnts)
puntos = []

for c in cnts:
   x, y, w, h = cv2.boundingRect(c)
   puntos.append([x, y, w, h])

def medicion (puntos1, m): #Función que calcula el tamaño, dibuja las líneas y escribe los valores

    x1, y1, w1, h1 = puntos1[m]
    cv2.circle(dst, (x1, y1), 5, (0, 200, 0), -1)
    cv2.circle(dst, (x1+w1, y1), 5, (0, 200, 0), -1)
    cv2.circle(dst, (x1, y1+h1), 5, (0, 200, 0), -1)
    cv2.circle(dst, (x1+w1, y1+h1), 5, (0, 200, 0), -1)
    cv2.rectangle(dst, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)

    distancia_pixeles_x = w1
    distancia_pixeles_y = h1
    distancia_mm_x = (distancia_pixeles_x*100)/300
    distancia_mm_y = (distancia_pixeles_y*100)/300

    cv2.putText(dst, "{:.2f} mm".format(distancia_mm_x), ((x1-30)+(distancia_pixeles_x//2), y1-30), 1, 1, (0,0,0), 1, cv2.LINE_AA)
    cv2.line(dst, (x1, y1 - 20), (x1+w1, y1 - 20), (0, 0, 255), 2)
    cv2.line(dst, (x1 + w1, y1 - 30), (x1 + w1, y1 - 10), (0, 0, 255), 2)
    cv2.line(dst, (x1, y1 - 30), (x1, y1 - 10), (0, 0, 255), 2)

    cv2.putText(dst, "{:.2f} mm".format(distancia_mm_y), (x1-10, y1 + (distancia_pixeles_y//2)), 1, 1, (0,0,0), 1, cv2.LINE_AA)
    cv2.line(dst, (x1 - 20, y1), (x1 - 20, y1 + h1), (0, 0, 255), 2)
    cv2.line(dst, (x1 - 30, y1 + h1), (x1 - 10, y1 + h1), (0, 0, 255), 2)
    cv2.line(dst, (x1 - 30, y1), (x1-10, y1), (0, 0, 255), 2)


# Goma m=1
medicion(puntos, 1)

# Moneda m=2
medicion(puntos, 2)

# Tarjeta m=11
medicion(puntos, 13)

# Papel m=12

medicion(puntos, 12)

cv2.imshow('Imagen', imagen)
cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()