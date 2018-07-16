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
        self.cont_id = 0

        self.start_connection()

    def start_connection(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(self.destino)
        
    def close_connection(self):
        self._socket.close()
        
    def trata_id(self, id):
        id = id.replace('x', '')                                          # remove todos os xs do id
        if str(bin(self.cont_id + 1))[2:] == id:                          # se o contador + 1 for igual ao do frame atual
            self.cont_id = self.cont_id + 1                               # está tudo certo e o contador é incrementado
            return 0
        else:                                                             # se não, está errado
            return 1


    def trata_frame(self, frame):
        inicio_frame = 0                                                  #
        fim_frame = 0                                                     #
        frame = frame.decode('UTF-8')                                     #
        frame = str(frame)                                                #
        for i, c in enumerate(frame):                                     #
            if c == '@' and self.achou == 0:                              #
                inicio_frame = i                                          #
                self.achou = 1                                            #
            elif c == '@' and self.achou == 1 and frame[i-3:i] != 'ESC':  #
                fim_frame = i                                             #
        self.frame = frame[inicio_frame:fim_frame + 1]                    #
                                                                          # conforme apresentado na classe cliente
        id = self.frame[1:9]                                              # id tem 8 bits, de 1 até 9
        origem = self.frame[9:25]                                         # origem/destino tem 16 bits, de 9 até 25
        dados = self.frame[25:-17]                                        # os dados vão de 25 até onde começa o checksum
        checksum = self.frame[-17:-1]                                     # checksum são os 17 ultimos dados, sem contar com flag final

        check_id = self.trata_id(id)                                      # manda o id para a função e rotorna se está certo
        print(check_id)
        #self.trata_origem(origem)
        #self.trata_checksum(dados, checksum)

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
    
