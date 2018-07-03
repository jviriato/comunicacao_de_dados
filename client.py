#!/usr/bin/env python

import socket
import sys

class Client:
    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 4242
        self.startConnection()

    def start_connection(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def close_connection(self):
        self._socket.close()

    def send_msg(self):
        msg = raw_input()
        while msg != '\x18':
            self._socket.send(msg)
            msg = raw_input()
        self.close_connection()
