import RPi.GPIO as GPIO
import time

ENA = 15
motor_A_1 = 11
motor_A_2 = 13

GPIO.setmode(GPIO.BOARD)

GPIO.setup(ENA, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(motor_A_1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(motor_A_2, GPIO.OUT, initial = GPIO.LOW)



for i in range(0,5):
    GPIO.output(ENA,GPIO.HIGH)
    GPIO.output(motor_A_1,GPIO.LOW)
    GPIO.output(motor_A_2,GPIO.LOW)
    print("Low Low")
    time.sleep(2)
    GPIO.output(ENA,GPIO.HIGH)
    GPIO.output(motor_A_1,GPIO.HIGH)
    GPIO.output(motor_A_2,GPIO.LOW)
    print("High Low")
    time.sleep(2)
    GPIO.output(ENA,GPIO.HIGH)
    GPIO.output(motor_A_1,GPIO.LOW)
    GPIO.output(motor_A_2,GPIO.HIGH)
    print("Low High")
    time.sleep(2) 

GPIO.output(ENA,GPIO.LOW)
GPIO.output(motor_A_1,GPIO.LOW)
GPIO.output(motor_A_2,GPIO.LOW)

GPIO.cleanup()