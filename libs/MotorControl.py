from typing import ByteString
from Jetson.GPIO.gpio import PWM
import RPi.GPIO as GPIO
import time

class Motor:
    """The Motor class simplifies the control of a single motor.
    
    To initialize provide pin1 and pin2 for the Motor connections.
    Methods:
        turn_on -> to turn on the motor and spin it in a provided direction.
        motor_stop -> stops the motor.
        destroy -> cleans up the GPIO pins.
    """

    def __init__(self, pin_a, pin_b,pwm_pin = None,speed_control = False,pwm_freq = 2000):
        """Initialize the motor pins and set them as outputs
        
        set speed_control to True to be able to modify motor speed
        (when this is enabled a pwm_pin needs to be also provided)
        a default frequency of 2000 is used.
        """

        self.pin_a = pin_a
        self.pin_b = pin_b
        self.speed_control = speed_control
        if self.speed_control == True:
            if pwm_pin != 33 and pwm_pin != 32:
                print("Invalid GPIO pin: this pin does not support PWM")
                raise Exception
            self.pwm_pin = pwm_pin
        self.direction = None
        self.speed = None

        # Setup the pins as outputs
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_a, GPIO.OUT, initial= GPIO.LOW)
        GPIO.setup(self.pin_b, GPIO.OUT, initial= GPIO.LOW)
        if self.speed_control == True:
            GPIO.setup(self.pwm_pin, GPIO.OUT, initial= GPIO.LOW)
            self.pwm = GPIO.PWM(self.pwm_pin,pwm_freq)
            self.pwm.start(100) # the pwm is reversed in this case thus 100 will mean the motor is off
        print(f"Motor({self.pin_a},{self.pin_b}) initialized succesfully!")

    # Direction is "cv" or "ccv" or a int 1 or -1 
    def turn_on(self,direction,speed = 100):
        """Direction-> is "cv" or "ccv" or a int 1 or -1. 
        Speed-> is a int value from 0(off) up to 100(full speed).
        
        Turns the motor ON spinning in the set direction. 
        THIS TOGGLES THE MOTOR ON AND IT HAS TO BE TURNED OFF MANUALLY! 
        """
        self.speed = (speed*-1)+100 # inverts the speed because of how the pwm is wired 
        if isinstance(direction,str):# Checks if direction is a string
            print(direction)
            if direction == "cv":
                self.direction = 1
            if direction == "ccv":
                self.direction = -1
        else:
            self.direction = direction

        if self.direction == 1:
            GPIO.output(self.pin_a,GPIO.LOW)
            GPIO.output(self.pin_b,GPIO.HIGH)
            if self.speed_control: # only set the speed if speed control is used
                self.pwm.ChangeDutyCycle(self.speed)
        else:
            GPIO.output(self.pin_a,GPIO.HIGH)
            GPIO.output(self.pin_b,GPIO.LOW)
            if self.speed_control: # only set the speed if speed control is used
                self.pwm.ChangeDutyCycle(self.speed)

        print(f"Motor({self.pin_a},{self.pin_b}) on | dir={self.direction} | speed={speed}")

    def motor_stop(self):
        """Stops the motor."""

        GPIO.output(self.pin_a, GPIO.LOW)
        GPIO.output(self.pin_b, GPIO.LOW)
        if self.speed_control: # only set the motor speed to 0 if speed control is used
            self.pwm.ChangeDutyCycle(0)

        print(f"Motor({self.pin_a},{self.pin_b}) off")

    def destroy(self):
        """Cleans up the GPIO pins."""

        try:
            self.motor_stop()
            GPIO.cleanup(self.pin_a)
            GPIO.cleanup(self.pin_b)
            GPIO.cleanup(self.pwm_pin)
            print("Motor destroyed -> pins released")
        except e:
            print(e)

    def __del__(self):
        self.destroy()

# Test
# testMotor = Motor(11,13)
# testMotor2 = Motor(19,21)
# time.sleep(1)
# testMotor.turn_on(1)
# testMotor2.turn_on(1)
# time.sleep(1)
# testMotor.turn_on(-1)
# testMotor2.turn_on(-1)
# time.sleep(1)
# testMotor.turn_on(1)
# testMotor2.turn_on(1)
# time.sleep(1)
# testMotor.turn_on(-1)
# testMotor2.turn_on(-1)
# time.sleep(1)
# testMotor.motor_stop()
# testMotor2.motor_stop()
# time.sleep(1)
# testMotor.destroy()
# testMotor2.destroy()

