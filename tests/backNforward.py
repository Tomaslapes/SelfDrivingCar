from libs import MotorControl,Steer
import time

steer = Steer.Steer(32)
testMotor = MotorControl.Motor(11,13,33,True)
testMotor2 = MotorControl.Motor(31,29,33,True)

steer.steer(0.48)
SPEED = 100

while True:
    testMotor.turn_on(-1,speed=SPEED)
    testMotor2.turn_on(-1,speed=SPEED)
    time.sleep(1)
    testMotor.motor_stop()
    testMotor2.motor_stop()
    time.sleep(1.5)
    testMotor.turn_on(1,speed=SPEED)
    testMotor2.turn_on(1,speed=SPEED)
    time.sleep(1)
    testMotor.motor_stop()
    testMotor2.motor_stop()
    time.sleep(1.5)    

    

