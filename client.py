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
        bytes_file = self.file.read(1024)               # bytes_file = 1KB do arquivo
        while (bytes_file):                             # enquanto restar arquivo
            frame = self.delimitacao_frame(bytes_file)  # monta o frame
            self._socket.send(frame)                    # manda o frame
            bytes_file = self.file.read(1024)           # reseta os bytes
        self.close_connection()

    def checksum(self, bytes_file):
        sum_of_checksum = str(bin(sum(bytes_file)))     # soma os bytes, transforma em binario e em string
        sum_of_checksum = sum_of_checksum[2:]           # tira os dois primeiros bytes
        sum_of_checksum = sum_of_checksum + str('0101') # para teste
        len_sum = len(sum_of_checksum)                  # tamanho da soma

        while(len_sum > 16):                            # checksum tem que ser no maximo de tamanho 16, se não
            lim = len_sum - 16                          # bytes mais a esquerda
            extra = sum_of_checksum[:lim]               # separados para a soma
            sum_of_checksum = sum_of_checksum[lim:]     # retirados da soma
            sum_of_checksum = '0b' + sum_of_checksum
            extra = '0b' + extra
            #print("Soma do Checksum: " + sum_of_checksum)
            #print("Bits à esquerda: " + extra)
            
            #extra e sum_of_checksum são strings. Portanto, 0 vale 48 e 1 vale 49 em binário (ASCII)
            #print(type(extra))
            print("Valor de extra em binário: ")
            print(int(extra, 2))
            print("Valor de sum_of_checksum em binário:")
            print(int(sum_of_checksum, 2))

            soma_dos_dois = int(extra, 2) + int(sum_of_checksum, 2)
            negacao = ~soma_dos_dois
            print("Soma dos dois: " + str(soma_dos_dois))
            print("Negação: " + str(negacao))
            


            sum_of_checksum = sum_of_checksum & extra # soma do extra com a soma
            print(sum_of_checksum)
            len_sum = len(sum_of_checksum)

        checksum = not sum_of_checksum                  # complemento e final do checksum
        print(checksum)
        return checksum


    def delimitacao_frame(self, bytes_file):            # @ header data trailer @
        ini_end = '@'                                   # inicio e fim do frame
        frame = ini_end                                 # frame começa com @
        frame = frame + str(bytes_file)                 # coloca os dados no frame
        frame = frame + str(self.checksum(bytes_file))  # coloca o checksum no frame
        frame = frame + ini_end                         # frame termina com @

        return frame

        # header = endereços de origem e destino e outras infos de controle   header = go back n ARQ
        # trailer = bits redundantes para detecção e correção de erros        trailer = ARQ, checksum
        # data = + byte-stuffing

def main():
    c = Client('raniery.jpg')
    c.send_msg()

if __name__ == '__main__':
    main()
    
