#Arquivo do servidor do jogo
import socket
from constantes import *

clientes = []


def fun_principal():
    """
    A função é responsável por criar um socket servidor do tipo TCP

    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        servidor.bind(("", PORTA))
        servidor.listen()
    except:
        return print("Servidor não iniciado")

    if concexao(clientes, servidor):
        msg_publica("Bem-vindos à batalha-naval!\n")


def concexao(jogadores, server):
    """
    A função testa e retorna verdadeiro quando os 2 jogadores se conectarem

    """
    while True:
        cliente, ende = server.accept()
        jogadores.append(cliente)
        if len(jogadores) == JOGADORES_PRONTOS:
            return True
        elif len(jogadores) == 1:
            msg_privada(jogadores[JOGADOR1], "Aguarde enquanto seu oponente conecta!")


def msg_publica(msg):
    """
    :param msg: Mensagem à ser enviada
    A função é responsável por enviar uma mensagem para todos os jogadores
    """
    for jogador in clientes:
        jogador.sendall(msg.encode("utf-8"))


def msg_privada(cliente, msg):
    """
    :param msg: Mensagem à ser enviada
    :param cliente: cliente à enviar os dados
    A função irá enviar uma mensagem para um determinado jogador,
    tal jogador, assim como a mensagem, serão recebidas como parâmetros da função

    """
    cliente.sendall(msg.encode("utf-8"))


def dados_recebidos(cliente):
    """
    Função responsável por receber dados dos jogadores
    :param cliente: cliente à enviar os dados
    :return: mensagem decodificada recebida do cliente
    """
    msg = cliente.recv(2048)
    return msg.decode("utf-8")