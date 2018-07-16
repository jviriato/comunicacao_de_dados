#!/usr/bin/env python

import socket
import sys


class Server:


    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 5010
        self.destino = (self.TCP_IP, self.TCP_PORT)

        self.achou = 0
        self.frame = None

        self.start_connection()

    def start_connection(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(self.destino)

    def trata_frame(self, frame):
        indices = [i for i, x in enumerate(str(frame)) if x == '@']
        print(indices)
        
    def close_connection(self):
        self._socket.close()

    def trata_frame(self, frame):
        inicio_frame = 0
        fim_frame = 0
        frame = frame.decode('UTF-8')
        frame = str(frame)
        for i, c in enumerate(frame):
            if c == '@' and self.achou == 0:
                inicio_frame = i
                self.achou = 1
            elif c == '@' and self.achou == 1 and frame[i-3:i] != 'ESC':
                fim_frame = i
                self.achou = 0
        self.frame = frame[inicio_frame:fim_frame+1]

        id = self.frame[1]
        origem = self.frame[2:15]
        checksum = self.frame[-16:-1]
        checksum = int(checksum, 2)


    def receive_msg(self):
        self._socket.listen(5)
        f = open("rani.jpg", 'wb')
        while True:
            print("Esperando...")
            c, addr = self._socket.accept()
            print("Conexao de:" + str(addr))
            l = c.recv(4096)
            self.trata_frame(l)
            while(l):
                f.write(l)
                l = c.recv(4096)
                # self.trata_frame(l)
            f.close()
        self.close_connection()

def main():
    s = Server()
    s.receive_msg()

if __name__ == '__main__':
    main()
    
