import cv2
import numpy as np

# imgPath = 'Computer-Vision/OpenCV_TESTS/images/korsord.jpg'
imgPath = 'Computer-Vision/OpenCV_TESTS/images/natverksgatan.jpg'
# imgPath = 'Computer-Vision/OpenCV_TESTS/images/road.jpg'

img = cv2.imread(imgPath)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
# cv2.imshow('edges', edges)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100,
                        minLineLength=100, maxLineGap=10)

for line in lines:
    # rho, theta = line[0]
    # a = np.cos(theta)
    # b = np.sin(theta)     # For HoughLines
    # x0 = a*rho
    # y0 = b*rho

    # x1 = int(x0 + 1000*(-b))
    # y1 = int(x0 + 1000*(a))
    # x2 = int(x0 - 1000*(-b))
    # y2 = int(x0 - 1000*(a))

    x1, y1, x2, y2 = line[0]  # HoughLinesP

    cv2.line(img, (x1, y1), (x2, y2), (10, 255, 50), 2)


cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
