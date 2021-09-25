import torch
from libs import Car
import cv2
from rich.console import Console

console = Console()

# Model setup
model = torch.load("/Models/3_0-07Steer 5E 42BS LR0-0001 gpu.pth")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Car setup
CAR = Car.Car((32), (11, 13, 33, True), (31, 29, 33, True))
CAR_SPEED = 87
CAR_STEER = 0.5

# Camera setup
camera = cv2.VideoCapture(0, cv2.CAP_V4L)
# Camera image settings
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv2.CAP_PROP_EXPOSURE, -4)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
camera.set(cv2.CAP_PROP_BUFFERSIZE,1)


DRIVING = True

while DRIVING:
    # ********** IMAGE PROCCESSING ********** #
    #ret, frame = camera.read()
    ret,frame = camera.retrieve(camera.grab())
    input_img = torch.from_numpy(frame)
    output = model(input_img)
    console.log(output.shape)
    output = torch.reshape(output,(-1,))
    console.log(output.shape)
    console.log(output)

    CAR.update_car(output.item(), CAR_SPEED)


