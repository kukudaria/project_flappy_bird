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
    pipes = [bottom_pipe, top_pipe]
    pipe = random.choice(pipes)
    return pipe


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
    return life_countdown, last_collision_time


def check_collision(pipes, life_countdown, last_collision_time):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            life_countdown, last_collision_time = ummunity(last_collision_time, life_countdown)

    if bird_rect.top <= -indent or bird_rect.bottom >= indent2 + 80:
        death_sound.play()
        life_countdown -= 1

    if life_countdown <= 0:
        return False, life_countdown, last_collision_time

    return True, life_countdown, last_collision_time


def stop_bonus(last_bonus_time, score, fake_score):
    if pygame.time.get_ticks() - last_bonus_time > 200:  # The time is in ms.
        score += 1
        fake_score += 1
        score_sound.play()
        last_bonus_time = pygame.time.get_ticks()
    return score, last_bonus_time, fake_score


def check_bon_coll(bonuses, score, last_bonus_time, fake_score):
    for bonus in bonuses:
        if bird_rect.colliderect(bonus):
            score, last_bonus_time, fake_score = stop_bonus(last_bonus_time, score, fake_score)
            bonuses.pop()
    return fake_score, score, last_bonus_time


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
            return bonus, random_bonus_surface


def move_bonuses(bonuses_list_rect):
    for bonus in bonuses_list_rect:
        bonus.centerx -= 6
    return bonuses_list_rect


def draw_bonuses(random_bonus_surface, bonuses_list_rect):
    for bonus in bonuses_list_rect:
        screen.blit(random_bonus_surface, bonus)


def life_display(game_state):
    if game_state == 'main_game':
        life_surface = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
        life_rect = life_surface.get_rect(center=(50, indent - 60))
        screen.blit(life_surface, life_rect)
        life_count_surface = game_font.render(str(int(life_countdown)), True, (255, 255, 255))
        life_count_rect = life_count_surface.get_rect(center=(80, indent - 60))
        screen.blit(life_count_surface, life_count_rect)
    if game_state == 'game_over':
        life_surface = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
        life_rect = life_surface.get_rect(center=(50, indent - 60))
        screen.blit(life_surface, life_rect)
        life_count_surface = game_font.render('0', True, (255, 255, 255))
        life_count_rect = life_count_surface.get_rect(center=(80, indent - 60))
        screen.blit(life_count_surface, life_count_rect)


def update_life_countdown(life_countdown, fake_score):
    if fake_score % 2 == 0 and fake_score != 0:
        life_countdown += 1
        life_sound.play()
        fake_score = 0
    return life_countdown, fake_score


indent2 = 450
indent = 50 * 2
screenx = 288 * 2
screeny = 512
pygame.mixer.pre_init(frequency=44100, size=8, channels=1, buffer=1024)
pygame.init()
pygame.display.set_caption('Scary Flappy Bird (Red Ver.2.0)')
screen = pygame.display.set_mode((screenx, screeny))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 20)
check_fake_score = True

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = fake_score = 0
high_score = 0
life_countdown = 5
invulnerability = False
last_collision_time = 0
last_bonus_time = 0

bg_surface = pygame.transform.scale2x(pygame.image.load('assets/cave.jpg').convert())

# Bonuses
life_bonus_surface = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
invul_bonus_surface = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
big_bonus_surface = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
small_bonus_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
heart_bonus_surface = pygame.image.load('assets/heart.png').convert_alpha()
#bonuses = [life_bonus_surface, invul_bonus_surface, big_bonus_surface, small_bonus_surface]

bonus_height = [200, 250, 300, 350, 400]
bonuses = [heart_bonus_surface]
bonus_list = []
SPAWNBONUS = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNBONUS, 5000)

# Bird
bird_downflap = pygame.image.load('assets/redbird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/redbird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(indent, screeny / 2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Pipes
pipe_surface = pygame.image.load('assets/pipe-red.png')
pipe_list = []
SPAWNPINE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPINE, 500)
pipe_height = [300, 350, 400]

# Game_over
game_over_surface = pygame.image.load('assets/game_over.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(screenx / 2, screeny / 2))

# Sound
flap_sound = pygame.mixer.Sound('audio/sfx_wing.wav')
death_sound = pygame.mixer.Sound('audio/sfx_hit.wav')
score_sound = pygame.mixer.Sound('audio/sfx_point.wav')
life_sound = pygame.mixer.Sound('audio/life_sound.wav')


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
                bonus_list.clear()
                bird_rect.center = (indent, screeny / 2)
                bird_movement = 0
                score = fake_score = 0

        if event.type == SPAWNPINE:
            pipe_list.append(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

        if event.type == SPAWNBONUS:
            bonus_rect, random_bonus_surface = create_bonus(pipe_list, bonuses)
            bonus_list.append(bonus_rect)

    screen.blit(bg_surface, (0, 0))

    if game_active:

        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        if pygame.time.get_ticks() - last_collision_time > 500:
            screen.blit(rotated_bird, bird_rect)
        elif pygame.time.get_ticks() % 3 != 0:
            screen.blit(rotated_bird, bird_rect)

        check_collision(pipe_list, life_countdown, last_collision_time)
        fake_score, score,  last_bonus_time = check_bon_coll(bonus_list, score, last_bonus_time, fake_score)
        game_active, life_countdown, last_collision_time = check_collision(pipe_list, life_countdown, last_collision_time)

        life_countdown, fake_score = update_life_countdown(life_countdown, fake_score)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Bonuses
        if bonus_list:
            bonus_list = move_bonuses(bonus_list)
            draw_bonuses(random_bonus_surface, bonus_list)

        score_display('main_game')
        life_display('main_game')

    else:
        life_countdown = 5
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
        life_display('game_over')

    pygame.display.update()
    clock.tick(70)
