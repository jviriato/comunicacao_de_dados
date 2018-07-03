#!/usr/bin/env python

import socket
import sys


class Server:

    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 4242
        self.start_connection()

    def start_connection(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def close_connection(self):
        self._socket.close()
