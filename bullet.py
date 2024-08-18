import pygame
from settings import bullet_img, SCREEN_WIDTH
from main import enemy, enemy_group

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_group, player, enemy):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.bullet_group = bullet_group
        self.player = player
        self.enemy = enemy

    def update(self):
        # mover bala
        self.rect.x += (self.direction * self.speed)
        # verificando se a bala saiu da tela
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # verificando colisão com os personagens
        if pygame.sprite.spritecollide(self.player, self.bullet_group, False):
            if self.player.alive:
                self.player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(self.enemy, self.bullet_group, False):
                if self.enemy.alive:
                    self.enemy.health -= 25
                    self.kill()
