from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import random
import time


class Quiz:
    def __init__(self):
        self.servidor_quiz = socket(AF_INET, SOCK_DGRAM)
        self.servidor_quiz.bind(('localhost', 4000))

        self.rodada_aberta = False
        self.rodada = 0

        self.lista_de_jogadores = []
        self.lista_de_nomes = []
        self.dict_respondeu = {}
        self.lista_de_perguntas = []
        self.classificacao = []

        self.arquivo_de_texto = 'Perguntas&Respostas.txt'

    def start(self):
        while len(self.lista_de_jogadores) < 5:

            nome_cliente, endereco_cliente = self.servidor_quiz.recvfrom(2048)

            if not self.jogador_esta_na_partida(endereco_cliente):
                self.lista_de_jogadores.append([0, (len(self.lista_de_jogadores), nome_cliente, endereco_cliente)])
                print(f'{nome_cliente.decode()} entrou, {len(self.lista_de_jogadores)} jogadores estão na partida,'
                      f' faltam {5 - len(self.lista_de_jogadores)}')
                self.servidor_quiz.sendto(f'Voce entrou no jogo, {len(self.lista_de_jogadores)} '
                                          f'jogadores estão na partida'.encode(), endereco_cliente)
                if len(self.lista_de_jogadores) > 1:
                    self.mensagem_geral(f'se quiser começar digite "start"')
            else:
                if nome_cliente.decode() == 'start' and len(self.lista_de_jogadores) > 1:
                    break
                else:
                    self.servidor_quiz.sendto('voce ja entrou, ou ja existe alguem com esse nome'.encode(),
                                              endereco_cliente)

    def receber_texto(self):
        arquivo = open(str(self.arquivo_de_texto), 'r')
        while True:
            try:
                linha = arquivo.readline()
                if linha == '':
                    arquivo.close()
                    break
                linha = linha.split(' ; ')
                pergunta, resposta = linha[0], linha[1][:len(linha[1]) - 1]
                self.lista_de_perguntas.append((pergunta, resposta))
            except EOFError:
                arquivo.close()
                break

    def mensagem_geral(self, msg):
        for jogador in self.lista_de_jogadores:
            quiz.servidor_quiz.sendto(msg.encode(), jogador[1][2])

    def encerrar_rodada(self):
        self.rodada_aberta = False
        self.rodada += 1

    def esperar_10_segundos(self):
        rodada_inicio = self.rodada
        time.sleep(10)
        if self.rodada_aberta and self.rodada == rodada_inicio:
            self.encerrar_rodada()

    def pergunta_aleatoria(self):
        index = random.randint(0, len(self.lista_de_perguntas) - 1)
        pergunta = self.lista_de_perguntas[index][0]
        resposta = self.lista_de_perguntas[index][1]
        self.lista_de_perguntas.pop(index)
        return pergunta, resposta

    def buscar_indicie(self, endereco):
        index = 0
        while self.lista_de_jogadores[index][1][2] != endereco:
            index += 1
        return index

    def jogador_esta_na_partida(self, endereco):
        try:
            index = 0
            while self.lista_de_jogadores[index][1][2] != endereco:
                index += 1
            return True
        except IndexError:
            return False

    def muda_ponto(self, endereco, acao):
        index = self.buscar_indicie(endereco)
        if acao == 'e':
            self.lista_de_jogadores[index][0] -= 5
        elif acao == 's':
            self.lista_de_jogadores[index][0] -= 1
        elif acao == 'a':
            self.lista_de_jogadores[index][0] += 25

    def perguntar(self):
        pergunta, resposta = self.pergunta_aleatoria()
        self.mensagem_geral(pergunta)
        self.rodada_aberta = True
        Thread(target=self.esperar_10_segundos).start()
        while self.rodada_aberta:
            try:
                palpite, endereco_cliente = self.servidor_quiz.recvfrom(2048)
                if self.verificar_validade_da_mensagem(endereco_cliente):
                    self.dict_respondeu[endereco_cliente] = 1
                    if palpite.decode() == resposta:
                        self.muda_ponto(endereco_cliente, 'a')
                        self.servidor_quiz.sendto('Voce acretou, recebeu 25 pontos'.encode(), endereco_cliente)
                        self.encerrar_rodada()
                    else:
                        self.muda_ponto(endereco_cliente, 'e')
                        self.servidor_quiz.sendto('Voce errou, perdeu 5 pontos'.encode(), endereco_cliente)
            except OSError:
                pass

    def verificar_se_respondeu(self):
        for jogador_ in self.lista_de_jogadores:
            try:
                self.dict_respondeu.pop(jogador_[1][2])
            except KeyError:
                self.muda_ponto(jogador_[1][2], 's')
                self.servidor_quiz.sendto('Voce nao respondeu a pergunta, perdeu 1 ponto'.encode(), jogador_[1][2])

    def verificar_quem_ganhou(self):
        print(self.lista_de_jogadores)
        for jogador__ in self.lista_de_jogadores:
            self.classificacao.append((jogador__[0], jogador__[1][1].decode()))
            print(self.classificacao)
        return sorted(self.classificacao, reverse=True)

    def verificar_validade_da_mensagem(self, endereco):
        for jogador___ in self.lista_de_jogadores:
            if jogador___[1][2] == endereco:
                return True
        return False

    def fabricar_classificacao(self):
        self.classificacao = self.verificar_quem_ganhou()
        print(self.classificacao)
        tabela = '\n' \
                 ':::::::::::::::::::::::::::::::::::::::\n' \
                 '::    CLASSIFICAÇÂO   :::  PONTUAÇÂO ::\n' \
                 ':::::::::::::::::::::::::::::::::::::::\n'
        for i in range(len(self.lista_de_jogadores)):
            tabela += f':: {i + 1}º -'
            tabela += f'  {self.classificacao[i][1]}'
            tabela += ' ' * (10 - (len(self.classificacao[i][1])))
            tabela += f'   ::: {self.classificacao[i][0]} pontos  ::\n'
        tabela += ':::::::::::::::::::::::::::::::::::::::\n'
        print(tabela)
        return tabela


continuar = True
while continuar:
    quiz = Quiz()
    quiz.receber_texto()
    print('recebeu texto')
    quiz.start()
    quiz.servidor_quiz.settimeout(0.5)
    print('startou')
    for rodada in range(1, 6):
        quiz.mensagem_geral(f'Vamos para a rodada {quiz.rodada + 1} em 5 segundos, se prepare\n')
        time.sleep(5)
        mensagem_rodada = '::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n' \
                          f'::::::::::::::::::::::::::     RODADA {quiz.rodada + 1}     ::::::::::::::::::::::::::\n' \
                          '::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n'
        quiz.mensagem_geral(mensagem_rodada)
        quiz.perguntar()
        quiz.verificar_se_respondeu()
        print('perguntou')
    classi = quiz.fabricar_classificacao()
    quiz.mensagem_geral(classi + '\n')
    quiz.mensagem_geral('acabou')
    quiz.servidor_quiz.settimeout(None)

    if not 's' == input('voce quer jogar de novo? (se sim digite "s")\n'):
        continuar = False
