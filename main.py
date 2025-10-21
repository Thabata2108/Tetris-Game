import pygame, sys, os, random
from settings import *
from game import jogar

pygame.init()
pygame.display.set_caption("Tetris – FACULTY Edition")

# === Caminhos ===
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BG_DIR = os.path.join(ASSETS_DIR, "backgrounds")

# === Inicializa tela ===
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

# === Música de fundo ===
pygame.mixer.init()
MUSIC_PATH = os.path.join(ASSETS_DIR, "music.mp3")  # coloque sua música aqui
if os.path.exists(MUSIC_PATH):
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

# === Funções ===
def carregar_background():
    arquivos = [f for f in os.listdir(BG_DIR) if f.endswith((".png", ".jpg"))]
    if not arquivos:
        return None
    img = pygame.image.load(os.path.join(BG_DIR, random.choice(arquivos)))
    return pygame.transform.scale(img, (LARGURA_TELA, ALTURA_TELA))

def desenhar_botao(texto, y):
    fonte_btn = pygame.font.SysFont("tahoma", 18, bold=True)
    largura, altura = 200, 45
    x = LARGURA_TELA // 2 - largura // 2
    ret = pygame.Rect(x, y, largura, altura)
    pygame.draw.rect(tela, PRETO, ret, border_radius=8)
    txt = fonte_btn.render(texto, True, BRANCO)
    tela.blit(txt, (x + (largura - txt.get_width()) // 2, y + (altura - txt.get_height()) // 2))
    return ret

def desenhar_instrucoes():
    fonte_info = pygame.font.SysFont("tahoma", 18)
    painel = pygame.Surface((150, 90), pygame.SRCALPHA)
    painel.fill((0, 0, 0, 120))
    pygame.draw.rect(painel, BRANCO, painel.get_rect(), width=2, border_radius=0)
    texto1 = fonte_info.render("\u2190 \u2192  Mover", True, BRANCO)
    texto2 = fonte_info.render("   \u2191     Girar", True, BRANCO)
    texto3 = fonte_info.render("   \u2193     Acelerar", True, BRANCO)
    painel.blit(texto1, (20, 10))
    painel.blit(texto2, (20, 35))
    painel.blit(texto3, (20, 60))
    tela.blit(painel, (LARGURA_TELA//2 - 180, ALTURA_TELA - 100))

def menu():
    pygame.mixer.music.play(-1)  # garante que reinicie no menu
    bg_img = carregar_background()
    dificuldade = "Médio"
    clock = pygame.time.Clock()
    
    while True:
        tela.blit(bg_img, (0, 0)) if bg_img else tela.fill((220, 220, 220))
        titulo = pygame.font.SysFont("tahoma", 36, bold=True).render("TETRIS FACULTY", True, PRETO)
        tela.blit(titulo, (LARGURA_TELA//2 - titulo.get_width()//2, 80))
        
        botao_jogar = desenhar_botao("JOGAR", 200)
        botao_dif = desenhar_botao(f"DIFICULDADE: {dificuldade}", 270)
        botao_sair = desenhar_botao("SAIR", 340)
        desenhar_instrucoes()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    jogar(tela, bg_img, DIFICULDADES[dificuldade])
                elif botao_dif.collidepoint(evento.pos):
                    chaves = list(DIFICULDADES.keys())
                    dificuldade = chaves[(chaves.index(dificuldade) + 1) % len(chaves)]
                elif botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    menu()
