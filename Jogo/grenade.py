import pygame
from config import GRAVITY, TILE_SIZE, grenade_img, explosion_group, enemy_group, SCREEN_WIDTH
from explosion import Explosao

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction 
    
    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed 
        dy = self.vel_y
        
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0
        
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed
            
        self.rect.x += dx
        self.rect.y += dy
        
        # Contador
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosao(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            
            # Importar o player aqui para evitar a importação circular
            from main import player
            
            # Verificação de proximidade com o jogador
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                    player.health -= 50
    
            # Verificação de proximidade com os inimigos
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                        enemy.health -= 50
                        

