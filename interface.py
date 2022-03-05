#Este arquivo é responsável pela interface dos jogadores

import threading
from servidor import *
from time import *
from batalha_naval import *
from random import randint

#Variáveis mais usadas do código
dado = randint(0, 1)
tabu_visual = []
tabu_posi = []
nick_jogadores = ["", ""]
embarcacoes = [["2", "2"], ["3"], ["4"], ["5"]]
pronto = []
#Chamada da função principal do arquivo do servidor
fun_principal()


def instrucoes_jogo(jogador, ind):
    """
    Essa função será chamada para a apresentação das regras do jogo de batalha-naval
    :param jogador: Lista com os clientes conectados ao server
    :param ind: Índice da lista de clientes
    """
    msg = "Estas serão as instruções para o jogo:\n" \
          "1- Assim que os dois jogadores estivem prontos, o jogo terá início!\n" \
          "2- Você irá posicionar suas embarcações, uma a uma, podendo direcioná-las de forma vertical ou horizontal;\n" \
          "3- Cada embarcação deverá ser posicionada dentro dos limites do tabuleiro;\n" \
          "4- Cada embarcação deverá possuir, em todas as direções, uma distência mínima de uma u. a. para suas outras embarcações\n" \
          "5- Quando todas as embarcações, as suas e as adversárias, estiverem posicionadas, os ataques irão começar!\n" \
          "6- Cada jogador terá uma bomba por rodada para tentar atingir uma embarcação inimiga;\n" \
          "7- O jogador que primeiro afundar todas as embarcações inimigas, será o vencedor do jogo!\n\n" \
          "Para sair do menu de instruções, digite 'sair'"
    msg_privada(jogador[ind], msg)
    while True:
        if dados_recebidos(jogador[ind]).upper() == SAIR:
            break
        else:
            msg_privada(jogador, "Opção inválida! Tente novamente")


def inicializacao_jogo(jogador, ind, nick, prt):
    """
    Função para receber as informações iniciais dos jogadores
    :param jogador: Lista com os clientes conectados ao server
    :param ind: Índice da lista de clientes
    :param nick: Lista com os nicks escolhidos pelos jogadores
    :param prt:
    :return:
    """
    msg_privada(jogador[ind], "Insira seu nick")
    nick[ind] = dados_recebidos(jogador[ind])
    msg_privada(jogador[ind], "Para acessar as regras, digite '1', caso desege continuar digite '2'")
    if int(dados_recebidos(jogador[ind])) == 1:
        instrucoes_jogo(jogador, ind)
    if len(prt) == 0:
        prt.append(None)
        msg_privada(jogador[ind], "Aguardando seu oponente para o início da BATALHA!!!")
    else:
        prt.append(None)

#Threads com a função de inicialização para que cada jogador navegue de forma separada
inic1 = threading.Thread(target=inicializacao_jogo, args=[clientes, 0, nick_jogadores, pronto])
inic2 = threading.Thread(target=inicializacao_jogo, args=[clientes, 1, nick_jogadores, pronto])
inic1.start()
inic2.start()

#Laço de checagem de saída dos jogadores de suas threads
while True:
    if len(pronto) == 2:
        msg_privada(clientes[dado], f"Olá {nick_jogadores[dado]}\nPor favor, insira a quantidade de linhas e colunas do nosso campo de batalha\n"\
                                    "A entrada deve ser da forma 'linha coluna'.")
        while True:
            linhas, colunas = map(int, dados_recebidos(clientes[dado]).split())
            if linhas < 10 or colunas < 10:
                msg_privada(clientes[dado], "O tabuleiro deve possuir dimensão mínima '10x10'. Por favor, forneça novos valores:\n")
            else:
                break
        break

#Criação dos tabuleiros dos jogadores
#Cada jogador possui 2 tabuleiros, 1 para o posicionamento das embarcações e 1 para a visualização de suas jogadas
for i in range(2):
    tabu_visual.append(campo_de_batalha(linhas, colunas))
    tabu_posi.append(campo_de_batalha(linhas, colunas))

msg_publica("Uma prévia do seu campo de batalha:")
msg_privada(clientes[0], f"{nick_jogadores[0]}, este será o seu campo de batalha\n{formar_campo(tabu_visual[0])}")
msg_privada(clientes[1], f"{nick_jogadores[1]}, este será o seu campo de batalha\n{formar_campo(tabu_visual[1])}")


#Aqui é a área para determinação da quantidade das embarcações conforme o tamanho do tabuleiro que foi fornecido
area_tab = linhas * colunas
adc_emb = (area_tab - AREA_MIN) // COE_EMB
adicionar_embarcacoes(adc_emb, embarcacoes)

