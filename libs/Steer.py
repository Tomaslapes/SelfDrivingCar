from Jetson.GPIO.gpio import PWM
import RPi.GPIO as GPIO
from scipy.interpolate import interp1d
import time

class Steer:
    def __init__(self,pwm_servo_pin,pwm_range = (4.0,8.0)):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pwm_servo_pin, GPIO.OUT, initial= GPIO.LOW)
        self.pwm_servo_pin = pwm_servo_pin

        self.pwm = GPIO.PWM(pwm_servo_pin,frequency_hz = 50)
        self.pwm.start(6.0)
        self.range = pwm_range

    def steer(self,angle):
        """Steer the wheels. Takes an input->[angle] between 0 and 1.0
        
        Instead of the need to specify an precise angle you provide only a value 
        between 0 and 1.0 with 0.5 being the default position. If you want to change
        the range of pwm duty cycles it is possible through an optional variable in the 
        innit method.
        """
        if angle>1.0 or angle<0.0:
            print("Invalid angle provided to the steer function!")
            return
        duty_cycle = (self.range[1]-self.range[0])*angle+self.range[0]
        print(f"Steering to DutyCycle{duty_cycle}") 
        self.pwm.ChangeDutyCycle(duty_cycle)       

    def destroy(self):
        try:
            self.pwm.ChangeDutyCycle(6.0)
            time.sleep(0.2)
            self.pwm.stop()
            GPIO.cleanup(self.pwm_servo_pin)
        except:
            print("Something went wrong trying to destroy the steer object")

    def __del__(self):
        self.destroy()
        
