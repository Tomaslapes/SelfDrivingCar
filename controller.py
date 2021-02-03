import socket
from ursina import Ursina, Button, color, Text, window, held_keys, Texture, Sprite, Slider, ThinSlider, Entity
from time import sleep
import pickle
import cv2

# Server Address
IP = "192.168.15.15"  # input("IP?: ")
PORT = 5420
ADDR = (IP, PORT)

# Communication settings
HEADER = 10
STEER_SPEED = 0.1
ACCEL = 1
CONNECTED = False

app = Ursina()
window.title = "Car controller"


# contr_socket.connect(ADDR)
#print(f"Succesfully connected to server: {ADDR[0]}:{ADDR[1]}!")

class GeneralButton(Button):
    def __init__(self, text, click_function):
        super().__init__(model="quad", text=f" {text} ", scale=0.2,)
        self.on_click = click_function
        self.fit_to_text(radius=.2)
        self.origin = (0, 9)

    def changeState(self, new_text, new_color=color.azure):
        self.color = new_color
        self.text = new_text


class CameraView(Sprite):
    def __init__(self):
        super().__init__(texture="image.jpg", origin=(0, -0.25), scale=3.0)

    def update(self):  # this method gets called automaticaly by ursina
        self.get_camera_image()  # get the camera image
        self.texture = "image.jpg"  # load the image
        self.texture.apply()  # apply it to the texture to refresh it (wont show othervise)

    def get_camera_image(self):
        frame = self.recieve_data()
        if type(frame) != type(None):

            cv2.imwrite('image.jpg', frame)
            return
        print("Frame is false")
        return

    def recieve_data(self):
        global HEADER
        try:
            message_init = contr_socket.recv(HEADER)
            print(message_init)
            message_len = int(message_init.decode("utf-8"))
            print("hello")
            print(message_len)

            message = contr_socket.recv(message_len)
            image = pickle.loads(message)
            print("\n", image)
            return image
        except Exception as e:
            print(e)
            return None


def connect():
    contr_socket.connect(ADDR)
    connect_button.changeState("Connected!")
    print(f"Successfully connected to server: {ADDR[0]}:{ADDR[1]}!")
    global CONNECTED
    CONNECTED = True


def encode_msg(speed, steer):
    encoded_msg = f"{str(speed)};{str(steer)[:5]}"
    return encoded_msg


def send(msg):
    print(msg)
    padded_msg = f"{len(msg):<{HEADER}}" + msg
    contr_socket.send(padded_msg.encode("utf-8"))


steer_value = 0.0
car_speed = 0


def update():
    global steer_value, car_speed

    if held_keys['a']:
        print(f"Steer LEFT: {steer_value}")
        if steer_value > -1.0:
            steer_value -= STEER_SPEED
    if held_keys['d']:
        print(f"Steer RIGHT: {steer_value}")
        if steer_value < 1.0:
            steer_value += STEER_SPEED
    if held_keys['w']:
        print(f"Move FORWARD: {car_speed}")
        if car_speed < 100:
            car_speed += ACCEL
    if held_keys['s']:
        print(f"Move BACKWARDS: {car_speed}")
        if car_speed > 0:
            car_speed -= ACCEL
    if held_keys["space"]:
        print("STOP!")
        car_speed = 0

    if CONNECTED:
        send(encode_msg(car_speed, steer_value))

    sleep(0.05)


contr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_button = GeneralButton("Connect", connect)
help_text = Text(
    "Use W and S to move forward or backwards.\n Use A and D to steer.\n Press [SPACE] to stop immediately", origin=(0, 3))

# Test Camera setup

#img = Image.open("oldLogo.png")
camera_view = CameraView()

app.run()
