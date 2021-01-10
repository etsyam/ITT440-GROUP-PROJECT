from socket import *
import threading
import time

global i
i = 0

class ThreadedServer():
    def listenToPelanggan(self, pelanggan, addr):
        global i
        while True:
            pelanggan.send("Welcome to the quiz \n") 
            authentication = pelanggan.recv(1024) 

            pelanggan.send("Username: ")
            m1 = pelanggan.recv(1024) 

            name= m1

            pelanggan.send("Enter the passcode: ")
            password = pelanggan.recv(1024) 

            print "Username: ", name
            print "Password: ", password

            file = open("pelajar.txt", "r") 
            str_file = file.read() 

            if str_file.find(name[i]): 
                if str_file.find(password[i]): 
                    
                    pelanggan.send("Successfuly Authenticated!.\n") 
                    file2 = open("attendance.txt", "a")	
                    file2.write(name)
                    file2.write(": yes") 
                    file2.close()

                    localtime1 = time.localtime(time.time())[4] 
                    print "Time->", time.localtime(time.time())[3], ":", time.localtime(time.time())[4] 

                    #Open questions
                    SoalanFile = open("Soalan.txt", "r")
                    Soalan = SoalanFile.read()
                    Soalan = [y for y in (x.strip() for x in Soalan.splitlines()) if y]
                    SoalanFile.close()

                    #Open answers
                    JawapanFile = open("Jawapan.txt","r")
                    Jawapan = JawapanFile.read()
                    Jawapan = [y for y in (x.strip() for x in Jawapan.splitlines()) if y]
                    JawapanFile.close()

                    
                    score = 0
                    for number in range(0, len(Soalan)): 
	                    pelanggan.send(Soalan[number])
	                    Jawapan = pelanggan.recv(1024)
	                    if Jawapan.lower() == Jawapan[number]:
	                    	score = score + 10
                    
	                #get localtime minute value again.
                    localtime2 = time.localtime(time.time())[4]
                    #subtract times.
                    timestamp = localtime2 - localtime1
                    #if>30 time is up.
                    if timestamp > 30:
                        print "Your time is up!\n"
                        pelanggan.close()
                   
                    print name, "Markah: ", str(score), "Markah Bonus: ",  str(10/(timestamp+1)), "Total Markah: ",str(score + 10/(timestamp+1))
            else:
               pelanggan.send("Authentications cannot be done.\n")

            i = i + 1
            file.close()


    def __init__(self, PelayanPort, PelayanName):
        try:
            PelayanSocket = socket(AF_INET, SOCK_STREAM)
        except:
            print "Socket tidak berjaya"
            exit(1)

        print "Socket berjaya"
        try:
            PelayanSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:
            print "Socket tidak boleh diguna"
            exit(1)
        print "Socket sedang diguna"
        try:
            PelayanSocket.bind((PelayanName, PelayanPort))
        except:
            print "Tidak boleh bind"
            exit(1)
        print "Bind berjaya"
        try:
            PelayanSocket.listen(40)
        except:
            print "Server cannot listen!"
            exit(1)
        print "Server is ready to receive"

        while True:
            connectionSocket, addr = PelayanSocket.accept()

            threading.Thread(target=self.listenToPelanggan, args=(connectionSocket, addr)).start()
            
if __name__ == "__main__":
    PelayanName = "192.168.1.27"
    PelayanPort = 8080
    ThreadedServer(PelayanPort, PelayanName)
