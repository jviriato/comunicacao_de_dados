#!/usr/bin/env python

import socket
import sys

class Client:
    def __init__(self, filename):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 5010
        self.origem = (self.TCP_IP, self.TCP_PORT)
        self.file = open(filename, 'rb')

        self.start_connection()

    def start_connection(self):
        print("Conectado")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(self.origem)

    def close_connection(self):
        self.file.close()
        self._socket.close()

    def send_msg(self):
        bytes_file = self.file.read(1024)         # bytes_file = 1KB do arquivo
        while (bytes_file):                       # enquanto restar arquivo
            frame = self.delimitacao_frame(bytes_file) # monta o frame
            self._socket.send(frame)              # manda o frame
            bytes_file = self.file.read(1024)     # reseta os bytes
        self.close_connection()

    def checksum(self):
        checksum = 1


    def delimitacao_frame(self, bytes_file):      # @ header data trailer @
        ini_end = '@'                             # inicio e fim do frame
        frame = ini_end                           # frame começa com @
        frame = frame + str(bytes_file)           # coloca os dados no frame
        frame = frame + str(self.checksum())      # coloca o checksum no frame
        frame = frame + ini_end                   # frame termina com @

        return frame

        # header = endereços de origem e destino e outras infos de controle   header = go back n ARQ
        # trailer = bits redundantes para detecção e correção de erros        trailer = ARQ, checksum
        # data = + byte-stuffing

def main():
    c = Client('raniery.jpg')
    c.send_msg()

if __name__ == '__main__':
    main()
    
