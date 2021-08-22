from libs import Car
import cv2

# Car setup
CAR = Car.Car((32), (11, 13, 33, True), (31, 29, 33, True))
CAR_SPEED = 90

# Camera setup
camera = cv2.VideoCapture(0, cv2.CAP_V4L)
# Camera image settings
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv2.CAP_PROP_EXPOSURE, -4)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
camera.set(cv2.CAP_PROP_BUFFERSIZE,1)

# Threshold settings
LOWER_LIMIT = 150
UPPER_LIMIT = 255

# Navigation settings
CONTROL_POINT = 0.45
SMOOTH_DIST = 10

DRIVING = True

while DRIVING:
    # ********** IMAGE PROCCESSING ********** #
    #ret, frame = camera.read()
    ret,frame = camera.retrieve(camera.grab())
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _thresh, threshold_image = cv2.threshold(
        gray_scale, LOWER_LIMIT, UPPER_LIMIT, cv2.THRESH_BINARY)

    locations = []
    img_slice = threshold_image[(int(frame.shape[0]*CONTROL_POINT) -
                                 SMOOTH_DIST):(int(frame.shape[0]*CONTROL_POINT)+SMOOTH_DIST)]
    for y, row in enumerate(img_slice):

        indices = [int(img_slice.shape[1]/2)]
        for x, value in enumerate(row):
            if value == 255:
                indices.append(x)

        locations.append(indices[int(len(indices)/2)])

        # TODO DEBUG - remove later
        frame = cv2.circle(
            frame, (indices[int(len(indices)/2)], y + int(frame.shape[0]*CONTROL_POINT)), radius=2, color=(15, 15, 230), thickness=-1)
        # DEBUG - remove later

    # ********** Point calculations ********** #
    control_points_list = []
    point_index = int(len(locations)/2)
    smoothing_window = locations[point_index -
                                 SMOOTH_DIST:point_index+SMOOTH_DIST]

    _sum = int(sum(smoothing_window)/len(smoothing_window))
    control_points_list.append((_sum, point_index))

    # TODO DEBUG - remove later
    _circle_y = point_index+int(frame.shape[0]*CONTROL_POINT)
    frame = cv2.circle(
        frame, (_sum,_circle_y), radius=8, color=(65, 230, 15), thickness=-1)
    # DEBUG - remove later

    # TODO DEBUG - remove later
    frame = cv2.line(
        frame, (int(frame.shape[1]/2), 0), (int(frame.shape[1]/2), frame.shape[0]), color=(255, 0, 0), thickness=2)
    frame = cv2.line(
        frame, (int(frame.shape[1]/2), _circle_y), (control_points_list[0][0],_circle_y), color=(255, 0, 0), thickness=2)
    # DEBUG - remove later

    point_distance = control_points_list[0][0]-int(frame.shape[1]/2)

    _steer_max = int(frame.shape[1]/2)
    steer_value = ((point_distance / _steer_max) / 2)+0.5

    # TODO DEBUG - remove later
    #print("Steer value: ", steer_value)

    cv2.imshow('video bw', threshold_image)
    cv2.imshow('video original', frame)
    # DEBUG - remove later
    CAR.update_car(steer_value, CAR_SPEED)

    if cv2.waitKey(1) == 27:
        break
    
