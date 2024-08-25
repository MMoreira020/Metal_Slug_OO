import pygame
import os
from config import GRAVITY, bullet_group, screen, RED, TILE_SIZE
from bullet import Bullet
import random

class Soldado(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0 
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # variáveis específicas de Ia
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.marcha = False
        self.marcha_lenta = 0
        
        # Carregar todas imagens do jogador
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'Jogo/img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'Jogo/img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)    

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        # Aplicar gravidade
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        
        # Verificar colisão com o piso
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
        
        self.rect.x += dx
        self.rect.y += dy
        
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
    
        
    def ai(self):
        from main import player  
        if self.alive and player.alive:
            if self.marcha == False and random.randint(1, 200) == 1:
                self.update_action(0) #0 ocioso
                self.marcha = True
                self.marcha_lenta = 50
            # verificar se a Ia esta perto do jogador
            if self.vision.colliderect(player.rect):
                # parar de correr e enfrentar o jogador
                self.update_action(0) # 0 correr
                # atirar
                self.shoot()
            else:
                if self.marcha == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False 
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) #1 correr
                    self.move_counter += 1
                    # atualizar a visão de IA conforme o nimigo se move
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.marcha_lenta -= 1
                    if self.marcha_lenta <= 0:
                        self.marcha = False
                
            
    def update_animation(self):
        # Animação de atualização
        ANIMATION_COOLDOWN = 100
        # atualizar imagem depedendo do quadro atual
        self.image = self.animation_list[self.action][self.frame_index]
        # Verificar se passou tempo suficiente desde a última atualização
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # se a animação acabar, a redefinição volta ao início
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0           

    def update_action(self, new_action):
        # A nova ação é diferenten da anterior 
        if new_action != self.action:
            self.action = new_action
            # Atualizar as configurações de animação
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()  
    
    def check_alive(self):
           if self.health <= 0:
               self.health = 0
               self.speed = 0
               self.alive = False
               self.update_action(3)
    
    def desenhar(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
