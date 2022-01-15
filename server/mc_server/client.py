
import socket

hote = "localhost"
port = 15555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))

socket.send(b"Hey my name is Olivier!")

socket.close()
