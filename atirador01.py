import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Atirador')

# Taxa de frames
clock = pygame.time.Clock()
FPS = 60
# Ação do jogador
moving_left = False
moving_right = False

# Definir cores
BG = (144, 201, 120)

def draw_bg():
    screen.fill(BG)
    

class Soldado(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'Jogo/img/{self.char_type}/Idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)    
            
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'Jogo/img/{self.char_type}/Run/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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
        
        self.rect.x += dx
        self.rect.y += dy
    
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
            self.frame_index = 0        
        
        
    
    def desenhar(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Soldado('player', 200, 200, 3, 5)
enemy = Soldado('enemy', 400, 200, 3, 5)

run = True
while run:
    
    clock.tick(FPS)
    
    draw_bg()
    
    player.update_animation()
    
    player.desenhar()
    enemy.desenhar()
 
    player.move(moving_left, moving_right)
    
    for event in pygame.event.get():
        # sair game
        if event.type == pygame.QUIT:
            run = False
        # teclado 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            
    pygame.display.update()
            
pygame.quit()
