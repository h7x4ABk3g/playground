#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM

HOST = '127.0.0.1'
PORT = 45130

with socket(AF_INET, SOCK_STREAM) as s:

    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
