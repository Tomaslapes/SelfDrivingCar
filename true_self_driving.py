from rich.console import Console
console = Console()
console.log("[green3]Program starting...")

with console.status("Loading libraries...",spinner="moon"):
    import torch
    import torch.nn as nn
    from torchvision.transforms import Resize
    from torchvision import models
    console.log("[green3]Torch loaded")
    from libs import Car
    import cv2
    console.log("[green3]CV2 loaded")


# Model setup
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with console.status("Started to load the model...",spinner="moon"):
    model = models.resnet18()
    model.fc = nn.Linear(model.fc.in_features,1)
    model.load_state_dict(torch.load("./Models/3_0-07Steer 5E 42BS LR0-0001 gpu_dict.pth"))
    # model.to(DEVICE)
    model.eval()
    console.log("[green3]Model loaded successfully!")

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
camera.set(cv2.CAP_PROP_FRAME_WIDTH,224)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,224)
camera.set(cv2.CAP_PROP_BUFFERSIZE,1)
console.log("[green3]Camera initialized successfully!")


DRIVING = True

with torch.no_grad():
    while DRIVING:
        # ********** IMAGE PROCCESSING ********** #
        #ret, frame = camera.read()
        ret,frame = camera.retrieve(camera.grab())
        console.log("Retrieved a frame")
        input_img = torch.from_numpy(frame)
        # input_img = input_img.to(DEVICE)
        input_img = input_img.transpose(0,2).transpose(1,2)
        input_img.unsqueeze_(0)
        input_img = Resize((244,244))(input_img)
        input_img = input_img.float() / 255.0
        console.log("Image is preped. Shape: ",input_img.shape)

        output = model(input_img)

        console.log(output.shape)
        output = torch.reshape(output,(-1,))
        console.log(output.shape)
        console.log(output)

        CAR.update_car(output.item(), CAR_SPEED)


