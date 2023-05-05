import sys
import random
import pygame
from pygame.locals import *

pygame.init()

WINDOW_SIZE = (1010, 720)
GRAVITY = 0.5
GAME_SPEED = 6
background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, WINDOW_SIZE)

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('assets/bird1.png').convert_alpha(),
                                   pygame.image.load('assets/bird2.png').convert_alpha(),
                                   pygame.image.load('assets/bird3.png').convert_alpha()]

        self.current_image = 0

        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = 200 
        self.rect[1] = WINDOW_SIZE[1] / 2 - 150

        self.FLY_STRENGHT = 10
        self.height = self.FLY_STRENGHT

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        # Gravity
        self.height += GRAVITY

        # Fly
        self.rect[1] += self.height

    def fly(self):
        self.height = -self.FLY_STRENGHT

class Ground(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/ground.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = position
        self.rect[1] = WINDOW_SIZE[1] - self.rect[3]

    def update(self):
        self.rect[0] -= GAME_SPEED

        if  is_off_screen(self):
            self.rect[0] = self.rect[2]

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, position, size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/pipe.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect[0] = position

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - size)
        else:
            self.rect[1] = WINDOW_SIZE[1] - size

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

def get_random_pipes(position):
    min_pipe_height = 60
    min_gap = 150
    max_gap = 260
    ground_height = ground_group.sprites()[0].rect[3]
    game_space = WINDOW_SIZE[1] - ground_height
    gap = random.randint(min_gap, max_gap) // 2 * 2 
    pipe_size = random.randint(min_pipe_height, game_space - gap - min_pipe_height) 
    sizes = [game_space - gap - pipe_size, pipe_size]
    sizes = [[sizes[0] + ground_height, sizes[1]], [sizes[1] + ground_height, sizes[0]]]
    size = random.choice(sizes) 
    pipe = Pipe(False, position, size[0]) 
    pipe_inverted = Pipe(True, position, size[1]) 
    return (pipe, pipe_inverted)

def  is_off_screen(sprite):
    return sprite.rect[0] <= -(sprite.rect[2])

pygame.display.set_caption('Flappy Python')
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
ground1 = Ground(0)
ground2 = Ground(ground1.rect[2])
ground_group.add(ground1, ground2)

pipe_group = pygame.sprite.Group()
pipes = [get_random_pipes(1000 + 350 * i) for i in range(4)]
pipe_group.add(pipes)
 
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and GAME_SPEED != 0:
                bird.fly()

    screen.blit(background, (0, 0))

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(pipe_group.sprites()[-1].rect[0] + 350)
        pipe_group.add(pipes)

    bird_group.update()
    bird_group.draw(screen)

    pipe_group.update()
    pipe_group.draw(screen)

    ground_group.update()
    ground_group.draw(screen)

    clock.tick(60)
    pygame.display.update()

    if pygame.sprite.groupcollide(bird_group, ground_group, False, False) or pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        GAME_SPEED = 0
        GRAVITY = 0
        bird.height = 0
