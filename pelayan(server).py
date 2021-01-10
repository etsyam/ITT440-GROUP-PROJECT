from socket import *

    def __init__(self, serverPort, serverName):
        try:
            serverSocket = socket(AF_INET, SOCK_STREAM)
        except:
            print "Socket tidak berjaya"
            exit(1)

        print "Socket berjaya"
        try:
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:
            print "Socket tidak boleh diguna"
            exit(1)
        print "Socket sedang diguna"
        try:
            serverSocket.bind((serverName, serverPort))
        except:
            print "Tidak boleh bind"
            exit(1)
        print "Bind berjaya"
        try:
            serverSocket.listen(40)
        except:
            print "Server cannot listen!"
            exit(1)
        print "Server is ready to receive"

        while True:
            connectionSocket, addr = serverSocket.accept()

            threading.Thread(target=self.listenToClient, args=(connectionSocket, addr)).start()
