import matplotlib.pyplot as plt
import cv2
import numpy as np

videoPath = 'Computer-Vision/OpenCV_TESTS/images/test_video.mp4'


def roi(img, vertices):
    mask = np.zeros_like(img)
    # channelCount = img.shape[2]
    # match_mask_color = (255,)*channelCount
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    maskedImage = cv2.bitwise_and(img, mask)
    return maskedImage


def drawLines(img, lines):
    img = np.copy(img)
    blankImage = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(blankImage, (x1, y1), (x2, y2),
                     (0, 255, 200), thickness=3)
    img = cv2.addWeighted(img, 0.8, blankImage, 1, 0.0)
    return img


# imgPath = 'Computer-Vision/OpenCV_TESTS/images/endless-road.jpg'
# image = cv2.imread(imgPath)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def process(image):
    height = image.shape[0]
    width = image.shape[1]

    roi_vertices = [
        (0, height),
        (width/2, height/2),
        (width, height)
    ]

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cannyImage = cv2.Canny(gray_image, 100, 120)
    maskedImage = roi(cannyImage, np.array([roi_vertices], np.int32))

    lines = cv2.HoughLinesP(maskedImage, rho=2, theta=np.pi/60, threshold=50,
                            lines=np.array([]), minLineLength=1, maxLineGap=100)

    lineImage = drawLines(image, lines)
    return lineImage


cap = cv2.VideoCapture(videoPath)

while cap.isOpened():
    ret, frame = cap.read()
    frame = process(frame)
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
