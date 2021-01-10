from socket import *

    def __init__(self, serverPort, serverName):
        try:
            serverSocket = socket(AF_INET, SOCK_STREAM)
        except:
            print "Socket cannot be created"
            exit(1)

        print "Socket is created"
        try:
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:
            print "Socket cannot be used"
            exit(1)
        print "Socket is being used"
        try:
            serverSocket.bind((serverName, serverPort))
        except:
            print "Binding cannot de done"
            exit(1)
        print "Binding is done"
        try:
            serverSocket.listen(45)
        except:
            print "Server cannot listen!"
            exit(1)
        print "Server is ready to receive"

        while True:
            connectionSocket, addr = serverSocket.accept()

            threading.Thread(target=self.listenToClient, args=(connectionSocket, addr)).start()
