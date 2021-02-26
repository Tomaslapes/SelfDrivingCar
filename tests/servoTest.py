from Jetson.GPIO.gpio import PWM
import RPi.GPIO as GPIO
import time

def servoDutyCycle(pulse_ms, freq = 50):
    period_ms = 1.0 / freq * 1000.0
    duty_cycle = int(pulse_ms/(period_ms/65535.0))
    return duty_cycle

GPIO.setmode(GPIO.BOARD)

GPIO.setup(32, GPIO.OUT, initial= GPIO.LOW)

pwm = GPIO.PWM(32,frequency_hz = 50)
pwm.start(5)

time.sleep(1)
#duty = 4.0

pwm.ChangeDutyCycle(4)
time.sleep(2)
pwm.ChangeDutyCycle(8)
time.sleep(2)
pwm.ChangeDutyCycle(4)
time.sleep(2)
pwm.ChangeDutyCycle(8)
time.sleep(2)
pwm.ChangeDutyCycle(4)
time.sleep(2)
pwm.ChangeDutyCycle(8)
time.sleep(2)
pwm.ChangeDutyCycle(5.5)
time.sleep(2)
#while duty <= 11.0:
#    pwm.ChangeDutyCycle(duty)
#    time.sleep(0.1)
#    duty += 0.1



pwm.ChangeDutyCycle(6)
time.sleep(1)
pwm.stop()

GPIO.cleanup()