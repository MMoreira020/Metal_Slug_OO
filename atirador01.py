import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Atirador')

class Soldado(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Jogo/img/player/Idle/0.png')
        self.igm = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.igm.get_rect()
        self.rect.center = (x, y)
    
    def desenhar(self):
        screen.blit(self.igm, self.rect)


player = Soldado(200, 200, 3)
player2 = Soldado(400, 200, 3)

run = True
while run:
    
    player.desenhar()
    player2.desenhar()
    
    for event in pygame.event.get():
        # sair game
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()
            
pygame.quit()
