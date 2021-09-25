from rich.console import Console
console = Console()
console.log("[green3]Program starting...")

with console.status("Loading libraries...",spinner="moon"):
    import torch
    console.log("[green3]Torch loaded")
    from libs import Car
    import cv2
    console.log("[green3]CV2 loaded")


# Model setup

with console.status("Started to load the model...",spinner="moon"):
    model = torch.load("./Models/3_0-07Steer 5E 42BS LR0-0001 gpu.pth")
    console.log("[green3]Model loaded successfully!")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Car setup
CAR = Car.Car((32), (11, 13, 33, True), (31, 29, 33, True))
CAR_SPEED = 87
CAR_STEER = 0.5
console.log("[green3]CAR initialized successfully!")

# Camera setup
camera = cv2.VideoCapture(0, cv2.CAP_V4L)
# Camera image settings
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv2.CAP_PROP_EXPOSURE, -4)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
camera.set(cv2.CAP_PROP_BUFFERSIZE,1)
console.log("[green3]Camera initialized successfully!")


DRIVING = True

while DRIVING:
    # ********** IMAGE PROCCESSING ********** #
    #ret, frame = camera.read()
    ret,frame = camera.retrieve(camera.grab())
    input_img = torch.from_numpy(frame)
    input_img = input_img.transpose(0,2).transpose(1,2)
    input_img.unsqueeze_(0)
    console.log(input_img.shape)

    output = model(input_img.float())

    console.log(output.shape)
    output = torch.reshape(output,(-1,))
    console.log(output.shape)
    console.log(output)

    CAR.update_car(output.item(), CAR_SPEED)


