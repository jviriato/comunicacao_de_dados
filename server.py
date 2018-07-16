#!/usr/bin/env python

import socket
import sys


class Server:

    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 5010
        self.destino = (self.TCP_IP, self.TCP_PORT)

        self.start_connection()

    def start_connection(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(self.destino)

    def trata_frame(self, frame):
        indices = [i for i, x in enumerate(str(frame)) if x == '@']
        print(indices)
        
    def close_connection(self):
        self._socket.close()

    def receive_msg(self):
        self._socket.listen(5)
        f = open("rani.jpg", 'wb')
        while True:
            print("Esperando...")
            c, addr = self._socket.accept()
            print("Conexao de:" + str(addr))
            l = c.recv(1024)
            self.trata_frame(l)
            while(l):
                f.write(l)
                l = c.recv(1024)
                self.trata_frame(l)
            f.close()
        self.close_connection()

def main():
    s = Server()
    s.receive_msg()

if __name__ == '__main__':
    main()
    
