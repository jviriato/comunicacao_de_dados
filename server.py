#!/usr/bin/env python

import socket
import sys
from operator import xor

class Server:

    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 5010
        self.destino = (self.TCP_IP, self.TCP_PORT)

        self.frame = None
        self.cont_id = 0
        self.frames_perdidos = 0
        self.frames_com_erro = 0

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
    
    def trata_checksum(self, dados, checksum):
        dados = list(dados)                                               # separa os bytes em uma lista, já que bytes_file é uma string
        checksum = checksum.replace('x', '0')                             # troca os x por 0
        checksum = int(checksum, 2)
        i = 0                                                             # inicia o contador
        for dado in dados:                                                # para cada dado em dados
            dado = ord(dado)                                              # pega o valor da tabela ascii
            dados[i] = dado                                               # atualiza a lista
            i = i + 1                                                     # atualiza contador

        sum_of_checksum = sum(dados) + checksum                           # soma os bytes com o checksum
        sum_of_checksum = str(bin(sum_of_checksum))[2:]                   # transforma em binario e em string e tira os dois primeiros bytes
        len_sum = len(sum_of_checksum)                                    # tamanho da soma

        while (len_sum > 16):                                             # checksum tem que ser no maximo de tamanho 16, se não
            lim = len_sum - 16                                            # bytes mais a esquerda
            extra = sum_of_checksum[:lim]                                 # separados para a soma
            sum_of_checksum = sum_of_checksum[lim:]                       # retirados da soma
            s = bin(int(sum_of_checksum, 2) + int(extra, 2))              # soma dos bits mais a esquerda com o restante
            sum_of_checksum = str(s)                                      # passado para a string principal
            sum_of_checksum = sum_of_checksum[2:]                         # os dois primeiros bits '0b' são retirados
            len_sum = len(sum_of_checksum)                                # o tamanho da string é passado para a variável

        mask = 0xFFFF                                                     # mascara de 16 bits 1
        sum_of_checksum = int(sum_of_checksum, 2)

        checksum = str(bin(xor(sum_of_checksum, mask)))[2:]               # inversão dos bits com xor e retirada dos dois primeiros bits
        return checksum
    
    def trata_origem(self, origem):
        for i, c in enumerate(origem):                                    # para to.do c na string origem
            if c == 'x':                                                  # se o caractere c for igual a x
                lim = i                                                   # a seperação terá que ser feita aí, então limite = indice
                break                                                     # já pode sair do for
        ip = origem[:lim]                                                 # a primeira parte é o ip
        porta = origem[lim:].replace('x', '')                             # a segunda parte é a porta, retirando os xs a mais
        if ip == self.TCP_IP and porta == str(self.TCP_PORT):
            return 0
        else:
            return 1
    
    def trata_frame(self, frame):
        achou = 0
        inicio_frame = 0                                                  # variavel do inicio do frame é inicializada
        fim_frame = 0                                                     # variavel do fim do frame é inicializada
        frame = frame.decode('UTF-8')                                     # frame é decodificado
        frame = str(frame)                                                # variavel é passada para string
        for i, c in enumerate(frame):                                     # para to.do c no frame
            if c == '@' and achou == 0:                              # se c for igual a flag inicial @ e ainda não achou nenhum flag
                inicio_frame = i                                          # inicio do frame é igual ao indice de c
                achou = 1                                            # e achou é igual a 1
            elif c == '@' and achou == 1 and frame[i-3:i] != 'ESC':  # se achou outra flag, já tinha achado outra antes e as 3 letras anteriores não forem ESC
                fim_frame = i                                             # fim do frame é igual ao indice de c
        self.frame = frame[inicio_frame:fim_frame + 1]                    # coloca os limites no frame
                                                                          
                                                                          # conforme apresentado na classe cliente
        id = self.frame[1:9]                                              # id tem 8 bits, de 1 até 9
        origem = self.frame[9:25]                                         # origem/destino tem 16 bits, de 9 até 25
        dados = self.frame[25:-17]                                        # os dados vão de 25 até onde começa o checksum
        checksum = self.frame[-17:-1]                                     # checksum são os 17 ultimos dados, sem contar com flag final
        
        check_id = self.trata_id(id)                                      # manda o id para a função e retorna se está certo
        if check_id == 1:                                                 # se for igual a 1, frame(s) anterior(es) foi(foram) perdido(s)
            self.frames_perdidos = self.frames_perdidos + 1               # acrescenta a variavel de frames perdidos em 1
            return 1
        check_origem = self.trata_origem(origem)                          # manda a origem para a função de tratamento
        if check_origem == 1:                                             # se for igual a 1, frame enviado com erro
            self.frames_com_erro = self.frames_com_erro + 1               # acrescenta a variavel de frames com erro em 1
            return 1
        check_checksum = self.trata_checksum(dados, checksum)             # manda os dados e o checksum para o tratamento
        if check_checksum == 1:                                           # se for igual a 1, frame enviado com erro
            self.frames_com_erro = self.frames_com_erro + 1               # acrescenta a variavel de frames com erro em 1
            return 1
        
        #não envia ack em nenhum dos casos acima, só a partir de agora
        print(frame)
        c.send('ack'.encode('UTF-8'))     #enviar id?
        return 0, dados
    
    def tirabytestuffing(self, d):

        d = str(d)                       # passa para string
        d2 = d.replace('ESCESC', 'ESC')     # escapa o escape primeiro
        d3 = d2.replace('ESC@', '@')      # escapa a flag

        return d3
        
    def receive_msg(self):
        self._socket.listen(5)
        f = open("rani.jpg", 'wb')
        while True:
            c, addr = self._socket.accept()
            print("Conexao de: " + str(addr))
            while True:
                l = c.recv(4096)
                if not l: break
                ok, d = self.trata_frame(l, c)
                if ok == 0:
                    d = self.tirabytestuffing(d)
                    f.write(l)
        f.close()
        self.close_connection()

def main():
    s = Server()
    s.receive_msg()

if __name__ == '__main__':
    main()
    
