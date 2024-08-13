import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Atirador')

# Taxa de frames
clock = pygame.time.Clock()
FPS = 60

# Definir variáveis do jogo
GRAVITY = 0.75
# Ação do jogador
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# Carregar imagens
# Bala
bullet_img = pygame.image.load('Jogo/img/icons/bullet.png').convert_alpha()
# Granada
grenade_img = pygame.image.load('Jogo/img/icons/grenade.png').convert_alpha()

# Definir cores
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

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
        
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self):
        # mover bala
        self.rect.x += (self.direction * self.speed)
        # verificando se a bala saiu da tela
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        # verificando colisão com os caracteres
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 25
                self.kill()
            
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction 
    
    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed 
        dy = self.vel_y
        
        # Verificar colisão com o piso
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0
        
        # verifica a colisão com as paredes
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            
        # atualizar pos da granada
        self.rect.x += dx
        self.rect.y += dy       
        
# grupo de sprites
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()

        
player = Soldado('player', 200, 200, 3, 5, 20, 5)
enemy = Soldado('enemy', 400, 200, 3, 5, 20, 0)

run = True
while run:
    
    clock.tick(FPS)
    
    draw_bg()
    
    player.update()
    player.desenhar()
    
    enemy.update()
    enemy.desenhar()

    #atualizar e desenhar grupos
    bullet_group.update()
    grenade_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    
    # Atualiza as ações do jogador
    if player.alive:
        # Atirar balas
        if shoot:
            player.shoot()
        # lançar granadas
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), \
                        player.rect.top, player.direction)
            grenade_group.add(grenade)
            # Reduzir grandas
            player.grenades -= 1
            grenade_thrown = True          
        if player.in_air:
            player.update_action(2) #2: Pular
        elif moving_left or moving_right:
            player.update_action(1) #1: correr
        else:
            player.update_action(0) #0: ocioso
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
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
                
    # mouse
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:  # Botão direito do mouse
            pass
        if event.button == 1:  # Botão esquerdo do mouse
            shoot = True
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:  # Botão esquerdo do mouse
            shoot = False
            
    pygame.display.update()
            
pygame.quit()
