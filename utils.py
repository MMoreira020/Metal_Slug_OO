from settings import screen, BG, RED, SCREEN_WIDTH
import pygame

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
