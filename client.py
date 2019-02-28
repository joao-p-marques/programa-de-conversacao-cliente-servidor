import socket
import json
from datetime import datetime
import sys
import fcntl
import os
import selectors

HOST = "localhost"
PORT = 1024

# set sys.stdin non-blocking
orig_fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
fcntl.fcntl(sys.stdin, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)

sel = selectors.DefaultSelector()

def process_data(stdin):
    global sock
    msg_txt = stdin.read()
    msg = {
        "timestamp" : datetime.now().timestamp(),
        "name" : "Me",
        "message" : msg_txt
    }
    sock.send(json.dumps(msg).encode('utf-8')) # send data

def receive_data(conn):
    data = conn.recv(1024)  
    print(json.loads(data.decode('utf-8'))) # print the result
    


sock = socket.socket() # creates new socket
sock.connect((HOST, PORT)) # binds socket to localhost on port 1024
sock.setblocking(False) # socket is non-blocking

sel.register(sys.stdin, selectors.EVENT_READ, process_data)
sel.register(sock, selectors.EVENT_READ, receive_data)

while True:
    sys.stdout.write("Message: ")
    sys.stdout.flush()
    for key, mask in sel.select():
        callback = key.data
        callback(key.fileobj)

