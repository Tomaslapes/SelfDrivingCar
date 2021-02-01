from libs import MotorControl
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)
myPwm =GPIO.PWM(33,2000)
myPwm.start(0)

testMotor = MotorControl.Motor(11,13)
time.sleep(1)
testMotor.turn_on("cv")
time.sleep(5)
testMotor.turn_on("ccv")
time.sleep(5)

myPwm.ChangeDutyCycle(50)

time.sleep(1)
testMotor.turn_on("cv")
time.sleep(5)
testMotor.turn_on("ccv")
time.sleep(5)

testMotor.motor_stop()
testMotor.destroy()
