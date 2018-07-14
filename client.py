#!/usr/bin/env python

import socket
import sys
from operator import xor

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
    
    def bytestuffing(self, bytes_file):

        bytes_file = str(bytes_file)                         # passa para string
        bytes_file2 = bytes_file.replace('ESC', 'ESCESC')    # escapa o escape primeiro
        bytes_file3 = bytes_file2.replace('@', 'ESC@')       # escapa a flag

        return bytes_file3

    def send_msg(self):
        bytes_file = self.file.read(1024)                    # bytes_file = 1KB do arquivo
        id = 0                                               # contador para os frames
        while (bytes_file):                                  # enquanto restar arquivo
            id = id + 1                                      # incrementa o id
            #bytes_file = self.bytestuffing(bytes_file)       # antes de enviar, faz o bytestuffing
            frame = self.delimitacao_frame(bytes_file, id)   # monta o frame
            self._socket.send(frame)                         # manda o frame
            bytes_file = self.file.read(1024)                # reseta os bytes
        self.close_connection()

    def checksum(self, bytes_file):
        sum_of_checksum = str(bin(sum(bytes_file)))          # soma os bytes, transforma em binario e em string
        sum_of_checksum = sum_of_checksum[2:]                # tira os dois primeiros bytes
        sum_of_checksum = sum_of_checksum + str('0101')      # para teste
        len_sum = len(sum_of_checksum)                       # tamanho da soma

        while(len_sum > 16):                                 # checksum tem que ser no maximo de tamanho 16, se não
            lim = len_sum - 16                               # bytes mais a esquerda
            extra = sum_of_checksum[:lim]                    # separados para a soma
            sum_of_checksum = sum_of_checksum[lim:]          # retirados da soma
            s = bin(int(sum_of_checksum, 2) + int(extra, 2)) # soma dos bits mais a esquerda com o restante
            sum_of_checksum = str(s)                         # passado para a string principal
            sum_of_checksum = sum_of_checksum[2:]            # os dois primeiros bits '0b' são retirados
            len_sum = len(sum_of_checksum)                   # o tamanho da string é passado para a variável

        mask = 0xFFFF                                        # mascara de 16 bits 1
        sum_of_checksum = int(sum_of_checksum, 2)            

        checksum = str(bin(xor(sum_of_checksum, mask)))[2:]  # inversão dos bits com xor e retirada dos dois primeiros bits
        return checksum
    
    def origem_destino(self):
        ip_porta = self.TCP_IP + str(self.TCP_PORT)

        return ip_porta

      # | Flag | ID | Data | Checksum | Flag |

    def delimitacao_frame(self, bytes_file, id):             # @ header data trailer @
        ini_end = '@'                                        # inicio e fim do frame
        frame = ini_end                                      # frame começa com @
        frame = frame + str(id)                              # logo após vem o id
        frame = frame + self.origem_destino()                     # coloca a origem
        frame = frame + str(bytes_file)                      # coloca os dados no frame
        frame = frame + str(self.checksum(bytes_file))       # coloca o checksum no frame
        frame = frame + ini_end                              # frame termina com @

        return frame

        # header = endereços de origem e destino e outras infos de controle   header = go back n ARQ
        # trailer = bits redundantes para detecção e correção de erros        trailer = ARQ, checksum
        # data = + byte-stuffing

def main():
    c = Client('raniery.jpg')
    c.send_msg()

if __name__ == '__main__':
    main()
    
