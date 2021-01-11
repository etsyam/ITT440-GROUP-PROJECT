import socket
import select
from thread import *
import sys
import time
import random


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_add="192.168.1.39"
port= 8080
server.bind((ip_add, port))
server.listen(100)

list_of_clients=[]


Q = [" What is the tallest building in Malaysia? \n a.KLCC b.KL Tower c.Menara Maybank d.Menara CIMB",
     " At what date is our National Day? \n a.31/8 b.31/9 c.25/7 d.26/5",
     " Where is Aquaria? \n a.Selangor b.Johor c.Terengganu d.KL",
     " What is the year now in Malaysia \n a.1997 b.1998 c.2020 d.2021",
     " How many prime minister do we have? \n a.7 b.8 c.9 d.10"]

A = ['a', 'a', 'd', 'd', 'b']

Count=[]
client = ["address",-1]
bzr =[0, 0, 0]

def clientthread(conn, addr):
    conn.send("\nWelcome to Karhut! Answer the questions before any other players!\n Press any key on the keyboard and ENTER as a buzzer for the given question\n")
    
    while True:
            message = conn.recv(2048)
            if message:
                if bzr[0]==0:
                    client[0] = conn
                    bzr[0] = 1
                    i = 0
                    while i < len(list_of_clients):
                            if list_of_clients[i] == client[0]:
                                break
                            i +=1
                    client[1] = i

                elif bzr[0] ==1 and conn==client[0]:
                        bol = message[0] == A[bzr[2]][0]
                        print (A[bzr[2]][0])
                        if bol:
                            broadcast("player" + str(client[1]+1) + " +1" + "\n\n")
                            Count[i] += 1
                            if Count[i]==5:
                                broadcast("player" + str(client[1]+1) + " WON" + "\n")
                                end_quiz()
                                sys.exit()

                        else:
                            broadcast("player" + str(client[1]+1) + " +0" + "\n\n")
                            Count[i] += 0
                        bzr[0]=0
                        if len(Q) != 0:
                            Q.pop(bzr[2])
                            A.pop(bzr[2])
                        if len(Q)==0:
                            end_quiz()
                        quiz()

                else:
                        conn.send(" player " + str(client[1]+1) + " pressed buzzer first\n\n")
            else:
                    remove(conn)

def broadcast(message):
    for clients in list_of_clients:
        try:
            clients.send(message)
        except:
            clients.close()
            remove(clients)
def end_quiz():
        broadcast("Game Over\n")
        bzr[1]=1
        i = Count.index(max(Count))
        broadcast("player " + str(i+1)+ " wins!! by scoring "+str(Count[i])+" points.")
        for x in range(len(list_of_clients)):
            list_of_clients[x].send("You scored " + str(Count[x]) + " points.")
            
        server.close()


def quiz():
    bzr[2] = random.randint(0,10000)%len(Q)
    if len(Q) != 0:
        for connection in list_of_clients:
            connection.send(Q[bzr[2]])
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    Count.append(0)
    print (addr[0] + " connected")
    start_new_thread(clientthread,(conn,addr))
    if(len(list_of_clients)==3):
        quiz()
conn.close()
server.close()
