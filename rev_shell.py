#!/usr/bin/python

import socket

def shell():
    while True:
        cmd = s.recv(1024) # receive command from server
        if cmd.decode('utf-8') == "exit":
            break
        output = "message from client"
        s.send(output.encode('utf-8')) #send output to server

#socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect
s.connect(("192.168.92.128",7777)) #server IP and to which port to connect to
shell()
s.close()