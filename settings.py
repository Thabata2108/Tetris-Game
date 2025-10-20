import pygame

# Inicializa pygame para fontes
pygame.init()

# Configurações de tela
LARGURA_TELA = 450
ALTURA_TELA = 600
TAMANHO_BLOCO = 30
FPS = 70

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (180, 180, 180)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 200)
AMARELO = (255, 255, 0)

# Fonte padrão
FONTE = pygame.font.SysFont("tahoma", 18, bold=True)

# Dificuldades
DIFICULDADES = {
    "Fácil": 600,
    "Médio": 300,
    "Difícil": 100
}

# Tamanho do grid
COLUNAS = 15
LINHAS = 16
