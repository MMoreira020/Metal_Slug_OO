import pygame

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Atirador')

# Taxa de frames
FPS = 60

# Definir variáveis do jogo
GRAVITY = 0.75
scale = 1.5
TILE_SIZE = 40

# Carregar imagens
bullet_img = pygame.image.load('Jogo/img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('Jogo/img/icons/grenade.png').convert_alpha()

# Definir cores
BG = (144, 201, 120)
RED = (255, 0, 0)
