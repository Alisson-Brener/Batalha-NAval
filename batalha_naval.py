#Este arquivo é responsável pelas funções de lógica do jogo

def campo_de_batalha(lin, col):
    """
    A função irá criar um tabuleiro na forma de uma lista 2x2
    :param lin: Nº de linhas do tabuleiro
    :param col: Nº de colunas do tabuleiro
    :return: Uma lista 2x2
    """
    tab = []
    for i in range(lin):
        tab.append([])
        for j in range(col):
            tab[i].append("*")
    return tab


def formar_campo(tab):
    """
    Transforma o tabuleiro em uma string para a impressão
    :param tab: Tabuleiro(lista 2x2)
    :return: O tabuleiro em forma de string pronto para a impressão
    """
    campo = ""
    lin = len(tab)
    col = len(tab[0])
    for i in range(lin):
        if i == 0:
            for k in range(col):
                if k == 0:
                    campo += "/  " + "0  "
                else:
                    campo += str(k)
                    if k + 1 < col:
                        if k > 9:
                            campo += " "
                        else:
                            campo += "  "
                    else:
                        campo += "\n\n"
        for j in range(col):
            if j == 0:
                if i < 10:
                    campo += str(i) + "  "
                else:
                    campo += str(i) + " "
            campo += tab[i][j]
            if j+1 < col:
                campo += "  "
            else:
                campo += "\n"
    return campo


def adicionar_embarcacoes(adc, emb):
    """
    A função irá adicionar embarcações conforme o tamanho do tabuleiro
    :param adc: Um inteiro com a quantidade de embarcações a ser adicionada
    :param emb: Lista de embarcações
    """
    for i in range(adc):
        emb[i % 4].append(emb[i % 4][0])


def testa_pos(x, y, tab, num_emb, hor, ver):
    """
    A função fará a verificação da possibilidade da embarcação ser posicionada em determinada coordenada
    :param x: Inteiro com a linha do tabuleiro
    :param y: Inteiro com a Coluna do tabuleiro
    :param tab: Tabuleiro
    :param num_emb: Classe da embarcação
    :param hor: Representa a orientação de posicionamento da embarcação
    :param ver: Representa a orientação de posicionamento da embarcação
    :return: Caso não haja problemas com a coordenada passada, retornará verdadeiro, caso contrário retornará falso
    """
    for k in range(int(num_emb[0])):
        try:
            if tab[x+(k*ver)][y+(k*hor)] != "*":
                return False
        except IndexError:
            return False
        #Teste aos arredores
        try:
            if tab[x+(k*ver)-1][y+(k*hor)] != "*" and tab[x+(k*ver)-1][y+(k*hor)] != "@" and x+(k*ver)-1 >= 0:
                return False
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)+1][y+(k*hor)] != "*" and tab[x+(k*ver)+1][y+(k*hor)] != "@":
                return False
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)][y+(k*hor)-1] != "*" and tab[x+(k*ver)][y+(k*hor)-1] != "@" and y+(k*hor)-1 >= 0:
                return False
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)][y+(k*hor)+1] != "*" and tab[x+(k*ver)][y+(k*hor)+1] != "@":
                return False
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)-1][y+(k*hor)+1] != "*" and tab[x+(k*ver)-1][y+(k*hor)+1] != "@" and x+(k*ver)-1 >= 0:
                return False
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)-1][y+(k*hor)-1] != "*" and tab[x+(k*ver)-1][y+(k*hor)-1] != "@" and x+(k*ver)-1 >= 0 and y+(k*hor)-1 >= 0:
                return False
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)+1][y+(k*hor)+1] != "*" and tab[x+(k*ver)+1][y+(k*hor)+1] != "@":
                return False
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)+1][y+(k*hor)-1] != "*" and tab[x+(k*ver)+1][y+(k*hor)-1] != "@" and y+(k*hor)-1 >= 0:
                return False
        except IndexError:
            pass

    return True


def pos_emb(x, y, tab, num_emb, hor, ver):
    """
    Posicionará a embarcação caso a coordenada apresentada seja aceita
    :param x: Inteiro com a linha do tabuleiro
    :param y: Inteiro com a Coluna do tabuleiro
    :param tab: Tabuleiro
    :param num_emb: Classe da embarcação
    :param hor: Representa a orientação de posicionamento da embarcação
    :param ver: Representa a orientação de posicionamento da embarcação
    """
    for k in range(int(num_emb[0])):
        tab[x + (k * ver)][y + (k * hor)] = num_emb[0]
        try:
            if tab[x + (k * ver) - 1][y + (k * hor)] == "*" and x+(k*ver)-1 >= 0:
                tab[x + (k * ver) - 1][y + (k * hor)] = "@"
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)+1][y+(k*hor)] == "*":
                tab[x+(k*ver)+1][y+(k*hor)] = "@"
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)][y+(k*hor)-1] == "*" and y+(k*hor)-1 >= 0:
                tab[x+(k*ver)][y+(k*hor)-1] = "@"
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)][y+(k*hor)+1] == "*":
                tab[x+(k*ver)][y+(k*hor)+1] = "@"
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)-1][y+(k*hor)+1] == "*" and x+(k*ver)-1 >= 0:
                tab[x+(k*ver)-1][y+(k*hor)+1] = "@"
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)-1][y+(k*hor)-1] == "*" and x+(k*ver)-1 >= 0 and y+(k*hor)-1 >= 0:
                tab[x+(k*ver)-1][y+(k*hor)-1] = "@"
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)+1][y+(k*hor)+1] == "*":
                tab[x+(k*ver)+1][y+(k*hor)+1] = "@"
        except IndexError:
            pass
        try:
            if tab[x+(k*ver)+1][y+(k*hor)-1] == "*" and y+(k*hor)-1 >= 0:
                tab[x + (k * ver) + 1][y + (k * hor) - 1] = "@"
        except IndexError:
            pass


def testa_tiro(x, y, tabu):
    """
    A função irá testar se o tiro atingiu água ou uma embarcação
    :param x: linha
    :param y: coluna
    :param tabu: tabuleiro
    :return: verdadeiro caso acerte uma embarcação, falso caso contrário
    """
    if tabu[x][y] != "*" and tabu[x][y] != "X" and tabu[x][y] != "@":
        return True
    return False


def troca_car(x, y, tabu, car):
    """
    A função fará a troca do caractere dependendo do resultado do tiro dado
    :param x: linha
    :param y: coluna
    :param tabu: tabuleiro
    :param car: caractere substituto
    """
    tabu[x][y] = car


def pontos(emb):
    """
    Retorno da quantidade de pontos feitos para que a partida seja vencida
    :param emb: lista de embarcações
    :return: pontos a serem feitos
    """
    return len(emb[0]) * 2 + len(emb[1]) * 3 + len(emb[2]) * 4 + len(emb[3]) * 5


def pontos_feitos(tabu):
    """
    A função contará a quantidade de pontos atuais do jogador
    :param tabu: tabuleiro
    :return: pontos atuais do jogador
    """
    pts_feitos = 0
    for i in range(len(tabu)):
        for j in range(len(tabu[0])):
            if tabu[i][j] != "X" and tabu[i][j] != "*":
                pts_feitos += 1
    return pts_feitos