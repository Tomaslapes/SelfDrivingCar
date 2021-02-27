from libs import Car
import cv2

# Car setup
#CAR = Car.Car((32), (11, 13, 33, True), (31, 29, 33, True))

# Camera setup
camera = cv2.VideoCapture(0, cv2.CAP_V4L)
#ret, frame = camera.read()
# Camera exposure settings
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv2.CAP_PROP_EXPOSURE, 5)

# Threshold settings
LOWER_LIMIT = 170
UPPER_LIMIT = 255

# Navigation settings
CONTROL_POINTS = [
    0.1, 0.15, 0.2,
    0.25, 0.3, 0.45,
    0.6, 0.75, 0.90
]
SMOOTH_DIST = 10

DRIVING = True

while DRIVING:
    # ********** IMAGE PROCCESSING ********** #
    
    #ret, frame = camera.read()
    status, frame = camera.retrieve(camera.grab())

    frame = cv2.resize(frame,(320,180))
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _thresh, threshold_image = cv2.threshold(
        gray_scale, LOWER_LIMIT, UPPER_LIMIT, cv2.THRESH_BINARY)
    print("Start")
    locations = []
    for y, row in enumerate(threshold_image):

        indices = [int(threshold_image.shape[1]/2)]
        for x, value in enumerate(row):
            if value == 255:
                indices.append(x)

        locations.append(indices[int(len(indices)/2)])

        # TODO DEBUG - remove later
        #frame = cv2.circle(
        #    frame, (indices[int(len(indices)/2)], y), radius=2, color=(15, 15, 230), thickness=-1)
        # DEBUG - remove later

    # ********** Point calculations ********** #
    control_points_list = []
    for control_point in CONTROL_POINTS:
        point_index = int(len(locations)*control_point)
        smoothing_window = locations[point_index -
                                     SMOOTH_DIST:point_index+SMOOTH_DIST]
        _sum = int(sum(smoothing_window)/len(smoothing_window))
        control_points_list.append((_sum, point_index))
        #frame = cv2.circle(
        #    frame, (_sum, point_index), radius=8, color=(65, 230, 15), thickness=-1)
    # TODO DEBUG - remove later
    #frame = cv2.line(
    #    frame, (int(frame.shape[1]/2), 0), (int(frame.shape[1]/2), frame.shape[0]), color=(255, 0, 0), thickness=2)
    #frame = cv2.line(
    #    frame, (int(frame.shape[1]/2), control_points_list[5][1]), control_points_list[5], color=(255, 0, 0), thickness=2)
    # DEBUG - remove later

    point_distance = control_points_list[5][0]-int(frame.shape[1]/2)

    _steer_max = int(frame.shape[1]/2)
    steer_value = ((point_distance / _steer_max) / 2)+0.5

    # TODO DEBUG - remove later
    print("Steer value: ", steer_value)
    print("End-computation")
    print("start show")
    cv2.imshow('video bw', threshold_image)
    cv2.imshow('video original', frame)
    print("end show")
    #CAR.update_car(steer_value, 0)
    
    if cv2.waitKey(1) == 27:
        break
    # DEBUG - remove later
