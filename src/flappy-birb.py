import pygame
import random
import time
from pygame.locals import *

WIDTH = 400
HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15
GROUND_WIDTH = 2 * WIDTH
GROUND_HEIGHT= 100
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150

birb_sprite = pygame.image.load(('src/assets/birb.png'))
pipe_sprite = pygame.image.load(('src/assets/pipe-green.png'))
bg_sprite = pygame.image.load(('src/assets/background-night.png'))
ground_sprite = pygame.image.load(('src/assets/base.png'))

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = SPEED
        self.image=birb_sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH/6
        self.rect[1] = HEIGHT/6
    
    def update(self):
        self.speed += GRAVITY
        self.rect[1] += self.speed

    def bump(self):
        self.speed -= SPEED

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inv, x, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pipe_sprite.convert_alpha(),(PIPE_WIDTH,PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = x

        if inv:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bg_sprite,(GROUND_WIDTH,GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = HEIGHT-GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED


def offscreen(obj):
    return obj.rect[0]< -(obj.rect[2])

def generate_pipe(x):
    size = random.randint(100,320)
    pipe = Pipe(False,x,size)
    inv_pipe = Pipe(True,x,HEIGHT-size-PIPE_GAP)
    return pipe,inv_pipe

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))

bg = pygame.transform.scale(bg_sprite,(WIDTH,HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range (2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range (2):
    pipes = generate_pipe(WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

begin = True

while begin:
    clock.tick(15)

    for _ in pygame.event.get():
        if _.type == QUIT:
            pygame.quit()
        if _.type == KEYDOWN:
            if _.type==K_SPACE:
                bird.bump()
                begin=False
        
    screen.blit(bg,(0,0))

    if offscreen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    ground_group.update()
    bird_group.draw(screen)
    ground_group.draw(screen)
    pygame.display.update()

while True:
    clock.tick(15)

    for _ in pygame.event.get():
        if _.type == QUIT:
            pygame.quit()
        if _.type == KEYDOWN:
            if _.key == K_SPACE:
                bird.bump()

    screen.blit(bg, (0, 0))

    if offscreen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if offscreen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = generate_pipe(WIDTH* 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        time.sleep(1)
        break


