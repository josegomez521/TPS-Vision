
import cv2
import numpy as np
import glob

# Dimensiones del tablero de ajedrez
CHECKERBOARD = (9,6)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objpoints = []
imgpoints = []

#Creamos un arreglo donde cada fila va a tener coordenadas de las esquinas en 3D del patrón
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

# Leemos las imagenes del directorio tmp
imagenes = glob.glob('tmp/*.png')

for fname in imagenes:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret == True:

        # Con objpoints y imgpoints creamos las correspondencias de puntos
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)

    cv2.imshow('img', img)
    cv2.waitKey(400)


#Calibramos la cámara pasado los valores de los puntos 3D conocidos (objpoints)
#y las correspondientes coordenadas de píxeles de las esquinas detectadas (imgpoints)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Matriz de la cámara : \n")
print(mtx)
print("dist : \n")
print(dist)
print("rvecs : \n")
print(rvecs)
print("tvecs : \n")
print(tvecs)

# Muestro las imágenes sin calibrar y calibradas aplicando undistort
for fname in imagenes:

   img2 = cv2.imread(fname)
   imagundist = cv2.undistort(img2, mtx, dist, None, None)

   cv2.imshow('Sin calibrar', img2)
   cv2.imshow('Calibrada', imagundist)
   cv2.waitKey(0)

cv2.destroyAllWindows()

