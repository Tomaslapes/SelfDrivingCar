import socket
from ursina import Ursina, Button, color, Text, window, held_keys, Sprite, Slider
from time import sleep
import pickle
import cv2
from pyPS4Controller.controller import Controller


# Controller setup
PS4_CONTROLLER = None


# Server Address
IP = "192.168.15.15"  # input("IP?: ")
PORT = 5420
ADDR = (IP, PORT)

# Communication settings
HEADER = 10
STEER_SPEED = 0.05
ACCEL = 1
SPEED_THR = 50  # Speed threashold for low value compensation
CONNECTED = False

app = Ursina()
window.title = "Car controller"


# contr_socket.connect(ADDR)
#print(f"Succesfully connected to server: {ADDR[0]}:{ADDR[1]}!")

class GeneralButton(Button):
    def __init__(self, text, click_function, origin = (0,9)):
        super().__init__(model="quad", text=f" {text} ", scale=0.2,)
        self.on_click = click_function
        self.fit_to_text(radius=.2)
        self.origin = origin

    def changeState(self, new_text, new_color=color.azure):
        self.color = new_color
        self.text = new_text


class CameraView(Sprite):
    def __init__(self):
        super().__init__(texture="image.jpg", origin=(0, -1), scale=5)

    def update(self):  # this method gets called automaticaly by ursina
        self.get_camera_image()  # get the camera image
        self.texture = "image.jpg"  # load the image
        self.texture.apply()  # apply it to the texture to refresh it (wont show othervise)

    def get_camera_image(self):
        frame = self.recieve_data()
        if type(frame) != type(None):
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('image.jpg', frame)
            return
        # print("No camera data")
        return

    def recieve_data(self):
        global HEADER
        try:
            message_init = contr_socket.recv(HEADER)
            message_len = int(message_init.decode("utf-8"))

            message = contr_socket.recv(message_len)
            image = pickle.loads(message)
            return image
        except Exception as e:
            # print(e)
            return None



class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_L3_up(self,value):
        print("Up: ",value)

    def on_L3_down(self,value):
        print("Down: ",value)


def connect():
    contr_socket.connect(ADDR)
    connect_button.changeState("Connected!")
    print(f"Successfully connected to server: {ADDR[0]}:{ADDR[1]}!")
    global CONNECTED
    CONNECTED = True


def connect_controller():
    if PS4_CONTROLLER != None:
        controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
        controller.listen()
        print("connect controller")


def encode_msg(speed, steer):
    encoded_msg = f"{str(speed)};{str(steer)[:5]}"
    return encoded_msg


def send(msg):
    # print(msg)
    padded_msg = f"{len(msg):<{HEADER}}" + msg
    contr_socket.send(padded_msg.encode("utf-8"))


steer_value = 0.0
car_speed = 0


def update():
    global steer_value, car_speed

    if held_keys['a']:
        #print(f"Steer LEFT: {steer_value}")
        if steer_value > 0.0:
            steer_value -= STEER_SPEED
    if held_keys['d']:
        #print(f"Steer RIGHT: {steer_value}")
        if steer_value < 1.0:
            steer_value += STEER_SPEED
    if held_keys['w']:
        #print(f"Move FORWARD: {car_speed}")
        if car_speed < 100:
            if (car_speed + ACCEL) > 0 and car_speed < SPEED_THR:
                car_speed = SPEED_THR
            car_speed += ACCEL
    if held_keys['s']:
        #print(f"Move BACKWARDS: {car_speed}")
        if car_speed > -100:
            if (car_speed - ACCEL) < 0 and car_speed > -SPEED_THR:
                car_speed = -SPEED_THR
            car_speed -= ACCEL
    if held_keys["space"]:
        # print("STOP!")
        car_speed = 0
    if held_keys["x"]:
        steer_value = 0.5

    Steer_Slider.value = steer_value
    Speed_Slider.value = car_speed

    if CONNECTED:
        send(encode_msg(car_speed, steer_value))

    sleep(0.025)


contr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_button = GeneralButton("Connect to car", connect)
connect_controller = GeneralButton("Connect PS4 controller",connect_controller,origin=(0,7.5))
help_text = Text(
    "Use W and S to move forward or backwards.\n Use A and D to steer.\n Press [SPACE] to stop immediately and X to center the steering.", 
    origin=(0, 4))

# Camera setup
camera_view = CameraView()


def set_speed():
    car_speed = Speed_Slider.value


def set_steer():
    steer_value = Steer_Slider.value


Steer_Slider = Slider(min=-0.0, max=1.0, default=0.0, height=0.05, y=-0.1, x=-0.25,
                      label=Text(origin=(0, 4), text="Steer value"), on_value_changed=set_steer)

Speed_Slider = Slider(min=-100, max=100, default=0.0, height=0.05, y=-0.2, x=-0.25,
                      label=Text(origin=(0, 8), text="Speed"), on_value_changed=set_speed)


app.run()
