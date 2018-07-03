#!/usr/bin/env python

import socket
import sys

class Client:
    TCP_IP = '127.0.0.1'
    TCP_PORT = 4242
    BUFFER_SIZE = 1024
    
    def start_connection:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        

    def stop_connection:
        s.close()