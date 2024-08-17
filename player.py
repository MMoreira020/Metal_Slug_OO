import pygame
import os
from settings import GRAVITY, bullet_img, screen
from bullet import Bullet

class Soldado(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start = ammo
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
        
        # Carregar todas imagens do jogador
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # Redefinir lista temporária de imagens
            temp_list = []
            # Conta o número de arquivos na pasta
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
        # redefinir variáveis de movimento 
        dx = 0
        dy = 0
        # Movimentando para esquerda ou direita
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        
        # pular
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        # Aplicar gravidade
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        
        # Verificar colisão com o piso
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
        
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self, bullet_group, enemy):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction),
                            self.rect.centery, self.direction, bullet_group, self, enemy)
            bullet_group.add(bullet)
            self.ammo -= 1

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
