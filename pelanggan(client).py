from socket import *
import os

#setup class
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

    
pelayanName = "192.168.1.27"
pelayanPort = 8080

pelangganSocket = socket(AF_INET, SOCK_STREAM)

pelangganSocket.connect((pelayanName, pelayanPort))

message = clientSocket.recv(1024) 
print message

while True:

    try:
        jawapan = raw_input('Isi mesej:')

        if message[1:9] == "Soalan":
            soalan2 = raw_input("Simpan jawapan? (Y/N):")

            if soalan0] == 'Y' or jawapan2[0] == 'y':
                pelangganSocket.send(jawapan)
            else:
                print "Ok, berikan jawapan baru!\n"
                continue
        elif jawapan == "exit":
            pelangganSocket.close()
            exit(0)
        else:
            pelangganSocket.send(jawapan)
        cls() 
        message = pelangganSocket.recv(1024)

        print message

    except:
        pelangganSocket.close()
        exit(0)
