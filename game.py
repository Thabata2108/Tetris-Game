import pygame, sys, random
from settings import *
from tetris import *

OFFSET_Y = 117  # distância em pixels do topo da tela


def tela_game_over(tela, bg_img, pontuacao, velocidade_queda):
    """Exibe a tela de Game Over com opções."""
    pygame.mixer.music.pause()
    clock = pygame.time.Clock()
    fonte_titulo = pygame.font.SysFont("tahoma", 48, bold=True)
    fonte_pontuacao = pygame.font.SysFont("tahoma", 24, bold=True)
    fonte_botao = pygame.font.SysFont("tahoma", 22, bold=True)

    while True:
        tela.blit(bg_img, (0, 0))

        # Texto "GAME OVER"
        titulo = fonte_titulo.render("GAME OVER", True, BRANCO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 150))

        # Pontuação final
        texto_pontos = fonte_pontuacao.render(f"Sua pontuação: {pontuacao}", True, BRANCO)
        tela.blit(texto_pontos, (LARGURA_TELA // 2 - texto_pontos.get_width() // 2, 230))

        # Botões
        largura_botao, altura_botao = 200, 45
        espacamento = 20
        x = LARGURA_TELA // 2 - largura_botao // 2

        botao_reiniciar = pygame.Rect(x, 320, largura_botao, altura_botao)
        botao_menu = pygame.Rect(x, 320 + altura_botao + espacamento, largura_botao, altura_botao)

        mouse_pos = pygame.mouse.get_pos()

        # Efeitos de hover
        cor_reiniciar = (220, 220, 220) if botao_reiniciar.collidepoint(mouse_pos) else BRANCO
        cor_menu = (220, 220, 220) if botao_menu.collidepoint(mouse_pos) else BRANCO

        # Desenhar botões
        pygame.draw.rect(tela, cor_reiniciar, botao_reiniciar, border_radius=8)
        pygame.draw.rect(tela, cor_menu, botao_menu, border_radius=8)

        txt_reiniciar = fonte_botao.render("Reiniciar", True, PRETO)
        txt_menu = fonte_botao.render("Voltar ao Menu", True, PRETO)

        tela.blit(txt_reiniciar, (botao_reiniciar.centerx - txt_reiniciar.get_width() // 2,
                                  botao_reiniciar.centery - txt_reiniciar.get_height() // 2))
        tela.blit(txt_menu, (botao_menu.centerx - txt_menu.get_width() // 2,
                             botao_menu.centery - txt_menu.get_height() // 2))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_reiniciar.collidepoint(evento.pos):
                    pygame.mixer.music.unpause() 
                    return "reiniciar"
                elif botao_menu.collidepoint(evento.pos):
                    pygame.mixer.music.unpause()
                    return "menu"

        pygame.display.update()
        clock.tick(30)


def jogar(tela, bg_img, velocidade_queda):
    clock = pygame.time.Clock()
    grid = criar_grade()
    peca_atual = Peca(COLUNAS // 2 - 2, 0, random.choice(FORMAS))
    proxima_peca = Peca(COLUNAS // 2 - 2, 0, random.choice(FORMAS))
    tempo_queda = 0
    pontuacao = 0
    rodando = True

    while rodando:
        tela.blit(bg_img, (0, 0))
        tempo_queda += clock.get_rawtime()
        clock.tick(FPS)

        # Cabeçalho superior
        espacamento_topo = 20
        espacamento_lateral = 20

        # Texto de pontuação (lado esquerdo)
        texto_pont = FONTE.render(f"Pontos: {pontuacao}", True, BRANCO)
        tela.blit(texto_pont, (espacamento_lateral, espacamento_topo))

        # Botão voltar (lado direito)
        largura_botao = 110
        altura_botao = 35
        voltar_rect = pygame.Rect(
            LARGURA_TELA - largura_botao - espacamento_lateral,
            espacamento_topo - 5,
            largura_botao,
            altura_botao
        )

        # Efeito hover
        mouse_pos = pygame.mouse.get_pos()
        cor_botao = (220, 220, 220) if voltar_rect.collidepoint(mouse_pos) else BRANCO
        pygame.draw.rect(tela, cor_botao, voltar_rect, border_radius=8)

        voltar_txt = FONTE.render("Voltar", True, PRETO)
        tela.blit(
            voltar_txt,
            (
                voltar_rect.centerx - voltar_txt.get_width() // 2,
                voltar_rect.centery - voltar_txt.get_height() // 2
            )
        )

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and voltar_rect.collidepoint(evento.pos):
                return  # volta ao menu
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    peca_atual.x -= 1
                    if not posicao_valida(peca_atual, grid):
                        peca_atual.x += 1
                elif evento.key == pygame.K_RIGHT:
                    peca_atual.x += 1
                    if not posicao_valida(peca_atual, grid):
                        peca_atual.x -= 1
                elif evento.key == pygame.K_DOWN:
                    peca_atual.y += 1
                    if not posicao_valida(peca_atual, grid):
                        peca_atual.y -= 1
                elif evento.key == pygame.K_UP:
                    peca_atual.rotacionar()
                    if not posicao_valida(peca_atual, grid):
                        peca_atual.rotacionar()

        # Queda automática
        if tempo_queda > velocidade_queda:
            peca_atual.y += 1
            if not posicao_valida(peca_atual, grid):
                peca_atual.y -= 1
                fundir_peca(peca_atual, grid)
                pontuacao += remover_linhas(grid)
                peca_atual = proxima_peca
                proxima_peca = Peca(COLUNAS // 2 - 2, 0, random.choice(FORMAS))
                if not posicao_valida(peca_atual, grid):
                    pygame.time.wait(500)
                    acao = tela_game_over(tela, bg_img, pontuacao, velocidade_queda)
                    if acao == "reiniciar":
                        jogar(tela, bg_img, velocidade_queda)
                    return  # volta ao menu depois de reiniciar ou sair
            tempo_queda = 0

        # Desenhar blocos da grade
        for i in range(LINHAS):
            for j in range(COLUNAS):
                pygame.draw.rect(
                    tela,
                    grid[i][j],
                    (j * TAMANHO_BLOCO, i * TAMANHO_BLOCO + OFFSET_Y, TAMANHO_BLOCO - 1, TAMANHO_BLOCO - 1)
                )

        # Desenhar peça atual
        for i, linha in enumerate(peca_atual.forma):
            for j, valor in enumerate(linha):
                if valor:
                    pygame.draw.rect(
                        tela,
                        peca_atual.cor,
                        (
                            (peca_atual.x + j) * TAMANHO_BLOCO,
                            (peca_atual.y + i) * TAMANHO_BLOCO + OFFSET_Y,
                            TAMANHO_BLOCO - 1,
                            TAMANHO_BLOCO - 1
                        )
                    )

        # Atualiza a tela
        pygame.display.update()
