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
    
    def trata_checksum(self, dados, checksum):
        dados = list(dados)                                               # separa os bytes em uma lista, já que bytes_file é uma string
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
        print(checksum)
        return checksum

    def trata_frame(self, frame):
        inicio_frame = 0                                                  # variavel do inicio do frame é inicializada
        fim_frame = 0                                                     # variavel do fim do frame é inicializada
        frame = frame.decode('UTF-8')                                     # frame é decodificado
        frame = str(frame)                                                # variavel é passada para string
        for i, c in enumerate(frame):                                     # para to.do c no frame
            if c == '@' and self.achou == 0:                              # se c for igual a flag inicial @ e ainda não achou nenhum flag
                inicio_frame = i                                          # inicio do frame é igual ao indice de c
                self.achou = 1                                            # e achou é igual a 1
            elif c == '@' and self.achou == 1 and frame[i-3:i] != 'ESC':  # se achou outra flag, já tinha achado outra antes e as 3 letras anteriores não forem ESC
                fim_frame = i                                             # fim do frame é igual ao indice de c
        self.frame = frame[inicio_frame:fim_frame + 1]                    # coloca os limites no frame
                                                                          
                                                                          # conforme apresentado na classe cliente
        id = self.frame[1:9]                                              # id tem 8 bits, de 1 até 9
        origem = self.frame[9:25]                                         # origem/destino tem 16 bits, de 9 até 25
        dados = self.frame[25:-17]                                        # os dados vão de 25 até onde começa o checksum
        checksum = self.frame[-17:-1]                                     # checksum são os 17 ultimos dados, sem contar com flag final

        check_id = self.trata_id(id)                                      # manda o id para a função e rotorna se está certo
        if check_id == 0: pass                                            # se o retorno for 0, o id está certo, passa para o outro tratamento
        #else: ..........                                                 # se não, ....
        #self.trata_origem(origem)
        check_checksum = self.trata_checksum(dados, checksum)             # manda os dados e o checksum para o tratamento
        if check_checksum == 0: pass                                      # se o retorno for 0, significa que o checksum estava certo
        #else: ..........                                                 # se não, estava errado e ....


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
    
