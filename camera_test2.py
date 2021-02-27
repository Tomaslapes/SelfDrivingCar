import cv2
from time import sleep


# Camera setup
camera = cv2.VideoCapture(0, cv2.CAP_V4L)
# Camera exposure settings
camera.set(cv2.CAP_PROP_FPS,25)
#camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
#camera.set(cv2.CAP_PROP_EXPOSURE, -5)

while True:
    # ********** IMAGE PROCCESSING ********** #
    ret, frame = camera.read()
    frame = cv2.resize(frame,(640,360))
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _thresh, threshold_image = cv2.threshold(
        gray_scale, 170, 255, cv2.THRESH_BINARY)

    print(threshold_image.shape)
    cv2.imshow('video bw', threshold_image)
    cv2.imshow('video original', frame)

    if cv2.waitKey(1) == 27:
        break
    # DEBUG - remove later