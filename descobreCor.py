import cv2 as cv
import numpy as np
camera = cv.VideoCapture(0, cv.CAP_DSHOW)


def nothing(param):
    pass


cv.namedWindow("result")
cv.createTrackbar("h", 'result', 0, 179, nothing)
cv.createTrackbar("s", 'result', 0, 255, nothing)
cv.createTrackbar("v", 'result', 0, 255, nothing)

while 1:
    _, frame = camera.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    h = cv.getTrackbarPos("h", "result")
    s = cv.getTrackbarPos("s", "result")
    v = cv.getTrackbarPos("v", "result")
    lower = np.array([h, s, v])
    upper = np.array([255, 255, 255])

    mask = cv.inRange(hsv, lower, upper )
    cv.imshow("Mask", mask)

    print(h, s, v)
    cv.imshow("result", frame)
    k = cv.waitKey(60)
    if k == 27:
        break

camera.release()
cv.destroyAllWindows()
