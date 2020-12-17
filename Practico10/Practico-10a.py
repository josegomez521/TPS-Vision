import os
import cv2
import glob

#Definimos la resolución que aplicaremos en cornerSubPix, 30 iteraciones y 0.001 de error
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#Creamos un directorio para almacenar aquellas imágenes que reconozca el patrón
dir = 'tmp'
if(not os.path.exists(dir)):
    os.mkdir(dir)
output_file = '{}/{:05}.png'

images = glob.glob('imgDist/*.jpg') #Cargo las imagenes del directorio imgDist en images

counter = 0

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

    if ret is True:
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        img = cv2.drawChessboardCorners(img, (9, 6), corners2, ret)

    cv2.imshow('img', img)

    # Si ret de cada imagen es True y si se presiona 's' guardamos esa imagen (gray) en el directorio dir
    # que se usará para la calibración en Practico-10b

    key = cv2.waitKey(0) & 0xFF
    if(ret is True) and (key == ord('s')):
        cv2.imwrite(output_file.format(dir, counter), gray)
        counter += 1
    if(key == ord('q')):
        break

cv2.destroyAllWindows()