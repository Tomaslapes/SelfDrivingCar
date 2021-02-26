from libs import Steer
import time

steer = Steer.Steer(32)

time.sleep(1)
steer.steer(0.0)
time.sleep(1)
steer.steer(1.0)
time.sleep(1)
steer.steer(0.1)
time.sleep(1)
steer.steer(0.2)
time.sleep(1)
steer.steer(0.3)
time.sleep(1)
steer.steer(0.4)
time.sleep(1)
steer.destroy()