import pygame

# Inicializar Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Atirador')

# Taxa de frames
clock = pygame.time.Clock()
FPS = 60

# Definir variáveis do jogo
GRAVITY = 0.75
TILE_SIZE = 40

# Inicializar variáveis de controle
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# Carregar imagens
# bala
bullet_img = pygame.image.load('Jogo/img/icons/bullet.png').convert_alpha()
# granada
grenade_img = pygame.image.load('Jogo/img/icons/grenade.png').convert_alpha()

# definir fonte
font = pygame.font.SysFont('Futura', 30)


# Definir cores
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Grupos de sprites
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
