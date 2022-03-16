# ProjetoQuiz
O projeto 1 consiste num quiz com 20 perguntas e respostas. Durante uma partida serão selecionadas 5 perguntas, o jogo pode ser jogado por até cinco participantes, os jogadores do quiz devem participar da mesma máquina. Para criação do quiz utilizamos o protocolo UDP e a programação de sockets para o transporte de dados. Foi usada a arquitetura ‘Cliente-Servidor’ para comunicação dos jogadores com o servidor.
como usar:
Para rodar o código do quiz é necessário seguir os seguintes passos:

⦁	Redigir um arquivo de texto denominado ‘Perguntas&Respostas.txt’ e colocá-lo no mesmo local do código. 
Seguindo o seguinte padrão => 
‘pergunta1' ; 'resposta1'
com uma linha de sobra no final do arquivo
OBS.: O arquivo padrão vai estar disponibilizado no GITHUB juntamente com o código fonte.

⦁	O código está dividido em 2 partes, seguindo a arquitetura ‘Cliente - Servidor’, o nome dos arquivos são: cliente = ‘CodigoClienteQuiz.py’ e servidor = ‘CodigoServidorQuiz.py’. Para executar, é necessário rodar primeiro o código do servidor.

⦁	Os clientes têm que indicar o nome do participante. A partir de dois clientes na partida, será liberada a opção de começar o jogo, digitando: ‘start’, o quiz comporta até 5 jogadores. A operação de início do quiz pode ser realizada por qualquer um dos jogadores. A partir do início, serão disponibilizadas as perguntas e os jogadores terão que responder.
OBS.: As respostas são palavras únicas que começam com letras maiúsculas.