#Apenas uma informação geral, talvez seja retirada no futuro
msg_publica("Quantidades de cada tipo de embarcações:\n"
            f"2: {len(embarcacoes[0])}\n"
            f"3: {len(embarcacoes[1])}\n"
            f"4: {len(embarcacoes[2])}\n"
            f"5: {len(embarcacoes[3])}\n")

#Essa é apenas uma variável de auxílio nas utilizações das threads
pronto.clear()

def inicio_combate(emb, jogador, ind, tab, nick):
    """
    Função para o posicionamento de embarcações dos jogadores
    :param emb: Lista com todas as embarcações
    :param jogador: Lista com os clientes conectados ao server
    :param ind: Índice da lista de clientes
    :param tab: Tabuleiro de batalha
    :param nick: Lista com os nicks escolhidos pelos jogadores
    """
    msg_privada(jogador[ind], f"{nick[ind]}, você deseja posicionar as embarcações manualmente ou de forma aleatória?\n1- Manual\n2- Aleatória")
    posi = int(dados_recebidos(jogador[ind]))
    for i in range(len(emb)):
        for j in range(len(emb[i])):
            if posi == 1:
                while True:
                    msg_privada(jogador[ind], f"{nick[ind]}, posicione a embarcação {emb[i][j]} seguindo as instruções do início do jogo")
                    x, y = map(int, dados_recebidos(jogador[ind]).split())
                    msg_privada(jogador[ind], "Selecione a horientação da embarcação\n1- Vertical\n2- Horizontal")
                    orientacao = int(dados_recebidos(jogador[ind]))
                    if orientacao == 1:
                        hor = 0
                        ver = 1
                    else:
                        hor = 1
                        ver = 0
                    if testa_pos(x, y, tab, emb[i], hor, ver):
                        pos_emb(x, y, tab, emb[i], hor, ver)
                        msg_privada(jogador[ind], f"{formar_campo(tab)}")
                        break
                    else:
                        msg_privada(jogador[ind], "Coordenada não disponível, tente novamente!")

            elif posi == 2:
                while True:
                    aleatorio_lin = randint(0, linhas)
                    aleatorio_col = randint(0, colunas)
                    orientacao_aleatoria = randint(1, 2)
                    if orientacao_aleatoria == 1:
                        hor = 0
                        ver = 1
                    else:
                        hor = 1
                        ver = 0
                    if testa_pos(aleatorio_lin, aleatorio_col, tab, emb[i], hor, ver):
                        pos_emb(aleatorio_lin, aleatorio_col, tab, emb[i], hor, ver)
                        msg_privada(jogador[ind], f"{formar_campo(tab)}")
                        break

    pronto.append(None)

#Threads para posicionamente das embarcações
combate_jogador1 = threading.Thread(target=inicio_combate, args=[embarcacoes, clientes, 0, tabu_posi[0], nick_jogadores])
combate_jogador2 = threading.Thread(target=inicio_combate, args=[embarcacoes, clientes, 1, tabu_posi[1], nick_jogadores])
combate_jogador1.start()
combate_jogador2.start()

pontos_totais = pontos(embarcacoes)
#Laço principal
while True:
    if len(pronto) == 2:
        msg_publica("Todas as embarcações foram posicionadas")
        pronto.clear()
        while True:
            for i in range(2):
                while True:
                    msg_privada(clientes[i], "Forneça a coordenada do seu tiro no formato 'linha coluna'")
                    x, y = map(int, dados_recebidos(clientes[i]).split())
                    if x < linhas and y < colunas:
                        break
                    else:
                        msg_privada(clientes[i], "Coordenada inválida, tente novamente!")

                if testa_tiro(x, y, tabu_posi[i - 1]):
                    msg_publica("Uma embarcação foi atingida")
                    troca_car(x, y, tabu_visual[i], tabu_posi[i - 1][x][y])
                    msg_privada(clientes[i-1], f"Tiro de {nick_jogadores[i]} em {x} {y} Acertou uma embarcação\n")
                    if pontos_totais == pontos_feitos(tabu_visual[i]):
                        msg_publica(f"PARABÉNS, {nick_jogadores[i]}!")
                        sleep(5)
                        pronto.append(None)
                        break
                else:
                    msg_publica(f"Tiro na água de {nick_jogadores[i]}!")
                    troca_car(x, y, tabu_visual[i], "X")
                msg_publica(f"{nick_jogadores[i]} pontos = {pontos_feitos(tabu_visual[i])}")
                msg_privada(clientes[i], formar_campo(tabu_visual[i]))
            if len(pronto) == 1:
                break
        break