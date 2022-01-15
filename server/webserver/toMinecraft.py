import socket
import os

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('127.0.0.1', 15555))
try:
    while True:
        socket.listen(5)
        client, address = socket.accept()

        response = client.recv(255)
        if response != "":
            os.system("echo '" + str(response, 'UTF-8') + "'")
except KeyboardInterrupt:
    client.close()
    socket.close()
