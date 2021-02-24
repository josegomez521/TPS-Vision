import cv2
import numpy as np



def clics(event, x, y, flags, param):
    global puntos, transformar, imagen1

    if transformar == True:

        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(imagen1, (x, y), 5, (0, 255, 0), -1)
            puntos.append([x, y])

            if len(puntos) == 3:       #Si ya tengo 3 puntos llamo a la función transformación
                transformacionafin(puntos)
                transformar = False    #deshabilito la función clics a realizar la transformación, hasta que se presione 'h'
                imagen1 = aux.copy()           #Restauro la imagen original
                puntos = []            #Restauro puntos


def transformacionafin (puntos1):

    pts1 = np.float32([[0, 0], [ancho2, 0], [0, alto2]])
    pts2 = np.float32([puntos1])

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(imagen2, M, (ancho1, alto1))

    # Máscara

    imagenblanco = 255*np.ones((alto2, ancho2, 3), dtype=np.uint8)
    alpha = cv2.warpAffine(imagenblanco, M, (ancho1, alto1))
    alpha = alpha.astype(float) / 255.0 # Normalizo la máscara alfa para mantener la intensidad entre 0 y 1

    imagen1 = np.array(dst * alpha + aux * (1 - alpha), dtype=np.uint8)

    cv2.imshow('Blend', imagen1)


puntos = []
imagen1 = cv2.imread('imagen1.png')
imagen2 = cv2.imread('imagen2.png')

ancho1= imagen1.shape[1]  # columnas
alto1 = imagen1.shape[0]  # filas
ancho2= imagen2.shape[1]  # columnas
alto2 = imagen2.shape[0]  # filasa

aux = imagen1.copy()
cv2.namedWindow('Imagen1')
cv2.setMouseCallback('Imagen1', clics)
transformar = False

while True:

    cv2.imshow('Imagen1', imagen1)
    cv2.imshow('Imagen2', imagen2)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('a'):
        cv2.destroyWindow('Blend')    #cierro la ventana blend que podría estar abierta en un evento anterior
        transformar = True          #Habilito a que la función de eventos del mouse pueda realizar la transformación


    elif k == ord('q'):
        break

cv2.destroyAllWindows()