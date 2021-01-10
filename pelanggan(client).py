from socket import *



pelayanName = "192.168.1.27"
pelayanPort = 8080

pelangganSocket = socket(AF_INET, SOCK_STREAM)

pelangganSocket.connect((pelayanName, pelayanPort))

message = clientSocket.recv(1024)  # for welcome and authentication info
print message
