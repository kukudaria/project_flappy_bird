import pygame
import sys


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,  450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('assets/background-day.png').convert()

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_rect = bird_surface.get_rect(center=(50, 256))

gravity = 0.25
bird_movement = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12

    screen.blit(bg_surface, (0, 0))
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
    screen.blit(floor_surface, (floor_x_pos, 450))

    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)

    pygame.display.update()
    clock.tick(120)
