import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,  indent2))
    screen.blit(floor_surface, (floor_x_pos + screenx, indent2))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(350 * 2, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(350 * 2, random_pipe_pos - 160))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes


# ???????
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screeny:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def ummunity(last_collision_time, life_countdown):
    if pygame.time.get_ticks() - last_collision_time > 500:  # The time is in ms.
        life_countdown -= 1
        last_collision_time = pygame.time.get_ticks()
        death_sound.play()
        print(last_collision_time, life_countdown)

    return life_countdown, last_collision_time


def check_collision(pipes, life_countdown, last_collision_time):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            life_countdown, last_collision_time = ummunity(last_collision_time, life_countdown)

    if bird_rect.top <= -indent or bird_rect.bottom >= indent2:
        death_sound.play()
        life_countdown -= 1

    if life_countdown <= 0:
        return False, life_countdown, last_collision_time

    return True, life_countdown, last_collision_time


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, - bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(indent, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screenx / 2, indent - 60))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screenx / 2, indent - 60))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(screenx / 2, 425))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def create_bonus(pipes, bonuses):
    while True:
        random_bonus_pos = random.choice(bonus_height)
        random_bonus_surface = random.choice(bonuses)
        bonus = random_bonus_surface.get_rect(midtop=(350 * 2, random_bonus_pos))
        pipes_bonuses_collisions = []

        for pipe in pipes:
            pipes_bonuses_collisions.append(bonus.colliderect(pipe))
            if not True in pipes_bonuses_collisions:
                return bonuses



def move_bonuses(bonuses_list_rect):
    for bonus in bonuses_list_rect[0]:
        bonus.centerx -= 5
    return bonuses_list_rect



def draw_bonuses(bonuses, bonuses_list_rect):
    random_bonus_surface = random.choice(bonuses)
    for bonus in bonuses_list_rect:
        screen.blit(random_bonus_surface, bonus)


indent2 = 450
indent = 50 * 2
screenx = 288 * 2
screeny = 512
pygame.mixer.pre_init(frequency=44100, size=8, channels=1, buffer=1024)
pygame.init()
screen = pygame.display.set_mode((screenx, screeny))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 20)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
life_countdown = 3
invulnerability = False
last_collision_time = 0

bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())

# Floor
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
floor_x_pos = 0

# Bonuses
life_bonus_surface = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
invul_bonus_surface = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
big_bonus_surface = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
small_bonus_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bonus_height = [200, 250, 300, 350, 400]
bonuses = [life_bonus_surface, invul_bonus_surface, big_bonus_surface, small_bonus_surface]
bonus_list = []
SPAWNBONUS = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNBONUS, 2000)

# Bird
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(indent, screeny / 2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Pipes
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
SPAWNPINE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPINE, 1000)
pipe_height = [200, 300, 400]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(screenx / 2, screeny / 2))

# Sound
flap_sound = pygame.mixer.Sound('audio/sfx_wing.wav')
death_sound = pygame.mixer.Sound('audio/sfx_hit.wav')
score_sound = pygame.mixer.Sound('audio/sfx_point.wav')

score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (indent, screeny / 2)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPINE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

        if event.type == SPAWNBONUS:
            bonus_list.append(create_bonus(pipe_list, bonuses))

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        check_collision(pipe_list, life_countdown, last_collision_time)
        game_active, life_countdown, last_collision_time = check_collision(pipe_list, life_countdown, last_collision_time)
        print(life_countdown)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Bonuses
        if bonus_list:
            bonus_list = move_bonuses(bonus_list)
            draw_bonuses(bonuses, bonus_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        life_countdown = 3
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -screenx:
        floor_x_pos = 0
    screen.blit(floor_surface, (floor_x_pos, indent2))

    pygame.display.update()
    clock.tick(70)
