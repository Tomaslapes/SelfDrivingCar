from libs import MotorControl
import time
import math

testMotor = MotorControl.Motor(11,13,33,True,pwm_freq=50)
#testMotor2 = MotorControl.Motor(29,31,32,True)

for i in range(0,100):
    testMotor.turn_on(1,i)
    #testMotor2.turn_on(1,i)
    time.sleep(0.15)


testMotor.turn_on(1,1)
#testMotor2.turn_on(1,100)
time.sleep(2)
testMotor.turn_on(1,2)
time.sleep(2)
testMotor.turn_on(1,3)
time.sleep(2)
testMotor.turn_on(1,4)