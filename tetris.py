import random
from settings import *

# Formatos das peças
FORMAS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

CORES = [
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (255, 165, 0),
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0)
]


class Peca:
    def __init__(self, x, y, forma):
        self.x = x
        self.y = y
        self.forma = forma
        self.cor = random.choice(CORES)

    def rotacionar(self):
        self.forma = [list(linha) for linha in zip(*self.forma[::-1])]


def criar_grade():
    return [[PRETO for _ in range(COLUNAS)] for _ in range(LINHAS)]


def posicao_valida(peca, grid):
    for i, linha in enumerate(peca.forma):
        for j, valor in enumerate(linha):
            if valor:
                x, y = peca.x + j, peca.y + i
                if x < 0 or x >= COLUNAS or y >= LINHAS or (y >= 0 and grid[y][x] != PRETO):
                    return False
    return True


def fundir_peca(peca, grid):
    for i, linha in enumerate(peca.forma):
        for j, valor in enumerate(linha):
            if valor:
                grid[peca.y + i][peca.x + j] = peca.cor


def remover_linhas(grid):
    linhas_removidas = 0
    for i in range(LINHAS - 1, -1, -1):
        if PRETO not in grid[i]:
            del grid[i]
            grid.insert(0, [PRETO for _ in range(COLUNAS)])
            linhas_removidas += 1
    return linhas_removidas * 10  # 10 pontos por linha
