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
        CAR_SPEED = (int(value)/MAX_VALUE)*100
        CAR.update_car(CAR_STEER, int(CAR_SPEED))
        sleep(0.1)

    def on_L3_down(self,value):
        CAR_SPEED = (int(value)/MAX_VALUE)*100
        CAR.update_car(CAR_STEER, int(CAR_SPEED))
        sleep(0.1)

PS4_CONTROLLER = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
PS4_CONTROLLER.listen(timeout=100)