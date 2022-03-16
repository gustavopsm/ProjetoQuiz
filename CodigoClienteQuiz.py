from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import sys
import os


def receber_mensagem(cliente_teste):
    while jogo.jogo_aberto:
        mensagemrecebida, endereco_do_servidor = cliente_teste.recvfrom(2048)
        if mensagemrecebida.decode() == 'acabou':
            print('O JOGO ACABOU')
            jogo.jogo_aberto = False
        else:
            print(f'{mensagemrecebida.decode()}')


jogador_quiz = socket(AF_INET, SOCK_DGRAM)
endereco_servidor = ('localhost', 4000)

meu_nome = input('digite seu nome (máximo 10 caracteres) => ')
while len(meu_nome) > 10:
    meu_nome = input('nome inválido (máximo 10 caracteres) => ')
jogador_quiz.sendto(meu_nome.encode(), endereco_servidor)


class Jogo:

    def __init__(self):
        self.jogo_aberto = True


jogo = Jogo()
Thread(target=receber_mensagem, args=(jogador_quiz,)).start()

while jogo.jogo_aberto:
    mensagem = input()
    jogador_quiz.sendto(mensagem.encode(), endereco_servidor)
