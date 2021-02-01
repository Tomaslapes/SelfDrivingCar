from libs import Steer,MotorControl
import time

steer = Steer.Steer(32)
testMotor = MotorControl.Motor(11,13,33,True)
testMotor2 = MotorControl.Motor(31,29,33,True)

steer.steer(0.5)

while True:
    
    testMotor.motor_stop()
    testMotor2.motor_stop()
    steer.steer(0.0)
    time.sleep(1)
    testMotor.turn_on(1)                      
    testMotor2.turn_on(1)
    time.sleep(3)
    testMotor.motor_stop()
    testMotor2.motor_stop()
    steer.steer(1.0)
    time.sleep(1)
    testMotor.turn_on(1)
    testMotor2.turn_on(1)
    time.sleep(3)

    

