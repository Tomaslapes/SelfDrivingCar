from libs import Steer,MotorControl
import time

steer = Steer.Steer(32)
testMotor = MotorControl.Motor(11,13,33,True)
testMotor2 = MotorControl.Motor(31,29,33,True)
steer.steer(0.0)
time.sleep(0.2)
testMotor.turn_on(1)
testMotor2.turn_on(1)

while True:
    print("")
    


