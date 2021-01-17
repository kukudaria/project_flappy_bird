import pygame
import sys
import random


class Field:

    def __init__(self, screenx, screeny, bg_image, gravity, life_countdown, game_over_image, life_surface_image, indent, game_font):
        self.screenx = screenx
        self.screeny = screeny
        self.gravity = gravity
        self.indent = indent
        self.game_font = game_font
        self.life_countdown = life_countdown
        self.screen = pygame.display.set_mode((self.screenx, self.screeny))
        self.bg_surface = pygame.transform.scale2x(pygame.image.load(bg_image).convert())
        self.game_over_surface = pygame.image.load(game_over_image).convert_alpha()
        self.game_over_rect = self.game_over_surface.get_rect(center=(self.screenx // 2, self.screeny // 2))
        self.life_surface = pygame.image.load(life_surface_image).convert_alpha()
        self.life_rect = self.life_surface.get_rect(center=(50, self.indent - 60))
        self.life_count_surface = self.game_font.render(str(int(self.life_countdown)), True, (255, 255, 255))
        self.life_count_rect = self.life_count_surface.get_rect(center=(80, self.indent - 60))
        self.score = 0
        self.high_score = 0
        self.score_surface = self.game_font.render(str(int(self.score)), True, (255, 255, 255))
        self.score_rect = self.score_surface.get_rect(center=(self.screenx // 2, self.indent - 60))
        self.pipe_list = []
        self.bonus_list = []

    def fill(self):
        self.screen.blit(self.bg_surface, (0, 0))

    def draw_score(self):
        self.screen.blit(self.life_surface, self.life_rect)
        self.screen.blit(self.life_count_surface, self.life_count_rect)
        self.screen.blit(self.score_surface, self.score_rect)

    def update(self):
        pygame.display.update()

    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.screen.blit(self.game_over_surface, self.game_over_rect)
        self.score_surface = self.game_font.render(str(int(self.score)), True, (255, 255, 255))
        self.score_rect = self.score_surface.get_rect(center=(screenx // 2, indent - 60))
        self.screen.blit(self.score_surface, self.score_rect)

        high_score_surface = self.game_font.render(f'High score: {int(self.high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(self.screenx // 2, 425))
        self.screen.blit(high_score_surface, high_score_rect)


class Pipe:

    def __init__(self, pipe_image, pipe_height):
        self.pipe_surface = pygame.image.load(pipe_image)
        self.pipe_height = pipe_height
        self.random_pipe_pos = random.choice(self.pipe_height)
        self.bottom_pipe = self.pipe_surface.get_rect(midtop=(350 * 2, self.random_pipe_pos))
        self.top_pipe = self.pipe_surface.get_rect(midbottom=(350 * 2, self.random_pipe_pos - 160))
        self.pipes = [self.bottom_pipe, self.top_pipe]
        self.pipe = random.choice(self.pipes)

    def move(self):
        self.pipe.centerx -= 4

    def draw(self, field):
        if self.pipe.bottom >= field.screeny:
            field.screen.blit(self.pipe_surface, self.pipe)
        else:
            self.flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
            field.screen.blit(self.flip_pipe, self.pipe)


class Bird:

    def __init__(self, bird_downflap_image, bird_midflap_image, bird_upflap_image, indent, indent2, field):
        self.bird_downflap = pygame.image.load(bird_downflap_image).convert_alpha()
        self.bird_midflap = pygame.image.load(bird_midflap_image).convert_alpha()
        self.bird_upflap = pygame.image.load(bird_upflap_image).convert_alpha()
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_index = 0
        self.bird_movement = 0
        self.indent = indent
        self.indent2 = indent2
        self.last_collision_time = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(self.indent, field.screeny // 2))

    def rotate_bird(self):
        self.bird_surface = pygame.transform.rotozoom(self.bird_surface, - self.bird_movement * 3, 1)

    def bird_animation(self):
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(self.indent, self.bird_rect.centery))

    def change_movement(self):
        self.bird_movement = -6

    def flap(self):
        if self.bird_index < 2:
            self.bird_index += 1
        else:
            self.bird_index = 0

    def move(self, field):
        self.bird_movement += field.gravity
        self.bird_surface_new = pygame.transform.rotozoom(self.bird_surface, - self.bird_movement * 3, 1)
        self.bird_rect.centery += self.bird_movement

    def draw(self, field):
        if pygame.time.get_ticks() - self.last_collision_time > 500:
            field.screen.blit(self.bird_surface_new, self.bird_rect)
        elif pygame.time.get_ticks() % 3 != 0:
            field.screen.blit(self.bird_surface_new, self.bird_rect)

    def check_collision(self, field, death_sound):
        if self.bird_rect.collidelist([pipe.pipe for pipe in field.pipe_list]) != -1:
            if pygame.time.get_ticks() - self.last_collision_time > 500:
                field.life_countdown -= 1
                field.life_count_surface = field.game_font.render(str(int(field.life_countdown)), True, (255, 255, 255))
                death_sound.play()
                self.last_collision_time = pygame.time.get_ticks()

        if self.bird_rect.top <= -10 or self.bird_rect.bottom >= self.indent2 + 80:
            field.life_countdown = 0
            field.life_count_surface = field.game_font.render(str(int(field.life_countdown)), True, (255, 255, 255))
            death_sound.play()

    def check_bon_coll(self, field, score_sound, life_sound):
        index = self.bird_rect.collidelist([bonus.heart_bonus_rect for bonus in field.bonus_list])
        if index != -1:
            field.bonus_list.pop(index)
            score_sound.play()
            field.score += 1
            field.score_surface = field.game_font.render(str(int(field.score)), True, (255, 255, 255))
            field.score_rect = field.score_surface.get_rect(center=(field.screenx // 2, field.indent - 60))
            if field.score % 5 == 0:
                field.life_countdown += 1
                field.life_count_surface = field.game_font.render(str(int(field.life_countdown)), True, (255, 255, 255))
                life_sound.play()


class Bonus:

    def __init__(self, heart_bonus_surface_image, bonus_height):
        self.bonus_height = bonus_height
        self.random_bonus_pos = random.choice(self.bonus_height)
        self.heart_bonus_surface = pygame.image.load(heart_bonus_surface_image).convert_alpha()
        self.heart_bonus_rect = self.heart_bonus_surface.get_rect(midtop=(350 * 2, self.random_bonus_pos))

    def move(self):
        self.heart_bonus_rect.centerx += -6

    def draw(self, field):
        field.screen.blit(self.heart_bonus_surface, self.heart_bonus_rect)


if __name__ == '__main__':
    pygame.mixer.pre_init(frequency=44100, size=8, channels=1, buffer=1024)
    pygame.init()
    pygame.display.set_caption('Scary Flappy Bird (Red Ver.2.0)')
    game_font = pygame.font.Font('04B_19.TTF', 20)
    indent2 = 450
    indent = 50 * 2
    screenx = 288 * 2
    screeny = 512
    gravity = 0.25
    fps = 70
    life_countdown = 5
    flap_sound = pygame.mixer.Sound('audio/sfx_wing.wav')
    death_sound = pygame.mixer.Sound('audio/sfx_hit.wav')
    score_sound = pygame.mixer.Sound('audio/sfx_point.wav')
    life_sound = pygame.mixer.Sound('audio/life_sound.wav')
    bg_image = 'assets/cave.jpg'
    pipe_image = 'assets/pipe-red.png'
    bird_downflap_image = 'assets/redbird-downflap.png'
    bird_midflap_image = life_surface_image = 'assets/redbird-midflap.png'
    bird_upflap_image = 'assets/redbird-upflap.png'
    game_over_image = 'assets/game_over.png'
    heart_bonus_surface_image = 'assets/heart.png'
    pipe_height = [300, 350, 400]
    bonus_height = [200, 250, 300, 350, 400]
    field = Field(screenx, screeny, bg_image, gravity, life_countdown, game_over_image, life_surface_image, indent, game_font)
    bird = Bird(bird_downflap_image, bird_midflap_image, bird_upflap_image, indent, indent2, field)
    SPAWNPINE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPINE, 500)
    BIRDFLAP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRDFLAP, 200)
    SPAWNBONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWNBONUS, 5000)
    game_active = True
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird.change_movement()
                    flap_sound.play()

                if event.key == pygame.K_SPACE and game_active is False:
                    game_active = True
                    field.life_countdown = 5
                    field.life_count_surface = field.game_font.render(str(int(field.life_countdown)), True, (255, 255, 255))
                    field.pipe_list.clear()
                    field.bonus_list.clear()
                    bird.bird_rect.center = (indent, screeny // 2)
                    bird.bird_movement = 0
                    field.score = 0
                    field.score_surface = field.game_font.render(str(int(field.score)), True, (255, 255, 255))

            if event.type == BIRDFLAP:
                bird.flap()
                bird.bird_animation()

            if event.type == SPAWNPINE:
                field.pipe_list.append(Pipe(pipe_image, pipe_height))

            if event.type == SPAWNBONUS:
                field.bonus_list.append(Bonus(heart_bonus_surface_image, bonus_height))

        field.fill()
        if game_active:
            bird.move(field)
            bird.draw(field)

            for pipe in field.pipe_list:
                pipe.move()
                pipe.draw(field)

            for bonus in field.bonus_list:
                bonus.move()
                bonus.draw(field)

            field.draw_score()

            bird.check_collision(field, death_sound)
            bird.check_bon_coll(field, score_sound, life_sound)
            if field.life_countdown <= 0:
                game_active = False

        else:
            field.game_over()

        field.update()
        clock.tick(fps)
