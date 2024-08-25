import pygame
from config import TILE_SIZE
from soldier import Soldado

# Carregar imagens
heal_box_img = pygame.image.load('Jogo/img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('Jogo/img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('Jogo/img/icons/grenade_box.png').convert_alpha()

item_boxes = {
    'Health': heal_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img
}


class CaixaDeItem(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    
    def update(self):
        from main import player
        # verificar se o jogador pegou a caixa
        if pygame.sprite.collide_rect(self, player):
            
            # verificar o tipo da caixa
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3
            # deletar a caixa do item
            self.kill()