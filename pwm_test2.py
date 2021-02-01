from libs import MotorControl
import time
import math

testMotor = MotorControl.Motor(11,13,33,True)
testMotor2 = MotorControl.Motor(31,29,32,True)

for i in range(0,100):
    testMotor.turn_on(1,i)
    testMotor2.turn_on(1,i)
    time.sleep(0.15)


testMotor.turn_on(1,100)
testMotor2.turn_on(1,100)

time.sleep(2)

testMotor.turn_on(-1,100)
testMotor2.turn_on(-1,100)

time.sleep(2)

testMotor.motor_stop()
testMotor2.motor_stop()

time.sleep(2)

testMotor.turn_on(1,50)
testMotor2.turn_on(1,50)

time.sleep(2)

testMotor.turn_on(-1,50)
testMotor2.turn_on(-1,50)

time.sleep(2) 

