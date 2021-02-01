import socket

# Server Address
IP = socket.gethostbyname(socket.gethostname())
PORT = 5420
ADDR = (IP, PORT)

# Communication settings
HEADER = 10

# Ques
COMMAND_LIST = []

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(ADDR)
print(f"[STATUS] Server successfully boud to IP: {ADDR[0]}:{ADDR[1]}")
server_socket.listen()
print(f"[STATUS] Server is listening to incoming connections!")

SERVER_ONLINE = True

while SERVER_ONLINE:
    client_socket, client_addr = server_socket.accept()
    print(f"[INFO] New connection from address {client_addr} established!")
    while client_socket:
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
print("Server shutdown!")
    


