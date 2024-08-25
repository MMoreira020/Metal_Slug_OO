import pygame
import sys
from config import screen, clock, FPS, enemy_group, bullet_group, grenade_group, explosion_group, shoot, grenade, grenade_thrown, moving_left, moving_right, item_box_group, font, WHITE, bullet_img, grenade_img
from utils import draw_bg, draw_text
from soldier import Soldado
from enemy import Inimigo
from bullet import Bullet
from grenade import Grenade
from itembox import CaixaDeItem
from barra_de_saude import HealthBar

# Caixas de itens
item_box = CaixaDeItem('Health', 100, 260)
item_box_group.add(item_box)
item_box = CaixaDeItem('Ammo', 400, 260)
item_box_group.add(item_box)
item_box = CaixaDeItem('Grenade', 500, 260)
item_box_group.add(item_box)


player = Soldado('player', 200, 200, 1.65, 5, 20, 5)
health_bar = HealthBar(10, 10, player.health, player.health)

enemy = Inimigo(500, 200, 1.65, 2, 20, 0)  
enemy2 = Inimigo(300, 200, 1.65, 2, 20, 0)
enemy_group.add(enemy)
enemy_group.add(enemy2)


run = True
while run:
    
    clock.tick(FPS)
    
    draw_bg()
    # mostar cura do jogador
    health_bar.draw(player.health)
    # mostrar munição
    draw_text(f'AMMO: ', font, WHITE, 10, 35)
    for x in range(player.ammo):
        screen.blit(bullet_img, (90 + (x * 10), 40))
    # mostrar granada
    draw_text(f'GRENADES: ', font, WHITE, 10, 60)
    for x in range(player.grenades):
        screen.blit(grenade_img, (135 + (x * 15), 60))
    
    player.update()
    player.desenhar()
   
    for enemy in enemy_group: 
        enemy.ai()
        enemy.update()
        enemy.desenhar()

    # Atualizar e desenhar grupos
    bullet_group.update()
    grenade_group.update()
    explosion_group.update()
    item_box_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)
    item_box_group.draw(screen)
    
    # Atualiza as ações do jogador
    if player.alive:
        # Atirar balas
        if shoot:
            player.shoot()
        # Lançar granadas
        elif grenade and not grenade_thrown and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), 
                              player.rect.top, player.direction)
            grenade_group.add(grenade)
            # Reduzir granadas
            player.grenades -= 1
            grenade_thrown = True          
        if player.in_air:
            player.update_action(2)  # 2: Pular
        elif moving_left or moving_right:
            player.update_action(1)  # 1: correr
        else:
            player.update_action(0)  # 0: ocioso
        player.move(moving_left, moving_right)
    
    # Capturar eventos
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
sys.exit()
