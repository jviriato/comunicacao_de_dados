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

        bytes_file = str(bytes_file)                           # passa para string
        bytes_file2 = bytes_file.replace('ESC', 'ESCESC')      # escapa o escape primeiro
        bytes_file3 = bytes_file2.replace('@', 'ESC@')         # escapa a flag

        return bytes_file3

    def send_msg(self):
        bytes_file = self.file.read(1024)                      # bytes_file = 1KB do arquivo
        id = 0                                                 # contador para os frames
        pode_mandar = True
        while (bytes_file):                                    # enquanto restar arquivo
            id = id + 1                                        # incrementa o id
            bytes_file = self.bytestuffing(bytes_file)         # antes de enviar, faz o bytestuffing
            frame = self.delimitacao_frame(bytes_file, id)     # monta o frame
            self._socket.send(frame)                           # manda o frame
            bytes_file = self.file.read(1024)                  # reseta os bytes
            self._socket.settimeout(6.0)
            pode_mandar = False
            while(not pode_mandar):
                try:
                    c, address = self._socket.recvfrom(1024)
                    c = c.decode('UTF-8')
                    if c[:3] == 'ack':        # mandar id junto?
                        print(c)
                        pode_mandar = True
                except socket.timeout:
                    self._socket.send(frame)
                    self._socket.settimeout(None)

        self.close_connection()

    def checksum(self, bytes_file):
        bytes_file = list(bytes_file)                          # separa os bytes em uma lista, já que bytes_file é uma string
        i = 0                                                  # inicia o contador
        for bytes in bytes_file:                               # para to.do byte em bytes_file
            bytes = ord(bytes)                                 # pega o valor da tabela ascii
            bytes_file[i] = bytes                              # atualiza a lista
            i = i + 1                                          # atualiza contador

        sum_of_checksum = str(bin(sum(bytes_file)))            # soma os bytes, transforma em binario e em string
        sum_of_checksum = sum_of_checksum[2:]                  # tira os dois primeiros bytes
        len_sum = len(sum_of_checksum)                         # tamanho da soma

        while(len_sum > 16):                                   # checksum tem que ser no maximo de tamanho 16, se não
            lim = len_sum - 16                                 # bytes mais a esquerda
            extra = sum_of_checksum[:lim]                      # separados para a soma
            sum_of_checksum = sum_of_checksum[lim:]            # retirados da soma
            s = bin(int(sum_of_checksum, 2) + int(extra, 2))   # soma dos bits mais a esquerda com o restante
            sum_of_checksum = str(s)                           # passado para a string principal
            sum_of_checksum = sum_of_checksum[2:]              # os dois primeiros bits '0b' são retirados
            len_sum = len(sum_of_checksum)                     # o tamanho da string é passado para a variável

        mask = 0xFFFF                                          # mascara de 16 bits 1
        sum_of_checksum = int(sum_of_checksum, 2)            

        checksum = str(bin(xor(sum_of_checksum, mask)))[2:]    # inversão dos bits com xor e retirada dos dois primeiros bits
        i = len(checksum)
        if i != 16:                                            # se for menor do que 16
            checksum = list(checksum)                          # tranforma em uma lista
            while i != 16:                                     # enquanto for menor que 16
                checksum.insert(0, 'x')                        # adiciona xs no começo
                i = i + 1                                      # incrementa o contador
        checksum = "".join(checksum)                           # reune a lista
        return checksum
    
    def origem_destino(self):
        ip_porta = self.TCP_IP + 'x' + str(self.TCP_PORT)      # origem é igual ao ip + porta (as duas são strings e se concatenam)
        
        i = len(ip_porta)                                      # tamanho da string
        if i != 16:                                            # se for != de 16
            ip_porta = list(ip_porta)                          # transforma em lista
            while i != 16:                                     # enquanto for menor que 16
                ip_porta.append('x')                           # completa com x
                i = i + 1                                      # incrementa o contador
        ip_porta = "".join(ip_porta)                           # reune a lista
        
        return str(ip_porta)
    
    def completa_0(self, num):
        num = str(num)                                         # tranforma em uma string
        i = len(num)                                           # inicia o contador
        if i != 8:                                             # se for menor do que 8
            num = list(num)                                    # tranforma em uma lista
            while i != 8:                                      # enquanto for menor que 8
                num.insert(0, 'x')                             # adiciona xs no começo
                i = i + 1                                      # incrementa o contador
        num = "".join(num)                                     # reune a lista

        return str(num)
    

      # | Flag | ID | Ori/Dest | Data | Checksum | Flag |
      # 0      1    9          25     ?         +16     +1
      # 0     +1    +8        +16     ?         +16     +1

    def delimitacao_frame(self, bytes_file, id):               # @ header data trailer @
        ini_end = '@'                                          # inicio e fim do frame
        frame = ini_end                                        # frame começa com @
        frame = frame + str(self.completa_0(str(bin(id))[2:])) # logo após vem o id
        frame = frame + self.origem_destino()                  # coloca a origem
        frame = frame + str(bytes_file)                        # coloca os dados no frame
        frame = frame + self.checksum(bytes_file)              # coloca o checksum no frame
        frame = frame + ini_end                                # frame termina com @
        
        print(frame)
        frame = frame.encode('UTF-8')
        return frame

def main():
    c = Client('raniery.jpg')
    c.send_msg()

if __name__ == '__main__':
    main()
    
