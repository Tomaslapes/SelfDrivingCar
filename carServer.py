import socket
import cv2
import pickle
import threading

# Server Address
IP = "192.168.15.15"  # socket.gethostbyname(socket.getfqdn())
PORT = 5420
ADDR = (IP, PORT)

# Communication settings
HEADER = 10
# Camera setup
cam = cv2.VideoCapture(0)

# Ques
COMMAND_LIST = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(ADDR)
print(f"[STATUS] Server successfully boud to IP: {ADDR[0]}:{ADDR[1]}")
server_socket.listen()
print(f"[STATUS] Server is listening to incoming connections!")

SERVER_ONLINE = True


def send_camera_feed():
    while True:
        ret, frame = cam.read()
        encoded_image = pickle.dump(frame)
        padded_msg = bytes(
            f"{len(encoded_image):<{HEADER}}", "utf-8") + encoded_image
        print(len(padded_msg))
        #client_socket.send(padded_msg)


while SERVER_ONLINE:
    client_socket, client_addr = server_socket.accept()
    print(f"[INFO] New connection from address {client_addr} established!")
    while client_socket:
        camera_thread = threading.Thread(target=send_camera_feed, daemon=True)
        try:
            message_init = client_socket.recv(HEADER)
            msg_length = int(message_init)

            message = client_socket.recv(msg_length)
            message = message.decode('utf-8')
            print(message)

        except:
            SERVER_ONLINE = False
            client_socket.shutdown(socket.SHUT_RDWR)
            break

    break

server_socket.close()
cam.release()
print("Server shutdown!")
