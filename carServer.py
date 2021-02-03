import socket
import cv2
import pickle
from time import sleep
# Import custom libraries
from libs import Car


# Server Address
IP = "192.168.15.15"  # socket.gethostbyname(socket.getfqdn())
PORT = 5420
ADDR = (IP, PORT)

# Communication settings
HEADER = 10
# Camera setup
cam = cv2.VideoCapture(0, cv2.CAP_V4L)

# Car setup
CAR = Car.Car((32), (11, 13, 33, True), (31, 29, 33, True))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(ADDR)
print(f"[STATUS] Server successfully boud to IP: {ADDR[0]}:{ADDR[1]}")
server_socket.listen()
print(f"[STATUS] Server is listening to incoming connections!")


def send_camera_feed(cam, HEADER, client_socket):
    print("Send camera data")
    # while True:
    ret, frame = cam.read()
    if type(frame) == type(None):
        frame = None  # np.zeros((10,10))
    img = cv2.resize(frame, (100, 100))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    encoded_image = pickle.dumps(img)
    prefix = bytes(f"{len(encoded_image):<{HEADER}}", "utf-8")
    padded_msg = prefix + encoded_image
    print("Image size: ", len(padded_msg))
    client_socket.send(padded_msg)
    print("send")


SERVER_ONLINE = True

while SERVER_ONLINE:
    client_socket, client_addr = server_socket.accept()
    print(f"[INFO] New connection from address {client_addr} established!")
    #camera_thread = threading.Thread(target=send_camera_feed,args=[cam,HEADER,client_socket], daemon=False)
    # camera_thread.start()
    while client_socket:
        try:
            message_init = client_socket.recv(HEADER)
            msg_length = int(message_init)

            message = client_socket.recv(msg_length)
            message = message.decode('utf-8')
            commands = message.split(";")
            CAR_SPEED = int(commands[0])
            CAR_STEER = float(commands[1])
            CAR.update_car(CAR_STEER, CAR_SPEED)
            print(message)

            send_camera_feed(cam, HEADER, client_socket)

        except Exception as e:
            print(e)
            SERVER_ONLINE = False
            client_socket.shutdown(socket.SHUT_RDWR)
            break

    break


server_socket.close()
cam.release()
print("Server shutdown!")
