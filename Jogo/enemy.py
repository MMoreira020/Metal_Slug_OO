from soldier import Soldado
import pygame
import random
from config import TILE_SIZE

class Inimigo(Soldado):
    def __init__(self, x, y, scale, speed, ammo, grenades):
        super().__init__('enemy', x, y, scale, speed, ammo, grenades)
        self.marcha = False
        self.marcha_lenta = 0
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)

    def ai(self):
        from main import player
        if self.alive and player.alive:
            if self.marcha == False and random.randint(1, 200) == 1:
                self.update_action(0)  # 0 ocioso
                self.marcha = True
                self.marcha_lenta = 50
            # verificar se a IA está perto do jogador
            if self.vision.colliderect(player.rect):
                # parar de correr e enfrentar o jogador
                self.update_action(0)  # 0 ocioso
                # atirar
                self.shoot()
            else:
                if not self.marcha:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False 
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # 1 correr
                    self.move_counter += 1
                    # atualizar a visão da IA conforme o inimigo se move
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.marcha_lenta -= 1
                    if self.marcha_lenta <= 0:
                        self.marcha = False
