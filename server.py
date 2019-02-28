from socket import *
import json
import selectors
import socket
import threading

HOST = "localhost"
PORT = 1024

sel = selectors.DefaultSelector()

def accept(sock, mask):
    global client_list
    (conn, addr) = sock.accept() # returns new socket and addr.
    if conn not in client_list:
        client_list.append(conn)
    print('accepted', conn, 'from', addr);
    conn.setblocking(False) # program doesn't wait
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    global client_list
    data = conn.recv(1024)  # Should be ready
    if data:
        for client in client_list:
            client.send(data)
            print('echoing', repr(data), 'to', client)
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

sock = socket.socket() # creates new socket
sock.bind((HOST, PORT)) # binds socket to localhost on port 1024
sock.listen(100) # socket will accept up to 100 connections
sock.setblocking(False) # socket is non-blocking
sel.register(sock, selectors.EVENT_READ, accept) # selector registers socket for selection, for EVENT_READ, and callback is accept()

client_list = []

while True:
    events = sel.select() # blocks in select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)

