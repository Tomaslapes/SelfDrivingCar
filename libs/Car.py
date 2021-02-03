from libs import Steer
from libs import MotorControl


class Car():
    def __init__(self, steer, motor_1, motor_2):
        self.steer = Steer.Steer(steer)
        self.motor_1 = MotorControl.Motor(
            motor_1[0], motor_1[1], motor_1[2], motor_1[3])
        self.motor_2 = MotorControl.Motor(
            motor_2[0], motor_2[1], motor_2[2], motor_2[3])
        self.SPEED = 0
        self.STEER = 0.0

    def update_car(self, steer, speed):
        self.steer.steer(steer)

        if speed == 0:
            self.motor_1.motor_stop()
            self.motor_2.motor_stop()
            return
        dir = 1
        if speed < 0:
            dir = -1
        self.motor_1.turn_on(dir, speed=self.SPEED)
        self.motor_2.turn_on(dir, speed=self.SPEED)
