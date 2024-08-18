import pygame
from settings import screen, FPS
from utils import draw_bg
from player import Soldado
from bullet import Bullet
from grenade import Grenade
from explosão import Explosion

pygame.init()
clock = pygame.time.Clock()

# Inicializar variáveis do jogo
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# Criar grupos de sprites
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# Criar instâncias de personagens
player = Soldado('player', 200, 200, 3, 5, 20, 5)
enemy = Soldado('enemy', 400, 200, 3, 5, 20, 0)
enemy_group.add(enemy)

run = True
while run:
    clock.tick(FPS)
    draw_bg()

    player.update()
    player.desenhar()

    enemy.update()
    enemy.desenhar()

    # Atualizar e desenhar grupos
    bullet_group.update()
    grenade_group.update()
    explosion_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)

    # Atualiza as ações do jogador
    if player.alive:
        # Atirar balas
        if shoot:
            player.shoot(bullet_group, enemy)
        # Lançar granadas
        elif grenade and not grenade_thrown and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), 
                              player.rect.top, player.direction)
            grenade_group.add(grenade)
            player.grenades -= 1
            grenade_thrown = True

        if player.in_air:
            player.update_action(2)  # Pular
        elif moving_left or moving_right:
            player.update_action(1)  # Correr
        else:
            player.update_action(0)  # Ocioso
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        # Sair do jogo
        if event.type == pygame.QUIT:
            run = False
        # Teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

        # Mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Botão direito do mouse
                pass
            if event.button == 1:  # Botão esquerdo do mouse
                shoot = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botão esquerdo do mouse
                shoot = False

    pygame.display.update()

pygame.quit()
