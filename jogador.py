#Arquivo do socket cliente(jogadores)
import threading
import socket
from constantes import *


def fun_pricipal():
    """
    A função irá criar um socket cliente do tipo TCP, que nessa implementação será cada jogador
    :return:
    """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORTA))
    except:
        return print("\nNão foi possível se concectar")

    print("Jogador conectado")

    thread_1 = threading.Thread(target=receber_mensagem, args=[cliente])
    thread_2 = threading.Thread(target=enviar_mensagem, args=[cliente])

    thread_1.start()
    thread_2.start()


def receber_mensagem(cliente):
    """
    A função é resposável por receber as informações/mensagens do servidor

    """
    while True:
        try:
            mensagem = cliente.recv(2048).decode("utf-8")
            if mensagem == ENCERRAMENTO:
                cliente.close()
            else:
                print(mensagem+"\n")
        except:
            print("\nNão foi possivel manter conexão")
            print("Pressione <Enter> para continuar...")
            cliente.close()
            break


def enviar_mensagem(cliente):
    """
    A função é responsável por enviar informações do clinte(jogador) para o servidor

    """
    while True:
        try:
            mensagem = input("\n")
            cliente.send(f'{mensagem}'.encode("utf-8"))
        except:
            break


fun_pricipal()