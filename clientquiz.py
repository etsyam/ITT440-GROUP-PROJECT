import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_addr = "192.168.1.39"
port = 8080
server.connect((ip_addr, port))

while True:
    sockets_list = [sys.stdin, server]

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print (message)
        else:
            message = sys.stdin.readline()
            server.send(message)
            sys.stdout.flush()
            
server.close()
sys.exit()
