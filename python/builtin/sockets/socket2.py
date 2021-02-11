#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 45130

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))    # Connect to server at HOST:PORT
    s.sendall(b'Hello, world') # Send DATA
    data = s.recv(1024)
    print(data)
