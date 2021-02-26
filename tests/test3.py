from libs import MotorControl
import time

testMotor = MotorControl.Motor(11,13)
time.sleep(1)
testMotor.turn_on("cv")
time.sleep(5)
testMotor.turn_on("ccv")
time.sleep(5)
testMotor.motor_stop()
testMotor.destroy()

