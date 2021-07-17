from libs import Car
from pyPS4Controller.controller import Controller
from time import sleep

# Car setup
CAR = Car.Car((32), (11, 13, 33, True), (31, 29, 33, True))
CAR_SPEED = 0
CAR_STEER = 0.0
# Controller setup
MAX_VALUE = 32767

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
        CAR_STEER = -1*((int(value)/(MAX_VALUE*2))-0.5)
        print(CAR_STEER)
        CAR.update_car(float(CAR_STEER),CAR_SPEED )

    #def on_L3_right(self, value):
    #    CAR_STEER = -1*((int(value)/(MAX_VALUE*2)) -0.5)
    #    print(CAR_STEER)
    #    CAR.update_car(float(CAR_STEER),CAR_SPEED)

PS4_CONTROLLER = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
PS4_CONTROLLER.listen(timeout=100)
