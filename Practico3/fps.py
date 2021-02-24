
import cv2

"""import sys

if (len(sys.argv)>1):
    filename = sys.argv[1]
else:
    print('Pass a filename as first argument')
    sys.exit(0)"""

cap = cv2.VideoCapture('Video.mp4')
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
fps = int(cap.get(cv2.CAP_PROP_FPS))
resolucion = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

print('Fps =',fps)
print('Resolución =',resolucion)
out = cv2.VideoWriter('output.mp4v', fourcc, fps, resolucion)

delay = int(1000/fps)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(gray)
        cv2.imshow('Image gray', gray)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
    else:
        break


cap.release()
out.release()
cv2.destroyAllWindows()