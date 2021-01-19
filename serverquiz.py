from socket import *
import select
from thread import *
import sys
import time
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_add="192.168.1.39"
port= 8080
server.bind((ip_address, port))
server.listen(100)

list_of_clients=[]

soalan = [" Bangunan apakah yang tertinggi di Malaysia? \n a.KLCC b.KL Tower c.Menara Maybank d.Menara CIMB",
     " Bilakah tarikh kemerdekaan di Malaysia? \n a.31/8 b.31/9 c.25/7 d.26/5",
     " Di manakah terletaknya Aquaria? \n a.Selangor b.Johor c.Terengganu d.KL",
     " Tahun apakah kini di Malaysia? \n a.1997 b.1998 c.2020 d.2021",
     " Berapakah hitungan Perdana Menteri di Malaysia sejak kemerdekaan? \n a.7 b.8 c.9 d.10"]

jawapan = ['a', 'a', 'd', 'd', 'b']

calculate=[]
client = ["address",-1]
buzzer =[0, 0, 0]

def clientthread(conn, addr):
    conn.send("\nSelamat Datang ke Kahuurr Kuiz! Sila jawab soalan sebelum pemain lain cuba menjawab!!\n Tekan apa sahaja key di papan kekunci anda dan tekan enter untuk buzzer\n")
    
    while True:
            mesej = conn.recv(2048)
            if mesej:
                if buzzer[0]==0:
                    client[0] = conn
                    buzzer[0] = 1
                    i = 0
                    while i < len(list_of_clients):
                            if list_of_clients[i] == client[0]:
                                break
                            i +=1
                    client[1] = i

                elif buzzer[0] ==1 and conn==client[0]:
                        kira = mesej[0] == jawapan[buzzer[2]][0]
                        print (jawapan[buzzer[2]][0])
                        if kira:
                            broadcast("Pemain" + str(client[1]+1) + " +1" + "\n\n")
                            calculate[i] += 1
                            if calculate[i]==5:
                                broadcast("pemain" + str(client[1]+1) + " WON" + "\n")
                                end_soalanquiz()
                                sys.exit()

                        else:
                            broadcast("Pemain" + str(client[1]+1) + " +0" + "\n\n")
                            calculate[i] += 0
                        buzzer[0]=0
                        if len(soalan) != 0:
                            soalan.pop(buzzer[2])
                            jawapan.pop(buzzer[2])
                        if len(soalan)==0:
                            end_soalanquiz()
                        soalanquiz()

                else:
                        conn.send(" Pemain " + str(client[1]+1) + " tekan buzzer!!\n\n")
            else:
                    tamat(conn)

def broadcast(mesej):
    for clients in list_of_clients:
        try:
            clients.send(mesej)
        except:
            clients.close()
            tamat(clients)
def end_soalanquiz():
        broadcast("Permainan Tamat\n")
        buzzer[1]=1
        i = calculate.index(max(calculate))
        broadcast("pemain " + str(i+1)+ " menang dengan markah "+str(calculate[i])+" mata.")
        for x in range(len(list_of_clients)):
            list_of_clients[x].send("Anda dapat " + str(calculate[x]) + " mata.")
            
        server.close()


def soalanquiz():
    buzzer[2] = random.randint(0,10000)%len(soalan)
    if len(soalan) != 0:
        for connection in list_of_clients:
            connection.send(soalan[buzzer[2]])
def tamat(connection):
    if connection in list_of_clients:
        list_of_clients.tamat(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    calculate.append(0)
    print (addr[0] + " connected")
    start_new_thread(clientthread,(conn,addr))
    if(len(list_of_clients)==3):
        soalanquiz()
conn.close()
server.close()

