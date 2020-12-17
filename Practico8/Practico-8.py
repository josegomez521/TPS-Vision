import cv2
import numpy as np


def clics(event, x, y, flags, param):
    global puntos, transformar, imagen

    if transformar == True:

        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(imagen, (x, y), 5, (0, 0, 255), -1)
            puntos.append([x, y])

            if len(puntos) == 4:       #Si ya tengo 4 puntos llamo a la función transformación
                transformacion(puntos)
                transformar = False    #deshabilito la función clics a realizar la transformación, hasta que se presione 'h'
                imagen = aux.copy()           #Restauro la imagen original
                puntos = []            #Restauro puntos


def transformacion (puntos1):
    pts1 = np.float32([puntos1])
    pts2 = np.float32([[0, 0], [556, 0], [0, 562], [556, 562]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(imagen, M, (556, 562))
    cv2.imshow('dst', dst)


puntos = []
imagen = cv2.imread('vent.dist.persp.jpg')
aux = imagen.copy()
cv2.namedWindow('Imagen')
cv2.setMouseCallback('Imagen', clics)
transformar = False

while True:

    cv2.imshow('Imagen', imagen)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('h'):
        cv2.destroyWindow('dst')    #cierro la ventana destino que podría estar abierta en un evento anterior
        transformar = True          #Habilito a que la función de eventos del mouse pueda realizar la transformación

    elif k == ord('q'):
        break

cv2.destroyAllWindows()