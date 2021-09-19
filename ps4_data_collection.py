from libs import Car
from pyPS4Controller.controller import Controller
from secrets import token_hex
import cv2
from os.path import join
import csv

# Car setup
CAR = Car.Car((32), (11, 13, 33, True), (31, 29, 33, True))
CAR_SPEED = 0
CAR_STEER = 0.0
# Controller setup
MAX_VALUE = 32767
# File setup
DATA_DIR = "/DATA/SelfDrivingCar/"


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_L3_up(self,value):
        global CAR_STEER, CAR_SPEED
        CAR_SPEED = (int(value)/MAX_VALUE)*-100
        CAR.update_car(float(CAR_STEER), int(CAR_SPEED))

    def on_L3_down(self,value):
        global CAR_STEER, CAR_SPEED
        CAR_SPEED = (int(value)/MAX_VALUE)*-100
        CAR.update_car(float(CAR_STEER), int(CAR_SPEED))

    def on_L2_press(self, value):
        global CAR_STEER, CAR_SPEED
        CAR_STEER = -1*((int(value)*-1/(MAX_VALUE*2))-0.5)
        print(CAR_STEER)
        CAR.update_car(float(CAR_STEER),CAR_SPEED )

    def on_circle_press(self):
        # Save the image and steering angle
        # Generate a random alphanumeric token for the name of the file
        file_name = join(DATA_DIR,token_hex(nbytes=16)+".jpg")
        # Camera setup
        camera = cv2.VideoCapture(0, cv2.CAP_V4L)
        ret, frame = camera.read()
        frame = cv2.resize(frame,(500,500))
        cv2.imwrite(file_name,frame)
        with open("data.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([file_name,CAR_STEER])
        camera.release()
        print("X pressed")

PS4_CONTROLLER = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
PS4_CONTROLLER.listen(timeout=100)

