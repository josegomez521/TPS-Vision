import cv2
import numpy as np

drawing = False  # true if mouse is pressed
imagen1 = cv2.imread('futb.jpg')
imagen2 = imagen1.copy()               # Utilizo tres imágenes para lograr el efecto de agrandamiento del cuadro
imagen3 = imagen1.copy()
restaurar = imagen1.copy()
angulo = 45
tx = 200
ty = 200


ix, iy = -1, -1
ix2, iy2 = -1, -1
i = -1
M = -1
M2 = -1


def euclidea (angulo1, tx1, ty1, imagenCortada):
    global M, M2, imagenSalida

    ancho = imagen1.shape[1]  # columnas
    alto = imagen1.shape[0]  # filas


    M = np.float32([[1, 0, tx1+ix], [0, 1, ty1+iy]])
    imagenTrasladada = cv2.warpAffine(imagenCortada, M, (ancho, alto))

    centrox = ((ix2-ix)/2) + ix + tx1
    centroy = ((iy2-iy)/2) + iy + ty1
    centro = (centrox, centroy)

    M2 = cv2.getRotationMatrix2D(centro, angulo1, 1)
    imagenSalida = cv2.warpAffine(imagenTrasladada, M2, (ancho, alto))

    cv2.imshow('Imagen de salida', imagenSalida)





def draw(event, x, y, flags, param):
    global ix, iy, drawing, imagen1, imagen2, imagen3, imagenOut, ix2, iy2, i
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            imagen1 = imagen2.copy()  # Cada vez que muevo el mouse, debo dibujar un cuadro nuevo, para ello utilizo una copia de la última imágen utilizada antes de dejar de presionar el botón
            cv2.rectangle(imagen1, (ix, iy), (x, y), (0, 255, 0), 1)
            ix2, iy2 = x, y
            imagen3 = imagen1.copy()  # Guardo la nueva imagen1 para poder utilizarla cuando suelte el botón


    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if iy2 < iy:
            i = iy2
            iy2 = iy
            iy = i

        if ix2 < ix:
            i = ix2
            ix2 = ix
            ix = i

        imagenOut = imagen1[iy:iy2, ix:ix2]  #al soltar el botón guardo en imagenOut el último cuadro seleccionado, para poder mostrarla y guardarla caso de presionar "g"
        imagen2 = imagen3.copy() #Cada cuadro dibujado irá quedando en la imágen principal hasta presionar "r"



cv2.namedWindow('imagen1')
cv2.setMouseCallback('imagen1', draw)

while(1):
    cv2.imshow('imagen1', imagen1)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('e'):
        euclidea(angulo, tx, ty, imagenOut)
        cv2.imwrite('Transformacion Euclidea.png', imagenSalida)

    elif k == ord('r'):
        imagen1 = restaurar
        imagen2 = restaurar
        imagen3 = restaurar
        cv2.destroyWindow("Imagen de salida")

    elif k == ord('q'):
        break

cv2.destroyAllWindows()
